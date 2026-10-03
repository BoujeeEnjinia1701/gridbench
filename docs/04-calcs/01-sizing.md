---
doc_id: GBN-CAL-001
title: GridBench sizing calculations
project: GridBench
doc_type: Calculation
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (grid, mass, tipping, stiffness, moisture and temperature, dowel location, clamps and inserts, fixture change, buildability, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); $250 budget, 45 x 120 mm aprons, flanged tee nuts, rubber-padded feet; results re-run
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design made constructable (GBN-DDR-003); mass, stability and cost re-run; cost reported against the value-engineering target
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Shelf screws (decision 3) and light-duty marking (decision 2) added: mass and cost re-run; light-duty rating recorded as decided'
---

# GridBench sizing calculations

On paper, GridBench meets seven of its twelve requirements (four by calculation, three by design), has two at risk, has one that cannot be verified at TRL 3, misses one in part, and is over its cost target. Version 0.4 adds the eight screws that fix the shelf down to the low rails and the paint marker for the light-duty rings, carrying out decisions Amish made on 2026-10-02: core parts now cost USD 272.20, USD 22.20 over the USD 250 value-engineering target [K4], and the ballasted bench is 69.6 kg [B2]; no requirement status changes. Version 0.3 follows the design-for-construction changes of GBN-DDR-003: the aprons and low rails butt between the legs on M8 bolts and cross dowels, the worktop is held by nine brackets, the tile by four screws into rail inserts, and the fixtures sit on threaded positions. The bench is 1.9 kg heavier (43.8 kg), tips at 117 N empty and 186 N ballasted, and its core parts cost USD 268.40: value-engineering target USD 250, USD 18.40 over the target [K4]. Stiffness and every other result are unchanged. Version 0.2 applied the recommendations Amish accepted on 2026-09-25 (GBN-DDR-002): `budget_usd` is now $250, the long and end aprons are 45 x 120 mm instead of 45 x 95 mm, flanged M6 tee nuts pressed in from the underside replace the screw-in inserts wherever the underside is clear, and the levelling feet carry rubber pads. R10 (cost) was then met at $245.90. R6 (stiffness) now has margin: 0.37 mm against 0.5 mm, down from 0.49 mm. R7 (clamp hold-down) is met on paper at the 130 tee-nut positions (pull-through factor 1.51 to 2.42) and on the tile, but not at the 122 insert positions that sit over a frame member, where a screw-in insert must stay and its pull-out factor is still 0.57 to 0.92. R3 (coarse field accuracy, template-drilled build) and R4 (relocation within 0.03 mm) are at risk. R5 (flatness) cannot be verified at TRL 3. The first issue of this note changed four details of the TRL 2 concept, which stand: the printed toe clamp is deeper (30 mm instead of 16 mm) with a rated torque of 1.6 N·m instead of 2 N·m, every precision fixture carries one round and one diamond locating pin, the fence is printed in two 190 mm segments that fit a 200 mm bed, and two concrete slabs on the shelf form the ballast. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace a push test for tipping, a pull test of clamps and inserts, or inspection of the tile. The empty bench tips at about 117 N at its front edge [C2]; it must be ballasted or anchored before use. See GBN-PRC-001, Safety.

## Scope and method

The note checks every requirement in GBN-REQ-001 v0.5 against the design in GBN-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, its derived dimensions and its grid functions, so the hole counts, bays, rail spans and foot positions used here are the ones in the STEP files and in drawing GBN-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes its output to `docs/04-calcs/sizing-output.txt`.

