# GridBench

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Advanced Manufacturing · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $220 USD · **Difficulty:** 2 of 5

A modular fixture and workbench standard: a 25 mm hole grid plate with printable and machined clamps, stops and jigs, so community workshops can hold, assemble and test parts repeatably.

![GridBench concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Concept rationale

A shared grid lets jigs designed for one project be reused in any workshop, which is the manufacturing counterpart of the lab's documentation kit, ReadyKit. GridBench adopts the 25 mm, M6 pattern of metric optical breadboards ([RP Photonics](https://www.rp-photonics.com/optical_breadboards.html)) rather than inventing a new one, so commercial accessories fit from day one, and splits the top into a cheap plywood field for area and a small aluminum tile for precision, so precision is paid for only where it is used.

Keeping it open and garage-buildable is the point: a fixture standard only helps if many benches share it. A timber frame, one sheet of plywood, one aluminum plate and printed clamps can be built with a drill press and taps, and each jig can be published as a build123d file that fits any GridBench.

## Burning platform

Most making happens in small firms. Small and medium enterprises are about 90 % of businesses and more than half of employment worldwide ([World Bank](https://www.worldbank.org/ext/en/topic/competitiveness/small-and-medium-enterprises-smes-finance)), and in the United States more than 98 % of the roughly 244,000 manufacturers employ fewer than 500 people ([ITIF, citing the National Association of Manufacturers](https://itif.org/publications/2025/06/17/mep-program-critical-for-small-manufacturers-underpinning-america-s-manufacturing-revival/)). These firms rarely own modular fixture systems: a 1,200 x 800 mm fixture table from one leading system starts at about $2,561 before clamps ([Siegmund System 16 listing](https://weldingtablesandfixtures.com/products/4-161025-p-siegmund-1200x800mm-basic-system-16-welding-table)).

Demand for local, repeatable making is rising with repair. The world generated a record 62 million tonnes of e-waste in 2022 and only 22 % was formally recycled ([ITU and UNITAR, Global E-waste Monitor 2024](https://www.itu.int/hub/2024/04/the-world-generated-62-million-tonnes-of-electronic-waste-in-just-one-year-and-recycled-way-too-little-un-agencies-warn/)), and repair and remanufacture depend on holding parts accurately without factory tooling.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Makerspaces and fab labs | Shared bench where members set up a published jig in minutes; the Fab Lab network alone has over 1,750 labs in 100 countries ([Fab Foundation](https://fabfoundation.org/about/)) |
| Electronics and appliance repair | Holding boards, housings and motors for disassembly, rework and testing with the indicator post |
| Small-batch manufacturing | Drilling, gluing and assembly jigs for runs of 10 to 500 parts |
| Technical education | Teaching datums, location and clamping on a bench students can build |
| Open hardware and research labs | Build and check fixtures shipped with designs; optics and sensor setups on the M6 grid |
| Furniture and joinery | Stops and fences for repeat cuts and drilling on the plywood field |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| European Union | The repair directive must apply in member states by 31 July 2026, requiring producers to offer repair and spare parts ([European Commission](https://commission.europa.eu/law/law-topic/consumer-protection-law/directive-repair-goods_en)); independent repairers need low-cost, repeatable workholding. |
| United States | More than 98 % of manufacturers employ fewer than 500 people ([ITIF, citing NAM](https://itif.org/publications/2025/06/17/mep-program-critical-for-small-manufacturers-underpinning-america-s-manufacturing-revival/)); makerspaces and job shops can share jigs as files. |
| India | MSMEs account for 30.1 % of GDP and 35.4 % of manufacturing ([Press Information Bureau, 2025](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2142170&reg=48&lang=2)); consistent quality helps small units supply larger buyers. |
| Ghana | Suame Magazine in Kumasi, an artisan engineering cluster, had over 80,000 people working in it by 2018 ([Adu-Gyamfi and Adjei, AfricaLics working paper](https://openair.africa/wp-content/uploads/2018/09/WP-16.pdf)); shared jigs could make artisan-made parts interchangeable. |
| Kenya | The informal sector created about 85 % of new jobs in 2023, according to the national statistics bureau ([Kenyan Wallstreet, reporting KNBS](https://kenyanwallstreet.com/informal-sector-creates-85-of-new-jobs-in-kenya-in-2023-knbs-survey)); jua kali workshops make parts with hand tools and could build the bench locally. |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. Advanced manufacturing was the lab's thinnest applied area. The real-world trigger was Gridfinity, a free 42 mm storage grid created in 2022 ([Wikipedia](https://en.wikipedia.org/wiki/Gridfinity)) that makers now extend without any central supplier; no open grid does the same for holding and checking parts.

## Problem

Repeatable building needs repeatable fixturing, and commercial modular fixture systems are costly while improvised jigs are one-off. Problem statement: [docs/01-problem.md](docs/01-problem.md).

## Concept

A 1,200 x 600 mm workbench with a 25 mm, M6 hole grid: a plywood field with threaded inserts for general holding, a flush 300 x 300 mm aluminum precision tile with dowel bores for repeatable location, printed clamps, stops and V-blocks, and an instrument post with a dial indicator to check parts in place. Parts cost is estimated at about $239, above the $220 budget; options are in the review note.

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Requirements: [docs/03-requirements.md](docs/03-requirements.md)

## Key components

- Bolted timber bench frame with levelling feet and a lower shelf
- 18 mm plywood grid worktop, 25 mm pitch, M6 inserts on a 50 mm sub-grid
- Aluminum precision tile, 300 x 300 mm, 144 M6 holes and 9 dowel bores 8 mm H7
- Hardened 8 mm dowel pins
- Printable clamp, stop, fence and V-block library
- Instrument post with a 0.01 mm dial indicator

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Drilling, tapping and clamping create chip, projectile and pinch hazards: wear eye protection and secure work before cutting. The empty bench can tip under a firm push at the top edge; ballast the shelf or anchor it to a wall. Printed clamps can crack under overload; respect the rated screw torque. Not for welding or hot work.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (GBN-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `GBN-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.
