"""GridBench parametric model (build123d), TRL 3, massing-plus level of detail.

Revised 2026-09-25 under GBN-DDR-002 (recommendations accepted by Amish): 45 x 120 mm aprons,
flanged M6 tee nuts pressed in from the underside at every insert position with a clear underside,
screw-in inserts kept only where a frame member lies below, and rubber-padded levelling feet.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    gridbench-assembly.step / .stl   the bench with worktop, tile, fixture set, ballast and anchor
    precision-tile.step / .stl       300 x 300 mm aluminum tile, all 144 M6 holes, 9 dowel bores,
                                     4 counterbored fixing holes
    worktop.step / .stl              plywood worktop with the tile pocket and a representative
                                     8 x 8 patch of grid holes (front-left corner)

Axes: X along the bench (1,200 mm), Y front to back (front at -Y), Z up, floor at Z = 0,
worktop surface at Z = PARAMS["h"]. The worktop is centered on X = Y = 0. Grid hole centers sit at
12.5 + 25 k mm from the front-left corner of the worktop in both directions; the tile continues the
same grid.

The plywood field has 1,008 holes. To keep the STEP and STL files small, the worktop carries only a
representative 8 x 8 patch of them (with its inserts); the full pattern is defined by grid_points()
and drawn as surface marks in the concept media. The tile, whose holes are the precision interface,
is modeled with every hole. Main dimensions and interfaces only; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (GBN-CAL-001) and drawing GBN-DWG-001
(cad/src/sheets.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # grid standard (R1): 25 mm pitch, M6, 12.5 mm edge offset
    "pitch": 25.0, "edge": 12.5,
    "plain_d": 6.6,                  # plain pin holes in the plywood field
    "insert_hole_d": 8.5, "insert_od": 10.0, "insert_len": 13.0, "insert_every": 2,   # 50 mm sub-grid
    # 5 flanged M6 tee nuts, pressed in from the underside (GBN-DDR-002, R7 option a)
    "tee_hole_d": 8.0, "tee_flange_d": 19.0, "tee_flange_t": 1.5, "tee_barrel_d": 7.9, "tee_barrel_len": 9.5,
    # 4 worktop
    "top_l": 1200.0, "top_d": 600.0, "top_t": 18.0, "h": 900.0,
    # 6 precision tile, flush in a through pocket, on packers over two cross rails
    "tile": 300.0, "tile_t": 12.7, "tile_x0": 225.0, "tile_y0": -150.0,
    "tap_drill_d": 5.0, "dowel_d": 8.0, "dowel_pitch": 100.0, "cbore_d": 11.0, "cbore_depth": 6.5,
    "fix_hole_d": 7.0, "fix_offset": (22.5, 125.0),   # fixing holes: X from each tile edge, +/- Y
    # 1 frame, bolted softwood (width in plan, depth in Z)
    "leg": 70.0, "leg_inset": 20.0, "foot_h": 25.0,
    "apron": (45.0, 120.0), "rail": (45.0, 70.0), "low_rail_z": 105.0,
    "cross_x": (-300.0, 0.0, 247.5, 502.5),          # cross rail centers; the last two carry the tile
    # 2 levelling feet with rubber pads (GBN-DDR-002)
    "foot_pad_d": 50.0, "foot_pad_t": 12.0, "rubber_t": 3.0, "adjust": 15.0,
    # 3 shelf, resting on the two low rails
    "shelf_t": 12.0,
    # 14 ballast: two concrete paving slabs on the shelf
    "slab": (400.0, 400.0, 35.0), "slab_gap": 40.0,
    # 7, 13 dowel pins (round and diamond), 8 mm h6 x 20
    "pin_len": 20.0,
    # 8 printed toe clamp (PETG): length, width, body depth, slot width
    "clamp": (70.0, 24.0, 30.0), "clamp_slot": 6.6,
    # 9 printed fence (two 200 mm segments), stops, V-block
    "fence_seg": (190.0, 25.0, 50.0), "vblock": (100.0, 60.0, 60.0), "stop_d": 12.0, "stop_h": 24.0,
    # 10 instrument post on a grid foot; 11 dial indicator
    "post": (20.0, 40.0, 350.0), "post_foot": (80.0, 60.0, 12.0), "arm_d": 18.0, "arm_z": 300.0,
    # 15 wall anchor brackets (optional), steel angle
    "anchor": (50.0, 50.0, 40.0, 4.0),
}


def derived(p=PARAMS):
    """Dimensions the calc note and the drawing quote, computed from PARAMS."""
    L, D, H = p["top_l"], p["top_d"], p["h"]
    leg = p["leg"]
    lx = L / 2 - p["leg_inset"] - leg / 2            # leg center, X
    ly = D / 2 - p["leg_inset"] - leg / 2            # leg center, Y
    z_under = H - p["top_t"]
    aw, ah = p["apron"]
    nx, ny = int(round(L / p["pitch"])), int(round(D / p["pitch"]))
    long_apron_y = ly + leg / 2 - aw / 2
    end_apron_x = lx + leg / 2 - aw / 2
    rail_len = 2 * long_apron_y - aw                  # between the inner faces of the long aprons
    low_rail_len = 2 * lx - leg
    shelf = (low_rail_len, 2 * ly + p["rail"][0], p["shelf_t"])
    shelf_z = p["low_rail_z"] + p["rail"][1]          # underside of the shelf
    return dict(
        lx=lx, ly=ly, z_under=z_under, nx=nx, ny=ny,
        leg_h=z_under - p["foot_h"],
        long_apron_y=long_apron_y, end_apron_x=end_apron_x,
        long_apron_len=L - 2 * p["leg_inset"], end_apron_len=2 * ly - leg,
        rail_len=rail_len, low_rail_len=low_rail_len,
        shelf=shelf, shelf_z=shelf_z,
        packer_t=(H - p["tile_t"]) - z_under,           # tile underside above the rail tops
        tile_under=H - p["tile_t"],
        apron_span=2 * lx,                             # leg center to leg center along X
        rail_span=2 * long_apron_y,                    # apron center to apron center along Y
        foot_base_y=2 * ly, foot_base_x=2 * lx,
    )


def grid_points(p=PARAMS):
    """All grid hole centers (x, y) with their column and row index."""
    L, D, pitch, e = p["top_l"], p["top_d"], p["pitch"], p["edge"]
    nx, ny = int(round(L / pitch)), int(round(D / pitch))
    return [(i, j, -L / 2 + e + pitch * i, -D / 2 + e + pitch * j) for i in range(nx) for j in range(ny)]


def in_tile(x, y, p=PARAMS):
    return (p["tile_x0"] < x < p["tile_x0"] + p["tile"]) and (p["tile_y0"] < y < p["tile_y0"] + p["tile"])


def classify(p=PARAMS):
    """Split the grid into tile holes, insert positions and plain pin holes."""
    tile, ins, plain = [], [], []
    k = p["insert_every"]
    for i, j, x, y in grid_points(p):
        if in_tile(x, y, p):
            tile.append((x, y))
        elif i % k == 0 and j % k == 0:
            ins.append((x, y))
        else:
            plain.append((x, y))
    return tile, ins, plain


def frame_footprint(p=PARAMS):
    """Plan rectangles (xmin, xmax, ymin, ymax) of the frame members directly under the worktop."""
    d = derived(p)
    aw = p["apron"][0]
    rw = p["rail"][0]
    leg = p["leg"]
    out = []
    for sy in (-1, 1):
        yc = sy * d["long_apron_y"]
        out.append((-d["long_apron_len"] / 2, d["long_apron_len"] / 2, yc - aw / 2, yc + aw / 2))
    for sx in (-1, 1):
        xc = sx * d["end_apron_x"]
        out.append((xc - aw / 2, xc + aw / 2, -d["end_apron_len"] / 2, d["end_apron_len"] / 2))
    for x in p["cross_x"]:
        out.append((x - rw / 2, x + rw / 2, -d["rail_len"] / 2, d["rail_len"] / 2))
    for sx in (-1, 1):
        for sy in (-1, 1):
            out.append((sx * d["lx"] - leg / 2, sx * d["lx"] + leg / 2, sy * d["ly"] - leg / 2, sy * d["ly"] + leg / 2))
    return out


def insert_kinds(p=PARAMS):
    """Split the insert positions: tee nuts where the flange has a clear underside, screw-in inserts
    where a frame member lies within the flange radius (GBN-DDR-002)."""
    _, ins, _ = classify(p)
    r = p["tee_flange_d"] / 2
    fp = frame_footprint(p)
    def blocked(x, y):
        for x1, x2, y1, y2 in fp:
            dx = max(x1 - x, 0.0, x - x2)
            dy = max(y1 - y, 0.0, y - y2)
            if dx * dx + dy * dy < r * r:
                return True
        return False
    tee = [(x, y) for x, y in ins if not blocked(x, y)]
    screw = [(x, y) for x, y in ins if blocked(x, y)]
    return tee, screw


def dowel_points(p=PARAMS):
    x0, y0, s = p["tile_x0"], p["tile_y0"], p["tile"]
    c = [s / 2 - p["dowel_pitch"], s / 2, s / 2 + p["dowel_pitch"]]
    return [(x0 + a, y0 + b) for a in c for b in c]


def fixing_points(p=PARAMS):
    x0, s = p["tile_x0"], p["tile"]
    fx, fy = p["fix_offset"]
    return [(x0 + fx, sy * fy) for sy in (-1, 1)] + [(x0 + s - fx, sy * fy) for sy in (-1, 1)]


def _b3d():
    import build123d
    return build123d


def rod(a, c, r):
    """Round bar of radius r between two 3D points."""
    b = _b3d()
    a, c = b.Vector(*a), b.Vector(*c)
    return b.Solid.make_cylinder(r, (c - a).length, b.Plane(origin=a, z_dir=(c - a).normalized()))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def drilled(solid, pts, z_top, d, depth):
    """Cut round holes of diameter d, depth from z_top downward, at (x, y) points, in one boolean."""
    b = _b3d()
    cutters = b.Compound(children=[b.Pos(x, y, z_top - depth / 2) * b.Cylinder(d / 2, depth) for x, y in pts])
    return solid - cutters


def patch(pts, p=PARAMS, n=8):
    """Holes in the representative front-left patch of n x n grid positions."""
    xmax = -p["top_l"] / 2 + p["pitch"] * n
    ymax = -p["top_d"] / 2 + p["pitch"] * n
    return [(x, y) for x, y in pts if x < xmax and y < ymax]


def build_parts(p=PARAMS, full_top_holes=False):
    """Return {key: solid} for the BOM lines that have geometry (1 to 11, 13 to 15)."""
    b = _b3d()
    d = derived(p)
    H, L, D = p["h"], p["top_l"], p["top_d"]
    lx, ly, zu = d["lx"], d["ly"], d["z_under"]
    leg = p["leg"]
    aw, ah = p["apron"]
    rw, rh = p["rail"]
    x0, y0, s, tt = p["tile_x0"], p["tile_y0"], p["tile"], p["tile_t"]
    tcx, tcy = x0 + s / 2, y0 + s / 2
    tile_pts, ins_pts, plain_pts = classify(p)
    out = {}

    # 1 frame: legs, aprons, cross rails, low rails, and hardwood packers under the tile
    legs = [box(sx * lx, sy * ly, p["foot_h"] + d["leg_h"] / 2, leg, leg, d["leg_h"]) for sx in (-1, 1) for sy in (-1, 1)]
    aprons = [box(0, sy * d["long_apron_y"], zu - ah / 2, d["long_apron_len"], aw, ah) for sy in (-1, 1)]
    aprons += [box(sx * d["end_apron_x"], 0, zu - ah / 2, aw, d["end_apron_len"], ah) for sx in (-1, 1)]
    cross = [box(x, 0, zu - rh / 2, rw, d["rail_len"], rh) for x in p["cross_x"]]
    low = [box(0, sy * ly, p["low_rail_z"] + rh / 2, d["low_rail_len"], rw, rh) for sy in (-1, 1)]
    pk = d["packer_t"]
    packers = [box(x, tcy, zu + pk / 2, rw, s, pk) for x in p["cross_x"] if x0 < x < x0 + s]
    out["frame"] = fuse(legs + aprons + cross + low + packers)

    # 2 levelling feet (rubber pad, steel pad and threaded stem into the leg)
    rt = p["rubber_t"]
    out["feet"] = fuse([b.Pos(sx * lx, sy * ly, 0) * (b.Pos(0, 0, rt / 2) * b.Cylinder(p["foot_pad_d"] / 2 - 1, rt)
                                                      + b.Pos(0, 0, rt + (p["foot_pad_t"] - rt) / 2) * b.Cylinder(p["foot_pad_d"] / 2, p["foot_pad_t"] - rt)
                                                      + b.Pos(0, 0, p["foot_pad_t"] + 7) * b.Cylinder(5, 14))
                        for sx in (-1, 1) for sy in (-1, 1)])

    # 3 shelf
    sl, sd, st = d["shelf"]
    out["shelf"] = box(0, 0, d["shelf_z"] + st / 2, sl, sd, st)

    # 4 worktop with the through pocket and a representative patch of holes (or all of them)
    top = box(0, 0, H - p["top_t"] / 2, L, D, p["top_t"]) - box(tcx, tcy, H - p["top_t"] / 2, s, s, p["top_t"] + 2)
    pl = plain_pts if full_top_holes else patch(plain_pts, p)
    tee_pts, screw_pts = insert_kinds(p)
    tp = tee_pts if full_top_holes else patch(tee_pts, p)
    sp = screw_pts if full_top_holes else patch(screw_pts, p)
    top = drilled(top, pl, H + 1, p["plain_d"], p["top_t"] + 2)
    top = drilled(top, sp, H + 1, p["insert_hole_d"], p["top_t"] + 2)
    top = drilled(top, tp, H + 1, p["tee_hole_d"], p["top_t"] + 2)
    out["worktop"] = top

    # 5 M6 threaded inserts in the patch: screw-in sleeves over frame members, flanged tee nuts
    # pressed in from the underside elsewhere (barrel up into the plywood, flange under it)
    screw_in = [b.Pos(x, y, H - p["insert_len"] / 2) * (b.Cylinder(p["insert_od"] / 2 - 0.75, p["insert_len"])
                                                        - b.Cylinder(2.5, p["insert_len"] + 1)) for x, y in sp]
    zb = zu
    tee = [b.Pos(x, y, zb) * ((b.Pos(0, 0, -p["tee_flange_t"] / 2) * b.Cylinder(p["tee_flange_d"] / 2, p["tee_flange_t"])
                               + b.Pos(0, 0, p["tee_barrel_len"] / 2) * b.Cylinder(p["tee_barrel_d"] / 2, p["tee_barrel_len"]))
                              - b.Pos(0, 0, p["tee_barrel_len"] / 2 - 1) * b.Cylinder(2.5, p["tee_barrel_len"] + 4)) for x, y in tp]
    out["inserts"] = fuse(screw_in + tee)

    # 6 precision tile: every M6 tap hole, dowel bores and counterbored fixing holes
    tile = box(tcx, tcy, H - tt / 2, s, s, tt)
    tile = drilled(tile, tile_pts, H + 1, p["tap_drill_d"], tt + 2)
    tile = drilled(tile, dowel_points(p), H + 1, p["dowel_d"], tt + 2)
    tile = drilled(tile, fixing_points(p), H + 1, p["fix_hole_d"], tt + 2)
    tile = drilled(tile, fixing_points(p), H + 0.01, p["cbore_d"], p["cbore_depth"])
    out["tile"] = tile

    # 7 round dowel and 13 diamond (relieved) pin, in two bores of the front row
    dp = dowel_points(p)
    r = p["dowel_d"] / 2
    pin_z = H + p["pin_len"] / 2 - 6
    out["pins"] = b.Pos(dp[0][0], dp[0][1], pin_z) * b.Cylinder(r, p["pin_len"])
    dia = b.Cylinder(r, p["pin_len"]) & b.Box(p["dowel_d"], 3.0, p["pin_len"] + 1)   # relieved across the pin line
    out["diamond"] = b.Pos(dp[3][0], dp[3][1], pin_z) * dia

    # 8 printed toe clamps: slotted body, heel, M6 screw and knob
    cl, cw, ct = p["clamp"]
    def toe(x, y, ang, z0):
        body = box(0, 0, z0 + ct / 2, cl, cw, ct) - box(-cl * 0.1, 0, z0 + ct / 2, cl * 0.45, p["clamp_slot"], ct + 2)
        heel = box(cl / 2 - 7, 0, (z0) / 2, 14, cw, z0) if z0 > 0 else None
        c = body + heel if heel else body
        screw = b.Pos(0, 0, (z0 + ct + 12) / 2) * b.Cylinder(3, z0 + ct + 12) + b.Pos(0, 0, z0 + ct + 6) * b.Cylinder(10, 12)
        return b.Pos(x, y, H) * (b.Rot(0, 0, ang) * c + screw)
    wx, wy = x0 + 100, -40.0            # example workpiece, 160 x 100 x 40, on the pins
    out["clamps"] = fuse([toe(wx - 5, 40, 90, 40.0), toe(x0 + 205, -40, 0, 40.0)])

    # 9 fence (two segments on grid holes), stop pins, V-block, on the plywood field
    fl, fw, fh = p["fence_seg"]
    fence = [box(-400 + fl / 2 + i * fl, 187.5, H + fh / 2, fl - 1, fw, fh) for i in range(2)]
    stops = [b.Pos(x, -12.5, H + p["stop_h"] / 2) * b.Cylinder(p["stop_d"] / 2, p["stop_h"]) for x in (-462.5, -137.5)]
    vl, vw, vh = p["vblock"]
    vb = box(-300, -150, H + vh / 2, vl, vw, vh) - b.Pos(-300, -150, H + vh) * b.Rot(45, 0, 0) * b.Box(vl + 4, vw * 0.83, vw * 0.83)
    out["fixtures"] = fuse(fence + stops + [vb])

    # 10 instrument post, 11 dial indicator
    PX, PY = x0 + s + 12.5, 237.5
    IX, IY = x0 + 150, wy
    az = H + p["arm_z"]
    pw, pd, ph = p["post"]
    fl_, fw_, ft_ = p["post_foot"]
    out["post"] = fuse([box(PX, PY, H + ft_ / 2, fl_, fw_, ft_), box(PX, PY, H + ft_ + ph / 2, pw, pd, ph),
                        rod((PX, PY, az), (IX, IY + 25, az), p["arm_d"] / 2), box(PX, PY, az, 36, 50, 40)])
    out["indicator"] = fuse([b.Pos(IX, IY, H + 135) * b.Rot(90, 0, 0) * b.Cylinder(28, 18),
                             rod((IX, IY, H + 40), (IX, IY, H + 107), 3),
                             rod((IX, IY + 9, H + 135), (IX, IY + 25, H + 135), 5),
                             rod((IX, IY + 25, H + 135), (IX, IY + 25, az), 6)])

    # 14 ballast slabs on the shelf
    ax_, ay_, az_ = p["slab"]
    zs = d["shelf_z"] + st + az_ / 2
    out["ballast"] = fuse([box(sx * (ax_ / 2 + p["slab_gap"] / 2), 0, zs, ax_, ay_, az_) for sx in (-1, 1)])

    # 15 wall anchor brackets (optional), steel angles on the back apron
    a1, a2, aw_, at = p["anchor"]
    yb = d["long_apron_y"] + aw / 2
    def angle(x):
        return (box(x, yb + at / 2, zu - a1 / 2, aw_, at, a1) + box(x, yb + a2 / 2, zu - at / 2, aw_, a2, at))
    out["anchor"] = fuse([angle(-400.0), angle(400.0)])

    # example workpiece (context only, not in the BOM)
    out["_workpiece"] = box(wx, wy, H + 20, 160, 100, 40)
    return out


def assembly(p=PARAMS, full_top_holes=False, with_workpiece=False):
    b = _b3d()
    parts = build_parts(p, full_top_holes)
    kids = [v for k, v in parts.items() if with_workpiece or not k.startswith("_")]
    return b.Compound(children=kids)


if __name__ == "__main__":
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    asm = assembly()
    for name, shape in (("gridbench-assembly", asm), ("precision-tile", parts["tile"]), ("worktop", parts["worktop"])):
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.5)
        print(f"exported {name}: volume {shape.volume / 1e6:.3f} L")
    t, i, pl = classify()
    tn, sn = insert_kinds()
    print(f"inserts: {len(tn)} tee nuts from the underside, {len(sn)} screw-in over frame members")
    print(f"grid: {len(t) + len(i) + len(pl)} positions ({len(t)} tile, {len(i)} inserts, {len(pl)} plain); "
          f"worktop exports a representative patch of {len(patch(pl)) + len(patch(i))} holes")