The design case is a bench in an indoor workshop at 10 to 35 °C and 20 to 80 % relative humidity, with the loads in GBN-REQ-001: 150 kg spread over the top, 500 N at the middle of a bay and a 150 N horizontal push at the top edge.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Densities | Softwood 500 kg/m³, plywood 680 kg/m³, aluminum 2,700 kg/m³, concrete 2,300 kg/m³ | Typical values |
| Plywood stiffness | E = 7 GPa, mean of the two in-plane directions, treated as an isotropic plate (ν = 0.3); holes reduce stiffness by the ligament efficiency 0.736 [A5] | Assumption; to confirm from the supplier's data for 18 mm birch |
| Frame timber | C16 softwood, mean E = 8 GPa, characteristic bending strength 16 MPa; joints pinned (no frame action) | EN 338 strength class values; conservative joint model |
| Plate theory | Simply supported rectangular plate, central point load or uniform load, coefficients from Timoshenko's tables by aspect ratio | Standard handbook method; edges screwed to rails are stiffer than simply supported |
| Moisture | Equilibrium moisture content at 21 °C: 4.5, 7.7, 11.0 and 16.0 % at 20, 40, 60 and 80 % RH | USDA Forest Products Laboratory, *Wood Handbook* (FPL-GTR-190, 2010), Table 4-2 |
| Moisture movement | Plywood in-plane strain 0.007 % per 1 % moisture content | **Unsourced estimate**; the *Wood Handbook* gives no plywood figure (checked 2026-09-25) |
| Hole position | Shared CNC router ±0.10 mm; printed drilling template ±0.10 mm per 200 mm placement | Assumptions |
| Fits | 8 mm H7 bore (0 to +0.015 mm), h6 pin (0 to -0.009 mm) | ISO 286 limits for 6 to 10 mm |
| Screws | M6, torque to tension T = K F d with nut factor K = 0.15 to 0.25 (nominal 0.2) | Common engineering range |
| PETG | Sustained bending stress limit 12 MPa (about a quarter of the short-term strength of printed PETG); CTE 60 × 10⁻⁶ /K | Assumptions; creep data for printed PETG to be confirmed |
| Inserts | Pull-out by shear of the plywood on the insert's outer cylinder (10 mm by 13 mm) at 2.5 to 4 MPa; for a tee nut, the same shear strength on a cylinder of the 19 mm flange diameter through the 18 mm sheet | Assumption; no test data found |
| Tee-nut flange bearing | Plywood bearing strength perpendicular to the face 10 MPa under the flange | Assumption; to be confirmed by a pull test at TRL 4 |
| Friction | Levelling feet on a workshop floor, μ = 0.2 (hard plastic) to 0.5 (rubber); the adopted rubber pads use 0.5 | Typical range |
| Timber prices | 70 x 70 mm $4.50/m, 45 x 120 mm $2.80/m, 45 x 70 mm $1.80/m, 10 % waste | Indicative 2026 retail |
| Frame hardware (GBN-DDR-003) | M8 x 120 bolt with washer $0.45 and 0.065 kg; M8 cross dowel $0.35 and 0.020 kg; 6 x 100 structural screw $0.20 and 0.020 kg; worktop bracket 0.030 kg; $1.00 of glue and small screws | Indicative 2026 retail; catalogue masses |

## A. Grid (R1)

- **Positions.** The 1,200 x 600 mm top holds a 48 x 24 grid of 1,152 positions: 144 tapped holes in the tile, 252 insert positions on the 50 mm sub-grid and 756 plain 6.6 mm holes. The first and last holes sit 12.5 mm from each edge [A1].
- **Tile continuity.** The tile's edges fall midway between grid lines, so its first hole is 12.5 mm from its edge and all 144 holes continue the field grid [A2]. A fixture can straddle both zones.
- **Ligaments.** Each 8 mm dowel bore sits at the center of a grid square, 17.7 mm from the nearest M6 hole, leaving a 10.7 mm ligament [A3]. The four counterbored fixing holes leave 7.5 mm [A4]. Both are ample for a 12.7 mm plate.

## B. Mass (context for R12)

- **Bench.** Frame timber 22.4 kg, worktop 7.2 kg, tile 3.0 kg, shelf 4.4 kg, inserts, feet and fasteners 2.4 kg, frame bolts, cross dowels, brackets and shelf screws 2.7 kg, and fixtures 1.7 kg give 43.8 kg [B1], against 41.9 kg in v0.2. The frame timber is lighter than in v0.2 because the long aprons no longer run through the legs (GBN-DDR-003); the bolts and brackets more than make up for it.
- **Ballast.** Two 400 x 400 x 35 mm concrete slabs weigh 12.9 kg each, 25.8 kg together; the ballasted bench is 69.6 kg [B2]. Each slab is light enough for one person to lift.

## C. Tipping and sliding (R12)

- **Base.** The feet are at 1,090 x 490 mm centers, so a push at the front edge acts at 900 mm against a 245 mm lever [C1].
- **Empty bench.** It tips at 117 N, below the 150 N target; along the bench it would take 260 N [C2]. R12 is not met by the empty bench.
- **Ballast.** At least 12.4 kg of ballast is needed [C3]. With the two slabs the bench tips at 186 N, a factor of 1.24 on 150 N [C4]. R12 is met on paper with the ballast in place.
- **Sliding.** On hard feet the empty bench would slide at about 86 N, before it tips. With the adopted rubber pads it slides at about 215 N empty and 341 N ballasted [C5], so a firm push no longer moves it. Sliding is not a requirement.
- **Anchor.** For the optional wall anchor, the tie force for a 150 N pull on the empty bench is only 34 N [C6], so light angle brackets suffice.

