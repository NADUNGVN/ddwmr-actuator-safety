"""Write the new-version all-path/all-hash non-query preflight receipt."""
from __future__ import annotations

import json
from validation.autonomous_w2.g4.preflight_bindings_v2 import PROJECT, RESULT_REL, verify
from validation.autonomous_w2.g4.matched_v6_common_v2 import write_json


def main() -> int:
    report = verify()
    write_json(PROJECT / RESULT_REL / "binding_preflight_v3.json", report, max_bytes=1_048_576, exclusive=True)
    print(json.dumps({key: value for key, value in report.items() if key != "pairs"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
