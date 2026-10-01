"""Read-only R5 verifier for stored Auer proof-to-common composition."""
from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))
from validation.baselines.auer2013.replay_ivp import canonical_sha256, replay_native_proof
from validation.g2.hashing import semantic_json_sha256
from validation.g2.rational import Budget, Interval, InvalidInput, ResourceLimit, parse_q
from validation.g4.common_tube import TubeSegment, check_tube_segments

PROFILE_REL = Path("validation/configs/auer_r5_composition_replay_profile_v1.json")
PROOF_NAME = "r4_ddwmr_single_query_native_v2.json"
EVIDENCE_NAME = "r4_ddwmr_single_query_evidence_v2.json"
COMMON_REL = Path("inputs/r4_common_check_v2.json")
COMPOSITION_REL = Path("inputs/r4_composition_v1.json")
DEPENDENCY = "shared validation.g2 exact Fraction/Interval/Budget and Taylor sin/cos; separately disclosed and not an independent arithmetic library"
EXPECTED_QUERY = "state_low_neg__scene_d020_l-200__T_020__V_m1_m1"
EXPECTED_SCENE = "scene_d020_l-200"
EXPECTED_PROOF_BODY_SHA256 = "4e49a66b69d869758f28ecfdba84eccefde4e38d8a1fa4f70d3c6e3f2701be70"
EXPECTED_PROOF_FILE_SHA256 = "8d394d836c5b92b733403b16b1786cb7fe410ab8fb8610c694c0a7c88e5dde4e"

class Stop(Exception):
    def __init__(self, category: str, detail: str, reason: str | None = None):
        super().__init__(detail); self.category, self.detail, self.reason = category, detail, reason

def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
    return h.hexdigest()

def strict_json(path: Path) -> Any:
    def pairs(items):
        out = {}
        for k, v in items:
            if k in out: raise ValueError(f"duplicate JSON key {k!r}")
            out[k] = v
        return out
    def bad_constant(x): raise ValueError(f"non-finite JSON number {x}")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)

def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))

def resolve(path) -> Path:
    return Path(path).expanduser().resolve()

def safe_path(root: Path, rel: str) -> Path:
    p = (root / rel).resolve()
    if p != root and root not in p.parents: raise Stop("invalid_or_tampered_input", f"path escapes root: {rel}")
    return p

def diff(a: Any, e: Any, path="$") -> str | None:
    if type(a) is not type(e): return f"{path}: stored type {type(a).__name__}, expected {type(e).__name__}"
    if isinstance(e, dict):
        for k in sorted(set(a) | set(e)):
            p = f"{path}.{k}"
            if k not in a: return f"{p}: missing from stored record"
            if k not in e: return f"{p}: unexpected stored field"
            d = diff(a[k], e[k], p)
            if d: return d
        return None
    if isinstance(e, list):
        if len(a) != len(e): return f"{path}: stored length {len(a)}, expected {len(e)}"
        for i, (av, ev) in enumerate(zip(a, e)):
            d = diff(av, ev, f"{path}[{i}]")
            if d: return d
        return None
    return None if a == e else f"{path}: stored value {a!r}, expected {e!r}"

def same(a: Any, b: Any) -> bool:
    return diff(a, b) is None

def verify_snapshot(root: Path, expected_sha: str, schema: str):
    mf, sf = root / "snapshot_manifest.json", root / "snapshot_manifest.sha256"
    if not mf.is_file() or not sf.is_file(): raise Stop("invalid_or_tampered_input", f"snapshot manifest/sidecar missing: {root}")
    raw = mf.read_bytes(); actual_sha = sha_bytes(raw)
    if actual_sha != expected_sha: raise Stop("invalid_or_tampered_input", f"snapshot manifest hash mismatch: {actual_sha}")
    if sf.read_text(encoding="ascii").split()[0] != actual_sha: raise Stop("invalid_or_tampered_input", "snapshot sidecar mismatch")
    manifest = strict_json(mf)
    if manifest.get("schema") != schema: raise Stop("invalid_or_tampered_input", f"unexpected snapshot schema {manifest.get('schema')!r}")
    members = {}
    for item in manifest.get("members", []):
        rel = item.get("snapshot_relative_path")
        if not isinstance(rel, str) or rel in members: raise Stop("invalid_or_tampered_input", "invalid/duplicate snapshot member")
        members[rel] = item
    if len(members) != manifest.get("member_count"): raise Stop("invalid_or_tampered_input", "snapshot member count mismatch")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*")
              if p.is_file() and p.name not in {"snapshot_manifest.json", "snapshot_manifest.sha256"}}
    extras = actual - set(members)
    unlisted_noncache = {rel for rel in extras if "__pycache__" not in Path(rel).parts and Path(rel).suffix != ".pyc"}
    if set(members) - actual or unlisted_noncache:
        raise Stop("invalid_or_tampered_input", f"snapshot file set mismatch; missing={sorted(set(members)-actual)[:3]}, extra_noncache={sorted(unlisted_noncache)[:3]}")
    for rel, item in members.items():
        p = safe_path(root, rel)
        if p.stat().st_size != item["bytes"] or sha_file(p) != item["sha256"]:
            raise Stop("invalid_or_tampered_input", f"snapshot member mismatch: {rel}")
    return manifest, members