## D. Stiffness and strength (R6)

- **Worktop.** The largest plywood bay is 255 x 470 mm clear between rails and aprons [D1]. Under 500 N at its center the plywood deflects 0.19 mm relative to its supports [D2]. The TRL 2 strip estimate (0.41 mm) ignored the plate action.
- **Frame.** The two cross rails of that bay add 0.07 mm [D3] and the 45 x 120 mm long aprons, spanning 1,090 mm between legs, add 0.11 mm [D4]. The total is 0.37 mm against the 0.5 mm target [D5], with the joints treated as pinned (conservative) and the worktop not counted as stiffening the aprons.
- **Apron depth.** The v0.1 aprons, 45 x 95 mm, gave 0.49 mm, with almost no margin [D6]; the deeper aprons were accepted under GBN-DDR-002. 45 x 145 mm aprons would give 0.32 mm [D7], not enough gain to justify the extra depth.
- **Distributed load.** 150 kg over the top is 2.04 kPa. The plywood deflects 0.030 mm; each long apron 0.26 mm at a bending stress of 1.0 MPa, a sixteenth of the C16 strength [D8]. The legs see 0.10 MPa [D9].
- **Tile.** Spanning 255 mm between its packers, the tile deflects 0.061 mm under 500 N at its center, at 4.9 MPa [D10]. Heavy point loads on the tile therefore affect R5 while they act; the tile recovers elastically.
- **Shelf.** The slabs bend the shelf 0.38 mm over its 490 mm span [D11].

## E. Moisture and temperature (R3, R4)

- **Humidity band.** Between 40 and 60 % RH wood settles at 7.7 to 11.0 % moisture content; a top built at the middle, 9.35 %, swings ±1.65 % [E1].
- **Plywood field.** With the unsourced coefficient of 0.007 % per % moisture content, the field moves ±0.115 mm over 1,000 mm within the R3 humidity band [E2], and ±0.40 mm over the full 20 to 80 % operating range [E3]. The TRL 2 figure of up to 0.4 mm over 1,200 mm for a 5 % swing is consistent with this.
- **Hole to hole over 1,000 mm.** A CNC-drilled top reaches ±0.22 mm against the ±0.3 mm target [E4]. A template-drilled top reaches ±0.34 mm statistically against ±0.5 mm, but ±0.62 mm if every template step errs the same way [E4]. R3 is at risk for the template build and rests on an unsourced coefficient.
- **Tile.** The tile grows 0.069 mm over 300 mm, and 0.046 mm across the 200 mm dowel span, per 10 K [E5]. A PETG fixture with pins 200 mm apart mismatches the tile by 0.074 mm per 10 K [E6]; the diamond pin (section F) absorbs this along the pin line.

## F. Dowel location (R4)

- **Fit.** An 8 mm h6 pin in an H7 bore has 0 to 0.024 mm diametral clearance [F1].
- **Two round pins bind.** Pin and bore pitch errors of ±0.05 mm each add up to 0.10 mm, far more than the minimum clearance of zero, so a fixture on two round pins may not go down at all [F2]. The design now uses one round pin and one diamond (relieved) pin per precision fixture, the standard machinist's arrangement (BOM line 13).
- **Relocation.** With pins 200 mm apart, a point 100 mm from the round pin returns within 0.036 mm in the worst case and about 0.015 mm statistically, against 0.03 mm [F3]. R4 is at risk; pushing each fixture against the same side of its pins in use would bring the worst case close to zero. Hole position to ±0.05 mm by drill press and jig is not verifiable at TRL 3.

## G. Clamps and inserts (R7)

