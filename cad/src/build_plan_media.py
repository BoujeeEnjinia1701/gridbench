"""GridBench prototype build plan pictures (GBN-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|layouts|sheets|joints|steps ...]
A single sheet, joint or step can be drawn alone, for example `sheets 105` or `joints 3` or `steps 9`,
which keeps the memory use of one process small. With no argument it draws everything.
Every picture is drawn from cad/src/model.py (build_components), so the pictures and the model
never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    docs/05-build-plan/worktop-holes.png   every hole in the worktop, by kind
    cad/drawings/GBN-DWG-101 to 116        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import (PARAMS as P, build_components, derived, classify, insert_kinds, fixing_points,  # noqa: E402
                   dowel_points, arm_geometry, bracket_points, fixture_holes)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
H = P["h"]
_C = {}


def C(k):
    if not _C:
        _C.update(build_components(P))
    return _C[k]


_MK = {}


def marks(kind):
    """Light stand-ins for every grid hole and insert (thin octagonal disks), so the pictures show the
    full grid without cutting 1,008 holes: 'plain' (dark, on the surface), 'tee' (tee nut flanges under
    the worktop) and 'screw' (screw-in inserts, flush in the surface)."""
    if kind not in _MK:
        from build123d import Compound, Pos, RegularPolygon, extrude
        tile, ins, plain = classify(P)
        tee, scr = insert_kinds(P)
        zu = D["z_under"]
        disk = lambda r, h: extrude(RegularPolygon(r, 8), amount=h)  # noqa: E731
        if kind == "plain":
            _MK[kind] = Compound(children=[Pos(x, y, H) * disk(P["plain_d"] / 2, 0.6) for x, y in plain])
        elif kind == "tee":
            _MK[kind] = Compound(children=[Pos(x, y, zu - P["tee_flange_t"]) * disk(P["tee_flange_d"] / 2, P["tee_flange_t"]) for x, y in tee])
        else:
            _MK[kind] = Compound(children=[Pos(x, y, H) * disk(P["insert_od"] / 2, 0.6) for x, y in scr])
    return _MK[kind]


def S(*ks):
    out = None
    for k in ks:
        out = C(k) if out is None else out + C(k)
    return out


COL = {"leg": "#B07A3B", "end_apron": "#C8955A", "apron": "#D2A46B", "low_rail": "#A26C33", "rail": "#C08A4E",
       "packer": "#7C4A1E", "bolt": "#111827", "shelf": "#E6CF9E", "worktop": "#E2C48E", "tee": "#C9A227",
       "bracket": "#475569", "tile": "#94A3B8", "pins": "#1F2937", "clamp": "#0F766E", "fixture": "#14B8A6",
       "post": "#475569", "pfoot": "#0D9488", "aclamp": "#0E7490", "arm": "#6B7280", "indicator": "#1D4ED8",
       "ballast": "#A8A29E", "feet": "#374151", "anchor": "#57534E", "work": "#CBD5E1"}


def _fuse(shapes):
    from build123d import Compound
    return Compound(children=list(shapes))


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


LEGS = ("leg_lf", "leg_lb", "leg_rf", "leg_rb")
RAILS = ("rail_1", "rail_2", "rail_3", "rail_4")


def made():
    return {
        "legs": part("Legs (4)", S(*LEGS), COL["leg"]),
        "feet": part("Levelling feet and M10 T-nuts (4)", S("feet", "tnuts"), COL["feet"]),
        "end_aprons": part("End aprons (2)", S("end_apron_l", "end_apron_r"), COL["end_apron"]),
        "aprons": part("Long aprons (2)", S("apron_f", "apron_b"), COL["apron"]),
        "low_rails": part("Low rails (2)", S("low_rail_f", "low_rail_b"), COL["low_rail"]),
        "bolts": part("M8 bolts and cross dowels (24)", C("frame_bolts"), COL["bolt"]),
        "rails": part("Cross rails (4) and their screws", S(*RAILS, "rail_screws"), COL["rail"]),
        "packers": part("Packers under the tile (2)", S("packer_1", "packer_2"), COL["packer"]),
        "shelf": part("Shelf", C("shelf"), COL["shelf"]),
        "worktop": part("Worktop", C("worktop"), COL["worktop"]),
        "inserts": part("Tee nuts and screw-in inserts", _fuse([marks("tee"), marks("screw")]), COL["tee"]),
        "brackets": part("Worktop brackets (9)", S("brackets", "bracket_screws"), COL["bracket"]),
        "tile": part("Precision tile, rail inserts and screws", S("tile", "rail_inserts", "tile_screws"), COL["tile"]),
        "ballast": part("Ballast slabs (2)", C("ballast"), COL["ballast"]),
        "pins": part("Round and diamond pins", S("pins", "diamond"), COL["pins"]),
        "clamps": part("Toe clamps (2 shown)", S("clamps", "clamp_screws"), COL["clamp"]),
        "fixtures": part("Fence, stop pins and V-block", S("fence", "stops", "vblock", "fixture_screws"), COL["fixture"]),
        "post": part("Instrument post, foot, arm and clamps", S("post_foot", "post", "post_screws", "arm_clamps", "arm"), COL["post"]),
        "indicator": part("Dial indicator on its drop rod", S("indicator", "drop_rod"), COL["indicator"]),
        "anchor": part("Wall anchor angles (optional)", C("anchor"), COL["anchor"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"legs": (0, 0, 0), "feet": (0, 0, -170), "end_aprons": (0, 0, 220), "aprons": (0, -150, 220),
           "low_rails": (0, -150, 0), "bolts": (0, -330, 120), "rails": (0, 0, 420), "packers": (0, 0, 540),
           "shelf": (0, -520, 0), "worktop": (0, 0, 760), "inserts": (0, 0, 640), "brackets": (0, 0, 330),
           "tile": (0, 0, 920), "ballast": (0, -560, -330), "pins": (0, 0, 1080), "clamps": (0, 0, 1180),
           "fixtures": (0, 0, 1050), "post": (0, 0, 1200), "indicator": (0, 0, 1300), "anchor": (600, 350, 0)}
    from build123d import Compound
    one = [x for x in C("anchor").solids() if x.bounding_box().center().X > 0]
    M["anchor"] = part("Wall anchor angles (optional; one of two shown)", Compound(children=one), COL["anchor"])
    parts = []
    for k, p in M.items():
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "GridBench prototype: every component, pulled apart",
                       subtitle="Numbered in build order; 20, the wall anchor, is optional. Seen from the front right and above",
                       elev=20, azim=-55, size=(12, 10), dpi=150, key=True)


# ----------------------------------------------------------------- worktop hole layout
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    tile, ins, plain = classify(P)
    tee, scr = insert_kinds(P)
    L, Dp = P["top_l"], P["top_d"]
    X = lambda x: x + L / 2  # noqa: E731
    Y = lambda y: y + Dp / 2  # noqa: E731
    fig = plt.figure(figsize=(13, 8.6), dpi=150)
    ax = fig.add_axes([0.04, 0.12, 0.92, 0.74]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), L, Dp, fc="#F5EBDD", ec=INK, lw=1.2))
    x0, y0, s, g = P["tile_x0"], P["tile_y0"], P["tile"], P["pocket_gap"]
    ax.add_patch(Rectangle((X(x0 - g), Y(y0 - g)), s + 2 * g, s + 2 * g, fc="white", ec=INK, lw=1.0))
    for cx in (x0 - g, x0 + s + g):
        for cy in (y0 - g, y0 + s + g):
            ax.add_patch(plt.Circle((X(cx), Y(cy)), P["pocket_relief_d"] / 2, fc="white", ec=INK, lw=0.8))
    ax.text(X(x0 + s / 2), Y(y0 + s / 2), "Pocket for the tile\n301 x 301, cut right through\n8 mm relief hole at each corner\n\n824.5 to 1,125.5 from the left edge\n149.5 to 450.5 from the front edge",
            ha="center", va="center", fontsize=8.5, color=MUT)
    for x, y in plain:
        ax.add_patch(plt.Circle((X(x), Y(y)), 3.3, fc="white", ec="#6B7280", lw=0.4))
    for x, y in tee:
        ax.add_patch(plt.Circle((X(x), Y(y)), 4.0, fc=AC, ec=AC, lw=0.4))
    for x, y in scr:
        ax.add_patch(plt.Circle((X(x), Y(y)), 4.25, fc="#C2410C", ec="#C2410C", lw=0.4))
    for k, v in enumerate((12.5, 112.5, 212.5, 412.5, 612.5, 812.5, 1012.5, 1187.5)):
        ax.text(v, -14, f"{v:g}", ha="center", va="top", fontsize=7.5, color=AC)
        ax.plot([v, v], [-3, -11], color=AC, lw=0.5)
    for v in (12.5, 112.5, 212.5, 312.5, 412.5, 512.5, 587.5):
        ax.text(-8, v, f"{v:g}", ha="right", va="center", fontsize=7.5, color=AC)
        ax.plot([-1, -6], [v, v], color=AC, lw=0.5)
    ax.text(L / 2, -36, "from the left edge, mm (holes every 25 mm)", ha="center", va="top", fontsize=8.5, color=MUT)
    ax.text(-56, Dp / 2, "from the front edge, mm", rotation=90, ha="center", va="center", fontsize=8.5, color=MUT)
    ax.set_xlim(-70, L + 10); ax.set_ylim(-48, Dp + 10)
    fig.text(0.03, 0.965, "Worktop: every hole, seen from above", fontsize=14, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Front edge at the bottom. Hole centres are 12.5 mm in from each edge, then every 25 mm both ways. "
             "Every second hole in both directions (the 50 mm sub-grid) is threaded.", fontsize=9, color=MUT, va="top")
    ky = 0.075
    for i, (c, ec, t) in enumerate((("white", "#6B7280", f"Plain hole 6.6 mm, for pins and stops ({len(plain)})"),
                                     (AC, AC, f"8.0 mm hole for a tee nut pressed in from below ({len(tee)})"),
                                     ("#C2410C", "#C2410C", f"8.5 mm hole for a screw-in insert, over the frame ({len(scr)})"))):
        xk = 0.05 + i * 0.31
        fig.patches.append(plt.Circle((xk, ky), 0.006, transform=fig.transFigure, fc=c, ec=ec, lw=0.8))
        fig.text(xk + 0.012, ky, t, fontsize=8.5, color=INK, va="center")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/gridbench", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "worktop-holes.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


# ----------------------------------------------------------------- making sketches
def flat(shape, origin, x_dir, z_dir):
    import build123d as b
    return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_local_coords(shape)


def at_origin(shape):
    import build123d as b
    c = shape.bounding_box().center()
    return b.Pos(-c.X, -c.Y, -c.Z) * shape


def _near(key, shape, pad):
    """A piece of a neighbour round a part, so the inset zooms in on where the part sits."""
    bb = shape.bounding_box()
    return part(key, win(C(key), bb.min.X - pad, bb.max.X + pad, bb.min.Y - pad, bb.max.Y + pad,
                        bb.min.Z - 40, bb.max.Z + pad), "#D1D5DB")


def _bar():
    import build123d as b
    vx, vy = P["vblock_at"]
    r = 15.0
    zc = H + P["vblock"][2] - (P["vblock"][1] - 10.0) / 2 + r * math.sqrt(2)
    return b.Pos(vx, vy, zc) * b.Rot(0, 90, 0) * b.Cylinder(r, 160)


def sheets(which=None):
    import build123d as b
    M = made()
    base = dict(project="GridBench", date=DATE)
    zu, ah, rh = D["z_under"], P["apron"][1], P["rail"][1]
    frame_ctx = [M["legs"], M["aprons"], M["end_aprons"], M["low_rails"], M["rails"]]
    jobs = {}

    jobs[101] = lambda: bv.component_sheet(
        Part("Leg", C("leg_lf"), COL["leg"]), [M["aprons"], M["end_aprons"], M["low_rails"], M["shelf"]],
        dwg_no="GBN-DWG-101", title="GridBench leg (make 4): making sketch", material="Sawn softwood 70 x 70 mm, C16 or better",
        view_shape=at_origin(C("leg_lf")), inset_view=(22, -55),
        notes=[f"Make four. Cut 70 x 70 mm softwood to {D['leg_h']:.0f} mm, square both ends.",
               "Each leg has an outside corner, where its end face (toward the end of",
               "  the bench) meets its side face (toward the front or back).",
               "End face: two 9 mm holes 12.5 mm from the centre toward the outside",
               "  corner, 40 and 100 mm down from the top (long apron); two 9 mm",
               "  holes on the centre line, 100 and 130 mm up from the foot (low rail).",
               "Side face: two 9 mm holes 12.5 mm from the centre toward the outside",
               "  corner, 20 and 70 mm down from the top (end apron).",
               "Drill all six square to the face, right through, in a drill stand.",
               "Foot: bore 12 mm, 60 deep, on the centre; tap in the M10 T-nut.",
               "Round or chamfer every outside edge about 2 mm.",
               "Check: a 9 mm rod passes each hole square; the leg stands upright."], **base)

    jobs[102] = lambda: bv.component_sheet(
        Part("End apron", C("end_apron_l"), COL["end_apron"]), [M["legs"], M["aprons"]],
        dwg_no="GBN-DWG-102", title="GridBench end apron (make 2): making sketch", material="Sawn softwood 45 x 120 mm, C16 or better",
        view_shape=at_origin(C("end_apron_l")), inset_view=(22, -30),
        notes=[f"Make two. Cut 45 x 120 mm softwood to {D['end_apron_len']:.0f} mm, ends square.",
               "In each end: two 9 mm holes along the length, 52 mm deep, centred in",
               "  the 45 mm thickness, 50 and 100 mm up from the lower edge.",
               "In the inside face: two 10 mm holes 30 mm deep, 40 mm from the end,",
               "  at the same heights. They meet the end holes; the cross dowels",
               "  (barrel nuts) go in here and the bolts screw into them.",
               "Fit: butts between two legs, flush with their tops and outside faces,",
               "  held by two M8 x 120 bolts through the leg into the cross dowels.",
               "Check: an M8 bolt pushed into an end hole shows through the",
               "  cross dowel hole; the ends are square to the faces."], **base)

    jobs[103] = lambda: bv.component_sheet(
        Part("Long apron", C("apron_f"), COL["apron"]), [M["legs"], M["end_aprons"], M["rails"]],
        dwg_no="GBN-DWG-103", title="GridBench long apron (make 2): making sketch", material="Sawn softwood 45 x 120 mm, C16 or better",
        view_shape=b.Rot(0, 90, 0) * at_origin(C("apron_f")), inset_view=(22, -60),
        notes=[f"Make two. Cut 45 x 120 mm softwood to {D['long_apron_len']:,.0f} mm, ends square.",
               "In each end: two 9 mm holes along the length, 52 mm deep, centred in",
               "  the thickness, 20 and 80 mm up from the lower edge.",
               "In the inside face: two 10 mm cross dowel holes 30 mm deep, 40 mm",
               "  from the end, at the same heights.",
               "Cross rail screws: 4 mm pilot holes right through, 63 and 106 mm up",
               "  from the lower edge, at 210, 510, 757.5 and 1,005 mm from the left end.",
               "Fit: butts between the legs, flush with their tops and outside faces,",
               "  on two M8 x 120 bolts and cross dowels at each end.",
               "The cross rails butt against the inside face; brackets hold the top.",
               "Check: the two aprons are the same length within 0.5 mm."], **base)

    jobs[104] = lambda: bv.component_sheet(
        Part("Low rail", C("low_rail_f"), COL["low_rail"]), [M["legs"], M["shelf"]],
        dwg_no="GBN-DWG-104", title="GridBench low rail (make 2): making sketch", material="Sawn softwood 45 x 70 mm, C16 or better",
        view_shape=b.Rot(0, 90, 0) * at_origin(C("low_rail_f")), inset_view=(22, -60),
        notes=[f"Make two. Cut 45 x 70 mm softwood to {D['low_rail_len']:,.0f} mm, ends square.",
               "In each end: two 9 mm holes along the length, 52 mm deep, centred in",
               "  the thickness, 20 and 50 mm up from the lower edge.",
               "In the inside face: two 10 mm cross dowel holes 30 mm deep, 40 mm",
               "  from the end, at the same heights.",
               "Fit: butts between the legs on their centre line, 105 mm above the",
               "  floor (80 mm above the foot of the leg); two M8 x 120 bolts and",
               "  cross dowels at each end. The shelf rests on its top face.",
               "Check: same length as the long aprons within 0.5 mm."], **base)

    def rail_sheet():
        r4 = C("rail_4")
        return bv.component_sheet(
            Part("Cross rail", r4, COL["rail"]), [M["legs"], M["aprons"], M["end_aprons"], M["packers"]],
            dwg_no="GBN-DWG-105", title="GridBench cross rail (make 4; one notched): making sketch",
            material="Sawn softwood 45 x 70 mm, C16 or better", view_shape=at_origin(r4), inset_view=(30, -40),
            notes=[f"Make four. Cut 45 x 70 mm softwood to {D['rail_len']:.0f} mm, ends square.",
                   "Drawn: the rail nearest the right-hand legs. Saw a notch 15 mm wide",
                   "  (along the bench) by 25 mm long out of each end, full height, on",
                   "  the side toward the legs, so the rail clears their corners.",
                   "The other three rails are plain.",
                   "Ends: two 4 mm pilot holes 40 mm deep, 13 and 56 mm up from the",
                   "  lower edge (in the unnotched 30 mm of the notched rail).",
                   "Fit: tops flush with the aprons; centres 210, 510, 757.5 and 1,012.5 mm",
                   "  from the inside face of the left legs. Two 6 x 100 mm structural",
                   "  screws through the apron into each end.",
                   "The two 8.5 mm holes shown (tile rails only) are drilled in step 10.",
                   "Check: each rail drops between the aprons without forcing."], **base)
    jobs[105] = rail_sheet

    jobs[106] = lambda: bv.component_sheet(
        Part("Packer", C("packer_1"), COL["packer"]), [M["rails"], M["aprons"], M["end_aprons"]],
        dwg_no="GBN-DWG-106", title="GridBench packer under the tile (make 2): making sketch",
        material="Hardwood strip 45 x 6 mm, planed", view_shape=at_origin(C("packer_1")), inset_view=(50, -40),
        notes=[f"Make two. Hardwood strip 45 wide, 300 long, planed to {D['packer_t']:.1f} mm.",
               "The right thickness is 18 mm (the worktop) less the tile's real",
               "  thickness: measure the tile and the worktop first and plane to suit,",
               "  so the tile sits flush with the plywood.",
               "Fit: glued to the top of each of the two tile rails, centred on the",
               "  rail, running front to back under the tile pocket.",
               "Two 8.5 mm insert holes go through it in step 10, 125 mm each side",
               "  of the centre.",
               "Check: both packers the same thickness within 0.05 mm."], **base)

    jobs[107] = lambda: bv.component_sheet(
        Part("Shelf", C("shelf"), COL["shelf"]), [M["legs"], M["low_rails"], M["ballast"]],
        dwg_no="GBN-DWG-107", title="GridBench shelf: making sketch", material="Plywood 12 mm",
        view_shape=at_origin(C("shelf")), inset_view=(30, -50),
        notes=[f"Cut 12 mm plywood to {D['shelf'][0]:,.0f} x {D['shelf'][1]:.0f} mm, square.",
               "Round the corners about 5 mm and sand the edges.",
               "Fit: rests on the top faces of the two low rails, flush with their",
               "  outside faces, 5 mm clear of the legs at each end. It is slid in",
               "  from the front, above the front low rail, then lowered.",
               "It carries the two ballast slabs, side by side, 40 mm apart.",
               "Check: it lies flat on both rails and does not touch a leg."], **base)

    def worktop_sheet():
        top = C("worktop")
        x0, s, g = P["tile_x0"], P["tile"], P["pocket_gap"]
        plain = b.Pos(0, 0, H - P["top_t"] / 2) * b.Box(P["top_l"], P["top_d"], P["top_t"])
        plain -= b.Pos(x0 + s / 2, P["tile_y0"] + s / 2, H - P["top_t"] / 2) * b.Box(s + 2 * g, s + 2 * g, P["top_t"] + 2)
        return bv.component_sheet(
            Part("Worktop", top, COL["worktop"]), [M["legs"], M["aprons"], M["end_aprons"], M["rails"]],
            dwg_no="GBN-DWG-108", title="GridBench worktop: making sketch", material="Birch plywood 18 mm, one 1,200 x 600 mm panel",
            view_shape=at_origin(plain), inset_view=(30, -55),
            notes=["Cut 18 mm birch plywood to 1,200 x 600 mm, square within 0.5 mm.",
                   "Holes (shown on the hole layout, not here): 1,008 on a 25 mm grid, first",
                   "  centres 12.5 mm from the left and front edges; 756 plain 6.6 mm,",
                   "  130 at 8.0 mm for tee nuts, 122 at 8.5 mm for screw-in inserts.",
                   "  Drill on a shared CNC router, or with a printed drilling template",
                   "  indexed from the left and front edges, never from the last hole.",
                   "Tile pocket: 301 x 301 mm right through, 824.5 to 1,125.5 mm from the",
                   "  left edge and 149.5 to 450.5 mm from the front edge. Drill an 8 mm",
                   "  relief hole on each corner first, then jigsaw and rout to the line.",
                   "Round all edges 1 mm; seal both faces with a thin finish.",
                   "Fit: on the aprons and rails, held by nine steel brackets from below.",
                   "Check: corner to corner diagonals equal within 1 mm."], **base)
    jobs[108] = worktop_sheet

    def tile_sheet():
        t = C("tile")
        return bv.component_sheet(
            Part("Precision tile", t, COL["tile"]), [M["worktop"], M["packers"], M["rails"]],
            dwg_no="GBN-DWG-109", title="GridBench precision tile: making sketch",
            material="Cast aluminium tooling plate 300 x 300 x 12.7 mm", view_shape=at_origin(t), inset_view=(35, -50),
            notes=["Cast tooling plate 300 x 300 x 12.7 mm, edges square; chamfer 0.5 mm.",
                   "Measure from the left and front edges. 144 M6 holes on a 25 mm grid,",
                   "  first centres 12.5 mm in: drill 5.0 mm through in a drilling jig,",
                   "  then tap M6 with a spiral-point tap held square in a tapping guide.",
                   "Nine dowel bores at 50, 150 and 250 mm both ways (centres of grid",
                   "  squares): drill 7.8 mm, then ream 8 mm H7 through.",
                   "Four fixing holes 7 mm, 22.5 mm in from the left and right edges",
                   "  and 25 mm in from the front and back edges; counterbore 11 mm,",
                   "  6.5 mm deep, from the top, for M6 x 20 cap screws.",
                   "Deburr; stone the top flat. Mark the top face and the front edge.",
                   "Fit: flush in the worktop pocket, 0.5 mm gap round it, on the",
                   "  packers; four screws into inserts in the two tile rails.",
                   "Check: an 8 mm h6 pin slides into every bore; holes on pitch ±0.05."], **base)
    jobs[109] = tile_sheet

    def clamp_sheet():
        cl = C("clamps")
        one = cl & (b.Pos(312.5, 40, H + 40) * b.Box(60, 100, 100))
        return bv.component_sheet(
            Part("Toe clamp", one, COL["clamp"]), [M["tile"], part("Workpiece", C("_workpiece"), COL["work"])],
            dwg_no="GBN-DWG-110", title="GridBench printed toe clamp (make 4): making sketch",
            material="PETG, 3D printed, 6 walls, 40 % infill", view_shape=flat(one, (312.5, 40, H + 40), (0, 1, 0), (0, 0, 1)),
            inset_view=(35, -40),
            notes=["Print four in PETG lying on a side face, so the layers run along",
                   "  the clamp: 6 walls, 40 % infill, about 50 g each.",
                   "Body 70 long, 24 wide, 30 deep. Slot 6.6 mm wide, 31.5 mm long,",
                   "  its centre 7 mm from the middle toward the toe end.",
                   "Heel at the other end, 14 mm long, as tall as the work (40 mm here).",
                   "Fit: an M6 x 80 cap screw with a printed knob passes through the",
                   "  slot into a threaded hole; the toe presses the work, the heel",
                   "  stands on the table. Slide the body so the screw is nearer the toe.",
                   "Mark 1.6 N m MAX on the top: never tighten past it.",
                   "Check: no cracks or gaps between layers at the slot ends."], **base)
    jobs[110] = clamp_sheet

    def fence_sheet():
        f = C("fence")
        one = f & (b.Pos(P["fence_x"][0], P["fence_y"], H + 30) * b.Box(196, 40, 70))
        return bv.component_sheet(
            Part("Fence segment", one, COL["fixture"]), [_near("worktop", one, 120)],
            dwg_no="GBN-DWG-111", title="GridBench fence segment (make 2): making sketch",
            material="PETG, 3D printed", view_shape=at_origin(one), inset_view=(35, -60),
            notes=["Print two in PETG, lying on a 190 x 50 mm face: 190 long, 25 wide,",
                   "  50 tall. Every part fits a 200 x 200 mm bed.",
                   "Two 6.6 mm holes top to bottom, 50 mm each side of the centre (100",
                   "  apart, on the threaded 50 mm sub-grid).",
                   "Counterbore each 11 mm from the top down to 12 mm above the base,",
                   "  so an M6 x 30 cap screw reaches the thread below the worktop.",
                   "Fit: two M6 x 30 cap screws into threaded grid positions; the two",
                   "  segments stand end to end with a 10 mm gap.",
                   "Check: the front face is square to the base (engineer's square)."], **base)
    jobs[111] = fence_sheet

    def vblock_sheet():
        v = C("vblock")
        return bv.component_sheet(
            Part("V-block", v, COL["fixture"]), [_near("worktop", v, 80), part("Bar", _bar(), COL["work"])],
            dwg_no="GBN-DWG-112", title="GridBench V-block: making sketch", material="PETG, 3D printed",
            view_shape=at_origin(v), inset_view=(35, -60),
            notes=["Print in PETG standing on one 60 x 60 mm end, so the V needs no",
                   "  support: 100 long, 60 wide, 60 tall.",
                   "The 90 degree V runs the full length: 50 mm wide at the top, with a",
                   "  5 mm flat each side, its bottom 35 mm above the base. It holds",
                   "  round bar from about 8 to 45 mm across.",
                   "Two 6.6 mm holes from the V bottom to the base, 25 mm each side",
                   "  of the centre; counterbore 11 mm down to 12 mm above the base.",
                   "Fit: two M6 x 30 cap screws into threaded grid positions 50 apart.",
                   "Check: a 20 mm bar rests on both faces of the V."], **base)
    jobs[112] = vblock_sheet

    def stop_sheet():
        st = C("stops")
        x, y = P["stops_at"][0]
        one = st & (b.Pos(x, y, H) * b.Box(30, 30, 80))
        return bv.component_sheet(
            Part("Stop pin", one, COL["fixture"]), [_near("worktop", one, 40)],
            dwg_no="GBN-DWG-113", title="GridBench stop pin (make 6): making sketch", material="PETG, 3D printed",
            view_shape=at_origin(one), inset_view=(35, -60),
            notes=["Print six in PETG standing upright: head 12 mm across, 24 mm tall,",
                   "  with a spigot 6.3 mm across and 12 mm long below it.",
                   "The spigot drops into any 6.6 mm plain hole; the head is the stop.",
                   "For heavy use, press a 6 mm steel dowel into a 5.8 mm hole",
                   "  printed through the head instead of the printed spigot.",
                   "Check: the spigot drops into a plain hole by hand and does not",
                   "  rock more than about 0.3 mm at the top."], **base)
    jobs[113] = stop_sheet

    def foot_sheet():
        f = C("post_foot")
        return bv.component_sheet(
            Part("Post foot", f, COL["pfoot"]), [_near("worktop", f, 70), _near("tile", f, 70), part("Post", _near("post", f, 80).shape, COL["post"])],
            dwg_no="GBN-DWG-114", title="GridBench instrument post foot: making sketch", material="PETG, 3D printed, 100 % infill",
            view_shape=at_origin(f), inset_view=(30, -50),
            notes=["Print flat in PETG at 100 % infill: 74 x 74 x 12 mm.",
                   "Two 6.6 mm holes at opposite corners, 25 mm from the centre both",
                   "  ways (on the threaded 50 mm sub-grid), for M6 x 30 cap screws.",
                   "Two 5.5 mm holes on the centre line, 10 mm each side of the centre,",
                   "  counterbored 9 mm, 5 mm deep, from the underside, for the M5 x 20",
                   "  screws that go up into the extrusion.",
                   "Fit: the extrusion stands on its top face, its 40 mm side front to",
                   "  back; the foot screws down onto any two threaded grid positions.",
                   "Check: the extrusion stands square to the foot."], **base)
    jobs[114] = foot_sheet

    def armclamp_sheet():
        a = C("arm_clamps")
        A = arm_geometry(P)
        one = a & (b.Pos(A["px"], A["py"], A["az"]) * b.Box(120, 80, 60))
        return bv.component_sheet(
            Part("Arm clamp", one, COL["aclamp"]), [part("Post", C("post"), COL["post"]), part("Arm", C("arm"), COL["arm"])],
            dwg_no="GBN-DWG-115", title="GridBench arm clamp (on the post): making sketch", material="PETG, 3D printed, 100 % infill",
            view_shape=at_origin(one), inset_view=(25, -40),
            notes=["Print in PETG at 100 % infill: 64 wide, 50 deep, 40 tall.",
                   "Slot 20.4 x 40.4 mm top to bottom for the post (0.2 mm clear",
                   "  each side), its centre 13 mm right of the block's centre.",
                   "Bore 18.4 mm front to back for the arm, 25 mm left of the post",
                   "  centre and half way up, so the arm passes beside the post.",
                   "Print a hex pocket for an M6 nut and a 6.6 mm hole into the slot",
                   "  and into the bore, each locked by an M6 thumb screw.",
                   "Fit: slides on the post; the arm slides through the bore.",
                   "Check: slides freely when loose and does not move when locked."], **base)
    jobs[115] = armclamp_sheet

    def endclamp_sheet():
        a = C("arm_clamps")
        A = arm_geometry(P)
        one = a & (b.Pos(A["ax"], A["yc"], A["az"]) * b.Box(60, 70, 60))
        return bv.component_sheet(
            Part("End clamp", one, COL["aclamp"]), [part("Arm", C("arm"), COL["arm"]), part("Drop rod", C("drop_rod"), COL["arm"]),
                                                   part("Indicator", C("indicator"), COL["indicator"])],
            dwg_no="GBN-DWG-116", title="GridBench end clamp (arm to drop rod): making sketch", material="PETG, 3D printed, 100 % infill",
            view_shape=at_origin(one), inset_view=(25, -40),
            notes=["Print in PETG at 100 % infill: 30 wide, 50 deep, 30 tall.",
                   "Arm bore 18.4 mm from the back face, 27 mm deep (blind).",
                   "Drop rod bore 12.4 mm top to bottom, its centre 14 mm in front of",
                   "  the block's centre, so it passes 6 mm in front of the arm's end.",
                   "Hex pockets and 6.6 mm holes for two M6 thumb screws, one onto",
                   "  the arm and one onto the drop rod.",
                   "Fit: on the end of the arm; the 12 mm drop rod slides up and down",
                   "  in it and carries the dial indicator by its lug back.",
                   "Check: the drop rod stands upright when the arm is level."], **base)
    jobs[116] = endclamp_sheet

    keys = sorted(jobs) if which is None else [int(w) for w in which]
    return [jobs[k]() for k in keys]


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def joints(which=None):
    zu, ah = D["z_under"], P["apron"][1]
    lx, ly = D["lx"], D["ly"]
    jobs = {}

    def j1():
        zc = zu - ah + P["apron_bolt_z"][1]                     # level with the long apron's upper bolts
        bx = (lx - 150, lx + 50, ly - 150, ly + 50, zu - ah - 5, zc)
        return bv.joint([
            part("Back right leg", win(C("leg_rb"), *bx), COL["leg"]),
            part("Long apron", win(C("apron_b"), *bx), COL["apron"]),
            part("End apron", win(C("end_apron_r"), *bx), COL["end_apron"]),
            part("M8 x 120 bolt and cross dowel", win(C("frame_bolts"), *bx), COL["bolt"])],
            OUT / "joint-01.png", "Joint 1: aprons to a leg (back right leg)",
            subtitle="Cut level with the upper bolt of the long apron, seen from above. The bolt passes through the leg into a cross dowel",
            elev=62, azim=-120, size=(8, 6))
    jobs[1] = j1

    def j2():
        zc = P["low_rail_z"] + P["low_bolt_z"][1]
        bx = (lx - 160, lx + 50, ly - 90, ly + 50, P["low_rail_z"] - 5, zc)
        return bv.joint([
            part("Back right leg", win(C("leg_rb"), *bx), COL["leg"]),
            part("Low rail", win(C("low_rail_b"), *bx), COL["low_rail"]),
            part("M8 x 120 bolt and cross dowel", win(C("frame_bolts"), *bx), COL["bolt"])],
            OUT / "joint-02.png", "Joint 2: low rail to a leg (back right)",
            subtitle="Cut level with the upper bolt, seen from above. The same joint as the aprons, on the leg's centre line",
            elev=62, azim=-120, size=(8, 6))
    jobs[2] = j2

    def j3():
        zc = zu - P["rail"][1] + P["rail_screw_z"][1]
        bx = (lx - 120, lx + 40, -ly - 45, -ly + 110, zu - P["rail"][1] - 5, zc)
        return bv.joint([
            part("Front right leg", win(C("leg_rf"), *bx), COL["leg"]),
            part("Long apron", win(C("apron_f"), *bx), COL["apron"]),
            part("Notched cross rail", win(C("rail_4"), *bx), COL["rail"]),
            part("6 x 100 screw", win(C("rail_screws"), *bx[:5], zc + 2.5), COL["bolt"])],
            OUT / "joint-03.png", "Joint 3: the notched cross rail beside the right legs",
            subtitle="Cut level with the upper screw, seen from above and behind. The notch clears the leg corner; screws through the apron hold the rail",
            elev=62, azim=125, size=(8, 6))
    jobs[3] = j3

    def j4():
        bx = (-lx - 45, -lx + 45, -ly - 45, -ly + 45, -2, 110)
        return bv.joint([
            part("Leg (cut open)", win(C("leg_lf"), *bx), COL["leg"]),
            part("M10 T-nut", win(C("tnuts"), *bx), "#C9A227"),
            part("Levelling foot with rubber pad", win(C("feet"), *bx), COL["feet"])],
            OUT / "joint-04.png", "Joint 4: levelling foot in the leg end (front left)",
            subtitle="Cut through the leg. The T-nut flange bears on the leg end; the foot screws through it into the bore",
            cut="+Y", elev=12, azim=-90, size=(8, 6))
    jobs[4] = j4

    def j5():
        x = P["bracket_x"][1]
        y = -(D["long_apron_y"] - P["apron"][0] / 2)
        bx = (x - 45, x + 45, y - 50, y + 60, zu - 70, H + 1)
        return bv.joint([
            part("Worktop (underside)", win(C("worktop"), bx[0], bx[1], bx[2], bx[3] + 90, bx[4], bx[5]), COL["worktop"]),
            part("Front apron", win(C("apron_f"), *bx), COL["apron"]),
            part("Steel angle bracket", win(C("brackets"), *bx), COL["bracket"]),
            part("4 x 25 screw into the apron, 4 x 16 up into the top", win(C("bracket_screws"), *bx), COL["bolt"])],
            OUT / "joint-05.png", "Joint 5: worktop bracket on the front apron",
            subtitle="Seen from inside the frame and below. One screw into the apron, one up into the worktop",
            elev=-30, azim=70, size=(8, 6))
    jobs[5] = j5

    def j6():
        y = -187.5                                                # a threaded row; the cut runs along its hole centres
        bx = (-362.5, -262.5, y, y + 40, zu - 40, H + 1)
        return bv.joint([
            part("Worktop (cut along a row of holes)", win(C("worktop"), *bx), COL["worktop"]),
            part("Cross rail below", win(C("rail_1"), *bx), COL["rail"]),
            part("Tee nut, pressed in from below", win(C("tee_nuts"), *bx), "#C9A227"),
            part("Screw-in insert, over the rail", win(C("screw_inserts"), *bx), "#C2410C")],
            OUT / "joint-06.png", "Joint 6: threaded positions in the worktop",
            subtitle="Cut along a row of holes, seen from the front. Over a frame member a screw-in insert from the top; elsewhere a tee nut from below",
            elev=12, azim=-90, size=(8, 6))
    jobs[6] = j6

    def j7():
        fx, fy = fixing_points(P)[2]
        bx = (fx - 40, fx + 40, fy - 30, fy + 30, zu - 40, H + 1)
        return bv.joint([
            part("Worktop", win(C("worktop"), *bx), COL["worktop"]),
            part("Precision tile (cut open)", win(C("tile"), *bx), COL["tile"]),
            part("Packer", win(C("packer_2"), *bx), COL["packer"]),
            part("Tile rail", win(C("rail_4"), *bx), COL["rail"]),
            part("M6 screw-in insert", win(C("rail_inserts"), *bx), "#C2410C"),
            part("M6 x 20 cap screw", win(C("tile_screws"), *bx), COL["bolt"])],
            OUT / "joint-07.png", "Joint 7: tile fixing screw (front right)",
            subtitle="Cut through the screw. The tile sits flush on the packer with 0.5 mm clear of the pocket",
            cut="+Y", elev=10, azim=-90, size=(8, 6))
    jobs[7] = j7

    def j8():
        bx = (240, 470, -120, 90, H - 14, H + 90)
        return bv.joint([
            part("Precision tile", win(C("tile"), *bx), COL["tile"]),
            part("Workpiece (example)", win(C("_workpiece"), *bx), COL["work"]),
            part("Round and diamond pins", win(S("pins", "diamond"), *bx), COL["pins"]),
            part("Toe clamps", win(C("clamps"), *bx), COL["clamp"]),
            part("M6 x 80 screws with knobs", win(C("clamp_screws"), *bx), COL["bolt"])],
            OUT / "joint-08.png", "Joint 8: work held on the tile",
            subtitle="Each toe clamp screw goes into a threaded tile hole; the toe presses the work, the heel stands on the tile",
            elev=30, azim=-60, size=(8, 6))
    jobs[8] = j8

    def j9():
        A = arm_geometry(P)
        bx = (A["px"] - 60, A["px"] + 60, A["py"] - 60, A["py"] + 60, H - 20, H + 60)
        return bv.joint([
            part("Worktop", win(C("worktop"), *bx), COL["worktop"]),
            part("Post foot (cut open)", win(C("post_foot"), *bx), COL["pfoot"]),
            part("Post, 20 x 40 extrusion", win(C("post"), *bx), COL["post"]),
            part("M5 x 20 screws up into the post", win(C("post_screws"), *bx), COL["bolt"])],
            OUT / "joint-09.png", "Joint 9: post foot on the worktop",
            subtitle="Cut through the post's two M5 screws, which hold it from below; two M6 screws hold the foot to the grid",
            cut="-X", elev=12, azim=-20, size=(8, 6))
    jobs[9] = j9

    def j10():
        A = arm_geometry(P)
        bx = (A["ax"] - 45, A["px"] + 40, A["arm_end"] - 40, A["py"] + 50, A["az"] - 80, A["az"] + 40)
        return bv.joint([
            part("Post", win(C("post"), *bx), COL["post"]),
            part("Arm clamp and end clamp", win(C("arm_clamps"), *bx), COL["aclamp"]),
            part("Arm, 18 mm", win(C("arm"), *bx), COL["arm"]),
            part("Drop rod, 12 mm", win(C("drop_rod"), *bx), "#9CA3AF"),
            part("Dial indicator lug", win(C("indicator"), *bx), COL["indicator"])],
            OUT / "joint-10.png", "Joint 10: arm, clamps and drop rod",
            subtitle="The arm passes beside the post through the arm clamp; the drop rod passes in front of the arm's end",
            elev=40, azim=-50, size=(8, 6))
    jobs[10] = j10

    def j11():
        x = P["anchor_x"][1]
        bx = (x - 60, x + 60, D["long_apron_y"] - 40, P["top_d"] / 2 + 10, zu - ah - 70, zu + 20)
        return bv.joint([
            part("Rear apron", win(C("apron_b"), *bx), COL["apron"]),
            part("Worktop", win(C("worktop"), *bx), COL["worktop"]),
            part("Wall anchor angle (optional)", win(C("anchor"), *bx), COL["anchor"])],
            OUT / "joint-11.png", "Joint 11: wall anchor angle (optional)",
            subtitle="Seen from behind and below. One leg screws up into the rear apron, the other into the wall",
            elev=-20, azim=60, size=(8, 6))
    jobs[11] = j11

    keys = sorted(jobs) if which is None else [int(w) for w in which]
    return [jobs[k]() for k in keys]


# ----------------------------------------------------------------- assembly steps
def steps(which=None):
    M = made()
    zu = D["z_under"]
    jobs = {}

    def st(n, done, new, title, sub, **kw):
        return bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw)

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)
    legs, feet = M["legs"], M["feet"]
    ends = M["end_aprons"]
    jobs[1] = lambda: st(1, [legs], [mv(part("M10 T-nuts", C("tnuts"), "#C9A227"), (0, 0, -120)),
                                     mv(part("Levelling feet", C("feet"), COL["feet"]), (0, 0, -260))],
                         "T-nuts and feet into the legs",
                         "Tap each T-nut into the 12 mm bore in the leg foot; screw the foot in to mid travel (13 mm showing)",
                         elev=12, azim=-55, label_done=False)
    jobs[2] = lambda: st(2, [legs, feet], [mv(ends, (0, 0, 200)),
                                           mv(part("M8 bolts (front legs)", _bolts("end", "-y"), COL["bolt"]), (0, -180, 0)),
                                           mv(part("M8 bolts (back legs)", _bolts("end", "+y"), COL["bolt"]), (0, 180, 0))],
                         "end aprons between the legs",
                         "Two bolts through each leg into cross dowels in the apron end; tops and outside faces flush. Snug only",
                         elev=18, azim=-55, label_done=False)
    jobs[3] = lambda: st(3, [legs, feet, ends], [mv(M["aprons"], (0, -220, 120)),
                                                  mv(part("M8 bolts (right legs)", _bolts("apron", "+x"), COL["bolt"]), (250, 0, 0)),
                                                  mv(part("M8 bolts (left legs)", _bolts("apron", "-x"), COL["bolt"]), (-250, 0, 0))],
                         "long aprons join the two end frames",
                         "Two bolts through each leg into each apron end; check the frame is square (equal diagonals), then tighten",
                         elev=18, azim=-55, label_done=False)
    frame1 = [legs, feet, ends, M["aprons"]]
    jobs[4] = lambda: st(4, frame1, [mv(M["low_rails"], (0, -220, 0)),
                                     mv(part("M8 bolts (right legs)", _bolts("low", "+x"), COL["bolt"]), (250, 0, 0)),
                                     mv(part("M8 bolts (left legs)", _bolts("low", "-x"), COL["bolt"]), (-250, 0, 0))],
                         "low rails between the legs",
                         "Two bolts each end, 105 mm above the floor; tighten all frame bolts firmly",
                         elev=18, azim=-55, label_done=False)
    frame2 = frame1 + [M["low_rails"]]
    jobs[5] = lambda: st(5, frame2, [mv(M["rails"], (0, 0, 220))], "cross rails between the long aprons",
                         "Tops flush with the aprons; notched rail beside the right legs; two 6 x 100 screws through the apron into each end",
                         elev=30, azim=-55, label_done=False)
    frame3 = frame2 + [M["rails"]]
    jobs[6] = lambda: st(6, frame3, [mv(M["packers"], (0, 0, 160))], "packers onto the two tile rails",
                         "Glue each packer centred on the top of a tile rail, running front to back; clamp until set",
                         elev=35, azim=-55, label_done=False)
    frame4 = frame3 + [M["packers"]]
    jobs[7] = lambda: st(7, frame4, [mv(M["shelf"], (0, -450, 60))], "shelf onto the low rails",
                         "Slide it in from the front above the front low rail, then lower it onto both rails",
                         elev=22, azim=-55, label_done=False)
    frame5 = frame4 + [M["shelf"]]
    jobs[8] = lambda: st(8, [M["worktop"]], [mv(part("Tee nuts, 130 (from below)", marks("tee"), "#C9A227"), (0, 0, -120)),
                                             mv(part("Screw-in inserts, 122 (from the top)", marks("screw"), "#C2410C"), (0, 0, 120))],
                         "threaded inserts into the worktop",
                         "Tee nuts pressed in from the underside; screw-in inserts driven flush from the top where a frame member will be below",
                         elev=-25, azim=-60, label_done=False)
    top = part("Worktop with its inserts", _fuse([C("worktop"), marks("tee"), marks("screw"), marks("plain")]), COL["worktop"])
    jobs[9] = lambda: st(9, frame5, [mv(top, (0, 0, 260)), mv(M["brackets"], (0, 0, -140))],
                         "worktop onto the frame",
                         "20 mm overhang all round, tile pocket over the two tile rails; nine brackets screwed to the aprons and up into the worktop",
                         elev=22, azim=-55, label_done=False)
    bench = frame5 + [top, M["brackets"]]
    jobs[10] = lambda: st(10, bench, [mv(part("Rail inserts", C("rail_inserts"), "#C2410C"), (0, 0, 120)),
                                      mv(part("Precision tile", C("tile"), COL["tile"]), (0, 0, 240)),
                                      mv(part("M6 x 20 cap screws", C("tile_screws"), COL["bolt"]), (0, 0, 380))],
                          "precision tile into its pocket",
                          "Drill the packers and rails through the pocket, drive four inserts, drop the tile in flush and fit four screws",
                          elev=35, azim=-50, label_done=False)
    bench2 = bench + [M["tile"]]
    jobs[11] = lambda: st(11, bench2, [mv(M["ballast"], (0, -600, 0))], "ballast slabs onto the shelf",
                          "Two 13 kg slabs, side by side, centred, 40 mm apart. Lift with a straight back",
                          elev=18, azim=-55, label_done=False)
    bench3 = bench2 + [M["ballast"]]
    jobs[12] = lambda: st(12, bench3, [mv(M["fixtures"], (0, 0, 200))], "fence, stop pins and V-block",
                          "Each fence segment and the V-block on two M6 x 30 screws into threaded positions; stop pins into plain holes",
                          elev=32, azim=-55, label_done=False)
    bench4 = bench3 + [M["fixtures"]]
    work = part("Workpiece (example)", C("_workpiece"), COL["work"])
    jobs[13] = lambda: st(13, bench4, [mv(M["pins"], (0, 0, 120)), mv(work, (0, 0, 220)), mv(M["clamps"], (0, 0, 340))],
                          "pins, work and toe clamps on the tile",
                          "Pins into two bores; work against them; each clamp on an M6 x 80 screw into a tile hole, 1.6 N m at most",
                          elev=32, azim=-55, label_done=False)
    bench5 = bench4 + [M["pins"], work, M["clamps"]]
    jobs[14] = lambda: st(14, bench5, [mv(M["post"], (0, 0, 260)), mv(M["indicator"], (0, 0, 420))],
                          "instrument post, arm and dial indicator",
                          "Foot on two M6 x 30 screws; arm clamp on the post, arm through it; indicator on the drop rod, its point on the work",
                          elev=25, azim=-55, label_done=False)
    bench6 = bench5 + [M["post"], M["indicator"]]
    jobs[15] = lambda: st(15, bench6, [mv(M["anchor"], (0, 260, 0))], "wall anchor angles (optional)",
                          "Seen from behind. Bench against the wall; each angle screwed up into the rear apron and into wall plugs",
                          elev=18, azim=90, label_done=False)
    keys = sorted(jobs) if which is None else [int(w) for w in which]
    return [jobs[k]() for k in keys]


def _bolts(kind, side=None):
    """The frame bolts (each fused with its cross dowel) of one joint family: 'low' for the low rails,
    'apron' for the long aprons (bolts along the bench), 'end' for the end aprons (bolts across it)."""
    import build123d as b
    zu = D["z_under"]
    sols = C("frame_bolts").solids()
    if kind == "low":
        sel = [s for s in sols if s.bounding_box().center().Z < 400]
    else:
        up = [s for s in sols if s.bounding_box().center().Z > 400]
        along_x = [s for s in up if s.bounding_box().size.X > 60]
        ids = {id(s) for s in along_x}
        sel = along_x if kind == "apron" else [s for s in up if id(s) not in ids]
    if side:
        ax_, sg = side[1], (1 if side[0] == "+" else -1)
        sel = [s for s in sel if sg * getattr(s.bounding_box().center(), ax_.upper()) > 0]
    return b.Compound(children=sel)


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "layouts", "sheets", "joints", "steps"]
    fns = {"overview": overview, "layouts": layouts, "sheets": sheets, "joints": joints, "steps": steps}
    i = 0
    while i < len(args):
        w = args[i]
        sub = []
        while i + 1 < len(args) and args[i + 1].isdigit():
            sub.append(args[i + 1]); i += 1
        r = fns[w](sub) if (sub and w in ("sheets", "joints", "steps")) else fns[w]()
        print(w, "->", r)
        i += 1
