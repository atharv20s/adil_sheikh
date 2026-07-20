"""
Generate Consensus-Dependent Security Table (Table B / Table 3)
=============================================================

This script calculates the consensus-dependent security probabilities and
operational metrics for all 9 BFT consensus algorithms and the Without Blockchain baseline.

Every attack is derived directly from the architectural characteristics of each protocol:
  - Sensor: P = x^{2m} * (1 - eta * n_val/n_global)
  - FDI: P = x^{2m} * (1 - beta * N_phases)
  - Comm: P = x^{2k_1} * sigma_CO
  - MitM: P = y^2 / n_val
  - Replay: P = 0.0 (except Without Blockchain where P = z)
  - Sybil: P = binomial_tail(n_val, f_limit, p_c_eff)
  - DoS: P = p_dos * ((f_limit + 1)/n_val) * sigma_CO * (1 - exp(-L / tau_dos))
  - DDoS: P = p_ddos * ((f_limit + 1)/n_val) * sigma_CO * (1 - exp(-L / tau_dos))
  - Byzantine: P = binomial_tail(n_val, f_limit, p_c_eff)
  - Key: P = p_r_shamir(3, 5, p_r_eff_key)
  - SCADA: P = (P_SCADA * x)^m * p_c_eff * (1 - exp(-L / tau_scada))
  - Receiver: P = p_r_eff_recv^k2 * x^m * (1 - exp(-L / tau_recv))
"""

import math
from math import comb, floor
from dataclasses import dataclass
from typing import Dict, List
import os

# ═══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

X = 0.95            # per-sensor security level
M = 10              # critical sensor subset size
Y_MITM = 0.05       # MitM baseline probability
Z_REPLAY = 0.15     # Replay baseline probability
P_DOS = 0.20        # DoS probability
P_DDOS = 0.35       # DDoS probability
P_KEY = 0.01        # Key compromise probability (per-share for Shamir)
P_SCADA = 0.01      # SCADA compromise probability
P_R = 0.01          # Receiver compromise probability
P_C = 0.05          # Per-validator compromise probability

# Time constants for temporal scaling (seconds)
TAU_DOS = 1.0       # DoS time constant
TAU_RECV = 2.0      # Receiver time constant
TAU_SCADA = 5.0     # SCADA time constant

# ═══════════════════════════════════════════════════════════════════════════════
#  PROTOCOL DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ProtocolConfig:
    name: str
    n_val: int          # Committee size
    f_limit: int        # Fault threshold
    has_vrf: bool       # VRF leader election
    has_credit: bool    # Credit weighting / reputation
    msg_count: float    # Message count (M_c)
    phases: int         # Voting phases
    latency_ms: float
    tps: float

PROTOCOLS = [
    ProtocolConfig("OM(m)",        51, 16, False, False, 2.14e27, 3, 43350.0, 1.15),
    ProtocolConfig("Classic PBFT", 51, 16, False, False, 7854.0,  3, 7650.0,  6.54),
    ProtocolConfig("IBFT 2.0",     21, 6,  False, False, 1323.0,  2, 2500.0,  20.0),
    ProtocolConfig("QBFT",         17, 5,  False, False, 595.0,   2, 1500.0,  33.3),
    ProtocolConfig("CE-PBFT",      25, 8,  False, True,  1900.0,  3, 800.0,   62.5),
    ProtocolConfig("G-PBFT",       30, 9,  False, False, 2730.0,  3, 650.0,   76.9),
    ProtocolConfig("SV-PBFT",      20, 6,  False, True,  1200.0,  3, 500.0,   100.0),
    ProtocolConfig("Tower BFT",    51, 16, False, False, 1275.0,  1, 242.9,   205.8),
    ProtocolConfig("RVR",          51, 16, True,  True,  1020.0,  1, 200.0,   250.0),
]

def binomial_tail(n: int, f: int, p_c: float) -> float:
    return sum(comb(n, i) * (p_c ** i) * ((1.0 - p_c) ** (n - i))
               for i in range(f + 1, n + 1))

def p_r_shamir(k: int, d: int, p_r: float = P_R) -> float:
    return sum(comb(d, i) * (p_r ** i) * ((1.0 - p_r) ** (d - i))
               for i in range(k, d + 1))

