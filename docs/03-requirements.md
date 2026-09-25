---
doc_id: GBN-REQ-001
title: GridBench requirements
project: GridBench
doc_type: Requirements
version: "0.2"
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
---

# GridBench requirements

Twelve requirements define a garage-built grid bench and fixture set. At concept stage, three are not met or are at risk: cost (R10), tipping stability without ballast (R12) and the long-span accuracy of the plywood field in humid seasons (R3). Status values are estimates from the design precis (GBN-PRC-001) and must be checked by calculation at TRL 3 and by test later.

## Requirements

Table 1. GridBench requirements and concept status.

| ID | Requirement | Target | Verification | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Grid standard | 25.00 mm pitch in X and Y, M6 threads, hole centers 12.5 mm from the worktop edges; fits metric optical breadboard accessories | Inspection of drawing; fit test with a commercial M6 accessory | Met by design |
| R2 | Worktop size and height | At least 1,200 x 600 mm; top at 900 mm, adjustable ±15 mm with levelling feet | Measurement | Met by design |
| R3 | Coarse field hole position | ±0.3 mm hole to hole over 1,000 mm at 40 to 60 % RH (template-drilled build: ±0.5 mm) | Measurement with steel rule and pin gauges | At risk: plywood moisture movement could reach about 0.4 mm over 1,200 mm (estimate) |
| R4 | Precision tile location | Hole position ±0.05 mm; a part relocated on two 8 mm dowels returns within 0.03 mm | Dial indicator test, 10 relocations | Unverified; depends on machining access (drill press with jig, or CNC) |
| R5 | Flatness | Tile 0.05 mm over 300 mm; worktop 0.5 mm over 1,000 mm | Straightedge and feeler gauges | Tile met if bought as cast tooling plate; worktop unverified |
| R6 | Stiffness and load | 150 kg distributed load; deflection 0.5 mm or less under 500 N at the middle of a bay | Load test | Met by estimate (about 0.3 to 0.4 mm) |
| R7 | Clamp hold-down | Each printed toe clamp holds 500 N at the part with no visible creep after 8 h at 25 °C | Spring scale pull test | Unverified (PETG creep) |
| R8 | Fixture change | Swap one fixture for another in 60 s or less with one 5 mm hex key | Timed trial | Met by design |
| R9 | Buildability | Built with hand and garage tools plus an FDM printer (200 x 200 mm bed); CNC optional | Build review | Met by design |
| R10 | Parts cost | $220 or less for bench, grid, tile, fixture set and indicator | Priced BOM | **Not met: about $239 (indicative)** |
| R11 | Openness | All geometry as build123d source; fixture library parametric; CERN-OHL-S-2.0 | Repository review | Met by design |
| R12 | Stability and edges | No tipping under 150 N horizontal at the top edge; all exposed edges chamfered or rounded 0.5 mm or more | Push test; inspection | **Not met without ballast:** about 105 N empty, about 160 N with 20 kg on the shelf (estimates) |

## Design load case

- Distributed load: 150 kg over the worktop (a fixture set, tools and parts).
- Point load: 500 N from a person leaning on a clamped part, at the middle of a bay between cross rails.
- Horizontal push: 150 N at the front edge of the worktop, as when pushing a tight part onto dowels or filing.

## Assumptions

- Birch plywood with a modulus of about 7 GPa along the face grain (estimate, to be checked at TRL 3).
- Pine or equivalent softwood frame at about 500 kg/m³.
- Workshop humidity swings of about 5 % in wood moisture content between seasons.

## Requirements not met

- **R10 cost:** about $239 against $220. Options are in the precis and the review note.
- **R12 stability:** the empty bench is too light to resist 150 N at the top edge. Ballast on the shelf or a wall anchor is needed.
- **R3 at risk:** the plywood field may drift with humidity over its full length. The precision tile carries all tight-tolerance work.
