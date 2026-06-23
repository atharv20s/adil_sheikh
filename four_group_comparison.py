"""
BFT Consensus Four-Group Comparison
===================================
Evaluates nine consensus protocols across four evolutionary groups under
four distinct threat profiles using the Static-Temporal Security Framework (STSF).
"""

import os
import math
from typing import Dict, List, Tuple

# Import math model functions and constants
from probabilistic_model import (
    p_ta_no_blockchain, p_tab_blockchain, p_temporal_poisson, p_secure_correlated, throughput_tps, p_r_vrf
)

import json

# Load protocols dynamically from protocols.json
protocols_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "protocols.json")
with open(protocols_json_path, "r", encoding="utf-8") as f:
    PROTOCOLS_DATA = json.load(f)

PROTOCOLS = []
for name, data in PROTOCOLS_DATA.items():
    PROTOCOLS.append({
        "name": name,
        "group": data["group"],
        "latency_ms": data["latency_ms"],
        "msg_complexity": data["msg_complexity"],
        "msg_count": data["msg_count"],
        "tps": data["tps"]
    })

# Define the 4 threat profiles:
# (profile_name, lambda_val, description)
THREAT_PROFILES = [
    ("Key Theft", 0.001, "Physical/side-channel key exploitation"),
    ("MitM Hijack", 1.0, "Man-in-the-middle session compromise"),
    ("FDI Sensor", 20.0, "False Data Injection sensor spoofing"),
    ("Replay Flood", 50.0, "Aggressive packet replay flood")
]


def run_comparison():
    print("=" * 90)
    print("  BFT consensus comparison across 4 groups and 4 threat profiles")
    print("=" * 90)
    print("  Model parameters:")
    print("    Sensor vulnerability x = 0.95")
    print("    Critical sensor subset m = 10")
    print("    Residual risk P_other = 0.05")
    print("    Correlation coefficient rho = 0.3")
    print("-" * 90)

    # Dictionary to store all results
    # results[protocol_name][threat_profile] = (p_temporal, p_secure)
    comparison_results = {}

    for proto in PROTOCOLS:
        name = proto["name"]
        comparison_results[name] = {}
        latency = proto["latency_ms"]

        # Protocol-specific static adjustments: RVR uses VRF leader hiding natively
        if name == "RVR":
            p_r_eff = p_r_vrf(k_compromised=1)
            p_ta_proto = p_ta_no_blockchain(0.95, n_sen=10, p_r=p_r_eff)
            p_tab_proto = p_tab_blockchain(0.95, n_sen=10, p_r_override=p_r_eff)
        else:
            p_ta_proto = p_ta_no_blockchain(0.95, n_sen=10)
            p_tab_proto = p_tab_blockchain(0.95, n_sen=10)

        for profile_name, lam, desc in THREAT_PROFILES:
            pt = p_temporal_poisson(latency, lam, p_ta_proto)
            ps = p_secure_correlated(p_tab_proto, pt, rho=0.3, p_other=0.05)
            comparison_results[name][profile_name] = (pt, ps)

    # Print comparative ASCII table
    print(f"{'Protocol':<14} | {'Latency':<8} | {'Complexity':<10} | {'TPS':<6} | "
          f"{'P_sec (Key)':<11} | {'P_sec (MitM)':<12} | {'P_sec (FDI)':<11} | {'P_sec (Replay)':<13}")
    print("-" * 105)
    for proto in PROTOCOLS:
        name = proto["name"]
        lat_str = f"{proto['latency_ms']:.1f}ms"
        tps_str = f"{proto['tps']:.1f}"
        
        ps_key = comparison_results[name]["Key Theft"][1]
        ps_mitm = comparison_results[name]["MitM Hijack"][1]
        ps_fdi = comparison_results[name]["FDI Sensor"][1]
        ps_replay = comparison_results[name]["Replay Flood"][1]

        print(f"{name:<14} | {lat_str:<8} | {proto['msg_complexity']:<10} | {tps_str:<6} | "
              f"{ps_key:.5f}     | {ps_mitm:.5f}      | {ps_fdi:.5f}     | {ps_replay:.5f}")
    
    print("=" * 90)

    # Generate LaTeX comparison table
    latex_table = generate_latex_table(comparison_results)
    
    # Save LaTeX table code to a file
    latex_table_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recovered_comparison_table.tex")
    with open(latex_table_path, "w", encoding="utf-8") as f:
        f.write(latex_table)
    print(f"  [OK] LaTeX table written to: {latex_table_path}")


