"""
IEEE Figure Generator for BFT Comparison
=========================================
Generates 10 publication-quality figures representing the Static-Temporal 
Security Framework (STSF) and comparisons across nine consensus protocols.
Style guidelines:
  - White background, no colored fills
  - Thin lines (1.2-2.0 pt)
  - Axis labels in proper serif font
  - Minimal grid, clean ticks
"""

import os
import sys
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm

# Import unified math functions and constants
from probabilistic_model import (
    N_NODES, N_SEN, BFT_LIMIT, P_SCADA, P_R,
    p_ta_no_blockchain, p_tab_blockchain, p_tab_with_key_mgmt,
    p_r_shamir, p_r_mpc, p_r_multisig, p_r_vrf,
    om_latency_ms, om_latency_ms_lower, om_latency_bounds, om_message_count,
    pbft_latency_ms, tbft_latency_ms, tbft_message_count,
    p_temporal_poisson, p_secure, p_secure_correlated, throughput_tps,
    p_ta_bayes, p_ta_bayes_sensitivity,
    security_gain_vs_om, sensitivity_ranking, latency_distribution
)

# ═══════════════════════════════════════════════════════════════
#  IEEE SETUP AND STYLE
# ═══════════════════════════════════════════════════════════════

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Bitstream Vera Serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 9.5,
    "axes.titlesize": 10.5,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8.0,
    "lines.linewidth": 1.5,
    "axes.linewidth": 0.6,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linewidth": 0.5,
})

FIGURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIGURE_DIR, exist_ok=True)

# Load protocols dynamically from protocols.json
protocols_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "protocols.json")
with open(protocols_json_path, "r", encoding="utf-8") as f:
    PROTOCOLS_DATA = json.load(f)

C_OM     = PROTOCOLS_DATA["OM(m)"]["color"]
C_PBFT   = PROTOCOLS_DATA["Classic PBFT"]["color"]
C_IBFT   = PROTOCOLS_DATA["IBFT 2.0"]["color"]
C_QBFT   = PROTOCOLS_DATA["QBFT"]["color"]
C_CEPBFT = PROTOCOLS_DATA["CE-PBFT"]["color"]
C_GPBFT  = PROTOCOLS_DATA["G-PBFT"]["color"]
C_SVPBFT = PROTOCOLS_DATA["SV-PBFT"]["color"]
C_TOWER  = PROTOCOLS_DATA["Tower BFT"]["color"]
C_RVR    = PROTOCOLS_DATA["RVR"]["color"]

PROTOCOLS = []
for name, data in PROTOCOLS_DATA.items():
    PROTOCOLS.append((
        name,
        data["color"],
        data["latency_ms"],
        data["msg_count"],
        data["group_id"]
    ))

GROUP_COLORS = {"G1": "#E74C3C", "G2": "#8E44AD", "G3": "#27AE60", "G4": "#2C3E50"}
GROUP_LABELS = {
    "G1": "G1: Classical BFT",
    "G2": "G2: Committee-Delegated",
    "G3": "G3: Hierarchical PBFT",
    "G4": "G4: Sub-Second BFT",
}