- **Lever.** The toe clamp's screw is 30 mm from the toe contact and 28 mm from the heel, so the part receives 0.483 of the screw tension. The 30 mm deep body, less its 6.6 mm slot, has a section modulus of 2,610 mm³ [G1].
- **TRL 2 clamp.** At 16 mm deep and 2 N·m, the clamp body would carry about 33 MPa, nearly three times the sustained limit for printed PETG [G3], so it would creep. The body is now 30 mm deep and the rated torque 1.6 N·m.
- **Revised clamp.** At 1.6 N·m the part receives 515 to 858 N over the nut factor range (target 500 N), at a peak body stress of 9.9 MPa against 12 MPa [G2, G4]. Printed on its side, the bending stress runs along the layers.
- **Inserts.** A screw-in insert resists 1.02 to 1.63 kN before the plywood shears around it, while the screw tension reaches 1.78 kN at the low nut factor; the factor is 0.57 to 0.92 [G5]. A screw-in insert therefore cannot guarantee 500 N at the part. On the tile, 12.7 mm of thread engagement is ample [G6] and R7 is met on paper, subject to PETG creep data.
- **Tee nuts (GBN-DDR-002).** Flanged M6 tee nuts pressed in from the underside now take the load at every insert position whose 19 mm flange has a clear underside: 130 of the 252 positions. The other 122 lie within the flange radius of an apron, cross rail or leg and keep a screw-in insert [G5b]. To pull out, a tee nut must punch its flange through the full sheet: 2.69 to 4.30 kN, a factor of 1.51 to 2.42 on the highest screw tension [G5c]. The flange bears on the plywood at 7.6 MPa against an assumed 10 MPa (factor 1.31), and the 9.5 mm barrel gives ample thread engagement [G5d]. R7 is met on paper at the tee-nut positions and not met at the 122 screw-in positions over the frame; Amish decided on 2026-10-02 to rate those positions light duty and ring them on the worktop in a contrasting colour: at 0.92 N·m the screw tension stays within the lowest insert strength, and the part receives 296 to 493 N [G5e].

## H. Fixture change (R8)

- Two screws out, two in, at 9 s each (12 turns at 2 turns per second plus 3 s to engage), 10 s to lift and place and 10 s to seat on the pins give 56 s against 60 s [H1]. R8 is met on paper with a thin margin; printed knobs or quarter-turn fasteners would widen it.

## I. Buildability (R9)

- **Printing.** The largest printed footprint is now the 190 mm fence segment, within a 200 x 200 mm bed; the TRL 2 fence was 400 mm long and would not have fitted [I1].
- **Tile.** Drilling and tapping 144 holes, reaming 9 bores and counterboring 4 takes about 4.2 h on a drill press with a tapping guide [I2], longer than the TRL 2 estimate of 2.5 h for tapping alone.

## K. Timber and cost (R10)

- **Timber.** The frame uses 3.43 m of 70 x 70 mm, 2.88 m of 45 x 120 mm and 3.92 m of 45 x 70 mm, 10.2 m in all [K1]. With 10 % waste and $23.40 of hardware (24 M8 x 120 bolts with washers, 24 M8 cross dowels, 16 structural screws and $1.00 of glue and small screws) the frame costs $57.00 [K2] (BOM line 1; $43.50 in v0.2, when the frame had no joints).
- **Inserts.** 130 tee nuts at $0.12 and 126 screw-in inserts at $0.10 (122 in the worktop, 4 in the tile rails) cost $28.20 [K2b] (BOM line 5).
- **Totals.** The 17-line BOM gives core parts of $272.20, the user-supplied dial indicator $15.00 and the optional anchor brackets $5.00, $292.20 in all [K3]. Besides the frame and inserts, the design-for-construction changes added the nine worktop brackets ($3.60, line 17), the arm clamps and drop rod (line 10, $12.00 to $15.00) and the longer screw set (line 12, $12.00 to $14.00). The eight shelf screws and the paint marker for the light-duty rings, added on 2026-10-02, take line 12 to $17.80 [K2c].
- **Against the value-engineering target.** Value-engineering target: USD 250 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 272.20 (USD 22.20 over the target, 8.9 %); everything including the indicator and anchor is 16.9 % over [K4]. Core plus indicator is $287.20, against $239.20 at TRL 2 [K5]. The main cost drivers and the savings worth trying are in the design decisions register (GBN-DEC-001, Value engineering).

## L. Results against every requirement

