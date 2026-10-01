"""Create the R4 source-hash-bound manifest for the unchanged exact-rational backend."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "validation/baselines/auer2013"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    source_functions = [
        ("validation/g2/rational.py", ["Budget", "Interval", "parse_q", "qobj"]),
        ("validation/g2/interval.py", ["interval_sine", "interval_cosine", "sqrt_lower"]),
        ("validation/baselines/auer2013/piecewise.py", ["clip_value", "clip_interval", "clip_derivative_interval", "DualInterval"]),
        ("validation/baselines/auer2013/rhs.py", ["augmented_rhs", "DDWMR interval RHS and Jacobian"]),
        ("validation/baselines/auer2013/residual_ivp.py", ["Auer residual derivative iteration", "outward integral bound", "native full-time tube"]),
        ("validation/baselines/auer2013/replay_ivp.py", ["independent local interval AD", "native proof replay", "inclusion recomputation"]),
        ("validation/baselines/auer2013/r4_worker.py", ["resource-budgeted execution", "record binding", "one common predicate call"]),
        ("validation/baselines/auer2013/process_limiter.py", ["Windows Job Object process-memory limit", "hard wall timeout"]),
    ]
    sources = [{"path": name, "sha256": sha256(ROOT / name), "covered_functions": covered} for name, covered in source_functions]
    python_hash = sha256(Path(sys.executable).resolve())
    method_path = ROOT / "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md"
    profile_v1 = BASELINE / "small_case_resource_profile_v1.json"
    profile_v2 = BASELINE / "small_case_resource_profile_v2.json"
    manifest = {
        "schema": "ddwmr-g4-auer-arithmetic-backend-manifest-v2",
        "backend_id": "DDWMR_EXACT_RATIONAL_TAYLOR_INTERVAL_V1",
        "status": "R4_LOCAL_SOURCE_BOUND_CANDIDATE; independent proof replay implemented; external scientific review pending",
        "manifest_hash_semantics": "SHA-256 over exact file bytes; this file does not contain its own digest.",
        "python_runtime": {
            "executable": Path(sys.executable).resolve().as_posix(),
            "version": sys.version,
            "implementation": platform.python_implementation(),
            "executable_sha256": python_hash,
            "compiler_reported_by_interpreter": platform.python_compiler(),
            "project_compile_command": None,
            "project_link_flags": [],
            "reason": "Python exact-rational source; no native Auer executable or project compile/link step.",
        },
        "numeric_model": {
            "endpoint_representation": "reduced exact signed numerator / positive denominator",
            "rounding_mode": "exact rational arithmetic; no binary floating-point proof endpoints",
            "working_precision": "exact rationals bounded by the frozen rational bit/operation profile",
            "max_rational_bits": 32768,
            "division_domain": "reject if the divisor interval contains zero",
            "serialization": "exact rational numerator/denominator pairs",
            "nonfinite_values": "not representable as accepted proof endpoints",
        },
        "transcendental_contract": {
            "sin_cos": "exact rational Taylor polynomials with global Lagrange remainder and safe intersection with [-1,1]; no host libm or argument reduction",
            "sqrt": "exact rational bisection and square comparisons for the common predicate checker",
            "range_widening": "broad enclosures are accepted only if inclusion closes; otherwise UNKNOWN/resource stop",
            "unsafe_fallback": "none",
        },
        "method_and_profile": {
            "method_contract_path": "docs/reviews/G4_AUER_METHOD_CONTRACT_v2.md",
            "method_contract_sha256": sha256(method_path),
            "resource_profile_v1_path": "validation/baselines/auer2013/small_case_resource_profile_v1.json",
            "resource_profile_v1_sha256": sha256(profile_v1),
            "active_resource_profile_path": "validation/baselines/auer2013/small_case_resource_profile_v2.json",
            "active_resource_profile_sha256": sha256(profile_v2),
            "process_limit": "Windows Job Object process commit-memory limit plus parent monotonic hard timeout",
        },
        "proof_critical_source_files": sources,
        "independence_boundary": {
            "producer_and_checker_are_separate_modules": True,
            "checker_imports_producer": False,
            "checker_imports_producer_ddwmr_rhs": False,
            "shared_exact_arithmetic_sources": ["validation/g2/rational.py", "validation/g2/interval.py"],
            "shared_dependency_with_g2_and_r3": True,
            "independent_arithmetic_library": False,
        },
        "excluded_backend": {
            "name": "PROFIL/BIAS 2.0.8 x86-64 with host glibc/libm sine/cosine",
            "reason": "unresolved all-input directed transcendental error contract; finite probes do not certify all arguments",
            "used_for_r4_proof_output": False,
        },
        "software_reproduction_claim": "paper-faithful Auer 2013 method reconstruction; not original VALENCIA software or binary reproduction",
    }
    destination = BASELINE / "ARITHMETIC_BACKEND_MANIFEST_v2.json"
    raw = (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    destination.write_bytes(raw)
    print(json.dumps({"path": str(destination), "sha256": hashlib.sha256(raw).hexdigest(), "source_count": len(sources)}, sort_keys=True))


if __name__ == "__main__":
    main()