def apply_style(fig, ax):
    """Remove top and right spines, tighten layout."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

# ═══════════════════════════════════════════════════════════════
#  FIGURES IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════

def fig1_latency_vs_ptemporal():
    """Fig 1: Consensus Latency vs Temporal Vulnerability P_temporal."""
    L_vals = np.logspace(-1, 2.5, 500)  # 0.1s to 316s
    p_ta_val = p_ta_no_blockchain(0.95, n_sen=10) # m = 10 critical sensors
    
    lambdas = [0.001, 1.0, 5.0, 20.0, 50.0]
    lambda_labels = [
        r"$\lambda=0.001$ (Key theft)", 
        r"$\lambda=1$ (MitM hijack)", 
        r"$\lambda=5$ (Moderate)",
        r"$\lambda=20$ (FDI sensor)", 
        r"$\lambda=50$ (Replay flood)"
    ]
    lambda_colors = ["#3498DB", "#2ECC71", "#F39C12", "#E74C3C", "#8E44AD"]

    fig, ax = plt.subplots(figsize=(7, 4.5))

    for lam, label, color in zip(lambdas, lambda_labels, lambda_colors):
        p_temps = [p_temporal_poisson(L * 1000.0, lam, p_ta_val) for L in L_vals]
        ax.plot(L_vals, p_temps, lw=1.8, label=label, color=color)

    # Mark protocol positions at FDI rate (lambda=20)
    from probabilistic_model import p_r_vrf
    for name, color, lat_ms, _, grp in PROTOCOLS:
        lat_s = lat_ms / 1000.0
        if name == "RVR":
            p_r_eff = p_r_vrf(k_compromised=1)
            p_ta_proto = p_ta_no_blockchain(0.95, n_sen=10, p_r=p_r_eff)
        else:
            p_ta_proto = p_ta_val
        pt = p_temporal_poisson(lat_ms, 20.0, p_ta_proto)
        marker = "o" if grp in ("G1", "G2") else "D"
        ax.plot(lat_s, pt, marker, color=color, ms=7, zorder=5,
                markeredgecolor="black", markeredgewidth=0.6)
        if name in ("OM(m)", "Tower BFT", "RVR", "QBFT", "Classic PBFT"):
            offset = (8, 5) if name != "Tower BFT" else (8, -12)
            ax.annotate(name, (lat_s, pt), textcoords="offset points",
                        xytext=offset, fontsize=7.5, fontweight="bold", color=color)

    ax.set_xscale("log")
    ax.set_xlabel("Consensus Latency L (seconds)")
    ax.set_ylabel(r"Temporal Vulnerability $P_{temporal}(\lambda, L)$")
    ax.set_title("Temporal Vulnerability vs Consensus Latency (m = 10 sensors)", fontweight="bold")
    ax.set_ylim(-0.02, 1.02)
    ax.axhline(y=0.5, color="gray", ls="--", alpha=0.4, lw=0.8)
    ax.text(0.12, 0.52, "Critical Threshold (0.50)", fontsize=7.5, color="gray", transform=ax.get_yaxis_transform())
    ax.legend(loc="lower right", framealpha=0.9)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_ptemporal_vs_latency.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 1 -> {path}")


def fig2_latency_vs_psecure():
    """Fig 2: P_secure vs Latency and component failure decomposition."""
    L_vals = np.logspace(-1, 2.5, 500)
    p_ta_val = p_ta_no_blockchain(0.95, n_sen=10)
    p_tab_val = p_tab_blockchain(0.95, n_sen=10)
    lam = 20.0 # FDI rate

    p_secure_vals = []
    p_temp_vals = []
    for L in L_vals:
        pt = p_temporal_poisson(L * 1000.0, lam, p_ta_val)
        ps = p_secure(p_tab_val, pt, p_other=0.05)
        p_secure_vals.append(ps)
        p_temp_vals.append(pt)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))

    # Panel A: P_secure, P_temporal, P_static
    ax1.plot(L_vals, p_secure_vals, lw=2.0, color="#2C3E50", label=r"$P_{secure}$")
    ax1.plot(L_vals, p_temp_vals, lw=1.5, color="#E74C3C", ls="--", label=r"$P_{temporal}$")
    ax1.plot(L_vals, [p_tab_val]*len(L_vals), lw=1.5, color="#2980B9", ls=":", label=r"$P_{static}$ ($P_{TAb}$)")
    ax1.axhline(y=0.95, color="#27AE60", ls="--", alpha=0.4, lw=0.8)
    ax1.axhline(y=0.80, color="#F39C12", ls="--", alpha=0.4, lw=0.8)
    ax1.axhline(y=0.50, color="#E74C3C", ls="--", alpha=0.4, lw=0.8)
    ax1.text(0.12, 0.96, "Target: 0.95", fontsize=7.5, color="#27AE60", transform=ax1.get_yaxis_transform())
    ax1.text(0.12, 0.81, "Acceptable: 0.80", fontsize=7.5, color="#F39C12", transform=ax1.get_yaxis_transform())
    ax1.text(0.12, 0.51, "Critical: 0.50", fontsize=7.5, color="#E74C3C", transform=ax1.get_yaxis_transform())

    for name, color, lat_ms, _, grp in PROTOCOLS:
        lat_s = lat_ms / 1000.0
        if name == "RVR":
            p_r_eff = p_r_vrf(k_compromised=1)
            p_ta_proto = p_ta_no_blockchain(0.95, n_sen=10, p_r=p_r_eff)
            p_tab_proto = p_tab_blockchain(0.95, n_sen=10, p_r_override=p_r_eff)
        else:
            p_ta_proto = p_ta_val
            p_tab_proto = p_tab_val
            
        pt = p_temporal_poisson(lat_ms, lam, p_ta_proto)
        ps = p_secure_correlated(p_tab_proto, pt, rho=0.3, p_other=0.05)
        ax1.plot(lat_s, ps, "o", color=GROUP_COLORS[grp], ms=6, zorder=5,
                 markeredgecolor="black", markeredgewidth=0.5)
        if name in ("OM(m)", "Classic PBFT", "CE-PBFT", "Tower BFT", "RVR"):
            offset = (8, 4) if ps > 0.5 else (8, -10)
            ax1.annotate(name, (lat_s, ps), textcoords="offset points",
                         xytext=offset, fontsize=7.5, fontweight="bold", color=GROUP_COLORS[grp])

    ax1.set_xscale("log")
    ax1.set_xlabel("Consensus Latency L (seconds)")
    ax1.set_ylabel("Probability")
    ax1.set_title(r"(a) Security & Failure Curves vs Latency ($\lambda=20$)")
    ax1.set_ylim(-0.02, 1.05)
    ax1.legend(loc="lower left")

    # Panel B: Failure Decomposition
    ax2.fill_between(L_vals, 0, p_temp_vals, alpha=0.25, color="#E74C3C", label=r"$P_{temporal}$ (latency-driven)")
    ax2.fill_between(L_vals, 0, [0.05]*len(L_vals), alpha=0.25, color="#F39C12", label=r"$P_{other}$ (residual risk)")
    ax2.plot(L_vals, p_temp_vals, lw=1.5, color="#E74C3C")
    ax2.axhline(y=0.05, lw=1.2, color="#F39C12", ls="--")
    ax2.text(0.5, 0.08, r"$P_{TAb} \approx 0$ (cryptographic static - negligible)", fontsize=8, color="#2980B9",
             style="italic", transform=ax2.transAxes, ha="center")

    ax2.set_xscale("log")
    ax2.set_xlabel("Consensus Latency L (seconds)")
    ax2.set_ylabel("Probability Component")
    ax2.set_title("(b) Failure Decomposition")
    ax2.set_ylim(-0.02, 1.02)
    ax2.legend(loc="upper left")

    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_latency_vs_psecure.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 2 -> {path}")


def fig3_heatmap():
    """Fig 3: Contour heatmap of temporal vulnerability over L and lambda."""
    L_vals = np.logspace(-1, 2.5, 200)
    lam_vals = np.logspace(-3, 2, 200)
    p_ta_val = p_ta_no_blockchain(0.95, n_sen=10)

    Z = np.zeros((len(lam_vals), len(L_vals)))
    for i, lam in enumerate(lam_vals):
        for j, L in enumerate(L_vals):
            Z[i, j] = p_temporal_poisson(L * 1000.0, lam, p_ta_val)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    im = ax.pcolormesh(L_vals, lam_vals, Z, cmap="RdYlGn_r", shading="gouraud", vmin=0, vmax=1)
    cbar = fig.colorbar(im, ax=ax, label=r"Temporal Vulnerability $P_{temporal}(\lambda, L)$", pad=0.02)

    CS = ax.contour(L_vals, lam_vals, Z, levels=[0.01, 0.05, 0.1, 0.5, 0.9],
                    colors="black", linewidths=0.6, linestyles="--")
    ax.clabel(CS, inline=True, fontsize=7.5, fmt="%.2f")

    # Mark protocols at FDI rate (lambda = 20)
    for name, color, lat_ms, _, grp in PROTOCOLS:
        lat_s = lat_ms / 1000.0
        ax.plot(lat_s, 20.0, "o", color="white", ms=6, zorder=5,
                markeredgecolor="black", markeredgewidth=1.0)
        if name in ("OM(m)", "Tower BFT", "RVR", "CE-PBFT", "Classic PBFT"):
            ax.annotate(name, (lat_s, 20.0), textcoords="offset points",
                        xytext=(4, 5), fontsize=7.5, color="white", fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.15", fc="black", alpha=0.6, ec="none"))

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Consensus Latency L (seconds)")
    ax.set_ylabel(r"Attack Rate $\lambda$ (attacks/second)")
    ax.set_title("Vulnerability Map: Latency vs. Attack Rate (m = 10 sensors)", fontweight="bold")

    attack_types = [(0.001, "Key theft"), (1.0, "MitM hijack"), (20.0, "FDI sensor"), (50.0, "Replay flood")]
    for lam_at, label in attack_types:
        ax.axhline(y=lam_at, color="black", ls=":", alpha=0.2, lw=0.5)
        ax.annotate(label, (L_vals[-1], lam_at), textcoords="offset points",
                    xytext=(-50, 2), fontsize=7, color="#444")

    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_attack_rate_heatmap.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 3 -> {path}")


def fig4_f_vs_latency():
    """Fig 4: Fault level (f) vs Latency with group envelopes."""
    f_vals = np.array(range(0, 26))

    # G1: OM and PBFT
    om_vals = [om_latency_ms(f) / 1000.0 for f in f_vals]
    pbft_base = pbft_latency_ms() / 1000.0
    pbft_vals = [pbft_base * (1.0 + 0.04 * f) for f in f_vals]

    # G2: IBFT and QBFT
    ibft_base = 2.5
    ibft_vals = [ibft_base * (1.0 + 0.02 * f) for f in f_vals]
    qbft_base = 1.5
    qbft_vals = [qbft_base * (1.0 + 0.02 * f) for f in f_vals]

    # G3: CE-PBFT, G-PBFT, SV-PBFT
    ce_base = 0.8
    ce_vals = [ce_base * (1.0 + 0.015 * f) for f in f_vals]
    g_base = 0.65
    g_vals = [g_base * (1.0 + 0.015 * f) for f in f_vals]
    sv_base = 0.5
    sv_vals = [sv_base * (1.0 + 0.015 * f) for f in f_vals]

    # G4: Tower BFT and RVR
    tower_vals = [tbft_latency_ms(N_NODES, f) / 1000.0 for f in f_vals]
    rvr_base = 0.2
    rvr_vals = [rvr_base * (1.0 + 0.01 * f) for f in f_vals]

    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Shaded group envelopes
    ax.fill_between(f_vals, pbft_vals, om_vals, alpha=0.08, color="#E74C3C", label="G1 Envelope")
    ax.fill_between(f_vals, qbft_vals, ibft_vals, alpha=0.08, color="#8E44AD", label="G2 Envelope")
    ax.fill_between(f_vals, sv_vals, ce_vals, alpha=0.08, color="#27AE60", label="G3 Envelope")
    ax.fill_between(f_vals, rvr_vals, tower_vals, alpha=0.08, color="#2C3E50", label="G4 Envelope")

    # Plot faded/dashed and solid curves
    ax.plot(f_vals, om_vals, "-", color=C_OM, lw=1.8, label="OM(m) (G1)")
    ax.plot(f_vals, pbft_vals, "--", color=C_PBFT, lw=1.2, alpha=0.5, label="Classic PBFT (G1)")
    
    ax.plot(f_vals, ibft_vals, "--", color=C_IBFT, lw=1.2, alpha=0.5, label="IBFT 2.0 (G2)")
    ax.plot(f_vals, qbft_vals, "-", color=C_QBFT, lw=1.8, label="QBFT (G2)")
    
    ax.plot(f_vals, ce_vals, "--", color=C_CEPBFT, lw=1.2, alpha=0.5, label="CE-PBFT (G3)")
    ax.plot(f_vals, g_vals, "-.", color=C_GPBFT, lw=1.2, alpha=0.5, label="G-PBFT (G3)")
    ax.plot(f_vals, sv_vals, "-", color=C_SVPBFT, lw=1.8, label="SV-PBFT (G3)")
    
    ax.plot(f_vals, tower_vals, "-", color=C_TOWER, lw=2.0, label="Tower BFT (G4)")
    ax.plot(f_vals, rvr_vals, "-.", color=C_RVR, lw=1.2, alpha=0.5, label="RVR (G4)")

    ax.axvline(x=BFT_LIMIT, color="red", ls="--", alpha=0.5, lw=0.8)
    ax.text(BFT_LIMIT + 0.3, 10.0, f"BFT Limit (f={BFT_LIMIT})", fontsize=8, color="red")

    ax.set_yscale("log")
    ax.set_xlabel("Number of Byzantine Faulty Nodes (f)")
    ax.set_ylabel("Consensus Latency (seconds, log scale)")
    ax.set_title("Latency Scaling Under Byzantine Faults (Group Bands)", fontweight="bold")
    ax.legend(loc="upper left", ncol=2, fontsize=7.5)
    ax.set_xlim(-0.5, 25.5)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_f_vs_latency.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 4 -> {path}")


def fig5_pareto():
    """Fig 5: Pareto Frontier (Security vs Latency)."""
    lam = 20.0
    p_ta_val = p_ta_no_blockchain(0.95, n_sen=10)
    p_tab_val = p_tab_blockchain(0.95, n_sen=10)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    
    group_colors = {"G1": "#E74C3C", "G2": "#E67E22", "G3": "#27AE60", "G4": "#2980B9"}
    group_labels_custom = {
        "G1": "G1: Classical BFT",
        "G2": "G2: Committee-Delegated",
        "G3": "G3: Hierarchical PBFT",
        "G4": "G4: Sub-Second BFT",
    }

    points = []
    for name, color, lat_ms, msgs, grp in PROTOCOLS:
        lat_s = lat_ms / 1000.0
        if name == "RVR":
            p_r_eff = p_r_vrf(k_compromised=1)
            p_ta_proto = p_ta_no_blockchain(0.95, n_sen=10, p_r=p_r_eff)
            p_tab_proto = p_tab_blockchain(0.95, n_sen=10, p_r_override=p_r_eff)
        else:
            p_ta_proto = p_ta_val
            p_tab_proto = p_tab_val
            
        pt = p_temporal_poisson(lat_ms, lam, p_ta_proto)
        ps = p_secure_correlated(p_tab_proto, pt, rho=0.3, p_other=0.05)
        points.append((name, lat_s, ps, color, grp, msgs))

    # Identify Pareto frontier (minimizing latency, maximizing security)
    # Sort by latency ascending
    sorted_pts = sorted(points, key=lambda p: p[1])
    frontier = []
    max_sec = -1
    for pt in sorted_pts:
        if pt[2] > max_sec:
            frontier.append(pt)
            max_sec = pt[2]

    # Red zone for dominated/unacceptable security
    ax.axhspan(0, 0.05, alpha=0.05, color="red")
    ax.text(1.0, 0.015, "Critical Vulnerability Zone ($P_{secure} \\approx 0$)", fontsize=9, color="#E74C3C", alpha=0.7, style="italic")

    # Plot frontier line
    if len(frontier) > 0:
        fx = [p[1] for p in frontier]
        fy = [p[2] for p in frontier]
        # Extend line to the right to show boundary
        fx_extended = fx + [fx[-1] * 100.0]
        fy_extended = fy + [fy[-1]]
        ax.step(fx_extended, fy_extended, where="post", color="gold", ls="--", lw=1.8, zorder=3, label="Efficient Frontier")

    # Plot all protocols
    for name, lat_s, ps, color, grp, msgs in points:
        is_frontier = any(fp[0] == name for fp in frontier) and ps > 0.001
        edge = "gold" if is_frontier else "black"
        edgew = 1.5 if is_frontier else 0.5
        size = 120 if is_frontier else 75
        ax.scatter(lat_s, ps, c=group_colors[grp], s=size, marker="o", edgecolors=edge, linewidths=edgew, zorder=5)
        
        offset_y = 6 if ps > 0.05 else -12
        ax.annotate(name, (lat_s, ps), textcoords="offset points",
                     xytext=(8, offset_y), fontsize=7.5, va="center", color=group_colors[grp], fontweight="bold")

    for grp, label in group_labels_custom.items():
        ax.scatter([], [], c=group_colors[grp], s=60, label=label, edgecolors="black", linewidths=0.5)

    ax.set_xscale("log")
    ax.set_xlabel("Consensus Latency L (seconds, log scale)")
    ax.set_ylabel(r"$P_{secure}$ (higher is better)")
    ax.set_title("Pareto Frontier: Security vs. Latency (Zoomed)", fontweight="bold")
    ax.legend(loc="upper right", framealpha=0.9)
    ax.set_ylim(-0.02, 0.45)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_pareto_frontier.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 5 -> {path}")


def fig6_component_contribution():
    """Fig 6: Stacked bar chart showing Sheikh's sensor term collapse vs critical subsets."""
    x_vals = [0.90, 0.95, 0.99, 0.995, 0.999]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    # Left: absolute components for all sensors (N_SEN = 3854)
    sensors_all = [x ** N_SEN for x in x_vals]
    scada = [P_SCADA for _ in x_vals]
    receiver = [P_R for _ in x_vals]

    bar_x = np.arange(len(x_vals))
    bar_w = 0.22

    ax1.bar(bar_x - bar_w, sensors_all, bar_w, label=r"$P_{SA} = x^{3854}$", color="#3498DB", edgecolor="white")
    ax1.bar(bar_x, scada, bar_w, label=r"$P_{SCADA} = 0.01$", color="#E74C3C", edgecolor="white")
    ax1.bar(bar_x + bar_w, receiver, bar_w, label=r"$P_R = 0.01$", color="#F39C12", edgecolor="white")

    ax1.set_yscale("log")
    ax1.set_xticks(bar_x)
    ax1.set_xticklabels([f"x={x}" for x in x_vals])
    ax1.set_ylabel("Component Probability (log scale)")
    ax1.set_title(r"(a) Baseline Model Exponents ($n_{sen}=3854$)", fontsize=9.5)
    ax1.legend(loc="upper left")
    ax1.set_ylim(1e-180, 10.0)

    # Right: percentage contribution for critical subset (m = 10 sensors)
    pct_scada = []
    pct_recv = []
    pct_sensor = []
    
    for x in x_vals:
        p_sa_m = x ** 10  # critical sensors subset
        total = p_sa_m + P_SCADA + P_R  # unweighted absolute sum
        pct_sensor.append(p_sa_m / total * 100.0)
        pct_scada.append(P_SCADA / total * 100.0)
        pct_recv.append(P_R / total * 100.0)

    ax2.bar(bar_x, pct_scada, 0.45, label="SCADA", color="#E74C3C", edgecolor="white")
    ax2.bar(bar_x, pct_recv, 0.45, bottom=pct_scada, label="Receiver", color="#F39C12", edgecolor="white")
    bottom_s = [a+b for a,b in zip(pct_scada, pct_recv)]
    ax2.bar(bar_x, pct_sensor, 0.45, bottom=bottom_s, label="Sensors", color="#3498DB", edgecolor="white")

    ax2.set_xticks(bar_x)
    ax2.set_xticklabels([f"x={x}" for x in x_vals])
    ax2.set_ylabel("Risk Contribution (%)")
    ax2.set_title(r"(b) Refined Model Contribution (m = 10 critical sensors)", fontsize=9.5)
    ax2.legend(loc="upper right")
    ax2.set_ylim(0, 105)

    fig.suptitle("Component Contribution to Attack Risk: Sheikh's Model vs Refinement", fontweight="bold", y=0.98)
    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_component_contribution.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 6 -> {path}")


