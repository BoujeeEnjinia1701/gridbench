---
doc_id: GBN-DEC-001
title: GridBench design decisions register
project: GridBench
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions, items to confirm, value engineering and decisions made to date
---

# GridBench design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, GBN-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Review of the design-for-construction changes (bolt and cross dowel frame joints, notched rail, shorter shelf, worktop brackets, tile pocket and fixing, T-nuts, fixtures on threaded positions, arm clamps, wall anchor) | (a) accept as recorded; (b) amend named changes | (a): none changes what the bench does, its pitch or its safety case | The whole build plan follows them | GBN-DDR-003 |
| 2 | Clamp rating at the 122 screw-in positions over the frame, where R7 is not met (pull-out factor 0.57 to 0.92) | (a) rate them light duty at 0.92 N·m (296 to 493 N at the part) and mark them on the worktop; (b) move the insert sub-grid off the frame lines; (c) relax R7 at those positions | (a) | How the worktop is marked; safety stop S5 | GBN-DDR-002, O4; GBN-CAL-001 [G5e] |
| 3 | Racking stiffness of the frame | (a) end low rails between the legs at each end; (b) screw the shelf down to the low rails; (c) leave as is until a TRL 4 push test | None yet | Steps 4 and 7 | GBN-DDR-002, O3 |
| 4 | First workshops and regions for co-design | Workshops and regions to approach first | None yet | Not part of the TRL 3 build | GBN-DDR-001, O1 |
| 5 | Wall anchor angles in the product renders | (a) leave them out of the renders and keep them in the model, drawing and BOM; (b) render them with a wall | (a) | None (renders only) | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 6 | Full hole pattern in the renders, representative patch in the exported CAD | (a) keep the split; (b) export every hole | (a): the full pattern makes very large STEP and STL files | None (renders and exports only) | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 7 | Appearance-only details in the renders (index ticks, name plate, bolt heads, knobs, sample block and bar) | (a) render detail only; (b) adopt them into the design and the BOM | (a) | None unless adopted | `docs/REVIEW.md`, 2026-09-26, item 4 |

The fourth appearance item of 2026-09-26, the toe clamp screws on tile holes, is settled by GBN-DDR-003: the model now puts them there too.

## To confirm when parts are bought

*Table 2. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The tile offcut's real thickness, flatness and price | The packers are planed to suit its thickness; R5 depends on its flatness; the USD 28 price is unverified | GBN-CAL-001; BOM line 6 |
| 2 | The plywood's real thickness | Packer thickness and the 15 to 18 mm screw reach below the surface both assume 18 | GBN-DDR-003, P6 and P9 |
| 3 | The tee nut's flange (19), barrel (9.5) and hole size (8.0), and the screw-in insert's hole size (8.5) | The worktop is drilled to these sizes before the parts can be tried | BOM line 5 |
| 4 | The M8 cross dowel's diameter (10) and the bolt length (120) | They set the cross dowel holes and how far the bolt reaches into the member | GBN-DDR-003, P1 |
| 5 | The levelling foot thread and the T-nut's barrel size | They set the 12 mm bore in the leg end | GBN-DDR-003, P8 |
| 6 | The 20 x 40 extrusion's core hole size | The post is held by M5 screws tapped into its core holes | GBN-DDR-003, P10 |
| 7 | A sourced figure for plywood in-plane moisture movement | R3 uses an unsourced 0.007 % per % moisture content | GBN-CAL-001 [E2] |
| 8 | Whether the tile can be drilled to ±0.05 without CNC, with a drilling jig on a drill press | R4 hole position cannot be verified on paper | GBN-PRC-001, Open questions |

## Value engineering

Value-engineering target: USD 250 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 268.40 (USD 18.40 over the target) for the core parts, from `bom/bom.csv` [K3], [K4]; with the user-supplied dial indicator and the optional wall anchor, USD 288.40. Main cost drivers and savings worth trying:

- **Frame, USD 57.00.** About USD 33.60 of timber and USD 23.40 of bolts, cross dowels and screws [K2]. Worth trying: one bolt instead of two at each low rail end (about USD 3.20); bolts and cross dowels bought as a bulk furniture-fitting pack; or a glued and screwed frame (about USD 15 less, but it no longer comes apart).
- **Worktop, USD 45.00.** A half sheet of birch plywood plus router wear. Worth trying: a full sheet shared with the shelf, or a cheaper sheet faced only on the top.
- **Threaded inserts, USD 28.20.** Worth trying: a bulk price for tee nuts and inserts; leaving the 122 screw-in positions as plain holes if decision 2 rates them light duty anyway.
- **Precision tile, USD 28.00.** An unverified offcut price. Worth trying: offcut dealers' minimum-cut prices; a 250 x 250 tile if the fixture library allows.
- **Instrument post and arm, USD 15.00, and fastener kit, USD 14.00.** Worth trying: steel bar and screws from bulk stock.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items A1 to A10: cost options (dial indicator user-supplied, tile as an offcut), 25 mm M6 grid, two zones, 50 mm insert sub-grid, bolted timber frame, printed PETG fixtures, ballast plus optional wall anchor, fixture metadata block, CERN-OHL-S-2.0 fixture library, tile at the right | Amish: "i accept all your recommendations, go with them across all repos." | GBN-DDR-001, GBN-DDR-002 |
| 2026-09-25 | `budget_usd` raised from USD 220 to USD 250 (O2) | Amish, same instruction | GBN-DDR-002 |
| 2026-09-25 | Flanged tee nuts from the underside, screw-in inserts only over the frame (D1); 45 x 120 mm aprons (D2); rubber-padded feet (D3) | Amish, same instruction | GBN-DDR-002 |
| 2026-09-30 | Build plan format approved; outstanding decisions kept in this register, not the build plan; the design to be made physically buildable as the pictures are drawn | Amish: "this is the correct build plan ... this is a good quality document format. Extend this across all the other repos"; "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | GBN-BLD-001, GBN-DDR-003 |
| 2026-10-01 | `budget_usd` is a hypothetical value-engineering target, not a limit; cost is reported as over or under it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering |
