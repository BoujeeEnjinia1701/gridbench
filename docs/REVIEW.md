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

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: A1 cost options (a) and (b), indicator user-supplied and tile as offcut, with R10 redefined to exclude the indicator; A2 25 mm, M6 grid; A3 two zones; A4 inserts on the 50 mm sub-grid; A5 bolted timber frame; A6 printed PETG fixtures with a machined option; A7 ballast shelf plus optional wall anchor; A8 fixture metadata block; A9 fixture library stays CERN-OHL-S-2.0; A10 tile at the right of the worktop. `budget_usd` is unchanged at $220. No pitch or problem rewording was recommended, so none was applied.

### Still awaiting Amish

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