def fig7_key_management():
    """Fig 7: Receiver key management defense-in-depth comparison."""
    schemes = [
        ("None (Baseline)", P_R),
        ("Shamir(3,5)",      p_r_shamir(3, 5)),
        ("Shamir(4,7)",      p_r_shamir(4, 7)),
        ("MPC(3,5)",         p_r_mpc(3, 5)),
        ("MPC(5,9)",         p_r_mpc(5, 9)),
        ("Multisig(3,5)",    p_r_multisig(3, 5)),
        ("Multisig(5,7)",    p_r_multisig(5, 7)),
    ]

    names = [s[0] for s in schemes]
    pr_vals = [s[1] for s in schemes]
    multipliers = [P_R / max(pr, 1e-35) for pr in pr_vals]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12.5, 4.2))
    colors = ["#E74C3C", "#3498DB", "#2980B9", "#27AE60", "#16A085", "#8E44AD", "#9B59B6"]

    # Panel A: Effective P_R
    bars1 = ax1.barh(range(len(names)), pr_vals, color=colors, edgecolor="white", height=0.55)
    ax1.set_xscale("log")
    ax1.set_yticks(range(len(names)))
    ax1.set_yticklabels(names, fontsize=8.0)
    ax1.set_xlabel("Effective Receiver Compromise $P_R$")
    ax1.set_title(r"(a) Effective $P_R$ (log scale)")
    ax1.invert_yaxis()
    for i, bar in enumerate(bars1):
        ax1.text(pr_vals[i] * 1.5, i, f"{pr_vals[i]:.2e}", va="center", fontsize=7.0)
    ax1.grid(axis="x", alpha=0.3)

    # Panel B: Multipliers
    bars2 = ax2.barh(range(len(names)), multipliers, color=colors, edgecolor="white", height=0.55)
    ax2.set_xscale("log")
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels([])
    ax2.set_xlabel("Vulnerability Reduction Multiplier")
    ax2.set_title("(b) Security Gain Factor")
    ax2.invert_yaxis()
    for i, bar in enumerate(bars2):
        ax2.text(multipliers[i] * 1.5, i, f"{multipliers[i]:,.0f}x", va="center", fontsize=7.0, fontweight="bold")
    ax2.grid(axis="x", alpha=0.3)

    # Panel C: Resulting P_secure with Tower BFT (L = 242.9ms, lambda = 20)
    tbft_lat = 242.9
    psecure_vals = []
    p_ta_m10 = p_ta_no_blockchain(0.95, n_sen=10)
    p_tab_m10 = p_tab_blockchain(0.95, n_sen=10)

    for name_s, pr_eff in schemes:
        # P_TA with modified P_R and equal weighting (critical subset m=10)
        p_ta_km = 0.25 * (2.0 * (0.95 ** 10) + P_SCADA + pr_eff)
        pt = p_temporal_poisson(tbft_lat, 20.0, p_ta_km)
        ps = p_secure(0.0, pt, p_other=0.05) # static P_TAb ≈ 0
        psecure_vals.append(ps)

    bars3 = ax3.barh(range(len(names)), psecure_vals, color=colors, edgecolor="white", height=0.55)
    ax3.set_xlim(0.88, 0.96)
    ax3.set_yticks(range(len(names)))
    ax3.set_yticklabels([])
    ax3.set_xlabel(r"$P_{secure}$ (Tower BFT, $\lambda=20$)")
    ax3.set_title(r"(c) Overall $P_{secure}$")
    ax3.invert_yaxis()
    for i, bar in enumerate(bars3):
        ax3.text(psecure_vals[i] + 0.0005, i, f"{psecure_vals[i]:.4f}", va="center", fontsize=7.0)
    ax3.axvline(x=0.95, color="#27AE60", ls="--", alpha=0.6, lw=0.8)
    ax3.grid(axis="x", alpha=0.3)

    fig.suptitle("Key Management Defence-in-Depth Analysis (m = 10 sensors)", fontweight="bold", y=0.98)
    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_key_management.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 7 -> {path}")


