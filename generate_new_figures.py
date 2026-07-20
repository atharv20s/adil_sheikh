"""
New Figures Generator for IDS -> BFT Blockchain Paper
=====================================================
Generates Figure 4 (SPOF Risk), Figure 10 (eta sensitivity), and Figure 11 (beta sensitivity)
according to the Figure & Table Design Book.
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import comb, floor, exp

# Setup styles similar to IEEE setup
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

# ═══════════════════════════════════════════════════════════════════
#  FIGURE 4: SPOF RISK (P_Byz vs p_c sweep)
# ═══════════════════════════════════════════════════════════════════
def generate_fig4():
    print("Generating Figure 4 (SPOF Risk)...")
    pc_vals = np.linspace(0.01, 0.20, 100)
    p_byz_ids = np.ones_like(pc_vals)
    
    n = 51
    f = 16
    p_byz_bft = []
    for pc in pc_vals:
        val = sum(comb(n, i) * (pc**i) * ((1.0 - pc)**(n - i)) for i in range(f + 1, n + 1))
        p_byz_bft.append(val)
    
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.plot(pc_vals, p_byz_ids, color='#C0392B', linestyle='--', label='Centralized IDS (SPOF)')
    ax.plot(pc_vals, p_byz_bft, color='#2980B9', linestyle='-', label='BFT Blockchain ($n=51, f=16$)')
    
    ax.set_yscale('log')
    ax.set_xlabel('Per-Validator / Coordinator Compromise Probability ($p_c$)')
    ax.set_ylabel('Byzantine Failure Probability ($P_{Byz}$)')
    ax.set_title('Single Point of Failure (SPOF) Risk Comparison')
    ax.legend(loc='lower right')
    
    # Highlight threshold
    ax.axhline(1e-5, color='gray', linestyle=':', alpha=0.5)
    ax.text(0.02, 2e-5, '$10^{-5}$ Safety Threshold', color='gray', fontsize=7.5)
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_spof_risk.png"), dpi=300)
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════
#  FIGURE 10 & 11: SENSITIVITY SWEEPS (eta and beta)
# ═══════════════════════════════════════════════════════════════════
def p_temporal_poisson(latency_ms, lambda_attack, p_ta_val):
    latency_sec = latency_ms / 1000.0
    exponent = lambda_attack * latency_sec * p_ta_val
    if exponent > 700:
        return 1.0
    return 1.0 - exp(-exponent)

def p_secure_correlated(p_static, p_temporal, rho=0.3, p_other=0.05):
    p_joint = rho * min(p_static, p_temporal)
    p_fail = min(1.0, max(0.0, p_static + p_temporal - p_joint))
    return (1.0 - p_fail) * (1.0 - p_other)

def generate_fig10_11():
    print("Generating Figure 10 (eta) and Figure 11 (beta)...")
    eta_vals = np.linspace(0.05, 0.25, 50)
    beta_vals = np.linspace(0.05, 0.25, 50)
    
    # Latencies
    l_pbft = 7650.0
    l_tbft = 242.9
    l_rvr = 200.0
    
    # E1 baseline P_TA (Sheikh Model A, n_sen=3854)
    # At x=0.95, n_sen=3854, P_TA=0.005
    p_ta_base = 0.005
    p_tab_base = 1e-172
    
    # ── Figure 10 (eta sensitivity) ──
    fig10, ax10 = plt.subplots(figsize=(4.5, 3.5))
    
    ps_pbft_eta = []
    ps_tbft_eta = []
    ps_rvr_eta = []
    
    for eta in eta_vals:
        # PBFT
        pt = p_temporal_poisson(l_pbft, 20.0, p_ta_base)
        p_tab_adj = p_tab_base * (1.0 - eta * 0.5)
        ps_pbft_eta.append(p_secure_correlated(p_tab_adj, pt))
        
        # Tower BFT
        pt = p_temporal_poisson(l_tbft, 20.0, p_ta_base)
        ps_tbft_eta.append(p_secure_correlated(p_tab_adj, pt))
        
        # RVR
        pt = p_temporal_poisson(l_rvr, 20.0, p_ta_base)
        ps_rvr_eta.append(p_secure_correlated(p_tab_adj, pt))
        
    ax10.plot(eta_vals, ps_pbft_eta, color='#E67E22', label='Classic PBFT')
    ax10.plot(eta_vals, ps_tbft_eta, color='#2C3E50', label='Tower BFT')
    ax10.plot(eta_vals, ps_rvr_eta, color='#1ABC9C', label='RVR')
    
    ax10.set_xlabel('Spatial Cross-Verification Factor ($\eta$)')
    ax10.set_ylabel('Overall Security Probability ($P_{secure}$)')
    ax10.set_title('Sensitivity of $P_{secure}$ to Spatial Validation Factor $\eta$')
    ax10.legend(loc='center left')
    ax10.spines["top"].set_visible(False)
    ax10.spines["right"].set_visible(False)
    fig10.tight_layout()
    fig10.savefig(os.path.join(FIGURE_DIR, "fig_eta_sensitivity.png"), dpi=300)
    plt.close(fig10)
    
    # ── Figure 11 (beta sensitivity) ──
    fig11, ax11 = plt.subplots(figsize=(4.5, 3.5))
    
    ps_pbft_beta = []
    ps_tbft_beta = []
    ps_rvr_beta = []
    
    for beta in beta_vals:
        # PBFT
        pt = p_temporal_poisson(l_pbft, 20.0, p_ta_base)
        p_tab_adj = p_tab_base * (1.0 - beta * 0.3)
        ps_pbft_beta.append(p_secure_correlated(p_tab_adj, pt))
        
        # Tower BFT
        pt = p_temporal_poisson(l_tbft, 20.0, p_ta_base)
        ps_tbft_beta.append(p_secure_correlated(p_tab_adj, pt))
        
        # RVR
        pt = p_temporal_poisson(l_rvr, 20.0, p_ta_base)
        ps_rvr_beta.append(p_secure_correlated(p_tab_adj, pt))
        
    ax11.plot(beta_vals, ps_pbft_beta, color='#E67E22', label='Classic PBFT')
    ax11.plot(beta_vals, ps_tbft_beta, color='#2C3E50', label='Tower BFT')
    ax11.plot(beta_vals, ps_rvr_beta, color='#1ABC9C', label='RVR')
    
    ax11.set_xlabel('Voting Phase Factor ($\\beta$)')
    ax11.set_ylabel('Overall Security Probability ($P_{secure}$)')
    ax11.set_title('Sensitivity of $P_{secure}$ to Voting Phase Factor $\\beta$')
    ax11.legend(loc='center left')
    ax11.spines["top"].set_visible(False)
    ax11.spines["right"].set_visible(False)
    fig11.tight_layout()
    fig11.savefig(os.path.join(FIGURE_DIR, "fig_beta_sensitivity.png"), dpi=300)
    plt.close(fig11)

if __name__ == "__main__":
    generate_fig4()
    generate_fig10_11()
    print("New figures successfully created and saved to the 'figures' directory.")
