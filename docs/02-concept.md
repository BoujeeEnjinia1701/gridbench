---
doc_id: GBN-PRC-001
title: GridBench design precis
project: GridBench
doc_type: Design precis
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, components, first-order numbers, safety, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; design choices adopted as recommended (GBN-DDR-001); numbers from GBN-CAL-001; deeper clamp, diamond pin, split fence, ballast slabs; priced BOM
---

# GridBench design precis

## Summary

GridBench is a 1,200 x 600 mm workbench whose top is a 25 mm hole grid with M6 threads, the same pattern as metric optical breadboards. A cheap plywood field covers most of the top for general holding, and a 300 x 300 mm aluminum precision tile, set flush on the same grid, carries work that must repeat to a few hundredths of a millimeter. Printed clamps, stops, fences and V-blocks bolt to either zone, and a post with a user-supplied dial indicator checks parts in place. Two concrete slabs on the shelf keep the bench from tipping. The core parts cost $239.20, above the $220 budget; a $250 fallback budget awaits Amish (see Cost). The parametric model is `cad/src/model.py`, the general arrangement is drawing GBN-DWG-001 and the calculations are GBN-CAL-001.

![GridBench concept](../media/hero.png)

Figure 1. GridBench with a 1.75 m person for scale. Concept, not for fabrication.

## How it works

1. **One grid everywhere.** Hole centers sit at 12.5 + 25k mm from the front-left corner of the worktop, in both directions. The tile's edges fall midway between grid lines, so its holes continue the plywood grid, a fixture can straddle both zones and any fixture file places itself by grid coordinates (column, row).
2. **Locate on dowels, clamp on threads.** As on machinist fixture plates, location and clamping are separate. On the tile, nine reamed 8 mm H7 bores at 100 mm pitch sit in the centers of grid squares, between the M6 holes. A precision fixture or part nest carries one round and one diamond (relieved) 8 mm h6 pin that drop into two bores, then M6 screws clamp it down. Two round pins would bind on any pitch error (GBN-CAL-001, section F). On the plywood field, 6.6 mm plain holes take stop pins, and M6 threaded inserts on a 50 mm sub-grid take clamps.
3. **Work and check in the same setup.** The instrument post bolts to any grid hole and carries a dial indicator on an arm, so a part can be checked before it is unclamped (Figure 3).
4. **Fixtures travel as files.** Each fixture is a parametric build123d part with a short metadata block that states its grid footprint and datum. A workshop that builds a GridBench can print or machine a published jig and expect it to fit. Jigs documented with the lab's ReadyKit toolchain can carry their own drawings and revision history.

![Material flow at a fixture](../media/flow.png)

Figure 3. Material flow for one part at a fixture. Times and the rework rate are estimates or targets; the fixture change time is from GBN-CAL-001.

![Exploded view](../media/exploded.png)

Figure 2. Exploded view. Callout numbers match the lines in `bom/bom.csv`.

## Main components

Table 1. Main components (numbers match the BOM and Figure 2).

| No. | Component | Design |
| --- | --- | --- |
| 1 | Bench frame | Bolted softwood: four 70 x 70 mm legs at 1,090 x 490 mm centers, 45 x 95 mm aprons, four 45 x 70 mm cross rails (clear bays 255 mm or less), two low rails for the shelf, two 5.3 mm hardwood packers under the tile |
| 2 | Levelling feet | Four M10 feet in T-nuts, ±15 mm adjustment |
| 3 | Lower shelf | 12 mm plywood, 1,020 x 535 mm, resting on the low rails; carries the ballast |
| 4 | Plywood grid worktop | 18 mm birch plywood, 1,200 x 600 mm, 1,008 holes on the 25 mm grid, 300 x 300 mm through pocket for the tile |
| 5 | M6 threaded inserts | 252 screw-in inserts, 10 mm OD by 13 mm, on the 50 mm sub-grid |
| 6 | Precision grid tile | Cast aluminum tooling plate (offcut), 300 x 300 x 12.7 mm, 144 M6 tapped holes, 9 reamed 8 mm H7 bores, 4 counterbored fixing holes to the two cross rails |
| 7 | Round dowel pins | 8 mm h6 hardened pins, 20 mm long; one per precision fixture |
| 8 | Printed toe clamps | PETG, 70 x 24 x 30 mm body with a 6.6 mm slot and a heel, printed on its side; rated screw torque 1.6 N·m |
| 9 | Printed fence, stops and V-block | Fence in two 190 mm segments, each on two grid holes; stop pins for 6.6 mm holes; 90° V-block |
| 10 | Instrument post and arm | 20 x 40 mm aluminum extrusion on a printed grid foot, 18 mm arm |
| 11 | Dial indicator | 0.01 mm resolution, 10 mm travel, 8 mm stem; user-supplied |
| 12 | M6 fastener kit | Cap screws, washers and printed knobs (no callout) |
| 13 | Diamond locating pins | 8 mm h6 relieved pins; one per precision fixture, paired with a round pin |
| 14 | Ballast slabs | Two 400 x 400 x 35 mm concrete paving slabs, 12.9 kg each, on the shelf |
| 15 | Wall anchor brackets | Optional pair of steel angles from the rear apron to a wall |
| 16 | Tile machining tools | M6 taps, drills, 8 mm H7 reamer and a tapping guide (no callout) |

## Key numbers

All values are from GBN-CAL-001, where every assumption is stated. They are paper estimates, not test results.

Table 2. Key numbers.