def fig8_message_complexity():
    """Fig 8: Horizontal log bar chart of message complexity with inset zoom."""
    names = [p[0] for p in PROTOCOLS]
    msgs = [p[3] for p in PROTOCOLS]
    colors = [p[1] for p in PROTOCOLS]

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bars = ax.barh(range(len(names)), msgs, color=colors, edgecolor="white", height=0.55)
    
    ax.set_xscale("log")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9.0)
    ax.set_xlabel("Message Complexity per Block (log scale)")
    ax.set_title("Consensus Protocol Message Overhead", fontweight="bold")
    ax.invert_yaxis()

    for i, bar in enumerate(bars):
        val = msgs[i]
        label = f"{val:.1e}" if val >= 1.0e6 else f"{val:,.0f}"
        ax.text(val * 1.5, i, label, va="center", fontsize=8.0, fontweight="bold")

    # Inset zoom without OM(m)
    axins = ax.inset_axes([0.45, 0.45, 0.5, 0.45])
    # Filter out OM(m) which is the first protocol
    names_sub = names[1:]
    msgs_sub = msgs[1:]
    colors_sub = colors[1:]
    
    bars_ins = axins.barh(range(len(names_sub)), msgs_sub, color=colors_sub, edgecolor="white", height=0.55)
    axins.set_yticks(range(len(names_sub)))
    axins.set_yticklabels(names_sub, fontsize=6.5)
    axins.set_xlabel("Messages (linear scale)", fontsize=7)
    axins.set_title("Excluding OM(m) (Linear Zoom)", fontsize=7.5, fontweight="bold")
    axins.invert_yaxis()
    axins.grid(axis="x", alpha=0.3)
    axins.tick_params(axis="both", labelsize=6.5)
    
    for i, bar in enumerate(bars_ins):
        val = msgs_sub[i]
        axins.text(val + 100, i, f"{val:,.0f}", va="center", fontsize=6.0)

    ax.grid(axis="x", alpha=0.3)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_message_complexity.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 8 -> {path}")


