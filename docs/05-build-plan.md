---
doc_id: GBN-BLD-001
title: GridBench prototype build plan
project: GridBench
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (GBN-DDR-003)
---

# GridBench prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order; 20, the wall anchor, is optional.*

The prototype is one GridBench: a bolted softwood frame on four levelling feet, carrying an 18 mm plywood worktop drilled on a 25 mm grid, with a 300 x 300 mm aluminium precision tile set flush in it at the right, two concrete slabs on a lower shelf, and a set of printed fixtures and an instrument post that screw onto the grid. Figure 1 shows the 20 components in the order you make or fit them. Sixteen kinds of part are made in a garage workshop, each with its own making sketch: the legs, end and long aprons, low and cross rails, packers and shelf (sawing and drilling timber), the worktop (drilling and routing plywood), the tile (drilling, reaming and tapping aluminium plate), and the toe clamps, fence, V-block, stop pins, post foot and two arm clamps (3D printing in PETG). Everything else is bought and fitted: feet, bolts and cross dowels, tee nuts and inserts, brackets, pins, the extrusion and rods for the post and arm, the dial indicator and the slabs. The parts cost about USD 268 from the bill of materials, with the dial indicator supplied by the user.

> **Safety:** Drilling, tapping, routing and sawing make chips and can throw work: wear safety glasses, clamp the work, and keep hands clear of turning tools. The finished bench tips at about 117 N at its front edge when empty, so the two ballast slabs (about 13 kg each) go on the shelf before the bench is used; lift each with a straight back. The worktop is about 7 kg and awkward: lift it with a second person. Printed clamps can crack and release a part if overtightened: never tighten a clamp screw past 1.6 N·m. The bench is plywood and PETG: no welding, grinding sparks or hot work on it.

## 2. What changed to make it buildable

The concept showed what the bench does; some of its parts could not be made, fixed or assembled as drawn. Each change below keeps what the bench does, and all of them are recorded in decision record GBN-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Long aprons | Full-length aprons running through the legs, with no joint | Aprons 1,020 mm long, butted between the legs on two M8 bolts and cross dowels at each end (Figure 5) | Nothing overlaps, and the frame comes apart for moving |
| End aprons and low rails | No joint to the legs | The same bolt and cross dowel joint (Figures 5 and 8) | One joint for the whole frame |
| Cross rails | No fixing; the rail under the tile's right edge ran into the right-hand legs | Two screws through the apron into each end; that rail notched round the leg corners (Figure 10) | The rail keeps its place under the tile |
| Shelf | As long as the gap between the legs, so it could not go in | 10 mm shorter, 5 mm clear at each end (Figure 12) | It slides in and drops onto the rails |
| Worktop | No fixing to the frame; a square-cornered pocket the same size as the tile | Nine steel brackets underneath (Figure 16); pocket 0.5 mm larger all round with relief holes at the corners (Figure 13) | No screw blocks a grid hole; the tile drops in |
| Precision tile | Fixing holes with nothing to screw into | Four cap screws into threaded inserts in the two tile rails (Figure 18) | Uses the insert already in the bill of materials |
| Feet | Foot stems ending in solid wood | A T-nut in a 12 mm bore in each leg end (Figure 3) | The foot screws in and adjusts |
| Fixtures | Fence, V-block, post foot and clamp screws on unthreaded holes or between holes | Every fixture on threaded positions, with one screw length for the plywood (Figures 20 and 25) | Each one can be screwed down |
| Instrument arm | The arm passed through the post; no clamp at the drop rod | Two printed clamps; the arm passes beside the post and the drop rod beside the arm's end (Figure 28) | Nothing passes through anything else |
| Wall anchor (optional) | A flat leg pointing at no wall | One leg under the rear apron, the other down the wall (Figure 29) | It can be fixed to a wall |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing in front of the bench; "front" is where you stand. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Legs (make 4)

![Figure 2. Making sketch of the leg](../cad/drawings/GBN-DWG-101.png)

*Figure 2. Leg making sketch (GBN-DWG-101).*

**What it is and what it is made from.** The four corner posts that carry everything. Sawn softwood 70 x 70 mm, strength class C16 or better, straight and dry.

**How to make it.**