| Quantity | Value | Note |
| --- | --- | --- |
| Grid positions | 1,152 (48 x 24): 144 on the tile, 252 inserts and 756 plain holes | 25 mm pitch, 12.5 mm edge offset |
| Bench mass | 40.2 kg empty; 65.9 kg with two ballast slabs | Densities in GBN-CAL-001, Table 1 |
| Tipping force at the top edge | 107 N empty; 176 N with the ballast (target 150 N) | Feet 245 mm from the center line, push at 900 mm |
| Deflection, 500 N at bay center | 0.19 mm in the plywood; 0.49 mm including rails and aprons (target 0.5 mm) | Plate theory, E about 7 GPa, pinned joints |
| Plywood field moisture movement | ±0.115 mm over 1,000 mm at 40 to 60 % RH; ±0.40 mm over 20 to 80 % RH | Sourced moisture contents; plywood coefficient 0.007 % per % still unsourced |
| Tile thermal growth | 0.069 mm over 300 mm per 10 K | Aluminum, 23 x 10⁻⁶ /K |
| Dowel relocation | 0.036 mm worst case, 0.015 mm statistical (target 0.03 mm) | Round plus diamond pin, 200 mm apart |
| Clamp force at the part | 515 to 858 N at 1.6 N·m; body stress 9.9 MPa or less | M6, nut factor 0.15 to 0.25 |
| Insert pull-out | 1.02 to 1.63 kN against up to 1.78 kN of screw tension | Assumed shear strength; R7 not met on the plywood field |
| Fixture change | 56 s (target 60 s) | Two screws out, two in |
| Tile machining | About 4.2 h by drill press with a tapping guide | 144 holes, 9 reamed bores, 4 counterbores |

## Key design choices

Each choice below is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (GBN-DDR-001).

1. **Grid: 25 mm, M6.** Matches metric optical breadboards, so commercial posts, clamps and bases fit ([RP Photonics, "Optical breadboards"](https://www.rp-photonics.com/optical_breadboards.html)). A heavy 50 mm variant is left for later.
2. **Two zones instead of one precise top.** A full aluminum top of 1,200 x 600 mm would cost several times the budget. Plywood gives area; the tile gives precision where it is needed.
3. **Inserts on a 50 mm sub-grid,** with the 25 mm holes kept for pins. Inserts at every plywood hole would add about $75 and a day of fitting.
4. **Bolted timber frame** for the prototype, with welded steel as a documented variant.
5. **PETG printed fixtures with steel where it matters.** Dowels, screws and the tile are metal; bodies are printed, with a machined option for heavily used jigs.
6. **Tile at the right of the worktop,** leaving the left 800 mm free for large parts.
7. **Ballast on the shelf plus an optional wall anchor,** for stability.
8. **Fixture files carry a metadata block** stating grid footprint and datum; the fixture library stays under CERN-OHL-S-2.0.

Four details changed at TRL 3 because of GBN-CAL-001, within these choices: the toe clamp body is 30 mm deep instead of 16 mm and its rated torque is 1.6 N·m instead of 2 N·m (the TRL 2 clamp would have carried about 33 MPa and crept); each precision fixture uses one round and one diamond pin; the fence is two 190 mm segments so that it fits a 200 mm print bed; and the ballast is two concrete slabs, 25.8 kg in all.

## Cost

The priced BOM (`bom/bom.csv`, 16 lines) gives core parts of $239.20, 8.7 % over the $220 budget, with the dial indicator ($15.00) user-supplied and the wall anchor brackets ($5.00) optional; everything together is $259.20. The largest items are the plywood worktop ($45.00), the frame ($41.40), the tile offcut ($28.00) and the inserts ($25.20). The cost options adopted in GBN-DDR-001 (indicator user-supplied, tile as offcut) are not enough on their own. Raising `budget_usd` to $250 would cover the core parts with $10.80 to spare; this is **Proposed, awaiting Amish**, and `project.yaml` is unchanged.

## Safety

> **Safety:** Drilling, tapping and routing the worktop and tile create chips and projectiles: wear eye protection and clamp work before cutting. Clamps and toe clamps create pinch points; keep fingers clear when tightening. The empty bench tips at about 107 N at the top edge (GBN-CAL-001), below the 150 N design push, so place both ballast slabs on the shelf or anchor the bench to a wall before use, and lift each 13 kg slab with a straight back. Chamfer or round all plywood, tile and printed edges. Printed clamps can crack and release a part under load; do not exceed the rated screw torque of 1.6 N·m, and do not use printed clamps for machining with a milling machine. Screw-in inserts in the plywood field may pull out before a clamp reaches its rated force. The bench is not for welding, grinding sparks or hot work: plywood and PETG are combustible.

## Open questions

- [ ] R7 on the plywood field: tee nuts from below, a lower rated torque on the plywood, or a relaxed target. Proposed, awaiting Amish (`docs/REVIEW.md`).
- [ ] `budget_usd` of $250 (GBN-DDR-001 O2). Proposed, awaiting Amish.
- [ ] First workshops and regions for co-design (GBN-DDR-001 O1). Proposed, awaiting Amish.
- [ ] Can the tile be drilled to ±0.05 mm without CNC, using a printed or steel drill jig on a drill press? Not verifiable on paper.
- [ ] A sourced figure for plywood in-plane moisture movement; the moisture contents are now sourced, the coefficient is not.
- [ ] Flatness of cast tooling plate bought as offcut, and of the plywood sheet once screwed down (R5).
