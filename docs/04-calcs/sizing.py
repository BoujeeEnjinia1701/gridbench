"""GridBench sizing calculations, GBN-CAL-001 v0.2 (TRL 3; revised under GBN-DDR-002).

Run from the repo root:  python docs/04-calcs/sizing.py
Imports PARAMS and the derived dimensions from cad/src/model.py, reads bom/bom.csv and
budget_usd from project.yaml, and prints every number quoted in docs/04-calcs/01-sizing.md.
Each printed line carries a tag such as [C2] that the note cites. First-principles estimates
for a paper proof of concept; the assumptions are listed in the note (Table 1).
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, classify, dowel_points, fixing_points, grid_points, insert_kinds  # noqa: E402

G = 9.81
D = derived(P)
OUT = []


def say(tag, text):
    line = f"[{tag}] {text}"
    OUT.append(line)
    print(line)


# ---------------- assumptions (Table 1 of the note) ----------------
RHO_SOFT, RHO_PLY, RHO_AL, RHO_CONC = 500.0, 680.0, 2700.0, 2300.0    # kg/m3
E_PLY = 7000.0          # MPa, birch plywood, mean of the two in-plane directions (assumption)
NU = 0.3                # isotropic plate approximation
E_SOFT = 8000.0         # MPa, C16 softwood mean modulus
F_M_SOFT = 16.0         # MPa, C16 characteristic bending strength
E_AL = 69000.0          # MPa
ALPHA_AL, ALPHA_PETG = 23e-6, 60e-6    # 1/K
MOIST_COEF = 0.007e-2   # plywood in-plane strain per 1 % moisture content (assumption, unsourced)
EMC = {20: 4.5, 40: 7.7, 60: 11.0, 80: 16.0}   # % at 21 °C, USDA Wood Handbook Table 4-2
CNC_POS = 0.10          # mm, shared CNC router hole position (assumption)
TEMPLATE_STEP = 0.10    # mm per indexing step of a printed drilling template (assumption)
TEMPLATE_SPAN = 200.0   # mm covered per template placement
K_NUT = (0.15, 0.20, 0.25)   # nut factor, low, nominal, high
T_CLAMP = 1.6           # N m, rated clamp screw torque (this note)
PETG_SUSTAINED = 12.0   # MPa, allowable sustained bending stress for printed PETG (assumption)
INSERT_TAU = (2.5, 4.0) # MPa, effective shear strength of plywood around a screw-in insert (assumption)
PLY_BEARING = 10.0      # MPa, plywood bearing strength perpendicular to the face under a tee-nut flange (assumption)
MU_FEET = (0.2, 0.5)    # friction, levelling feet on a workshop floor: hard plastic, rubber
MU_RUBBER = MU_FEET[1]  # rubber pads on the feet (GBN-DDR-002)
PUSH, PUSH_H = 150.0, P["h"]   # N at the top edge (R12)
POINT = 500.0           # N (R6)
DIST_KG = 150.0         # kg (R6)
T_ROOM = 10.0           # K, workshop temperature swing considered

# ---------------- A. Grid (R1) ----------------
tile, ins, plain = classify(P)
pts = grid_points(P)
say("A1", f"grid {D['nx']} x {D['ny']} = {len(pts)} positions: {len(tile)} tile, {len(ins)} inserts, {len(plain)} plain; "
          f"first hole {P['edge']:.1f} mm from each edge; last {P['top_l'] / 2 - max(x for *_, x, _ in pts):.1f} mm")
x0 = P["tile_x0"]
off = ((x0 + P["top_l"] / 2 - P["edge"]) / P["pitch"]) % 1
first = min(x for x, y in tile) - x0
say("A2", f"tile edge falls midway between grid lines ({off * P['pitch']:.1f} mm); first tile hole {first:.1f} mm from the tile edge, "
          f"so the 144 tile holes continue the field grid")
dmin = min(math.dist(a, b) for a in dowel_points(P) for b in tile)
say("A3", f"dowel bore to nearest M6 hole {dmin:.1f} mm between centers; ligament {dmin - P['dowel_d'] / 2 - 3.0:.1f} mm")
fmin = min(math.dist(a, b) for a in fixing_points(P) for b in tile)
say("A4", f"fixing counterbore to nearest M6 hole {fmin:.1f} mm; ligament {fmin - P['cbore_d'] / 2 - 3.0:.1f} mm")
lig_ply = (P["pitch"] - P["plain_d"]) / P["pitch"]
say("A5", f"plywood ligament efficiency (25 - 6.6) / 25 = {lig_ply:.3f}; tile (25 - 5.0) / 25 = {(P['pitch'] - P['tap_drill_d']) / P['pitch']:.3f}")

# ---------------- B. Mass and center of mass ----------------
leg, (aw, ah), (rw, rh) = P["leg"], P["apron"], P["rail"]
m_leg = 4 * leg * leg * D["leg_h"]
m_apr = 2 * D["long_apron_len"] * aw * ah + 2 * D["end_apron_len"] * aw * ah
m_rail = len(P["cross_x"]) * D["rail_len"] * rw * rh + 2 * D["low_rail_len"] * rw * rh
m_pack = 2 * rw * P["tile"] * D["packer_t"]
V_frame = (m_leg + m_apr + m_rail + m_pack) * 1e-9
mass = {}
mass["frame"] = V_frame * RHO_SOFT
tee_pts, screw_pts = insert_kinds(P)
holes_v = (len(plain) * math.pi / 4 * P["plain_d"] ** 2 + len(screw_pts) * math.pi / 4 * P["insert_hole_d"] ** 2
           + len(tee_pts) * math.pi / 4 * P["tee_hole_d"] ** 2) * P["top_t"]
mass["worktop"] = ((P["top_l"] * P["top_d"] - P["tile"] ** 2) * P["top_t"] - holes_v) * 1e-9 * RHO_PLY
tile_holes = (len(tile) * math.pi / 4 * P["tap_drill_d"] ** 2 + 9 * math.pi / 4 * P["dowel_d"] ** 2) * P["tile_t"]
mass["tile"] = (P["tile"] ** 2 * P["tile_t"] - tile_holes) * 1e-9 * RHO_AL
sl, sd, st = D["shelf"]
mass["shelf"] = sl * sd * st * 1e-9 * RHO_PLY
mass["inserts, feet, fasteners"] = len(ins) * 0.004 + 4 * 0.15 + 0.8
mass["fixtures, post, indicator"] = 0.6 + 0.8 + 0.3
m_empty = sum(mass.values())
m_slab = math.prod(P["slab"]) * 1e-9 * RHO_CONC
say("B1", "masses kg: " + ", ".join(f"{k} {v:.1f}" for k, v in mass.items()) + f"; bench {m_empty:.1f} kg")
say("B2", f"ballast slab {m_slab:.1f} kg each, two {2 * m_slab:.1f} kg; bench with ballast {m_empty + 2 * m_slab:.1f} kg")
# center of mass height (for the record; tipping about the feet uses plan offsets only)
z_items = [(mass["frame"], 0.55 * P["h"]), (mass["worktop"], P["h"] - 9), (mass["tile"], P["h"] - 6),
           (mass["shelf"], D["shelf_z"] + 6), (mass["inserts, feet, fasteners"], 400), (mass["fixtures, post, indicator"], P["h"] + 60)]
zc = sum(m * z for m, z in z_items) / m_empty
say("B3", f"center of mass about {zc:.0f} mm above the floor, empty")

# ---------------- C. Tipping and sliding (R12) ----------------
b_y = D["ly"]                                # feet at +/- ly; push front to back is the short base
def f_tip(m, b=b_y):
    return m * G * b / PUSH_H
say("C1", f"feet {D['foot_base_x']:.0f} x {D['foot_base_y']:.0f} mm (centers); lever for a front push {b_y:.0f} mm, push height {PUSH_H:.0f} mm")
say("C2", f"tipping force empty {f_tip(m_empty):.0f} N (target {PUSH:.0f} N); along the bench {f_tip(m_empty, D['lx']):.0f} N")
m_need = PUSH * PUSH_H / (G * b_y)
say("C3", f"mass needed for {PUSH:.0f} N: {m_need:.1f} kg, so ballast of at least {m_need - m_empty:.1f} kg")
m_bal = m_empty + 2 * m_slab
say("C4", f"with two slabs: tipping force {f_tip(m_bal):.0f} N, factor {f_tip(m_bal) / PUSH:.2f} on 150 N")
say("C5", f"sliding force on hard feet (mu {MU_FEET[0]}): empty {MU_FEET[0] * m_empty * G:.0f} N, ballasted {MU_FEET[0] * m_bal * G:.0f} N; "
          f"on the adopted rubber pads (mu {MU_RUBBER}): empty {MU_RUBBER * m_empty * G:.0f} N, ballasted {MU_RUBBER * m_bal * G:.0f} N")
a_h = D["z_under"] - 20
f_anchor = max(0.0, (PUSH * PUSH_H - m_empty * G * b_y) / a_h)
say("C6", f"wall anchor (optional) tie force for a 150 N pull on the empty bench: {f_anchor:.0f} N at {a_h:.0f} mm")

# ---------------- D. Stiffness and strength (R6) ----------------
def plate_D(E, t):
    return E * t ** 3 / (12 * (1 - NU ** 2))
bays = sorted([-D["end_apron_x"]] + list(P["cross_x"]) + [D["end_apron_x"]])
spans = [b - a for a, b in zip(bays, bays[1:])]
a_bay = max(s for s, (a, b) in zip(spans, zip(bays, bays[1:])) if not (a >= x0 - 1 and b <= x0 + P["tile"] + 1)) - rw
b_bay = D["rail_span"] - aw
# Timoshenko, simply supported plate, central point load: w = alpha P a^2 / D; alpha for b/a
ALPHA_P = [(1.0, 0.01160), (1.2, 0.01353), (1.4, 0.01484), (1.6, 0.01570), (1.8, 0.01620), (2.0, 0.01651), (3.0, 0.01690)]
ALPHA_Q = [(1.0, 0.00406), (1.2, 0.00564), (1.4, 0.00705), (1.6, 0.00830), (1.8, 0.00931), (2.0, 0.01013), (3.0, 0.01223)]
def interp(tab, r):
    for (r1, a1), (r2, a2) in zip(tab, tab[1:]):
        if r1 <= r <= r2:
            return a1 + (a2 - a1) * (r - r1) / (r2 - r1)
    return tab[-1][1]
ratio = b_bay / a_bay
Dp = plate_D(E_PLY * lig_ply, P["top_t"])
w_plate = interp(ALPHA_P, ratio) * POINT * a_bay ** 2 / Dp
say("D1", f"largest plywood bay {a_bay:.0f} x {b_bay:.0f} mm clear (b/a {ratio:.2f}); plate stiffness with holes {Dp / 1e6:.2f} kN m")
say("D2", f"local worktop deflection, 500 N at bay center: {w_plate:.2f} mm (TRL 2 strip estimate 0.41 mm)")
I_rail = rw * rh ** 3 / 12
w_rail = (POINT / 2) * D["rail_span"] ** 3 / (48 * E_SOFT * I_rail)
say("D3", f"each of the two bay cross rails takes about 250 N: deflection {w_rail:.2f} mm, adds {w_rail:.2f} mm at bay center")
def apron_defl(F_each, a, span, I):
    # simply supported, point load at distance a from one support, deflection at the load
    bb = span - a
    return F_each * a ** 2 * bb ** 2 / (3 * E_SOFT * I * span)
span_ap = D["apron_span"]
I_ap = aw * ah ** 3 / 12
a_load = span_ap / 2 - 150.0          # bay center at x = -150, measured from the left leg
w_ap = apron_defl(POINT / 2, a_load, span_ap, I_ap)
say("D4", f"long apron 45 x {ah:.0f} over {span_ap:.0f} mm between legs: {w_ap:.2f} mm under 250 N at the bay")
w_tot = w_plate + w_rail + w_ap
say("D5", f"total at the worst bay center: {w_tot:.2f} mm (target 0.5 mm); worktop relative to its supports {w_plate:.2f} mm")
for tag, h_alt in (("D6", 95.0), ("D7", 145.0)):
    w_alt = apron_defl(POINT / 2, a_load, span_ap, aw * h_alt ** 3 / 12)
    say(tag, f"for comparison, 45 x {h_alt:.0f} aprons: apron {w_alt:.2f} mm, total {w_plate + w_rail + w_alt:.2f} mm")
q = DIST_KG * G / (P["top_l"] * P["top_d"])
w_q = interp(ALPHA_Q, ratio) * q * a_bay ** 4 / Dp
W_ap = (DIST_KG * G + mass["worktop"] * G + mass["tile"] * G) / 2
w_ap_q = 5 * (W_ap / span_ap) * span_ap ** 4 / (384 * E_SOFT * I_ap)
M_ap = (W_ap / span_ap) * span_ap ** 2 / 8
sig_ap = M_ap / (aw * ah ** 2 / 6)
say("D8", f"150 kg spread: {q * 1000:.2f} kPa; plate {w_q:.3f} mm; each long apron {w_ap_q:.2f} mm, stress {sig_ap:.1f} MPa "
          f"(C16 f_m,k {F_M_SOFT:.0f} MPa, ratio {F_M_SOFT / sig_ap:.1f})")
leg_stress = (DIST_KG + m_empty) * G / 4 / (leg * leg)
say("D9", f"leg compression {leg_stress:.2f} MPa per leg")
I_tile = P["tile"] * P["tile_t"] ** 3 / 12 * (P["pitch"] - P["tap_drill_d"]) / P["pitch"]
span_tile = P["cross_x"][3] - P["cross_x"][2]
w_tile = POINT * span_tile ** 3 / (48 * E_AL * I_tile)
sig_tile = POINT * span_tile / 4 / (I_tile / (P["tile_t"] / 2))
say("D10", f"tile over {span_tile:.0f} mm between packers, 500 N at center: {w_tile:.3f} mm, stress {sig_tile:.1f} MPa")
sh_span = 2 * D["ly"]
I_sh = sl * st ** 3 / 12
w_sh = 5 * (2 * m_slab * G) * sh_span ** 3 / (384 * E_PLY * I_sh)
say("D11", f"shelf under {2 * m_slab:.0f} kg of slabs, spread, {sh_span:.0f} mm span: {w_sh:.2f} mm")

# ---------------- E. Moisture and temperature (R3, R4) ----------------
mc_mid = (EMC[40] + EMC[60]) / 2
mc_half = (EMC[60] - EMC[40]) / 2
e_moist = mc_half * MOIST_COEF * 1000.0
say("E1", f"EMC at 40 and 60 % RH: {EMC[40]} and {EMC[60]} %; built at {mc_mid:.2f} %, swing +/-{mc_half:.2f} %")
say("E2", f"plywood field over 1,000 mm: +/-{e_moist:.3f} mm from moisture (coefficient {MOIST_COEF * 100:.3f} % per % MC, unsourced)")
e_full = (EMC[80] - EMC[20]) / 2 * MOIST_COEF * 1000.0
say("E3", f"over the full 20 to 80 % RH operating range: +/-{e_full:.2f} mm over 1,000 mm")
cnc = CNC_POS + e_moist
steps = 1000.0 / TEMPLATE_SPAN
tpl_wc = steps * TEMPLATE_STEP + e_moist
tpl_rss = math.sqrt(steps) * TEMPLATE_STEP + e_moist
say("E4", f"hole to hole over 1,000 mm: CNC {cnc:.2f} mm (target 0.3); template worst case {tpl_wc:.2f} mm, "
          f"statistical {tpl_rss:.2f} mm (target 0.5)")
g_tile = ALPHA_AL * P["tile"] * T_ROOM
say("E5", f"tile growth {g_tile:.3f} mm over 300 mm per {T_ROOM:.0f} K; across the 200 mm dowel span {ALPHA_AL * 200 * T_ROOM:.3f} mm")
mis = (ALPHA_PETG - ALPHA_AL) * P["dowel_pitch"] * 2 * T_ROOM
say("E6", f"PETG fixture with pins 200 mm apart against the tile: {mis:.3f} mm mismatch per {T_ROOM:.0f} K")

# ---------------- F. Dowel location (R4) ----------------
c_min, c_max = 0.0, 0.015 + 0.009       # H7 (0/+0.015) with h6 (0/-0.009) at 8 mm
say("F1", f"8 mm H7/h6 diametral clearance {c_min:.3f} to {c_max:.3f} mm")
pitch_err = 0.05 + 0.05
say("F2", f"two round pins need pitch error below the clearance ({c_min:.3f} mm minimum); tile +/-0.05 plus fixture +/-0.05 gives up to "
          f"{pitch_err:.2f} mm, so two round pins can bind: use one round and one diamond pin")
L_pin = 2 * P["dowel_pitch"]
rot = c_max / L_pin
wc = c_max + rot * 100.0
rss = math.sqrt((c_max / 2) ** 2 + (rot * 100.0 / 2) ** 2) * 2 / math.sqrt(3)
say("F3", f"relocation at a point 100 mm from the round pin, pins {L_pin:.0f} mm apart: worst case {wc:.3f} mm, "
          f"typical (uniform clearances, RSS) {rss:.3f} mm; target 0.03 mm")

# ---------------- G. Clamps and inserts (R7) ----------------
cl, cw, ct = P["clamp"]
a_toe = cl / 2 - 5.0           # screw to toe contact
b_heel = cl / 2 - 7.0          # screw to heel center
share = b_heel / (a_toe + b_heel)
Zc = (cw - P["clamp_slot"]) * ct ** 2 / 6
say("G1", f"toe clamp: screw to toe {a_toe:.0f} mm, to heel {b_heel:.0f} mm; part gets {share:.3f} of screw tension; section modulus {Zc:.0f} mm3")
for k in K_NUT:
    F = T_CLAMP * 1000 / (k * 6.0)
    Fp = F * share
    sig = Fp * a_toe / Zc
    say(f"G2-{k}", f"K {k}: screw {F:.0f} N, part {Fp:.0f} N, clamp stress {sig:.1f} MPa")
F_lo = T_CLAMP * 1000 / (K_NUT[2] * 6.0) * share
F_hi = T_CLAMP * 1000 / (K_NUT[0] * 6.0)
sig_hi = F_hi * share * a_toe / Zc
Z16 = (cw - P["clamp_slot"]) * 16 ** 2 / 6
F2 = 2000 / (0.2 * 6.0)
say("G3", f"TRL 2 clamp (16 mm deep, 2 N m, K 0.2): part {F2 * share:.0f} N, stress {F2 * share * a_toe / Z16:.0f} MPa, "
          f"above the {PETG_SUSTAINED:.0f} MPa sustained limit")
say("G4", f"rated 1.6 N m: part force {F_lo:.0f} to {F_hi * share:.0f} N (target 500 N); peak stress {sig_hi:.1f} MPa "
          f"against {PETG_SUSTAINED:.0f} MPa")
A_ins = math.pi * P["insert_od"] * P["insert_len"]
cap = [t * A_ins for t in INSERT_TAU]
say("G5", f"insert pull-out, shear on {A_ins:.0f} mm2: {cap[0] / 1000:.2f} to {cap[1] / 1000:.2f} kN; "
          f"screw tension up to {F_hi / 1000:.2f} kN; factor {cap[0] / F_hi:.2f} to {cap[1] / F_hi:.2f}")
say("G5b", f"insert positions: {len(tee_pts)} flanged tee nuts from the underside, {len(screw_pts)} screw-in inserts "
           f"where a frame member lies within {P['tee_flange_d'] / 2:.1f} mm of the hole")
A_punch = math.pi * P["tee_flange_d"] * P["top_t"]
cap_t = [t * A_punch for t in INSERT_TAU]
A_bear = math.pi / 4 * (P["tee_flange_d"] ** 2 - P["tee_hole_d"] ** 2)
say("G5c", f"tee nut pull-through, shear on {A_punch:.0f} mm2 around the {P['tee_flange_d']:.0f} mm flange: {cap_t[0] / 1000:.2f} to "
           f"{cap_t[1] / 1000:.2f} kN; factor {cap_t[0] / F_hi:.2f} to {cap_t[1] / F_hi:.2f} on {F_hi / 1000:.2f} kN")
say("G5d", f"flange bearing on {A_bear:.0f} mm2: {F_hi / A_bear:.1f} MPa at {F_hi / 1000:.2f} kN against {PLY_BEARING:.0f} MPa "
           f"(factor {PLY_BEARING / (F_hi / A_bear):.2f}); thread engagement {P['tee_barrel_len']:.1f} mm")
T_light = cap[0] * K_NUT[0] * 6.0 / 1000
say("G5e", f"screw-in positions over the frame, light-duty option: torque {T_light:.2f} N m keeps screw tension within "
           f"{cap[0] / 1000:.2f} kN; part force {T_light * 1000 / (K_NUT[2] * 6.0) * share:.0f} to {T_light * 1000 / (K_NUT[0] * 6.0) * share:.0f} N")
say("G6", f"M6 in the tile: thread engagement {P['tile_t']:.1f} mm, more than twice the 6 mm diameter")

# ---------------- H. Fixture change (R8) ----------------
ENGAGE = 12.0           # mm of thread engaged per clamping screw (M6 x 20 through an 8 mm fixture base)
turns = ENGAGE / 1.0
t_screw = turns / 2.0 + 3
t_change = 4 * t_screw + 10 + 10
say("H1", f"fixture change: 4 screw operations at {t_screw:.0f} s ({turns:.0f} turns at 2 turns/s plus 3 s to engage), 10 s lift and place, "
          f"10 s to seat on pins: {t_change:.0f} s (target 60 s)")

# ---------------- I. Buildability (R9) ----------------
prints = {"toe clamp": (cl, ct + 40), "fence segment": P["fence_seg"][:2], "V-block": P["vblock"][:2], "post foot": P["post_foot"][:2]}
big = max(max(v) for v in prints.values())
say("I1", f"largest printed footprint {big:.0f} mm (fence segment); bed 200 mm; the TRL 2 fence was 400 mm")
t_tile = len(tile) * (0.5 + 1.0) / 60 + 9 * 3 / 60 + 4 * 2 / 60
say("I2", f"tile machining by drill press and tapping guide: about {t_tile:.1f} h "
          f"({len(tile)} holes at 1.5 min, 9 reamed bores at 3 min, 4 counterbores)")

# ---------------- K. Timber and cost (R10) ----------------
AP = f"45 x {ah:.0f}"
rates = {"70 x 70": 4.50, AP: 2.80, "45 x 70": 1.80}
lengths = {"70 x 70": 4 * D["leg_h"] / 1000, AP: (2 * D["long_apron_len"] + 2 * D["end_apron_len"]) / 1000,
           "45 x 70": (len(P["cross_x"]) * D["rail_len"] + 2 * D["low_rail_len"]) / 1000}
timber = sum(lengths[k] * rates[k] for k in rates)
frame_cost = timber * 1.10 + 9.0
say("K1", "timber by section: " + ", ".join(f"{k} {v:.2f} m" for k, v in lengths.items())
          + f"; total {sum(lengths.values()):.1f} m")
say("K2", f"frame cost {timber:.2f} + 10 % waste + $9 hardware = ${frame_cost:.2f}")
import yaml  # noqa: E402
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
tot = {"core": 0.0, "user-supplied": 0.0, "optional": 0.0}
for r in rows:
    c = float(r["qty"]) * float(r["unit_cost_usd"])
    tot[r["make_buy"] if r["make_buy"] in ("user-supplied", "optional") else "core"] += c
say("K2b", f"threaded inserts: {len(tee_pts)} tee nuts at $0.12 and {len(screw_pts)} screw-in at $0.10 = "
           f"${len(tee_pts) * 0.12 + len(screw_pts) * 0.10:.2f}")
alt = 220.0   # the TRL 3 v0.1 budget, for comparison
say("K3", f"BOM {len(rows)} lines; core parts ${tot['core']:.2f}; user-supplied indicator ${tot['user-supplied']:.2f}; "
          f"optional anchor ${tot['optional']:.2f}; everything ${sum(tot.values()):.2f}")
say("K4", f"against budget_usd ${budget:.0f}: core {tot['core'] / budget * 100 - 100:+.1f} % (${budget - tot['core']:.2f} spare), "
          f"everything {sum(tot.values()) / budget * 100 - 100:+.1f} %; against the former ${alt:.0f}: core {tot['core'] / alt * 100 - 100:+.1f} %")
say("K5", f"TRL 2 total $239.20 (with indicator); CAL-001 v0.1 core $239.20; now (core plus indicator) ${tot['core'] + tot['user-supplied']:.2f}")

if __name__ == "__main__":
    (Path(__file__).parent / "sizing-output.txt").write_text("\n".join(OUT) + "\n")
