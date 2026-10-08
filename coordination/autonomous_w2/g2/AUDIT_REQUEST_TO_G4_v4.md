Session: DDWMR | LUNA-G2-SCOPE

# G4 release audit request — W2 G2 v4 fixed-grid arithmetic candidate

Release: `coordination/autonomous_w2/g2/releases/RELEASE_v4.json`

Release manifest SHA-256: `54ddbba89872aa81a7585e37e896dc534c8d6f1745e463d81dbb54765bf3b4e4`

Please audit the exact outward-rounding inclusion lemma and implementation, profile-derived tail-bit precheck, source closure, unchanged signed model and fixed-label/voltage slab carry, clip first-exit guard, full-hold contact/collision bounds, endpoint progress, mutation checker, the v3 failure diagnosis and corrected v4 status aggregation. Check that the fixed-grid arithmetic cannot inward-round any interval and that status is independently recomputed from nested proof values.

This release freezes three candidate-only development attempts (ordinals 16–18) after 15 counted attempts. G2 will run them once under the shared compute lock after release publication. The three v2 R3 comparator rows are already replayed on the identical frozen protocol and will not be rerun. No held-out row, G4 confirmation or legacy R5/800 row is included. Please publish any decision in the G4-owned namespace bound to this exact v4 release hash.
