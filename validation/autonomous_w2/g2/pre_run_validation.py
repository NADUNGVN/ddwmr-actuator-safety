"""Capture reproducible non-query fixture/screen evidence before development rows."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .fixtures import run as run_g2_fixtures
from .prepare_r3_baseline_v1 import prepare as verify_r3_preparation
from .r3_input_fixtures import verify as verify_r3_inputs


ROOT = Path(__file__).resolve().parents[3]
OUT_REL = "results/validation/autonomous_w2/g2/pre_run_validation_v1.json"


def capture_module(module: str) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, "-m", module],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
        env={**__import__("os").environ, "PYTHONHASHSEED": "0", "PYTHONUTF8": "1"},
    )
    return {
        "command": f"python -m {module}",
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "stdout_sha256": hashlib.sha256(proc.stdout.encode("utf-8")).hexdigest(),
        "stderr_sha256": hashlib.sha256(proc.stderr.encode("utf-8")).hexdigest(),
    }


def run() -> dict[str, Any]:
    checks = {
        "g2_analytic_fixtures": {"command": "python -m validation.autonomous_w2.g2.fixtures", "exit_code": 0, "results": run_g2_fixtures()},
        "r3_input_nonquery_fixtures": verify_r3_inputs(),
        "r3_preparation_idempotence": verify_r3_preparation(),
        "analytic_point_screen": capture_module("validation.autonomous_w2.g2.analytic_task_screen"),
    }
    if checks["analytic_point_screen"]["exit_code"] != 0:
        raise RuntimeError("ANALYTIC_POINT_SCREEN_FAILED")
    report = {
        "schema": "G2_W2_PRE_RUN_VALIDATION_v1",
        "session": "DDWMR | LUNA-G2-SCOPE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "native_attempts_before_receipt": 0,
        "held_out_rows": 0,
        "legacy_800_row_study": "NOT_RUN",
        "checks": checks,
        "prior_nonquery_failures": [
            {
                "command": "python -m validation.autonomous_w2.g2.fixtures",
                "status": "FAILED_THEN_CORRECTED",
                "failure": "AssertionError at fixtures.py's exact-point expectation matrix[0][0] == I.point(-3); the coefficient is an interval because C_L and C_R have positive width.",
                "correction": "Assertions now require interval containment of nominal signed coefficients; the voltage-current coefficient is checked as a positive interval containing 1, because it is 1/lambda_L.",
                "captured_terminal_trace": [
                    "File \"validation/autonomous_w2/g2/fixtures.py\", line 34, in run",
                    "assert matrix[0][0] == I.point(-3)",
                    "AssertionError",
                ],
            },
            {
                "command": "python -m validation.autonomous_w2.g2.r3_input_fixtures",
                "status": "FAILED_THEN_CORRECTED",
                "failure": "TypeError from Fraction(string_num, string_den) while checking the nine positive-width input coordinates.",
                "correction": "Convert the JSON numerator/denominator strings to integers before constructing Fraction.",
                "captured_terminal_trace": [
                    "File \"validation/autonomous_w2/g2/r3_input_fixtures.py\", line 23, in <genexpr>",
                    "Fraction(pair[0][\"num\"], pair[0][\"den\"]) < Fraction(pair[1][\"num\"], pair[1][\"den\"])",
                    "TypeError: both arguments should be Rational instances",
                ],
            },
        ],
    }
    output = ROOT / OUT_REL
    if output.exists():
        raise FileExistsError("PRE_RUN_VALIDATION_RECEIPT_ALREADY_EXISTS")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
