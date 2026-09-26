---
doc_id: GBN-CAL-001
title: GridBench sizing calculations
project: GridBench
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (grid, mass, tipping, stiffness, moisture and temperature, dowel location, clamps and inserts, fixture change, buildability, cost)
---

# GridBench sizing calculations

On paper, GridBench meets seven of its twelve requirements (four by calculation, three by design), has two at risk, has one that cannot be verified at TRL 3 and misses two. The misses are cost and clamp hold-down on the plywood field. R10 (cost) is not met: the core parts cost $239.20 against the $220 budget, even with the dial indicator user-supplied; it would be met under the $250 fallback budget, which awaits Amish. R7 (clamp hold-down) is not met on the plywood field, because a screw-in M6 insert in 18 mm plywood may pull out at the screw tension needed to give 500 N at the part (factor 0.57 to 0.92); on the aluminum tile R7 is met on paper. R3 (coarse field accuracy, template-drilled build) and R4 (relocation within 0.03 mm) are at risk. R5 (flatness) cannot be verified at TRL 3. The calculations changed four details of the TRL 2 concept: the printed toe clamp is deeper (30 mm instead of 16 mm) with a rated torque of 1.6 N·m instead of 2 N·m, every precision fixture carries one round and one diamond locating pin instead of two round pins, the fence is printed in two 190 mm segments that fit a 200 mm bed, and two concrete slabs on the shelf form the ballast. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace a push test for tipping, a pull test of clamps and inserts, or inspection of the tile. The empty bench tips at about 107 N at its front edge [C2]; it must be ballasted or anchored before use. See GBN-PRC-001, Safety.

## Scope and method

The note checks every requirement in GBN-REQ-001 v0.3 against the design in GBN-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, its derived dimensions and its grid functions, so the hole counts, bays, rail spans and foot positions used here are the ones in the STEP files and in drawing GBN-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes its output to `docs/04-calcs/sizing-output.txt`.

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
| Inserts | Pull-out by shear of the plywood on the insert's outer cylinder (10 mm by 13 mm) at 2.5 to 4 MPa | Assumption; no test data found |
| Friction | Levelling feet on a workshop floor, μ = 0.2 (hard plastic) to 0.5 (rubber) | Typical range |
| Timber prices | 70 x 70 mm $4.50/m, 45 x 95 mm $2.20/m, 45 x 70 mm $1.80/m, 10 % waste, $9 of bolts and screws | Indicative 2026 retail |

## A. Grid (R1)

- **Positions.** The 1,200 x 600 mm top holds a 48 x 24 grid of 1,152 positions: 144 tapped holes in the tile, 252 insert positions on the 50 mm sub-grid and 756 plain 6.6 mm holes. The first and last holes sit 12.5 mm from each edge [A1].
- **Tile continuity.** The tile's edges fall midway between grid lines, so its first hole is 12.5 mm from its edge and all 144 holes continue the field grid [A2]. A fixture can straddle both zones.
- **Ligaments.** Each 8 mm dowel bore sits at the center of a grid square, 17.7 mm from the nearest M6 hole, leaving a 10.7 mm ligament [A3]. The four counterbored fixing holes leave 7.5 mm [A4]. Both are ample for a 12.7 mm plate.

## B. Mass (context for R12)

- **Bench.** Frame 21.4 kg, worktop 7.2 kg, tile 3.0 kg, shelf 4.5 kg and small parts 4.1 kg give 40.2 kg [B1], matching the TRL 2 estimate of about 40 kg.
- **Ballast.** Two 400 x 400 x 35 mm concrete slabs weigh 12.9 kg each, 25.8 kg together; the ballasted bench is 65.9 kg [B2]. Each slab is light enough for one person to lift.

## C. Tipping and sliding (R12)

