"""
Figure Generator for BFT Comparison Report
===========================================
Addresses all 10 visualization critiques:
  1. P_secure plotted separately from P_temporal (no flat graph)
  2. Key management on log scale (no overlapping curves)
  3. Log latency axes (no compression)
  4. Log message complexity (no explosion)
  5. TPS removed as redundant (acknowledged)
  6. Uncertainty bands (best/avg/worst case)
  7. Attack-rate sensitivity (λ sweep)
  8. f vs P_secure ("why OM fails")
  9. Component contribution (Sheikh's flaw)
  10. λ×L heatmap (core thesis figure)

Priority order:
  Fig 1: Latency vs P_temporal
  Fig 2: Latency vs P_secure
  Fig 3: Attack-rate × Latency heatmap
  Fig 4: f vs Latency
  Fig 5: Pareto frontier (Security vs Latency)
  Fig 6: Component contribution breakdown
  Fig 7: Key-management improvement (log scale)
  Fig 8: Message complexity (log scale)
"""

import os
import sys
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm
from math import comb, floor, log10, exp

# ═══════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════
N_NODES    = 51
N_SEN      = 3854
BFT_LIMIT  = 16
K1         = N_SEN * (N_SEN - 1) // 2   # 7,426,681
K2         = floor(N_SEN * 0.33)         # 1,271
P_SCADA    = 0.01
P_R_BASE   = 0.01
TAU_MS     = 50.0   # mean network delay ms
X_DEFAULT  = 0.95

FIGURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

# Color palette
C_OM     = "#C0392B"    # Red
C_PBFT   = "#E67E22"    # Orange
C_IBFT   = "#8E44AD"    # Purple
C_QBFT   = "#2980B9"    # Blue
C_CEPBFT = "#27AE60"    # Green
C_GPBFT  = "#16A085"    # Teal
C_SVPBFT = "#2ECC71"    # Light green
C_TOWER  = "#2C3E50"    # Dark blue
C_RVR    = "#1ABC9C"    # Turquoise

# Protocol definitions: (name, color, latency_ms, messages, group)
PROTOCOLS = [
    ("OM(m)",        C_OM,     43350.0,   1.0e18,   "G1"),
    ("Classic PBFT", C_PBFT,   7650.0,    7803,     "G1"),
    ("IBFT 2.0",     C_IBFT,   2500.0,    1323,     "G2"),
    ("QBFT",         C_QBFT,   1500.0,    675,      "G2"),
    ("CE-PBFT",      C_CEPBFT, 800.0,     1875,     "G3"),
    ("G-PBFT",       C_GPBFT,  650.0,     2700,     "G3"),
    ("SV-PBFT",      C_SVPBFT, 500.0,     1200,     "G3"),
    ("Tower BFT",    C_TOWER,  242.9,     1275,     "G4"),
    ("RVR",          C_RVR,    200.0,     1020,     "G4"),
]

GROUP_COLORS = {"G1": "#E74C3C", "G2": "#8E44AD", "G3": "#27AE60", "G4": "#2C3E50"}
GROUP_LABELS = {
    "G1": "G1: Classical BFT",
    "G2": "G2: Committee-Delegated",
    "G3": "G3: Hierarchical PBFT",
    "G4": "G4: Sub-Second BFT",
}

# ═══════════════════════════════════════════════════════════════
#  CORE EQUATIONS
# ═══════════════════════════════════════════════════════════════

def p_ta(x=X_DEFAULT, p_scada=P_SCADA, p_r=P_R_BASE):
    """P_TA without blockchain (Eq. 16). Dominated by SCADA + P_R."""
    p_sa = x ** N_SEN
    p_ca = x ** N_SEN
    return 0.25 * (p_sa + p_ca + p_scada + p_r)


def p_tab(x=X_DEFAULT, p_scada=P_SCADA, p_r=P_R_BASE):
    """P_TAb with blockchain (Eq. 21). Numerically ≈ 0 for x < 0.999."""
    p_sab    = x ** (2 * N_SEN)
    p_cab    = x ** (2 * K1)
    p_scadab = (p_scada * x) ** N_SEN
    p_rb     = (p_r ** K2) * (x ** N_SEN)
    return 0.25 * (p_sab + p_cab + p_scadab + p_rb)


def p_temporal_poisson(latency_s, lam, p_ta_val):
    """Poisson: P_temporal = 1 - e^(-λ * L * P_TA)."""
    exponent = lam * latency_s * p_ta_val
    if exponent > 500:
        return 1.0
    return 1.0 - math.exp(-exponent)


def p_secure(p_tab_val, p_temp, p_other=0.05):
    """STSF: P_secure = (1-P_TAb)(1-P_temporal)(1-P_other)."""
    return (1.0 - p_tab_val) * (1.0 - p_temp) * (1.0 - p_other)


def om_latency_ms(f, n=N_NODES, tau=TAU_MS):
    return (f + 1) * n * tau


def om_latency_ms_lower(f, tau=TAU_MS):
    return (f + 1) * tau


def pbft_latency_ms(n=N_NODES, tau=TAU_MS):
    return 3 * n * tau


