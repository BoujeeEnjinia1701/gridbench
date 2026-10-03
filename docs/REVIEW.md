# Review note: GridBench

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (GBN-PRB-001 v0.2): problem, users, operating environment, constraints, cited prior work (optical breadboards, fixture tables, machinist fixture plates, MFT tables, Gridfinity and Multiboard), out of scope, a new co-design checklist and open questions.
- `docs/03-requirements.md` (GBN-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets, verification method and concept status, a design load case and assumptions.
- `docs/02-concept.md` (GBN-PRC-001 v0.2): how it works, 12 numbered components, first-order numbers with assumptions, six key design choices, cost and options, safety, open questions; hero, exploded and flow figures.
- `cad/src/concept_media.py`: massing model of the bench (timber frame, feet, shelf, plywood worktop with the full 25 mm hole pattern, inserts, aluminum tile with M6 holes and dowel bores, dowel pins, toe clamps, fence, stops, V-block, instrument post and dial indicator, and an example workpiece); 1.75 m scale figure.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with BOM callouts 1 to 11, `flow.png` (material flow for one part at a fixture), `model.glb` and `viewer.html`. No cutaway: the worktop is solid plywood with the tile flush in a pocket, so a section adds little.
- `bom/bom.csv`: 12 lines with indicative prices, numbered to match the exploded view (line 12, fasteners, has no callout); `bom/bom-notes.md` updated.
- `README.md`: hero image and links line, and the Concept rationale, Burning platform, Where it could be used (6 industries, 5 regions), What sparked the idea, Problem, Concept, Key components and Safety sections expanded with cited sources.
- `docs/pdf/`: branded PDFs of the three controlled documents.

Notes on the model: the roughly 1,300 holes are drawn as thin dark disks on the surface rather than cut, and are left out of the blueprint's hidden-line views, because cutting and projecting them ran out of memory. The hero, exploded view and 3D model show them.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Grid | 25 mm, M6, 1,152 positions (144 on tile, 252 inserts, 756 plain holes) | R1 met by design |
| Worktop | 1,200 x 600 mm at 900 mm, ±15 mm feet | R2 met |
| Bench mass | About 40 kg | |
| Deflection, 500 N mid-bay | About 0.3 to 0.4 mm | R6 met by estimate |
| Dowel relocation | About 0.03 mm (8 mm h6 in H7) | R4 unverified |
| Plywood moisture movement | Up to about 0.4 mm over 1,200 mm (unsourced estimate) | **R3 at risk** |
| Clamp force at 2 N·m | About 0.8 kN | R7 unverified (PETG creep) |
| Tipping force at top edge | About 105 N empty, about 160 N with 20 kg on the shelf | **R12 not met without ballast** |
| Parts cost | About $239 | **R10 not met, about 9 % over $220** |

Requirements not met or at risk:

- **R10 cost not met:** about $239 against $220.
- **R12 stability not met** for the empty bench (about 105 N against 150 N); met with about 20 kg of ballast or a wall anchor.
- **R3 at risk:** plywood moves with humidity; the moisture coefficient used is an estimate without a source and must be confirmed.
- **R4, R5 (worktop), R7 unverified:** they depend on machining access, plywood flatness and PETG creep.

### Proposed, awaiting Amish

Update: items 1 to 8 are Decided by Amish, 2026-09-25: go with recommendation (GBN-DDR-001 v0.2, GBN-DDR-002); item 9 has no recommendation and stays Proposed, awaiting Amish.

1. **Budget.** Options: (a) dial indicator user-supplied, about $224; (b) also buy the tile as offcut stock, about $214 (price unverified); (c) raise `budget_usd` to $250. Recommendation: (a) plus (b), (c) as fallback. `project.yaml` is unchanged.
2. **Grid standard:** 25 mm, M6 (optical breadboard compatible) versus 50 mm, M8 or 16 mm bores. Recommendation: 25 mm, M6, with a heavy variant considered later.
3. **Two zones** (plywood field plus aluminum tile) versus an all-plywood or all-aluminum top. Recommendation: two zones.
4. **Inserts on a 50 mm sub-grid** versus every hole. Recommendation: 50 mm.
5. **Frame:** bolted timber versus welded steel. Recommendation: timber for the prototype.
6. **Fixture bodies:** printed PETG with metal dowels and screws versus machined. Recommendation: printed, with a machined option.
7. **Stability fix:** ballast on the shelf, wall anchor or wider splayed feet. Recommendation: ballast shelf plus an optional anchor bracket.
8. **Fixture file convention** (a metadata block giving footprint and datum) and the **fixture library license** (CERN-OHL-S-2.0 or permissive). Recommendation: metadata block; keep CERN-OHL-S-2.0 unless adoption by commercial jig makers is a goal.
9. **First workshops and regions** for co-design.

### Safety concerns

- Chips and projectiles when drilling, tapping and routing the worktop and tile; eye protection and clamped work.
- Pinch points at clamps.
- Tipping of the empty bench under a firm push (estimate about 105 N).
- Printed clamps cracking under overload and releasing a part; torque limit of 2 N·m proposed.
- Combustible top and fixtures: not for welding, grinding sparks or hot work.

### Problems and notes

- WebSearch budget ran out before a source for plywood in-plane moisture movement was found; the figure in the precis is flagged as unsourced.
- Sibling projects: none of the shared components (FieldNode, CellGuard, MotionCore, ThermaCart, TwinKit) applies. ReadyKit is referenced as the documentation counterpart only; there is no technical dependency.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review the media and this note, then decide items 1 and 2. If approved, run `/advance-trl3` to check deflection, tipping, clamp and insert loads and moisture movement by calculation, and to produce the parametric model, a tile drawing sheet and a fully priced BOM.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item with a recommendation is adopted as recommended for TRL 3 under that instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (GBN-DDR-001 v0.1, status proposed): items A1 to A10 adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; items O1 and O2 left "Proposed, awaiting Amish".
- `docs/04-calcs/01-sizing.md` (GBN-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: grid geometry, mass, tipping and sliding, worktop and frame stiffness, moisture and thermal movement, dowel location, clamp stress and insert pull-out, fixture change time, buildability, timber and cost, with a status for every requirement. The script imports the model's parameters and reads the BOM and `project.yaml`; every number in the note is printed by it (also written to `docs/04-calcs/sizing-output.txt`).
- `cad/src/model.py`: parametric build123d model (frame, feet, shelf, worktop with tile pocket, inserts, tile with all 144 M6 holes, 9 dowel bores and 4 counterbored fixing holes, round and diamond pins, toe clamps, fence, stops, V-block, post, indicator, ballast slabs, anchor brackets). Exports `cad/step/` and `cad/stl/` for `gridbench-assembly`, `precision-tile` and `worktop`. To keep the repo small, the worktop carries a representative 8 x 8 patch of its 1,008 holes; the full pattern is defined by `grid_points()` and drawn as surface marks in the media. `cad/` is about 5 MB.
- `cad/src/sheets.py` and `cad/drawings/GBN-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:20, with a 1:5 tile detail, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". GBN-DWG-001 was free because the concept blueprint is GBN-DWG-010.
- `bom/bom.csv` (16 lines, all priced with a supplier type) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked. Project-side wrappers (the kit is unchanged) keep the hole marks out of the blueprint projection, as at TRL 2, and out of the web model, and export the glTF at a coarser tessellation after clearing the render meshes: `model.glb` fell from 10.8 MB to 1.3 MB. No cutaway is made (`cut=False`, as at TRL 2), so the kit's cutaway limitation does not arise.
- GBN-PRB-001, GBN-PRC-001 and GBN-REQ-001 revised to v0.3; `README.md` and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated; PDFs rebuilt in `docs/pdf/`.

Detail changes found necessary by the calculations, within the adopted choices: the toe clamp body is 30 mm deep instead of 16 mm and the rated torque 1.6 N·m instead of 2 N·m (the TRL 2 clamp would have carried about 33 MPa in PETG); each precision fixture uses one round and one diamond pin (two round pins can bind on pitch error); the fence is two 190 mm segments (the 400 mm fence did not fit a 200 mm bed); the ballast is two 12.9 kg concrete slabs; the shelf is 535 mm deep so it actually rests on the low rails (the TRL 2 model's shelf ended at their inner faces); and two 5.3 mm packers seat the tile flush on its cross rails.

### Requirement status (GBN-CAL-001, Table 2)

2 not met, 2 at risk, 1 not verifiable at TRL 3, 4 met on paper, 3 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R10 Parts cost | **Not met** at $220 | Core parts $239.20 (+8.7 %); met under the $250 fallback (-4.3 %); $259.20 with indicator and anchor |
| R7 Clamp hold-down | **Not met** on the plywood field | Insert pull-out 1.02 to 1.63 kN against up to 1.78 kN of screw tension (factor 0.57 to 0.92); on the tile, 515 to 858 N at the part, 9.9 MPa in the clamp |
| R3 Coarse field accuracy | At risk | CNC ±0.22 mm (target 0.3); template ±0.34 mm statistical, ±0.62 mm worst case (target 0.5); moisture coefficient unsourced |
| R4 Tile location | At risk | Relocation 0.036 mm worst case, 0.015 mm statistical (target 0.03); hole position not verifiable |
| R5 Flatness | Not verifiable at TRL 3 | Depends on the plate and sheet as supplied |
| R6, R8, R9, R12 | Met on paper | 0.49 mm under 500 N (target 0.5); 56 s fixture change (target 60); largest print 190 mm; 176 N with ballast (107 N empty) |
| R1, R2, R11 | Met by design | 1,152 grid positions, tile on grid; 1,200 x 600 mm at 900 ±15 mm; open source |

Key numbers: bench 40.2 kg (65.9 kg ballasted); tile 3.0 kg, 0.061 mm under 500 N; plywood field ±0.115 mm over 1,000 mm at 40 to 60 % RH; tile machining about 4.2 h by drill press.

### Decisions recorded (GBN-DDR-001)

Decided by Amish, 2026-09-25: go with recommendation (first adopted for TRL 3, open for his review): A1 cost options (a) and (b), indicator user-supplied and tile as offcut, with R10 redefined to exclude the indicator; A2 25 mm, M6 grid; A3 two zones; A4 inserts on the 50 mm sub-grid; A5 bolted timber frame; A6 printed PETG fixtures with a machined option; A7 ballast shelf plus optional wall anchor; A8 fixture metadata block; A9 fixture library stays CERN-OHL-S-2.0; A10 tile at the right of the worktop. `budget_usd` is unchanged at $220. No pitch or problem rewording was recommended, so none was applied.

### Still awaiting Amish

Update: items 2 and 3 (option a) and the apron and rubber-pad suggestions in item 4 are Decided by Amish, 2026-09-25: go with recommendation (GBN-DDR-002). Item 1 and the racking suggestion in item 4 stay Proposed, awaiting Amish.

1. **O1, first workshops and regions for co-design.** No recommendation was made; none is chosen.
2. **O2, `budget_usd` of $250** (TRL 2 cost option c). Recommended at TRL 2 as the fallback; GBN-CAL-001 shows it is now needed for R10. Not applied.
3. **New, R7 on the plywood field.** Options: (a) flanged tee nuts pressed in from the underside, so clamp load bears on the plywood instead of shearing it (not yet priced; positions over rails would keep a screw-in insert); (b) a lower rated torque on the plywood field (1.2 N·m), accepting about 390 N at the part at the high nut factor; (c) keep screw-in inserts and relax R7 to 500 N on the tile only. Recommendation: (a). Not applied.
4. **Suggestions only, not in the repo:** 45 x 120 mm aprons would take R6 from 0.49 mm to 0.37 mm for a few dollars more timber (not priced); rubber pads on the feet would raise the sliding force of the empty bench from about 79 N; end low rails or a screwed-down shelf would add racking stiffness, which no requirement covers yet.

### Safety concerns

- Tipping: the empty bench tips at about 107 N at the front edge, below the 150 N design push. The slabs or the wall anchor must be in place before use; each slab is about 13 kg to lift.
- Clamp and insert failure: an overtightened clamp can pull an insert out of the plywood or crack a printed clamp and release a part. The 1.6 N·m limit needs to be marked on the clamps.
- Chips, projectiles and pinch points when drilling, tapping and routing, and at clamps; eye protection and clamped work.
- Combustible top and fixtures: not for welding, grinding sparks or hot work.

### Gaps and notes

- Citations: WebFetch on 2026-09-25 verified the equilibrium moisture contents (USDA *Wood Handbook*, FPL-GTR-190, Table 4-2: 4.5, 7.7, 11.0 and 16.0 % at 20, 40, 60 and 80 % RH, 21 °C) and they are now cited. No source for plywood in-plane moisture movement was found in *Wood Handbook* chapters 11, 12 and 13 or in Wikipedia; the 0.007 % per % figure stays flagged as unsourced. WebSearch was unavailable. The tile offcut price and the cast plate flatness (R5) are also unverified.
- Assumptions that only tests can settle: insert pull-out strength, PETG creep at 10 MPa, plywood modulus, and the moisture coefficient.
- Drawing: the 1:20 views are small on an ANSI B sheet; the tile detail at 1:5 carries the grid dimensions.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. No test, build or firmware material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on O2 (the $250 budget) and on the R7 insert options above; O1 stays open. For the record only, TRL 4 would need: a built bench and tile; a lab test report (TST, `environment: lab`) of tipping force with and without ballast, deflection under 500 N, insert and clamp pull tests with 8 h creep, tile hole position and flatness, dowel relocation over 10 cycles, and hole position over 1,000 mm at two humidities; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, and is recorded in `docs/decisions/0002-recommendations-accepted.md` (GBN-DDR-002 v0.1). Items without a recommendation stay open.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| A1 to A10 (DDR-001) | Cost options, grid, zones, insert spacing, frame, fixture bodies, stability, file convention, license, tile position | Adopted for TRL 3, open for review | Decided; status wording in DDR-001 v0.2, PRB-001 and PRC-001 updated |
| O2 budget | Raise `budget_usd` | $220 | $250; R10 target $250 |
| R7 option (a) | Flanged M6 tee nuts pressed in from the underside; screw-in inserts where a frame member lies below | 252 screw-in inserts, pull-out factor 0.57 to 0.92 | 130 tee nuts (factor 1.51 to 2.42) and 122 screw-in inserts; BOM line 5 $25.20 to $27.80 |
| Deeper aprons (TRL 3 suggestion) | 45 x 120 mm aprons | 45 x 95 mm, 0.49 mm under 500 N | 0.37 mm; frame $41.40 to $43.50; bench 40.2 kg to 41.9 kg |
| Rubber pads (TRL 3 suggestion) | Rubber pads on the levelling feet | Empty bench slides at about 79 N (hard feet) | About 206 N empty, 332 N ballasted; feet $2.00 to $2.50 each |

Knock-on figures: tipping 107 N to 112 N empty and 176 N to 181 N with ballast; core parts $239.20 to $245.90 ($4.10 under $250).

Files changed: `project.yaml` (budget, evidence), `README.md`, `docs/01-problem.md` (GBN-PRB-001 v0.4), `docs/02-concept.md` (GBN-PRC-001 v0.4), `docs/03-requirements.md` (GBN-REQ-001 v0.4), `docs/04-calcs/01-sizing.md` (GBN-CAL-001 v0.2) and `sizing.py`, `docs/decisions/0001-trl2-review-decisions.md` (GBN-DDR-001 v0.2), `bom/bom.csv` and `bom-notes.md`, `cad/src/model.py` (STEP and STL re-exported), `cad/src/sheets.py` (GBN-DWG-001 Rev P1 to P2), `cad/src/concept_media.py` (all of `media/` re-rendered and checked), and all PDFs in `docs/pdf/`. The README "What sparked the idea" section was rewritten around Honoré Blanc's hand-filed interchangeable musket locks as reported by Jefferson in 1785, and the footer line about gap-filling areas was removed.

### Requirement status (GBN-CAL-001 v0.2)

1 not met in part, 2 at risk, 1 not verifiable at TRL 3, 5 met on paper, 3 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R7 Clamp hold-down | **Not met** at the 122 screw-in positions over the frame | Pull-out factor 0.57 to 0.92 there; tee nuts 1.51 to 2.42 at 130 positions; tile met on paper |
| R3 Coarse field accuracy | At risk | Template ±0.34 mm statistical, ±0.62 mm worst case; moisture coefficient unsourced |
| R4 Tile location | At risk | 0.036 mm worst case against 0.03 mm |
| R5 Flatness | Not verifiable at TRL 3 | Depends on stock as supplied |
| R6, R8, R9, R10, R12 | Met on paper | 0.37 mm; 56 s; 190 mm print; $245.90 against $250; 181 N ballasted |
| R1, R2, R11 | Met by design | |

### Still awaiting Amish

1. **O1, first workshops and regions for co-design.** No recommendation; none chosen.
2. **O3, racking stiffness:** end low rails or a screwed-down shelf. The TRL 3 note named both without recommending one.
3. **O4 (new), the 122 screw-in positions over the frame:** (a) rate them light duty at 0.92 N·m, giving 296 to 493 N at the part (GBN-CAL-001, G5e); (b) move the insert sub-grid off the frame lines; (c) relax R7 there. Recommendation: (a).

### Cross-repo actions

None. No decision in this repo needs a change in another repo.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl` and `trl_target` stay at 3. Pull tests of the tee nuts and inserts, push tests for tipping and sliding with the rubber pads, and all purchasing are recorded as decided-in-principle work for TRL 4 and not started.

### Notes

- The decision wording relies on Amish's chat message as relayed to this session on 2026-09-25.
- New assumptions flagged in GBN-CAL-001 v0.2: plywood bearing strength under a tee-nut flange (10 MPa), tee-nut pull-through on the same shear strength as inserts, and indicative prices for tee nuts ($0.12), 45 x 120 mm timber ($2.80/m) and rubber-padded feet ($2.50).

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to fix the weaker sources. Changes, all in `README.md`:

| Claim | Old source | New source |
| --- | --- | --- |
| US manufacturers with fewer than 500 employees (Burning platform and United States row) | ITIF, citing NAM | National Association of Manufacturers, [Facts About Manufacturing](https://nam.org/mfgdata/facts-about-manufacturing-expanded/). Figures updated to the NAM page: about 239,000 firms in 2022, more than 98 % with fewer than 500 employees. |
| Kenya row | Kenyan Wallstreet, reporting KNBS (85 % of new jobs informal) | Kenya National Bureau of Statistics, [Economic Survey 2024, popular version](https://www.knbs.or.ke/wp-content/uploads/2024/05/2024-Economic-Survey-Popular-Version.pdf). The 85 % figure could not be verified in a KNBS document that could be fetched, so the row now states only the growth rates in that document (informal employment 4.5 %, formal wage employment 4.1 %, 2023). |
| What sparked the idea: how Blanc made the parts | Wikipedia, "Honoré Blanc" | Jefferson to Jay, 30 August 1785 (Founders Online), already the section's primary source. The hand-filing, jig and gauge detail was removed because it rested only on Wikipedia; the section now quotes Jefferson's own words ("by tools of his own contrivance"). The inspiration event is unchanged. |

No country rows were replaced. `docs/01-problem.md` did not cite these sources, so no controlled document changed. The RP Photonics link (grid convention) and the Siegmund dealer listing (a price, for which the listing is the primary source) were not flagged and were kept.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo on 2026-09-26 for the first batch of product renders. This session added `cad/src/product_model.py` (appearance model, 42 parts), set the README hero image to `media/render-hero.png` with a link to `media/render-exploded.png`, and wrote this note. The render files are produced later by the portfolio render pipeline. No other file changed: `model.py`, the BOM, the drawings and the controlled documents are untouched.

### What product_model.py adds

- `product_parts()`, `TITLE` and `RENDER_VIEWS` (hero from the front right at about 30 deg, exploded from the front right at about 28 deg, and a detail view of the worktop and fixture set without the frame at about 42 deg).
- Worktop: all 1,008 grid holes cut (cut per 150 mm cell so the mesh stays light), eased 1 mm edges, lamination lines on the plywood edges, laser-etched index ticks every 100 mm along the front and left margins, brass screw-in inserts flush in the top and zinc tee nuts underneath.
- Precision tile: chamfered top edge, every M6 hole, the 9 dowel bores, and cap screws seated in the 4 counterbores.
- Frame: members with eased arrises, domed M8 carriage bolt heads at every leg joint, a teal name plate on the front apron; levelling feet with rubber pads, filleted steel pads and lock nuts; shelf and ballast slabs with softened edges.
- Fixture set: toe clamps with a toe relief, grip ribs, M6 screws, washers and lobed knobs; round and diamond pins; a machined sample block; fence segments with cap screws and a sight line; stop pins with collars; a V-block holding a sample round bar; a slotted instrument post with end cap, arm clamps, and a dial indicator with bezel, graduated face, needle, crystal and contact point on the sample block.
- Context: a compact section of workshop floor.

### Differences from model.py

1. **Toe-clamp screw positions.** Proposed, awaiting Amish. model.py places the two clamp screws at (320, 40) and (430, -40) mm, which fall between tile holes (holes sit at 12.5 + 25k mm). The appearance model puts each screw on the nearest tile hole, (312.5, 37.5) and (437.5, -37.5), and slides the clamp bodies in their slots to stay near the model.py positions. Recommendation: update model.py to the same hole-centered positions at the next model revision.
2. **Wall anchor brackets (BOM 15, optional) left out.** Proposed, awaiting Amish. With no wall in the scene the brackets read as loose tabs behind the bench. Recommendation: keep them out of product renders and keep them in model.py, the drawing and the BOM as they are.
3. **Full hole pattern in the worktop.** Proposed, awaiting Amish. model.py cuts a representative 8 x 8 patch to keep STEP and STL files small; the appearance model cuts all 1,008 holes so the grid reads in renders. Grid positions come from model.py (`classify()`, `insert_kinds()`), so nothing moves. Recommendation: keep this split (patch in the exported CAD, full pattern in renders).
4. **Appearance-only additions** (lamination lines, index ticks, name plate, bolt heads, knobs, the sample block and bar) change no dimension or interface. The index ticks and name plate are not in the BOM. Recommendation: treat them as render detail only unless Amish wants them adopted.

### Status

This is an appearance model only: no tolerances, fabrication detail or build instructions. `trl` and `trl_target` stay at 3, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: design for construction and prototype build plan (kit 1.7.0)

Amish approved the build plan format on 2026-09-30 ("this is the correct build plan ... this is a good quality document format. Extend this across all the other repos"), asked for outstanding decisions to go in a separate design decisions register, and asked for any design that cannot be built as drawn to be made physically feasible. On 2026-10-01 he set `budget_usd` as a value-engineering target, not a limit. This session installed kit 1.7.0, ran `/build-plan` and stopped at TRL 3.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- `cad/src/model.py`: every component is now its own solid (`build_components()`), with a constructability check (`python cad/src/model.py --check`, 92 checks, all pass). STEP and STL re-exported to `cad/step/` and `cad/stl/`.
- `docs/decisions/0003-design-for-construction.md` (GBN-DDR-003 v0.1, Draft): every change below, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `cad/src/build_plan_media.py`: overview, worktop hole layout, 16 making sketches (`cad/drawings/GBN-DWG-101` to `116`), 11 joint close-ups and 15 assembly step pictures in `docs/05-build-plan/`.
- `docs/05-build-plan.md` (GBN-BLD-001 v0.1) and `docs/06-design-decisions.md` (GBN-DEC-001 v0.1, with a Value engineering section).
- GBN-DWG-001 to Rev P4; concept media re-rendered from the updated model.
- GBN-CAL-001 v0.3 and `sizing.py`, GBN-PRC-001 v0.5, GBN-REQ-001 v0.5, `bom/bom.csv` (17 lines) and `bom/bom-notes.md`, `project.yaml` (`design_state: constructable`, new evidence), `README.md` (links line and "Building the prototype"); PDFs rebuilt.

### Design changes made for construction (GBN-DDR-003)

1. Long aprons shortened to 1,020 mm and butted between the legs (they ran through them); every apron and low rail end held by two M8 x 120 bolts into M8 cross dowels, the end-apron bolts staggered against the long-apron bolts inside the leg.
2. Cross rail under the tile's right edge notched 15 x 25 mm at both ends (it ran 15 mm into the right-hand legs); every cross rail held by two 6 x 100 mm screws through the apron at each end.
3. Shelf 1,010 mm long instead of 1,020 mm, so it fits between the legs.
4. Tile pocket 301 x 301 mm with 8 mm corner relief holes (it was the tile's exact size with square corners).
5. Tile held by four M6 x 20 cap screws into screw-in inserts in the two tile rails (the counterbored holes had nothing to screw into).
6. Worktop held by nine steel angle brackets on the apron inside faces (it had no fixing), each clear of every tee nut and cross rail.
7. Leg ends bored 12 mm with an M10 T-nut for each levelling foot (the stems ended in solid wood).
8. Fence, V-block, post foot and toe clamp screws moved onto threaded positions; stop pins given a spigot; one screw length rule (15 to 18 mm below the plywood surface, 12 mm at most on the tile).
9. Instrument arm passes beside the post through a printed arm clamp, and the drop rod beside the arm's end through a printed end clamp (the arm passed through the post); post foot 74 x 74 mm on two M6 screws, post held by two M5 screws; post moved to the plywood directly behind the tile.
10. V-block's V narrowed to 50 mm with 5 mm flats, so the block is 60 mm tall as specified (the V cut its top edges off).
11. Optional wall anchor angles fixed under the rear apron and down the wall (the flat leg pointed at no wall).

### Key results

- Mass 43.8 kg empty (was 41.9 kg), 69.5 kg with ballast; tipping 117 N empty, 186 N with ballast (target 150 N); stiffness unchanged at 0.37 mm.
- Value-engineering target: USD 250. Estimated cost of the constructable design: USD 268.40 (USD 18.40 over the target). The cost drivers and savings worth trying are in GBN-DEC-001.
- Requirements: R7 not met at the 122 screw-in positions (unchanged); R10 over the value-engineering target by USD 18.40; R3 and R4 at risk; R5 not verifiable at TRL 3; R6, R8, R9 and R12 met on paper; R1, R2 and R11 met by design.

### Decisions proposed and awaiting Amish

All are in the design decisions register (`docs/06-design-decisions.md`): review of GBN-DDR-003; O4, the light-duty rating of the 122 screw-in positions (recommended); O3, racking stiffness; O1, first workshops; and three appearance items from 2026-09-26 (wall anchor out of renders, full holes only in renders, render-only details). No budget decision is proposed: the budget is a value-engineering target.

### Stale outputs

The photoreal renders `media/render-hero.png`, `media/render-exploded.png` and `media/render-detail.png` (made on Amish's Mac, not in this cloud copy), `media/card.png` and `media/social-preview.png`, and the appearance model `cad/src/product_model.py` still show the concept: fixture positions, post and arm without clamps, and no brackets, T-nuts or frame bolts. The appearance model reads the apron length from `model.py`, so it already butts the aprons between the legs. They are not regenerated here and need updating on the Mac.

### Safety concerns

Unchanged in kind: tipping of the empty bench (117 N), chips and projectiles when drilling, tapping and routing, pinch points at clamps, printed clamps cracking above 1.6 N·m, screw-in positions over the frame pulling out before full clamp force, and no hot work. The build plan adds six safety stops (S1 to S6), including a two-person lift for the worktop.

### Recommended next step

Amish to review GBN-DDR-003 and the register. TRL 4 remains on hold; a TRL 4 build would follow GBN-BLD-001 and record the first checks of its section 5.

### Picture check

Every picture made in this session was looked at: the overview, the worktop hole layout, the 16 making sketches, the 11 joint close-ups, the 15 step pictures, the general arrangement and the concept media (hero, exploded view, flow, blueprint). Pictures that were unclear were redrawn: joints 1, 2 and 3 as sections cut level with a bolt or screw and seen from above, joints 5, 6, 7 and 9 with the cut facing the camera, the long members' sketches drawn standing on end so their views fit the sheet, the packer and fixture sketches with insets that zoom in on where the part sits, the step pictures with bolts pulled out on the correct side, and the overview with the shelf, slabs and wall anchor moved clear of the frame. `python .kit/drawing.py --check-text cad/drawings/*.svg media/concept-blueprint.svg` finds no overlapping text. One known weakness: in joint 3 the leader for the front right leg ends at the leg's corner beside the apron, because the kit picks the leader point.

## Session 2026-10-02: open decisions decided by Amish

Authority: Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." The recommendations approved are those written for the open decisions in the design decisions register. No model, BOM quantity or price, or picture was changed; where a decision needs one, it is listed below as a follow-up. `trl` and `trl_target` stay at 3. No commit or push.

### Decisions recorded

7, all moved to "Decisions made" in `docs/06-design-decisions.md`, dated 2026-10-02:

1. Design for construction (GBN-DDR-003) accepted as recorded.
2. Clamp rating: the 122 screw-in positions over the frame rated light duty at 0.92 N·m (296 to 493 N at the part), marked on the worktop in a contrasting colour and stated in the fixture library notes.
3. Racking: shelf screwed down to the low rails now; push test at TRL 4; end low rails only if the frame still sways.
4. First workshops for co-design: makerspaces or technical colleges with a CNC router that teach fixturing; first candidate a member lab of the Fab Lab network.
5. Wall anchor angles: left out of the renders, kept in the model, drawing and BOM.
6. Hole pattern: full pattern in the renders, representative patch in the exported CAD.
7. Appearance-only render details: render detail only.

### Documents changed

- `docs/06-design-decisions.md` (GBN-DEC-001 v0.2): also withdraws the plain-hole saving under Value engineering
- `docs/decisions/0003-design-for-construction.md` (GBN-DDR-003 v0.2): accepted; status stays Draft
- `docs/decisions/0002-recommendations-accepted.md` (GBN-DDR-002 v0.2): O1, O3 and O4 decided
- `docs/decisions/0001-trl2-review-decisions.md` (GBN-DDR-001 v0.3): O1 decided
- `docs/02-concept.md` (GBN-PRC-001 v0.6): open items closed with the decisions
- `docs/03-requirements.md` (GBN-REQ-001 v0.6): R7 note on the light-duty rating
- `docs/05-build-plan.md` (GBN-BLD-001 v0.2): safety stop S5 states the light-duty rating and marking

### Follow-up actions to carry approved decisions into the design

1. Decision 2 (drawings): Show the contrasting-colour marking of the 122 light-duty positions on the worktop making sketch and GA drawing GBN-DWG-001.
2. Decision 2 (pictures): Show the marking in the build plan worktop pictures.
3. Decision 2 (bom): Add the marking paint or marker to the fastener kit line of the BOM.
4. Decision 2 (docs): State the light-duty rating (0.92 N·m, 296 to 493 N at the part) in the fixture library notes.
5. Decision 3 (model): Add the screws that fix the shelf down to the low rails in `cad/src/model.py`, with the constructability checks re-run.
6. Decision 3 (pictures): Show the shelf screws in build plan steps 4 and 7 and the shelf making sketch.
7. Decision 3 (bom): Add the shelf screws to the fastener kit line of the BOM.

### Points found in the review

- A saving in Value engineering (leave the 122 screw-in positions as plain holes 'if decision 2 rates them light duty anyway') contradicts item 2: the light-duty rating depends on the screw-in inserts being there.

## Session 2026-10-02: approved follow-ups carried out

Authority: Amish, 2026-10-02: "497 follow-up actions that need CAD, drawing, picture, BOM or calculation work ... APPROVED CHANGES, COMPLETE THESE", and for the renders, "Photoreal renders are out of date in most repos ... COMPLETE THESE". `trl` and `trl_target` stay at 3; `budget_usd` is unchanged. No commit or push.

### Follow-ups

1. Decision 2 (drawings): done. GBN-DWG-001 Rev P5 rings the 122 light-duty positions in red on the top view, with a leader and a note; the worktop making sketch GBN-DWG-108 Rev P2 rings them on its top view and says how to paint them.
2. Decision 2 (pictures): done. The hole layout (`docs/05-build-plan/worktop-holes.png`) rings every screw-in position and adds a legend line; steps 8 and 9 show the red rings, and later steps carry them.
3. Decision 2 (bom): done. Line 12 adds one paint marker in a contrasting colour ($3.00, indicative retail); line 4 states the rings.
4. Decision 2 (docs): done. There was no separate fixture library notes file, so a "Fixture library notes" section is added to the precis (`docs/02-concept.md` v0.7), stating the light-duty rating (0.92 N·m, 296 to 493 N at the part) and the marking. The build plan worktop steps state it too.
5. Decision 3 (model): done. `cad/src/model.py` adds eight 4 x 30 mm countersunk wood screws (four into each low rail at 105, 375, 635 and 905 mm from the shelf's left end), with clearance and countersink holes in the shelf and pilot holes in the rails. Four new checks (screws in their shelf holes, reaching into the rails, clear of the ballast, clear of the frame bolts and legs); 96 of 96 checks pass. STEP and STL regenerated.
6. Decision 3 (pictures): done for step 7 (shelf and its screws), the shelf making sketch GBN-DWG-107 Rev P2 (eight holes and the screws in the inset), the low rail sketch GBN-DWG-104 Rev P2 and the overview. Step 4 comes before the shelf, so its picture shows no screws; its text now says the shelf is screwed into the rail tops in step 7.
7. Decision 3 (bom): done. Line 12 adds the eight shelf screws (8 at an indicative $0.10); line 3 states them.

Cross-repo actions: none.

### Results

- Requirement status changes: none. R7 stays not met at the 122 screw-in positions (rated light duty, as decided); R10 stays over the value-engineering target, now by $22.20.
- Value-engineering target: USD 250. Estimated cost of the constructable design: USD 272.20 (USD 22.20 over the target) [K4]; line 12 rises from $14.00 to $17.80 [K2c]; everything $292.20.
- Mass: bench 43.8 kg empty (fasteners 2.7 kg, up about 0.03 kg); 69.6 kg with the ballast [B1], [B2]; anchor tie force 34 N [C6].
- Appearance model (`cad/src/product_model.py`) brought into line with the constructable design: hex bolt heads and washers on the legs at the model's 24 bolt positions (were carriage bolts on the aprons), tile pocket with 0.5 mm clearance and corner relief holes, the nine worktop brackets, the eight shelf screw heads, the red light-duty rings, and the fence, V-block, stops, toe clamps, post foot screws, arm clamp, end clamp, drop rod and indicator at the model's positions. Remaining appearance differences are those Amish decided on 2026-10-02 (wall anchor left out, full hole pattern, render-only details); hidden details (rail notch, cross dowels) are not drawn. Render scenes exported to `/home/claude/renders/gridbench`; photoreal renders, `card.png` and `social-preview.png` are to be made on Amish's Mac.

### Documents changed

- `cad/src/model.py`, `cad/src/sheets.py`, `cad/src/build_plan_media.py`, `cad/src/product_model.py`, `cad/src/concept_media.py`; `cad/step/`, `cad/stl/`
- `cad/drawings/GBN-DWG-001` Rev P5; `GBN-DWG-104`, `GBN-DWG-107`, `GBN-DWG-108` Rev P2
- `docs/05-build-plan/`: worktop-holes, overview, steps 7 to 15
- `bom/bom.csv` (lines 3, 4, 12), `bom/bom-notes.md`
- `docs/04-calcs/sizing.py`, `sizing-output.txt`, `01-sizing.md` (GBN-CAL-001 v0.4)
- `docs/05-build-plan.md` (GBN-BLD-001 v0.3), `docs/02-concept.md` (GBN-PRC-001 v0.7), `docs/03-requirements.md` (GBN-REQ-001 v0.7), `docs/06-design-decisions.md` (GBN-DEC-001 v0.3), `README.md`
- Concept media regenerated (`media/`)

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