- **Base.** The feet are at 1,090 x 490 mm centers, so a push at the front edge acts at 900 mm against a 245 mm lever [C1].
- **Empty bench.** It tips at 107 N, below the 150 N target; along the bench it would take 239 N [C2]. R12 is not met by the empty bench.
- **Ballast.** At least 16.0 kg of ballast is needed [C3]. With the two slabs the bench tips at 176 N, a factor of 1.17 on 150 N [C4]. R12 is met on paper with the ballast in place.
- **Sliding.** On hard feet the empty bench slides at about 79 N, before it tips; ballasted, at 129 to 323 N [C5]. Sliding is not a requirement, but rubber pads make the bench feel firmer.
- **Anchor.** For the optional wall anchor, the tie force for a 150 N pull on the empty bench is only 45 N [C6], so light angle brackets suffice.

## D. Stiffness and strength (R6)

- **Worktop.** The largest plywood bay is 255 x 470 mm clear between rails and aprons [D1]. Under 500 N at its center the plywood deflects 0.19 mm relative to its supports [D2]. The TRL 2 strip estimate (0.41 mm) ignored the plate action.
- **Frame.** The two cross rails of that bay add 0.07 mm [D3] and the 45 x 95 mm long aprons, spanning 1,090 mm between legs, add 0.22 mm [D4]. The total is 0.49 mm against the 0.5 mm target [D5]: met on paper, with almost no margin, and only because the joints are treated as pinned (conservative) and the worktop is not counted as stiffening the aprons.
- **Deeper aprons.** 45 x 120 mm aprons would bring the total to 0.37 mm [D6], and 45 x 145 mm to 0.32 mm [D7]. This is left as a suggestion in the review note; the design is unchanged.
- **Distributed load.** 150 kg over the top is 2.04 kPa. The plywood deflects 0.030 mm; each long apron 0.52 mm at a bending stress of 1.6 MPa, a tenth of the C16 strength [D8]. The legs see 0.10 MPa [D9].
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
- **Inserts.** A screw-in insert resists 1.02 to 1.63 kN before the plywood shears around it, while the screw tension reaches 1.78 kN at the low nut factor; the factor is 0.57 to 0.92 [G5]. On the plywood field, R7 is not met: the torque that guarantees 500 N at the part can pull an insert. On the tile, 12.7 mm of thread engagement is ample [G6] and R7 is met on paper, subject to PETG creep data.
- **Option (awaiting Amish).** Flanged tee nuts pressed in from the underside would bear on the plywood instead of shearing it. This is recorded in the review note, not applied.

## H. Fixture change (R8)

- Two screws out, two in, at 9 s each (12 turns at 2 turns per second plus 3 s to engage), 10 s to lift and place and 10 s to seat on the pins give 56 s against 60 s [H1]. R8 is met on paper with a thin margin; printed knobs or quarter-turn fasteners would widen it.

## I. Buildability (R9)

- **Printing.** The largest printed footprint is now the 190 mm fence segment, within a 200 x 200 mm bed; the TRL 2 fence was 400 mm long and would not have fitted [I1].
- **Tile.** Drilling and tapping 144 holes, reaming 9 bores and counterboring 4 takes about 4.2 h on a drill press with a tapping guide [I2], longer than the TRL 2 estimate of 2.5 h for tapping alone.

## K. Timber and cost (R10)

- **Timber.** The frame uses 3.43 m of 70 x 70 mm, 3.16 m of 45 x 95 mm and 3.92 m of 45 x 70 mm, 10.5 m in all [K1], for $41.38 with waste and hardware [K2] (BOM line 1, $41.40).
- **Totals.** The 16-line BOM gives core parts of $239.20, the user-supplied dial indicator $15.00 and the optional anchor brackets $5.00, $259.20 in all [K3].
- **Against the budgets.** Core parts are 8.7 % over the $220 `budget_usd`. Against the proposed $250 fallback, core parts are 4.3 % under and everything is 3.7 % over [K4]. The TRL 3 equivalent of the TRL 2 total (core plus indicator) is $254.20, up from $239.20, mainly for the diamond pins, the ballast and the tile tooling now priced separately [K5].

## L. Results against every requirement