1. Cut four lengths of 857, square at both ends.
2. On each leg, pick the outside corner: the edge where its end face (the face toward the end of the bench) meets its side face (the face toward the front or back). Mark both faces.
3. End face: two 9 mm holes, 12.5 from the centre line toward the outside corner, 40 and 100 down from the top (for the long apron). Two 9 mm holes on the centre line, 100 and 130 up from the foot (for the low rail).
4. Side face: two 9 mm holes, 12.5 from the centre line toward the outside corner, 20 and 70 down from the top (for the end apron).
5. Drill all six right through, square to the face, in a drill stand or with a drilling guide.
6. Foot: bore 12 mm, 60 deep, on the centre of the bottom end. Tap an M10 T-nut into it until its flange is flat on the end.
7. Round or chamfer every outside edge about 2 mm.

**How it fits the parts next to it.**

![Figure 3. Joint 4: levelling foot in the leg end](05-build-plan/joint-04.png)

*Figure 3. The T-nut flange bears on the leg end; the foot screws through the T-nut into the bore.*

The aprons and low rails butt against the leg's inside faces, flush with its top and outside faces, and are bolted through it (Figure 5). The levelling foot screws into the T-nut; set it with 13 mm of thread showing, which leaves 15 mm of adjustment up or down.

**Check before moving on.** A 9 mm rod passes through each hole square; the leg stands upright on its foot.

### 3.2 End aprons (make 2)

![Figure 4. Making sketch of the end apron](../cad/drawings/GBN-DWG-102.png)

*Figure 4. End apron making sketch (GBN-DWG-102).*

**What it is and what it is made from.** The deep rail across each end of the bench, under the worktop. Sawn softwood 45 x 120 mm, C16 or better.

**How to make it.**

1. Cut two lengths of 420, ends square.
2. In each end: two 9 mm holes along the length, 52 deep, centred in the 45 mm thickness, 50 and 100 up from the lower edge. A drilling guide or a drill stand on its side keeps them straight.
3. In the inside face: two 10 mm holes, 30 deep, 40 in from each end, at the same heights. Each meets an end hole; an M8 cross dowel goes in here, and the bolt from the leg screws into it.

**How it fits the parts next to it.**

![Figure 5. Joint 1: aprons to a leg](05-build-plan/joint-01.png)

*Figure 5. Cut level with a long apron bolt, seen from above: each bolt passes through the leg into a cross dowel in the apron.*

Each end apron butts between two legs, flush with their tops and outside faces. Two M8 x 120 hex bolts with washers go through the leg's side face into the cross dowels. The end apron bolts sit at different heights from the long apron bolts, so the two pairs miss each other inside the leg.

**Check before moving on.** An M8 bolt pushed into an end hole shows through the cross dowel hole; the ends are square to the faces.

### 3.3 Long aprons (make 2)

![Figure 6. Making sketch of the long apron](../cad/drawings/GBN-DWG-103.png)

*Figure 6. Long apron making sketch (GBN-DWG-103), drawn standing on end.*

**What it is and what it is made from.** The deep rails along the front and back, which carry most of the worktop. Sawn softwood 45 x 120 mm, C16 or better.

**How to make it.**

1. Cut two lengths of 1,020, ends square. The two must match within 0.5.
2. In each end: two 9 mm holes along the length, 52 deep, centred in the thickness, 20 and 80 up from the lower edge.
3. In the inside face: two 10 mm cross dowel holes, 30 deep, 40 in from each end, at the same heights.
4. Cross rail screw holes: 4 mm pilot holes right through, 63 and 106 up from the lower edge, at 210, 510, 757.5 and 1,005 from the left end.

**How it fits the parts next to it.** It butts between the legs like the end apron (Figure 5), on two bolts and cross dowels at each end. The cross rails butt against its inside face (Figure 10), and the worktop brackets screw to its inside face (Figure 16).

**Check before moving on.** Both aprons the same length within 0.5; the pilot holes line up when the two are laid side by side.

### 3.4 Low rails (make 2)

![Figure 7. Making sketch of the low rail](../cad/drawings/GBN-DWG-104.png)

*Figure 7. Low rail making sketch (GBN-DWG-104), drawn standing on end.*

**What it is and what it is made from.** The front and back rails near the floor that carry the shelf and the ballast. Sawn softwood 45 x 70 mm, C16 or better.

