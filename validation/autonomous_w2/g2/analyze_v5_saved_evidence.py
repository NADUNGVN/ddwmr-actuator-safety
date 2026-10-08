from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/validation/autonomous_w2/g2/v5_saved_evidence_summary_v1.json'
if OUT.exists():
    raise FileExistsError('SUMMARY_ALREADY_EXISTS')
rows = {}
for attempt, action in enumerate(('ZERO','NOMINAL','ALTERNATIVE'), start=1):
    path = ROOT / f'results/validation/autonomous_w2/g2/development_v5/attempt_{attempt:02d}_W2_G2_DEV_001_{action}/row.json'
    row = json.loads(path.read_text(encoding='utf-8'))
    valid = [slab for slab in row['slabs'] if slab['clip_interior']['proved_strict']]
    first_bad = next((slab for slab in row['slabs'] if not slab['clip_interior']['proved_strict']), None)
    widths = {}
    if valid:
        for name, bounds in valid[-1]['internal_endpoint_range'].items():
            lo, hi = map(Fraction, bounds)
            widths[name] = {'width_exact': str(hi-lo), 'width_decimal': float(hi-lo)}
    rows[action] = {
        'status': row['safety_status'],
        'reason_codes': row['reason_codes'],
        'slab_count': len(row['slabs']),
        'clip_proved_prefix_slab_count': len(valid),
        'first_clip_failure': None if first_bad is None else {
            'index': first_bad['index'],
            'start_s': first_bad['start_s'],
            'beta_upper': first_bad['clip_interior']['beta_upper'],
            'beta_decimal': [float(Fraction(x)) for x in first_bad['clip_interior']['beta_upper']],
        },
        'minimum_contact_margin_on_proved_clip_prefix_N': None if not valid else str(min(Fraction(s['contact']['margin_lower_N']) for s in valid)),
        'minimum_collision_margin_on_proved_clip_prefix_m': None if not valid else str(min(Fraction(s['collision']['margin_lower_m']) for s in valid)),
        'endpoint_width_after_last_proved_clip_slab': widths,
        'full_row_contact_margin_lower_N': row['contact_margin_lower_min_N'],
        'full_row_collision_margin_lower_m': row['collision_margin_lower_min_m'],
        'full_row_progress_m': row['progress_enclosure_m'],
        'full_row_progress_decimal_m': [float(Fraction(x)) for x in row['progress_enclosure_m']],
        'operation_count': row['arithmetic']['interval_operations'],
        'max_rational_bits': row['arithmetic']['max_rational_bits'],
    }
witness = json.loads((ROOT / 'results/validation/autonomous_w2/g2/clip_branch_point_witness_v1.json').read_text(encoding='utf-8'))
point_actions = {}
for name, action in witness['actions'].items():
    slips = [Fraction(s['absolute_slip_upper']) for s in action['slabs']]
    point_actions[name] = {
        'all_slabs_strictly_inside_clip': action['all_slabs_strictly_inside_clip'],
        'maximum_slab_absolute_slip_upper': str(max(slips)),
        'maximum_slab_absolute_slip_decimal': float(max(slips)),
        'progress_enclosure_m': action.get('progress_enclosure_m'),
    }
summary = {
    'schema': 'G2_W2_V5_SAVED_EVIDENCE_SUMMARY_v1',
    'session': 'DDWMR | LUNA-G2-SCOPE',
    'classification': 'read-only analysis of saved development proof rows and existing exact point witness; no query, worker, or native attempt',
    'rows': rows,
    'exact_center_point_branch_witness': point_actions,
    'point_witness_interpretation': witness.get('interpretation'),
    'native_attempts_added': 0,
}
OUT.write_text(json.dumps(summary, sort_keys=True, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary, sort_keys=True, indent=2))
