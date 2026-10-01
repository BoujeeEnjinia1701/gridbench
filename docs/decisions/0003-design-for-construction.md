---
doc_id: GBN-DDR-003
title: GridBench design for construction
project: GridBench
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** proposed. Made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. Nothing here changes what the bench does, its pitch or its safety case.

## Context

On 2026-09-30 Amish approved the illustrated build plan format and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of GBN-DDR-002 showed what GridBench does and carried the right sizes, but several parts could not be made, fixed or assembled as drawn. Checking the model with build123d (solid intersections, distances and grid positions) found the problems below.

The changes keep what the bench does: the same 1,200 x 600 mm worktop at 900 mm, the same 25 mm grid with 1,152 positions, the same 130 tee nuts and 122 screw-in inserts, the same precision tile, pins, clamps, fence, stops, V-block, instrument post, ballast and feet. Every change is in `cad/src/model.py`, which now also runs 92 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must not touch are apart by at least the stated clearance. All 92 pass.

## Options considered

For each problem the simplest physically sound fix that a garage workshop can make was chosen. Where a fix had a cheaper alternative that would change how the bench is used (for example gluing the frame instead of bolting it), the alternative is noted in the Why column and left for value engineering.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The long aprons ran the full 1,160 mm through the legs: 1.5 litres of each apron overlapped the four legs. Nothing joined any frame member to a leg. | Long aprons cut to 1,020 mm and butted between the legs, flush with their tops and outside faces. Every apron and low rail end is held by two M8 x 120 bolts through the leg into M8 cross dowels (barrel nuts) set 40 mm in from the member's end. The end-apron bolts (50 and 100 mm up from the apron's lower edge) are staggered against the long-apron bolts (20 and 80 mm up) so the two pairs miss each other inside the leg. | A bolt and cross dowel joint is the usual knock-down bench joint: square ends, straight holes, no housing to cut, and it can be taken apart to move the bench. It keeps the BOM's bolted timber frame. Gluing instead would be cheaper but permanent. |
| P2 | The cross rail at 502.5 mm (under the tile's right edge) passed 15 mm into the two right-hand legs. | That rail is notched 15 x 25 mm at both ends, full height, on the side toward the legs. | Keeps the rail under the tile's right edge and the four tile fixing screws where they were; one saw cut each end. |
| P3 | The cross rails had no fixing. | Two 6 x 100 mm structural screws through the apron into each rail end. | Simple, strong enough for 250 N per rail [D3], and the screw heads are hidden under the worktop overhang. |
| P4 | The shelf was exactly as long as the gap between the legs (1,020 mm), so it could not be put in. | Shelf 1,010 mm long, 5 mm clear of the legs at each end; it slides in from the front above the front low rail and drops onto both rails. | It now fits and still bears 45 mm on each low rail. |
| P5 | The tile filled its pocket with no clearance and square corners, while a routed pocket has round corners. | Pocket 301 x 301 mm (0.5 mm clear all round) with an 8 mm relief hole on each corner. | The tile drops in by hand and seats on its packers. The tile still sits on the grid to within the 0.5 mm clearance, which is inside R3's field tolerance; the tile's own holes carry the precise work. |
| P6 | The tile's four counterbored fixing holes had nothing to screw into: no thread in the rails or packers. | Four M6 screw-in inserts driven into the two tile rails through the packers, and four M6 x 20 cap screws in the counterbores. | Reuses the insert already in the BOM; a cap screw head (10 mm) sits below the surface in the 11 mm by 6.5 mm counterbore. |
| P7 | Nothing held the worktop to the frame. | Nine steel angle brackets, 30 x 30 x 3 mm and 20 mm wide, on the inside faces of the long aprons (four each) and the left end apron (one), each with one screw into the apron and one up into the worktop. Each sits midway between two threaded positions, 5.5 mm clear of the nearest tee nut flange. | Screws through the top would block grid holes. The brackets miss every tee nut and cross rail (checked). The right end has no bracket because the cross rail beside it leaves no room; the end apron and legs still carry it. |
| P8 | The levelling feet's stems floated 1 mm into the solid leg. | Each leg end bored 12 mm, 60 mm deep, with an M10 T-nut tapped in; the foot screws through it. | This is how the BOM's "M10 T-nut in the leg" works; the T-nut flange bears on the leg end. |
| P9 | The fence segments, V-block, instrument post foot and one toe clamp sat on unthreaded holes or between holes, so they could not be screwed down; the toe clamp screws missed the tile holes. | Every fixture moved to threaded positions: fence segments centred 287.5 and 87.5 mm left of centre on the 50 mm sub-grid, 10 mm apart, each with two counterbored M6 x 30 screws; V-block on two M6 x 30 screws; post foot (now 74 x 74 mm) on two M6 x 30 screws; toe clamp screws on tile holes (as the appearance model already had them). Stop pins got a 6.3 mm spigot into a plain hole. A screw-length rule follows: on the plywood a screw reaches 15 to 18 mm below the surface (it then engages a tee nut or a screw-in insert fully); on the tile, no more than 12 mm. | These are example placements of the fixture set; each fixture still does what it did. The counterbores leave a 12 mm floor so one screw length (M6 x 30) serves all plywood fixtures. |
| P10 | The instrument arm ran from the centre of the post, through the post, and the drop rod met the arm end with no clamp. | A printed arm clamp (64 x 50 x 40 mm) slides on the post with the 18 mm arm passing 25 mm beside it; a printed end clamp on the arm's end holds the 12 mm drop rod 6 mm in front of the arm's end. Two M5 x 20 screws hold the post to its foot from below. The post moves to the plywood directly behind the tile, and the arm reaches straight forward over the work. | Each part now passes beside the next instead of through it; the clamps lock with M6 thumb screws, as the BOM's "printed clamps" intended. |
| P11 | The V-block's V was wider than the block, so its top edges vanished and it stood 55 mm tall, not 60 mm. | V 50 mm wide at the top with a 5 mm flat each side, its bottom 35 mm above the base. | Keeps the stated 100 x 60 x 60 mm block and gives printable flats. |
| P12 | The optional wall anchor angles had one leg flat under the worktop overhang, pointing back, where it could not reach a wall. | Each angle's flat leg screws up under the rear apron and its other leg runs down the wall, flush with the worktop's back edge. | A bench pushed against a wall can then be fixed to it; the tie force is still only 35 N [C6]. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Bench 43.8 kg empty (was 41.9 kg), 69.5 kg with the ballast [B1], [B2]. The frame timber is lighter (the overlapping apron length is gone) and 2.6 kg of bolts, cross dowels, screws and brackets is added. | Parts added for construction. |
| Stability | Tipping force 117 N empty (was 112 N) and 186 N with the ballast (was 181 N) [C2], [C4]; sliding 215 N and 341 N on rubber pads [C5]. | Follows the mass. R12 is still met only with the ballast. |
| Stiffness | Unchanged: 0.37 mm under 500 N [D5]. The bays, aprons and rails are the same size and in the same places. | |
| Cost | BOM line 1 (frame) $43.50 to $57.00 [K2]; line 5 $27.80 to $28.20; line 10 $12.00 to $15.00; line 12 $12.00 to $14.00; new line 17, nine worktop brackets, $3.60. Core parts $268.40 [K3]. Value-engineering target: USD 250. Estimated cost of the constructable design: USD 268.40 (USD 18.40 over the target) [K4]. `budget_usd` is unchanged. | Parts added for construction; the budget is a value-engineering target (Amish, 2026-10-01). |
| Drawing | GBN-DWG-001 Rev P4; making sketches GBN-DWG-101 to 116 added. | Follows the model. |
| Documents | GBN-CAL-001 v0.3, GBN-PRC-001 v0.5, GBN-REQ-001 v0.5: mass, stability and cost updated; R10 is now reported against the value-engineering target. No other requirement changed status. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

None of the changes alters what the bench does, its pitch or its safety case, so none is held back. Amish's review of the whole record is the open item, listed in the design decisions register (GBN-DEC-001).

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan GBN-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: R10 is now reported as USD 18.40 over the value-engineering target rather than met; otherwise unchanged (R7 not met at the 122 screw-in positions, R3 and R4 at risk, R5 not verifiable at TRL 3, R1, R2 and R11 met by design, R6, R8, R9 and R12 met on paper).
- The appearance model `cad/src/product_model.py` and the photoreal renders (`media/render-*.png`, made on Amish's Mac) still show the concept fixture positions, post and arm, and have no brackets, bolts or T-nuts. They need updating on the Mac; they are not regenerated here.
- The open decisions of GBN-DDR-001 and GBN-DDR-002 (O1, O3, O4) are unchanged and are listed in the register.
