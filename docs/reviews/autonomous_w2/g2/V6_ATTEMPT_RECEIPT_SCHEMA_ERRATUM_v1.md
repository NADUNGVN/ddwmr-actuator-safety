Session: DDWMR | LUNA-G2-SCOPE

# Erratum — G2 v6 terminal attempt receipts use the intent schema label

**Issued:** 2026-10-08. **Disposition:** interpretive correction only. No evidence bytes or source files were changed.

## Correction

The three terminal `attempt_receipt.json` files and the three corresponding terminal records nested in `stage_receipt.json` reuse the schema label `G2_W2_V6_ATTEMPT_INTENT_v1`. That label is incorrect for terminal records: it belongs on the separate `attempt_intent.json` launch-intent files. The affected objects contain terminal fields including `status: REPLAYED`, safety/task outcomes, row and replay hashes, checker/worker accounting, and reason codes. Read them as terminal receipts, not as launch intents.

This erratum does not assign a replacement schema identifier and does not rewrite the historical JSON. The separate `attempt_intent.json` objects keep their existing intent interpretation.

## Byte and binding preservation

The receipt bytes, saved rows, replay outputs, source, bindings, source-closure pins, and attempt counts remain unchanged. The SHA-256 values below identify the original receipt bytes exactly:

| Terminal object | SHA-256 |
|---|---|
| `results/validation/autonomous_w2/g2/development_centered_v6/attempt_01_W2_G2_DEV_001_ZERO/attempt_receipt.json` | `3a4cdb69facdd07b4be3126114e467f8dcb58ea91d1af7a7ad93852b03f87f83` |
| `results/validation/autonomous_w2/g2/development_centered_v6/attempt_02_W2_G2_DEV_001_NOMINAL/attempt_receipt.json` | `13a27d0af11db3c3080e3c695225dbf4fa9b68db1331fb39c992709c132186a5` |
| `results/validation/autonomous_w2/g2/development_centered_v6/attempt_03_W2_G2_DEV_001_ALTERNATIVE/attempt_receipt.json` | `83c19513e4b48bd6aa18e9521369366799d359e5ed740ec1771d993dd5e1fa7b` |
| `results/validation/autonomous_w2/g2/development_centered_v6/stage_receipt.json` (includes the same three nested terminal records) | `9b906c008af8ff51f92bb55d4f1fe072f9a4ebdc48f4caf64c29feec58f0aa36` |

The associated native rows and replay records remain pinned by their receipt fields and by G2 release v6, SHA-256 `789d6b371f3a74c1f5241d08d187956e549bc2776648145869754971e16b8e55`. No proof or source binding is changed by correcting the interpretation of the schema label.

## Accounting remains unchanged

- G2 native attempts: **24/24 consumed**; the v6 stage contributes three counted attempts.
- G4's prior v6 wrapper attempt: one worker attempt before its producer marker, **zero native calls**; this is counted separately from G2.
- R5 study: **800/800 NOT_RUN**. Auer 1,944-query batch: `NOT_RUN`.

Downstream reports should call the affected records terminal receipts and preserve the original hashes above. No historical artifact needs to be regenerated for this correction.
