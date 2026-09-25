# GridBench

**Area:** Advanced Manufacturing · **Status:** Concept · **Prototype budget:** about $220 USD · **Difficulty:** 2 of 5

A modular fixture and workbench standard: a 25 mm hole grid plate with printable and machined clamps, stops and jigs, so community workshops can hold, assemble and test parts repeatably.

## Concept rationale

A shared grid lets jigs designed for one project be reused in any workshop, which is the manufacturing counterpart of the documentation kit.

## Burning platform

Local manufacturing of repairable products depends on small workshops producing consistent parts without expensive tooling.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. Advanced manufacturing was the lab's thinnest applied area.

## Problem

Repeatable building needs repeatable fixturing, and commercial modular fixture systems are costly while improvised jigs are one-off.

## Concept

A modular fixture and workbench standard: a 25 mm hole grid plate with printable and machined clamps, stops and jigs, so community workshops can hold, assemble and test parts repeatably.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Plywood or aluminum grid plate, 25 mm pitch
- Printable clamp and stop library
- Machined dowel pins and bushings
- Bench frame with levelling feet
- Test instrument mounts

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Clamps and machining create pinch and projectile hazards; wear eye protection and secure work before cutting.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.