def generate_latex_table(results: dict) -> str:
    """Generates a structured LaTeX table for the report."""
    latex = []
    latex.append(r"\begin{table*}[t]")
    latex.append(r"\caption{Static-Temporal Security Framework (STSF) Comparison of Byzantine Consensus Protocols ($x=0.95, m=10, P_{other}=0.05, \rho=0.3$)}")
    latex.append(r"\label{tab:stsf_comparison}")
    latex.append(r"\centering")
    latex.append(r"\scriptsize")
    latex.append(r"\begin{tabular}{@{}llrrcccccc@{}}")
    latex.append(r"\toprule")
    latex.append(r"\multirow{2}{*}{\textbf{Group}} & \multirow{2}{*}{\textbf{Protocol}} & \multirow{2}{*}{\textbf{Latency}} & \multirow{2}{*}{\textbf{Throughput}} & \textbf{Message} & \multicolumn{4}{c}{\textbf{Security Probability $P_{secure}$ by Threat Profile}} \\")
    latex.append(r"\cmidrule(lr){6-9}")
    latex.append(r" & & \textbf{(ms)} & \textbf{(TPS)} & \textbf{Complexity} & \textbf{Key Theft} & \textbf{MitM Hijack} & \textbf{FDI Sensor} & \textbf{Replay Flood} \\")
    latex.append(r" & & & & & ($\lambda=0.001$) & ($\lambda=1.0$) & ($\lambda=20.0$) & ($\lambda=50.0$) \\")
    latex.append(r"\midrule")

    current_group = ""
    for proto in PROTOCOLS:
        name = proto["name"]
        group = proto["group"]
        group_short = group.split(":")[0] # e.g. G1
        
        # Add visual separator for new groups
        if current_group != group:
            if current_group != "":
                latex.append(r"\cmidrule(lr){1-9}")
            current_group = group
            group_label = f"\\textbf{{{group_short}}}"
        else:
            group_label = ""

        lat_val = f"{proto['latency_ms']:.1f}"
        tps_val = f"{proto['tps']:.1f}"
        
        ps_key = results[name]["Key Theft"][1]
        ps_mitm = results[name]["MitM Hijack"][1]
        ps_fdi = results[name]["FDI Sensor"][1]
        ps_replay = results[name]["Replay Flood"][1]

        # Format results (round to 4 decimal places)
        ps_key_str = f"{ps_key:.4f}"
        ps_mitm_str = f"{ps_mitm:.4f}"
        ps_fdi_str = f"{ps_fdi:.4f}"
        ps_replay_str = f"{ps_replay:.4f}"

        # Bold highly secure ones
        if ps_key >= 0.94: ps_key_str = f"\\textbf{{{ps_key_str}}}"
        if ps_mitm >= 0.85: ps_mitm_str = f"\\textbf{{{ps_mitm_str}}}"
        if ps_fdi >= 0.20: ps_fdi_str = f"\\textbf{{{ps_fdi_str}}}"
        if ps_replay >= 0.001: ps_replay_str = f"\\textbf{{{ps_replay_str}}}"

        # LaTeX format complexity
        comp_esc = proto["msg_complexity"]

        latex.append(f"{group_label} & {name} & {lat_val} & {tps_val} & $\\mathcal{{O}}({comp_esc})$ & "
                     f"{ps_key_str} & {ps_mitm_str} & {ps_fdi_str} & {ps_replay_str} \\\\")

    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"\end{table*}")

    return "\n".join(latex)


if __name__ == "__main__":
    run_comparison()