def verify_r4_outputs(root: Path, mf: Path, profile: dict):
    if mf != (root / "r4_output_artifact_manifest_v1.json").resolve(): raise Stop("invalid_or_tampered_input", "R4 manifest path/root mismatch")
    frozen = profile["frozen_sha256"]["r4_output_artifact_manifest"]
    if not mf.is_file() or sha_file(mf) != frozen: raise Stop("invalid_or_tampered_input", "R4 output-artifact manifest hash mismatch")
    manifest = strict_json(mf)
    if manifest.get("source_snapshot_v10_manifest_sha256") != profile["frozen_sha256"]["r4_source_snapshot_v10_manifest"] or manifest.get("matched_query_evaluations") != 0:
        raise Stop("invalid_or_tampered_input", "R4 manifest source binding or matched-query count changed")
    artifacts = {}
    for item in manifest.get("artifacts", []):
        rel = item.get("path")
        if not isinstance(rel, str) or rel in artifacts: raise Stop("invalid_or_tampered_input", "invalid/duplicate R4 output path")
        p = safe_path(root, rel)
        if not p.is_file() or p.stat().st_size != item.get("bytes") or sha_file(p) != item.get("sha256"):
            raise Stop("invalid_or_tampered_input", f"R4 output artifact mismatch: {rel}")
        artifacts[rel] = item
    if len(artifacts) != profile["counts"]["r4_output_artifacts"]: raise Stop("invalid_or_tampered_input", "R4 output artifact count mismatch")
    if manifest.get("status") != "R4_SINGLE_CASE_RUNS_AND_FAILED_ATTEMPTS_HASHED; NO_MATCHED_BATCH":
        raise Stop("invalid_or_tampered_input", "R4 output manifest status changed")
    return manifest, artifacts

def project_file(argument: str, rel: str, label: str) -> Path:
    p = resolve(argument)
    if p != (PROJECT / rel).resolve() or not p.is_file(): raise Stop("invalid_or_tampered_input", f"{label} is not the frozen v11 project file: {p}")
    return p

def check_hash(path: Path, expected: str, label: str):
    actual = sha_file(path)
    if actual != expected: raise Stop("invalid_or_tampered_input", f"{label} SHA-256 mismatch: expected {expected}; got {actual}")
    return actual

def check_trial(path: Path, trial_mode: bool, trial_root: Path | None, protected_r4_artifacts: set[Path], label: str):
    if not trial_mode or trial_root is None or path == trial_root or trial_root not in path.parents:
        raise Stop("invalid_or_tampered_input", f"{label} override requires a copy under --trial-root and --trial-mode")
    if path in protected_r4_artifacts:
        raise Stop("invalid_or_tampered_input", f"{label} trial overwrites a manifest-listed R4 artifact")

def check_work_ledger(ev: dict, profile: dict):
    w = profile["r4_work_ledger"]; r = ev.get("rational_work", {})
    checks = {
        "producer": (ev.get("producer_work", {}).get("operations"), w["producer_operations"]),
        "native_replay": (ev.get("native_proof_replay", {}).get("work", {}).get("rational_operations"), w["native_replay_operations"]),
        "tamper_replay": (ev.get("tamper_replay_work_operations"), w["tamper_replay_operations"]),
        "combined": (r.get("combined"), w["combined_operations"]),
        "cap": (r.get("cap"), w["combined_operation_cap"]),
        "common": (r.get("common_predicate"), w["common_predicate_operations"]),
    }
    for k, (a, e) in checks.items():
        if a != e: raise Stop("invalid_or_tampered_input", f"R4 work ledger mismatch at {k}: {a!r} != {e!r}")
    if ev.get("combined_operation_cap") != w["combined_operation_cap"]: raise Stop("invalid_or_tampered_input", "R4 combined cap mismatch")
    remaining = w["combined_operation_cap"] - w["producer_operations"] - w["native_replay_operations"] - w["tamper_replay_operations"]
    if remaining != w["common_budget_remaining_operations"] or remaining != profile["resource_limits"]["common_rational_operation_cap"]:
        raise Stop("invalid_or_tampered_input", "R4 remaining common-budget arithmetic mismatch")