**How to make it.**

1. Cut two lengths of 1,020, ends square.
2. In each end: two 9 mm holes along the length, 52 deep, centred in the thickness, 20 and 50 up from the lower edge.
3. In the inside face: two 10 mm cross dowel holes, 30 deep, 40 in from each end, at the same heights.

**How it fits the parts next to it.**

![Figure 8. Joint 2: low rail to a leg](05-build-plan/joint-02.png)

*Figure 8. Cut level with the upper bolt: the same bolt and cross dowel joint as the aprons, on the leg's centre line.*

The rail butts between the legs on their centre line, its lower edge 105 above the floor (80 above the foot of the leg). The shelf rests on its top face.

**Check before moving on.** Same length as the long aprons within 0.5.

### 3.5 Cross rails (make 4; one notched)

![Figure 9. Making sketch of the cross rail](../cad/drawings/GBN-DWG-105.png)

*Figure 9. Cross rail making sketch (GBN-DWG-105), drawn for the notched rail.*

**What it is and what it is made from.** Four rails from front to back under the worktop. They split it into bays no wider than 255, and the two on the right carry the precision tile. Sawn softwood 45 x 70 mm, C16 or better.

**How to make it.**

1. Cut four lengths of 470, ends square.
2. Take the rail that will sit nearest the right-hand legs. At each end, on the side toward the legs, saw out a notch 15 wide (along the bench) and 25 long, full height, so the rail clears the leg corners.
3. Ends of all four: two 4 mm pilot holes, 40 deep, 13 and 56 up from the lower edge (in the unnotched 30 mm of the notched rail).

**How it fits the parts next to it.**

![Figure 10. Joint 3: the notched cross rail beside the right legs](05-build-plan/joint-03.png)

*Figure 10. Cut level with the upper screw: the notch clears the leg corner, and screws through the apron hold the rail.*

The rails butt between the long aprons with their tops flush, centred 210, 510, 757.5 and 1,012.5 from the inside face of the left legs. Two 6 x 100 structural screws go through the apron into each rail end. The two right-hand rails are the tile rails; their insert holes are drilled in step 10.

**Check before moving on.** Each rail drops between the aprons without forcing and its top is flush with theirs.

### 3.6 Packers under the tile (make 2)

![Figure 11. Making sketch of the packer](../cad/drawings/GBN-DWG-106.png)

*Figure 11. Packer making sketch (GBN-DWG-106).*

**What it is and what it is made from.** Two thin hardwood strips on the tile rails that bring the tile up flush with the plywood. Hardwood strip 45 wide, about 6 thick, planed.

**How to make it.**

1. Measure the tile's thickness and the worktop's thickness. The packer thickness is the worktop's less the tile's: 5.3 for a 12.7 tile in 18 plywood.
2. Cut two lengths of 300 and plane both to that thickness, within 0.05.

**How it fits the parts next to it.** Each packer is glued centred on the top of a tile rail, running front to back under the tile pocket. The tile rests on both packers (Figure 18).

**Check before moving on.** Both packers the same thickness within 0.05.

### 3.7 Shelf

![Figure 12. Making sketch of the shelf](../cad/drawings/GBN-DWG-107.png)

*Figure 12. Shelf making sketch (GBN-DWG-107).*

**What it is and what it is made from.** The lower shelf that carries the ballast. Plywood 12 mm.

**How to make it.** Cut 1,010 x 535, square; round the corners about 5 and sand the edges.

**How it fits the parts next to it.** It rests on the top faces of the two low rails, flush with their outside faces, 5 clear of the legs at each end. It goes in from the front, above the front low rail, and is lowered onto both rails (step 7).

**Check before moving on.** It lies flat on both rails and touches no leg.

### 3.8 Worktop

![Figure 13. Making sketch of the worktop](../cad/drawings/GBN-DWG-108.png)

*Figure 13. Worktop making sketch (GBN-DWG-108); the holes are on the hole layout, Figure 14.*

![Figure 14. Every hole in the worktop](05-build-plan/worktop-holes.png)

*Figure 14. Every hole, seen from above with the front edge at the bottom: plain holes, tee nut holes and screw-in insert holes.*