def compute_all_attacks(proto: ProtocolConfig) -> Dict[str, float]:
    k1 = M * (M - 1) // 2   # 45 pairwise links
    k2 = floor(M * 0.33)    # 3
    L_sec = proto.latency_ms / 1000.0
    
    # 1. Validator credit weighting discount
    p_c_eff = P_C * (1.0 - 0.40) if proto.has_credit else P_C  # 0.03 vs 0.05
    
    # 2. Sybil & Byzantine
    p_sybil_byz = binomial_tail(proto.n_val, proto.f_limit, p_c_eff)
    
    # 3. Message complexity scaling factor sigma_CO
    log_mc = math.log10(proto.msg_count)
    log_mc_max = math.log10(2.14e27)
    sigma_co = log_mc / log_mc_max
    
    # 4. Key compromise (using credit weighting)
    p_r_eff_key = P_R * (1.0 - 0.40) if proto.has_credit else P_R
    p_key_bc = p_r_shamir(3, 5, p_r_eff_key)
    
    # 5. Receiver override (VRF leader election & latency finality)
    if proto.has_vrf:
        p_r_eff_recv = P_R * (1.0 / proto.n_val)
        p_receiver_static = p_r_eff_recv ** k2 * X ** M
    else:
        p_receiver_static = P_R ** k2 * X ** M
    p_receiver = p_receiver_static * (1.0 - math.exp(-L_sec / TAU_RECV))
        
    # DoS/DDoS temporal scaling
    dos_time_factor = (1.0 - math.exp(-L_sec / TAU_DOS))
    p_dos = P_DOS * ((proto.f_limit + 1) / proto.n_val) * sigma_co * dos_time_factor
    p_ddos = P_DDOS * ((proto.f_limit + 1) / proto.n_val) * sigma_co * dos_time_factor
    
    # SCADA temporal scaling
    scada_time_factor = (1.0 - math.exp(-L_sec / TAU_SCADA))
    p_scada = (P_SCADA * X) ** M * p_c_eff * scada_time_factor
        
    return {
        'Sensor':    X ** (2 * M) * (1.0 - 0.15 * (proto.n_val / 51.0)),
        'FDI':       X ** (2 * M) * (1.0 - 0.10 * proto.phases),
        'Comm':      X ** (2 * k1) * sigma_co,
        'MitM':      Y_MITM ** 2 / proto.n_val,
        'Replay':    0.0,
        'Sybil':     p_sybil_byz,
        'DoS':       p_dos,
        'DDoS':      p_ddos,
        'Byzantine': p_sybil_byz,
        'Key':       p_key_bc,
        'SCADA':     p_scada,
        'Receiver':  p_receiver,
    }

def p_compromise(attacks: Dict[str, float]) -> float:
    product = 1.0
    for p in attacks.values():
        product *= (1.0 - p)
    return 1.0 - product

def fmt_latex(val: float) -> str:
    if val == 0.0:
        return r"$\approx 0$"
    elif val == 1.0:
        return "$1.0$"
    elif val >= 0.01:
        return f"${val:.3f}$"
    elif val >= 0.001:
        return f"${val:.4f}$"
    else:
        exp_val = math.floor(math.log10(abs(val)))
        mantissa = val / (10.0 ** exp_val)
        return f"${mantissa:.2f}{{\\times}}10^{{{exp_val}}}$"