def fig9_f_vs_psecure():
    """Fig 9: f vs Latency & P_secure stacked panels showing OM collapse vs PBFT vs Tower BFT stability."""
    f_vals = range(0, 26)
    lam = 20.0
    p_ta_val = p_ta_no_blockchain(0.95, n_sen=10)
    p_tab_val = p_tab_blockchain(0.95, n_sen=10)

    om_lats = []
    pbft_lats = []
    tbft_lats = []

    om_ps = []
    pbft_ps = []
    tbft_ps = []

    for f in f_vals:
        # OM(m) latency
        om_lat = om_latency_ms(f) / 1000.0
        om_pt = p_temporal_poisson(om_lat * 1000.0, lam, p_ta_val)
        om_ps.append(p_secure(p_tab_val, om_pt, 0.05))
        om_lats.append(om_lat)

        # PBFT latency scaling with view-change
        pbft_lat = (pbft_latency_ms() * (1.0 + 0.04 * f)) / 1000.0
        pbft_pt = p_temporal_poisson(pbft_lat * 1000.0, lam, p_ta_val)
        pbft_ps.append(p_secure(p_tab_val, pbft_pt, 0.05))
        pbft_lats.append(pbft_lat)

        # Tower BFT latency
        tbft_lat = tbft_latency_ms(N_NODES, f) / 1000.0
        tbft_pt = p_temporal_poisson(tbft_lat * 1000.0, lam, p_ta_val)
        tbft_ps.append(p_secure(p_tab_val, tbft_pt, 0.05))
        tbft_lats.append(tbft_lat)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 6.8), sharex=True)

    # Top panel: Latency vs f
    ax1.plot(f_vals, om_lats, "o-", color=C_OM, lw=1.8, ms=4, label="OM(m)")
    ax1.plot(f_vals, pbft_lats, "s-", color=C_PBFT, lw=1.5, ms=4, label="Classic PBFT + VC")
    ax1.plot(f_vals, tbft_lats, "D-", color=C_TOWER, lw=2.0, ms=4, label="Tower BFT")
    ax1.set_yscale("log")
    ax1.set_ylabel("Consensus Latency (seconds, log scale)")
    ax1.set_title("Latency and Security Sensitivity to Byzantine Fault Count", fontweight="bold")
    ax1.axvline(x=BFT_LIMIT, color="red", ls="--", alpha=0.5, lw=0.8)
    ax1.text(BFT_LIMIT + 0.3, 1.0, f"BFT Limit (f={BFT_LIMIT})", fontsize=8, color="red")
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.3)

    # Bottom panel: Psecure vs f
    ax2.plot(f_vals, om_ps, "o-", color=C_OM, lw=1.8, ms=4, label="OM(m)")
    ax2.plot(f_vals, pbft_ps, "s-", color=C_PBFT, lw=1.5, ms=4, label="Classic PBFT + VC")
    ax2.plot(f_vals, tbft_ps, "D-", color=C_TOWER, lw=2.0, ms=4, label="Tower BFT")
    ax2.axvline(x=BFT_LIMIT, color="red", ls="--", alpha=0.5, lw=0.8)
    ax2.axhline(y=0.95, color="#27AE60", ls=":", alpha=0.5, lw=0.8)
    ax2.axhline(y=0.80, color="#F39C12", ls=":", alpha=0.5, lw=0.8)
    ax2.axhline(y=0.50, color="#E74C3C", ls=":", alpha=0.5, lw=0.8)
    ax2.set_xlabel("Number of Byzantine Faulty Nodes (f)")
    ax2.set_ylabel(r"$P_{secure}$")
    ax2.set_ylim(-0.02, 1.0)
    ax2.set_xlim(-0.5, 25.5)
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_f_vs_psecure.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 9 -> {path}")


def fig10_sensitivity_lambda():
    """Fig 10: Security Sensitivity to Attack Rate lambda."""
    lam_vals = np.logspace(-3, 2.5, 300)
    p_ta_val = p_ta_no_blockchain(0.95, n_sen=10)
    p_tab_val = p_tab_blockchain(0.95, n_sen=10)

    # Representative protocols from each of the 4 groups
    group_representatives = [
        ("OM(m) [Group 1]",     43350.0, C_OM,    "-"),
        ("QBFT [Group 2]",      1500.0,  C_QBFT,  "--"),
        ("SV-PBFT [Group 3]",   500.0,   C_SVPBFT, "-."),
        ("Tower BFT [Group 4]", 242.9,   C_TOWER, "-"),
    ]

    fig, ax = plt.subplots(figsize=(7, 4.5))

    for name, lat_ms, color, ls in group_representatives:
        ps_vals = []
        for lam in lam_vals:
            pt = p_temporal_poisson(lat_ms, lam, p_ta_val)
            ps = p_secure(p_tab_val, pt, p_other=0.05)
            ps_vals.append(ps)
        ax.plot(lam_vals, ps_vals, lw=2.0, color=color, ls=ls, label=name)

    # Label attack rate zones
    attack_marks = [(0.001, "Key theft"), (1.0, "MitM hijack"), (20.0, "FDI sensor"), (50.0, "Replay flood")]
    for lam_at, label in attack_marks:
        ax.axvline(x=lam_at, color="gray", ls=":", alpha=0.3, lw=0.6)
        ax.text(lam_at, 0.97, label, fontsize=7.5, color="gray", rotation=90, ha="right", va="top")

    ax.axhline(y=0.95, color="#27AE60", ls="--", alpha=0.4, lw=0.8)
    ax.axhline(y=0.50, color="#E74C3C", ls="--", alpha=0.4, lw=0.8)

    ax.set_xscale("log")
    ax.set_xlabel("Attack Rate $\lambda$ (attacks/second, log scale)")
    ax.set_ylabel(r"$P_{secure}$")
    ax.set_title("Security Sensitivity to Attack Rate", fontweight="bold")
    ax.legend(loc="lower left")
    ax.set_ylim(-0.02, 1.0)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_sensitivity_lambda.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 10 -> {path}")