**What it is and what it is made from.** The working surface: a plywood panel drilled on the 25 mm grid, with a pocket for the precision tile. Birch plywood 18 mm, one 1,200 x 600 panel.

**How to make it.**

1. Cut the panel to 1,200 x 600, square within 0.5 (measure both diagonals).
2. Mark the front edge and the left edge: every hole is measured from these two.
3. Hole centres are 12.5 from the left and front edges, then every 25 both ways: 48 along and 24 back. Every second hole in both directions (the 50 mm sub-grid) is threaded; the rest are plain.
4. Drill as Figure 14: 756 plain holes of 6.6, 130 holes of 8.0 for tee nuts, and 122 holes of 8.5 for screw-in inserts (the threaded positions that will sit over a frame member). Use a shared CNC router if you can. Otherwise use a printed drilling template indexed from the left and front edges each time, never from the last hole drilled, so errors do not add up.
5. Tile pocket: 301 x 301, right through, from 824.5 to 1,125.5 from the left edge and 149.5 to 450.5 from the front edge. Drill an 8 mm relief hole centred on each corner first, then cut inside the line with a jigsaw and rout to the line against a straightedge.
6. Round every edge 1 mm and seal both faces with a thin finish so the panel takes up moisture evenly.

**How it fits the parts next to it.**

![Figure 15. Joint 6: threaded positions in the worktop](05-build-plan/joint-06.png)

*Figure 15. Cut along a row of holes: a tee nut pressed in from below, and a screw-in insert from the top where a cross rail is underneath.*

The tee nuts and inserts go in before the worktop goes on the frame (step 8). The worktop sits on the aprons and rails with 20 overhang all round and is held by nine brackets from below:

![Figure 16. Joint 5: worktop bracket on the front apron](05-build-plan/joint-05.png)

*Figure 16. Each bracket is screwed to the apron's inside face and up into the worktop, midway between two threaded positions.*

**Check before moving on.** Diagonals equal within 1; a 6 mm pin drops into any plain hole; the pocket is 301 within 0.3 both ways.

### 3.9 Precision tile

![Figure 17. Making sketch of the precision tile](../cad/drawings/GBN-DWG-109.png)

*Figure 17. Precision tile making sketch (GBN-DWG-109).*

**What it is and what it is made from.** The flush aluminium plate for work that must repeat to a few hundredths of a millimetre. Cast aluminium tooling plate 300 x 300 x 12.7, bought as an offcut.

**How to make it.**

1. Check the plate is square and flat (a straightedge and 0.05 feeler gauge). Chamfer the top edges 0.5. Mark the top face and the front edge.
2. Measure from the left and front edges. 144 M6 holes on the 25 mm grid, first centres 12.5 in: drill 5.0 right through using a drilling jig on a drill press, then tap M6 with a spiral-point tap held square in a tapping guide, with cutting fluid.
3. Nine dowel bores at 50, 150 and 250 both ways (the centres of grid squares): drill 7.8, then ream 8 mm H7 right through.
4. Four fixing holes of 7.0, 22.5 in from the left and right edges and 25 in from the front and back edges; counterbore each 11 across and 6.5 deep from the top.
5. Deburr every hole and stone the top face flat.

**How it fits the parts next to it.**

![Figure 18. Joint 7: tile fixing screw](05-build-plan/joint-07.png)

*Figure 18. Cut through a fixing screw: the tile sits flush on the packer, 0.5 clear of the pocket, held by a cap screw into an insert in the rail.*

The tile drops into the pocket and rests on the two packers, flush with the plywood. Four M6 x 20 cap screws go through the counterbored holes into screw-in inserts in the tile rails. Its holes continue the plywood grid to within the 0.5 pocket clearance. A screw in the tile must reach no more than 12 below its top face: the holes over the two packers are blind below that.

**Check before moving on.** An 8 mm h6 pin slides into every bore by hand; an M6 screw runs into every tapped hole by hand.

### 3.10 Toe clamps (make 4)

![Figure 19. Making sketch of the toe clamp](../cad/drawings/GBN-DWG-110.png)

*Figure 19. Toe clamp making sketch (GBN-DWG-110).*

**What it is and what it is made from.** A printed clamp that presses work down onto the tile or the worktop. PETG, printed with 6 walls and 40 % infill.

