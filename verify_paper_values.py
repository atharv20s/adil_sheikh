"""Verify P_secure values for both papers."""
from probabilistic_model import *

print("=" * 72)
print("  PAPER 1 & 2: P_secure Verification for All 9 Protocols")
print("=" * 72)

# Protocol data from protocols.json
protocols = [
    ("OM(m)",        43350.0, None),
    ("Classic PBFT",  7650.0, None),
    ("IBFT 2.0",      2500.0, None),
    ("QBFT",          1500.0, None),
    ("CE-PBFT",        800.0, None),
    ("G-PBFT",         650.0, None),
    ("SV-PBFT",        500.0, None),
    ("Tower BFT",      242.9, None),
    ("RVR",            200.0, "vrf"),
]

x = 0.95
n_sen = N_SEN  # 3854 (Sheikh's full count)
lambda_fdi = 20.0
p_other = 0.05

# Without blockchain
p_ta_val = p_ta_no_blockchain(x, n_sen=n_sen, weights=None)
print(f"\nP_TA (without blockchain, x=0.95): {p_ta_val:.6f}")

# With blockchain (same for all protocols except RVR)
p_tab_val = p_tab_blockchain(x, n_sen=n_sen, weights=None)
log10_ptab = log10_p_tab_blockchain(x, n_sen=n_sen, weights=None)
print(f"P_TAb (with blockchain, x=0.95): ~10^{log10_ptab:.0f}")

print(f"\nAttack rate: lambda = {lambda_fdi} s^-1 (FDI)")
print(f"P_other = {p_other}")
print()

print(f"{'Protocol':<15} {'L (ms)':>10} {'P_temporal':>12} {'P_secure':>10} {'lambda*L*Pta':>12}")
print("-" * 65)

for name, lat_ms, special in protocols:
    if special == "vrf":
        p_r_eff = p_r_vrf(k_compromised=1)
        p_ta_proto = p_ta_no_blockchain(x, n_sen=n_sen, p_r=p_r_eff, weights=None)
    else:
        p_ta_proto = p_ta_val
    
    pt = p_temporal_poisson(lat_ms, lambda_fdi, p_ta_proto)
    
    # P_secure = (1 - P_TAb)(1 - P_temporal)(1 - P_other)
    # Since P_TAb ~ 0, this simplifies to (1 - P_temporal)(1 - P_other)
    ps_simple = (1.0 - pt) * (1.0 - p_other)
    
    # Also compute lambda*L*P_TA for the table
    lam_l_pta = lambda_fdi * (lat_ms / 1000.0) * p_ta_proto
    
    print(f"{name:<15} {lat_ms:>10.1f} {pt:>12.3f} {ps_simple:>10.3f} {lam_l_pta:>12.3f}")

print()
print("=" * 72)
print("  Multi-attack-type analysis (for Paper 1 Table)")
print("=" * 72)

lambdas = [100, 20, 1, 0.001]
lambda_names = ["Replay", "FDI", "MitM", "Key Theft"]

# No blockchain case
print(f"\n{'Protocol':<15}", end="")
for ln in lambda_names:
    print(f" {ln:>12}", end="")
print()
print("-" * 65)

# Without blockchain - over 1 minute observation
print(f"{'No Blockchain':<15}", end="")
for lam in lambdas:
    # For no blockchain, use 60s observation window
    p_no_bc = 1 - exp(-lam * 60 * p_ta_val)
    # Cap at P_other limit
    ps_no_bc = (1 - p_no_bc) * (1 - p_other)
    print(f" {ps_no_bc:>12.3f}", end="")
print()

for name, lat_ms, special in protocols:
    if special == "vrf":
        p_r_eff = p_r_vrf(k_compromised=1)
        p_ta_proto = p_ta_no_blockchain(x, n_sen=n_sen, p_r=p_r_eff, weights=None)
    else:
        p_ta_proto = p_ta_val
    
    print(f"{name:<15}", end="")
    for lam in lambdas:
        pt = p_temporal_poisson(lat_ms, lam, p_ta_proto)
        ps = (1.0 - pt) * (1.0 - p_other)
        print(f" {ps:>12.3f}", end="")
    print()

print()
print("=" * 72)
print("  Sensor subset impact (for Paper 1 Table)")
print("=" * 72)

subset_sizes = [3854, 50, 20, 10, 5]
tbft_lat = 242.9

print(f"\n{'m':<10} {'P_TA(m)':>12} {'P_temporal':>12} {'P_secure':>10}")
print("-" * 50)
for m in subset_sizes:
    p_ta_m = p_ta_no_blockchain(x, n_sen=m, weights=None)
    pt_m = p_temporal_poisson(tbft_lat, lambda_fdi, p_ta_m)
    ps_m = (1.0 - pt_m) * (1.0 - p_other)
    print(f"{m:<10} {p_ta_m:>12.6f} {pt_m:>12.3f} {ps_m:>10.3f}")

print()
print("=" * 72)
print("  Improvement factors (for Paper 1 'Improvement' column)")
print("=" * 72)

# Baseline: no blockchain, 1 minute window, FDI
p_no_bc_fdi = 1 - exp(-lambda_fdi * 60 * p_ta_val)
ps_baseline = (1 - p_no_bc_fdi) * (1 - p_other)
print(f"\nNo-blockchain P_secure (1-min window, FDI): {ps_baseline:.6f}")

for name, lat_ms, special in protocols:
    if special == "vrf":
        p_r_eff = p_r_vrf(k_compromised=1)
        p_ta_proto = p_ta_no_blockchain(x, n_sen=n_sen, p_r=p_r_eff, weights=None)
    else:
        p_ta_proto = p_ta_val
    
    pt = p_temporal_poisson(lat_ms, lambda_fdi, p_ta_proto)
    ps = (1.0 - pt) * (1.0 - p_other)
    improvement = ps / max(ps_baseline, 1e-30) if ps_baseline > 0 else float('inf')
    print(f"  {name:<15}: P_secure = {ps:.3f}, Improvement = {improvement:.1f}x")
