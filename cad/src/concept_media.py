"""GridBench concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the parts from cad/src/model.py (PARAMS) and renders the media set with .kit/concept.py.
Parts are colored and numbered to match bom/bom.csv. Figures on the sheet and in the flow diagram
come from docs/04-calcs/sizing.py (GBN-CAL-001). Not for fabrication.

Coordinates in mm, as in model.py: X along the bench, Y front to back (front at -Y), Z up, floor at
Z = 0, worktop surface at Z = 900. The model cuts only a representative patch of the 1,008 plywood
holes; here every grid position is drawn as a thin dark disk on the surface (as at TRL 2), which
reads as a hole at render scale and is far lighter to mesh than 1,000 boolean cuts.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build123d  # noqa: E402
from build123d import Compound, Pos, RegularPolygon, extrude  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all  # noqa: E402
from model import PARAMS as P, build_parts, classify, dowel_points  # noqa: E402

H = P["h"]
WOOD, PLY, ALU, STEEL = "#C8A06A", "#E2C48E", "#B8C2CC", "#6B7280"
PRINT, PRINT2, BRASS, HOLE = "#0F766E", "#14B8A6", "#C9A227", "#3F3A33"


def disk(r, h):
    """Octagonal disk: light to mesh, reads as a round hole at render scale."""
    return extrude(RegularPolygon(r, 8), amount=h)


tile_xy, ins_xy, plain_xy = classify(P)
ply_holes = Compound(children=[Pos(x, y, H) * disk(P["plain_d"] / 2, 0.6) for x, y in plain_xy])
inserts_mark = Compound(children=[Pos(x, y, H) * disk(P["insert_od"] / 2 - 0.5, 0.6) for x, y in ins_xy])
ins_bores = Compound(children=[Pos(x, y, H + 0.6) * disk(2.6, 0.4) for x, y in ins_xy])
tile_holes = Compound(children=[Pos(x, y, H) * disk(2.5, 0.6) for x, y in tile_xy]
                      + [Pos(x, y, H) * disk(P["dowel_d"] / 2, 0.6) for x, y in dowel_points(P)])

m = build_parts(P)
parts = [
    Part("Bench frame, bolted timber", m["frame"], WOOD, 1, (0, 0, -420)),
    Part("Levelling feet, M10, rubber pads (4)", m["feet"], STEEL, 2, (0, 0, -300)),
    Part("Lower shelf", m["shelf"], PLY, 3, (0, -700, -300)),
    Part("Ballast slabs, concrete (2)", m["ballast"], "#A8A29E", 14, (0, -700, -150)),
    Part("Wall anchor brackets (optional)", m["anchor"], STEEL, 15, (0, 800, 250)),
    Part("Plywood grid worktop (coarse field)", m["worktop"], PLY, 4, (0, 0, 0)),
    Part("Pin holes, 6.6 mm", ply_holes, HOLE, None, (0, 0, 0)),
    Part("M6 tee nuts and inserts, 50 mm sub-grid", inserts_mark, BRASS, 5, (0, 0, 0)),
    Part("Insert bores", ins_bores, HOLE, None, (0, 0, 0)),
    Part("Precision grid tile, aluminum", m["tile"], ALU, 6, (0, 0, 200)),
    Part("Tile holes", tile_holes, "#374151", None, (0, 0, 200)),
    Part("Round dowel pin, 8 mm h6", m["pins"], "#374151", 7, (0, 0, 330)),
    Part("Diamond locating pin, 8 mm h6", m["diamond"], "#111827", 13, (0, 0, 330)),
    Part("Printed toe clamps", m["clamps"], PRINT, 8, (0, 0, 530)),
    Part("Printed fence, stops and V-block", m["fixtures"], PRINT2, 9, (0, 0, 320)),
    Part("Instrument post and arm", m["post"], "#475569", 10, (250, 300, 150)),
    Part("Dial indicator, 0.01 mm (user-supplied)", m["indicator"], "#1D4ED8", 11, (0, 0, 680)),
    Part("Workpiece (example, not in BOM)", m["_workpiece"], "#9CA3AF", None, (0, 0, 430)),
]

# Blueprint views: leave the ~1,300 hole marks out of hidden-line removal. With them the
# projection runs out of memory, and at sheet scale they would print as a grey smear anyway.
import drawing  # noqa: E402  (the kit module that render_all imports its view projector from)
_HOLE_MARKS = {id(ply_holes), id(ins_bores), id(tile_holes), id(inserts_mark)}
_project_views = drawing.project_views


def _views_without_hole_marks(part, workdir, **kw):
    kids = [k for k in part.children if id(k) not in _HOLE_MARKS]
    return _project_views(Compound(children=kids), workdir, **kw)


drawing.project_views = _views_without_hole_marks

# Web model: the kit exports glTF at build123d's default (very fine) tessellation, and the ~2,000
# hole-mark disks alone made model.glb about 13 MB. Without changing the kit, the web model here
# leaves the marks out (the tile keeps its real holes and the worktop its representative patch) and
# uses a coarser tessellation; the viewer is for massing, not measurement.
_export_gltf = build123d.export_gltf


def _coarse_gltf(shape, path, *a, **kw):
    from OCP.BRepTools import BRepTools
    BRepTools.Clean_s(shape.wrapped)   # drop the finer meshes left by the renders, so the settings below apply
    kw.setdefault("linear_deflection", 0.5)
    kw.setdefault("angular_deflection", 0.5)
    return _export_gltf(shape, path, *a, **kw)


build123d.export_gltf = _coarse_gltf
_export_web_model = concept.export_web_model


def _web_model_without_marks(parts, *a, **kw):
    return _export_web_model([p for p in parts if id(p.shape) not in _HOLE_MARKS], *a, **kw)


concept.export_web_model = _web_model_without_marks

render_all(
    parts, project="GridBench", title="Grid workbench and fixture set", dwg_no="GBN-DWG-010", date="2026-09-25",
    key_figures=["25 mm grid, M6, same as metric optical breadboards; 1,152 positions",
                 "Worktop 1,200 x 600 mm at 900 mm; tile 300 x 300 mm, 9 dowel bores 8 H7",
                 "41.9 kg empty; tips at 112 N empty, 181 N with 25.8 kg ballast",
                 "0.37 mm under 500 N at a bay with 45 x 120 aprons (target 0.5 mm)",
                 "Core parts $245.90 vs $250 budget (GBN-CAL-001 v0.2)"],
    cut=False,  # a section adds little: the worktop is solid plywood with the tile flush in a pocket
    flow={"title": "material flow for one part at a fixture (times are estimates)", "unit": "",
          "stages": [("Blank in", "from stock or printer"), ("Locate", "2 pins, ~10 s"),
                     ("Clamp", "2 toe clamps, ~20 s"), ("Work", "drill, assemble or test"),
                     ("Check", "indicator, ~20 s"), ("Part out", "next part")],
          "losses": [(4, "Rework after check, target per 100 parts", 1)]},
)