def fig11_sensor_sensitivity():
    """Fig 11: Sensor Count Sensitivity Analysis (m = 10, 25, 50, 100, 500, 3854)"""
    from probabilistic_model import log10_p_tab_blockchain
    # 2-panel figure: Panel A (log10(P_TAb) vs m), Panel B (P_secure vs x)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))

    # Panel A: log10(P_TAb) vs m
    m_range = np.linspace(10, 3854, 200)
    x_nominal = 0.95
    log_p_tab_vals = [log10_p_tab_blockchain(x_nominal, n_sen=int(m)) for m in m_range]
    
    ax1.plot(m_range, log_p_tab_vals, lw=2.0, color="#2C3E50")
    ax1.set_xlabel("Critical Sensor Subset Size m")
    ax1.set_ylabel(r"$\log_{10}(P_{TAb})$ (Static Compromise)")
    ax1.set_title(r"(a) Static Security Underflow vs. m ($x=0.95$)")
    ax1.grid(True, alpha=0.3)
    
    # Highlight specific values of m
    highlight_ms = [10, 25, 50, 100, 500, 3854]
    highlight_colors = ["#1ABC9C", "#2ECC71", "#3498DB", "#9B59B6", "#F1C40F", "#E74C3C"]
    for m_h, col_h in zip(highlight_ms, highlight_colors):
        log_val = log10_p_tab_blockchain(x_nominal, n_sen=int(m_h))
        ax1.plot(m_h, log_val, "o", color=col_h, ms=5, markeredgecolor="black", markeredgewidth=0.5)
        # Offset annotation text slightly depending on position
        offset = (5, 5) if m_h < 1000 else (-45, -10)
        ax1.annotate(f"m={m_h}", (m_h, log_val), textcoords="offset points", xytext=offset, fontsize=7.5, color=col_h, fontweight="bold")

    # Panel B: Psecure vs x for different m
    x_vals = np.linspace(0.90, 0.999, 100)
    lam = 20.0
    L_ms = 242.9 # Tower BFT
    
    for m, col in zip(highlight_ms, highlight_colors):
        p_sec_vals = []
        for x in x_vals:
            p_ta_m = p_ta_no_blockchain(x, n_sen=m)
            p_tab_m = p_tab_blockchain(x, n_sen=m)
            pt = p_temporal_poisson(L_ms, lam, p_ta_m)
            ps = p_secure_correlated(p_tab_m, pt, rho=0.3, p_other=0.05)
            p_sec_vals.append(ps)
            
        label = f"m = {m}" if m != 3854 else "m = 3854 (All)"
        ax2.plot(x_vals, p_sec_vals, lw=1.8, color=col, label=label)
        
    ax2.set_xlabel("Sensor Integrity/Uncertainty x")
    ax2.set_ylabel(r"$P_{secure}$ under FDI ($\lambda=20$)")
    ax2.set_title("Influence of Critical Sensor Subset Size m")
    ax2.set_ylim(-0.02, 1.02)
    ax2.legend(loc="lower left")
    ax2.grid(True, alpha=0.3)
    
    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_sensor_sensitivity.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 11 -> {path}")


def fig12_security_gain():
    """Fig 12: Security Gain vs OM(m) baseline bar chart."""
    proto_list = [
        ("OM(m)", 43350.0),
        ("Classic PBFT", 7650.0),
        ("IBFT 2.0", 2500.0),
        ("QBFT", 1500.0),
        ("CE-PBFT", 800.0),
        ("G-PBFT", 650.0),
        ("SV-PBFT", 500.0),
        ("Tower BFT", 242.9),
        ("RVR", 200.0),
    ]

    colors_list = [C_OM, C_PBFT, C_IBFT, C_QBFT, C_CEPBFT, C_GPBFT, C_SVPBFT, C_TOWER, C_RVR]

    # Compute gains at FDI rate (lambda=20)
    gains_fdi = security_gain_vs_om(proto_list, lambda_attack=20.0)
    # Compute gains at MitM rate (lambda=1)
    gains_mitm = security_gain_vs_om(proto_list, lambda_attack=1.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    names = [g[0] for g in gains_mitm]
    gain_vals_mitm = [g[2] for g in gains_mitm]
    gain_vals_fdi = [g[2] for g in gains_fdi]

    y_pos = range(len(names))

    # Panel A: MitM (lambda=1)
    bars1 = ax1.barh(y_pos, gain_vals_mitm, color=colors_list, edgecolor="white", height=0.55)
    ax1.set_xscale("log")
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names, fontsize=8.5)
    ax1.set_xlabel("Security Gain vs OM(m) (log scale)")
    ax1.set_title(r"(a) MitM Hijack ($\lambda=1$)", fontweight="bold")
    ax1.invert_yaxis()
    for i, bar in enumerate(bars1):
        val = gain_vals_mitm[i]
        label = f"{val:,.0f}x" if val >= 2 else f"{val:.1f}x"
        ax1.text(max(val * 1.3, 1.5), i, label, va="center", fontsize=7.5, fontweight="bold")
    ax1.axvline(x=1.0, color="gray", ls="--", alpha=0.5, lw=0.8)
    ax1.grid(axis="x", alpha=0.3)

    # Panel B: FDI (lambda=20)
    bars2 = ax2.barh(y_pos, gain_vals_fdi, color=colors_list, edgecolor="white", height=0.55)
    ax2.set_xscale("log")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([], fontsize=8.5)
    ax2.set_xlabel("Security Gain vs OM(m) (log scale)")
    ax2.set_title(r"(b) FDI Sensor ($\lambda=20$)", fontweight="bold")
    ax2.invert_yaxis()
    for i, bar in enumerate(bars2):
        val = gain_vals_fdi[i]
        label = f"{val:,.0f}x" if val >= 2 else f"{val:.1f}x"
        ax2.text(max(val * 1.3, 1.5), i, label, va="center", fontsize=7.5, fontweight="bold")
    ax2.axvline(x=1.0, color="gray", ls="--", alpha=0.5, lw=0.8)
    ax2.grid(axis="x", alpha=0.3)

    fig.suptitle("Security Gain Relative to OM(m) Baseline", fontweight="bold", y=0.98)
    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_security_gain.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 12 -> {path}")