def generate_latex_table() -> str:
    no_bc = {
        'Sensor':    X ** M,
        'FDI':       X ** M,
        'Comm':      X ** M,
        'MitM':      Y_MITM,
        'Replay':    Z_REPLAY,
        'Sybil':     1.0,
        'DoS':       P_DOS,
        'DDoS':      P_DDOS,
        'Byzantine': 1.0,
        'Key':       P_KEY,
        'SCADA':     P_SCADA,
        'Receiver':  P_R,
    }
    p_comp_no_bc = p_compromise(no_bc)
    p_sec_no_bc = 0.0 # system is compromised instantly by Sybil/Byz
    
    lines = []
    lines.append(r"\begin{table*}[t]")
    lines.append(r"\caption{Consensus-Dependent Joint Security: Protocol-Differentiating Joint Attack Probabilities and Overall Security ($x{=}0.95, m{=}10, p_c{=}0.05, y{=}0.05$)}")
    lines.append(r"\label{tab:consensus_security}")
    lines.append(r"\centering")
    lines.append(r"\scriptsize")
    lines.append(r"\setlength{\tabcolsep}{2.5pt}")
    lines.append(r"\begin{tabular}{@{}l|cccccccccccc|cc@{}}")
    lines.append(r"\toprule")
    lines.append(
        r"\textbf{Protocol} & "
        r"\textbf{$P_{\mathrm{Sensor}}$} & \textbf{$P_{\mathrm{FDI}}$} & \textbf{$P_{\mathrm{Comm}}$} & "
        r"\textbf{$P_{\mathrm{MitM}}$} & \textbf{$P_{\mathrm{Replay}}$} & \textbf{$P_{\mathrm{Sybil}}$} & "
        r"\textbf{$P_{\mathrm{DoS}}$} & \textbf{$P_{\mathrm{DDoS}}$} & \textbf{$P_{\mathrm{Byz}}$} & "
        r"\textbf{$P_{\mathrm{Key}}$} & \textbf{$P_{\mathrm{SCADA}}$} & \textbf{$P_{\mathrm{Receiver}}$} & "
        r"\textbf{$P_{\mathrm{Comp.}}$} & \textbf{$P_{\mathrm{sec}}$} \\"
    )
    lines.append(r"\midrule")

    for proto in PROTOCOLS:
        attacks = compute_all_attacks(proto)
        p_comp = p_compromise(attacks)
        p_sec = 1.0 - p_comp
        
        name_tex = proto.name.replace("(m)", "($m$)")
        rec_cell = fmt_latex(attacks['Receiver'])
        if proto.has_vrf:
            rec_cell += r"$\textsuperscript{\textdagger}$"
            
        row = (
            f"{name_tex} & "
            f"{fmt_latex(attacks['Sensor'])} & "
            f"{fmt_latex(attacks['FDI'])} & "
            f"{fmt_latex(attacks['Comm'])} & "
            f"{fmt_latex(attacks['MitM'])} & "
            f"{fmt_latex(attacks['Replay'])} & "
            f"{fmt_latex(attacks['Sybil'])} & "
            f"{fmt_latex(attacks['DoS'])} & "
            f"{fmt_latex(attacks['DDoS'])} & "
            f"{fmt_latex(attacks['Byzantine'])} & "
            f"{fmt_latex(attacks['Key'])} & "
            f"{fmt_latex(attacks['SCADA'])} & "
            f"{rec_cell} & "
            f"\\textbf{{{fmt_latex(p_comp)}}} & "
            f"\\textbf{{{fmt_latex(p_sec)}}} \\\\"
        )
        lines.append(row)

    lines.append(r"\midrule")
    lines.append(
        r"W/O Blockchain & "
        f"{fmt_latex(no_bc['Sensor'])} & "
        f"{fmt_latex(no_bc['FDI'])} & "
        f"{fmt_latex(no_bc['Comm'])} & "
        f"{fmt_latex(no_bc['MitM'])} & "
        f"{fmt_latex(no_bc['Replay'])} & "
        f"{fmt_latex(no_bc['Sybil'])} & "
        f"{fmt_latex(no_bc['DoS'])} & "
        f"{fmt_latex(no_bc['DDoS'])} & "
        f"{fmt_latex(no_bc['Byzantine'])} & "
        f"{fmt_latex(no_bc['Key'])} & "
        f"{fmt_latex(no_bc['SCADA'])} & "
        f"{fmt_latex(no_bc['Receiver'])} & "
        f"\\textbf{{{fmt_latex(p_comp_no_bc)}}} & "
        f"\\textbf{{$0.0$}} \\\\"
    )

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\vspace{2pt}")
    lines.append(
        r"\par\noindent\scriptsize\textit{Notes:} "
        r"All validator credit-evaluation weightings reduce effective validator compromise to $p_{c,eff} = 0.03$ (for CE-PBFT, SV-PBFT, and RVR) vs. $p_{c,eff} = 0.05$ baseline. "
        r"\textsuperscript{\textdagger}Proposed VRF-based receiver override reduction: $p_{r,eff\_recv} = P_R \cdot (1/n_{val})$~\cite{wang2025}. "
        r"All attack probabilities are joint and derived from consensus parameters (committee size $n_{val}$, voting phases, message complexity $M_c$, latency $L$, and credit weighting). "
        r"W/O Blockchain represents the centralized single-point vulnerability baseline."
    )
    lines.append(r"\end{table*}")

    return "\n".join(lines)


def main():
    latex = generate_latex_table()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    latex_path = os.path.join(script_dir, "table_consensus_security.tex")
    with open(latex_path, "w", encoding="utf-8") as f:
        f.write(latex)
    print(f"\nLaTeX table saved to: {latex_path}\n")

if __name__ == "__main__":
    main()
