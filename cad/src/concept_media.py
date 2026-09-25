"""GridBench concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X along the bench (1,200 mm), Y front to back (600 mm, front at -Y),
Z up, floor at Z = 0, worktop surface at Z = 900. The grid origin is the front-left corner
of the worktop; hole centers sit at 12.5 + 25 k mm from each edge, so the plywood field and
the aluminum precision tile share one continuous 25 mm grid.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Compound, RegularPolygon, extrude, Solid, Plane, Vector
from concept import Part, render_all

L, D = 1200.0, 600.0          # worktop length (X) and depth (Y)
H = 900.0                     # working height (top surface)
T_TOP = 18.0                  # plywood worktop thickness
PITCH = 25.0
TILE = 300.0                  # precision tile side
T_TILE = 12.7
TILE_X0 = 225.0               # tile spans X 225 to 525, Y -150 to 150 (on grid)
Z_UNDER = H - T_TOP           # underside of worktop

WOOD = "#C8A06A"
PLY = "#E2C48E"
ALU = "#B8C2CC"
STEEL = "#6B7280"
PRINT = "#0F766E"
PRINT2 = "#14B8A6"
BRASS = "#C9A227"


def grid(n, start):
    return [start + PITCH * i for i in range(n)]


XS = grid(int(L / PITCH), -L / 2 + PITCH / 2)       # 48 columns
YS = grid(int(D / PITCH), -D / 2 + PITCH / 2)       # 24 rows


def disk(r, h):
    """Octagonal disk: light to mesh, reads as a round hole at render scale."""
    return extrude(RegularPolygon(r, 8), amount=h)


def in_tile(x, y):
    return TILE_X0 < x < TILE_X0 + TILE and -TILE / 2 < y < TILE / 2


def on_insert(x, y):
    """M6 inserts on the 50 mm sub-grid of the plywood field."""
    i = round((x - XS[0]) / PITCH); j = round((y - YS[0]) / PITCH)
    return i % 2 == 0 and j % 2 == 0


# ---------------- 4 Plywood worktop (coarse field) ----------------
# Holes are drawn as thin dark disks on the surface: a massing model, and far lighter to mesh
# than 1,150 boolean cuts.
top = Pos(0, 0, H - T_TOP / 2) * Box(L, D, T_TOP)
top = top - Pos(TILE_X0 + TILE / 2, 0, H - T_TOP / 2) * Box(TILE, TILE, T_TOP + 2)
HOLE = "#3F3A33"
ply_holes = Compound(children=[Pos(x, y, H) * disk(3.3, 0.6)
                               for x in XS for y in YS if not in_tile(x, y) and not on_insert(x, y)])

# ---------------- 5 M6 threaded inserts (brass, flush, dark bore) ----------------
ins_xy = [(x, y) for x in XS for y in YS if on_insert(x, y) and not in_tile(x, y)]
inserts = Compound(children=[Pos(x, y, H) * disk(4.5, 0.6) for x, y in ins_xy])
ins_bores = Compound(children=[Pos(x, y, H + 0.6) * disk(2.6, 0.4) for x, y in ins_xy])

# ---------------- 6 Precision tile, 144 M6 holes plus 9 dowel bores ----------------
tcx = TILE_X0 + TILE / 2
tile = Pos(tcx, 0, H - T_TILE / 2) * Box(TILE, TILE, T_TILE)
dowel_xy = [(TILE_X0 + dx, dy) for dx in (50, 150, 250) for dy in (-100, 0, 100)]
tile_holes = Compound(children=[Pos(x, y, H) * disk(2.5, 0.6) for x in XS for y in YS if in_tile(x, y)]
                      + [Pos(x, y, H) * disk(4.0, 0.6) for x, y in dowel_xy])

# ---------------- 1 Bench frame (bolted timber) ----------------
LEG = 70.0
lx, ly = L / 2 - 20 - LEG / 2, D / 2 - 20 - LEG / 2
legs = [Pos(sx * lx, sy * ly, 25 + (Z_UNDER - 25) / 2) * Box(LEG, LEG, Z_UNDER - 25)
        for sx in (-1, 1) for sy in (-1, 1)]
aprons = [Pos(0, sy * (ly + LEG / 2 - 22.5), Z_UNDER - 47.5) * Box(L - 40, 45, 95) for sy in (-1, 1)]
aprons += [Pos(sx * (lx + LEG / 2 - 22.5), 0, Z_UNDER - 47.5) * Box(45, D - 40 - 90, 95) for sx in (-1, 1)]
cross = [Pos(x, 0, Z_UNDER - 35) * Box(45, D - 40 - 90, 70) for x in (-300.0, 0.0, 247.5, 502.5)]
low_rails = [Pos(0, sy * ly, 140) * Box(L - 40 - 2 * LEG, 45, 70) for sy in (-1, 1)]
frame = Compound(children=legs + aprons + cross + low_rails)

# ---------------- 2 Levelling feet ----------------
feet = Compound(children=[Pos(sx * lx, sy * ly, 0) * (Pos(0, 0, 6) * Cylinder(25, 12) + Pos(0, 0, 18) * Cylinder(5, 14))
                          for sx in (-1, 1) for sy in (-1, 1)])

# ---------------- 3 Lower shelf ----------------
shelf = Pos(0, 0, 175 + 6) * Box(L - 40 - 2 * LEG, 2 * ly - 45, 12)

# ---------------- 7 Dowel pins, two in use on the tile ----------------
Z0 = H
pins = Compound(children=[Pos(x, y, Z0 + 4) * Cylinder(4.0, 20) for x, y in ((TILE_X0 + 50, -100), (TILE_X0 + 150, -100))])

# ---------------- workpiece (context, not in BOM) located on the pins ----------------
work = Pos(TILE_X0 + 100, -40, Z0 + 20) * Box(160, 100, 40)

# ---------------- 8 Printed toe clamps (two shown on the tile) ----------------
def toe_clamp(x, y, ang):
    body = Rot(0, 0, ang) * (Pos(0, 0, 22) * Box(70, 24, 16) + Pos(28, 0, 11) * Box(14, 24, 22))
    screw = Pos(0, 0, 30) * Cylinder(3, 40) + Pos(0, 0, 36) * Cylinder(9, 12)
    return Pos(x, y, Z0) * (body + screw)


clamps = Compound(children=[toe_clamp(TILE_X0 + 100 - 5, 55, 90 + 180),
                            toe_clamp(TILE_X0 + 225, -40, 0)])

# ---------------- 9 Printed fence, stops and V-block on the plywood field ----------------
fence = Pos(-300, 187.5, Z0 + 25) * Box(400, 25, 50)
stops = [Pos(x, -12.5, Z0 + 12) * Cylinder(6, 24) for x in (-462.5, -137.5)]
vblock = Pos(-300, -150, Z0 + 30) * (Box(100, 60, 60) - Pos(0, 0, 30) * Rot(45, 0, 0) * Box(104, 50, 50))
fixtures = Compound(children=[fence, vblock] + stops)
tube_part = Pos(-300, -150, Z0 + 60) * Rot(0, 90, 0) * Cylinder(20, 260)

# ---------------- 10 Instrument post and arm (rear right) ----------------
def rod(p1, p2, r):
    """Round bar between two 3D points."""
    a, b = Vector(*p1), Vector(*p2)
    return Solid.make_cylinder(r, (b - a).length, Plane(origin=a, z_dir=(b - a).normalized()))


PX, PY = 537.5, 237.5            # post base on a grid hole, rear right corner of the tile
IX, IY = TILE_X0 + 150, -40      # indicator over the middle of the workpiece
ARM_Z = Z0 + 300
post = (Pos(PX, PY, Z0 + 6) * Box(80, 60, 12)
        + Pos(PX, PY, Z0 + 12 + 175) * Box(20, 40, 350)
        + rod((PX, PY, ARM_Z), (IX, IY + 25, ARM_Z), 9)
        + Pos(PX, PY, ARM_Z) * Box(36, 50, 40))
# ---------------- 11 Dial indicator over the workpiece ----------------
indicator = (Pos(IX, IY, Z0 + 135) * Rot(90, 0, 0) * Cylinder(28, 18)        # dial, facing the front
             + rod((IX, IY, Z0 + 40), (IX, IY, Z0 + 107), 3)                 # stem and contact point
             + rod((IX, IY + 9, Z0 + 135), (IX, IY + 25, Z0 + 135), 5)       # back lug
             + rod((IX, IY + 25, Z0 + 135), (IX, IY + 25, ARM_Z), 6))        # drop rod to the arm

parts = [
    Part("Bench frame, bolted timber", frame, WOOD, 1, (0, 0, -420)),
    Part("Levelling feet, M10 (4)", feet, STEEL, 2, (0, 0, -620)),
    Part("Lower shelf", shelf, PLY, 3, (0, -700, -300)),
    Part("Plywood grid worktop (coarse field)", top, PLY, 4, (0, 0, 0)),
    Part("Pin holes, 6.6 mm", ply_holes, HOLE, None, (0, 0, 0)),
    Part("M6 threaded inserts, 50 mm sub-grid", inserts, BRASS, 5, (0, 0, 0)),
    Part("Insert bores", ins_bores, HOLE, None, (0, 0, 0)),
    Part("Precision grid tile, aluminum", tile, ALU, 6, (0, 0, 200)),
    Part("Tile holes", tile_holes, "#374151", None, (0, 0, 200)),
    Part("Dowel pins, 8 mm h6", pins, "#374151", 7, (0, 0, 330)),
    Part("Printed toe clamps", clamps, PRINT, 8, (0, 0, 530)),
    Part("Printed fence, stops and V-block", fixtures, PRINT2, 9, (0, 0, 320)),
    Part("Instrument post and arm", post, "#475569", 10, (250, 300, 150)),
    Part("Dial indicator, 0.01 mm", indicator, "#1D4ED8", 11, (0, 0, 680)),
    Part("Workpiece (example, not in BOM)", work + tube_part, "#9CA3AF", None, (0, 0, 430)),
]

# Blueprint views: leave the ~1,300 hole marks out of hidden-line removal. With them the
# projection runs out of memory, and at sheet scale they would print as a grey smear anyway.
import drawing  # noqa: E402  (the kit module that render_all imports its view projector from)
_HOLE_MARKS = {id(ply_holes), id(ins_bores), id(tile_holes), id(inserts)}
_project_views = drawing.project_views


def _views_without_hole_marks(part, workdir, **kw):
    kids = [k for k in part.children if id(k) not in _HOLE_MARKS]
    return _project_views(Compound(children=kids), workdir, **kw)


drawing.project_views = _views_without_hole_marks

render_all(
    parts, project="GridBench", title="Grid workbench and fixture set concept", dwg_no="GBN-DWG-010",
    key_figures=["25 mm grid, M6, same as metric optical breadboards",
                 "Worktop 1,200 x 600 mm at 900 mm working height",
                 "Plywood field: 252 M6 inserts at 50 mm; 6.6 mm pin holes between",
                 "Aluminum tile 300 x 300 mm: 144 M6 holes, 9 dowel bores 8 mm H7",
                 "About 40 kg; parts about $240 vs $220 budget (estimates)"],
    cut=False,  # a section adds little: the worktop is solid plywood with the tile flush in a pocket
    flow={"title": "material flow for one part at a fixture (times are estimates)", "unit": "",
          "stages": [("Blank in", "from stock or printer"), ("Locate", "2 dowels, ~10 s"),
                     ("Clamp", "2 toe clamps, ~20 s"), ("Work", "drill, assemble or test"),
                     ("Check", "indicator, ~20 s"), ("Part out", "same fixture, next part")],
          "losses": [(4, "Rework after check, target per 100 parts", 1)]},
)
