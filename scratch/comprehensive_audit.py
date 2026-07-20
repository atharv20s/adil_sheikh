"""
Comprehensive Audit Script
===========================
Independently re-derives and verifies every metric in the paper.
"""
import math
from math import comb, floor, exp, log10

# =========================================================
# PART 1: Independent Re-derivation of Probability Model
# =========================================================

# Parameters from Sheikh et al. (2020)
x = 0.95       # per-sensor security level
m = 10          # critical sensor subset
n_sen = 3854    # total sensors
n_nodes = 51    # validators (50 EVs + 1 coordinator)
f_byz = 16      # floor((51-1)/3)
P_SCADA = 0.01
P_R = 0.01
y = 0.05        # MitM probability
z = 0.15        # Replay probability
p_dos = 0.20
p_ddos = 0.35
p_key = 0.01

print("=" * 80)
print("  PART 1: PROBABILITY MODEL AUDIT")
print("=" * 80)

# =========================================================
# A. WITHOUT BLOCKCHAIN (12 Attacks, m=10)
# =========================================================
print("\n--- A. Attack Probabilities WITHOUT Blockchain ---")

P_SA = x**m
P_FDI = x**m
P_CA = x**m
P_MitM = y
P_Replay = z
P_Sybil = 1.0
P_DoS = p_dos
P_DDoS = p_ddos
P_Byz = 1.0
P_Key = p_key
P_SCADA_atk = P_SCADA
P_R_atk = P_R

attacks_no_bc = {
    "Sensor (P_SA)": P_SA,
    "FDI (P_FDI)": P_FDI,
    "Communication (P_CA)": P_CA,
    "MitM": P_MitM,
    "Replay": P_Replay,
    "Sybil": P_Sybil,
    "DoS": P_DoS,
    "DDoS": P_DDoS,
    "Byzantine": P_Byz,
    "Key Compromise": P_Key,
    "SCADA": P_SCADA_atk,
    "Receiver": P_R_atk,
}

for name, prob in attacks_no_bc.items():
    print(f"  {name:30s} = {prob:.6f}")

# Full product (including Sybil=1 and Byz=1)
product_all = 1.0
for prob in attacks_no_bc.values():
    product_all *= (1.0 - prob)

P_compromise_no_bc = 1.0 - product_all
print(f"\n  P_Compromise_noBC (all 12) = {P_compromise_no_bc:.6f}")
print(f"  (Expected: 1.0 because Sybil=1 and Byz=1)")

# Limited (excluding Sybil and Byzantine)
attacks_limited = {k: v for k, v in attacks_no_bc.items() 
                   if k not in ["Sybil", "Byzantine"]}
product_limited = 1.0
for prob in attacks_limited.values():
    product_limited *= (1.0 - prob)

P_compromise_no_bc_limited = 1.0 - product_limited
print(f"  P_Compromise_noBC_limited  = {P_compromise_no_bc_limited:.6f}")
print(f"  (Paper claims: 0.982)")

# Manual computation
manual = 1.0 - (1-P_SA)**3 * (1-y) * (1-z) * (1-p_dos) * (1-p_ddos) * (1-p_key) * (1-P_SCADA) * (1-P_R)
print(f"  Manual computation:          {manual:.6f}")

# =========================================================
# B. WITH BLOCKCHAIN (12 Attacks, m=10)
# =========================================================
print("\n--- B. Attack Probabilities WITH Blockchain ---")

k1 = m * (m - 1) // 2  # = 45
k2 = floor(m * 0.33)    # = 3
p_c = 0.05  # validator compromise probability

P_SAb = x**(2*m)
P_FDI_BC = x**(2*m)
P_CAb = x**(2*k1)
P_MitM_BC = y**2
P_Replay_BC = 0.0
# Sybil with admission control
P_Sybil_BC = sum(comb(n_nodes, i) * p_c**i * (1-p_c)**(n_nodes-i) 
                 for i in range(f_byz+1, n_nodes+1))
P_DoS_BC = p_dos * ((f_byz + 1) / n_nodes)
P_DDoS_BC = p_ddos * ((f_byz + 1) / n_nodes)
P_Byz_BC = sum(comb(n_nodes, i) * p_c**i * (1-p_c)**(n_nodes-i) 
               for i in range(f_byz+1, n_nodes+1))