**How to make it.**

1. Print four lying on a side face, so the layers run along the clamp; about 50 g each.
2. The body is 70 long, 24 wide and 30 deep, with a slot 6.6 wide and 31.5 long whose centre is 7 from the middle toward the toe end. The heel at the other end is 14 long and as tall as the work it is for (40 here; print other heights as needed).
3. Mark "1.6 N·m MAX" on the top.

**How it fits the parts next to it.**

![Figure 20. Joint 8: work held on the tile](05-build-plan/joint-08.png)

*Figure 20. Each clamp's screw goes into a threaded tile hole; the toe presses the work and the heel stands on the tile.*

An M6 x 80 cap screw with a printed knob passes through the slot into a threaded hole. Slide the body so the screw is nearer the toe than the heel. Tighten to 1.6 N·m at most.

**Check before moving on.** No cracks or gaps between layers at the slot ends.

### 3.11 Fence segments (make 2)

![Figure 21. Making sketch of the fence segment](../cad/drawings/GBN-DWG-111.png)

*Figure 21. Fence segment making sketch (GBN-DWG-111).*

**What it is and what it is made from.** A straight edge to push work against. PETG, printed.

**How to make it.**

1. Print two lying on a 190 x 50 face: 190 long, 25 wide, 50 tall. They fit a 200 x 200 bed.
2. Two 6.6 holes top to bottom, 50 each side of the centre (100 apart), counterbored 11 from the top down to 12 above the base.

**How it fits the parts next to it.** Each segment stands on two threaded positions, 100 apart, held by two M6 x 30 cap screws. The two stand end to end with a 10 gap. On the plywood, every fixture screw reaches 15 to 18 below the surface, so it engages a tee nut or an insert fully: a 12 floor and an M6 x 30 screw does this.

**Check before moving on.** The front face is square to the base.

### 3.12 V-block

![Figure 22. Making sketch of the V-block](../cad/drawings/GBN-DWG-112.png)

*Figure 22. V-block making sketch (GBN-DWG-112).*

**What it is and what it is made from.** A block that holds round bar. PETG, printed.

**How to make it.**

1. Print standing on one 60 x 60 end, so the V needs no support: 100 long, 60 wide, 60 tall.
2. The 90° V runs the full length, 50 wide at the top with a 5 flat each side, its bottom 35 above the base. It holds bar from about 8 to 45 across.
3. Two 6.6 holes from the V bottom to the base, 25 each side of the centre, counterbored 11 down to 12 above the base.

**How it fits the parts next to it.** Two M6 x 30 cap screws into threaded positions 50 apart.

**Check before moving on.** A 20 mm bar rests on both faces of the V.

### 3.13 Stop pins (make 6)

![Figure 23. Making sketch of the stop pin](../cad/drawings/GBN-DWG-113.png)

*Figure 23. Stop pin making sketch (GBN-DWG-113).*

**What it is and what it is made from.** A peg that drops into any plain hole as a stop. PETG, printed.

**How to make it.** Print six standing upright: a head 12 across and 24 tall, with a spigot 6.3 across and 12 long below it. For heavy use, print a 5.8 hole through the head and press in a 6 mm steel dowel instead of the printed spigot.

**How it fits the parts next to it.** The spigot drops into any 6.6 plain hole; the head is the stop.

**Check before moving on.** The spigot drops in by hand and rocks no more than about 0.3 at the top.

### 3.14 Instrument post foot

![Figure 24. Making sketch of the post foot](../cad/drawings/GBN-DWG-114.png)

*Figure 24. Post foot making sketch (GBN-DWG-114).*

**What it is and what it is made from.** The printed base that holds the instrument post upright on the grid. PETG at 100 % infill.

**How to make it.**

1. Print flat: 74 x 74 x 12.
2. Two 6.6 holes at opposite corners, 25 from the centre both ways, for the M6 x 30 screws.
3. Two 5.5 holes on the centre line, 10 each side of the centre, counterbored 9 across and 5 deep from the underside, for the M5 x 20 screws into the extrusion.
4. Cut the 20 x 40 aluminium extrusion to 350 and tap M5 into its two core holes at one end, 12 deep.

**How it fits the parts next to it.**

