"""Windows Job Object guard for each R4 worker process (memory plus hard timeout)."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import subprocess
import sys
import time
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
JOB_OBJECT_LIMIT_ACTIVE_PROCESS = 0x00000008
JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
CREATE_SUSPENDED = 0x00000004


class _JobBasicLimitInformation(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class _IoCounters(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_ulonglong),
        ("WriteOperationCount", ctypes.c_ulonglong),
        ("OtherOperationCount", ctypes.c_ulonglong),
        ("ReadTransferCount", ctypes.c_ulonglong),
        ("WriteTransferCount", ctypes.c_ulonglong),
        ("OtherTransferCount", ctypes.c_ulonglong),
    ]


class _JobExtendedLimitInformation(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", _JobBasicLimitInformation),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


def _sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _api() -> tuple[Any, Any]:
    if os.name != "nt":
        raise RuntimeError("R4 resource enforcement requires Windows Job Objects")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    ntdll = ctypes.WinDLL("ntdll", use_last_error=True)
    ntdll.NtResumeProcess.argtypes = [wintypes.HANDLE]
    ntdll.NtResumeProcess.restype = wintypes.LONG
    return kernel32, ntdll


def _make_job(limit_bytes: int) -> tuple[Any, _JobExtendedLimitInformation]:
    kernel32, _ = _api()
    handle = kernel32.CreateJobObjectW(None, None)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    info = _JobExtendedLimitInformation()
    info.BasicLimitInformation.LimitFlags = (
        JOB_OBJECT_LIMIT_PROCESS_MEMORY
        | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        | JOB_OBJECT_LIMIT_ACTIVE_PROCESS
    )
    info.BasicLimitInformation.ActiveProcessLimit = 1
    info.ProcessMemoryLimit = limit_bytes
    if not kernel32.SetInformationJobObject(
        handle, JOB_OBJECT_EXTENDED_LIMIT_INFORMATION, ctypes.byref(info), ctypes.sizeof(info),
    ):
        error = ctypes.get_last_error()
        kernel32.CloseHandle(handle)
        raise ctypes.WinError(error)
    return handle, info


def _query_peak(handle: Any) -> tuple[int, int]:
    kernel32, _ = _api()
    info = _JobExtendedLimitInformation()
    returned = wintypes.DWORD(0)
    if not kernel32.QueryInformationJobObject(
        handle, JOB_OBJECT_EXTENDED_LIMIT_INFORMATION, ctypes.byref(info), ctypes.sizeof(info), ctypes.byref(returned),
    ):
        raise ctypes.WinError(ctypes.get_last_error())
    return int(info.PeakProcessMemoryUsed), int(info.ProcessMemoryLimit)


def _run_guarded(
    *, command: list[str], project: Path, memory_limit_mib: int, timeout_seconds: int,
    stdout_path: Path, probe_allocation_mib: int | None = None,
) -> dict[str, Any]:
    if memory_limit_mib < 1 or timeout_seconds < 1:
        raise ValueError("memory and wall caps must be positive")
    limit_bytes = memory_limit_mib * 1024 * 1024
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    started_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    start = time.monotonic()
    job, _configured = _make_job(limit_bytes)
    log = stdout_path.open("wb")
    process = None
    assigned_before_resume = False
    timed_out = False
    setup_error: str | None = None
    peak_bytes = 0
    configured_bytes = limit_bytes
    exit_code: int | None = None
    try:
        process = subprocess.Popen(
            command,
            cwd=project,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            creationflags=CREATE_SUSPENDED,
            close_fds=True,
        )
        kernel32, ntdll = _api()
        if not kernel32.AssignProcessToJobObject(job, wintypes.HANDLE(int(process._handle))):
            setup_error = f"AssignProcessToJobObject failed: {ctypes.WinError(ctypes.get_last_error())}"
            process.kill()
            process.wait()
        else:
            assigned_before_resume = True
            # subprocess.Popen closes the primary thread handle after launch;
            # NtResumeProcess resumes the still-suspended single-process job
            # member only after its Job Object limits have been installed.
            resume_status = int(ntdll.NtResumeProcess(wintypes.HANDLE(int(process._handle))))
            if resume_status != 0:
                setup_error = f"NtResumeProcess failed with NTSTATUS 0x{resume_status & 0xffffffff:08x}"
                kernel32.TerminateJobObject(job, 0xE0000002)
                process.wait()
            else:
                deadline = start + timeout_seconds
                while process.poll() is None:
                    if time.monotonic() >= deadline:
                        timed_out = True
                        kernel32.TerminateJobObject(job, 0xE0000001)
                        break
                    time.sleep(0.025)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    kernel32.TerminateJobObject(job, 0xE0000003)
                    process.wait(timeout=5)
                exit_code = process.returncode
        peak_bytes, configured_bytes = _query_peak(job)
    finally:
        log.flush()
        log.close()
        if process is not None and process.poll() is None:
            kernel32, _ = _api()
            kernel32.TerminateJobObject(job, 0xE0000004)
            process.wait()
        kernel32, _ = _api()
        kernel32.CloseHandle(job)

    elapsed = time.monotonic() - start
    log_bytes = stdout_path.read_bytes() if stdout_path.exists() else b""
    return {
        "schema": "ddwmr-g4-auer-windows-job-guard-record-v1",
        "status": "GUARD_SETUP_FAILURE" if setup_error else ("TIMEOUT" if timed_out else "PROCESS_EXITED"),
        "started_utc": started_utc,
        "elapsed_wall_seconds": elapsed,
        "timeout_seconds": timeout_seconds,
        "memory_limit_mib": memory_limit_mib,
        "memory_limit_bytes": limit_bytes,
        "job_process_memory_limit_bytes_reported": configured_bytes,
        "peak_process_memory_bytes_reported_by_job": peak_bytes,
        "process_memory_cap_installed": configured_bytes == limit_bytes,
        "worker_created_suspended_and_assigned_before_resume": assigned_before_resume,
        "timeout_terminated_job": timed_out,
        "worker_exit_code": exit_code,
        "worker_setup_error": setup_error,
        "worker_stdout_path": str(stdout_path),
        "worker_stdout_sha256": hashlib.sha256(log_bytes).hexdigest(),
        "worker_stdout_bytes": len(log_bytes),
        "command": command,
        "probe_requested_allocation_mib": probe_allocation_mib,
        "probe_enforcement_verified": (
            probe_allocation_mib is not None
            and exit_code not in (None, 0)
            and not timed_out
            and peak_bytes >= int(limit_bytes * 0.75)
            and peak_bytes <= limit_bytes
            and b'"memory_probe": "limit_reached"' in log_bytes
            and b'"allocation_error": "MemoryError"' in log_bytes
        ) if probe_allocation_mib is not None else None,
    }


def _strict_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--case", choices=("analytic", "ddwmr"))
    parser.add_argument("--snapshot-manifest-sha256")
    parser.add_argument("--proof-output", type=Path)
    parser.add_argument("--evidence-output", type=Path)
    parser.add_argument("--guard-output", type=Path, required=True)
    parser.add_argument("--stdout-output", type=Path, required=True)
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--probe-limit-mib", type=int, default=64)
    parser.add_argument("--probe-allocation-mib", type=int, default=256)
    args = parser.parse_args()
    project = args.project.resolve()
    if args.probe:
        worker_command = [sys.executable, "-m", "validation.baselines.auer2013.r4_worker", "--memory-probe-mib", str(args.probe_allocation_mib)]
        result = _run_guarded(
            command=worker_command, project=project, memory_limit_mib=args.probe_limit_mib,
            timeout_seconds=30, stdout_path=args.stdout_output.resolve(),
            probe_allocation_mib=args.probe_allocation_mib,
        )
        result["test_limit_isolated_from_frozen_ivp_profile"] = True
    else:
        if not all((args.profile, args.case, args.snapshot_manifest_sha256, args.proof_output, args.evidence_output)):
            parser.error("normal runs require profile, case, snapshot hash, proof and evidence output")
        profile_path = args.profile.resolve()
        profile = _strict_json(profile_path)
        memory = profile["memory_enforcement"]
        if memory.get("platform") != "Windows" or memory.get("mechanism") is None:
            raise SystemExit("frozen profile does not specify an enforceable Windows memory guard")
        worker_command = [
            sys.executable, "-m", "validation.baselines.auer2013.r4_worker",
            "--case", args.case,
            "--snapshot-manifest-sha256", args.snapshot_manifest_sha256,
            "--proof-output", str(args.proof_output.resolve()),
            "--evidence-output", str(args.evidence_output.resolve()),
        ]
        result = _run_guarded(
            command=worker_command, project=project,
            memory_limit_mib=int(profile["memory_limit_mib_per_ivp"]),
            timeout_seconds=int(profile["wall_time_seconds_per_ivp"]),
            stdout_path=args.stdout_output.resolve(),
        )
        result["profile_path"] = str(profile_path)
        result["profile_sha256"] = _sha256(profile_path)
        result["process_guard_mechanism"] = memory["mechanism"]
    result["guard_runner_source_sha256"] = _sha256(Path(__file__).resolve())
    output = args.guard_output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": result["status"],
        "exit_code": result.get("worker_exit_code"),
        "peak_process_memory_bytes": result.get("peak_process_memory_bytes_reported_by_job"),
        "probe_enforcement_verified": result.get("probe_enforcement_verified"),
        "guard_record": str(output),
    }, sort_keys=True))
    if result.get("status") == "GUARD_SETUP_FAILURE":
        return 21
    if result.get("status") == "TIMEOUT":
        return 10
    if args.probe:
        return 0 if result.get("probe_enforcement_verified") else 22
    return int(result.get("worker_exit_code") or 0)


if __name__ == "__main__":
    raise SystemExit(main())