P_Key_BC = sum(comb(5, i) * P_R**i * (1-P_R)**(5-i) for i in range(3, 6))
P_SCADA_BC = (P_SCADA * x)**m
P_R_BC = P_R**k2 * x**m

attacks_bc = {
    "Sensor (P_SAb)": P_SAb,
    "FDI (P_FDI_BC)": P_FDI_BC,
    "Communication (P_CAb)": P_CAb,
    "MitM (P_MitM_BC)": P_MitM_BC,
    "Replay (P_Replay_BC)": P_Replay_BC,
    "Sybil (P_Sybil_BC)": P_Sybil_BC,
    "DoS (P_DoS_BC)": P_DoS_BC,
    "DDoS (P_DDoS_BC)": P_DDoS_BC,
    "Byzantine (P_Byz_BC)": P_Byz_BC,
    "Key (P_Key_BC)": P_Key_BC,
    "SCADA (P_SCADA_BC)": P_SCADA_BC,
    "Receiver (P_R_BC)": P_R_BC,
}

for name, prob in attacks_bc.items():
    print(f"  {name:30s} = {prob:.6e}")

product_bc = 1.0
for prob in attacks_bc.values():
    product_bc *= (1.0 - prob)

P_compromise_bc = 1.0 - product_bc
print(f"\n  P_Compromise_BC_static      = {P_compromise_bc:.6e}")
print(f"  (Paper claims: 5.99e-7)")

# Identify the DOMINANT term
print("\n  --- Dominant BC attack terms ---")
sorted_attacks = sorted(attacks_bc.items(), key=lambda x: x[1], reverse=True)
for name, prob in sorted_attacks[:5]:
    print(f"  {name:30s} = {prob:.6e}")

# =========================================================
# C. SECURITY GAIN
# =========================================================
print("\n--- C. Security Gain Calculation ---")
if P_compromise_bc > 0:
    gain = P_compromise_no_bc_limited / P_compromise_bc
    print(f"  Static Security Gain = {P_compromise_no_bc_limited:.6f} / {P_compromise_bc:.6e}")
    print(f"                       = {gain:.2e}")
else:
    print(f"  P_compromise_BC is 0 -> infinite gain")

# =========================================================
# PART 2: MESSAGE COMPLEXITY AUDIT 
# =========================================================
print("\n" + "=" * 80)
print("  PART 2: MESSAGE COMPLEXITY AUDIT")
print("=" * 80)

n = n_nodes  # 51
f = f_byz    # 16

# OM(m): sum_{k=0}^{f} n^k
om_msgs = sum(n**k for k in range(f+1))
om_msgs_formula = (n**(f+1) - 1) / (n - 1)
print(f"\n  OM(m): sum(n^k, k=0..f={f})")
print(f"    Exact:   {om_msgs}")
print(f"    Formula: {om_msgs_formula:.2e}")
print(f"    log10:   {log10(om_msgs):.1f}")
print(f"    Paper claims: ~1.05e28 (protocols.json says 1e18)")

# Classic PBFT: 3n^2 + n (pre-prepare + prepare + commit)
pbft_msgs = 3 * n**2 + n
print(f"\n  Classic PBFT: 3n^2 + n = 3*{n}^2 + {n}")
print(f"    = {pbft_msgs}")
print(f"    Paper claims: 7,854 (protocols.json: 7,803)")
# Alternative: 3*n*(n-1) + n = 3n^2 - 3n + n = 3n^2 - 2n
pbft_msgs_alt = 3*n*(n-1) + n
print(f"    Alt (3n(n-1)+n): {pbft_msgs_alt}")

# IBFT 2.0: Uses n_val = 21 committee
n_val_ibft = 21
ibft_msgs = 3 * n_val_ibft**2
print(f"\n  IBFT 2.0: 3*n_val^2 = 3*{n_val_ibft}^2")
print(f"    = {ibft_msgs}")
print(f"    Paper claims: 1,323")

# QBFT: Uses n_val = 17
n_val_qbft = 17
qbft_msgs_paper = 2 * n_val_qbft**2 + n_val_qbft
qbft_msgs_alt = 3 * n_val_qbft**2
print(f"\n  QBFT: 2*n_val^2 + n_val = 2*{n_val_qbft}^2 + {n_val_qbft}")
print(f"    = {qbft_msgs_paper}")
print(f"    Alt (3*n_val^2): {qbft_msgs_alt}")
print(f"    Paper claims: 595 (protocols.json: 675)")

