---
doc_id: GBN-DDR-002
title: GridBench recommendations accepted
project: GridBench
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'O1, O3 and O4 decided by Amish on 2026-10-02'
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below that carried a recommendation is decided by Amish, 2026-09-25: go with recommendation. Items without a recommendation remained "Proposed, awaiting Amish" until Amish decided them on 2026-10-02 ("i approve your recommendations for all 555 open decisions.").

## Context

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Before that, GBN-DDR-001 v0.1 had adopted items A1 to A10 for TRL 3 work, open for his review, and left O1 and O2 open; the TRL 3 review note (`docs/REVIEW.md`, session 2026-09-25, TRL 3) added a recommendation on R7 and three suggestions. This record lists what is now decided, what changed in the repo and what stays open. TRL 4 remains on hold by Amish's instruction, and nothing here authorizes building, testing or purchasing.

## Options considered

The options for each item are those in `docs/REVIEW.md` (sessions 2026-09-25, /populate and TRL 3), GBN-DDR-001 and GBN-CAL-001 v0.1. Where an item offered several options, the recommended option is the decision.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| A1 | Cost options (DDR-001) | Dial indicator user-supplied; tile bought as offcut; R10 excludes the indicator | Already applied at TRL 3; status wording updated |
| A2 | Grid standard | 25 mm pitch, M6 | Status wording only |
| A3 | Worktop zones | Plywood field plus aluminum precision tile | Status wording only |
| A4 | Insert spacing | 50 mm sub-grid | Status wording only |
| A5 | Frame | Bolted timber; welded steel as a documented variant | Status wording only |
| A6 | Fixture bodies | Printed PETG with metal pins, screws and tile; machined option | Status wording only |
| A7 | Stability fix | Ballast on the shelf plus optional wall anchor | Status wording only |
| A8 | Fixture file convention | Metadata block giving grid footprint and datum | Status wording only |
| A9 | Fixture library license | CERN-OHL-S-2.0 | Status wording only |
| A10 | Tile position | Right of the worktop | Status wording only |
| O2 | Budget | Raise `budget_usd` from $220 to $250 | `project.yaml` $220 to $250; R10 target $250; core parts $245.90, R10 now met on paper ($4.10 margin) |
| D1 | R7 on the plywood field (TRL 3 review, option a) | Flanged M6 tee nuts pressed in from the underside; screw-in inserts kept where a frame member lies below | Model: 130 tee nuts (19 mm flange, 8.0 mm hole) and 122 screw-in inserts; BOM line 5 $25.20 to $27.80; GBN-CAL-001 G5b to G5d; R7 met on paper at 130 positions |
| D2 | Frame stiffness (TRL 3 review suggestion) | 45 x 120 mm aprons instead of 45 x 95 mm | Model and GA; deflection under 500 N 0.49 mm to 0.37 mm; bench 40.2 kg to 41.9 kg; frame $41.40 to $43.50 |
| D3 | Sliding (TRL 3 review suggestion) | Rubber pads on the levelling feet | Model and GA; BOM line 2 $2.00 to $2.50 each; empty sliding force 82 N on hard feet, 206 N on rubber pads |

Knock-on figures from GBN-CAL-001 v0.2: tipping force 107 N to 112 N empty and 176 N to 181 N ballasted; core parts $239.20 to $245.90.

*Table 2. Items left open on 2026-09-25, decided by Amish on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First workshops and regions for co-design. No recommendation was made. | Decided by Amish, 2026-10-02: makerspaces or technical colleges that have a CNC router and teach fixturing; first candidate to approach, a member lab of the Fab Lab network |
| O3 | Racking stiffness: end low rails or a screwed-down shelf. The TRL 3 review named both without recommending one, and no requirement covers racking yet. | Decided by Amish, 2026-10-02: screw the shelf down to the low rails now; push-test at TRL 4 and add end low rails only if the frame still sways |
| O4 | New: the 122 screw-in insert positions that sit over a frame member, where R7 is still not met (pull-out factor 0.57 to 0.92). Options: (a) rate them light duty at 0.92 N·m, giving 296 to 493 N at the part (GBN-CAL-001, G5e), and mark them on the worktop; (b) move the insert sub-grid off the frame lines; (c) relax R7 at those positions. Recommendation: (a). | Decided by Amish, 2026-10-02: (a), with the positions marked in a contrasting colour and the rating stated in the fixture library notes |

## Consequences

- `project.yaml`: `budget_usd` $250. No pitch or problem rewording was recommended, so none was applied. `trl` and `trl_target` stay at 3.
- GBN-PRB-001, GBN-PRC-001 and GBN-REQ-001 are revised to v0.4, GBN-CAL-001 to v0.2 and GBN-DDR-001 to v0.2. Drawing GBN-DWG-001 is at Rev P2. The concept media are re-rendered.
- Requirement status (GBN-CAL-001 v0.2): 1 not met in part (R7 at the 122 positions over the frame), 2 at risk (R3, R4), 1 not verifiable at TRL 3 (R5), 5 met on paper (R6, R8, R9, R10, R12), 3 met by design (R1, R2, R11).
- No cross-repo action arises from these decisions.
- On hold as TRL 4 work: pull tests of tee nuts and inserts, the tipping and sliding push tests with rubber pads, and any purchasing.
