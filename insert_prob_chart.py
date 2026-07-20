import sys

with open('intrusion_detection_bft_paper.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_table = r'''
\begin{table*}[t]
\caption{Probability Equation Summary: Formulas used to calculate the results in Table~\ref{tab:consensus_security}}
\label{tab:probability_equations_summary}
\centering
\scriptsize
\begin{tabular}{@{}llll@{}}
\toprule
\textbf{Attack Vector} & \textbf{Without Blockchain (Centralized)} & \textbf{With Blockchain (Consensus-Dependent)} & \textbf{Equation Source} \\
\midrule
Sensor ($P_{\mathrm{Sensor}}$) & $x^m$ & $x^{2m} \cdot (1 - \eta \frac{n_{val}}{n_{global}})$ & Section~\ref{sec:per_algo_compromise} (Eq.~18) \\
FDI ($P_{\mathrm{FDI}}$) & $x^m$ & $x^{2m} \cdot (1 - \beta N_{phases})$ & Section~\ref{sec:per_algo_compromise} (Eq.~19) \\
Comm. ($P_{\mathrm{Comm}}$) & $x^m$ & $x^{2k_1} \cdot \sigma_{CO}^{\text{Algo}}$ & Section~\ref{sec:per_algo_compromise} (Eq.~20) \\
MitM ($P_{\mathrm{MitM}}$) & $y$ & $y^2 / n_{val}$ & Section~\ref{sec:per_algo_compromise} (Eq.~22) \\
Replay ($P_{\mathrm{Replay}}$) & $z$ & $0.0$ & Section~\ref{sec:twelve_attacks} (Eq.~13) \\
Sybil ($P_{\mathrm{Sybil}}$) & $1.0$ & $\sum_{i=f+1}^{n_{val}} \binom{n_{val}}{i} p_{c,eff}^i (1 - p_{c,eff})^{n_{val}-i}$ & Section~\ref{sec:per_algo_compromise} (Eq.~23) \\
DoS ($P_{\mathrm{DoS}}$) & $p_{dos}$ & $p_{dos} (\frac{f+1}{n_{val}}) \sigma_{CO}^{\text{Algo}} (1 - e^{-L / \tau_{dos}})$ & Section~\ref{sec:per_algo_compromise} (Eq.~21) \\
DDoS ($P_{\mathrm{DDoS}}$) & $p_{ddos}$ & $p_{ddos} (\frac{f+1}{n_{val}}) \sigma_{CO}^{\text{Algo}} (1 - e^{-L / \tau_{dos}})$ & Derived via Eq.~21 \\
Byzantine ($P_{\mathrm{Byz}}$) & $1.0$ & $\sum_{i=f+1}^{n_{val}} \binom{n_{val}}{i} p_{c,eff}^i (1 - p_{c,eff})^{n_{val}-i}$ & Section~\ref{sec:per_algo_compromise} (Eq.~23) \\
Key ($P_{\mathrm{Key}}$) & $p_{key}$ & $P_{R,shamir}(3, 5, p_{r,eff\_key})$ & Section~\ref{sec:per_algo_compromise} (Eq.~24) \\
SCADA ($P_{\mathrm{SCADA}}$) & $0.01$ & $(P_{SCADA} \cdot x)^m \cdot p_{c,eff} \cdot (1 - e^{-L / \tau_{scada}})$ & Section~\ref{sec:per_algo_compromise} (Eq.~25) \\
Receiver ($P_{\mathrm{Receiver}}$) & $0.01$ & $(p_{r,eff\_recv})^{k_2} \cdot x^m \cdot (1 - e^{-L / \tau_{recv}})$ & Section~\ref{sec:per_algo_compromise} (Eq.~26) \\
\midrule
\textbf{Overall Compromise} & $P_{\mathrm{Comp}}^{\mathrm{noBC}} = 1 - \prod_{j} (1 - P_{atk}^j)$ & $P_{\mathrm{Comp}}^{\mathrm{Algo}} = 1 - \prod_{j} (1 - P_j^{\text{Algo}})$ & Section~\ref{sec:independence_limitations} \\
\bottomrule
\end{tabular}
\end{table*}

To explicitly cross-reference the probabilities presented in our results, Table~\ref{tab:probability_equations_summary} maps the evaluated probability scores from Table~\ref{tab:consensus_security} directly back to their governing mathematical equations and physical baseline models.
'''

insert_idx = -1
for i, line in enumerate(lines):
    if r'validating that consensus architecture directly governs distribution grid resilience.' in line:
        insert_idx = i + 1
        break

if insert_idx != -1:
    lines.insert(insert_idx, new_table)
    with open('intrusion_detection_bft_paper.tex', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('Inserted probability chart successfully!')
else:
    print('Could not find insertion point!')
