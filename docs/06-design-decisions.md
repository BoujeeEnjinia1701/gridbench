---
doc_id: GBN-DEC-001
title: GridBench design decisions register
project: GridBench
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions, items to confirm, value engineering and decisions made to date
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Amish approved the recommendations for all seven open decisions (2026-10-02); GBN-DDR-003 accepted; moved to decisions made; plain-hole saving withdrawn from value engineering'
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Value engineering updated for the shelf screws and light-duty marking added to carry out decisions 2 and 3'
---

# GridBench design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, GBN-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

Value-engineering target: USD 250 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 272.20 (USD 22.20 over the target) for the core parts, from `bom/bom.csv` [K3], [K4]; with the user-supplied dial indicator and the optional wall anchor, USD 292.20. The shelf screws and the paint marker for the light-duty rings, added on 2026-10-02 to carry out decisions 2 and 3, cost USD 3.80 [K2c]. Main cost drivers and savings worth trying:

- **Frame, USD 57.00.** About USD 33.60 of timber and USD 23.40 of bolts, cross dowels and screws [K2]. Worth trying: one bolt instead of two at each low rail end (about USD 3.20); bolts and cross dowels bought as a bulk furniture-fitting pack; or a glued and screwed frame (about USD 15 less, but it no longer comes apart).
- **Worktop, USD 45.00.** A half sheet of birch plywood plus router wear. Worth trying: a full sheet shared with the shelf, or a cheaper sheet faced only on the top.
- **Threaded inserts, USD 28.20.** Worth trying: a bulk price for tee nuts and inserts. (The earlier idea of leaving the 122 screw-in positions as plain holes is withdrawn: their light-duty rating, decided on 2026-10-02, depends on the inserts being there.)
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
| 2026-10-02 | Design for construction accepted as recorded: the bolt and cross dowel frame joints, notched rail, shorter shelf, worktop brackets, tile pocket and fixing, T-nuts, fixtures on threaded positions, arm clamps and wall anchor | Amish: "i approve your recommendations for all 555 open decisions." | GBN-DDR-003 |
| 2026-10-02 | Clamp rating: the 122 screw-in positions over the frame are rated light duty at 0.92 N·m (296 to 493 N at the part), marked on the worktop in a contrasting colour, and the rating is stated in the fixture library notes | Amish: "i approve your recommendations for all 555 open decisions." | GBN-DDR-002, O4; GBN-CAL-001 [G5e] |
| 2026-10-02 | Racking: the shelf is screwed down to the low rails now; the frame is push-tested at TRL 4, and end low rails are added only if it still sways | Amish: "i approve your recommendations for all 555 open decisions." | GBN-DDR-002, O3 |
| 2026-10-02 | First workshops for co-design: makerspaces or technical colleges that have a CNC router and teach fixturing; first candidate to approach, a member lab of the Fab Lab network | Amish: "i approve your recommendations for all 555 open decisions." | GBN-DDR-001, O1 |
| 2026-10-02 | Wall anchor angles: left out of the renders and kept in the model, drawing and BOM | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 2026-10-02 | Hole pattern: the split is kept, with the full pattern in the renders and a representative patch in the exported CAD | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 2026-10-02 | Appearance-only details (index ticks, name plate, bolt heads, knobs, sample block and bar): render detail only | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 4 |
