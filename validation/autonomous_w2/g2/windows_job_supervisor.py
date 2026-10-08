"""Windows Job Object process-tree guard used by the prepared G2 R6 stage."""
from __future__ import annotations

import ctypes
import hashlib
import os
import subprocess
import threading
import time
from dataclasses import dataclass
from typing import Mapping, Sequence

if os.name == "nt":
    from ctypes import wintypes

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
else:  # Keep fixture/helper imports possible on non-Windows; execution fails closed.
    wintypes = None  # type: ignore[assignment]
    _kernel32 = None


CREATE_SUSPENDED = 0x00000004
CREATE_BREAKAWAY_FROM_JOB = 0x01000000
JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION = 1
JOB_OBJECT_LIMIT_JOB_TIME = 0x00000004
JOB_OBJECT_LIMIT_ACTIVE_PROCESS = 0x00000008
JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100
JOB_OBJECT_LIMIT_JOB_MEMORY = 0x00000200
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
EXIT_WALL_LIMIT = 0xE0010001
EXIT_OUTPUT_LIMIT = 0xE0010002
EXIT_STAGE_WALL_LIMIT = 0xE0010003
EXIT_CPU_LIMIT = 0xE0010004
TICKS_PER_SECOND = 10_000_000


class JobGuardError(RuntimeError):
    """Raised when a Windows Job Object cannot be installed or controlled."""


class _IoCounters(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_uint64),
        ("WriteOperationCount", ctypes.c_uint64),
        ("OtherOperationCount", ctypes.c_uint64),
        ("ReadTransferCount", ctypes.c_uint64),
        ("WriteTransferCount", ctypes.c_uint64),
        ("OtherTransferCount", ctypes.c_uint64),
    ]


class _BasicLimitInformation(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", wintypes.DWORD if wintypes else ctypes.c_uint32),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD if wintypes else ctypes.c_uint32),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD if wintypes else ctypes.c_uint32),
        ("SchedulingClass", wintypes.DWORD if wintypes else ctypes.c_uint32),
    ]


class _ExtendedLimitInformation(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", _BasicLimitInformation),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class _BasicAccountingInformation(ctypes.Structure):
    _fields_ = [
        ("TotalUserTime", ctypes.c_int64),
        ("TotalKernelTime", ctypes.c_int64),
        ("ThisPeriodTotalUserTime", ctypes.c_int64),
        # The x64 Windows 11 ABI reserves one 64-bit slot after the time fields.
        ("_abi_padding_before_counts", ctypes.c_uint64),
        ("TotalPageFaultCount", ctypes.c_uint32),
        ("TotalProcesses", ctypes.c_uint32),
        ("ActiveProcesses", ctypes.c_uint32),
        ("TotalTerminatedProcesses", ctypes.c_uint32),
    ]


class _ThreadEntry32(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_uint32),
        ("cntUsage", ctypes.c_uint32),
        ("th32ThreadID", ctypes.c_uint32),
        ("th32OwnerProcessID", ctypes.c_uint32),
        ("tpBasePri", ctypes.c_int32),
        ("tpDeltaPri", ctypes.c_int32),
        ("dwFlags", ctypes.c_uint32),
    ]


def _win_error(where: str) -> JobGuardError:
    return JobGuardError(f"{where}: {ctypes.WinError(ctypes.get_last_error())}")


def _configure_api() -> None:
    if _kernel32 is None:
        raise JobGuardError("WINDOWS_JOB_OBJECT_REQUIRED")
    _kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    _kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    _kernel32.SetInformationJobObject.argtypes = [wintypes.HANDLE, wintypes.INT, ctypes.c_void_p, wintypes.DWORD]
    _kernel32.SetInformationJobObject.restype = wintypes.BOOL
    _kernel32.QueryInformationJobObject.argtypes = [wintypes.HANDLE, wintypes.INT, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    _kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    _kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    _kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    _kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
    _kernel32.ResumeThread.restype = wintypes.DWORD
    _kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _kernel32.TerminateJobObject.restype = wintypes.BOOL
    _kernel32.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
    _kernel32.IsProcessInJob.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    _kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    _kernel32.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ThreadEntry32)]
    _kernel32.Thread32First.restype = wintypes.BOOL
    _kernel32.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ThreadEntry32)]
    _kernel32.Thread32Next.restype = wintypes.BOOL
    _kernel32.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenThread.restype = wintypes.HANDLE


@dataclass(frozen=True)
class StreamEvidence:
    prefix: bytes
    bytes_observed: int
    sha256_observed: str
    overflow: bool
    drain_stopped_on_overflow: bool