# CE-PBFT: 3c^2 + c with c=25
c_ce = 25
ce_msgs = 3 * c_ce**2 + c_ce
print(f"\n  CE-PBFT: 3c^2 + c = 3*{c_ce}^2 + {c_ce}")
print(f"    = {ce_msgs}")
print(f"    Paper claims: 1,900 (protocols.json: 1,875)")

# G-PBFT: 3M^2 + M with M=30
M_g = 30
g_msgs = 3 * M_g**2 + M_g
print(f"\n  G-PBFT: 3M^2 + M = 3*{M_g}^2 + {M_g}")
print(f"    = {g_msgs}")
print(f"    Paper claims: 2,700")

# SV-PBFT: 3c^2 with c=20
c_sv = 20
sv_msgs = 3 * c_sv**2
print(f"\n  SV-PBFT: 3c^2 = 3*{c_sv}^2")
print(f"    = {sv_msgs}")
print(f"    Paper claims: 1,200")

# Tower BFT: n * S with S=25
s_tower = 25
tower_msgs = n * s_tower
print(f"\n  Tower BFT: n*S = {n}*{s_tower}")
print(f"    = {tower_msgs}")
print(f"    Paper claims: 1,275")

# RVR: n * S with S=20
s_rvr = 20
rvr_msgs = n * s_rvr
print(f"\n  RVR: n*S = {n}*{s_rvr}")
print(f"    = {rvr_msgs}")
print(f"    Paper claims: 1,020")

# =========================================================
# PART 3: COMMUNICATION OVERHEAD AUDIT
# =========================================================
print("\n" + "=" * 80)
print("  PART 3: COMMUNICATION OVERHEAD AUDIT")
print("=" * 80)

# CO = M_total / N_tx where N_tx = block_size = 50
block_size = 50

protocols_msgs = {
    "OM(m)": om_msgs,
    "Classic PBFT": pbft_msgs,
    "IBFT 2.0": ibft_msgs,
    "QBFT": qbft_msgs_paper,
    "CE-PBFT": ce_msgs,
    "G-PBFT": g_msgs,
    "SV-PBFT": sv_msgs,
    "Tower BFT": tower_msgs,
    "RVR": rvr_msgs,
}

paper_co = {
    "OM(m)": 2.1e26,
    "Classic PBFT": 154.0,
    "IBFT 2.0": 25.9,
    "QBFT": 11.6,
    "CE-PBFT": 37.2,
    "G-PBFT": 52.9,
    "SV-PBFT": 23.5,
    "Tower BFT": 25.0,
    "RVR": 20.0,
}

print(f"\n  CO = M_total / N_tx (block_size={block_size})")
print(f"  {'Protocol':<15} {'Computed CO':>15} {'Paper CO':>15} {'Match?':>10}")
print("  " + "-" * 60)
for proto, msgs in protocols_msgs.items():
    computed_co = msgs / block_size
    paper_val = paper_co[proto]
    match = "OK" if abs(computed_co - paper_val) / max(paper_val, 1e-10) < 0.05 else "MISMATCH"
    if proto == "OM(m)":
        print(f"  {proto:<15} {computed_co:>15.2e} {paper_val:>15.2e} {match:>10}")
    else:
        print(f"  {proto:<15} {computed_co:>15.1f} {paper_val:>15.1f} {match:>10}")

# =========================================================
# PART 4: LATENCY AUDIT
# =========================================================
print("\n" + "=" * 80)
print("  PART 4: LATENCY AUDIT")
print("=" * 80)

tau_ms = 50  # mean network delay

# OM(m): (f+1)*n*tau
om_latency = (f + 1) * n * tau_ms
print(f"\n  OM(m): (f+1)*n*tau = {f+1}*{n}*{tau_ms} = {om_latency} ms")
print(f"    Paper claims: 43,350 ms  ->  {'MATCH' if om_latency == 43350 else 'MISMATCH'}")

# Classic PBFT: 3*n*tau
pbft_latency = 3 * n * tau_ms
print(f"  Classic PBFT: 3*n*tau = 3*{n}*{tau_ms} = {pbft_latency} ms")
print(f"    Paper claims: 7,650 ms  ->  {'MATCH' if pbft_latency == 7650 else 'MISMATCH'}")

