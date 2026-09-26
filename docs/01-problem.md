---
doc_id: GBN-PRB-001
title: GridBench problem statement
project: GridBench
doc_type: Problem statement
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
  change: Populate to TRL 2 (users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; grid choice and budget scope adopted as recommended (GBN-DDR-001), humidity figures sourced
---

# GridBench problem statement

Small workshops cannot make the same part twice to the same standard without a way to put the part in the same place every time, and the tools that do this well are priced for industry while home-made jigs cannot be shared.

## The problem

Repeatable making depends on fixturing: a datum surface, locating features and clamps that hold each part in a known position while it is drilled, glued, assembled or measured. Industry solves this with modular fixture systems built on a hole grid. A 1,200 x 800 mm welding table from one well-known system, with 16 mm bores on a 50 mm grid, starts at about $2,561 before any clamps or stops ([Siegmund System 16, US distributor listing](https://weldingtablesandfixtures.com/products/4-161025-p-siegmund-1200x800mm-basic-system-16-welding-table)). That is more than ten times the whole prototype budget of this project.

Community workshops, makerspaces and informal engineering clusters instead build one-off jigs from scrap. These work, but each is tied to one bench and one person, is rarely documented, and cannot be sent to another workshop as a file. When a design from the lab's portfolio is built in two places, the two builds differ because the holding and checking steps differ.

The missing piece is an open, cheap, documented grid standard: a bench surface with a fixed hole pattern, a library of printable and machinable fixtures that fit it, and a way to publish a jig as a file that works on any bench built to the same pattern.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Makerspace or fab lab technician | A shared bench where members can set up a known jig in minutes and check parts | Mixed-skill users, shared tools, 3D printers and often a CNC router |
| Small manufacturer or repair shop | Batch assembly and inspection of 10 to 500 parts without buying an industrial fixture table | Workshop of 1 to 20 people, limited capital |
| Informal-sector artisan cluster | Consistent parts for customers and buyers, with tools made locally | Hand tools, drill press, access to a lathe or shared machine shop |
| Teacher or technical college | A teaching bench that shows datums, location and clamping | Classroom, safety supervision, repeated use by many students |
| Open hardware designer | A way to ship a build jig with a design, as a file | Designs published in repos like this one |

## Operating environment

- Indoor workshop, 10 to 35 °C, 20 to 80 % relative humidity, not air-conditioned in many target regions. Over that humidity range wood settles at about 4.5 to 16 % moisture content ([USDA Forest Products Laboratory, *Wood Handbook*, FPL-GTR-190, Table 4-2](https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_04.pdf)), so a plywood top moves with the seasons (GBN-CAL-001, section E).
- Loads from hand assembly, drilling with a hand drill or drill press, light filing and gluing. Not for welding heat or heavy machining forces.
- Users range from trained machinists to first-time makers.

## Constraints

- Garage-buildable prototype, about $220 USD in parts for the bench, grid, tile and fixture set (the dial indicator is user-supplied, GBN-DDR-001 A1), using timber or steel sections, plywood, one aluminum plate and 3D-printed parts.
- Build with common workshop tools: a drill press or hand router with a template, taps and a reamer. A shared CNC router speeds up the worktop but must not be required.
- The grid must be compatible with something already made in volume, so that commercial accessories fit.
- All files open: CAD in build123d source, hardware under CERN-OHL-S-2.0.

## Prior work

- **Metric optical breadboards** use M6 tapped holes on a 25 mm grid; imperial boards use 1/4-20 on 1 in ([RP Photonics Encyclopedia, "Optical breadboards"](https://www.rp-photonics.com/optical_breadboards.html)). This is a mature, precise grid with a large accessory market, but aluminum or steel breadboards of bench size are costly and too fine for rough work.
- **Modular welding and fixture tables** (for example Siegmund System 16, above) use large bores on a 50 mm grid with hardened surfaces. They are precise and robust, but priced for industry.
- **Machinist fixture plates** combine tapped holes with separate reamed dowel positions so that parts locate on pins and clamp on threads; Saunders Machine Works, for example, specifies dowel pin and bore tolerances in the ten-thousandths of an inch ([SMW fixture plate FAQ](https://saundersmachineworks.com/pages/fixture-plate-faq)). GridBench borrows this split of "locate on dowels, clamp on threads".
- **Multifunction woodworking tables** use 20 mm dog holes on a 96 mm pitch ([In The Woodshop, building an MFT](https://www.inthewoodshop.com/Powered%20Tools%20and%20Machinery/BuildingMFT1.html)). Widely copied and cheap, but coarse and not meant for small parts or measurement.
- **Open grid storage systems** show how fast a shared grid spreads when files are free: Gridfinity, designed by Zack Freedman in 2022 on a 42 mm grid ([Wikipedia, "Gridfinity"](https://en.wikipedia.org/wiki/Gridfinity)), and Multiboard on a 25 mm grid for walls ([GridPilot comparison](https://gridpilot.us/blog/gridfinity-vs-multiboard-vs-minutegrid)). Gridfinity's license is non-commercial, which limits use by small businesses. Neither is a fixture or workholding standard.

No open standard found combines a cheap worktop, a precision zone and a fixture library on one grid.

## Out of scope

- Welding tables (heat, spatter and weld current need steel tops).
- Heavy machining (milling forces need a machine table, not a bench).
- Powered or automated fixtures.

## Co-design and validation checklist

- [ ] Identify two or three first user workshops (for example a fab lab, a small repair business, a technical college) and a local partner. Proposed, awaiting Amish.
- [ ] Observe how those workshops hold and check parts today, and list the five most common jigs.
- [ ] Confirm which tools each workshop has (CNC router, drill press, lathe, 3D printer).
- [ ] Agree what "repeatable" means for their parts (target tolerance) before fixing R3 and R4.

## Open questions

- Grid: 25 mm with M6 only at first, with a coarser 50 mm variant for heavy work considered later. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (GBN-DDR-001 A2).
- Which workshops test the first benches, and in which countries? No recommendation made. Proposed, awaiting Amish (GBN-DDR-001 O1).