@dataclass(frozen=True)
class BoundedProcessResult:
    status: str
    termination_reason: str | None
    returncode: int | None
    pid: int | None
    process_assigned_before_resume: bool
    process_in_job: bool
    elapsed_seconds: float
    stdout: StreamEvidence
    stderr: StreamEvidence
    job_total_user_time_100ns: int
    job_total_kernel_time_100ns: int
    job_peak_memory_bytes: int
    job_total_processes: int
    job_active_processes_at_read: int
    job_terminated_processes: int
    stdin_error: str | None


class _BoundedDrain:
    def __init__(self, pipe, limit: int, overflow_event: threading.Event) -> None:
        self.pipe = pipe
        self.limit = limit
        self.overflow_event = overflow_event
        self.prefix = bytearray()
        self.total = 0
        self.digest = hashlib.sha256()
        self.thread = threading.Thread(target=self._run, name="r6-bounded-pipe-drain", daemon=True)

    def start(self) -> None:
        self.thread.start()

    def _run(self) -> None:
        try:
            while True:
                block = self.pipe.read(65536)
                if not block:
                    return
                self.total += len(block)
                remaining = self.limit - len(self.prefix)
                if remaining > 0:
                    retained = block[:remaining]
                    self.prefix.extend(retained)
                    self.digest.update(retained)
                if self.total > self.limit:
                    self.overflow_event.set()
                    # Stop draining after the first crossing block. The child
                    # then blocks on the finite OS pipe buffer until its Job is
                    # terminated; memory/hash work do not scale with extra output.
                    return
        except (OSError, ValueError):
            return

    def evidence(self) -> StreamEvidence:
        return StreamEvidence(
            bytes(self.prefix), self.total, self.digest.hexdigest(), self.total > self.limit, self.total > self.limit,
        )


def _create_job(*, wall_seconds: float, cpu_seconds: float | None, memory_bytes: int | None, max_processes: int):
    _configure_api()
    job = _kernel32.CreateJobObjectW(None, None)
    if not job:
        raise _win_error("CreateJobObjectW")
    info = _ExtendedLimitInformation()
    flags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE | JOB_OBJECT_LIMIT_ACTIVE_PROCESS
    if cpu_seconds is not None:
        flags |= JOB_OBJECT_LIMIT_JOB_TIME
        info.BasicLimitInformation.PerJobUserTimeLimit = int(cpu_seconds * TICKS_PER_SECOND)
    if memory_bytes is not None:
        flags |= JOB_OBJECT_LIMIT_PROCESS_MEMORY | JOB_OBJECT_LIMIT_JOB_MEMORY
        info.ProcessMemoryLimit = memory_bytes
        info.JobMemoryLimit = memory_bytes
    info.BasicLimitInformation.LimitFlags = flags
    info.BasicLimitInformation.ActiveProcessLimit = max_processes
    if not _kernel32.SetInformationJobObject(job, JOB_OBJECT_EXTENDED_LIMIT_INFORMATION, ctypes.byref(info), ctypes.sizeof(info)):
        error = _win_error("SetInformationJobObject")
        _kernel32.CloseHandle(job)
        raise error
    return job


def _is_process_in_job(process_handle: int, job) -> bool:
    answer = wintypes.BOOL()
    if not _kernel32.IsProcessInJob(wintypes.HANDLE(process_handle), job, ctypes.byref(answer)):
        raise _win_error("IsProcessInJob")
    return bool(answer.value)


def _resume_suspended_primary_thread(pid: int) -> None:
    """Reopen Popen's initially suspended primary thread by Toolhelp thread inventory."""
    snapshot = _kernel32.CreateToolhelp32Snapshot(0x00000004, 0)
    invalid_handle_value = ctypes.c_void_p(-1).value
    if not snapshot or snapshot == invalid_handle_value:
        raise _win_error("CreateToolhelp32Snapshot(threads)")
    thread_handle = None
    try:
        entry = _ThreadEntry32()
        entry.dwSize = ctypes.sizeof(entry)
        found_tid = None
        has_entry = _kernel32.Thread32First(snapshot, ctypes.byref(entry))
        while has_entry:
            if entry.th32OwnerProcessID == pid:
                found_tid = entry.th32ThreadID
                break
            entry.dwSize = ctypes.sizeof(entry)
            has_entry = _kernel32.Thread32Next(snapshot, ctypes.byref(entry))
        if found_tid is None:
            raise JobGuardError(f"SUSPENDED_PRIMARY_THREAD_NOT_FOUND:{pid}")
        thread_handle = _kernel32.OpenThread(0x0002, False, found_tid)  # THREAD_SUSPEND_RESUME
        if not thread_handle:
            raise _win_error("OpenThread(primary)")
        resume_result = _kernel32.ResumeThread(thread_handle)
        if resume_result == 0xFFFFFFFF:
            raise _win_error("ResumeThread(primary)")
        if resume_result != 1:
            raise JobGuardError(f"UNEXPECTED_INITIAL_SUSPEND_COUNT:{resume_result}")
    finally:
        if thread_handle:
            _kernel32.CloseHandle(thread_handle)
        _kernel32.CloseHandle(snapshot)


