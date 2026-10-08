"""Versioned non-query mapping receipt for the W2 matched-task freeze."""
from __future__ import annotations

import json
from validation.autonomous_w2.g4.preflight_mapping_v2 import ROOT, verify


def main() -> int:
    result = verify()
    out = ROOT / "results/validation/autonomous_w2/g4/matched_v6_task_development_v2/mapping_preflight_v3.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "rows"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
