import os

def add_formula_table():
    file_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define Table IV: Summary of Analytical Formulas
    formula_table_code = r"""
\begin{table*}[htbp]
\caption{Summary of Analytical Formulas and Closed-Form Security Equations in the STSF Framework}
\label{tab:all_formulas}
\centering
\scriptsize
\begin{tabular}{@{}llll@{}}
\toprule
\textbf{Category / Component} & \textbf{Security Metric / Variable} & \textbf{Analytical Closed-Form Equation} & \textbf{Baseline Parameters / Values} \\
\midrule
\textbf{Physical & Sensor Layer} & Sensor / FDI Compromise ($P_{\text{SA}}, P_{\text{FDI}}$) & $P_{\text{SA}} = P_{\text{FDI}} = x^m$ & $m=10, x=0.95 \implies P=0.599$ \\
\textbf{Communication Layer} & Comm. Hijack ($P_{\text{CA}}$) & $P_{\text{CA}} = x^m$ & $x=0.95, m=10 \implies P=0.599$ \\
& Man-in-the-Middle ($P_{\text{MitM}}$) & $P_{\text{MitM}} = y$ & $y=0.05$ (Modbus/DNP3 baseline) \\
& Replay Attack ($P_{\text{Replay}}$) & $P_{\text{Replay}} = z$ (Without Nonce) $\to 10^{-10}$ (With PoH) & $z=0.15$ \\
& Port DoS / Botnet DDoS & $P_{\text{DoS}} = p_{dos}, P_{\text{DDoS}} = p_{ddos}$ & $p_{dos}=0.20, p_{ddos}=0.35$ \\
\textbf{Consensus & Identity} & Sybil Identity Spoofing & $P_{\text{Sybil}} = 1.0$ (Unpermissioned) $\to 10^{-10}$ (BFT Admission) & $P_{\text{Sybil}}=1.0 \to 10^{-10}$ \\
& Byzantine Quorum Failure & $P_{\text{Byz, b}} = \sum_{k=f+1}^{n} \binom{n}{k} p_c^k (1-p_c)^{n-k}$ & $n=51, f=16, p_c=0.10 \implies 1.83 \times 10^{-10}$ \\
\textbf{Sheikh et al. Baseline} & Target Attack Model ($P_{\text{TA}}$) & $P_{\text{TA}} = \frac{1}{4}\left(2x^m + P_{\text{SCADA}} + P_R\right)$ & $P_{\text{TA}} \approx 0.0050$ (Centralized Baseline) \\
& Blockchain Protected ($P_{\text{TAb}}$) & $P_{\text{TAb}} = \frac{1}{4}\left(2P_{\text{SAb}} + P_{\text{SCADAb}} + P_{\text{Rb}}\right)$ & $P_{\text{TAb}} \approx 4.91 \times 10^{-173}$ (170 Orders Gain) \\
\textbf{Parallel Ingress Model} & System Compromise ($P_{\text{Compromise}}$) & $P_{\text{Compromise}} = 1 - \prod_{j=1}^{12} \left(1 - P_{\text{atk}}^j\right)$ & $P_{\text{Compromise}}^{\text{no\_BC}} = 0.9740 \to P_{\text{Compromise}}^{\text{BFT}} = 5.99 \times 10^{-7}$ \\
\textbf{Static-Temporal Model} & Realized Security ($P_{\text{secure}}$) & $P_{\text{secure}} = P_{\text{static}} \times e^{-\lambda W(\tau)}$ & $\lambda = 20\text{ s}^{-1}, W(\tau) < 0.024\text{ s}$ \\
& Poisson Vulnerability Window & $W(\tau) = L \cdot \left(1 - e^{-\lambda L}\right)$ & $L = 200\text{ ms (RVR)} \implies P_{\text{secure}} = 0.940$ \\
\textbf{Threshold Cryptography} & Shamir Key Recovery & $P_{\text{R,shamir}}(k,d) = \sum_{i=k}^{d} \binom{d}{i} P_{\text{share}}^i (1 - P_{\text{share}})^{d-i}$ & $(k=3, d=5), P_{\text{share}}=0.01 \implies 9.85 \times 10^{-6}$ \\
\textbf{Network Overhead} & Communication Overhead ($CO$) & $CO = \frac{M_{\text{total}}}{N_{\text{tx}}} \quad \text{[msgs/tx]}$ & $M_{\text{total}} = 3n^2+n \implies CO = 154\text{ msgs/tx}$ \\
\bottomrule
\end{tabular}
\end{table*}
"""

    # Insert Table IV in Section II (Without Blockchain Baseline)
    sec2_pos = content.find("\\section{Without Blockchain Baseline Security Evaluation (Centralized Architecture)}")
    if sec2_pos != -1:
        insert_pos = content.find("\n", sec2_pos) + 1
        content = content[:insert_pos] + "\n" + formula_table_code + "\n\n" + content[insert_pos:]

    # Add text references to \ref{tab:all_formulas} in Section I and Section II
    content = content.replace(
        "We complement this with a probabilistic evaluation across 12 distinct cyber-physical attack vectors",
        "We synthesize all underlying equations in Table~\\ref{tab:all_formulas} and complement this with a probabilistic evaluation across 12 distinct cyber-physical attack vectors"
    )

    content = content.replace(
        "To synthesize the security improvements, Table~\\ref{tab:comparison} contrasts the 12 attack vectors",
        "The complete closed-form equations for all security metrics are compiled in Table~\\ref{tab:all_formulas}. To synthesize the security improvements, Table~\\ref{tab:comparison} contrasts the 12 attack vectors"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Table IV (Summary of Analytical Formulas) and references added to both tex files!")

if __name__ == "__main__":
    add_formula_table()
