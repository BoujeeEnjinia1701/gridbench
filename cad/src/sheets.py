"""GridBench general arrangement sheet GBN-DWG-001, Rev P2 (TRL 3; Rev P2 under GBN-DDR-002).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/GBN-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is GBN-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, build_parts, derived, dowel_points, insert_kinds  # noqa: E402

TEE, SCREW = insert_kinds(P)

DATE = "2026-09-25"


def safe_project_views(part, workdir, line_weight=0.35, names=("front", "top", "right", "iso")):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name in names:
        origin, up = setups[name]
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name not in ("iso", "top") else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected {', '.join(names)}; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.0, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly()
    views = safe_project_views(asm, work)
    tile = build_parts()["tile"]
    tview = safe_project_views(tile, work / "tile", names=("top",))["top"]
    bb = asm.bounding_box()
    s = Sheet(project="GridBench", title="General arrangement", dwg_no="GBN-DWG-001", rev="P3",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Softwood frame, birch plywood top, cast aluminum tile; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Recommendations accepted (DDR-002): 45 x 120 aprons, tee nuts, rubber feet", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    H, Lt, Dt = P["h"], P["top_l"], P["top_d"]
    x0, t = P["tile_x0"], P["tile"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zg = Z(0)
    L.append(f'<line x1="{x - 8:.2f}" y1="{zg:.2f}" x2="{x + w + 4:.2f}" y2="{zg:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    L.append(_t(x + w + 5, zg - 1.2, "FLOOR", 2.0, 600, MUTED, "start"))
    xd = X(-Lt / 2) - 5
    # height (900 +/- 15) and worktop length (1,200) are dropped here: both are in the notes box and the overall views
    L += dim_h(X(-D["lx"]), X(D["lx"]), zg + 23, f"{2 * D['lx']:,.0f} FEET")
    L += [ext(X(-D["lx"]), zg + 1, X(-D["lx"]), zg + 24), ext(X(D["lx"]), zg + 1, X(D["lx"]), zg + 24)]
    L += leader(X(-120), Z(D["shelf_z"] + 30), X(-120) + 3, Z(D["shelf_z"] + 250), "14 BALLAST, 2 SLABS")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    L += dim_h(Xt(-Lt / 2), Xt(x0), Yt(Dt / 2) - 10, f"{x0 + Lt / 2:.0f}")
    L += dim_h(Xt(x0), Xt(x0 + t), Yt(Dt / 2) - 10, f"{t:.0f}")
    L += [ext(Xt(x0), Yt(P['tile_y0'] + t), Xt(x0), Yt(Dt / 2) - 11), ext(Xt(x0 + t), Yt(P['tile_y0'] + t), Xt(x0 + t), Yt(Dt / 2) - 11)]
    L += leader(Xt(x0 + t / 2), Yt(0), Xt(bb.max.X) + 9, Yt(Dt / 2) + 2, "6 PRECISION TILE, FLUSH")
    L += leader(Xt(-500), Yt(-250), Xt(bb.max.X) + 9, Yt(-Dt / 2) + 2, "4 PLYWOOD FIELD, 25 GRID")

    # right view (from +X): +Y to the right, Z up
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    # the 490 feet spacing (front to back) is given in the notes box

    # detail A: tile, top view at 1:5, left of the orthographic group
    kd = 0.2
    dx, dy, dw = M + 12, M + 34, t * kd
    s.add_svg(tview, dx, dy, dw, dw, scale=kd, label="Detail A: tile", sublabel="Top view, scale 1:5")
    Xd = lambda mx: dx + (mx - x0) * kd
    Yd = lambda my: dy + dw - (my - P["tile_y0"]) * kd
    L += dim_h(Xd(x0), Xd(x0 + 12.5), dy - 3, "12.5")
    L += dim_h(Xd(x0 + 12.5), Xd(x0 + 37.5), dy - 7, "25")
    dp = dowel_points(P)
    L += leader(Xd(dp[0][0]), Yd(dp[0][1]), Xd(dp[0][0]) + 2, dy + dw + 16, "9 x 8 H7, 100 PITCH")
    L += leader(Xd(x0 + 12.5), Yd(P["tile_y0"] + 12.5), Xd(x0) - 1, dy + dw + 22, "144 x M6", "start")
    s.add_notes("Detail A notes", ["Holes continue the field grid", "4 fixing holes, 7 mm, C'bore 11",
                                   "Tile 12.7 thick on 5.3 packers"], x=M + 4, y=dy + dw + 30, width=60)

    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 96, label="Isometric view", sublabel="Not to scale; worktop holes shown as a representative patch")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Worktop {Lt:,.0f} x {Dt:.0f} x {P['top_t']:.0f} birch ply, top at {H:.0f} ±{P['adjust']:.0f}",
        f"Grid {P['pitch']:.0f} pitch, first hole {P['edge']} from each edge; 1,152 positions",
        f"Field: 756 x {P['plain_d']} plain; 252 M6 on the 50 sub-grid: {len(TEE)} tee nuts from below, {len(SCREW)} screw-in over frame",
        f"Tile {t:.0f} x {t:.0f} x {P['tile_t']}, left edge {x0 + Lt / 2:.0f} from the worktop's left edge",
        f"Feet at {2 * D['lx']:,.0f} x {2 * D['ly']:.0f} centers; legs {P['leg']:.0f} square",
        f"Aprons {P['apron'][0]:.0f} x {P['apron'][1]:.0f}; cross rails {P['rail'][0]:.0f} x {P['rail'][1]:.0f} at X {', '.join(f'{v:g}' for v in P['cross_x'])}",
        "Ballast 2 x 12.9 kg slabs (GBN-CAL-001, C4)",
        "Toe clamp torque 1.6 N m max; one round + one diamond pin",
        "Levelling feet with 3 mm rubber pads",
        "All exposed edges chamfered or rounded 0.5 min",
        "Third-angle; front view from -Y; origin at worktop center",
    ], x=276, y=148, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "GBN-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