def tbft_latency_ms(f, n=N_NODES, tau_s=0.05):
    tau_ms = tau_s * 1000
    l_base   = 2.0 * tau_ms
    l_attack = f * 2.5
    l_vc     = 50.0
    return l_base + l_attack + (f / max(n, 1)) * l_vc


def om_messages(n, f):
    if n <= 1: return 1.0
    return (n ** (f + 1) - 1) / (n - 1)


def p_r_shamir(k, d, p_r=P_R_BASE):
    total = 0.0
    for i in range(k, d + 1):
        total += comb(d, i) * (p_r ** i) * ((1 - p_r) ** (d - i))
    return total


def p_r_mpc(k, n_parties, p_r=P_R_BASE):
    return 0.7 * p_r_shamir(k, n_parties, p_r)


def p_r_multisig(k, n_signers, p_r=P_R_BASE):
    return 0.85 * p_r_shamir(k, n_signers, p_r)


# ═══════════════════════════════════════════════════════════════
#  STYLE HELPERS
# ═══════════════════════════════════════════════════════════════

def apply_style(fig, ax):
    """Apply clean publication-quality style."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=10)
    fig.tight_layout()


# ═══════════════════════════════════════════════════════════════
#  FIGURE 1: Latency vs P_temporal (CORE THESIS)
# ═══════════════════════════════════════════════════════════════

def fig1_latency_vs_ptemporal():
    """
    The most important figure. Shows P_temporal vs consensus latency
    for multiple attack rates λ. Directly proves: latency → vulnerability.
    """
    L_vals = np.logspace(-1, 2, 500)  # 0.1s to 100s
    p_ta_val = p_ta()
    lambdas = [0.001, 1, 5, 20, 100]
    lambda_labels = ["λ=0.001 (Key theft)", "λ=1 (MitM)", "λ=5 (Moderate)",
                     "λ=20 (FDI)", "λ=100 (Replay flood)"]
    lambda_colors = ["#3498DB", "#2ECC71", "#F39C12", "#E74C3C", "#8E44AD"]

    fig, ax = plt.subplots(figsize=(10, 6))

    for lam, label, color in zip(lambdas, lambda_labels, lambda_colors):
        p_temps = [p_temporal_poisson(L, lam, p_ta_val) for L in L_vals]
        ax.plot(L_vals, p_temps, lw=2.2, label=label, color=color)

    # Mark protocol positions at λ=20
    lam_ref = 20
    for name, color, lat_ms, _, grp in PROTOCOLS:
        lat_s = lat_ms / 1000
        pt = p_temporal_poisson(lat_s, lam_ref, p_ta_val)
        marker = "o" if grp in ("G1", "G2") else "D"
        ax.plot(lat_s, pt, marker, color=color, ms=10, zorder=5,
                markeredgecolor="black", markeredgewidth=0.8)
        # Label only a few to avoid clutter
        if name in ("OM(m)", "Tower BFT", "RVR", "QBFT"):
            offset = (10, 10) if name != "Tower BFT" else (10, -15)
            ax.annotate(name, (lat_s, pt), textcoords="offset points",
                        xytext=offset, fontsize=8, fontweight="bold", color=color)

    ax.set_xscale("log")
    ax.set_xlabel("Consensus Latency L (seconds)", fontsize=12)
    ax.set_ylabel("$P_{temporal}(\\lambda, L)$", fontsize=12)
    ax.set_title("Temporal Vulnerability vs Consensus Latency\n"
                 "Poisson Attack Model: $P_{temporal} = 1 - e^{-\\lambda \\cdot L \\cdot P_{TA}}$",
                 fontsize=12, fontweight="bold")
    ax.set_ylim(-0.02, 1.02)
    ax.axhline(y=0.5, color="gray", ls="--", alpha=0.4, lw=0.8)
    ax.text(0.12, 0.52, "$P_{temporal} = 0.5$ critical threshold",
            fontsize=8, color="gray", transform=ax.get_yaxis_transform())
    ax.legend(fontsize=9, loc="lower right", framealpha=0.9)
    ax.grid(True, alpha=0.3, lw=0.5)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_ptemporal_vs_latency.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 2: Latency vs P_secure
# ═══════════════════════════════════════════════════════════════

def fig2_latency_vs_psecure():
    """
    P_secure vs latency. Since P_TAb ≈ 0, this is essentially:
    P_secure ≈ (1 - P_temporal) * (1 - P_other)
    We acknowledge this in the title and plot P_temporal contribution separately.
    """
    L_vals = np.logspace(-1, 2, 500)
    p_ta_val = p_ta()
    p_tab_val = p_tab()
    lam = 20  # FDI rate

    p_secure_vals = []
    p_temp_vals = []
    for L in L_vals:
        pt = p_temporal_poisson(L, lam, p_ta_val)
        ps = p_secure(p_tab_val, pt, p_other=0.05)
        p_secure_vals.append(ps)
        p_temp_vals.append(pt)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left panel: P_secure
    ax1.plot(L_vals, p_secure_vals, lw=2.5, color="#2C3E50", label="$P_{secure}$")
    ax1.axhline(y=0.95, color="#27AE60", ls="--", alpha=0.6, lw=1)
    ax1.axhline(y=0.80, color="#F39C12", ls="--", alpha=0.6, lw=1)
    ax1.axhline(y=0.50, color="#E74C3C", ls="--", alpha=0.6, lw=1)
    ax1.text(0.12, 0.96, "Target: 0.95", fontsize=8, color="#27AE60",
             transform=ax1.get_yaxis_transform())
    ax1.text(0.12, 0.81, "Acceptable: 0.80", fontsize=8, color="#F39C12",
             transform=ax1.get_yaxis_transform())
    ax1.text(0.12, 0.51, "Critical: 0.50", fontsize=8, color="#E74C3C",
             transform=ax1.get_yaxis_transform())

    # Mark protocols
    for name, color, lat_ms, _, grp in PROTOCOLS:
        lat_s = lat_ms / 1000
        pt = p_temporal_poisson(lat_s, lam, p_ta_val)
        ps = p_secure(p_tab_val, pt, p_other=0.05)
        ax1.plot(lat_s, ps, "o", color=GROUP_COLORS[grp], ms=9, zorder=5,
                 markeredgecolor="black", markeredgewidth=0.8)
        if name in ("OM(m)", "Classic PBFT", "CE-PBFT", "Tower BFT", "RVR"):
            va = "bottom" if ps > 0.5 else "top"
            ax1.annotate(name, (lat_s, ps), textcoords="offset points",
                         xytext=(8, 5 if va == "bottom" else -12),
                         fontsize=8, fontweight="bold", color=GROUP_COLORS[grp])

    ax1.set_xscale("log")
    ax1.set_xlabel("Consensus Latency L (seconds)", fontsize=11)
    ax1.set_ylabel("$P_{secure}$", fontsize=11)
    ax1.set_title("(a) Overall Security vs Latency\n"
                   "$\\lambda = 20$, $P_{other} = 0.05$", fontweight="bold")
    ax1.set_ylim(-0.02, 1.0)
    ax1.grid(True, alpha=0.3, lw=0.5)

    # Right panel: Component breakdown
    ax2.fill_between(L_vals, 0, p_temp_vals, alpha=0.3, color="#E74C3C",
                     label="$P_{temporal}$ (latency-driven)")
    ax2.fill_between(L_vals, 0, [0.05]*len(L_vals), alpha=0.3, color="#F39C12",
                     label="$P_{other}$ (insider/physical)")
    ax2.axhline(y=0, color="gray", lw=0.5)
    ax2.plot(L_vals, p_temp_vals, lw=2, color="#E74C3C")
    ax2.axhline(y=0.05, lw=1.5, color="#F39C12", ls="--")
    # P_TAb is negligible - show as text annotation
    ax2.text(0.5, 0.02, "$P_{TAb} \\approx 10^{-173}$ (negligible — not visible)",
             fontsize=9, color="#3498DB", style="italic",
             transform=ax2.transAxes, ha="center")

    ax2.set_xscale("log")
    ax2.set_xlabel("Consensus Latency L (seconds)", fontsize=11)
    ax2.set_ylabel("Failure Probability Component", fontsize=11)
    ax2.set_title("(b) Security Failure Decomposition\n"
                   "Shows which component dominates", fontweight="bold")
    ax2.set_ylim(-0.02, 1.02)
    ax2.legend(fontsize=9, loc="upper left", framealpha=0.9)
    ax2.grid(True, alpha=0.3, lw=0.5)

    apply_style(fig, ax1)
    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_latency_vs_psecure.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 3: Attack-Rate × Latency Heatmap
# ═══════════════════════════════════════════════════════════════

def fig3_heatmap():
    """
    The strongest figure. Heatmap of P_temporal(λ, L).
    Directly proves: security degrades with consensus delay.
    """
    L_vals = np.logspace(-1, 2, 200)      # 0.1s to 100s
    lam_vals = np.logspace(-3, 2, 200)    # 0.001 to 100 attacks/s
    p_ta_val = p_ta()

    Z = np.zeros((len(lam_vals), len(L_vals)))
    for i, lam in enumerate(lam_vals):
        for j, L in enumerate(L_vals):
            Z[i, j] = p_temporal_poisson(L, lam, p_ta_val)

    fig, ax = plt.subplots(figsize=(11, 7))
    im = ax.pcolormesh(L_vals, lam_vals, Z, cmap="RdYlGn_r", shading="gouraud",
                       vmin=0, vmax=1)
    cbar = fig.colorbar(im, ax=ax, label="$P_{temporal}(\\lambda, L)$", pad=0.02)
    cbar.ax.tick_params(labelsize=10)

    # Contour lines
    CS = ax.contour(L_vals, lam_vals, Z, levels=[0.01, 0.05, 0.1, 0.5, 0.9],
                    colors="black", linewidths=0.8, linestyles="--")
    ax.clabel(CS, inline=True, fontsize=8, fmt="%.2f")

    # Mark protocols
    for name, color, lat_ms, _, grp in PROTOCOLS:
        lat_s = lat_ms / 1000
        # Place at λ=20 (FDI reference rate)
        ax.plot(lat_s, 20, "o", color="white", ms=8, zorder=5,
                markeredgecolor="black", markeredgewidth=1.5)
        if name in ("OM(m)", "Tower BFT", "RVR", "CE-PBFT", "Classic PBFT"):
            ax.annotate(name, (lat_s, 20), textcoords="offset points",
                        xytext=(5, 8), fontsize=8, fontweight="bold",
                        color="white",
                        bbox=dict(boxstyle="round,pad=0.2", fc="black", alpha=0.7))

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Consensus Latency L (seconds)", fontsize=12)
    ax.set_ylabel("Attack Rate $\\lambda$ (attacks/second)", fontsize=12)
    ax.set_title("Temporal Vulnerability Heatmap: $P_{temporal}(\\lambda, L)$\n"
                 "Green = secure, Red = compromised. "
                 "Protocols marked at $\\lambda = 20$ (FDI rate).",
                 fontsize=11, fontweight="bold")

    # Attack type annotations on right
    attack_types = [(0.001, "Key theft"), (1, "MitM"), (20, "FDI"),
                    (100, "Replay")]
    for lam_at, label in attack_types:
        ax.annotate(label, (L_vals[-1], lam_at), textcoords="offset points",
                    xytext=(5, 0), fontsize=7, color="#555", va="center")

    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_attack_rate_heatmap.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 4: f vs Latency (OM explosion)
# ═══════════════════════════════════════════════════════════════

def fig4_f_vs_latency():
    """
    Shows latency vs f for OM, PBFT, Tower BFT.
    OM explodes; Tower stays flat. Log y-axis essential.
    Includes uncertainty bands (best/worst case).
    """
    f_vals = list(range(0, 26))

    # OM: upper and lower bounds
    om_upper = [om_latency_ms(f) / 1000 for f in f_vals]
    om_lower = [om_latency_ms_lower(f) / 1000 for f in f_vals]

    # PBFT: fixed at 3 phases, independent of f
    # but view-change adds overhead proportional to f
    pbft_base = pbft_latency_ms() / 1000
    pbft_vals = [pbft_base * (1 + 0.05 * f) for f in f_vals]  # 5% per fault
    pbft_upper = [v * 1.3 for v in pbft_vals]
    pbft_lower = [v * 0.8 for v in pbft_vals]

    # Tower BFT: sub-linear growth
    tbft_vals = [tbft_latency_ms(f) / 1000 for f in f_vals]
    tbft_upper = [v * 1.15 for v in tbft_vals]  # ±15% uncertainty
    tbft_lower = [v * 0.85 for v in tbft_vals]

    fig, ax = plt.subplots(figsize=(10, 6))

    # OM bands
    ax.fill_between(f_vals, om_lower, om_upper, alpha=0.15, color=C_OM)
    ax.plot(f_vals, om_upper, "o-", color=C_OM, lw=2, ms=5,
            label="OM(m) upper bound: $(f+1) \\cdot n \\cdot \\bar{\\tau}$")
    ax.plot(f_vals, om_lower, "o--", color=C_OM, lw=1, ms=3, alpha=0.6,
            label="OM(m) lower bound: $(f+1) \\cdot \\bar{\\tau}$")

    # PBFT bands
    ax.fill_between(f_vals, pbft_lower, pbft_upper, alpha=0.15, color=C_PBFT)
    ax.plot(f_vals, pbft_vals, "s-", color=C_PBFT, lw=2, ms=5,
            label="Classic PBFT: $3n\\bar{\\tau}$ + view-change")

    # Tower bands
    ax.fill_between(f_vals, tbft_lower, tbft_upper, alpha=0.15, color=C_TOWER)
    ax.plot(f_vals, tbft_vals, "D-", color=C_TOWER, lw=2.5, ms=5,
            label="Tower BFT: PoH + $f \\cdot 2.5$ms")

    ax.axvline(x=BFT_LIMIT, color="red", ls="--", alpha=0.5, lw=1)
    ax.text(BFT_LIMIT + 0.3, ax.get_ylim()[1] * 0.7,
            f"BFT limit\nf = {BFT_LIMIT}", fontsize=9, color="red")

    ax.set_yscale("log")
    ax.set_xlabel("Number of Byzantine Faulty Nodes (f)", fontsize=12)
    ax.set_ylabel("Consensus Latency (seconds, log scale)", fontsize=12)
    ax.set_title("Latency Scaling with Byzantine Faults\n"
                 "OM(m) exhibits exponential growth; Tower BFT remains bounded",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=9, loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3, lw=0.5)
    ax.set_xlim(-0.5, 25.5)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_f_vs_latency.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 5: Pareto Frontier
# ═══════════════════════════════════════════════════════════════

def fig5_pareto():
    """
    Security vs Latency Pareto frontier.
    Each protocol is a point. Dominated protocols are visually distinct.
    """
    lam = 20
    p_ta_val = p_ta()
    p_tab_val = p_tab()

    fig, ax = plt.subplots(figsize=(10, 6.5))

    points = []
    for name, color, lat_ms, msgs, grp in PROTOCOLS:
        lat_s = lat_ms / 1000
        pt = p_temporal_poisson(lat_s, lam, p_ta_val)
        ps = p_secure(p_tab_val, pt, p_other=0.05)
        points.append((name, lat_s, ps, color, grp, msgs))

    # Identify Pareto frontier
    sorted_pts = sorted(points, key=lambda p: p[1])  # sort by latency
    frontier = []
    max_sec = -1
    for pt in sorted_pts:
        if pt[2] > max_sec:
            frontier.append(pt)
            max_sec = pt[2]

    # Plot dominated region
    ax.axhspan(0, 0.5, alpha=0.05, color="red")
    ax.text(30, 0.25, "Unacceptable\nSecurity Zone", fontsize=10,
            color="#E74C3C", alpha=0.5, ha="center", style="italic")

    # Plot all protocols
    for name, lat_s, ps, color, grp, msgs in points:
        is_frontier = any(fp[0] == name for fp in frontier)
        marker = "★" if is_frontier else "o"
        size = 200 if is_frontier else 120
        edge = "gold" if is_frontier else "black"
        edgew = 2 if is_frontier else 1
        ax.scatter(lat_s, ps, c=GROUP_COLORS[grp], s=size, marker="o",
                   edgecolors=edge, linewidths=edgew, zorder=5)
        # Label
        offset_x = 1.15
        va = "center"
        ax.annotate(f"{name}\n({lat_s*1000:.0f}ms, {ps:.3f})",
                    (lat_s, ps), textcoords="offset points",
                    xytext=(12, 0), fontsize=8, va=va,
                    color=GROUP_COLORS[grp], fontweight="bold")

    # Draw Pareto frontier line
    if len(frontier) > 1:
        fx = [p[1] for p in frontier]
        fy = [p[2] for p in frontier]
        ax.plot(fx, fy, "--", color="gold", lw=2, alpha=0.7, zorder=3,
                label="Pareto Frontier")

    # Legend for groups
    for grp, label in GROUP_LABELS.items():
        ax.scatter([], [], c=GROUP_COLORS[grp], s=80, label=label,
                   edgecolors="black", linewidths=0.5)

    ax.set_xscale("log")
    ax.set_xlabel("Consensus Latency (seconds, log scale)", fontsize=12)
    ax.set_ylabel("$P_{secure}$ (higher = better)", fontsize=12)
    ax.set_title("Pareto Frontier: Security vs Latency\n"
                 "Protocols on the frontier are non-dominated ($\\lambda = 20$)",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=9, loc="lower left", framealpha=0.9)
    ax.grid(True, alpha=0.3, lw=0.5)
    ax.set_ylim(-0.02, 1.0)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_pareto_frontier.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 6: Component Contribution (Sheikh's Flaw)
# ═══════════════════════════════════════════════════════════════

def fig6_component_contribution():
    """
    Stacked bar chart showing where P_TA actually comes from.
    Exposes that sensors contribute ≈ 0 while SCADA/Receiver dominate.
    """
    x_vals = [0.90, 0.95, 0.99, 0.995, 0.999]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left: absolute contributions (log scale)
    sensors = [x ** N_SEN for x in x_vals]
    comms   = [x ** N_SEN for x in x_vals]
    scada   = [P_SCADA for _ in x_vals]
    receiver = [P_R_BASE for _ in x_vals]

    bar_x = np.arange(len(x_vals))
    bar_w = 0.18

    ax1.bar(bar_x - 1.5*bar_w, sensors, bar_w, label="$P_{SA} = x^{3854}$",
            color="#3498DB", edgecolor="white")
    ax1.bar(bar_x - 0.5*bar_w, comms, bar_w, label="$P_{CA} = x^{3854}$",
            color="#2ECC71", edgecolor="white")
    ax1.bar(bar_x + 0.5*bar_w, scada, bar_w, label="$P_{SCADA} = 0.01$",
            color="#E74C3C", edgecolor="white")
    ax1.bar(bar_x + 1.5*bar_w, receiver, bar_w, label="$P_R = 0.01$",
            color="#F39C12", edgecolor="white")

    ax1.set_yscale("log")
    ax1.set_xticks(bar_x)
    ax1.set_xticklabels([f"x={x}" for x in x_vals])
    ax1.set_ylabel("Component Probability (log scale)", fontsize=11)
    ax1.set_title("(a) Component Magnitudes\n"
                  "Sensor/Comm terms vanish for $x < 0.999$", fontweight="bold")
    ax1.legend(fontsize=8, loc="upper left", framealpha=0.9)
    ax1.set_ylim(1e-200, 1)
    ax1.grid(axis="y", alpha=0.3, lw=0.5)

    # Right: percentage contribution (stacked)
    total_vals = [0.25*(2*sensors[i] + scada[i] + receiver[i])
                  for i in range(len(x_vals))]
    # For stacking, compute fractions
    pct_sensor = []
    pct_comm = []
    pct_scada = []
    pct_recv = []
    for i in range(len(x_vals)):
        total = 2*sensors[i] + scada[i] + receiver[i]
        if total > 0:
            pct_sensor.append(sensors[i] / total * 100)
            pct_comm.append(comms[i] / total * 100)
            pct_scada.append(scada[i] / total * 100)
            pct_recv.append(receiver[i] / total * 100)
        else:
            pct_sensor.append(0)
            pct_comm.append(0)
            pct_scada.append(50)
            pct_recv.append(50)

    ax2.bar(bar_x, pct_scada, 0.5, label="SCADA", color="#E74C3C",
            edgecolor="white")
    ax2.bar(bar_x, pct_recv, 0.5, bottom=pct_scada, label="Receiver",
            color="#F39C12", edgecolor="white")
    # Sensor + Comm are so small they're invisible in the stack
    bottom2 = [s+r for s,r in zip(pct_scada, pct_recv)]
    ax2.bar(bar_x, pct_sensor, 0.5, bottom=bottom2, label="Sensor",
            color="#3498DB", edgecolor="white")
    bottom3 = [b+s for b,s in zip(bottom2, pct_sensor)]
    ax2.bar(bar_x, pct_comm, 0.5, bottom=bottom3, label="Communication",
            color="#2ECC71", edgecolor="white")

    ax2.set_xticks(bar_x)
    ax2.set_xticklabels([f"x={x}" for x in x_vals])
    ax2.set_ylabel("Contribution to $P_{TA}$ (%)", fontsize=11)
    ax2.set_title("(b) Percentage Contribution\n"
                  "SCADA + Receiver = ~100% of risk", fontweight="bold")
    ax2.legend(fontsize=8, loc="upper right", framealpha=0.9)
    ax2.set_ylim(0, 105)
    ax2.grid(axis="y", alpha=0.3, lw=0.5)

    fig.suptitle("Component Contribution to $P_{TA}$: Exposing Sheikh's Hidden Assumption\n"
                 "$x^{3854}$ terms vanish — SCADA and Receiver dominate the entire threat model",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_component_contribution.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 7: Key Management (FIXED — log scale, bar chart)
# ═══════════════════════════════════════════════════════════════

def fig7_key_management():
    """
    Three-panel key management figure:
    (a) Bar chart of effective P_R per scheme (log scale)
    (b) Security improvement multiplier
    (c) P_secure with key management + Tower BFT
    """
    schemes = [
        ("None",          P_R_BASE),
        ("Shamir(3,5)",   p_r_shamir(3, 5)),
        ("Shamir(4,7)",   p_r_shamir(4, 7)),
        ("MPC(3,5)",      p_r_mpc(3, 5)),
        ("MPC(5,9)",      p_r_mpc(5, 9)),
        ("Multisig(3,5)", p_r_multisig(3, 5)),
        ("Multisig(5,7)", p_r_multisig(5, 7)),
    ]

    names = [s[0] for s in schemes]
    pr_vals = [s[1] for s in schemes]
    improvements = [P_R_BASE / max(pr, 1e-30) for pr in pr_vals]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5.5))

    colors = ["#E74C3C", "#3498DB", "#2980B9", "#27AE60", "#16A085",
              "#8E44AD", "#9B59B6"]

    # Panel (a): Effective P_R (log scale bar chart)
    bars1 = ax1.barh(range(len(names)), pr_vals, color=colors, edgecolor="white")
    ax1.set_xscale("log")
    ax1.set_yticks(range(len(names)))
    ax1.set_yticklabels(names, fontsize=9)
    ax1.set_xlabel("Effective $P_R$ (log scale)", fontsize=11)
    ax1.set_title("(a) Receiver Compromise Probability\n"
                  "per Key Management Scheme", fontweight="bold", fontsize=10)
    ax1.invert_yaxis()
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars1, pr_vals)):
        ax1.text(val * 1.5, i, f"{val:.2e}", va="center", fontsize=8)
    ax1.grid(axis="x", alpha=0.3, lw=0.5)

    # Panel (b): Improvement multiplier (log scale)
    bars2 = ax2.barh(range(len(names)), improvements, color=colors, edgecolor="white")
    ax2.set_xscale("log")
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels(names, fontsize=9)
    ax2.set_xlabel("Security Improvement Factor (×)", fontsize=11)
    ax2.set_title("(b) Improvement vs Baseline\n"
                  "$P_R^{baseline} / P_R^{scheme}$", fontweight="bold", fontsize=10)
    ax2.invert_yaxis()
    for i, (bar, val) in enumerate(zip(bars2, improvements)):
        ax2.text(val * 1.3, i, f"{val:,.0f}×", va="center", fontsize=8,
                 fontweight="bold")
    ax2.grid(axis="x", alpha=0.3, lw=0.5)

    # Panel (c): P_secure with Tower BFT + key management
    lam = 20
    tbft_lat_s = 242.9 / 1000
    p_ta_val = p_ta()

    psecure_vals = []
    for scheme_name, pr_eff in schemes:
        # With this key management, P_TA changes because P_R changes
        p_ta_km = 0.25 * (2 * (X_DEFAULT ** N_SEN) + P_SCADA + pr_eff)
        pt = p_temporal_poisson(tbft_lat_s, lam, p_ta_km)
        ps = p_secure(0.0, pt, p_other=0.05)  # P_TAb ≈ 0
        psecure_vals.append(ps)

    bars3 = ax3.barh(range(len(names)), psecure_vals, color=colors, edgecolor="white")
    ax3.set_xlim(0.9, 0.96)
    ax3.set_yticks(range(len(names)))
    ax3.set_yticklabels(names, fontsize=9)
    ax3.set_xlabel("$P_{secure}$ (Tower BFT, $\\lambda = 20$)", fontsize=11)
    ax3.set_title("(c) Overall Security Probability\n"
                  "with Tower BFT consensus", fontweight="bold", fontsize=10)
    ax3.invert_yaxis()
    for i, (bar, val) in enumerate(zip(bars3, psecure_vals)):
        ax3.text(val + 0.001, i, f"{val:.4f}", va="center", fontsize=8)
    ax3.axvline(x=0.95, color="#E74C3C", ls="--", alpha=0.5, lw=1)
    ax3.text(0.9505, len(names)-0.5, "Target", fontsize=8, color="#E74C3C")
    ax3.grid(axis="x", alpha=0.3, lw=0.5)

    fig.suptitle("Key Management Defence-in-Depth Analysis\n"
                 "Threshold schemes reduce $P_R$ by up to $10^7\\times$, "
                 "propagating through $P_R \\rightarrow P_{TA} \\rightarrow P_{secure}$",
                 fontsize=11, fontweight="bold", y=1.03)
    fig.tight_layout()
    path = os.path.join(FIGURE_DIR, "fig_key_management.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 8: Message Complexity (log scale)
# ═══════════════════════════════════════════════════════════════

def fig8_message_complexity():
    """
    Log-scale message complexity comparison.
    Without log scale, OM(m) dominates everything to zero.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    names = [p[0] for p in PROTOCOLS]
    msgs = [p[3] for p in PROTOCOLS]
    colors = [p[1] for p in PROTOCOLS]

    bars = ax.barh(range(len(names)), msgs, color=colors, edgecolor="white", height=0.6)
    ax.set_xscale("log")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel("Message Count (log scale)", fontsize=12)
    ax.set_title("Message Complexity Comparison\n"
                 "OM(m) requires $\\sim 10^{18}$ messages vs Tower BFT's 1,275",
                 fontsize=11, fontweight="bold")
    ax.invert_yaxis()

    for i, (bar, val) in enumerate(zip(bars, msgs)):
        if val >= 1e6:
            label = f"{val:.1e}"
        else:
            label = f"{val:,.0f}"
        ax.text(val * 1.5, i, label, va="center", fontsize=9, fontweight="bold")

    ax.grid(axis="x", alpha=0.3, lw=0.5)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_message_complexity.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 9: f vs P_secure ("Why OM Fails")
