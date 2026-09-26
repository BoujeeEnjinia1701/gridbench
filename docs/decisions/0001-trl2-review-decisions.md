---
doc_id: GBN-DDR-001
title: GridBench TRL 2 review decisions
project: GridBench
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 work, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted in part. On 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." Items A1 to A10 and O2 are decided by Amish, 2026-09-25: go with recommendation (see GBN-DDR-002). Item O1 has no recommendation and remains "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis GBN-PRC-001 v0.2 listed six key design choices, each with options and a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carries a recommendation is therefore adopted as recommended for TRL 3 under that instruction and stays open for his review. Items without a recommendation stay open, and no new budget figure is applied.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in GBN-PRC-001 v0.2, Key design choices and Cost.

## Decision

*Table 1. Items adopted as recommended.*

| # | Item | Adopted recommendation | Status |
| --- | --- | --- | --- |
| A1 | Budget and cost options | Options (a) and (b): the dial indicator is user-supplied and outside the parts budget, and the tile is bought as offcut stock. R10 is redefined to cover the bench, grid, tile and fixture set without the indicator. Option (c), raising `budget_usd` to $250, was the fallback; it is decided under O2. | Decided by Amish, 2026-09-25: go with recommendation |
| A2 | Grid standard | 25 mm pitch, M6, compatible with metric optical breadboards; a heavy 50 mm variant to be considered later | Decided by Amish, 2026-09-25: go with recommendation |
| A3 | Worktop zones | Two zones: a plywood field plus a 300 x 300 mm aluminum precision tile on the same grid | Decided by Amish, 2026-09-25: go with recommendation |
| A4 | Insert spacing | M6 inserts on the 50 mm sub-grid; plain 6.6 mm holes between them for pins | Decided by Amish, 2026-09-25: go with recommendation |
| A5 | Frame | Bolted timber for the prototype; welded steel as a documented variant | Decided by Amish, 2026-09-25: go with recommendation |
| A6 | Fixture bodies | Printed PETG with metal dowels, screws and tile; a machined option for heavily used jigs | Decided by Amish, 2026-09-25: go with recommendation |
| A7 | Stability fix | Ballast on the shelf plus an optional wall anchor bracket | Decided by Amish, 2026-09-25: go with recommendation |
| A8 | Fixture file convention | A short fixture metadata block in each build123d file giving the grid footprint and datum | Decided by Amish, 2026-09-25: go with recommendation |
| A9 | Fixture library license | Keep CERN-OHL-S-2.0, as for all hardware in the portfolio | Decided by Amish, 2026-09-25: go with recommendation |
| A10 | Tile position | At the right of the worktop, leaving the left 800 mm free for large parts | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items listed as open in v0.1.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First workshops and regions for co-design. No recommendation was made and no preference is stated, so none is chosen here. | Proposed, awaiting Amish |
| O2 | Raise `budget_usd` from $220 to $250 (cost option c). Recommended at TRL 2 only as the fallback if offcut prices do not hold. GBN-CAL-001 v0.1 showed core parts at $239.20, so the fallback was needed for R10 to be met. `budget_usd` is now $250 in `project.yaml`. | Decided by Amish, 2026-09-25: go with recommendation |

## Consequences

- Update, v0.2: the consequences of Amish's 2026-09-25 acceptance, including the $250 budget and the design changes, are recorded in GBN-DDR-002. The bullets below describe v0.1.

- `project.yaml`: unchanged apart from the TRL fields. `budget_usd` stays at $220. No pitch or problem rewording was recommended, so none was applied.
- GBN-PRB-001, GBN-PRC-001 and GBN-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed". R10 now excludes the user-supplied dial indicator (A1). R12 is assessed with the ballast in place (A7).
- The TRL 3 calculations (GBN-CAL-001) led to four detail changes within these choices: a deeper printed toe clamp with a rated torque of 1.6 N·m, one round and one diamond locating pin per precision fixture, the fence printed in two 190 mm segments, and two concrete slabs as the ballast. With them the core parts cost $239.20.
- GBN-CAL-001 shows R10 not met at $220 (met at the $250 fallback, O2) and R7 not met on the plywood field because of insert pull-out. Options for R7 are proposed in `docs/REVIEW.md` and await Amish; this record does not decide them.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
