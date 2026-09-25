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