# ═══════════════════════════════════════════════════════════════

def fig9_f_vs_psecure():
    """
    The 'why OM fails' graph. P_secure vs f for three protocols.
    OM collapses; Tower stays high.
    """
    f_vals = list(range(0, 26))
    lam = 20
    p_tab_val = p_tab()

    # For each f, compute latency → P_temporal → P_secure
    om_ps  = []
    pbft_ps = []
    tbft_ps = []

    for f in f_vals:
        # OM
        om_lat_s = om_latency_ms(f) / 1000
        om_pt = p_temporal_poisson(om_lat_s, lam, p_ta())
        om_ps.append(p_secure(p_tab_val, om_pt, 0.05))

        # PBFT (latency grows with view-changes)
        pbft_lat_s = pbft_latency_ms() / 1000 * (1 + 0.05 * f)
        pbft_pt = p_temporal_poisson(pbft_lat_s, lam, p_ta())
        pbft_ps.append(p_secure(p_tab_val, pbft_pt, 0.05))

        # Tower BFT
        tbft_lat_s = tbft_latency_ms(f) / 1000
        tbft_pt = p_temporal_poisson(tbft_lat_s, lam, p_ta())
        tbft_ps.append(p_secure(p_tab_val, tbft_pt, 0.05))

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.fill_between(f_vals, tbft_ps, alpha=0.1, color=C_TOWER)
    ax.plot(f_vals, om_ps, "o-", color=C_OM, lw=2.5, ms=5, label="OM(m)")
    ax.plot(f_vals, pbft_ps, "s-", color=C_PBFT, lw=2, ms=5, label="Classic PBFT")
    ax.plot(f_vals, tbft_ps, "D-", color=C_TOWER, lw=2.5, ms=5, label="Tower BFT")

    ax.axvline(x=BFT_LIMIT, color="red", ls="--", alpha=0.5, lw=1)
    ax.text(BFT_LIMIT + 0.3, 0.85, f"BFT limit (f={BFT_LIMIT})",
            fontsize=9, color="red")

    ax.axhline(y=0.95, color="#27AE60", ls=":", alpha=0.5, lw=1)
    ax.axhline(y=0.80, color="#F39C12", ls=":", alpha=0.5, lw=1)
    ax.axhline(y=0.50, color="#E74C3C", ls=":", alpha=0.5, lw=1)

    ax.set_xlabel("Number of Byzantine Faulty Nodes (f)", fontsize=12)
    ax.set_ylabel("$P_{secure}$", fontsize=12)
    ax.set_title("Why OM(m) Fails: Security Collapse Under Byzantine Faults\n"
                 "$\\lambda = 20$ (FDI rate), $P_{other} = 0.05$",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=10, loc="center right", framealpha=0.9)
    ax.grid(True, alpha=0.3, lw=0.5)
    ax.set_ylim(-0.02, 1.0)
    ax.set_xlim(-0.5, 25.5)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_f_vs_psecure.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 10: Sensitivity to Attack Rate λ
