"""Non-query audit of the frozen G2-v6/Auer common physical-input map."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PLAN = Path("research/autonomous_w2/g4/matched_v6_task_development_v2")
TASK = Path("research/autonomous_w2/g2/task_protocol_v1.json")
RELEASE = Path("coordination/autonomous_w2/g2/releases/RELEASE_v6.json")
RELEASE_SHA = "789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55"
TASK_SHA = "8bc1c8fd460a62dc3f7ff1c8e4bef2dbaddbcaffbadd75d6c2c487e9e311c15a"
LABELS = ["rho_L", "rho_R", "C_L", "C_R", "lambda_L", "lambda_R", "R_L", "R_R", "B_L", "B_R", "k_L", "k_R"]
STATES = ["p_x", "p_y", "theta", "u", "r", "omega_L", "omega_R", "i_L", "i_R"]
PAIRS = [
    ("W2_G4_V6_ZERO", "W2_G4_AUER_ZERO", "W2_G2_DEV_001_ZERO", "W2_V0", ("0", "0")),
    ("W2_G4_V6_NOMINAL", "W2_G4_AUER_NOMINAL", "W2_G2_DEV_001_NOMINAL", "W2_VHALF", ("1/2", "1/2")),
    ("W2_G4_V6_ALTERNATIVE", "W2_G4_AUER_ALTERNATIVE", "W2_G2_DEV_001_ALTERNATIVE", "W2_V1", ("1", "1")),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def read(path: Path) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def q(value: Any) -> Fraction:
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, dict) and set(value) == {"num", "den"}:
        return Fraction(int(value["num"]), int(value["den"]))
    raise ValueError(f"unsupported rational spelling: {value!r}")


def eval_expr(expr: Any, labels: dict[str, Fraction]) -> Fraction:
    if isinstance(expr, dict) and set(expr) == {"num", "den"}:
        return q(expr)
    if not isinstance(expr, dict):
        raise ValueError("benchmark parameter expression must be an object")
    if set(expr) == {"const"}:
        return q(expr["const"])
    if set(expr) == {"var"}:
        return labels[expr["var"]]
    if set(expr) != {"op", "args"} or len(expr["args"]) != 2:
        raise ValueError(f"unsupported expression {expr!r}")
    a, b = (eval_expr(x, labels) for x in expr["args"])
    return {"add": lambda: a + b, "sub": lambda: a - b, "mul": lambda: a * b, "div": lambda: a / b}[expr["op"]]()


def rational_pair(value: list[Any]) -> tuple[Fraction, Fraction]:
    if len(value) != 2:
        raise ValueError("expected a two-endpoint interval")
    return q(value[0]), q(value[1])


def physical_input(task: dict[str, Any], action: tuple[str, str]) -> dict[str, Any]:
    return {
        "schema": "ddwmr-g4-w2-canonical-physical-input-v2",
        "task_protocol_sha256": TASK_SHA,
        "formulation": task["model"]["formulation"],
        "traction_law": task["model"]["phi"],
        "lipschitz_constant": task["model"]["lipschitz_constant"],
        "fixed_constants": task["model"]["fixed_constants"],
        "parameter_label_order": task["model"]["fixed_label_order"],
        "parameter_label_bounds": task["model"]["fixed_label_bounds"],
        "parameter_maps": task["model"]["parameter_maps"],
        "label_semantics": task["model"]["label_semantics"],
        "state_order": task["task"]["initial_box_state_order"],
        "initial_box": task["task"]["initial_box"],
        "hold_s": task["task"]["hold_s"],
        "voltage": list(action),
        "obstacle": task["task"]["obstacle"],
        "progress_metric": task["task"]["progress_metric"],
        "required_progress_m": task["task"]["required_progress_m"],
    }


def verify() -> dict[str, Any]:
    task = read(TASK)
    release_path = ROOT / RELEASE
    if sha(release_path) != RELEASE_SHA or sha(ROOT / TASK) != TASK_SHA:
        raise ValueError("peer release/task protocol digest mismatch")
    benchmark = read(PLAN / "benchmark_v2.json")
    protocol = read(PLAN / "protocol_v2.json")
    manifest = read(PLAN / "auer_input_manifest_v2.json")
    if protocol.get("task_protocol", {}).get("sha256") != TASK_SHA or protocol.get("peer_release", {}).get("sha256") != RELEASE_SHA:
        raise ValueError("protocol does not bind exact G2 v6 release and task")
    if task["model"]["fixed_label_order"] != LABELS or task["task"]["initial_box_state_order"] != STATES:
        raise ValueError("unexpected G2 state or label order")
    if benchmark["task_target"]["required_progress_m"] != {"num": "7", "den": "20"}:
        raise ValueError("benchmark progress threshold differs from G2 task")
    if q(benchmark["horizons"][0]["T"]) != q(task["task"]["hold_s"]):
        raise ValueError("horizon mismatch")
    if benchmark["law"] != {"name": "clip", "L_phi": {"num": "1", "den": "1"}}:
        raise ValueError("clip law or Lipschitz constant mismatch")

    label_order = [item["name"] for item in benchmark["parameter_labels"]]
    if label_order != LABELS:
        raise ValueError("parameter-label order differs")
    bound_pair = (Fraction(9999, 10000), Fraction(10001, 10000))
    for item in benchmark["parameter_labels"]:
        if rational_pair(item["range"]) != bound_pair:
            raise ValueError(f"narrowed/changed parameter label {item['name']}")
    if list(benchmark["parameter_cell"]["labels"]) != sorted(LABELS):
        raise ValueError("benchmark full Cartesian label cell has an unexpected key set")
    if any(rational_pair(benchmark["parameter_cell"]["labels"][name]) != bound_pair for name in LABELS):
        raise ValueError("benchmark label cell narrowed or changed")

    state_cell = benchmark["state_cells"][0]
    if state_cell["coordinates"] != STATES or len(state_cell["box"]) != 9:
        raise ValueError("benchmark state coordinate contract differs")
    task_box = [[Fraction(a), Fraction(b)] for a, b in task["task"]["initial_box"]]
    bench_box = [list(rational_pair(pair)) for pair in state_cell["box"]]
    if bench_box != task_box:
        raise ValueError("initial state box differs")
    expected_scene = {
        "id": "scene_v6_static_circle",
        "p_o": [{"num": "1", "den": "2"}, {"num": "1", "den": "10"}],
        "R_s": {"num": "3", "den": "50"},
    }
    if benchmark["scenes"] != [expected_scene]:
        raise ValueError("inflated static obstacle differs")

    # Audit the benchmark's parameter-expression map as exact rational algebra.
    center_labels = {name: Fraction(1) for name in LABELS}
    expected_fixed = {
        "m": Fraction(1), "I_z": Fraction(1), "R_w": Fraction(1), "b": Fraction(1), "v_s": Fraction(1),
        "c_u": Fraction(1), "c_r": Fraction(1), "J_L": Fraction(1), "J_R": Fraction(1),
        "L_L": Fraction(1), "L_R": Fraction(1), "R_L": Fraction(1), "R_R": Fraction(1),
        "B_L": Fraction(1), "B_R": Fraction(1), "k_L": Fraction(1), "k_R": Fraction(1),
        "C_L": Fraction(1), "C_R": Fraction(1),
    }
    mapped = {name: eval_expr(expr, center_labels) for name, expr in benchmark["fixed_parameters"].items()}
    if mapped != expected_fixed:
        raise ValueError(f"benchmark fixed-parameter map does not reproduce G2 nominal parameters: {mapped}")
    gear = benchmark["gear_witness"]
    for side in ("L", "R"):
        g = gear[side]
        labels = {name: Fraction(1) for name in LABELS}
        n = eval_expr(g["n"], labels)
        j_eff = eval_expr(g["J_wheel"], labels) + n * n * eval_expr(g["J_motor"], labels)
        b_eff = eval_expr(g["B_wheel"], labels) + n * n * eval_expr(g["B_motor"], labels)
        k_eff = n * eval_expr(g["k_motor"], labels)
        if (j_eff, b_eff, k_eff) != (Fraction(1), Fraction(1), Fraction(1)):
            raise ValueError(f"{side} gear witness does not map to effective J/B/k=1")

    bindings = {item["external_id"]: item for item in protocol["actions"]}
    auer_cases = {item["comparison_id"]: item for item in manifest["cases"]}
    rows = []
    for v6_id, auer_id, peer_id, auer_action, voltage in PAIRS:
        v6 = bindings.get(v6_id)
        auer = auer_cases.get(auer_id)
        if v6 is None or auer is None:
            raise ValueError(f"missing bijection for {v6_id}/{auer_id}")
        if v6["peer_action_id"] != peer_id or auer["peer_action_id"] != peer_id:
            raise ValueError("peer action mapping is not one-to-one")
        expected_v = [Fraction(x) for x in voltage]
        if [Fraction(x) for x in v6["voltage"]] != expected_v:
            raise ValueError(f"v6 action voltage mismatch {v6_id}")
        payload = auer["payload"]
        if payload["action"]["id"] != auer_action or [q(x) for x in payload["action"]["V"]] != expected_v:
            raise ValueError(f"Auer action voltage mapping mismatch {auer_id}")
        if payload["state_cell"]["coordinates"] != STATES:
            raise ValueError("Auer state order changed")
        if [list(rational_pair(pair)) for pair in payload["state_cell"]["box"]] != task_box:
            raise ValueError("Auer state box changed")
        if payload["horizon"]["T"] != {"num": "2", "den": "1"}:
            raise ValueError("Auer hold changed")
        if payload["scene"] != {"id": "scene_v6_static_circle", "p_o": expected_scene["p_o"], "R_s": expected_scene["R_s"]}:
            raise ValueError("Auer obstacle changed")
        labels = payload["parameter_cell"]["labels"]
        if set(labels) != set(LABELS) or any(rational_pair(labels[name]) != bound_pair for name in LABELS):
            raise ValueError("Auer fixed-label image changed")
        if auer["physical_input_sha256"] != v6["physical_input_sha256"]:
            raise ValueError("method arms do not map to same canonical physical input")
        if auer["physical_input_sha256"] != canonical_sha(physical_input(task, voltage)):
            raise ValueError("canonical physical input digest mismatch")
        rows.append({
            "external_id": v6_id,
            "auer_id": auer_id,
            "peer_action_id": peer_id,
            "voltage": list(voltage),
            "physical_input_sha256": v6["physical_input_sha256"],
            "v6_native_input_sha256": v6["v6_native_binding_input_sha256"],
            # The native Auer file is a separately serialized case.  Keep its
            # file digest distinct from the canonical physical-input digest.
            "auer_native_input_sha256": auer["native_case_sha256"],
            "same_full_state_box": True,
            "same_full_12_label_image": True,
            "same_clip_law_and_fixed_constants": True,
            "same_2s_hold_and_static_circle": True,
            "same_7_20_progress_target": True,
        })
    if len(set(r["physical_input_sha256"] for r in rows)) != 3:
        raise ValueError("each action must have its own canonical digest")
    return {
        "schema": "ddwmr-g4-w2-v6-matched-input-map-preflight-v2",
        "session": "DDWMR | LUNA-G4-AUER",
        "result": "PASS_NONQUERY_MAPPING",
        "task_protocol_sha256": TASK_SHA,
        "peer_release_sha256": RELEASE_SHA,
        "benchmark_sha256": sha(ROOT / PLAN / "benchmark_v2.json"),
        "action_count": 3,
        "label_count": 12,
        "state_count": 9,
        "true_side_labels_independent": True,
        "reference_symmetry_not_imposed_on_true_label_vectors": True,
        "exact_parameter_expression_map_checked": True,
        "gear_witness_checked_exactly": True,
        "rows": rows,
        "fresh_native_calls": 0,
    }


if __name__ == "__main__":
    result = verify()
    out = ROOT / "results/validation/autonomous_w2/g4/matched_v6_task_development_v2/mapping_preflight_v2.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, sort_keys=True))
