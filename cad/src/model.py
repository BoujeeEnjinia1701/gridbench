"""GridBench parametric model (build123d), TRL 3, constructable design.

Revised 2026-10-01 under GBN-DDR-003 (design for construction, made under Amish's 2026-09-30
instruction to make the design physically buildable; open for his review): long aprons and low
rails butt between the legs on M8 bolts and cross dowels; the cross rail beside the right legs is
notched round them; the shelf is 5 mm shorter each end so it drops in; the tile pocket has 0.5 mm
clearance and corner relief holes; the tile is held by four M6 cap screws into screw-in inserts in
its two rails; the worktop is held by nine steel angle brackets; the feet screw into M10 T-nuts in
bored leg ends; every fixture screw sits on a threaded grid position; the instrument post, arm and
indicator have printed clamps that hold without passing through each other; the wall anchor angle
fixes under the rear apron and down the wall. Run `python cad/src/model.py --check` for the
constructability checks.

Revised 2026-09-25 under GBN-DDR-002 (recommendations accepted by Amish): 45 x 120 mm aprons,
flanged M6 tee nuts pressed in from the underside at every insert position with a clear underside,
screw-in inserts kept only where a frame member lies below, and rubber-padded levelling feet.

Run from the repo root:  python cad/src/model.py [--check]
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
    "post": (20.0, 40.0, 350.0), "post_foot": (74.0, 74.0, 12.0), "arm_d": 18.0, "arm_z": 300.0,
    # 15 wall anchor brackets (optional), steel angle: legs, width, thickness; under the rear apron
    "anchor": (50.0, 50.0, 40.0, 4.0), "anchor_x": (-400.0, 400.0),
    # ---- design for construction (GBN-DDR-003) ----
    # frame joints: M8 bolts through the leg into an M8 cross dowel (barrel nut) in the member end
    "bolt_d": 8.0, "bolt_len": 120.0, "dowel_nut": (10.0, 30.0), "dowel_nut_in": 40.0,
    "apron_bolt_z": (20.0, 80.0),        # long aprons: bolt heights up from the apron's lower edge
    "end_bolt_z": (50.0, 100.0),         # end aprons: staggered so the bolts miss each other in the leg
    "low_bolt_z": (20.0, 50.0),          # low rails
    "rail_screw": (6.0, 100.0), "rail_screw_z": (13.0, 56.0),   # cross rail ends: 6 x 100 screws, up from the rail's lower edge
    "rail_notch": (15.0, 25.0),          # notch in the ends of the cross rail beside the right legs (X, Y)
    "shelf_end_gap": 5.0,                # clearance each end between the shelf and the legs
    "pocket_gap": 0.5, "pocket_relief_d": 8.0,   # tile pocket clearance each side and corner relief holes
    # worktop fixing: steel angle brackets on the apron inner faces, screwed up into the worktop
    "bracket": (30.0, 30.0, 20.0, 3.0),  # vertical leg, horizontal leg, width, thickness
    "bracket_x": (-412.5, -162.5, 137.5, 387.5), "bracket_end_y": -12.5,
    # feet: M10 T-nut in a bored leg end
    "tnut": (24.0, 1.5, 12.0, 12.0), "leg_bore": (12.0, 60.0),   # flange d, flange t, barrel d, barrel len; bore d, depth
    # tile fixing: M6 screw-in inserts in the rails (through the packers), M6 x 20 cap screws
    "tile_screw_len": 20.0, "rail_insert_depth": 15.0,
    # fixtures on threaded grid positions (x, y); screws reach 18 mm below the worktop surface
    "clamps_at": (((312.5, 40.0), (312.5, 37.5), 90.0), ((432.0, -37.5), (437.5, -37.5), 0.0)),  # body, screw, rotation
    "fence_x": (-287.5, -87.5), "fence_y": 162.5, "fence_screw_dx": 50.0, "fixture_floor": 12.0,
    "vblock_at": (-312.5, -187.5), "vblock_screw_dx": 25.0,
    "stops_at": ((-462.5, -12.5), (-137.5, -12.5)), "stop_spigot": (6.3, 12.0),
    "post_at": (387.5, 187.5), "post_foot_screws": ((-25.0, -25.0), (25.0, 25.0)),
    "arm_offset": 25.0, "arm_clamp": (64.0, 50.0, 40.0), "end_clamp": (30.0, 50.0, 30.0),
    "drop_rod_d": 12.0, "indicator_at": (362.5, -40.0), "lug": 25.0,
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
    shelf = (low_rail_len - 2 * p["shelf_end_gap"], 2 * ly + p["rail"][0], p["shelf_t"])
    shelf_z = p["low_rail_z"] + p["rail"][1]          # underside of the shelf
    return dict(
        lx=lx, ly=ly, z_under=z_under, nx=nx, ny=ny,
        leg_h=z_under - p["foot_h"],
        long_apron_y=long_apron_y, end_apron_x=end_apron_x,
        long_apron_len=2 * lx - leg, end_apron_len=2 * ly - leg,   # both butt between the legs (GBN-DDR-003)
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


def fixture_holes(p=PARAMS):
    """Grid positions that the modelled fixtures screw or pin into (always drilled in the worktop)."""
    fy, dx = p["fence_y"], p["fence_screw_dx"]
    vx, vy = p["vblock_at"]
    px, py = p["post_at"]
    pts = [(x + s * dx, fy) for x in p["fence_x"] for s in (-1, 1)]
    pts += [(vx + s * p["vblock_screw_dx"], vy) for s in (-1, 1)]
    pts += [(px + a, py + b) for a, b in p["post_foot_screws"]]
    return pts, list(p["stops_at"])


def bracket_points(p=PARAMS):
    """Worktop brackets: (x, y, inward normal) on the long apron inner faces and the left end apron."""
    d = derived(p)
    yi = d["long_apron_y"] - p["apron"][0] / 2
    out = [(x, sy * yi, (0, -sy)) for x in p["bracket_x"] for sy in (-1, 1)]
    out.append((-(d["end_apron_x"] - p["apron"][0] / 2), p["bracket_end_y"], (1, 0)))
    return out


def arm_geometry(p=PARAMS):
    """Instrument post, arm clamp, arm, end clamp, drop rod and indicator positions."""
    H = p["h"]
    px, py = p["post_at"]
    az = H + p["arm_z"]
    ax = px - p["arm_offset"]
    ix, iy = p["indicator_at"]
    ry = iy + p["lug"]                        # drop rod axis
    ecw, ecd, ech = p["end_clamp"]
    yc = ry + 14.0                            # end clamp centre: drop rod bore 14 mm in front of it
    arm_end = yc - 2.0                        # the arm stops 2 mm past the clamp centre (blind bore)
    arm_back = py + p["arm_clamp"][1] / 2 + 10.0
    return dict(px=px, py=py, az=az, ax=ax, ix=ix, iy=iy, ry=ry, yc=yc, arm_end=arm_end, arm_back=arm_back,
                acx=(ax - 18.0 + px + 14.0) / 2)


def _cyl(x, y, z0, z1, r):
    b = _b3d()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def build_components(p=PARAMS, full_top_holes=False):
    """Every component as its own solid, keyed by name (GBN-DDR-003). Fasteners are grouped."""
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
    bd = p["bolt_d"]
    nd, nl = p["dowel_nut"]
    C = {}

    # ---------- legs, bored at the foot for the T-nut
    bore_d, bore_h = p["leg_bore"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            k = f"leg_{'r' if sx > 0 else 'l'}{'b' if sy > 0 else 'f'}"
            lg = box(sx * lx, sy * ly, p["foot_h"] + d["leg_h"] / 2, leg, leg, d["leg_h"])
            lg -= _cyl(sx * lx, sy * ly, p["foot_h"] - 1, p["foot_h"] + bore_h, bore_d / 2)
            # bolt holes through the leg
            for zz in p["apron_bolt_z"]:
                z = zu - ah + zz
                lg -= rod((sx * (lx + leg / 2 + 1), sy * d["long_apron_y"], z), (sx * (lx - leg / 2 - 1), sy * d["long_apron_y"], z), bd / 2 + 0.5)
            for zz in p["end_bolt_z"]:
                z = zu - ah + zz
                lg -= rod((sx * d["end_apron_x"], sy * (ly + leg / 2 + 1), z), (sx * d["end_apron_x"], sy * (ly - leg / 2 - 1), z), bd / 2 + 0.5)
            for zz in p["low_bolt_z"]:
                z = p["low_rail_z"] + zz
                lg -= rod((sx * (lx + leg / 2 + 1), sy * ly, z), (sx * (lx - leg / 2 - 1), sy * ly, z), bd / 2 + 0.5)
            C[k] = lg

    # ---------- members that butt between the legs, with bolt holes and cross dowel holes
    def member(cx, cy, cz, sx_, sy_, sz_, axis, zs, z_low, inner_sign):
        """axis: 'x' or 'y', the member's length direction. zs: bolt heights from z_low.
        inner_sign: +1/-1, the side (across the member) its cross dowel holes open toward."""
        m = box(cx, cy, cz, sx_, sy_, sz_)
        half = (sx_ if axis == "x" else sy_) / 2
        for e in (-1, 1):
            for zz in zs:
                z = z_low + zz
                if axis == "x":
                    end = cx + e * half
                    m -= rod((end + e, cy, z), (end - e * (p["dowel_nut_in"] + 12), cy, z), bd / 2 + 0.5)
                    xn = end - e * p["dowel_nut_in"]
                    yface = cy + inner_sign * sy_ / 2
                    m -= rod((xn, yface + inner_sign, z), (xn, yface - inner_sign * nl, z), nd / 2)
                else:
                    end = cy + e * half
                    m -= rod((cx, end + e, z), (cx, end - e * (p["dowel_nut_in"] + 12), z), bd / 2 + 0.5)
                    yn = end - e * p["dowel_nut_in"]
                    xface = cx + inner_sign * sx_ / 2
                    m -= rod((xface + inner_sign, yn, z), (xface - inner_sign * nl, yn, z), nd / 2)
        return m

    for sy in (-1, 1):
        C[f"apron_{'b' if sy > 0 else 'f'}"] = member(0, sy * d["long_apron_y"], zu - ah / 2, d["long_apron_len"], aw, ah,
                                                      "x", p["apron_bolt_z"], zu - ah, -sy)
        C[f"low_rail_{'b' if sy > 0 else 'f'}"] = member(0, sy * ly, p["low_rail_z"] + rh / 2, d["low_rail_len"], rw, rh,
                                                         "x", p["low_bolt_z"], p["low_rail_z"], -sy)
    for sx in (-1, 1):
        C[f"end_apron_{'r' if sx > 0 else 'l'}"] = member(sx * d["end_apron_x"], 0, zu - ah / 2, aw, d["end_apron_len"], ah,
                                                          "y", p["end_bolt_z"], zu - ah, -sx)

    # ---------- cross rails; the one beside the right legs is notched round them; tile rails drilled for inserts
    nx_, ny_ = p["rail_notch"]
    fx = fixing_points(p)
    rdep = p["rail_insert_depth"]
    pk = d["packer_t"]
    for n, x in enumerate(p["cross_x"], 1):
        r = box(x, 0, zu - rh / 2, rw, d["rail_len"], rh)
        if x + rw / 2 > lx - leg / 2:
            for sy in (-1, 1):
                r -= box(lx - leg / 2 + nx_ / 2 + 0.0, sy * (d["rail_len"] / 2 - ny_ / 2), zu - rh / 2, nx_ + 0.0, ny_ + 0.02, rh + 2)
        for fxp, fyp in fx:
            if abs(fxp - x) < rw / 2:
                r -= _cyl(fxp, fyp, zu + pk - rdep, zu + 1, p["insert_hole_d"] / 2)
        C[f"rail_{n}"] = r
    # packers under the tile, on the two tile rails, drilled for the inserts
    for n, x in enumerate([x for x in p["cross_x"] if x0 < x < x0 + s], 1):
        pkr = box(x, tcy, zu + pk / 2, rw, s, pk)
        for fxp, fyp in fx:
            if abs(fxp - x) < rw / 2:
                pkr -= _cyl(fxp, fyp, zu - 1, zu + pk + 1, p["insert_hole_d"] / 2)
        C[f"packer_{n}"] = pkr

    # ---------- frame bolts, cross dowels and rail screws
    bolts = []
    def bolt_x(xo, xi, y, z, sgn):
        # head outside the leg at xo, shank to xi
        return (rod((xo + sgn * 6.5, y, z), (xo, y, z), 6.5) + rod((xo, y, z), (xi, y, z), bd / 2))
    def bolt_y(x, yo, yi, z, sgn):
        return (rod((x, yo + sgn * 6.5, z), (x, yo, z), 6.5) + rod((x, yo, z), (x, yi, z), bd / 2))
    for sx in (-1, 1):
        for sy in (-1, 1):
            xo = sx * (lx + leg / 2)
            for zz in p["apron_bolt_z"]:
                z = zu - ah + zz
                xi = sx * (lx - leg / 2 - p["bolt_len"] + leg)
                bolts.append(bolt_x(xo, xi, sy * d["long_apron_y"], z, sx))
                xn = sx * (lx - leg / 2 - p["dowel_nut_in"])
                bolts.append(rod((xn, sy * (d["long_apron_y"] - aw / 2) , z), (xn, sy * (d["long_apron_y"] - aw / 2 + nl), z), nd / 2 - 0.5))
            for zz in p["low_bolt_z"]:
                z = p["low_rail_z"] + zz
                xi = sx * (lx - leg / 2 - p["bolt_len"] + leg)
                bolts.append(bolt_x(xo, xi, sy * ly, z, sx))
                xn = sx * (lx - leg / 2 - p["dowel_nut_in"])
                bolts.append(rod((xn, sy * (ly - rw / 2), z), (xn, sy * (ly - rw / 2 + nl), z), nd / 2 - 0.5))
            yo = sy * (ly + leg / 2)
            for zz in p["end_bolt_z"]:
                z = zu - ah + zz
                yi = sy * (ly - leg / 2 - p["bolt_len"] + leg)
                bolts.append(bolt_y(sx * d["end_apron_x"], yo, yi, z, sy))
                yn = sy * (ly - leg / 2 - p["dowel_nut_in"])
                xf = sx * (d["end_apron_x"] - aw / 2)
                bolts.append(rod((xf, yn, z), (xf + sx * nl, yn, z), nd / 2 - 0.5))
    C["frame_bolts"] = fuse(bolts)
    rs_d, rs_l = p["rail_screw"]
    screws = []
    for x in p["cross_x"]:
        xs = x if x + rw / 2 <= lx - leg / 2 else (x - rw / 2 + (lx - leg / 2)) / 2
        for sy in (-1, 1):
            yo = sy * (d["long_apron_y"] + aw / 2)
            for zz in p["rail_screw_z"]:
                z = zu - rh + zz
                screws.append(rod((xs, yo + sy * 1.5, z), (xs, yo, z), 5.5) + rod((xs, yo, z), (xs, yo - sy * rs_l, z), rs_d / 2 - 0.6))
    C["rail_screws"] = fuse(screws)

    # ---------- levelling feet and T-nuts
    rt = p["rubber_t"]
    tf_d, tf_t, tb_d, tb_l = p["tnut"]
    feet, tnuts = [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * lx, sy * ly
            feet.append(_cyl(x, y, 0, rt, p["foot_pad_d"] / 2 - 1) + _cyl(x, y, rt, p["foot_pad_t"], p["foot_pad_d"] / 2)
                        + _cyl(x, y, p["foot_pad_t"], p["foot_h"] + 50, 5.0))
            tnuts.append((_cyl(x, y, p["foot_h"] - tf_t, p["foot_h"], tf_d / 2) + _cyl(x, y, p["foot_h"], p["foot_h"] + tb_l, tb_d / 2))
                         - _cyl(x, y, p["foot_h"] - tf_t - 1, p["foot_h"] + tb_l + 1, 5.0))
    C["feet"] = fuse(feet)
    C["tnuts"] = fuse(tnuts)

    # ---------- shelf
    sl, sd, st = d["shelf"]
    C["shelf"] = box(0, 0, d["shelf_z"] + st / 2, sl, sd, st)

    # ---------- worktop: through pocket with clearance and corner relief, grid holes
    g = p["pocket_gap"]
    top = box(0, 0, H - p["top_t"] / 2, L, D, p["top_t"]) - box(tcx, tcy, H - p["top_t"] / 2, s + 2 * g, s + 2 * g, p["top_t"] + 2)
    rr = p["pocket_relief_d"] / 2
    for cx_ in (x0 - g, x0 + s + g):
        for cy_ in (y0 - g, y0 + s + g):
            top -= _cyl(cx_, cy_, zu - 1, H + 1, rr)
    fix_screw_pts, stop_pts = fixture_holes(p)
    used = set(fix_screw_pts) | set(stop_pts)
    tee_pts, screw_pts = insert_kinds(p)
    def sel(pts):
        return pts if full_top_holes else sorted(set(patch(pts, p)) | (set(pts) & used))
    pl, tp, sp = sel(plain_pts), sel(tee_pts), sel(screw_pts)
    top = drilled(top, pl, H + 1, p["plain_d"], p["top_t"] + 2)
    top = drilled(top, sp, H + 1, p["insert_hole_d"], p["top_t"] + 2)
    top = drilled(top, tp, H + 1, p["tee_hole_d"], p["top_t"] + 2)
    C["worktop"] = top
    screw_in = [_cyl(x, y, H - p["insert_len"], H, p["insert_hole_d"] / 2) - _cyl(x, y, H - p["insert_len"] - 1, H + 1, 2.5) for x, y in sp]
    tee = [(_cyl(x, y, zu - p["tee_flange_t"], zu, p["tee_flange_d"] / 2) + _cyl(x, y, zu, zu + p["tee_barrel_len"], p["tee_hole_d"] / 2))
           - _cyl(x, y, zu - 3, zu + p["tee_barrel_len"] + 1, 2.5) for x, y in tp]
    C["tee_nuts"] = fuse(tee)
    C["screw_inserts"] = fuse(screw_in)

    # ---------- worktop brackets (steel angle), screwed to the apron and up into the worktop
    bv, bh, bw, bt = p["bracket"]
    brs, brscrews = [], []
    for x, y, (nxn, nyn) in bracket_points(p):
        if nyn != 0:
            sg = nyn
            vert = box(x, y + sg * bt / 2, zu - bv / 2, bw, bt, bv)
            hor = box(x, y + sg * bh / 2, zu - bt / 2, bw, bh, bt)
            brs.append(vert + hor)
            brscrews.append(_cyl(x, y + sg * (bh - 10), zu - bt - 2, zu + 14, 2.0))
            brscrews.append(rod((x, y + sg * (bt + 2), zu - bv + 12), (x, y - sg * 22, zu - bv + 12), 2.0))
        else:
            sg = nxn
            vert = box(x + sg * bt / 2, y, zu - bv / 2, bt, bw, bv)
            hor = box(x + sg * bh / 2, y, zu - bt / 2, bh, bw, bt)
            brs.append(vert + hor)
            brscrews.append(_cyl(x + sg * (bh - 10), y, zu - bt - 2, zu + 14, 2.0))
            brscrews.append(rod((x + sg * (bt + 2), y, zu - bv + 12), (x - sg * 22, y, zu - bv + 12), 2.0))
    C["brackets"] = fuse(brs)
    C["bracket_screws"] = fuse(brscrews)

    # ---------- precision tile, rail inserts and tile screws
    tile = box(tcx, tcy, H - tt / 2, s, s, tt)
    tile = drilled(tile, tile_pts, H + 1, p["tap_drill_d"], tt + 2)
    tile = drilled(tile, dowel_points(p), H + 1, p["dowel_d"], tt + 2)
    tile = drilled(tile, fx, H + 1, p["fix_hole_d"], tt + 2)
    tile = drilled(tile, fx, H + 0.01, p["cbore_d"], p["cbore_depth"])
    C["tile"] = tile
    zt = H - tt                                                  # tile underside = packer top
    C["rail_inserts"] = fuse([_cyl(x, y, zt - p["insert_len"], zt, p["insert_hole_d"] / 2) - _cyl(x, y, zt - p["insert_len"] - 1, zt + 1, 2.5)
                              for x, y in fx])
    zc = H + 0.01 - p["cbore_depth"]                            # counterbore floor
    C["tile_screws"] = fuse([_cyl(x, y, zc, zc + 6.0, 5.0) + _cyl(x, y, zc - p["tile_screw_len"], zc, 2.5) for x, y in fx])

    # ---------- pins
    dp = dowel_points(p)
    r = p["dowel_d"] / 2
    pin_z = H + p["pin_len"] / 2 - 6
    C["pins"] = b.Pos(dp[0][0], dp[0][1], pin_z) * b.Cylinder(r, p["pin_len"])
    dia = b.Cylinder(r, p["pin_len"]) & b.Box(p["dowel_d"], 3.0, p["pin_len"] + 1)
    C["diamond"] = b.Pos(dp[3][0], dp[3][1], pin_z) * dia

    # ---------- printed toe clamps on threaded tile holes, M6 x 80 screws with printed knobs
    cl, cw, ct = p["clamp"]
    z0 = 40.0                                                    # height of the example workpiece
    bodies, cscrews = [], []
    for (bx, by), (sx_, sy_), ang in p["clamps_at"]:
        body = box(0, 0, z0 + ct / 2, cl, cw, ct) - box(-cl * 0.1, 0, z0 + ct / 2, cl * 0.45, p["clamp_slot"], ct + 2)
        heel = box(cl / 2 - 7, 0, z0 / 2, 14, cw, z0)
        bodies.append(b.Pos(bx, by, H) * b.Rot(0, 0, ang) * (body + heel))
        top_z = H + z0 + ct
        cscrews.append(_cyl(sx_, sy_, H - 12, top_z, 2.5) + _cyl(sx_, sy_, top_z, top_z + 12, 10.0))
    C["clamps"] = fuse(bodies)
    C["clamp_screws"] = fuse(cscrews)

    # ---------- fence segments, stop pins, V-block, each on threaded grid positions
    fl, fw, fh = p["fence_seg"]
    ff = p["fixture_floor"]
    fy, fdx = p["fence_y"], p["fence_screw_dx"]
    segs, fscrews = [], []
    for xc in p["fence_x"]:
        sg = box(xc, fy, H + fh / 2, fl, fw, fh)
        for e in (-1, 1):
            sg -= _cyl(xc + e * fdx, fy, H - 1, H + fh + 1, p["plain_d"] / 2)
            sg -= _cyl(xc + e * fdx, fy, H + ff, H + fh + 1, p["cbore_d"] / 2)
            fscrews.append(_cyl(xc + e * fdx, fy, H + ff, H + ff + 6, 5.0) + _cyl(xc + e * fdx, fy, H + ff - 30 , H + ff, 2.5))
        segs.append(sg)
    C["fence"] = fuse(segs)
    sd_, sl_ = p["stop_spigot"]
    C["stops"] = fuse([_cyl(x, y, H, H + p["stop_h"], p["stop_d"] / 2) + _cyl(x, y, H - sl_, H, sd_ / 2) for x, y in p["stops_at"]])
    vl, vw, vh = p["vblock"]
    vx, vy = p["vblock_at"]
    vtop = vw - 10.0                                              # V 50 mm wide at the top, 5 mm lands each side
    vb = box(vx, vy, H + vh / 2, vl, vw, vh) - b.Pos(vx, vy, H + vh) * b.Rot(45, 0, 0) * b.Box(vl + 4, vtop / math.sqrt(2), vtop / math.sqrt(2))
    for e in (-1, 1):
        xs = vx + e * p["vblock_screw_dx"]
        vb -= _cyl(xs, vy, H - 1, H + vh, p["plain_d"] / 2)
        vb -= _cyl(xs, vy, H + ff, H + vh, p["cbore_d"] / 2)
        fscrews.append(_cyl(xs, vy, H + ff, H + ff + 6, 5.0) + _cyl(xs, vy, H + ff - 30, H + ff, 2.5))
    C["vblock"] = vb
    C["fixture_screws"] = fuse(fscrews)

    # ---------- instrument post: printed foot, extrusion, printed arm clamp, arm, end clamp, drop rod
    A = arm_geometry(p)
    px, py, az = A["px"], A["py"], A["az"]
    pw, pd, ph = p["post"]
    flx, fly, flt = p["post_foot"]
    foot = box(px, py, H + flt / 2, flx, fly, flt)
    pscrews = []
    for a, c in p["post_foot_screws"]:
        foot -= _cyl(px + a, py + c, H - 1, H + flt + 1, p["plain_d"] / 2)
        pscrews.append(_cyl(px + a, py + c, H + flt, H + flt + 6, 5.0) + _cyl(px + a, py + c, H + flt - 30, H + flt, 2.5))
    for e in (-1, 1):                                              # M5 screws up into the extrusion's core holes
        foot -= _cyl(px, py + e * 10, H - 1, H + 5, 4.5)
        foot -= _cyl(px, py + e * 10, H - 1, H + flt + 1, 2.75)
        pscrews.append(_cyl(px, py + e * 10, H + 0.5, H + 5, 4.25) + _cyl(px, py + e * 10, H + 5, H + flt + 13, 2.1))
    C["post_foot"] = foot
    ext = box(px, py, H + flt + ph / 2, pw, pd, ph)
    for e in (-1, 1):
        ext -= _cyl(px, py + e * 10, H + flt - 1, H + flt + ph + 1, 2.1)
    C["post"] = ext
    C["post_screws"] = fuse(pscrews)
    cw_, cd_, ch_ = p["arm_clamp"]
    acx = (A["ax"] - p["arm_d"] / 2 - 9.0 + px + pw / 2 + 7.0) / 2
    clamp1 = box(acx, py, az, cw_, cd_, ch_) - box(px, py, az, pw + 0.4, pd + 0.4, ch_ + 2)
    clamp1 -= rod((A["ax"], py + cd_, az), (A["ax"], py - cd_, az), p["arm_d"] / 2 + 0.2)
    ecw, ecd, ech = p["end_clamp"]
    clamp2 = box(A["ax"], A["yc"], az, ecw, ecd, ech)
    clamp2 -= rod((A["ax"], A["yc"] + ecd, az), (A["ax"], A["arm_end"], az), p["arm_d"] / 2 + 0.2)
    clamp2 -= _cyl(A["ax"], A["ry"], az - ech, az + ech, p["drop_rod_d"] / 2 + 0.2)
    C["arm_clamps"] = clamp1 + clamp2
    C["arm"] = rod((A["ax"], A["arm_back"], az), (A["ax"], A["arm_end"], az), p["arm_d"] / 2)
    ix, iy, ry = A["ix"], A["iy"], A["ry"]
    lug_z = H + 135
    C["drop_rod"] = rod((ix, ry, lug_z + 6), (ix, ry, az + ech / 2 + 10), p["drop_rod_d"] / 2)
    C["indicator"] = fuse([b.Pos(ix, iy, lug_z) * b.Rot(90, 0, 0) * b.Cylinder(28, 18),
                           rod((ix, iy, H + 40), (ix, iy, lug_z - 28), 4),
                           rod((ix, iy + 9, lug_z), (ix, ry - p["drop_rod_d"] / 2, lug_z), 5),
                           box(ix, ry, lug_z, 10, p["drop_rod_d"], 12)])

    # ---------- ballast slabs on the shelf
    ax_, ay_, az_ = p["slab"]
    zs = d["shelf_z"] + st + az_ / 2
    C["ballast"] = fuse([box(sx * (ax_ / 2 + p["slab_gap"] / 2), 0, zs, ax_, ay_, az_) for sx in (-1, 1)])

    # ---------- wall anchor brackets (optional): flat leg under the rear apron, other leg down the wall
    a1, a2, aw_, at = p["anchor"]
    yw = D / 2                                                   # the wall, at the worktop's rear edge
    zb = zu - ah                                                 # underside of the rear apron
    anc = []
    for x in p["anchor_x"]:
        anc.append(box(x, yw - a2 / 2, zb - at / 2, aw_, a2, at) + box(x, yw - at / 2, zb - a1 / 2, aw_, at, a1))
    C["anchor"] = fuse(anc)

    # example workpiece (context only, not in the BOM)
    C["_workpiece"] = box(x0 + 100, -40.0, H + 20, 160, 100, 40)
    return C


GROUPS = {   # old build_parts keys (BOM lines) to component keys, for the concept media and drawings
    "frame": ["leg_lf", "leg_lb", "leg_rf", "leg_rb", "apron_f", "apron_b", "end_apron_l", "end_apron_r",
              "rail_1", "rail_2", "rail_3", "rail_4", "low_rail_f", "low_rail_b", "packer_1", "packer_2",
              "frame_bolts", "rail_screws", "brackets", "bracket_screws"],
    "feet": ["feet", "tnuts"], "shelf": ["shelf"], "worktop": ["worktop"],
    "inserts": ["tee_nuts", "screw_inserts", "rail_inserts"], "tile": ["tile", "tile_screws"],
    "pins": ["pins"], "diamond": ["diamond"], "clamps": ["clamps", "clamp_screws"],
    "fixtures": ["fence", "stops", "vblock", "fixture_screws"],
    "post": ["post_foot", "post", "post_screws", "arm_clamps", "arm"], "indicator": ["indicator", "drop_rod"],
    "ballast": ["ballast"], "anchor": ["anchor"], "_workpiece": ["_workpiece"],
}


def build_parts(p=PARAMS, full_top_holes=False):
    """Return {key: solid} for the BOM lines that have geometry (1 to 11, 13 to 15), each the fusion
    of its components from build_components()."""
    b = _b3d()
    C = build_components(p, full_top_holes)
    return {k: b.Compound(children=[C[c] for c in v]) for k, v in GROUPS.items()}


def assembly(p=PARAMS, full_top_holes=False, with_workpiece=False):
    b = _b3d()
    C = build_components(p, full_top_holes)
    kids = [v for k, v in C.items() if with_workpiece or not k.startswith("_")]
    return b.Compound(children=kids)


# ----------------------------------------------------------------- constructability checks
def checks(p=PARAMS):
    """(name, kind, a, b, limit): kind 'apart' needs a clearance of at least limit mm and no overlap;
    'touch' needs the two to meet (distance under 0.05 mm) without overlapping more than limit mm3."""
    C = build_components(p)
    legs = ["leg_lf", "leg_lb", "leg_rf", "leg_rb"]
    out = []
    for m in ("apron_f", "apron_b", "end_apron_l", "end_apron_r", "low_rail_f", "low_rail_b"):
        for lg in legs:
            out.append((f"{m} / {lg}", "nolap", m, lg, 1.0))
        out.append((f"{m} touches a leg", "touch_any", m, legs, 1.0))
    for n in (1, 2, 3, 4):
        out.append((f"rail_{n} touches the aprons", "touch_any", f"rail_{n}", ["apron_f", "apron_b"], 1.0))
        for lg in legs + ["end_apron_l", "end_apron_r"]:
            out.append((f"rail_{n} / {lg}", "nolap", f"rail_{n}", lg, 1.0))
    for n, rail in ((1, "rail_3"), (2, "rail_4")):
        out += [(f"packer_{n} on {rail}", "touch", f"packer_{n}", rail, 1.0),
                (f"tile on packer_{n}", "touch", "tile", f"packer_{n}", 1.0)]
    out += [("shelf on the low rails", "touch_any", "shelf", ["low_rail_f", "low_rail_b"], 1.0),
            ("ballast on the shelf", "touch", "ballast", "shelf", 1.0),
            ("worktop on the aprons", "touch_any", "worktop", ["apron_f", "apron_b", "end_apron_l", "end_apron_r"], 1.0),
            ("tile clear of the worktop pocket", "apart", "tile", "worktop", 0.4),
            ("feet clear of the legs (thread in the T-nut)", "apart", "feet", legs, 0.5),
            ("T-nuts seat on the leg ends", "touch_any", "tnuts", legs, 1.0),
            ("brackets on the aprons", "touch_any", "brackets", ["apron_f", "apron_b", "end_apron_l"], 1.0),
            ("brackets under the worktop", "touch", "brackets", "worktop", 1.0),
            ("brackets clear of the tee nuts", "apart", "brackets", "tee_nuts", 2.0),
            ("brackets clear of the cross rails", "apart", "brackets", ["rail_1", "rail_2", "rail_3", "rail_4"], 2.0),
            ("tee nuts clear of the frame", "apart", "tee_nuts", legs + ["apron_f", "apron_b", "end_apron_l", "end_apron_r", "rail_1", "rail_2", "rail_3", "rail_4"], 0.0),
            ("rail inserts in the packers and rails", "nolap", "rail_inserts", ["packer_1", "packer_2", "rail_3", "rail_4"], 1.0),
            ("tile screws clear of the tile bores", "nolap", "tile_screws", "tile", 1.0),
            ("clamp screws in tile holes", "nolap", "clamp_screws", "tile", 1.0),
            ("clamps clear of the tile except the heels", "nolap", "clamps", "tile", 1.0),
            ("fence, stops and V-block on the worktop", "touch_any", "fence", ["worktop"], 1.0),
            ("fixture screws in their holes", "nolap", "fixture_screws", ["worktop", "fence", "vblock"], 1.0),
            ("stops in plain holes", "nolap", "stops", "worktop", 1.0),
            ("post foot on the worktop", "touch", "post_foot", "worktop", 1.0),
            ("post foot clear of the tile", "apart", "post_foot", "tile", 0.0),
            ("post on its foot", "touch", "post", "post_foot", 1.0),
            ("arm clear of the post", "apart", "arm", "post", 2.0),
            ("arm clamps on the post and arm (no overlap)", "nolap", "arm_clamps", ["post", "arm", "drop_rod"], 1.0),
            ("drop rod clear of the arm", "apart", "drop_rod", "arm", 2.0),
            ("indicator clear of the clamps", "apart", "indicator", ["clamps", "clamp_screws"], 2.0),
            ("indicator stem on the workpiece", "touch", "indicator", "_workpiece", 1.0),
            ("anchor under the rear apron", "touch", "anchor", "apron_b", 1.0),
            ("anchor clear of the legs and worktop", "apart", "anchor", legs + ["worktop"], 0.0),
            ("frame bolts in their holes", "nolap", "frame_bolts", legs + ["apron_f", "apron_b", "end_apron_l", "end_apron_r", "low_rail_f", "low_rail_b"], 1.0),
            ("rail screws in the rails and aprons", "nolap", "rail_screws", legs + ["frame_bolts"], 1.0),
            ]
    return C, out


def run_checks(p=PARAMS, verbose=True):
    b = _b3d()
    C, rules = checks(p)
    def shapes(k):
        return [C[x] for x in (k if isinstance(k, (list, tuple)) else [k])]
    def lap(a, c):
        try:
            return (a & c).volume
        except Exception:
            return 0.0
    def dist(a, c):
        try:
            return a.distance_to(c)
        except Exception:
            return float("nan")
    fails = 0
    for name, kind, ka, kb, lim in rules:
        A = C[ka]
        Bs = shapes(kb)
        ov = sum(lap(A, x) for x in Bs)
        ds = [dist(A, x) for x in Bs]
        dmin = min(ds)
        if kind == "nolap":
            ok = ov <= lim
            txt = f"overlap {ov:.1f} mm3"
        elif kind == "apart":
            ok = ov <= 1e-3 and dmin >= lim - 1e-6
            txt = f"clearance {dmin:.2f} mm (need {lim:g})"
        elif kind == "touch":
            ok = ov <= lim and dmin < 0.05
            txt = f"gap {dmin:.2f} mm, overlap {ov:.1f} mm3"
        else:  # touch_any
            ok = ov <= lim * len(Bs) and dmin < 0.05
            txt = f"nearest gap {dmin:.2f} mm, overlap {ov:.1f} mm3"
        fails += not ok
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {txt}")
    print(f"{len(rules) - fails} of {len(rules)} checks pass")
    return fails


if __name__ == "__main__":
    import sys
    if "--check" in sys.argv:
        raise SystemExit(1 if run_checks() else 0)
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    asm = assembly()
    import build123d as _b
    for name, shape in (("gridbench-assembly", asm), ("precision-tile", C["tile"]), ("worktop", C["worktop"])):
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.5)
        print(f"exported {name}: volume {shape.volume / 1e6:.3f} L")
    t, i, pl = classify()
    tn, sn = insert_kinds()
    print(f"inserts: {len(tn)} tee nuts from the underside, {len(sn)} screw-in over frame members")
    print(f"grid: {len(t) + len(i) + len(pl)} positions ({len(t)} tile, {len(i)} inserts, {len(pl)} plain); "
          f"worktop exports a representative patch plus the holes the fixtures use")