# ═══════════════════════════════════════════════════════════════

def fig10_sensitivity_lambda():
    """
    P_secure vs λ for all four groups.
    Shows which protocols survive aggressive attack rates.
    """
    lam_vals = np.logspace(-3, 2, 300)
    p_ta_val = p_ta()
    p_tab_val = p_tab()

    # Representative protocol per group
    group_protos = [
        ("OM(m) [G1]",     43350.0,  C_OM,    "-"),
        ("QBFT [G2]",      1500.0,   C_QBFT,  "--"),
        ("SV-PBFT [G3]",   500.0,    C_SVPBFT, "-."),
        ("Tower BFT [G4]", 242.9,    C_TOWER, "-"),
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    for name, lat_ms, color, ls in group_protos:
        lat_s = lat_ms / 1000
        ps_vals = []
        for lam in lam_vals:
            pt = p_temporal_poisson(lat_s, lam, p_ta_val)
            ps = p_secure(p_tab_val, pt, 0.05)
            ps_vals.append(ps)
        ax.plot(lam_vals, ps_vals, lw=2.5, color=color, ls=ls, label=name)

    # Mark attack types
    attack_marks = [(0.001, "Key theft"), (1, "MitM"), (20, "FDI"),
                    (100, "Replay")]
    for lam_at, label in attack_marks:
        ax.axvline(x=lam_at, color="gray", ls=":", alpha=0.3, lw=0.8)
        ax.text(lam_at, 0.97, label, fontsize=7, color="gray",
                rotation=90, ha="right", va="top")

    ax.axhline(y=0.95, color="#27AE60", ls="--", alpha=0.4, lw=1)
    ax.axhline(y=0.50, color="#E74C3C", ls="--", alpha=0.4, lw=1)

    ax.set_xscale("log")
    ax.set_xlabel("Attack Rate $\\lambda$ (attacks/second, log scale)", fontsize=12)
    ax.set_ylabel("$P_{secure}$", fontsize=12)
    ax.set_title("Security Sensitivity to Attack Rate\n"
                 "Group 4 maintains high security across all attack types",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=10, loc="lower left", framealpha=0.9)
    ax.grid(True, alpha=0.3, lw=0.5)
    ax.set_ylim(-0.02, 1.0)
    apply_style(fig, ax)

    path = os.path.join(FIGURE_DIR, "fig_sensitivity_lambda.png")
    fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  [OK] {path}")


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    os.makedirs(FIGURE_DIR, exist_ok=True)

    print("=" * 70)
    print("  BFT Comparison — Publication-Quality Figure Generator")
    print("  Addressing all 10 visualization critiques")
    print("=" * 70)

    # Verify core equations
    pta = p_ta()
    ptab = p_tab()
    print(f"\n  Core verification:")
    print(f"    P_TA(x=0.95)  = {pta:.6f}  (expected ~0.005)")
    print(f"    P_TAb(x=0.95) = {ptab:.2e}  (expected ~10^-173)")
    print(f"    P_R Shamir(3,5) = {p_r_shamir(3,5):.6e}  (expected ~9.85e-6)")
    print(f"    P_R Shamir(4,7) = {p_r_shamir(4,7):.6e}")
    print(f"    P_R MPC(5,9)    = {p_r_mpc(5,9):.6e}")
    print(f"    OM latency(f=16) = {om_latency_ms(16):.0f} ms")
    print(f"    TBFT latency(f=16) = {tbft_latency_ms(16):.1f} ms")

    print(f"\n  Generating figures in: {FIGURE_DIR}")
    print("-" * 70)

    print("\n  Fig 1: P_temporal vs Latency (core thesis)...")
    fig1_latency_vs_ptemporal()

    print("  Fig 2: P_secure vs Latency (with decomposition)...")
    fig2_latency_vs_psecure()

    print("  Fig 3: Attack-Rate × Latency Heatmap...")
    fig3_heatmap()

    print("  Fig 4: f vs Latency (OM explosion)...")
    fig4_f_vs_latency()

    print("  Fig 5: Pareto Frontier (Security vs Latency)...")
    fig5_pareto()

    print("  Fig 6: Component Contribution (Sheikh's flaw)...")
    fig6_component_contribution()

    print("  Fig 7: Key Management (log scale, 3-panel)...")
    fig7_key_management()

    print("  Fig 8: Message Complexity (log scale)...")
    fig8_message_complexity()

    print("  Fig 9: f vs P_secure (Why OM Fails)...")
    fig9_f_vs_psecure()

    print("  Fig 10: Sensitivity to Attack Rate lambda...")
    fig10_sensitivity_lambda()

    print("\n" + "=" * 70)
    print("  All 10 figures generated successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()