# Tower BFT: 2*tau (pipelined)
tower_latency = 2 * tau_ms  # Base: 2 network flights
tower_with_attack = tower_latency + 0 * 2.5 + (0/n) * 50  # f=0 for nominal
print(f"  Tower BFT (base): 2*tau = 2*{tau_ms} = {tower_latency} ms")
print(f"    Paper claims: 243 ms  ->  Check: 242.9 is used in code")
# Tower with f=0: 2*50 = 100ms. Paper says 243. Something doesn't add up.
# Let's check: tbft_latency_ms(51, 0, tau_s=0.05) = 2*50 = 100ms
# But paper says 242.9ms. There's a discrepancy.
print(f"  NOTE: tbft_latency_ms(n=51, f=0, tau=50ms) = {2*50+0+0} ms")
print(f"  But protocols.json says 242.9ms. Discrepancy!")

# =========================================================
# PART 5: THROUGHPUT AUDIT
# =========================================================
print("\n" + "=" * 80)
print("  PART 5: THROUGHPUT AUDIT")
print("=" * 80)

print(f"\n  TPS = block_size / (latency_ms / 1000)")
paper_latency = {
    "OM(m)": 43350, "Classic PBFT": 7650, "IBFT 2.0": 2500,
    "QBFT": 1500, "CE-PBFT": 800, "G-PBFT": 650,
    "SV-PBFT": 500, "Tower BFT": 243, "RVR": 200
}
paper_tps = {
    "OM(m)": 1.15, "Classic PBFT": 6.54, "IBFT 2.0": 20.0,
    "QBFT": 33.3, "CE-PBFT": 62.5, "G-PBFT": 76.9,
    "SV-PBFT": 100.0, "Tower BFT": 205.8, "RVR": 250.0
}

print(f"  {'Protocol':<15} {'Latency(ms)':>12} {'Computed TPS':>12} {'Paper TPS':>12} {'Match':>8}")
print("  " + "-" * 60)
for proto in paper_latency:
    lat = paper_latency[proto]
    computed_tps = block_size / (lat / 1000.0)
    paper_val = paper_tps[proto]
    match = "OK" if abs(computed_tps - paper_val) / max(paper_val, 0.001) < 0.02 else "MISMATCH"
    print(f"  {proto:<15} {lat:>12} {computed_tps:>12.2f} {paper_val:>12.2f} {match:>8}")

# =========================================================
# PART 6: SECURITY RANKING AUDIT
# =========================================================
print("\n" + "=" * 80)
print("  PART 6: SECURITY RANKING AUDIT")
print("=" * 80)

print(f"\n  P_secure = (1 - P_TAb)(1 - P_temporal)(1 - P_other)")
print(f"  Since P_TAb ~ 0: P_secure ~ (1 - P_temporal)(1 - 0.05)")
print(f"  P_temporal = 1 - exp(-lambda * L * P_TA)")
print(f"  Using P_TA = 0.005 (Sheikh, n_sen=3854), lambda=20")

lam = 20.0
P_TA = 0.005  # Sheikh model value
P_other = 0.05

print(f"\n  {'Protocol':<15} {'L(ms)':>8} {'lambda*L*PTA':>14} {'P_temporal':>12} {'P_secure':>10} {'Paper P_sec':>12}")
print("  " + "-" * 75)

paper_psecure = {
    "OM(m)": 0.012, "Classic PBFT": 0.442, "IBFT 2.0": 0.740,
    "QBFT": 0.818, "CE-PBFT": 0.877, "G-PBFT": 0.890,
    "SV-PBFT": 0.904, "Tower BFT": 0.927, "RVR": 0.940
}

for proto in paper_latency:
    lat = paper_latency[proto]
    exponent = lam * (lat / 1000.0) * P_TA
    p_temp = 1.0 - exp(-exponent)
    p_sec = (1.0 - p_temp) * (1.0 - P_other)
    paper_val = paper_psecure[proto]
    match = "OK" if abs(p_sec - paper_val) < 0.005 else "MISMATCH"
    print(f"  {proto:<15} {lat:>8} {exponent:>14.4f} {p_temp:>12.4f} {p_sec:>10.4f} {paper_val:>12.3f}  {match}")

