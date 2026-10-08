"""One W2 G2 numeric worker. Output is one self-contained JSON row on stdout."""
from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path

from .producer_v2 import ArithmeticLimit, InvalidInput, evaluate_bound_row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--action-id", required=True)
    args = parser.parse_args()
    binding_path = Path(args.binding)
    if not binding_path.is_absolute():
        binding_path = Path.cwd() / binding_path
    try:
        binding = json.loads(binding_path.read_text(encoding="utf-8"))
        record = evaluate_bound_row(binding, args.action_id)
    except InvalidInput as exc:
        record = {"schema": "G2_W2_WORKER_FAILURE_v1", "status": "INVALID_INPUT", "reason_code": str(exc)}
    except ArithmeticLimit as exc:
        record = {"schema": "G2_W2_WORKER_FAILURE_v1", "status": "RESOURCE_UNKNOWN", "reason_code": str(exc)}
    except BaseException as exc:
        record = {
            "schema": "G2_W2_WORKER_FAILURE_v1",
            "status": "EXECUTION_FAILURE",
            "reason_code": f"{type(exc).__name__}:{exc}",
            "traceback": traceback.format_exc(limit=8),
        }
    sys.stdout.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
