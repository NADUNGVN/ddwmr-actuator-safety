# Bibliographic erratum — Auer method contract v2

**Date:** 2026-10-01  
**Scope:** Rauh–Auer 2011 citation metadata only  
**Disposition:** correction sidecar; `G4_AUER_METHOD_CONTRACT_v2.md` remains byte-for-byte unchanged.

## Finding

The DOI `10.1007/s11128-010-0165-6` printed in method-contract v2 is not supported by the primary Reliable Computing issue and article evidence inspected for the R5 review. A failed DOI lookup is not proof that no DOI exists, so this erratum records the DOI as **unverified** and omits it from the corrected reference.

## Verified reference and source

A. Rauh and E. Auer, “Verified Simulation of ODEs and DAEs in ValEncIA-IVP,” *Reliable Computing* **15(4)**, 370–381 (2011). Official publisher PDF: <https://www.reliable-computing.org/reliable-computing-15-pp-370-381.pdf>.

The official PDF URL returned HTTP 200 with `Content-Type: application/pdf`. The saved source at `research/third_party/auer2013/references/rauh-auer-2011-valencia.pdf` is byte-identical to that official download (640,240 bytes; SHA-256 `1405b54eaa25c5d3874af74ac71087364f3a84ddada675c336e378779e902265`). Its printed header identifies *Reliable Computing* 15 and the title page is printed page 370. Printed pages 371–372 contain Algorithm 1 and Eqs. (3)–(6), the residual iteration and integrated error enclosure used as the method locator.

## Consequence and binding

This is a bibliography-only correction. The mathematical method clauses, equation locators, implementation contract, and all frozen R4/R5 outputs are unchanged. The R4/R5 producer/replay provenance remains bound to the exact v2 method-contract bytes (SHA-256 `2a5d74de613ccf5f716035732b31ee1dcca69ad3d11d45d1d1267a517a63fc63`). A future matched batch may bind those same bytes together with this erratum as separate metadata; the erratum is not a new proof premise and does not retroactively relabel any R4/R5 proof as a v3 proof.

**Status:** metadata correction verified against the official PDF; DOI remains unverified and is omitted.