def fig13_sensitivity_ranking():
    """Fig 13: Sensitivity ranking dual bar chart proving latency dominance."""
    # Compute for Tower BFT at FDI rate
    ranking_tower = sensitivity_ranking(latency_ms=242.9, lambda_attack=20.0)
    # Also compute for PBFT at MitM rate (lambda=1, where PBFT still has meaningful values)
    ranking_pbft = sensitivity_ranking(latency_ms=7650.0, lambda_attack=1.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    colors_bar = ["#2C3E50", "#E74C3C", "#3498DB", "#F39C12"]

    # Panel A: Tower BFT (lambda=20)
    labels = list(ranking_tower.keys())
    vals_tower = list(ranking_tower.values())
    bars1 = ax1.barh(labels, vals_tower, color=colors_bar, edgecolor="white", height=0.55)
    ax1.set_xlabel("Relative Sensitivity (%)")
    ax1.set_title(r"(a) Tower BFT ($\lambda=20$)")
    ax1.set_xlim(0, 105)
    for i, bar in enumerate(bars1):
        ax1.text(vals_tower[i] + 1.0, i, f"{vals_tower[i]:.1f}%", va="center", fontsize=8.0, fontweight="bold")

    # Panel B: Classic PBFT (lambda=1)
    vals_pbft = [ranking_pbft[k] for k in labels]
    bars2 = ax2.barh(labels, vals_pbft, color=colors_bar, edgecolor="white", height=0.55)
    ax2.set_xlabel("Relative Sensitivity (%)")
    ax2.set_title(r"(b) Classic PBFT ($\lambda=1$)")
    ax2.set_xlim(0, 105)
    for i, bar in enumerate(bars2):
        ax2.text(vals_pbft[i] + 1.0, i, f"{vals_pbft[i]:.1f}%", va="center", fontsize=8.0, fontweight="bold")

    fig.suptitle("Relative Parameter Sensitivity Analysis", fontweight="bold", y=0.98)
    apply_style(fig, ax1)
    apply_style(fig, ax2)
    path = os.path.join(FIGURE_DIR, "fig_sensitivity_ranking.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 13 -> {path}")


def fig14_model_comparison():
    """Fig 14: Comparison of Security Models (Sheikh Static vs STSF Temporal)"""
    lam = 20.0
    p_ta_val = p_ta_no_blockchain(0.95, n_sen=10)
    p_tab_val = p_tab_blockchain(0.95, n_sen=10)
    
    names = [p[0] for p in PROTOCOLS]
    
    static_vals = []
    temporal_vals = []
    
    for name, color, lat_ms, _, grp in PROTOCOLS:
        if name == "RVR":
            p_r_eff = p_r_vrf(k_compromised=1)
            p_ta_proto = p_ta_no_blockchain(0.95, n_sen=10, p_r=p_r_eff)
            p_tab_proto = p_tab_blockchain(0.95, n_sen=10, p_r_override=p_r_eff)
        else:
            p_ta_proto = p_ta_val
            p_tab_proto = p_tab_val
            
        p_sec_static = 1.0 - p_tab_proto
        static_vals.append(p_sec_static)
        
        pt = p_temporal_poisson(lat_ms, lam, p_ta_proto)
        p_sec_temp = p_secure_correlated(p_tab_proto, pt, rho=0.3, p_other=0.05)
        temporal_vals.append(p_sec_temp)
        
    fig, ax = plt.subplots(figsize=(8.5, 5))
    
    y_pos = np.arange(len(names))
    height = 0.35
    
    rects1 = ax.barh(y_pos - height/2, static_vals, height, label="Sheikh Static Model ($1 - P_{TAb}$)", color="#2C3E50", edgecolor="white")
    rects2 = ax.barh(y_pos + height/2, temporal_vals, height, label="STSF Temporal Model ($P_{secure}, \lambda=20$)", color="#E74C3C", edgecolor="white")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=9.0)
    ax.set_xlabel("Security Probability")
    ax.set_title("Comparison of Security Models: Static vs. Temporal (FDI, $\lambda=20$)", fontweight="bold")
    ax.set_xlim(0, 1.15)
    ax.legend(loc="lower left")
    ax.invert_yaxis()
    
    for rect in rects1:
        width = rect.get_width()
        ax.annotate(f"{width:.4f}",
                    xy=(width, rect.get_y() + rect.get_height() / 2),
                    xytext=(3, 0),
                    textcoords="offset points",
                    ha='left', va='center', fontsize=7.0)
                    
    for rect in rects2:
        width = rect.get_width()
        ax.annotate(f"{width:.4f}",
                    xy=(width, rect.get_y() + rect.get_height() / 2),
                    xytext=(3, 0),
                    textcoords="offset points",
                    ha='left', va='center', fontsize=7.0)
                    
    apply_style(fig, ax)
    
    path = os.path.join(FIGURE_DIR, "fig_model_comparison.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 14 -> {path}")


def fig15_latency_distribution():
    """Fig 15: Latency Distribution Boxplots under Network Delay Jitter"""
    from probabilistic_model import latency_distribution
    
    om_dist = [v / 1000.0 for v in latency_distribution("OM(m)", f=1)] 
    pbft_dist = [v / 1000.0 for v in latency_distribution("Classic PBFT", f=1)]
    tower_dist = [v / 1000.0 for v in latency_distribution("Tower BFT", f=1)]
    
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    bp = ax.boxplot([om_dist, pbft_dist, tower_dist], labels=["OM(m) (G1)", "Classic PBFT (G1)", "Tower BFT (G4)"],
                   patch_artist=True, medianprops=dict(color="black", lw=1.5))
    
    colors = [C_OM, C_PBFT, C_TOWER]
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
        
    ax.set_yscale("log")
    ax.set_ylabel("Consensus Latency (seconds, log scale)")
    ax.set_title("Consensus Latency Jitter under Network Delay Jitter (f = 1)", fontweight="bold")
    apply_style(fig, ax)
    
    path = os.path.join(FIGURE_DIR, "fig_latency_distribution.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 15 -> {path}")


def fig16_robustness_heatmap():
    """Fig 16: Protocol Robustness Maps (2x2 Multi-Panel Heatmaps)"""
    L_vals = np.logspace(-1, 2.0, 100) 
    lam_vals = np.logspace(-3, 2.0, 100) 
    p_ta_val = p_ta_no_blockchain(0.95, n_sen=10)
    
    p_tab_om = p_tab_blockchain(0.95, n_sen=10)
    p_tab_pbft = p_tab_blockchain(0.95, n_sen=10)
    p_tab_tower = p_tab_blockchain(0.95, n_sen=10)
    
    from probabilistic_model import p_r_vrf, p_secure_correlated
    p_r_vrf_val = p_r_vrf(k_compromised=1)
    p_tab_rvr = p_tab_blockchain(0.95, n_sen=10, p_r_override=p_r_vrf_val)
    p_ta_rvr = p_ta_no_blockchain(0.95, n_sen=10, p_r=p_r_vrf_val)
    
    p_ta_map = {
        "OM(m)": p_ta_val,
        "Classic PBFT": p_ta_val,
        "Tower BFT": p_ta_val,
        "RVR": p_ta_rvr
    }
    
    ops = {
        "OM(m)": (43.35, 20.0, p_tab_om, 0.0), 
        "Classic PBFT": (7.65, 20.0, p_tab_pbft, 0.3),
        "Tower BFT": (0.2429, 20.0, p_tab_tower, 0.3),
        "RVR": (0.20, 20.0, p_tab_rvr, 0.3)
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(11, 9.5), sharex=True, sharey=True)
    axes = axes.flatten()
    
    for i, (name, (op_L, op_lam, p_tab, rho)) in enumerate(ops.items()):
        ax = axes[i]
        p_ta_proto = p_ta_map[name]
        Z = np.zeros((len(lam_vals), len(L_vals)))
        for row, lam_val in enumerate(lam_vals):
            for col, L_val in enumerate(L_vals):
                pt = p_temporal_poisson(L_val * 1000.0, lam_val, p_ta_proto)
                Z[row, col] = p_secure_correlated(p_tab, pt, rho=rho, p_other=0.05)
                
        im = ax.pcolormesh(L_vals, lam_vals, Z, cmap="RdYlGn", shading="gouraud", vmin=0, vmax=0.95)
        CS = ax.contour(L_vals, lam_vals, Z, levels=[0.5, 0.8, 0.9], colors="black", linewidths=0.6, linestyles="--")
        ax.clabel(CS, inline=True, fontsize=7, fmt="%.2f")
        
        ax.plot(op_L, op_lam, "*", color="gold", ms=12, markeredgecolor="black", markeredgewidth=1.0, zorder=10)
        ax.annotate("Operating Point", (op_L, op_lam), textcoords="offset points", xytext=(8, 4),
                    fontsize=7.5, color="black", fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", alpha=0.8, ec="black", lw=0.5))
        
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"{name} Security Horizon", fontweight="bold", fontsize=10)
        
    fig.text(0.5, 0.02, "Consensus Latency L (seconds, log scale)", ha="center", fontsize=10)
    fig.text(0.02, 0.5, r"Attack Rate $\lambda$ (attacks/second, log scale)", va="center", rotation="vertical", fontsize=10)
    
    cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax, label=r"Security Probability $P_{secure}$")
    
    fig.suptitle("Consensus Protocol Robustness Maps under Variable Threats", fontweight="bold", y=0.96, fontsize=12)
    path = os.path.join(FIGURE_DIR, "fig_robustness_heatmap.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 16 -> {path}")