# Check: does higher CO always correspond to higher security?
print("\n  --- Security vs Communication Overhead Check ---")
print(f"  {'Protocol':<15} {'P_secure':>10} {'CO':>15} {'Latency(ms)':>12}")
print("  " + "-" * 55)
for proto in paper_latency:
    lat = paper_latency[proto]
    p_temp = 1.0 - exp(-lam * (lat/1000.0) * P_TA)
    p_sec = (1.0 - p_temp) * (1.0 - P_other)
    co = paper_co.get(proto, 0)
    co_str = f"{co:.2e}" if co > 1000 else f"{co:.1f}"
    print(f"  {proto:<15} {p_sec:>10.4f} {co_str:>15} {lat:>12}")

# =========================================================
# PART 7: INCONSISTENCY IN protocols.json MSG COUNTS
# =========================================================
print("\n" + "=" * 80)
print("  PART 7: protocols.json vs Paper Table C MESSAGE COUNT COMPARISON")
print("=" * 80)

json_msgs = {
    "OM(m)": 1e18,
    "Classic PBFT": 7803,
    "IBFT 2.0": 1323,
    "QBFT": 675,
    "CE-PBFT": 1875,
    "G-PBFT": 2700,
    "SV-PBFT": 1200,
    "Tower BFT": 1275,
    "RVR": 1020,
}

paper_table_msgs = {
    "OM(m)": 1.05e28,
    "Classic PBFT": 7854,
    "IBFT 2.0": 1323,
    "QBFT": 595,
    "CE-PBFT": 1900,
    "G-PBFT": 2700,
    "SV-PBFT": 1200,
    "Tower BFT": 1275,
    "RVR": 1020,
}

print(f"\n  {'Protocol':<15} {'Re-derived':>15} {'protocols.json':>15} {'Paper Table C':>15}")
print("  " + "-" * 65)
for proto in protocols_msgs:
    rd = protocols_msgs[proto]
    js = json_msgs[proto]
    pt = paper_table_msgs[proto]
    rd_str = f"{rd:.2e}" if rd > 1e6 else f"{rd}"
    js_str = f"{js:.2e}" if js > 1e6 else f"{int(js)}"
    pt_str = f"{pt:.2e}" if pt > 1e6 else f"{int(pt)}"
    print(f"  {proto:<15} {rd_str:>15} {js_str:>15} {pt_str:>15}")

# =========================================================
# PART 8: "BLOCKCHAIN WORSE THAN NO BLOCKCHAIN" BUG CHECK
# =========================================================
print("\n" + "=" * 80)
print("  PART 8: DOES BLOCKCHAIN ALWAYS IMPROVE SECURITY?")
print("=" * 80)

# The intrusion_detection_bft_paper uses a 12-attack model with m=10
# Without BC: P_compromise_limited = 0.982
# With BC: P_compromise_BC_static = 5.99e-7
# This always shows BC is better.

# The paper1 uses Sheikh's original 4-attack model with n_sen=3854
# Without BC: P_TA = 0.005
# With BC: P_TAb ~ 10^-173
# This also always shows BC is better.

# But the TEMPORAL model can cause issues:
# P_secure_noBC = some baseline over 60s window
# P_secure_BC = depends on consensus latency

# For No-BC over 60s at lambda=20:
P_TA_nobc = 0.005
p_nobc_60s = 1.0 - exp(-20 * 60 * P_TA_nobc)
ps_nobc = (1.0 - p_nobc_60s) * (1.0 - 0.05)
print(f"\n  No-BC P_secure (60s window, lambda=20): {ps_nobc:.6f}")

# For OM(m) BC:
p_temp_om = 1.0 - exp(-20 * 43.35 * P_TA_nobc)
ps_om = (1.0 - p_temp_om) * (1.0 - 0.05)
print(f"  OM(m) P_secure (43.35s window, lambda=20): {ps_om:.4f}")
print(f"  OM(m) is {'BETTER' if ps_om > ps_nobc else 'WORSE'} than No-BC")
print(f"  Improvement factor: {ps_om/ps_nobc:.1f}x")

# For Tower BFT:
p_temp_tower = 1.0 - exp(-20 * 0.243 * P_TA_nobc)
ps_tower = (1.0 - p_temp_tower) * (1.0 - 0.05)
print(f"  Tower BFT P_secure (0.243s window, lambda=20): {ps_tower:.4f}")
print(f"  Tower BFT is {'BETTER' if ps_tower > ps_nobc else 'WORSE'} than No-BC")
print(f"  Improvement factor: {ps_tower/ps_nobc:.1f}x")