*Table 2. Requirement status from this note.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R7 | Clamp hold-down | Part 515 to 858 N at 1.6 N·m; clamp 9.9 MPa; tee nut factor 1.51 to 2.42 at 130 positions; screw-in insert factor 0.57 to 0.92 at 122 positions [G4, G5, G5b, G5c] | 500 N, no creep after 8 h at 25 °C | **Not met** at the 122 screw-in positions over the frame; met on paper at the tee nuts and on the tile |
| R3 | Coarse field hole position | CNC ±0.22 mm; template ±0.34 mm statistical, ±0.62 mm worst case over 1,000 mm [E4] | ±0.3 mm (CNC); ±0.5 mm (template) at 40 to 60 % RH | **At risk** (template build; unsourced coefficient) |
| R4 | Precision tile location | Relocation 0.036 mm worst case, 0.015 mm statistical [F3]; hole position not verifiable | ±0.05 mm; 0.03 mm | **At risk** |
| R5 | Flatness | Depends on the plate as supplied and on the plywood sheet | Tile 0.05 mm over 300 mm; worktop 0.5 mm over 1,000 mm | Not verifiable at TRL 3 |
| R10 | Parts cost | $272.20 core (indicator user-supplied) [K3, K4] | $250 value-engineering target (`budget_usd`) | Over the value-engineering target by $22.20 |
| R6 | Stiffness and load | 0.37 mm total, 0.19 mm local, under 500 N; 150 kg at 1.0 MPa in the aprons [D5, D8] | 0.5 mm; 150 kg | Met on paper |
| R8 | Fixture change | 56 s [H1] | 60 s | Met on paper (thin margin) |
| R9 | Buildability | Largest print 190 mm; tile about 4.2 h by drill press [I1, I2] | 200 x 200 mm bed; CNC optional | Met on paper |
| R12 | Stability and edges | 186 N with 25.8 kg of ballast; 117 N empty [C2, C4] | 150 N; edges 0.5 mm or more | Met on paper with ballast (not met empty) |
| R1 | Grid standard | 1,152 positions at 25 mm, 12.5 mm edge offset, tile on grid [A1, A2] | 25.00 mm, M6, 12.5 mm | Met by design |
| R2 | Worktop size and height | 1,200 x 600 mm at 900 mm, feet ±15 mm (model) | At least 1,200 x 600 mm; 900 mm ±15 mm | Met by design |
| R11 | Openness | build123d source, CERN-OHL-S-2.0 | As stated | Met by design |

Counts: 1 not met (R7, in part), 1 over the value-engineering target (R10), 2 at risk, 1 not verifiable at TRL 3, 4 met on paper, 3 met by design. R12 counts as met on paper because the ballast is part of the adopted design. In v0.2, R10 was met at $245.90; the joints, fixings and clamps that make the design buildable (GBN-DDR-003) added $22.50. In v0.1, R10 was not met ($239.20 against $220) and R7 was not met anywhere on the plywood field.

## Checks against the TRL 2 figures

*Table 3. TRL 2 claims (GBN-PRC-001 v0.2) against this note.*

| TRL 2 claim | This note | Action |
| --- | --- | --- |
| 1,152 positions: 144 tile, 252 inserts, 756 plain | Same [A1] | Stands |
| Bench about 40 kg | 43.8 kg with the deeper aprons and the frame bolts and brackets [B1] | Precis updated |
| Deflection about 0.3 to 0.4 mm under 500 N | 0.19 mm local; 0.49 mm with 45 x 95 aprons, 0.37 mm with 45 x 120 [D2, D5, D6] | Aprons deepened (DDR-002) |
| Tipping about 105 N empty, about 160 N with 20 kg | 117 N empty; 186 N with 25.8 kg [C2, C4] | Precis updated |
| Tile growth about 0.07 mm over 300 mm per 10 K | 0.069 mm [E5] | Stands |
| Moisture movement up to about 0.4 mm over 1,200 mm | ±0.115 mm over 1,000 mm at 40 to 60 % RH; ±0.40 mm over 20 to 80 % RH [E2, E3] | Precis updated; coefficient still unsourced |
| Dowel relocation about 0.03 mm on two dowels | Two round pins can bind; round plus diamond pin gives 0.036 mm worst case [F2, F3] | Diamond pin added |
| Clamp force about 0.8 kN at 2 N·m | 805 N, but 33 MPa in a 16 mm body [G3] | Deeper body, 1.6 N·m |
| Insert pull-out 2 to 4 kN (unverified) | 1.02 to 1.63 kN (assumed shear) [G5]; tee nuts 2.69 to 4.30 kN [G5c] | Tee nuts where the underside is clear (DDR-002) |
| 400 mm printed fence | Does not fit a 200 mm bed [I1] | Two 190 mm segments |
| Tapping about 2.5 h | 4.2 h including drilling, reaming and counterbores [I2] | Precis updated |
| Parts about $239 (with indicator) | $287.20 with indicator; $272.20 core [K3, K5] | Reported against the USD 250 value-engineering target |