![Figure 25. Joint 9: post foot on the worktop](05-build-plan/joint-09.png)

*Figure 25. Cut through the post's two M5 screws, which hold it from below; two M6 screws hold the foot to the grid.*

The extrusion stands on the foot's top face with its 40 side running front to back. The foot screws down onto any two threaded positions diagonally 50 apart; the prototype puts it on the plywood directly behind the tile.

**Check before moving on.** The extrusion stands square to the foot.

### 3.15 Arm clamp and end clamp

![Figure 26. Making sketch of the arm clamp](../cad/drawings/GBN-DWG-115.png)

*Figure 26. Arm clamp making sketch (GBN-DWG-115).*

![Figure 27. Making sketch of the end clamp](../cad/drawings/GBN-DWG-116.png)

*Figure 27. End clamp making sketch (GBN-DWG-116).*

**What they are and what they are made from.** Two printed clamps that hold the arm on the post and the dial indicator's drop rod on the arm. PETG at 100 % infill.

**How to make them.**

1. Arm clamp: 64 wide, 50 deep, 40 tall. A slot 20.4 x 40.4 top to bottom for the post, its centre 13 right of the block's centre. A bore of 18.4 front to back for the arm, 25 left of the post's centre and half way up, so the arm passes beside the post.
2. End clamp: 30 wide, 50 deep, 30 tall. A blind bore of 18.4 from the back face, 27 deep, for the arm's end. A bore of 12.4 top to bottom for the drop rod, its centre 14 in front of the block's centre.
3. In each clamp, print a hex pocket for an M6 nut and a 6.6 hole into each bore or slot, for an M6 thumb screw.
4. Cut the 18 mm steel arm to 225 and the 12 mm steel drop rod to 200; deburr the ends.

**How they fit the parts next to them.**

![Figure 28. Joint 10: arm, clamps and drop rod](05-build-plan/joint-10.png)

*Figure 28. The arm passes beside the post through the arm clamp; the drop rod passes 6 in front of the arm's end through the end clamp.*

The arm clamp slides on the post and locks at any height; the arm slides through it and locks. The end clamp sits on the arm's end; the drop rod slides up and down in it and carries the dial indicator by its lug back.

**Check before moving on.** Each clamp slides freely when loose and does not move when locked; the drop rod hangs upright when the arm is level.

### 3.16 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Levelling feet (line 2).** Four M10 levelling feet with a 50 steel pad and 3 mm rubber base, and four M10 T-nuts for a 12 mm bore.
- **Frame fixings (line 1).** 24 M8 x 120 hex bolts with washers; 24 M8 cross dowels (barrel nuts) about 10 across and 20 to 30 long; 16 structural wood screws 6 x 100; wood glue for the packers.
- **Tee nuts and inserts (line 5).** 130 flanged M6 tee nuts with a 19 flange and 9.5 barrel for an 8.0 hole; 126 screw-in M6 inserts for wood, 10 outside, 13 long, for an 8.5 hole (122 in the worktop and 4 in the tile rails).
- **Worktop brackets (line 17).** Nine steel angle brackets 30 x 30 x 3, 20 wide, each with a 4 x 25 screw into the apron and a 4 x 16 screw up into the worktop.
- **Pins (lines 7 and 13).** Round 8 mm h6 hardened dowel pins 20 long, and diamond (relieved) 8 mm h6 locating pins 20 long. A precision fixture always uses one of each.
- **Post, arm and rod (line 10).** One 20 x 40 aluminium extrusion 350 long, one 18 mm steel bar 225 long, one 12 mm steel bar 200 long, four M6 thumb screws and nuts.
- **Dial indicator (line 11, user-supplied).** 0.01 resolution, 10 travel, 8 mm stem, lug back.
- **Fastener kit (line 12).** M6 cap screws: 10 x 30 (fixtures on the plywood), 4 x 80 (toe clamps, with printed knobs), 4 x 20 (tile), 10 x 16 (fixtures on the tile); 2 M5 x 20; washers; a 5 mm hex key.
- **Ballast slabs (line 14).** Two concrete paving slabs 400 x 400 x 35, about 13 kg each.
- **Wall anchor angles (line 15, optional).** Two steel angles 50 x 50 x 4, 40 wide, with screws and wall plugs:

