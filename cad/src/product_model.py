"""GridBench product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the birch plywood worktop with all 1,008 grid holes
cut, eased edges, laser-etched index ticks every 100 mm and brass screw-in inserts flush in the
top; the flanged tee nuts under it; the flush aluminum precision tile with chamfered edges, all
144 M6 holes, 9 dowel bores and cap screws in its counterbores; a bolted softwood frame with eased
arrises, carriage bolt heads and a name plate; rubber-padded levelling feet with lock nuts; the
shelf with two concrete ballast slabs; and the fixture set: two printed toe clamps with M6 screws,
washers and lobed knobs holding a machined sample block on a round and a diamond pin, a two-part
fence with cap screws, stop pins, a V-block holding a round bar, and the instrument post (slotted
extrusion) with its arm and a dial indicator touching the sample block. Context is a compact
section of workshop floor.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, position and interface comes from PARAMS, derived(), classify(),
insert_kinds(), dowel_points() and fixing_points() in model.py. Axes as model.py: X along the
bench, Y front to back (front at -Y), Z up, floor at Z = 0, worktop surface at Z = PARAMS["h"].
Differences from model.py (see docs/REVIEW.md, session 2026-09-26): the two toe-clamp screws are
moved onto the nearest tile hole centers, with the clamp bodies slid in their slots (CLAMPS); the
optional wall anchor brackets (BOM 15) are left out because no wall is shown; and the worktop
carries all 1,008 holes where model.py cuts a representative patch.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Compound, Cylinder, Pos, RegularPolygon, Rot, Sphere, chamfer,
                       extrude, fillet)
from model import (PARAMS, classify, derived, dowel_points, fixing_points, grid_points,
                   insert_kinds, rod)

TITLE = "GridBench: workbench with a 25 mm hole grid and fixture set"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); aluminum precision tile "
             "at right with toe clamps holding a sample block under the dial indicator, fence, stops and "
             "V-block on the plywood grid at left, ballast slabs on the shelf"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): frame, feet, shelf and "
             "ballast; tee nuts; plywood grid worktop and inserts; precision tile and screws; pins, sample "
             "block, toe clamps, fence, stops, V-block, instrument post and dial indicator"},
    {"name": "detail", "groups": ["shell", "accessory"], "explode": False, "el": 42, "az": -35,
     "note": "Detail from the front right and above (about 42 deg elevation): the worktop and fixture set "
             "without the frame, so the 25 mm hole grid, brass inserts and the flush precision tile read clearly"},
]

# Appearance-only placement: each toe-clamp screw sits on the nearest tile hole center, and the clamp
# body slides in its slot to stay close to its model.py position. model.py puts body and screw
# together at (320, 40) and (430, -40), which fall between tile holes.
CLAMPS = [((312.5, 40.0), (312.5, 37.5), 90.0),     # (body center, screw center, rotation deg)
          ((432.0, -37.5), (437.5, -37.5), 0.0)]

# Colours (restrained product palette; kit accent)
C_PLY = "#E2C48E"
C_PLY_EDGE = "#CDAE78"
C_WOOD = "#C8A06A"
C_ALU = "#C3CAD1"
C_STEEL = "#6B7280"
C_BLACKOX = "#2E3238"
C_BRASS = "#C9A227"
C_ZINC = "#B8BEC6"
C_RUBBER = "#1F2328"
C_ACCENT = "#0F766E"
C_PRINT_LT = "#E5E7EB"
C_KNOB = "#2B2F36"
C_INK = "#3F3A33"
C_LABEL = "#F4F4F2"
C_CONCRETE = "#A8A29E"
C_SAMPLE = "#9CA3AF"
C_FLOOR = "#D4D1CB"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _chamfer_try(shape, edges, sizes):
    edges = list(edges)
    for c in sizes:
        try:
            out = chamfer(edges, c)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _eased(cx, cy, cz, sx, sy, sz, r):
    """Timber member with eased arrises."""
    b = _box(cx, cy, cz, sx, sy, sz)
    return _fillet_try(b, b.edges(), [r, r * 0.6, 1.0])


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _cutters(pts, z_top, d, depth):
    return Compound(children=[Pos(x, y, z_top - depth / 2) * Cylinder(d / 2, depth) for x, y in pts])


def _cells(solid, hole_sets, xa, ya, size, nx, ny, z_top, depth):
    """Split `solid` into nx x ny square cells from (xa, ya) and drill each cell's holes.
    hole_sets: [(points, diameter), ...]. Returns a Compound of the cells."""
    cells = []
    for i in range(nx):
        for j in range(ny):
            x1, y1 = xa + size * i, ya + size * j
            c = solid & _box(x1 + size / 2, y1 + size / 2, z_top - depth / 2, size, size, depth + 20)
            if c.volume < 1.0:
                continue
            for pts, d in hole_sets:
                sub = [(x, y) for x, y in pts if x1 < x < x1 + size and y1 < y < y1 + size]
                if sub:
                    c = c - _cutters(sub, z_top, d, depth)
            cells.append(c)
    return Compound(children=cells)


def _cap_screw(x, y, z_top, d_head=10.0, h_head=6.0, down=True):
    """M6 socket head cap screw head, top face at z_top, with a hex socket."""
    s = _zcyl(x, y, z_top - h_head / 2, d_head / 2, h_head)
    s = _fillet_try(s, s.faces().sort_by(Axis.Z)[-1].edges(), [0.8, 0.5])
    s -= _hex_z(x, y, z_top - 1.5, 5.0, 3.2)
    return s


def product_parts(P=PARAMS):
    D = derived(P)
    H, L, Dp = P["h"], P["top_l"], P["top_d"]
    lx, ly, zu = D["lx"], D["ly"], D["z_under"]
    leg = P["leg"]
    aw, ah = P["apron"]
    rw, rh = P["rail"]
    x0, y0, s, tt = P["tile_x0"], P["tile_y0"], P["tile"], P["tile_t"]
    tcx, tcy = x0 + s / 2, y0 + s / 2
    tile_pts, _ins_pts, plain_pts = classify(P)
    tee_pts, screw_pts = insert_kinds(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # explode levels (mm)
    E_TOP, E_TILE, E_FIX, E_UP = 300.0, 470.0, 620.0, 760.0

    # ------------------------------------------------------------ worktop (BOM 4, 5)
    tt_ = P["top_t"]
    top = _box(0, 0, H - tt_ / 2, L, Dp, tt_)
    top = _fillet_try(top, top.edges().filter_by(Axis.Z), [3.0, 2.0])
    top = _fillet_try(top, top.faces().sort_by(Axis.Z)[-1].edges(), [1.0, 0.6])
    top = _fillet_try(top, top.faces().sort_by(Axis.Z)[0].edges(), [1.0, 0.6])
    # plywood lamination lines on the edges (appearance only)
    for zz in (H - 4.5, H - 9.0, H - 13.5):
        ring = _box(0, 0, zz, L + 2, Dp + 2, 0.35) - _box(0, 0, zz, L - 0.6, Dp - 0.6, 1.0)
        top -= ring
    top -= _box(tcx, tcy, H - tt_ / 2, s, s, tt_ + 2)
    # all 1,008 holes, cut per 150 mm cell (cell edges fall midway between grid lines) so that
    # each face carries few holes and tessellation stays fast; the cells meet flush
    top = _cells(top, [(plain_pts, P["plain_d"]), (screw_pts, P["insert_hole_d"]), (tee_pts, P["tee_hole_d"])],
                 -L / 2, -Dp / 2, 150.0, int(L // 150), int(Dp // 150), H + 1, tt_ + 2)
    add("Plywood grid worktop (birch)", top, C_PLY, "wood", 4, "shell", (0, 0, E_TOP))

    # laser-etched index ticks every 100 mm along the front and left margins
    ticks = []
    for i, j, x, y in grid_points(P):
        if j == 0 and i % 4 == 0:
            ticks.append(_box(x, -Dp / 2 + 3.2, H + 0.05, 0.8, 4.0, 0.1))
        if i == 0 and j % 4 == 0:
            ticks.append(_box(-L / 2 + 3.2, y, H + 0.05, 4.0, 0.8, 0.1))
    add("Grid index marks (laser-etched)", _fuse(ticks), C_INK, "paper", 4, "shell", (0, 0, E_TOP))

    ri = P["insert_od"] / 2 - 0.75
    ins = [_zcyl(x, y, H - P["insert_len"] / 2, ri, P["insert_len"]) - _zcyl(x, y, H - P["insert_len"] / 2, 2.5,
                                                                                P["insert_len"] + 1)
           for x, y in screw_pts]
    add("M6 screw-in inserts, brass (122)", Compound(children=ins), C_BRASS, "metal", 5, "shell",
        (0, 0, E_TOP + 110))

    tee = []
    for x, y in tee_pts:
        t = (_zcyl(x, y, zu - P["tee_flange_t"] / 2, P["tee_flange_d"] / 2, P["tee_flange_t"])
             + _zcyl(x, y, zu + P["tee_barrel_len"] / 2, P["tee_barrel_d"] / 2, P["tee_barrel_len"]))
        t -= _zcyl(x, y, zu + P["tee_barrel_len"] / 2 - 1, 2.5, P["tee_barrel_len"] + 4)
        tee.append(t)
    add("M6 flanged tee nuts, zinc (130)", Compound(children=tee), C_ZINC, "metal", 5, "internal",
        (0, 0, E_TOP - 150))

    # ------------------------------------------------------------ precision tile (BOM 6)
    tile = _box(tcx, tcy, H - tt / 2, s, s, tt)
    tile = _chamfer_try(tile, tile.faces().sort_by(Axis.Z)[-1].edges(), [0.8, 0.5])
    tile = _fillet_try(tile, tile.edges().filter_by(Axis.Z), [1.0, 0.5])
    tile -= _cutters(fixing_points(P), H + 0.01, P["cbore_d"], P["cbore_depth"])
    tile = _cells(tile, [(tile_pts, P["tap_drill_d"]), (dowel_points(P), P["dowel_d"]),
                         (fixing_points(P), P["fix_hole_d"])], x0, y0, 100.0, 3, 3, H + 1, tt + 2)
    add("Precision grid tile (aluminum)", tile, C_ALU, "metal", 6, "shell", (0, 0, E_TILE))
    fs = [_cap_screw(x, y, H - 0.5) for x, y in fixing_points(P)]
    add("Tile fixing cap screws", _fuse(fs), C_BLACKOX, "metal", 12, "shell", (0, 0, E_TILE + 90))

    # ------------------------------------------------------------ frame (BOM 1)
    members = [_eased(sx * lx, sy * ly, P["foot_h"] + D["leg_h"] / 2, leg, leg, D["leg_h"], 4.0)
               for sx in (-1, 1) for sy in (-1, 1)]
    members += [_eased(0, sy * D["long_apron_y"], zu - ah / 2, D["long_apron_len"], aw, ah, 3.0) for sy in (-1, 1)]
    members += [_eased(sx * D["end_apron_x"], 0, zu - ah / 2, aw, D["end_apron_len"], ah, 3.0) for sx in (-1, 1)]
    members += [_eased(x, 0, zu - rh / 2, rw, D["rail_len"], rh, 2.5) for x in P["cross_x"]]
    members += [_eased(0, sy * ly, P["low_rail_z"] + rh / 2, D["low_rail_len"], rw, rh, 2.5) for sy in (-1, 1)]
    add("Bench frame (bolted softwood)", Compound(children=members), C_WOOD, "wood", 1, "internal", (0, 0, 0))
    pk = D["packer_t"]
    packers = [_box(x, tcy, zu + pk / 2, rw, s, pk) for x in P["cross_x"] if x0 < x < x0 + s]
    add("Hardwood packers under the tile", _fuse(packers), "#9A6B3F", "wood", 1, "internal", (0, 0, E_TOP - 90))

    # carriage bolt heads (domed) on the outer faces of the aprons at each leg
    heads = []
    yo = ly + leg / 2
    xo = lx + leg / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            for dz in (-35.0, -85.0):
                h = Pos(sx * lx, sy * yo, zu + dz) * Rot(90 * sy, 0, 0) * (Sphere(9.5) & Pos(0, 0, 5) * Box(20, 20, 10))
                heads.append(h)
            h = Pos(sx * xo, sy * ly, zu - 60) * Rot(0, -90 * sx, 0) * (Sphere(9.5) & Pos(0, 0, 5) * Box(20, 20, 10))
            heads.append(h)
    add("Carriage bolt heads, M8", _fuse(heads), C_ZINC, "metal", 1, "internal", (0, 0, 0))

    # name plate on the front apron
    fy = -(D["long_apron_y"] + aw / 2)
    npl = _box(-lx + 150, fy - 0.3, zu - ah / 2, 150, 0.6, 34)
    npl = _fillet_try(npl, npl.edges().filter_by(Axis.Y), [3.0, 1.5])
    add("Name plate", npl, C_ACCENT, "painted", 1, "internal", (0, -60, 0))
    ink = (_box(-lx + 115, fy - 0.7, zu - ah / 2 + 5, 60, 0.3, 9) + _box(-lx + 115, fy - 0.7, zu - ah / 2 - 8, 60, 0.3, 3)
           + _box(-lx + 190, fy - 0.7, zu - ah / 2, 36, 0.3, 20) - _box(-lx + 190, fy - 0.7, zu - ah / 2, 28, 1, 12))
    add("Name plate print", ink, C_LABEL, "paper", 1, "internal", (0, -60, 0))

    # ------------------------------------------------------------ levelling feet (BOM 2)
    rt, pt_, pr = P["rubber_t"], P["foot_pad_t"], P["foot_pad_d"] / 2
    rub, pads, stems = [], [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * lx, sy * ly
            r_ = _zcyl(x, y, rt / 2, pr - 1, rt)
            rub.append(_fillet_try(r_, r_.faces().sort_by(Axis.Z)[0].edges(), [1.0, 0.5]))
            p_ = _zcyl(x, y, rt + (pt_ - rt) / 2, pr, pt_ - rt)
            pads.append(_fillet_try(p_, p_.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 2.0, 1.0]))
            stems.append(_zcyl(x, y, pt_ + 7, 5, 14) + _hex_z(x, y, pt_ + 6.5, 17.0, 6.0))
    add("Levelling foot rubber pads", _fuse(rub), C_RUBBER, "rubber", 2, "internal", (0, 0, -200))
    add("Levelling foot steel pads", _fuse(pads), C_STEEL, "metal", 2, "internal", (0, 0, -160))
    add("Levelling foot stems and lock nuts", _fuse(stems), C_ZINC, "metal", 2, "internal", (0, 0, -120))

    # ------------------------------------------------------------ shelf (BOM 3) and ballast (BOM 14)
    sl, sd, st = D["shelf"]
    shelf = _box(0, 0, D["shelf_z"] + st / 2, sl, sd, st)
    shelf = _fillet_try(shelf, shelf.edges(), [1.0, 0.6])
    add("Lower shelf (plywood)", shelf, C_PLY_EDGE, "wood", 3, "internal", (0, -650, -260))
    ax_, ay_, az_ = P["slab"]
    zs = D["shelf_z"] + st + az_ / 2
    slabs = []
    for sx in (-1, 1):
        b = _box(sx * (ax_ / 2 + P["slab_gap"] / 2), 0, zs, ax_, ay_, az_)
        slabs.append(_fillet_try(b, b.edges(), [2.5, 1.5]))
    add("Ballast slabs (concrete)", _fuse(slabs), C_CONCRETE, "paper", 14, "internal", (0, -650, -130))

    # ------------------------------------------------------------ pins (BOM 7, 13)
    dp = dowel_points(P)
    r = P["dowel_d"] / 2
    pin_z = H + P["pin_len"] / 2 - 6
    pin = _zcyl(dp[0][0], dp[0][1], pin_z, r, P["pin_len"])
    pin = _chamfer_try(pin, pin.faces().sort_by(Axis.Z)[-1].edges(), [0.8, 0.5])
    add("Round dowel pin, 8 mm", pin, C_STEEL, "metal", 7, "accessory", (0, 0, E_FIX))
    dia = Cylinder(r, P["pin_len"]) & Box(P["dowel_d"], 3.0, P["pin_len"] + 1)
    dia = Pos(dp[3][0], dp[3][1], pin_z) * dia
    add("Diamond locating pin, 8 mm", dia, C_BLACKOX, "metal", 13, "accessory", (0, 0, E_FIX))

    # ------------------------------------------------------------ sample part (context for the fixture, no BOM)
    wx, wy = x0 + 100, -40.0
    blk = _box(wx, wy, H + 20, 160, 100, 40)
    blk = _chamfer_try(blk, blk.edges(), [1.0, 0.6])
    blk -= _box(wx - 20, wy + 10, H + 35, 70, 50, 12)
    for hx in (wx + 45, wx + 60):
        blk -= _zcyl(hx, wy - 25, H + 30, 4.0, 22)
    add("Sample part (machined block)", blk, C_SAMPLE, "metal", None, "accessory", (0, 0, E_FIX + 60))

    # ------------------------------------------------------------ toe clamps (BOM 8) with screws and knobs (BOM 12)
    cl, cw, ct = P["clamp"]
    z0 = 40.0
    bodies, screws, knobs, washers = [], [], [], []
    for (bx_, by_), (sx_, sy_), ang in CLAMPS:
        body = _box(0, 0, z0 + ct / 2, cl, cw, ct)
        body = _fillet_try(body, body.edges().filter_by(Axis.Z), [3.0, 2.0])
        body = _fillet_try(body, body.faces().sort_by(Axis.Z)[-1].edges(), [2.0, 1.2])
        body -= _box(-cl * 0.1, 0, z0 + ct / 2, cl * 0.45, P["clamp_slot"], ct + 2)
        body -= _box(-cl / 2, 0, z0, 16, cw + 2, 10)                     # nose relief (toe)
        heel = _box(cl / 2 - 7, 0, z0 / 2, 14, cw, z0)
        heel = _fillet_try(heel, heel.edges().filter_by(Axis.Z), [2.0, 1.0])
        c = body + heel
        for k in range(4):                                               # grip ribs on the top
            c -= _box(cl / 2 - 26 + 6 * k, 0, z0 + ct, 2.0, cw + 2, 1.6)
        bodies.append(Pos(bx_, by_, H) * Rot(0, 0, ang) * c)
        zt = H + z0 + ct
        washers.append(_zcyl(sx_, sy_, zt + 0.8, 6.0, 1.6) - _zcyl(sx_, sy_, zt + 0.8, 3.2, 3))
        screws.append(_zcyl(sx_, sy_, (H - 8 + zt + 14) / 2, 3.0, zt + 14 - (H - 8)))
        k_ = _zcyl(sx_, sy_, zt + 1.6 + 7, 14, 14)
        for j in range(6):
            k_ -= Pos(sx_, sy_, zt + 8.6) * Rot(0, 0, 60 * j) * Pos(16.5, 0, 0) * Cylinder(5.0, 16)
        k_ = _fillet_try(k_, k_.faces().sort_by(Axis.Z)[-1].edges(), [2.0, 1.2, 0.6])
        knobs.append(k_)
    add("Printed toe clamps (PETG)", _fuse(bodies), C_ACCENT, "plastic", 8, "accessory", (0, 0, E_UP))
    add("Clamp washers", _fuse(washers), C_ZINC, "metal", 12, "accessory", (0, 0, E_UP + 90))
    add("Clamp M6 screws", _fuse(screws), C_BLACKOX, "metal", 12, "accessory", (0, 0, E_UP + 120))
    add("Printed clamp knobs", _fuse(knobs), C_KNOB, "plastic", 12, "accessory", (0, 0, E_UP + 150))

    # ------------------------------------------------------------ fence, stops, V-block (BOM 9)
    fl, fw, fh = P["fence_seg"]
    segs, fscr = [], []
    for i in range(2):
        cx = -400 + fl / 2 + i * fl
        f = _box(cx, 187.5, H + fh / 2, fl - 1, fw, fh)
        f = _fillet_try(f, f.edges().filter_by(Axis.Z), [2.0, 1.0])
        f = _fillet_try(f, f.faces().sort_by(Axis.Z)[-1].edges(), [1.5, 1.0])
        f -= _box(cx, 187.5 - fw / 2, H + fh - 8, fl - 20, 1.2, 1.0)    # sight line on the working face
        for hx in (cx - 62.5, cx + 62.5):
            f -= _zcyl(hx, 187.5, H + fh - 4, 5.6, 8.1)
            fscr.append(_cap_screw(hx, 187.5, H + fh - 1.5))
        segs.append(f)
    add("Printed fence segments (PETG)", _fuse(segs), C_PRINT_LT, "plastic", 9, "accessory", (0, 0, E_TILE))
    add("Fence cap screws", _fuse(fscr), C_BLACKOX, "metal", 12, "accessory", (0, 0, E_TILE + 120))

    stops = []
    for x in (-462.5, -137.5):
        st_ = _zcyl(x, -12.5, H + P["stop_h"] / 2, P["stop_d"] / 2, P["stop_h"])
        st_ = _fillet_try(st_, st_.faces().sort_by(Axis.Z)[-1].edges(), [2.0, 1.0])
        st_ += _zcyl(x, -12.5, H + 1.5, P["stop_d"] / 2 + 2.5, 3.0)
        st_ -= _zcyl(x, -12.5, H + P["stop_h"] - 3, 1.8, 3.2)
        stops.append(st_)
    add("Printed stop pins", _fuse(stops), C_ACCENT, "plastic", 9, "accessory", (0, 0, E_TILE))

    vl, vw, vh = P["vblock"]
    vb = _box(-300, -150, H + vh / 2, vl, vw, vh)
    vb = _fillet_try(vb, vb.edges().filter_by(Axis.Y), [2.0, 1.0])
    vb -= Pos(-300, -150, H + vh) * Rot(45, 0, 0) * Box(vl + 4, vw * 0.83, vw * 0.83)
    vb -= _box(-300, -150 - vw / 2, H + 15, vl - 24, 1.2, 12)             # side recess (print cue)
    add("Printed V-block (PETG)", vb, C_PRINT_LT, "plastic", 9, "accessory", (0, 0, E_TILE))
    apex = H + vh - vw * 0.83 / 2 ** 0.5
    bar_r = 15.0
    bar = _xcyl(-300, -150, apex + bar_r * 2 ** 0.5, bar_r, 150)
    bar = _chamfer_try(bar, bar.edges(), [1.0, 0.5])
    add("Sample round bar (steel)", bar, "#8B929A", "metal", None, "accessory", (0, 0, E_TILE + 150))

    # ------------------------------------------------------------ instrument post (BOM 10), indicator (BOM 11)
    PX, PY = x0 + s + 12.5, 237.5
    IX, IY = x0 + 150, wy
    azz = H + P["arm_z"]
    pw, pd, ph = P["post"]
    fl_, fw_, ft_ = P["post_foot"]
    EP = (300, 250, E_TILE)
    foot = _box(PX, PY, H + ft_ / 2, fl_, fw_, ft_)
    foot = _fillet_try(foot, foot.edges().filter_by(Axis.Z), [6.0, 4.0])
    foot = _fillet_try(foot, foot.faces().sort_by(Axis.Z)[-1].edges(), [1.5, 1.0])
    add("Printed post foot", foot, C_ACCENT, "plastic", 10, "accessory", EP)
    add("Post foot cap screw", _cap_screw(PX - 25, PY, H + ft_ + 6), C_BLACKOX, "metal", 12, "accessory",
        (300, 250, E_TILE + 60))
    post = _box(PX, PY, H + ft_ + ph / 2, pw, pd, ph)
    post = _fillet_try(post, post.edges().filter_by(Axis.Z), [1.5, 1.0])
    zc = H + ft_ + ph / 2
    for sx in (-1, 1):                                                   # T-slots on the wide faces
        for dy in (-10, 10):
            post -= _box(PX + sx * pw / 2, PY + dy, zc, 3.0, 6.0, ph + 2)
    for sy in (-1, 1):
        post -= _box(PX, PY + sy * pd / 2, zc, 6.0, 3.0, ph + 2)
    add("Instrument post (aluminum extrusion)", post, C_ALU, "metal", 10, "accessory", EP)
    cap = _box(PX, PY, H + ft_ + ph + 1.5, pw, pd, 3.0)
    cap = _fillet_try(cap, cap.edges(), [1.0, 0.5])
    add("Post end cap", cap, C_KNOB, "plastic", 10, "accessory", EP)
    arm = rod((PX, PY, azz), (IX, IY + 25, azz), P["arm_d"] / 2)
    add("Indicator arm (steel)", arm, C_ZINC, "metal", 10, "accessory", EP)
    cb = _box(PX, PY, azz, 36, 50, 40)
    cb = _fillet_try(cb, cb.edges(), [4.0, 2.5, 1.0])
    cb += _ycyl(PX + 24, PY, azz + 8, 7.0, 14) + Pos(PX + 24, PY, azz + 8) * Rot(0, 90, 0) * Cylinder(3, 16)
    add("Printed arm clamp and knob", cb, C_KNOB, "plastic", 10, "accessory", EP)
    swv = _zcyl(IX, IY + 25, azz, 11.0, 26)
    swv = _fillet_try(swv, swv.edges(), [2.0, 1.0])
    add("Printed swivel clamp", swv, C_KNOB, "plastic", 10, "accessory", EP)

    EI = EP
    iz = H + 135
    case = _ycyl(IX, IY, iz, 28, 18)
    case = _fillet_try(case, case.edges(), [2.0, 1.0])
    case += rod((IX, IY + 9, iz), (IX, IY + 25, iz), 5)                   # lug back
    case += rod((IX, IY + 25, iz), (IX, IY + 25, azz - 12), 6)            # drop rod to the swivel
    case += _zcyl(IX, IY, iz + 32, 3.5, 8) + Pos(IX, IY, iz + 38) * Sphere(4.5)
    add("Dial indicator case", case, C_ZINC, "metal", 11, "accessory", EI)
    bez = _ycyl(IX, IY - 10, iz, 29.5, 3.0) - _ycyl(IX, IY - 10, iz, 25.5, 4.0)
    bez = _fillet_try(bez, bez.edges(), [1.0, 0.5])
    add("Dial indicator bezel", bez, C_ACCENT, "painted", 11, "accessory", EI)
    face = _ycyl(IX, IY - 9.25, iz, 25.5, 0.4)
    add("Dial face", face, C_LABEL, "paper", 11, "accessory", EI)
    crystal = _ycyl(IX, IY - 11.0, iz, 25.6, 0.8)
    add("Dial crystal", crystal, "#DCEBF5", "clear", 11, "accessory", EI)
    marks = []
    for k in range(50):
        a = 2 * math.pi * k / 50
        ln = 4.0 if k % 5 == 0 else 2.2
        rr = 23.5 - ln / 2
        marks.append(Pos(IX + rr * math.sin(a), IY - 9.6, iz + rr * math.cos(a)) * Rot(0, math.degrees(a), 0)
                     * Box(0.6, 0.3, ln))
    marks.append(_box(IX, IY - 9.75, iz + 8, 1.0, 0.3, 18))                 # needle
    marks.append(_ycyl(IX, IY - 9.9, iz, 2.2, 0.6))
    add("Dial graduations and needle", _fuse(marks), C_KNOB, "paper", 11, "accessory", EI)
    stem = rod((IX, IY, H + 45), (IX, IY, iz - 28), 4.0)
    stem += rod((IX, IY, H + 40.5), (IX, IY, H + 46), 1.5) + Pos(IX, IY, H + 41.0) * Sphere(1.5)
    add("Dial indicator stem and contact point", stem, C_STEEL, "metal", 11, "accessory", EI)

    # ------------------------------------------------------------ context: a compact section of workshop floor
    fl0 = _box(0, 0, -10, L + 260, Dp + 260, 20)
    fl0 = _fillet_try(fl0, fl0.faces().sort_by(Axis.Z)[-1].edges(), [4.0, 2.0])
    add("Workshop floor section", fl0, C_FLOOR, "paper", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