*Table 2. Requirement status from this note.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R10 | Parts cost | $239.20 core (indicator user-supplied) [K3] | $220 (`budget_usd`); $250 fallback awaiting Amish | **Not met** at $220; met at $250 |
| R7 | Clamp hold-down | Part 515 to 858 N at 1.6 N·m; clamp 9.9 MPa; insert factor 0.57 to 0.92 [G4, G5] | 500 N, no creep after 8 h at 25 °C | **Not met** on the plywood field (insert pull-out); met on paper on the tile |
| R3 | Coarse field hole position | CNC ±0.22 mm; template ±0.34 mm statistical, ±0.62 mm worst case over 1,000 mm [E4] | ±0.3 mm (CNC); ±0.5 mm (template) at 40 to 60 % RH | **At risk** (template build; unsourced coefficient) |
| R4 | Precision tile location | Relocation 0.036 mm worst case, 0.015 mm statistical [F3]; hole position not verifiable | ±0.05 mm; 0.03 mm | **At risk** |
| R5 | Flatness | Depends on the plate as supplied and on the plywood sheet | Tile 0.05 mm over 300 mm; worktop 0.5 mm over 1,000 mm | Not verifiable at TRL 3 |
| R6 | Stiffness and load | 0.49 mm total, 0.19 mm local, under 500 N; 150 kg at 1.6 MPa in the aprons [D5, D8] | 0.5 mm; 150 kg | Met on paper (thin margin) |
| R8 | Fixture change | 56 s [H1] | 60 s | Met on paper (thin margin) |
| R9 | Buildability | Largest print 190 mm; tile about 4.2 h by drill press [I1, I2] | 200 x 200 mm bed; CNC optional | Met on paper |
| R12 | Stability and edges | 176 N with 25.8 kg of ballast; 107 N empty [C2, C4] | 150 N; edges 0.5 mm or more | Met on paper with ballast (not met empty) |
| R1 | Grid standard | 1,152 positions at 25 mm, 12.5 mm edge offset, tile on grid [A1, A2] | 25.00 mm, M6, 12.5 mm | Met by design |
| R2 | Worktop size and height | 1,200 x 600 mm at 900 mm, feet ±15 mm (model) | At least 1,200 x 600 mm; 900 mm ±15 mm | Met by design |
| R11 | Openness | build123d source, CERN-OHL-S-2.0 | As stated | Met by design |

Counts: 2 not met, 2 at risk, 1 not verifiable at TRL 3, 4 met on paper, 3 met by design. R12 counts as met on paper because the ballast is part of the adopted design.

## Checks against the TRL 2 figures

*Table 3. TRL 2 claims (GBN-PRC-001 v0.2) against this note.*

| TRL 2 claim | This note | Action |
| --- | --- | --- |
| 1,152 positions: 144 tile, 252 inserts, 756 plain | Same [A1] | Stands |
| Bench about 40 kg | 40.2 kg [B1] | Stands |
| Deflection about 0.3 to 0.4 mm under 500 N | 0.19 mm local, 0.49 mm with the frame [D2, D5] | Precis updated |
| Tipping about 105 N empty, about 160 N with 20 kg | 107 N empty; 176 N with 25.8 kg [C2, C4] | Precis updated |
| Tile growth about 0.07 mm over 300 mm per 10 K | 0.069 mm [E5] | Stands |
| Moisture movement up to about 0.4 mm over 1,200 mm | ±0.115 mm over 1,000 mm at 40 to 60 % RH; ±0.40 mm over 20 to 80 % RH [E2, E3] | Precis updated; coefficient still unsourced |
| Dowel relocation about 0.03 mm on two dowels | Two round pins can bind; round plus diamond pin gives 0.036 mm worst case [F2, F3] | Diamond pin added |
| Clamp force about 0.8 kN at 2 N·m | 805 N, but 33 MPa in a 16 mm body [G3] | Deeper body, 1.6 N·m |
| Insert pull-out 2 to 4 kN (unverified) | 1.02 to 1.63 kN (assumed shear) [G5] | R7 not met on the plywood field |
| 400 mm printed fence | Does not fit a 200 mm bed [I1] | Two 190 mm segments |
| Tapping about 2.5 h | 4.2 h including drilling, reaming and counterbores [I2] | Precis updated |
| Parts about $239 (with indicator) | $254.20 with indicator; $239.20 core [K3, K5] | BOM, precis and requirements updated |
