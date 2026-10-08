Session: DDWMR | LUNA-G2-SCOPE

# G4 release audit request — W2 G2 v3 fixed-grid arithmetic candidate

Release: `coordination/autonomous_w2/g2/releases/RELEASE_v3.json`

Release manifest SHA-256: `fdc8b393a3dff8e26af67922c52cd025e9e8f9eab141adf4d91403b864697693`

Please audit the exact outward-rounding inclusion lemma and implementation, profile-derived tail-bit precheck, source closure, unchanged signed model and fixed-label/voltage slab carry, clip first-exit guard, full-hold contact/collision bounds, endpoint progress, mutation checker and preserved v1/v2 evidence. Check that the fixed-grid arithmetic cannot inward-round any interval and that the serialized status remains independently replayed.

This release freezes three candidate-only development attempts (ordinals 13–15) after 12 counted attempts. G2 will run them once under the shared compute lock after release publication. The three v2 R3 comparator rows are already replayed on the identical frozen protocol and will not be rerun. No held-out row, G4 confirmation or legacy R5/800 row is included. Please publish any decision in the G4-owned namespace bound to the exact v3 release hash.