def run(args: argparse.Namespace):
    workspace = resolve(args.workspace_root)
    r5 = resolve(args.r5_snapshot)
    expected_r5_snapshot = workspace / "results/validation/g4/auer2013/r5_composition_replay_v1/source_snapshot_v11"
    if r5 != expected_r5_snapshot.resolve():
        raise Stop("invalid_or_tampered_input", "R5 source snapshot path differs from the specified workspace")
    r5_hash = args.r5_snapshot_manifest_sha256.lower()
    _, r5_members = verify_snapshot(r5, r5_hash, "ddwmr-g4-auer-local-source-snapshot-v11")
    if resolve(args.project_root) != PROJECT or PROJECT != (r5 / "project").resolve():
        raise Stop("invalid_or_tampered_input", "running project is not the frozen v11 project directory")
    profile_path = project_file(args.r5_profile, PROFILE_REL.as_posix(), "R5 profile")
    profile_member = r5_members.get(f"project/{PROFILE_REL.as_posix()}")
    if not profile_member or sha_file(profile_path) != profile_member["sha256"]:
        raise Stop("invalid_or_tampered_input", "R5 profile is not hash-bound by v11")
    profile = strict_json(profile_path)
    if profile.get("schema") != "ddwmr-g4-auer-composition-replay-profile-v1" or profile.get("status") != "FROZEN_BEFORE_FIRST_R5_REPLAY":
        raise Stop("invalid_or_tampered_input", "R5 profile schema/status mismatch")

    r4_base = workspace / "results/validation/g4/auer2013"
    expected_r5_artifacts = r4_base / "r5_composition_replay_v1"
    if resolve(args.r5_artifact_root) != expected_r5_artifacts.resolve():
        raise Stop("invalid_or_tampered_input", "R5 artifact root differs from the specified workspace")
    v10 = resolve(args.v10_snapshot)
    if v10 != (r4_base / "source_snapshot_v10").resolve():
        raise Stop("invalid_or_tampered_input", "v10 snapshot path differs from frozen R4 location")
    v10_hash = profile["frozen_sha256"]["r4_source_snapshot_v10_manifest"]
    _, v10_members = verify_snapshot(v10, v10_hash, "ddwmr-g4-auer-local-source-snapshot-v10")
    if len(v10_members) != profile["counts"]["v10_snapshot_members"]:
        raise Stop("invalid_or_tampered_input", "v10 snapshot member count mismatch")

    out_root = resolve(args.r4_output_root)
    if out_root != r4_base.resolve():
        raise Stop("invalid_or_tampered_input", "R4 output root differs from frozen location")
    out_manifest = resolve(args.r4_output_manifest)
    manifest, outputs = verify_r4_outputs(out_root, out_manifest, profile)
    protected_r4_artifacts = {(out_root / rel).resolve() for rel in outputs}
    if manifest.get("source_snapshot_v10_manifest_sha256") != v10_hash:
        raise Stop("invalid_or_tampered_input", "R4 output manifest is not bound to verified v10")

    paths = profile["project_paths"]
    names = {
        "selected_case_input": paths["selected_case_input"],
        "benchmark": paths["benchmark"],
        "r4_resource_profile": paths["r4_resource_profile"],
        "method_contract": paths["method_contract"],
        "arithmetic_backend_manifest": paths["arithmetic_backend_manifest"],
    }
    arg_names = {
        "selected_case_input": "case_input", "benchmark": "benchmark",
        "r4_resource_profile": "resource_profile", "method_contract": "method_contract",
        "arithmetic_backend_manifest": "backend_manifest",
    }
    fixed = {key: project_file(getattr(args, arg_names[key]), rel, key) for key, rel in names.items()}
    frozen = profile["frozen_sha256"]
    for name, path in fixed.items():
        check_hash(path, frozen[name], name)

    r5_root = resolve(args.r5_artifact_root)
    common_default = (r5_root / COMMON_REL).resolve()
    composition_default = (r5_root / COMPOSITION_REL).resolve()
    proof_path, common_path = resolve(args.native_proof), resolve(args.common_record)
    composition_path, evidence_path = resolve(args.composition), resolve(args.r4_evidence)
    trial_root = resolve(args.trial_root) if args.trial_root else None
    if evidence_path != (out_root / EVIDENCE_NAME).resolve():
        raise Stop("invalid_or_tampered_input", "R4 evidence path is not the frozen evidence artifact")
    if outputs.get(EVIDENCE_NAME, {}).get("sha256") != frozen["r4_evidence"]:
        raise Stop("invalid_or_tampered_input", "R4 evidence manifest binding mismatch")
    if outputs.get(PROOF_NAME, {}).get("sha256") != frozen["r4_native_proof_file"]:
        raise Stop("invalid_or_tampered_input", "R4 proof manifest binding mismatch")
    original_proof = (out_root / PROOF_NAME).resolve()
    if proof_path == original_proof:
        check_hash(proof_path, frozen["r4_native_proof_file"], "pristine R4 native proof")
    else:
        check_trial(proof_path, args.trial_mode, trial_root, protected_r4_artifacts, "native proof")
    if common_path == common_default:
        check_hash(common_path, frozen["r5_common_record_copy"], "R5 common-record copy")
    else:
        check_trial(common_path, args.trial_mode, trial_root, protected_r4_artifacts, "common record")
    if composition_path == composition_default:
        check_hash(composition_path, frozen["r5_composition_copy"], "R5 composition copy")
    else:
        check_trial(composition_path, args.trial_mode, trial_root, protected_r4_artifacts, "composition")
    overrides = proof_path != original_proof or common_path != common_default or composition_path != composition_default
    if bool(args.trial_mode) != bool(overrides):
        raise Stop("invalid_or_tampered_input", "trial-mode flag and artifact overrides disagree")

    runtime = profile["runtime"]
    executable = Path(sys.executable).resolve()
    if executable != Path(runtime["executable"]).resolve() or sha_file(executable) != runtime["executable_sha256"] or sys.version != runtime["version"]:
        raise Stop("invalid_or_tampered_input", "Python executable/version differs from frozen R4 arithmetic runtime")

    case = strict_json(fixed["selected_case_input"])
    benchmark = strict_json(fixed["benchmark"])
    resource = strict_json(fixed["r4_resource_profile"])
    evidence = strict_json(evidence_path)
    if evidence.get("schema") != "ddwmr-g4-auer-r4-worker-evidence-v1":
        raise Stop("invalid_or_tampered_input", "R4 evidence schema mismatch")
    check_work_ledger(evidence, profile)
    identity = profile["case_identity"]
    if case.get("query_id") != EXPECTED_QUERY or case.get("scene", {}).get("id") != EXPECTED_SCENE:
        raise Stop("invalid_or_tampered_input", "query/scene identity differs from selected R4 case")
    if case.get("candidate_manifest_v2_input_sha256") != identity["candidate_manifest_v2_input_sha256"]:
        raise Stop("invalid_or_tampered_input", "candidate-manifest input digest changed")
    if case.get("benchmark_path") != paths["benchmark"] or case.get("benchmark_sha256") != frozen["benchmark"]:
        raise Stop("invalid_or_tampered_input", "selected input benchmark binding mismatch")
    if benchmark.get("schema") != identity["benchmark_schema"]:
        raise Stop("invalid_or_tampered_input", "benchmark schema mismatch")
    if resource.get("max_rational_bits") != profile["resource_limits"]["max_rational_bits"] or resource.get("max_rational_operations_per_ivp_combined_producer_replay_and_common_check") != profile["r4_work_ledger"]["combined_operation_cap"]:
        raise Stop("invalid_or_tampered_input", "R4 resource-profile caps differ from R5 frozen expectations")

    for rel in profile["required_v10_source_members"]:
        member = v10_members.get(f"project/{rel}")
        active = safe_path(PROJECT, rel)
        if not member or not active.is_file() or sha_file(active) != member["sha256"]:
            raise Stop("invalid_or_tampered_input", f"active replay/common arithmetic source differs from v10: {rel}")
    backend = strict_json(fixed["arithmetic_backend_manifest"])
    if backend.get("backend_id") != identity["arithmetic_backend_id"]:
        raise Stop("invalid_or_tampered_input", "arithmetic backend identity mismatch")
    for item in backend.get("proof_critical_source_files", []):
        rel = item.get("path")
        member = v10_members.get(f"project/{rel}") if isinstance(rel, str) else None
        active = safe_path(PROJECT, rel) if isinstance(rel, str) else None
        if not member or active is None or not active.is_file() or member["sha256"] != item.get("sha256") or sha_file(active) != item["sha256"]:
            raise Stop("invalid_or_tampered_input", f"backend critical-source hash mismatch: {rel}")

    binding = {
        "input_path": paths["selected_case_input"], "input_sha256": frozen["selected_case_input"],
        "method_contract_path": paths["method_contract"], "method_contract_sha256": frozen["method_contract"],
        "arithmetic_backend_manifest_path": paths["arithmetic_backend_manifest"],
        "arithmetic_backend_manifest_sha256": frozen["arithmetic_backend_manifest"],
        "resource_profile_path": paths["r4_resource_profile"], "resource_profile_sha256": frozen["r4_resource_profile"],
        "source_snapshot_manifest_sha256": v10_hash,
        "solver_source_sha256": v10_members["project/validation/baselines/auer2013/residual_ivp.py"]["sha256"],
        "checker_source_sha256": v10_members["project/validation/baselines/auer2013/replay_ivp.py"]["sha256"],
        "arithmetic_dependency": DEPENDENCY,
    }
    if proof_path.stat().st_size > resource["max_serialized_proof_bytes"]:
        raise Stop("resource_limit", "stored proof exceeds frozen serialized-proof byte cap")
    try:
        envelope = strict_json(proof_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise Stop("native_proof_failure", f"stored proof cannot be parsed: {exc}") from exc
    proof_file_sha = sha_file(proof_path)
    if proof_path == original_proof and envelope.get("proof_sha256") != EXPECTED_PROOF_BODY_SHA256:
        raise Stop("invalid_or_tampered_input", "pristine proof-body digest differs from frozen binding")

    limits = profile["resource_limits"]
    native_budget = Budget(int(limits["max_rational_bits"]), int(limits["native_replay_operation_cap"]),
                           Fraction(int(limits["wall_time_seconds_per_replay"])))
    native_budget.set_stage("r5-native-proof-replay")
    rhs_counter = {"count": 0, "limit": int(limits["max_rhs_jacobian_evaluations"])}
    native = replay_native_proof(envelope, case=case, benchmark=benchmark, profile=resource, fixture=None,
                                 expected_binding=binding, budget=native_budget, rhs_eval_counter=rhs_counter)
    if not native.get("replayed"):
        if native.get("reason") == "resource_limit":
            raise Stop("resource_limit", f"native replay cap: {native.get('termination')}", native.get("reason"))
        raise Stop("native_proof_failure",
                   f"native stored-proof replay rejected: {native.get('reason')}: {native.get('detail', '')}",
                   native.get("reason"))
    if proof_path == original_proof and native["proof_sha256"] != EXPECTED_PROOF_BODY_SHA256:
        raise Stop("invalid_or_tampered_input", "native replay digest differs from frozen proof binding")
    if native["work"]["rational_operations"] != evidence["native_proof_replay"]["work"]["rational_operations"]:
        raise Stop("native_proof_failure", "native replay operation count differs from R4 evidence ledger")

    common_budget = Budget(int(limits["max_rational_bits"]), int(limits["common_rational_operation_cap"]),
                           Fraction(int(limits["wall_time_seconds_per_replay"])))
    common_budget.set_stage("r5-common-predicate-replay")
    labels = tuple((item["name"], Interval.from_json(case["fixed_labels"][item["name"]], common_budget))
                   for item in benchmark["parameter_labels"])
    segments = []
    for index, step in enumerate(envelope["proof"]["step_records"]):
        try:
            start = parse_q(step["time_closed"]["start"], common_budget)
            end = parse_q(step["time_closed"]["end"], common_budget)
            hull = tuple(Interval.from_json(row, common_budget) for row in step["full_time_total_hull_augmented"][:9])
            start_state = tuple(Interval.from_json(row, common_budget) for row in step["endpoint_start_augmented"][:9])
            end_state = tuple(Interval.from_json(row, common_budget) for row in step["endpoint_end_augmented"][:9])
            segments.append(TubeSegment.from_total_hull(
                segment_id=f"AUER:{case['query_id']}:{index}", t_start=start, t_end=end,
                state_hull=hull, labels=labels, endpoint_start=start_state, endpoint_end=end_state,
                radius_expansion_count=0, radius_expansion_mode="NATIVE_TOTAL_HULL",
                provenance={"native_method_id": envelope["proof"]["method_id"],
                            "native_proof_sha256": envelope["proof_sha256"],
                            "native_proof_file_sha256": proof_file_sha,
                            "source_snapshot_manifest_sha256": v10_hash},
            ))
        except ResourceLimit as exc:
            raise Stop("resource_limit", f"segment reconstruction cap: {exc.detail}", exc.kind) from exc
        except (InvalidInput, KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
            raise Stop("native_proof_failure", f"replayed proof slab cannot form common segment: {exc}") from exc
    initial = tuple(Interval.from_json(row, common_budget) for row in case["initial_state"])
    horizon = parse_q(case["horizon"], common_budget)
    scene = {"id": case["scene"]["id"], "p_o": case["scene"]["p_o"], "R_s": case["scene"]["R_s"]}
    try:
        common = check_tube_segments(tuple(segments), benchmark, scene, horizon, common_budget,
                                     initial_state=initial,
                                     sqrt_bisections=int(resource["transcendental_profile"]["square_root_bisections"]))
    except ResourceLimit as exc:
        raise Stop("resource_limit", f"common-predicate cap: {exc.detail}", exc.kind) from exc
    except (InvalidInput, KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        raise Stop("common_predicate_mismatch", f"proof-derived common predicate recomputation failed: {exc}") from exc
    if common.get("predicate_status") != "PASS_ON_SUPPLIED_TUBE":
        raise Stop("common_predicate_mismatch", f"recomputed status is {common.get('predicate_status')!r}")
    try:
        stored_common = strict_json(common_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise Stop("common_predicate_mismatch", f"stored common record cannot be parsed: {exc}") from exc
    mismatch = diff(stored_common, common)
    if mismatch: raise Stop("common_predicate_mismatch", mismatch)
    if common_path == common_default and not same(stored_common, evidence.get("common_predicate_check")):
        raise Stop("invalid_or_tampered_input", "pristine common copy differs from hash-bound R4 evidence")
    segment_json = [item.to_json() for item in segments]
    expected_composition = {
        "schema": "ddwmr-g4-auer-r4-proof-to-common-composition-v1",
        "query_id": case["query_id"],
        "candidate_manifest_v2_input_sha256": case["candidate_manifest_v2_input_sha256"],
        "held_voltage": case["held_voltage"],
        "native_proof_sha256": envelope["proof_sha256"],
        "native_proof_file_sha256": proof_file_sha,
        "source_snapshot_manifest_sha256": v10_hash,
        "radius_expansion_mode": "NATIVE_TOTAL_HULL",
        "radius_expansion_count": 0,
        "segments": segment_json,
        "segments_sha256": semantic_json_sha256(segment_json),
        "common_check_sha256": canonical_sha256(common),
        "common_check_predicate_status": common["predicate_status"],
        "common_check_certificate_emitted": False,
        "common_check_ode_tube_proof_replayed": False,
    }
    try:
        stored_composition = strict_json(composition_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise Stop("composition_mismatch", f"stored composition cannot be parsed: {exc}") from exc
    mismatch = diff(stored_composition, expected_composition)
    if mismatch: raise Stop("composition_mismatch", mismatch)
    if composition_path == composition_default and not same(stored_composition, evidence.get("typed_proof_to_common_composition")):
        raise Stop("invalid_or_tampered_input", "pristine composition copy differs from hash-bound R4 evidence")
    if proof_path == original_proof and proof_file_sha != frozen["r4_native_proof_file"]:
        raise Stop("invalid_or_tampered_input", "pristine proof file hash differs from frozen binding")

    return {
        "schema": "ddwmr-g4-auer-composition-replay-report-v1",
        "status": "PASS", "reason": None,
        "detail": "stored native proof, proof-derived common record, and stored composition all replay and match",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "query_id": case["query_id"],
        "native_proof_file_sha256": proof_file_sha,
        "native_proof_sha256": envelope["proof_sha256"],
        "native_replay_status": "PASS", "native_replay": native,
        "common_record_status": "PASS", "common_predicate_status": common["predicate_status"],
        "common_rational_operations": common_budget.operations,
        "composition_status": "PASS", "segment_count": len(segments),
        "segments_sha256": expected_composition["segments_sha256"],
        "common_check_sha256": expected_composition["common_check_sha256"],
        "r4_output_artifact_count_verified": len(outputs),
        "r4_source_snapshot_member_count_verified": len(v10_members),
        "r5_source_snapshot_member_count_verified": len(r5_members),
        "r4_output_artifact_manifest_sha256": sha_file(out_manifest),
        "r4_source_snapshot_v10_manifest_sha256": v10_hash,
        "r5_source_snapshot_v11_manifest_sha256": r5_hash,
        "input_sha256": {
            "selected_case_input": sha_file(fixed["selected_case_input"]),
            "benchmark": sha_file(fixed["benchmark"]),
            "r4_resource_profile": sha_file(fixed["r4_resource_profile"]),
            "method_contract": sha_file(fixed["method_contract"]),
            "arithmetic_backend_manifest": sha_file(fixed["arithmetic_backend_manifest"]),
            "native_proof_file": proof_file_sha,
            "r4_evidence": sha_file(evidence_path),
            "common_record": sha_file(common_path),
            "composition": sha_file(composition_path),
            "r5_profile": sha_file(profile_path),
        },
        "dependency_disclosure": {
            "native_checker": "validation.baselines.auer2013.replay_ivp.replay_native_proof; R4 producer not imported",
            "common_predicate": "validation.g4.common_tube.check_tube_segments",
            "shared_arithmetic": DEPENDENCY,
            "composition_expectation": "rebuilt from replay-validated proof and recomputed common result before comparing stored composition",
        },
        "certificate_emitted": False, "matched_query_evaluations": 0,
        "research_disposition": "HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED",
    }

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace-root", type=Path, required=True)
    p.add_argument("--project-root", type=Path, required=True)
    p.add_argument("--r5-snapshot", type=Path, required=True)
    p.add_argument("--r5-snapshot-manifest-sha256", required=True)
    p.add_argument("--r5-profile", type=Path, required=True)
    p.add_argument("--r5-artifact-root", type=Path, required=True)
    p.add_argument("--v10-snapshot", type=Path, required=True)
    p.add_argument("--r4-output-root", type=Path, required=True)
    p.add_argument("--r4-output-manifest", type=Path, required=True)
    p.add_argument("--case-input", type=Path, required=True)
    p.add_argument("--benchmark", type=Path, required=True)
    p.add_argument("--resource-profile", type=Path, required=True)
    p.add_argument("--method-contract", type=Path, required=True)
    p.add_argument("--backend-manifest", type=Path, required=True)
    p.add_argument("--native-proof", type=Path, required=True)
    p.add_argument("--r4-evidence", type=Path, required=True)
    p.add_argument("--common-record", type=Path, required=True)
    p.add_argument("--composition", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--trial-mode", action="store_true")
    p.add_argument("--trial-root", type=Path)
    args = p.parse_args()
    try:
        report, code = run(args), 0
    except Stop as exc:
        report = {
            "schema": "ddwmr-g4-auer-composition-replay-report-v1",
            "status": "REJECTED", "reason": exc.category, "detail": exc.detail,
            "native_reason": exc.reason,
            "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "certificate_emitted": False, "matched_query_evaluations": 0,
            "research_disposition": "HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED",
        }
        code = {"invalid_or_tampered_input": 10, "native_proof_failure": 11,
                "common_predicate_mismatch": 12, "composition_mismatch": 13,
                "resource_limit": 14}.get(exc.category, 10)
    except (OSError, ValueError, KeyError, TypeError, InvalidInput, ZeroDivisionError) as exc:
        report = {
            "schema": "ddwmr-g4-auer-composition-replay-report-v1",
            "status": "REJECTED", "reason": "invalid_or_tampered_input",
            "detail": f"premise validation error: {exc}", "native_reason": None,
            "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "certificate_emitted": False, "matched_query_evaluations": 0,
            "research_disposition": "HOLD; G1 restricted PASS; G2/G3/G4 UNVERIFIED; physical correspondence UNVERIFIED",
        }
        code = 10
    out = resolve(args.report)
    write_json(out, report)
    print(json.dumps({"status": report["status"], "reason": report.get("reason"),
                      "query_id": report.get("query_id"), "report": str(out)}, sort_keys=True))
    return code

if __name__ == "__main__":
    raise SystemExit(main())
