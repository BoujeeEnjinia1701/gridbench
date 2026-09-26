---
doc_id: GBN-REQ-001
title: GridBench requirements
project: GridBench
doc_type: Requirements
version: "0.4"
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
  change: Populate to TRL 2 (12 measurable requirements, status against the concept)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from GBN-CAL-001; R10 redefined to exclude the user-supplied indicator and R12 assessed with ballast (GBN-DDR-001)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# GridBench requirements

Twelve requirements define a garage-built grid bench and fixture set. The TRL 3 calculations (GBN-CAL-001 v0.2) find one not met in part: clamp hold-down (R7) at the 122 insert positions that sit over a frame member, where a screw-in insert may pull out. Two are at risk (R3, R4), one cannot be verified on paper (R5), five are met on paper and three are met by design. R10 changed at v0.4 under GBN-DDR-002: its target is now $250, the `budget_usd` Amish set on 2026-09-25, and it is met. At v0.3, under GBN-DDR-001, R10 was redefined to exclude the user-supplied dial indicator and R12 is assessed with the shelf ballast in place.

## Requirements

Table 1. GridBench requirements and TRL 3 status (GBN-CAL-001, Table 2).

| ID | Requirement | Target | Verification | TRL 3 status |
| --- | --- | --- | --- | --- |
| R1 | Grid standard | 25.00 mm pitch in X and Y, M6 threads, hole centers 12.5 mm from the worktop edges; fits metric optical breadboard accessories | Inspection of drawing; fit test with a commercial M6 accessory | Met by design: 1,152 positions, tile on the same grid |
| R2 | Worktop size and height | At least 1,200 x 600 mm; top at 900 mm, adjustable ±15 mm with levelling feet | Measurement | Met by design |
| R3 | Coarse field hole position | ±0.3 mm hole to hole over 1,000 mm at 40 to 60 % RH (template-drilled build: ±0.5 mm) | Measurement with steel rule and pin gauges | **At risk:** CNC ±0.22 mm; template ±0.34 mm statistical, ±0.62 mm worst case; moisture coefficient unsourced |
| R4 | Precision tile location | Hole position ±0.05 mm; a part relocated on two 8 mm dowels (one round, one diamond) returns within 0.03 mm | Dial indicator test, 10 relocations | **At risk:** 0.036 mm worst case, 0.015 mm statistical; hole position not verifiable at TRL 3 |
| R5 | Flatness | Tile 0.05 mm over 300 mm; worktop 0.5 mm over 1,000 mm | Straightedge and feeler gauges | Not verifiable at TRL 3 (depends on the plate and sheet as supplied) |
| R6 | Stiffness and load | 150 kg distributed load; deflection 0.5 mm or less under 500 N at the middle of a bay | Load test | Met on paper: 0.37 mm with 45 x 120 mm aprons; 150 kg at a sixteenth of the timber strength |
| R7 | Clamp hold-down | Each printed toe clamp holds 500 N at the part with no visible creep after 8 h at 25 °C | Spring scale pull test | **Not met at the 122 screw-in positions over the frame** (pull-out factor 0.57 to 0.92); met on paper at the 130 tee-nut positions (factor 1.51 to 2.42) and on the tile (515 to 858 N at 1.6 N·m, 9.9 MPa) |
| R8 | Fixture change | Swap one fixture for another in 60 s or less with one 5 mm hex key | Timed trial | Met on paper: 56 s (thin margin) |
| R9 | Buildability | Built with hand and garage tools plus an FDM printer (200 x 200 mm bed); CNC optional | Build review | Met on paper: largest print 190 mm; tile about 4.2 h by drill press |
| R10 | Parts cost | $250 or less (`budget_usd`, GBN-DDR-002) for bench, grid, tile and fixture set; the dial indicator is user-supplied and excluded (GBN-DDR-001 A1) | Priced BOM | Met on paper: $245.90 ($4.10 margin) |
| R11 | Openness | All geometry as build123d source; fixture library parametric; CERN-OHL-S-2.0 | Repository review | Met by design |
| R12 | Stability and edges | No tipping under 150 N horizontal at the top edge, with the shelf ballast in place; all exposed edges chamfered or rounded 0.5 mm or more | Push test; inspection | Met on paper with 25.8 kg of ballast (181 N); the empty bench tips at 112 N |

## Design load case

- Distributed load: 150 kg over the worktop (a fixture set, tools and parts).
- Point load: 500 N from a person leaning on a clamped part, at the middle of a bay between cross rails.
- Horizontal push: 150 N at the front edge of the worktop, as when pushing a tight part onto dowels or filing.

## Assumptions

- Birch plywood with a modulus of about 7 GPa, mean of the two in-plane directions (still an assumption; GBN-CAL-001, Table 1).
- C16 softwood frame at about 500 kg/m³, mean modulus 8 GPa.
- Workshop humidity between 40 and 60 % RH for R3, a moisture content swing of ±1.65 % (USDA *Wood Handbook*, Table 4-2).

## Requirements not met

- **R7 clamp hold-down at the 122 screw-in positions over the frame:** the screw tension that guarantees 500 N at the part can exceed the estimated pull-out strength of a screw-in insert. Tee nuts, decided under GBN-DDR-002, cannot be fitted there because a frame member blocks the underside. Options, with a light-duty rating recommended, are in GBN-DDR-002 (O4), proposed, awaiting Amish.
- **R3 and R4 at risk:** see GBN-CAL-001, sections E and F. The precision tile carries all tight-tolerance work.