def fig17_multi_lambda_comparison():
    """Fig 17: Multi-Lambda FDI Comparison (lambda = 5, 10, 20)"""
    lambdas = [5.0, 10.0, 20.0]
    p_ta_val = p_ta_no_blockchain(0.95, n_sen=10)
    p_tab_val = p_tab_blockchain(0.95, n_sen=10)
    
    names = [p[0] for p in PROTOCOLS]
    
    fig, ax = plt.subplots(figsize=(8, 5.5))
    
    y_pos = np.arange(len(names))
    height = 0.25
    
    colors = ["#3498DB", "#E67E22", "#E74C3C"]
    labels = [r"$\lambda = 5.0$", r"$\lambda = 10.0$", r"$\lambda = 20.0$"]
    
    bar_containers = []
    
    for idx, lam in enumerate(lambdas):
        ps_vals = []
        for name, color, lat_ms, _, grp in PROTOCOLS:
            if name == "RVR":
                p_r_eff = p_r_vrf(k_compromised=1)
                p_ta_proto = p_ta_no_blockchain(0.95, n_sen=10, p_r=p_r_eff)
                p_tab_proto = p_tab_blockchain(0.95, n_sen=10, p_r_override=p_r_eff)
            else:
                p_ta_proto = p_ta_val
                p_tab_proto = p_tab_val
                
            pt = p_temporal_poisson(lat_ms, lam, p_ta_proto)
            ps = p_secure_correlated(p_tab_proto, pt, rho=0.3, p_other=0.05)
            ps_vals.append(ps)
            
        offset = (idx - 1) * height
        rects = ax.barh(y_pos + offset, ps_vals, height, label=labels[idx], color=colors[idx], edgecolor="white")
        bar_containers.append(rects)
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=9.0)
    ax.set_xlabel(r"Security Probability $P_{secure}$")
    ax.set_ylabel("Protocol")
    ax.set_title("Security Probability under Varying FDI Threat Rates", fontweight="bold")
    ax.set_xlim(0, 1.05)
    ax.legend(loc="lower left")
    ax.invert_yaxis()
    
    for container in bar_containers:
        for rect in container:
            width = rect.get_width()
            if width > 0.01:
                ax.annotate(f"{width:.3f}",
                            xy=(width, rect.get_y() + rect.get_height() / 2),
                            xytext=(3, 0),
                            textcoords="offset points",
                            ha='left', va='center', fontsize=6.5)
                
    apply_style(fig, ax)
    
    path = os.path.join(FIGURE_DIR, "fig_multi_lambda_comparison.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 17 -> {path}")


def fig18_bayesian_sensitivity():
    """Fig 18: Bayesian gamma sensitivity heatmap."""
    result = p_ta_bayes_sensitivity()
    g_vals = result['gamma_vals']
    gr_vals = result['gamma_recv_vals']
    grid = result['p_ta_grid']

    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.pcolormesh(g_vals, gr_vals, grid.T, cmap="YlOrRd", shading="gouraud")
    cbar = fig.colorbar(im, ax=ax, label=r"$P_{TA}^{Bayes}$", pad=0.02)

    CS = ax.contour(g_vals, gr_vals, grid.T,
                    levels=[0.013, 0.016, 0.020, 0.024],
                    colors="black", linewidths=0.7, linestyles="--")
    ax.clabel(CS, inline=True, fontsize=8, fmt="%.3f")

    # Mark nominal values
    ax.plot(0.8, 0.6, "*", color="white", ms=14, zorder=5,
            markeredgecolor="black", markeredgewidth=1.0)
    ax.annotate(r"Nominal ($\gamma=0.8, \gamma_r=0.6$)", (0.8, 0.6),
                textcoords="offset points", xytext=(-80, -15), fontsize=8,
                color="white", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.15", fc="black", alpha=0.7, ec="none"))

    ax.set_xlabel(r"SCADA$\rightarrow$Sensor Coupling ($\gamma$)")
    ax.set_ylabel(r"SCADA$\rightarrow$Receiver Coupling ($\gamma_{recv}$)")
    ax.set_title("Bayesian Conditional Attack Model Sensitivity", fontweight="bold")

    # Add range annotation
    ax.text(0.02, 0.97, f"Range: [{result['min']:.4f}, {result['max']:.4f}]",
            transform=ax.transAxes, fontsize=8, va="top",
            bbox=dict(boxstyle="round", fc="white", alpha=0.8))

    apply_style(fig, ax)
    path = os.path.join(FIGURE_DIR, "fig_bayesian_sensitivity.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 18 -> {path}")


def fig19_correlation_sensitivity():
    """Fig 19: Correlation Sensitivity Sweep (rho = 0, 0.25, 0.5, 1.0)"""
    x_val = 0.98
    p_ta_val = p_ta_no_blockchain(x_val, n_sen=10)
    p_tab_val = p_tab_blockchain(x_val, n_sen=10)
    lam = 20.0
    L_vals = np.logspace(-1, 2.5, 500) # 0.1s to 316s
    
    fig, ax = plt.subplots(figsize=(7, 4.5))
    rhos = [0.0, 0.25, 0.5, 1.0]
    colors = ["#E74C3C", "#F39C12", "#2980B9", "#27AE60"]
    
    for rho, color in zip(rhos, colors):
        p_sec_vals = []
        for L in L_vals:
            pt = p_temporal_poisson(L * 1000.0, lam, p_ta_val)
            ps = p_secure_correlated(p_tab_val, pt, rho=rho, p_other=0.05)
            p_sec_vals.append(ps)
        ax.plot(L_vals, p_sec_vals, lw=1.8, color=color, label=f"Correlation $\\rho = {rho}$")
        
    ax.set_xscale("log")
    ax.set_xlabel("Consensus Latency L (seconds)")
    ax.set_ylabel(r"$P_{secure}$")
    ax.set_title(r"Security vs Latency under Correlated Attacks ($x=0.98, m=10, \lambda=20$)", fontweight="bold")
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="lower left")
    apply_style(fig, ax)
    
    path = os.path.join(FIGURE_DIR, "fig_correlation_sensitivity.png")
    fig.savefig(path, bbox_inches="tight", dpi=250)
    plt.close(fig)
    print(f"  [OK] Fig 19 -> {path}")




# ═══════════════════════════════════════════════════════════════
#  MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("  STSF IEEE Figure Generation Pipeline")
    print("=" * 65)
    
    fig1_latency_vs_ptemporal()
    fig2_latency_vs_psecure()
    fig3_heatmap()
    fig4_f_vs_latency()
    fig5_pareto()
    fig6_component_contribution()
    fig7_key_management()
    fig8_message_complexity()
    fig9_f_vs_psecure()
    fig10_sensitivity_lambda()
    fig11_sensor_sensitivity()
    fig12_security_gain()
    fig13_sensitivity_ranking()
    fig14_model_comparison()
    fig15_latency_distribution()
    fig16_robustness_heatmap()
    fig17_multi_lambda_comparison()
    fig18_bayesian_sensitivity()
    fig19_correlation_sensitivity()
    
    print("\n" + "=" * 65)
    print("  [OK] All 19 figures successfully written to ./figures/")
    print("=" * 65)


if __name__ == "__main__":
    main()