print("\n  CONCLUSION: The temporal model correctly shows BC is always better")
print("  because the consensus window (max 43s) < 60s observation window,")
print("  and additionally BC eliminates static vulnerability.")

# =========================================================
# PART 9: ORIGINAL SHEIKH EQUATIONS CHECK  
# =========================================================
print("\n" + "=" * 80)
print("  PART 9: SHEIKH et al. ORIGINAL EQUATIONS (n_sen=3854)")
print("=" * 80)

# Sheikh Eq 14-16: Without blockchain
P_SA_sheikh = x**n_sen  # ~10^-86
P_CA_sheikh = x**n_sen
P_TA_sheikh = 0.25 * (2*P_SA_sheikh + P_SCADA + P_R)
print(f"\n  P_SA = x^3854 = {P_SA_sheikh:.2e}")
print(f"  P_CA = x^3854 = {P_CA_sheikh:.2e}")
print(f"  P_TA = (1/4)(2*P_SA + P_SCADA + P_R) = {P_TA_sheikh:.6f}")

# Sheikh Eq 17-21: With blockchain
k1_sheikh = n_sen * (n_sen - 1) // 2  # 7,426,681
k2_sheikh = floor(n_sen * 0.33)  # 1,271

P_SAb_sheikh = x**(2*n_sen)
P_CAb_sheikh = x**(2*k1_sheikh)
P_SCADAb_sheikh = (P_SCADA * x)**n_sen
P_Rb_sheikh = P_R**k2_sheikh * x**n_sen

P_TAb_sheikh = 0.25 * (P_SAb_sheikh + P_CAb_sheikh + P_SCADAb_sheikh + P_Rb_sheikh)

print(f"\n  k1 = n_sen*(n_sen-1)/2 = {k1_sheikh}")
print(f"  k2 = floor(n_sen*0.33) = {k2_sheikh}")
print(f"  P_SAb = x^(2*3854) = x^{2*n_sen}")
print(f"  log10(P_SAb) = {2*n_sen*log10(x):.0f}")
print(f"  P_CAb = x^(2*k1) = x^{2*k1_sheikh}")
print(f"  log10(P_CAb) = {2*k1_sheikh*log10(x):.0f}")
print(f"  P_SCADAb = (P_SCADA*x)^3854")
print(f"  log10(P_SCADAb) = {n_sen*log10(P_SCADA*x):.0f}")
print(f"  P_Rb = P_R^1271 * x^3854")
print(f"  log10(P_Rb) = {k2_sheikh*log10(P_R) + n_sen*log10(x):.0f}")
print(f"  P_TAb ~ 10^{log10(0.25) + max(2*n_sen*log10(x), 2*k1_sheikh*log10(x), n_sen*log10(P_SCADA*x), k2_sheikh*log10(P_R)+n_sen*log10(x)):.0f}")

# =========================================================
# PART 10: IMPLEMENTATION vs PAPER COMPARISON
# =========================================================
print("\n" + "=" * 80)
print("  PART 10: probabilistic_model.py vs PAPER EQUATIONS")
print("=" * 80)

# The code's p_ta_no_blockchain uses WEIGHTED sum, not equal weights
# Paper 1 uses equal weights (1/4 each)
# intrusion_detection_bft_paper uses different model (12 attacks)
print("\n  The code has TWO different models:")
print("  1. p_ta_no_blockchain() - Sheikh's 4-component weighted model")
print("     Uses: w_s*P_SA + w_c*P_CA + w_sc*P_SCADA + w_r*P_R")
print("     Default weights: (0.20, 0.10, 0.40, 0.30)")
print("     Equal weights:   (0.25, 0.25, 0.25, 0.25)")
print()
print("  2. intrusion_detection paper - 12-attack parallel failure model")
print("     Uses: P_Compromise = 1 - Product(1 - P_i)")
print()
print("  CRITICAL: The implementation does NOT directly compute")
print("  P_Compromise = 1 - Product(1-P_i) for the 12-attack model!")
print("  Instead, verify_paper_values.py and generate_ieee_figures.py")
print("  use the 4-component Sheikh model for temporal calculations.")
print("  This means the temporal P_secure values in the tables are")
print("  computed using P_TA = 0.005, not P_TA based on 12 attacks!")