![Figure 29. Joint 11: wall anchor angle](05-build-plan/joint-11.png)

*Figure 29. One leg screws up into the rear apron; the other runs down the wall, flush with the worktop's back edge.*

- **Tile tools (line 16).** Two M6 spiral-point taps, 5.0 and 7.8 drills, an 8 mm H7 reamer and a tapping guide.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: T-nuts and feet into the legs

![Step 1](05-build-plan/step-01.png)

Tap each T-nut into the 12 mm bore in the foot of a leg until its flange is flat. Screw a levelling foot into each until 13 of thread shows.

### Step 2: end aprons between the legs

![Step 2](05-build-plan/step-02.png)

Lay two legs on the bench with their side faces up and an end apron between them, tops and outside faces flush. Push the cross dowels into the apron, slot toward the bolt, and fit two bolts with washers through each leg. Snug only. Make both end frames.

### Step 3: long aprons join the two end frames

![Step 3](05-build-plan/step-03.png)

With a helper holding the end frames upright, bolt the long aprons between them the same way. Measure both diagonals across the top of the frame; when they are equal within 2, tighten every bolt firmly.

### Step 4: low rails between the legs

![Step 4](05-build-plan/step-04.png)

Bolt the low rails between the legs, their lower edges 105 above the floor. Tighten every frame bolt firmly.

### Step 5: cross rails between the long aprons

![Step 5](05-build-plan/step-05.png)

Fit each rail with its top flush with the aprons, the notched one beside the right-hand legs, and drive two 6 x 100 screws through the apron's pilot holes into each end.

### Step 6: packers onto the two tile rails

![Step 6](05-build-plan/step-06.png)

Glue each packer centred on the top of a tile rail, running front to back, and clamp it until the glue sets. Wipe off any glue that squeezes out.

### Step 7: shelf onto the low rails

![Step 7](05-build-plan/step-07.png)

Slide the shelf in from the front, above the front low rail, and lower it onto both rails.

### Step 8: threaded inserts into the worktop

![Step 8](05-build-plan/step-08.png)

With the worktop upside down on a clean bench, press each tee nut into its 8.0 hole from the underside with a vice or a bolt and washer, until the flange is flat; do not hammer the prongs into the ply. Turn it over and drive each screw-in insert flush into its 8.5 hole from the top with a hex key, square to the face. **Hold point:** an M6 screw runs into every threaded position by hand.

### Step 9: worktop onto the frame

![Step 9](05-build-plan/step-09.png)

With a helper, lay the worktop on the frame with 20 overhang all round and its tile pocket over the two tile rails. Screw the nine brackets to the aprons and up into the worktop, each midway between two threaded positions.

### Step 10: precision tile into its pocket

![Step 10](05-build-plan/step-10.png)

Through the pocket, mark the four fixing hole centres on the packers, drill 8.5 and 15 deep through each packer into the rail, and drive a screw-in insert flush with the packer's top. Lower the tile in, top face up and marked edge to the front, and fit four M6 x 20 cap screws, tightening them evenly. **Hold point:** a straightedge across the tile and the plywood shows no step over 0.1.

### Step 11: ballast slabs onto the shelf

![Step 11](05-build-plan/step-11.png)

Lift each slab onto the shelf with a straight back and set them side by side, centred, 40 apart. **Hold point:** safety stop S4.

### Step 12: fence, stop pins and V-block

![Step 12](05-build-plan/step-12.png)

Screw each fence segment and the V-block down with two M6 x 30 cap screws into threaded positions; drop the stop pins into plain holes where they are needed.

### Step 13: pins, work and toe clamps on the tile

![Step 13](05-build-plan/step-13.png)

Put a round pin in one dowel bore and a diamond pin in another. Set the work against them, then fit each toe clamp on an M6 x 80 screw into a tile hole and tighten to 1.6 N·m at most.

### Step 14: instrument post, arm and dial indicator

![Step 14](05-build-plan/step-14.png)

Screw the post foot down with two M6 x 30 screws. Slide the arm clamp onto the post and the arm through it, fit the end clamp on the arm's end, hang the indicator from the drop rod by its lug back, and lower the drop rod until the indicator's point rests on the work with about 1 of travel used. Lock every thumb screw.

