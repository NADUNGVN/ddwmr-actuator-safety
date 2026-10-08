"""Create a new, isolated v3 namespace from the audited v2 task inputs."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from validation.autonomous_w2.g4.preflight_mapping_v2 import ROOT

OLD_PLAN = Path("research/autonomous_w2/g4/matched_v6_task_development_v2")
NEW_PLAN = Path("research/autonomous_w2/g4/matched_v6_task_development_v3")
RESULT = Path("results/validation/autonomous_w2/g4/matched_v6_task_development_v3")


def sha(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return hashlib.sha256(candidate.read_bytes()).hexdigest()


def dump(path: Path, value: Any) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8")


def replace_value(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [replace_value(item, replacements) for item in value]
    if isinstance(value, dict):
        return {
            replace_value(key, replacements) if isinstance(key, str) else key: replace_value(item, replacements)
            for key, item in value.items()
        }
    return value


def load(rel: Path) -> Any:
    raw = (ROOT / rel).read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig"
    return json.loads(raw.decode(encoding))


def build() -> dict[str, Any]:
    source_plan = ROOT / OLD_PLAN
    target_plan = ROOT / NEW_PLAN
    target_plan.mkdir(parents=True, exist_ok=True)
    result_root = ROOT / RESULT
    result_root.mkdir(parents=True, exist_ok=True)
    repl = {
        OLD_PLAN.as_posix(): NEW_PLAN.as_posix(),
        "protocol_v2.json": "protocol_v3.json",
        "benchmark_v2.json": "benchmark_v3.json",
        "auer_input_manifest_v2.json": "auer_input_manifest_v3.json",
        "auer_bindings_v2.json": "auer_bindings_v3.json",
        "auer_profile_v2.json": "auer_profile_v3.json",
        "common_profile_v2.json": "common_profile_v3.json",
        "native_source_snapshot_v2.json": "native_source_snapshot_v3.json",
        "freeze_manifest_v3.json": "freeze_manifest_v4.json",
        "freeze_receipt_v3.json": "freeze_receipt_v4.json",
        "source_closure_v3.json": "source_closure_v4.json",
        "binding_preflight_v4.json": "binding_preflight_v5.json",
        "mapping_preflight_v3.json": "mapping_preflight_v4.json",
        "v6_w2_worker_v2": "v6_w2_worker_v3",
        "auer_w2_worker_v2": "auer_w2_worker_v3",
        "v6_w2_adapter_v2": "v6_w2_adapter_v3",
        "auer_w2_adapter_v2": "auer_w2_adapter_v3",
        "matched_v6_common_v2": "matched_v6_common_v3",
        "v6_snapshot_v2": "v6_snapshot_v3",
        "auer_snapshot_v2": "auer_snapshot_v3",
        "run_matched_v6_w2_v2": "run_matched_v6_w2_v3",
        "windows_job_supervisor_v2": "windows_job_supervisor_v3",
    }

    # Carry only the frozen candidate inputs forward. Old results/receipts are
    # not copied or rewritten; historical proof rows remain at their G2 paths.
    names = (
        "protocol_v2.json", "benchmark_v2.json", "auer_input_manifest_v2.json",
        "auer_bindings_v2.json", "auer_profile_v2.json", "common_profile_v2.json",
        "g2_profile_centered_v6.json", "g2_release_v6.json", "g2_task_protocol_v1.json",
        "native_source_snapshot_v2.json",
    )
    for name in names:
        value = load(OLD_PLAN / name)
        value = replace_value(value, repl)
        out_name = name
        for old, new in repl.items():
            out_name = out_name.replace(old, new)
        if name == "protocol_v2.json":
            value["schema"] = "ddwmr-g4-w2-matched-v6-task-protocol-v3"
            value["candidate_version"] = "matched_v6_task_development_v3"
        if name == "benchmark_v2.json":
            value["schema"] = "ddwmr-g4-w2-matched-v6-benchmark-v3"
        if name == "auer_input_manifest_v2.json":
            value["schema"] = "ddwmr-g4-w2-auer-input-manifest-v3"
        if name == "auer_bindings_v2.json":
            value["schema"] = "ddwmr-g4-w2-auer-native-bindings-v3"
        if name == "native_source_snapshot_v2.json":
            value["schema"] = "ddwmr-g4-w2-native-source-snapshot-map-v3"
        if name == "prepare_output_v2.json":
            value["schema"] = "ddwmr-g4-w2-matched-candidate-build-v3"
        dump(NEW_PLAN / out_name, value)

    for old_id, new_id in (("auer_native_inputs", "auer_native_inputs"), ("v6_bindings", "v6_bindings")):
        src = source_plan / old_id
        dst = target_plan / new_id
        shutil.copytree(src, dst, dirs_exist_ok=True)
    for file in (target_plan / "v6_bindings").glob("*.json"):
        value = json.loads(file.read_text(encoding="utf-8"))
        value = replace_value(value, repl)
        value["binding_path"] = (NEW_PLAN / "v6_bindings" / file.name).as_posix()
        value["protocol_path"] = (NEW_PLAN / "g2_task_protocol_v1.json").as_posix()
        value["profile_path"] = (NEW_PLAN / "g2_profile_centered_v6.json").as_posix()
        value["result_root"] = (RESULT / "v6" / f"{int(file.stem):02d}_{value['comparison_id']}").as_posix()
        value["w2_wrapper_snapshot"] = "validation/autonomous_w2/g4/v6_snapshot_v3"
        # Fresh path/hash pairs for the exact byte-identical peer rows.
        value["source_files"][value["peer_saved_row_path"]] = value["peer_saved_row_sha256"]
        value["source_files"][value["core_binding_path"]] = value["core_binding_sha256"]
        dump(NEW_PLAN / "v6_bindings" / file.name, value)

    # Copy source snapshots into new immutable module namespaces. Auer's two
    # internal package imports are the only scientific-module text adaptation.
    for old_dir, new_dir in (("v6_snapshot_v2", "v6_snapshot_v3"), ("auer_snapshot_v2", "auer_snapshot_v3")):
        shutil.copytree(ROOT / "validation/autonomous_w2/g4" / old_dir,
                        ROOT / "validation/autonomous_w2/g4" / new_dir, dirs_exist_ok=True)
    solver = ROOT / "validation/autonomous_w2/g4/auer_snapshot_v3/solver_r9_w2.py"
    solver.write_text(solver.read_text(encoding="utf-8").replace("auer_snapshot_v2", "auer_snapshot_v3"), encoding="utf-8")

    # Bind native Auer cases and bindings to the new candidate-local copies.
    manifest_path = NEW_PLAN / "auer_input_manifest_v3.json"
    manifest = load(manifest_path)
    for item in manifest["cases"]:
        item["native_case_path"] = item["native_case_path"].replace(OLD_PLAN.as_posix(), NEW_PLAN.as_posix())
        item["native_case_path"] = item["native_case_path"].replace("benchmark_v2.json", "benchmark_v3.json")
        item["native_case_sha256"] = sha(item["native_case_path"])
        case_path = Path(item["native_case_path"])
        case = load(case_path)
        case["benchmark_path"] = (NEW_PLAN / "benchmark_v3.json").as_posix()
        case["benchmark_sha256"] = sha(NEW_PLAN / "benchmark_v3.json")
        dump(case_path, case)
        item["native_case_sha256"] = sha(item["native_case_path"])
    dump(manifest_path, manifest)

    # Copy and version the actual executable path. Native method source files
    # remain byte-identical except for Auer package imports.
    g4 = ROOT / "validation/autonomous_w2/g4"
    for old_name, new_name in {
        "matched_v6_common_v2.py": "matched_v6_common_v3.py",
        "v6_w2_adapter_v2.py": "v6_w2_adapter_v3.py",
        "auer_w2_adapter_v2.py": "auer_w2_adapter_v3.py",
        "windows_job_supervisor_v2.py": "windows_job_supervisor_v3.py",
    }.items():
        text = (g4 / old_name).read_text(encoding="utf-8")
        text = text.replace("matched_v6_task_development_v2", "matched_v6_task_development_v3")
        text = text.replace("v6_snapshot_v2", "v6_snapshot_v3").replace("auer_snapshot_v2", "auer_snapshot_v3")
        if new_name == "matched_v6_common_v3.py":
            start = text.index("def load_freeze()")
            end = text.index("\ndef verify_source_closure", start)
            helper = '''def load_authoritative_freeze(freeze_path: Path, receipt_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    expected_freeze = PROJECT / PLAN_REL / "freeze_manifest_v4.json"
    expected_receipt = PROJECT / RESULT_REL / "freeze_receipt_v4.json"
    if freeze_path.resolve() != expected_freeze.resolve() or receipt_path.resolve() != expected_receipt.resolve():
        raise InvalidInput("AUTHORITATIVE_FREEZE_PATH_REQUIRED")
    receipt = strict_json(expected_receipt)
    if receipt.get("freeze_manifest_path") != expected_freeze.relative_to(PROJECT).as_posix():
        raise InvalidInput("FREEZE_RECEIPT_PATH_BINDING")
    if receipt.get("source_closure_path") != "results/validation/autonomous_w2/g4/matched_v6_task_development_v3/source_closure_v4.json":
        raise InvalidInput("FREEZE_RECEIPT_CLOSURE_PATH_BINDING")
    if sha256_file(expected_freeze) != receipt.get("freeze_manifest_sha256"):
        raise InvalidInput("FROZEN_MANIFEST_SHA_MISMATCH")
    freeze = strict_json(expected_freeze)
    if sha256_file(PROJECT / freeze["protocol_path"]) != freeze.get("protocol_sha256"):
        raise InvalidInput("FREEZE_PROTOCOL_HASH_MISMATCH")
    if receipt.get("protocol_sha256") != freeze.get("protocol_sha256"):
        raise InvalidInput("FREEZE_RECEIPT_PROTOCOL_HASH")
    if freeze.get("freeze_receipt_path") != expected_receipt.relative_to(PROJECT).as_posix():
        raise InvalidInput("FREEZE_MANIFEST_RECEIPT_PATH_BINDING")
    if receipt.get("source_closure_sha256") != freeze.get("source_closure_sha256"):
        raise InvalidInput("FREEZE_RECEIPT_CLOSURE_HASH_BINDING")
    return freeze, receipt
'''
            text = text[:start] + helper + text[end:]
        (g4 / new_name).write_text(text, encoding="utf-8")

    auer_worker = (g4 / "auer_w2_worker_v2.py").read_text(encoding="utf-8")
    for old, new in (("matched_v6_task_development_v2", "matched_v6_task_development_v3"),
                     ("matched_v6_common_v2", "matched_v6_common_v3"),
                     ("auer_w2_adapter_v2", "auer_w2_adapter_v3"),
                     ("auer_snapshot_v2", "auer_snapshot_v3"),
                     ("freeze_manifest_v3.json", "freeze_manifest_v4.json"),
                     ("freeze_receipt_v3.json", "freeze_receipt_v4.json")):
        auer_worker = auer_worker.replace(old, new)
    (g4 / "auer_w2_worker_v3.py").write_text(auer_worker, encoding="utf-8")

    runner = (g4 / "run_matched_v6_w2_v2.py").read_text(encoding="utf-8")
    for old, new in (("matched_v6_task_development_v2", "matched_v6_task_development_v3"),
                     ("matched_v6_common_v2", "matched_v6_common_v3"),
                     ("windows_job_supervisor_v2", "windows_job_supervisor_v3"),
                     ("v6_w2_worker_v2", "v6_w2_worker_v3"), ("auer_w2_worker_v2", "auer_w2_worker_v3"),
                     ("protocol_v2.json", "protocol_v3.json"), ("freeze_manifest_v3.json", "freeze_manifest_v4.json"),
                     ("freeze_receipt_v3.json", "freeze_receipt_v4.json"),
                     ("matched_phase_receipt_v3.json", "matched_phase_receipt_v4.json")):
        runner = runner.replace(old, new)
    runner = runner.replace("phase_deadline = time.monotonic() + PHASE_WALL",
                            "phase_deadline = time.monotonic() + max(0.0, PHASE_WALL - (time.time() - float(freeze['phase_started_epoch'])))")
    (g4 / "run_matched_v6_w2_v3.py").write_text(runner, encoding="utf-8")

    auer_worker = (g4 / "auer_w2_worker_v3.py").read_text(encoding="utf-8")
    auer_worker = auer_worker.replace(
        "PLAN_REL, PROJECT, configure_integer_string_limit, initial_state_from_task,\n    scene_from_task, score_serialize_replay_progress, sha256_file, strict_json,",
        "PLAN_REL, PROJECT, configure_integer_string_limit, initial_state_from_task, load_authoritative_freeze,\n    scene_from_task, score_serialize_replay_progress, sha256_file, strict_json,",
    )
    old_block = (
        '    freeze_path = PROJECT / PLAN_REL / "freeze_manifest_v4.json"\n'
        '    freeze = strict_json(freeze_path)\n'
        '    freeze_receipt = strict_json(PROJECT / RESULT_REL / "freeze_receipt_v4.json")\n'
        '    if freeze_receipt.get("freeze_manifest_sha256") != sha256_file(freeze_path):\n'
        '        raise ValueError("FREEZE_RECEIPT_MANIFEST_HASH_MISMATCH")\n'
        '    if freeze_receipt.get("protocol_sha256") != freeze.get("protocol_sha256"):\n'
        '        raise ValueError("FREEZE_RECEIPT_PROTOCOL_HASH_MISMATCH")\n'
        '    closure = verify_source_closure(freeze)\n'
    )
    new_block = (
        '    freeze_path = PROJECT / PLAN_REL / "freeze_manifest_v4.json"\n'
        '    receipt_path = PROJECT / RESULT_REL / "freeze_receipt_v4.json"\n'
        '    freeze, freeze_receipt = load_authoritative_freeze(freeze_path, receipt_path)\n'
        '    closure = verify_source_closure(freeze)\n'
    )
    if old_block not in auer_worker:
        raise RuntimeError("AUER_WORKER_AUTHORITATIVE_FREEZE_BLOCK_NOT_FOUND")
    auer_worker = auer_worker.replace(old_block, new_block)
    marker = '    profile = strict_json(PROJECT / freeze["auer_profile_path"])\n'
    route_check = (
        '    if profile.get("matched_worker", {}).get("module") != "validation.autonomous_w2.g4.auer_w2_worker_v3":\n'
        '        raise ValueError("AUER_PROFILE_ACTUAL_WORKER_ROUTE_MISMATCH")\n'
        '    if freeze.get("method_worker_modules", {}).get("auer") != profile["matched_worker"]["module"]:\n'
        '        raise ValueError("AUER_FREEZE_PROFILE_WORKER_ROUTE_MISMATCH")\n'
        '    if profile.get("source_closure_manifest_path") != freeze.get("source_closure_path"):\n'
        '        raise ValueError("AUER_PROFILE_SOURCE_CLOSURE_PATH_STALE")\n'
    )
    auer_worker = auer_worker.replace(marker, marker + route_check)
    (g4 / "auer_w2_worker_v3.py").write_text(auer_worker, encoding="utf-8")

    profile_path = NEW_PLAN / "auer_profile_v3.json"
    profile = load(profile_path)
    profile["profile_id"] = "AUER_G4_W2_MATCHED_V6_DEVELOPMENT_V3_60S"
    profile["protocol_candidate"] = (NEW_PLAN / "protocol_v3.json").as_posix()
    profile["matched_worker"]["module"] = "validation.autonomous_w2.g4.auer_w2_worker_v3"
    profile["matched_worker"]["common_adapter"] = "validation.autonomous_w2.g4.auer_w2_adapter_v3"
    profile["matched_worker"]["native_solver"] = "validation.autonomous_w2.g4.auer_snapshot_v3.solver_r9_w2"
    profile["matched_worker"]["native_replay"] = "validation.autonomous_w2.g4.auer_snapshot_v3.replay_r9_w2"
    profile["source_closure_manifest_path"] = (RESULT / "source_closure_v4.json").as_posix()
    profile["source_snapshot_manifest_path"] = (NEW_PLAN / "native_source_snapshot_v3.json").as_posix()
    profile["external_guard_reference"] = "validation/autonomous_w2/g4/windows_job_supervisor_v3.py"
    profile["external_guard_reference_sha256"] = sha(profile["external_guard_reference"])
    dump(profile_path, profile)
    common = load(NEW_PLAN / "common_profile_v3.json")
    common["profile_id"] = "G4_COMMON_TUBE_W2_MATCHED_V6_60S_V3"
    common["protocol_candidate"] = (NEW_PLAN / "protocol_v3.json").as_posix()
    common["matched_workers"]["v6_module"] = "validation.autonomous_w2.g4.v6_w2_worker_v3"
    common["matched_workers"]["v6_replay_module"] = "native audit and common replay inside validation.autonomous_w2.g4.v6_w2_worker_v3"
    common["matched_workers"]["auer_module"] = "validation.autonomous_w2.g4.auer_w2_worker_v3"
    common["matched_workers"]["auer_replay_module"] = "native audit and common replay inside validation.autonomous_w2.g4.auer_w2_worker_v3"
    dump(NEW_PLAN / "common_profile_v3.json", common)

    # Finalize snapshot metadata after the solver package-import rewrite.
    snapshot_path = NEW_PLAN / "native_source_snapshot_v3.json"
    snapshot = load(snapshot_path)
    for entry in snapshot["copies"]:
        entry["snapshot_sha256"] = sha(entry["snapshot_path"])
        if entry["snapshot_path"].startswith("validation/autonomous_w2/g4/auer_snapshot_v3/") and entry["snapshot_path"].endswith("solver_r9_w2.py"):
            entry["adaptations"] = ["package import path v2 to v3; same solver equations and numerical profile"]
    dump(snapshot_path, snapshot)
    snapshot_sha = sha(snapshot_path)

    # Repoint each v6 outer binding to the actual v3 frozen source route.
    proto_path = NEW_PLAN / "protocol_v3.json"
    protocol = load(proto_path)
    for action in protocol["actions"]:
        ordinal = int(action["ordinal"])
        binding_path = NEW_PLAN / "v6_bindings" / f"{ordinal:02d}.json"
        binding = load(binding_path)
        binding["source_files"].pop((OLD_PLAN / "native_source_snapshot_v2.json").as_posix(), None)
        binding["source_files"][(NEW_PLAN / "native_source_snapshot_v3.json").as_posix()] = snapshot_sha
        binding["source_files"].pop("validation/autonomous_w2/g4/v6_w2_worker_v2.py", None)
        binding["source_files"].pop("validation/autonomous_w2/g4/v6_w2_adapter_v2.py", None)
        binding["source_files"]["validation/autonomous_w2/g4/v6_w2_worker_v3.py"] = sha("validation/autonomous_w2/g4/v6_w2_worker_v3.py")
        binding["source_files"]["validation/autonomous_w2/g4/v6_w2_adapter_v3.py"] = sha("validation/autonomous_w2/g4/v6_w2_adapter_v3.py")
        binding["source_files"][snapshot_path.as_posix()] = snapshot_sha
        binding["source_files"][(NEW_PLAN / "benchmark_v3.json").as_posix()] = sha(NEW_PLAN / "benchmark_v3.json")
        binding["source_snapshot_manifest_sha256"] = snapshot_sha
        binding["source_files"].pop("validation/autonomous_w2/g4/v6_snapshot_v2/producer_centered_v6.py", None)
        binding["source_files"].pop("validation/autonomous_w2/g4/v6_snapshot_v2/producer_v4.py", None)
        binding["source_files"].pop("validation/autonomous_w2/g4/v6_snapshot_v2/rational_interval_v3.py", None)
        binding["source_files"].pop("validation/autonomous_w2/g4/v6_snapshot_v2/checker_centered_v6.py", None)
        for rel in list(binding["source_files"]):
            binding["source_files"][rel.replace("v6_snapshot_v2/", "v6_snapshot_v3/")] = binding["source_files"].pop(rel)
        dump(binding_path, binding)
        action["native_binding_sha256"] = sha(binding_path)
    dump(proto_path, protocol)

    # Update Auer proof-binding objects after all candidate input/profile paths
    # are final. Their digests are canonical JSON plus one newline, as worker.
    binding_doc_path = NEW_PLAN / "auer_bindings_v3.json"
    bindings_doc = load(binding_doc_path)
    for entry in bindings_doc["bindings"]:
        case = next(item for item in manifest["cases"] if item["comparison_id"] == entry["comparison_id"])
        native = entry["native_binding"]
        native["input_path"] = case["native_case_path"]
        native["input_sha256"] = case["native_case_sha256"]
        native["resource_profile_path"] = profile_path.as_posix()
        native["resource_profile_sha256"] = sha(profile_path)
        native["source_snapshot_manifest_sha256"] = snapshot_sha
        native["solver_source_sha256"] = sha("validation/autonomous_w2/g4/auer_snapshot_v3/solver_r9_w2.py")
        native["checker_source_sha256"] = sha("validation/autonomous_w2/g4/auer_snapshot_v3/replay_r9_w2.py")
        entry["native_case_path"] = case["native_case_path"]
        entry["native_case_sha256"] = case["native_case_sha256"]
        entry["physical_input_sha256"] = case["physical_input_sha256"]
    dump(binding_doc_path, bindings_doc)
    dump(manifest_path, manifest)
    # Bind final Auer inputs and native binding hashes into the protocol after
    # the profile/case/snapshot hashes are settled.
    protocol = load(proto_path)
    for action in protocol["actions"]:
        entry = next(row for row in bindings_doc["bindings"] if row["comparison_id"] == action["auer_id"])
        case = next(row for row in manifest["cases"] if row["comparison_id"] == action["auer_id"])
        native_raw = json.dumps(entry["native_binding"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
        action["auer_native_binding_sha256"] = hashlib.sha256(native_raw).hexdigest()
        action["auer_native_input_path"] = case["native_case_path"]
        action["auer_native_input_file_sha256"] = case["native_case_sha256"]
        action["auer_input_digest"] = case["physical_input_sha256"]
        action["v6_native_binding_sha256"] = action["native_binding_sha256"]
    dump(proto_path, protocol)
    output = {
        "schema": "ddwmr-g4-w2-v3-preparation-receipt",
        "session": "DDWMR | LUNA-G4-AUER",
        "candidate_plan": NEW_PLAN.as_posix(),
        "candidate_result": RESULT.as_posix(),
        "task_sha256": sha("research/autonomous_w2/g2/task_protocol_v1.json"),
        "peer_release_sha256": sha("coordination/autonomous_w2/g2/releases/RELEASE_v6.json"),
        "ordered_action_count": 3,
        "historical_candidate_unchanged": True,
    }
    dump(RESULT / "candidate_prepare_receipt_v3.json", output)
    return output


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2))