def _query_job(job) -> tuple[int, int, int, int, int, int]:
    accounting = _BasicAccountingInformation()
    returned = wintypes.DWORD()
    if not _kernel32.QueryInformationJobObject(
        job, JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION, ctypes.byref(accounting), ctypes.sizeof(accounting), ctypes.byref(returned),
    ):
        raise _win_error("QueryInformationJobObject(accounting)")
    extended = _ExtendedLimitInformation()
    if not _kernel32.QueryInformationJobObject(
        job, JOB_OBJECT_EXTENDED_LIMIT_INFORMATION, ctypes.byref(extended), ctypes.sizeof(extended), ctypes.byref(returned),
    ):
        raise _win_error("QueryInformationJobObject(extended)")
    return (
        accounting.TotalUserTime, accounting.TotalKernelTime, extended.PeakJobMemoryUsed,
        accounting.TotalProcesses, accounting.ActiveProcesses, accounting.TotalTerminatedProcesses,
    )


def terminate_job(job, exit_code: int = EXIT_WALL_LIMIT) -> None:
    """Terminate all current members; failure is surfaced instead of falling back to process-only kill."""
    if not _kernel32.TerminateJobObject(job, exit_code):
        raise _win_error("TerminateJobObject")


def run_bounded_process(
    command: Sequence[str],
    *,
    cwd: str | os.PathLike[str],
    stdin_bytes: bytes = b"",
    wall_seconds: float,
    cpu_seconds: float | None,
    memory_bytes: int | None,
    max_processes: int,
    stdout_limit_bytes: int,
    stderr_limit_bytes: int,
    environment: Mapping[str, str] | None = None,
) -> BoundedProcessResult:
    """Run one fixed child, assigned while suspended, with bounded streams and kill-on-close job."""
    if os.name != "nt":
        raise JobGuardError("WINDOWS_JOB_OBJECT_REQUIRED")
    if not command or any(not isinstance(part, str) for part in command):
        raise ValueError("COMMAND_MUST_BE_A_NONEMPTY_STRING_SEQUENCE")
    if wall_seconds <= 0 or max_processes < 1 or min(stdout_limit_bytes, stderr_limit_bytes) < 0:
        raise ValueError("INVALID_RESOURCE_LIMIT")
    started = time.monotonic()
    job = _create_job(wall_seconds=wall_seconds, cpu_seconds=cpu_seconds, memory_bytes=memory_bytes, max_processes=max_processes)
    process: subprocess.Popen[bytes] | None = None
    overflow = threading.Event()
    stdout_drain: _BoundedDrain | None = None
    stderr_drain: _BoundedDrain | None = None
    writer_error: list[str] = []
    assigned = False
    in_job = False
    reason: str | None = None
    try:
        flags = CREATE_SUSPENDED
        process = subprocess.Popen(
            list(command), cwd=os.fspath(cwd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=False, close_fds=True, creationflags=flags, env=dict(environment) if environment is not None else None,
        )
        handle = int(process._handle)  # subprocess' Windows process HANDLE; assignment must precede ResumeThread.
        if not _kernel32.AssignProcessToJobObject(job, wintypes.HANDLE(handle)):
            raise _win_error("AssignProcessToJobObject")
        assigned = True
        in_job = _is_process_in_job(handle, job)
        if not in_job:
            raise JobGuardError("PROCESS_NOT_IN_ASSIGNED_JOB")
        stdout_drain = _BoundedDrain(process.stdout, stdout_limit_bytes, overflow)
        stderr_drain = _BoundedDrain(process.stderr, stderr_limit_bytes, overflow)
        stdout_drain.start()
        stderr_drain.start()

        _resume_suspended_primary_thread(process.pid)

        def write_stdin() -> None:
            assert process is not None and process.stdin is not None
            try:
                process.stdin.write(stdin_bytes)
                process.stdin.flush()
            except (BrokenPipeError, OSError, ValueError) as exc:
                writer_error.append(f"{type(exc).__name__}:{exc}")
            finally:
                try:
                    process.stdin.close()
                except OSError:
                    pass

        writer = threading.Thread(target=write_stdin, name="r6-bounded-stdin-writer", daemon=True)
        writer.start()
        deadline = started + wall_seconds
        next_cpu_check = started
        while process.poll() is None:
            if overflow.is_set():
                reason = "STDOUT_OR_STDERR_LIMIT"
                terminate_job(job, EXIT_OUTPUT_LIMIT)
                break
            now = time.monotonic()
            if cpu_seconds is not None and now >= next_cpu_check:
                observed_user_time = _query_job(job)[0]
                if observed_user_time >= int(cpu_seconds * TICKS_PER_SECOND):
                    reason = "CPU_LIMIT"
                    terminate_job(job, EXIT_CPU_LIMIT)
                    break
                next_cpu_check = now + 0.005
            if now >= deadline:
                reason = "WALL_LIMIT"
                terminate_job(job, EXIT_WALL_LIMIT)
                break
            time.sleep(0.005)
        try:
            process.wait(timeout=max(1.0, wall_seconds))
        except subprocess.TimeoutExpired:
            reason = reason or "JOB_TERMINATION_DID_NOT_COMPLETE"
            terminate_job(job, EXIT_WALL_LIMIT)
            process.wait(timeout=2.0)
        writer.join(timeout=2.0)
        stdout_drain.thread.join(timeout=3.0)
        stderr_drain.thread.join(timeout=3.0)
        if stdout_drain.thread.is_alive() or stderr_drain.thread.is_alive():
            raise JobGuardError("PIPE_DRAIN_DID_NOT_JOIN_AFTER_JOB_TERMINATION")
        user_time, kernel_time, peak_memory, total_proc, active_proc, terminated_proc = _query_job(job)
        if reason is None and cpu_seconds is not None and process.returncode not in (0, None):
            cap_ticks = int(cpu_seconds * TICKS_PER_SECOND)
            if user_time >= cap_ticks:
                reason = "CPU_LIMIT"
        if reason is None and (stdout_drain.evidence().overflow or stderr_drain.evidence().overflow):
            reason = "STDOUT_OR_STDERR_LIMIT"
        if reason is None and process.returncode not in (0, None) and terminated_proc > 0:
            reason = "JOB_LIMIT_OR_CHILD_FAILURE"
        status = "COMPLETED" if reason is None and process.returncode == 0 else (reason or "NONZERO_EXIT")
        return BoundedProcessResult(
            status=status, termination_reason=reason, returncode=process.returncode, pid=process.pid,
            process_assigned_before_resume=assigned, process_in_job=in_job,
            elapsed_seconds=time.monotonic() - started,
            stdout=stdout_drain.evidence(), stderr=stderr_drain.evidence(),
            job_total_user_time_100ns=user_time, job_total_kernel_time_100ns=kernel_time,
            job_peak_memory_bytes=peak_memory, job_total_processes=total_proc,
            job_active_processes_at_read=active_proc, job_terminated_processes=terminated_proc,
            stdin_error=writer_error[0] if writer_error else None,
        )
    except BaseException:
        if process is not None and process.poll() is None:
            try:
                terminate_job(job, EXIT_WALL_LIMIT)
            except BaseException:
                pass
            # The child might still be suspended and not yet assigned to this Job.
            try:
                _kernel32.TerminateProcess(wintypes.HANDLE(int(process._handle)), EXIT_WALL_LIMIT)
            except BaseException:
                pass
            try:
                process.wait(timeout=2.0)
            except BaseException:
                pass
        raise
    finally:
        if process is not None:
            for pipe in (process.stdin, process.stdout, process.stderr):
                if pipe is not None:
                    try:
                        pipe.close()
                    except OSError:
                        pass
        if job:
            _kernel32.CloseHandle(job)  # KILL_ON_JOB_CLOSE is the final cleanup guard.


def result_to_json(result: BoundedProcessResult) -> dict[str, object]:
    """Serialize bounded process evidence without losing stream hashes or observed counts."""
    import base64

    return {
        "status": result.status,
        "termination_reason": result.termination_reason,
        "returncode": result.returncode,
        "pid": result.pid,
        "process_assigned_before_resume": result.process_assigned_before_resume,
        "process_in_job": result.process_in_job,
        "elapsed_seconds_display_only": round(result.elapsed_seconds, 6),
        "stdout": {
            "prefix_base64": base64.b64encode(result.stdout.prefix).decode("ascii"),
            "bytes_observed": result.stdout.bytes_observed,
            "sha256_retained_prefix": result.stdout.sha256_observed,
            "overflow": result.stdout.overflow,
            "drain_stopped_on_overflow": result.stdout.drain_stopped_on_overflow,
        },
        "stderr": {
            "prefix_base64": base64.b64encode(result.stderr.prefix).decode("ascii"),
            "bytes_observed": result.stderr.bytes_observed,
            "sha256_retained_prefix": result.stderr.sha256_observed,
            "overflow": result.stderr.overflow,
            "drain_stopped_on_overflow": result.stderr.drain_stopped_on_overflow,
        },
        "job": {
            "total_user_time_100ns": result.job_total_user_time_100ns,
            "total_kernel_time_100ns": result.job_total_kernel_time_100ns,
            "peak_memory_bytes": result.job_peak_memory_bytes,
            "total_processes": result.job_total_processes,
            "active_processes_at_read": result.job_active_processes_at_read,
            "terminated_processes": result.job_terminated_processes,
        },
        "stdin_error": result.stdin_error,
    }