### Step 15: wall anchor angles (optional)

![Step 15](05-build-plan/step-15.png)

Push the bench against the wall. Screw each angle up into the rear apron and, through wall plugs, into the wall.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of GBN-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Grid fits a commercial accessory | R1 | Screw a metric optical breadboard post into threaded positions on the plywood and the tile | It seats square in every position tried |
| Height and level | R2 | Tape measure at each corner; spirit level both ways; adjust the feet | Top at 900, give or take 15; level |
| Hole position on the plywood | R3 | Steel rule and pin gauges between holes 1,000 apart, at two humidities | Within 0.3 (CNC-drilled) or 0.5 (template-drilled) |
| Tile hole position and relocation | R4 | Dial indicator on a part located by one round and one diamond pin, relocated 10 times | Returns within 0.03 |
| Flatness | R5 | Straightedge and feeler gauges | Tile within 0.05 over 300; worktop within 0.5 over 1,000 |
| Stiffness | R6 | 500 N (about 51 kg) at the middle of a bay; dial indicator under the worktop | Deflection 0.5 or less |
| Clamp hold-down | R7 | Spring scale pull on a clamped part at 1.6 N·m, at a tee nut position and on the tile; again after 8 h | Holds 500 N with no visible creep |
| Fixture change | R8 | Swap the V-block for a fence segment with one 5 mm hex key, timed | 60 s or less |
| Buildability | R9 | Review of this build | Hand and garage tools and a 200 x 200 printer were enough |
| Stability | R12 | Push gauge at the front top edge, with the ballast in place; feel every edge | No tipping at 150 N; every exposed edge rounded or chamfered 0.5 or more |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any cutting or drilling.** Safety glasses on; the work clamped, never hand held; long hair and sleeves tied back; no gloves near a turning drill or router.
- **S2. Before drilling and tapping the tile.** The tile clamped in a drill press vice or to the table; cutting fluid ready; the tap held square in its guide. Clear aluminium chips with a brush, not fingers.
- **S3. Before standing the frame up.** Every frame bolt tight; a helper to steady it. Lift the worktop with two people.
- **S4. Before any use of the bench.** Both ballast slabs on the shelf, or the wall anchor fitted. The bench does not rock on its feet.
- **S5. Before clamping.** Every toe clamp marked 1.6 N·m and a torque screwdriver to hand. Full clamping force only at tee nut positions and on the tile; the screw-in positions over the frame can pull out first.
- **S6. Always.** No welding, grinding sparks or hot work on the bench.

## 7. Tools, skills and workspace

**Tools.** Mitre or circular saw and a handsaw; jigsaw; router with a straight bit and a straightedge guide; drill press or a drill in a stand; drills 4, 5.0, 5.5, 6.6, 7.0, 7.8, 8.0, 8.5, 9, 10 and 12; 11 mm counterbore; 8 mm H7 reamer; M5 and M6 taps and a tapping guide; hand plane; shared CNC router or a printed drilling template; FDM printer with a bed of at least 200 x 200 that prints PETG; 13 mm spanner and socket; 5 mm hex key; torque screwdriver covering 0.5 to 2 N·m; tape measure, steel rule, engineer's square, straightedge and feeler gauges; spirit level; clamps.

**Skills.** No certified trade is needed. Basic woodwork (measuring, sawing square, drilling straight), routing to a line, drilling and tapping aluminium, and 3D printing. Nothing is powered: the bench has no electrical parts.

**Workspace.** A floor space about 2.5 x 2 m to build the frame; a bench for drilling; a ventilated place for the printer.

**Personal protective equipment.** Safety glasses for every cutting, drilling, routing and tapping step; hearing protection for sawing and routing; a dust mask when routing plywood; safety boots when moving the slabs.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/GBN-DWG-101` to `GBN-DWG-116`.
- General arrangement: `cad/drawings/GBN-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (GBN-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; mass [B1], tipping [C2], [C4], stiffness [D5], clamps and inserts [G4], [G5c], fixture change [H1], cost [K3].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (GBN-DDR-003), with GBN-DDR-001 and GBN-DDR-002; open items in `docs/06-design-decisions.md` (GBN-DEC-001).
- Requirements: `docs/03-requirements.md` (GBN-REQ-001 v0.5).
