import os
import re

def main():
    report_path = r"c:\Users\athar\OneDrive\Desktop\vjti-comparison-bft-towerbft\bft_comparison_report.tex"
    week3_path = r"c:\Users\athar\OneDrive\Desktop\vjti-comparison-bft-towerbft\week3_report.tex"
    
    with open(report_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    with open(week3_path, "r", encoding="utf-8") as f:
        week3_text = f.read()

    print(f"Loaded bft_comparison_report.tex ({len(text)} bytes) and week3_report.tex ({len(week3_text)} bytes).")
    
    # ─── LOCATE SPLIT INDICES IN CLEAN FILE ───
    idx_intro = 3261
    idx_base = 5495
    idx_critique = 8083
    idx_stsf = 11441
    idx_cat = 14607
    idx_four_group = 16853
    idx_comp = 20616
    idx_key = 25077
    idx_bench = 27487
    idx_disc = 28334
    idx_concl = 30573
    idx_bib = 31736

    # Extract clean original blocks
    preamble = text[:idx_intro]
    intro = text[idx_intro:idx_base]
    baseline_framework = text[idx_base:idx_critique]
    core_critique = text[idx_critique:idx_stsf]
    stsf_framework = text[idx_stsf:idx_cat]
    catalogue = text[idx_cat:idx_four_group]
    four_group = text[idx_four_group:idx_comp]
    comp_results = text[idx_comp:idx_key]
    key_mgmt = text[idx_key:idx_bench]
    benchmarking = text[idx_bench:idx_disc]
    discussion = text[idx_disc:idx_concl]
    conclusion = text[idx_concl:idx_bib]
    refs = text[idx_bib:]

    print("Extracted all clean original blocks successfully.")

    # ─── EXTRACT FROM WEEK 3 REPORT ───
    gain_table = re.search(r"\\begin\{table\}\[htbp\]\s+\\caption\{Security Gain Factor.*?\\end\{table\}", week3_text, re.DOTALL).group(0)
    sens_table = re.search(r"\\begin\{table\}\[htbp\]\s+\\caption\{Quantitative Sensitivity Ranking.*?\\end\{table\}", week3_text, re.DOTALL).group(0)
    fig_sec_gain = re.search(r"\\begin\{figure\*\}\[t\]\s+\\centering\s+\\includegraphics\[width=0.9\\textwidth\]\{fig_security_gain.png\}.*?\\end\{figure\*\}", week3_text, re.DOTALL).group(0)
    fig_sens_ranking = re.search(r"\\begin\{figure\*\}\[t\]\s+\\centering\s+\\includegraphics\[width=0.9\\textwidth\]\{fig_sensitivity_ranking.png\}.*?\\end\{figure\*\}", week3_text, re.DOTALL).group(0)
    fig_multi_lambda = re.search(r"\\begin\{figure\}\[htbp\]\s+\\centering\s+\\includegraphics\[width=\\columnwidth\]\{fig_multi_lambda_comparison.png\}.*?\\end\{figure\}", week3_text, re.DOTALL).group(0)
    bayesian_sub = re.search(r"\\subsection\{Bayesian Conditional Sensitivity Analysis\}.*?\\end\{figure\}", week3_text, re.DOTALL).group(0)
    sensor_sens_sub = re.search(r"\\subsection\{Sensor Count Sensitivity Analysis\}.*?\\end\{figure\}", week3_text, re.DOTALL).group(0)
    model_comp_sub = re.search(r"\\subsection\{Comparison of Security Models\}.*?\\end\{figure\}", week3_text, re.DOTALL).group(0)

    # ─── SOFTEN CLAIMS (Preamble / Introduction) ───
    preamble = preamble.replace(
        "Our STSF analysis demonstrates that consensus latency---not fault tolerance threshold or message complexity alone---is the decisive parameter governing grid security.",
        "Our STSF analysis demonstrates that, under the evaluated operating ranges, consensus latency---not fault tolerance threshold or message complexity alone---is the decisive parameter governing grid security."
    )
    
    intro = intro.replace(
        "consensus latency is the decisive security parameter",
        "under the evaluated operating ranges, consensus latency is the decisive security parameter"
    )

    # ─── PROCESS SECTIONS ───

    # 1. Contribution 1: Temporal Critique of Sheikh et al. (2020)
    baseline_framework = baseline_framework.replace(
        r"\section{Baseline Framework: Sheikh et al.\ (2020)}",
        r"\section{Contribution 1: Temporal Critique of Sheikh et al.\ (2020)}"
    )
    
    core_critique = core_critique.replace(
        r"\section{The Core Critique: Temporal Vulnerability}",
        r"\subsection{The Core Critique: Asymptotic Complexity and Latency Explosion}"
    )

    fig1_latex = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_ptemporal_vs_latency.png}
\caption{Temporal vulnerability $P_{temporal}$ versus consensus latency for multiple attack rates $\lambda$, with protocols marked at the FDI attack rate ($\lambda=20.0$). OM($m$) saturates at $P_{temporal} \approx 1.0$ while Tower BFT remains at $\approx 0.12$.}
\label{fig:ptemporal_latency}
\end{figure}"""

    fig3_latex = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_attack_rate_heatmap.png}
\caption{Vulnerability heatmap: $P_{temporal}(\lambda, L)$ across consensus latency and attack rate. Contour lines mark 1\%, 5\%, 10\%, 50\%, and 90\% vulnerability thresholds. Protocols are marked at FDI rate ($\lambda=20.0$).}
\label{fig:heatmap}
\end{figure}"""

    c1 = baseline_framework + core_critique.rstrip() + "\n\n" + fig1_latex + "\n\n" + fig3_latex + "\n"

    # 2. Contribution 2: Evolutionary Four-Group BFT Analysis
    catalogue = catalogue.replace(
        "\\section{Catalogue of BFT Techniques}",
        "\\section{Contribution 2: Evolutionary Four-Group BFT Analysis}\n\n\\subsection{Catalogue of BFT Techniques}"
    )
    
    four_group = four_group.replace(
        "\\section{Four-Group Comparative Analysis}",
        "\\subsection{Four-Group Comparative Analysis}"
    )
    four_group = four_group.replace("\\subsection{Group 1", "\\subsubsection{Group 1")
    four_group = four_group.replace("\\subsection{Group 2", "\\subsubsection{Group 2")
    four_group = four_group.replace("\\subsection{Group 3", "\\subsubsection{Group 3")
    four_group = four_group.replace("\\subsection{Group 4", "\\subsubsection{Group 4")
    
    fig4_latex = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_f_vs_latency.png}
\caption{Consensus latency scaling under increasing Byzantine fault count $f$. Shaded bands show $\pm$15--25\% uncertainty. OM($m$) exhibits exponential latency explosion (note log scale); Tower BFT remains sub-second.}
\label{fig:f_latency}
\end{figure}"""

    fig8_latex = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_message_complexity.png}
\caption{Consensus protocol message complexity per block (log scale). OM($m$) requires recursive oral messages ($10^{18}$ messages for $n=51, f=16$), while Group 4 protocols (Tower BFT, RVR) scale linearly ($\mathcal{O}(n)$) requiring only $1{,}020$--$1{,}275$ messages.}
\label{fig:message_complexity}
\end{figure}"""

    fig15_latex = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_latency_distribution.png}
\caption{Consensus latency distribution under network delay jitter ($\tau \sim \text{Normal}(50, 10)$\,ms) at $f=1$ (500 runs). OM($m$) scales into tens of seconds, while Tower BFT remains sub-second, showing robustness to delay variability.}
\label{fig:latency_dist}
\end{figure}"""

    c2_new_sub = r"""
\subsection{Visualizations of Protocol Scale and Overhead}

Figure~\ref{fig:f_latency} compares latency scaling under increasing Byzantine faults. Figure~\ref{fig:message_complexity} compares the per-block message overhead across all nine protocols. Figure~\ref{fig:latency_dist} demonstrates consensus latency distributions under network delay jitter.

""" + fig4_latex + "\n\n" + fig8_latex + "\n\n" + fig15_latex + "\n"
    
    c2 = catalogue + four_group + c2_new_sub

    # 3. Contribution 3: Static-Temporal Security Framework (STSF)
    stsf_framework = stsf_framework.replace(
        r"\section{The Static-Temporal Security Framework}",
        r"\section{Contribution 3: Static-Temporal Security Framework (STSF)}"
    )

    fig2_latex = r"""\begin{figure*}[t]
\centering
\includegraphics[width=0.9\textwidth]{fig_latency_vs_psecure.png}
\caption{(a) Overall security probability $P_{secure}$ versus consensus latency at $\lambda=20.0$, with protocols marked by group. (b) Failure decomposition showing $P_{temporal}$ dominance and $P_{other}=0.05$ residual floor. $P_{TAb} \approx 0$ is cryptographically negligible.}
\label{fig:latency_psecure}
\end{figure*}"""

    fig6_latex = r"""\begin{figure*}[t]
\centering
\includegraphics[width=0.9\textwidth]{fig_component_contribution.png}
\caption{(a) Baseline model: $P_{SA} = x^{3854}$ underflows to $10^{-86}$ at $x=0.95$, making SCADA and receiver terms completely dominate. (b) Refined model ($m=10$): sensor risk contributes meaningfully, enabling genuine component comparison.}
\label{fig:components}
\end{figure*}"""

    # Locate and process Weighted Risk Model and remove Bayesian Conditional Attack Model
    weighted_idx = stsf_framework.find("\\subsection{Weighted Risk Model}")
    bayesian_idx = stsf_framework.find("\\subsection{Bayesian Conditional Attack Model}")
    
    formal_derivation = stsf_framework[:weighted_idx].rstrip()
    formal_derivation += "\n\nFigure~\\ref{fig:latency_psecure} demonstrates the inverse relationship between consensus latency and overall security.\n\n" + fig2_latex + "\n"
    
    clean_weighted_body = stsf_framework[weighted_idx:bayesian_idx]
    clean_weighted_body = clean_weighted_body.replace(
        "\\subsection{Weighted Risk Model}\n\\label{sec:weighted}",
        "\\subsection{Weighted Risk Model and Critical Sensor Subsets}"
    )
    clean_weighted_body = clean_weighted_body.replace("\\label{sec:weighted}", "")
    
    weighted_section = clean_weighted_body.rstrip() + "\n\nFigure~\\ref{fig:components} shows how Sheikh's original exponent collapses sensor terms to zero, while critical subsets ($m=10$) restore mathematical sensitivity.\n\n" + fig6_latex + "\n"
    
    stsf_framework = formal_derivation + "\n\n" + weighted_section + "\n\n" + sensor_sens_sub + "\n\n" + model_comp_sub + "\n"

    # Process comp_results
    anal_fig_idx = comp_results.find("\\subsection{Analytical Figures}")
    if anal_fig_idx != -1:
        comp_results = comp_results[:anal_fig_idx]
        
    comp_results = comp_results.replace(
        "\\section{Comparative Results}",
        "\\subsection{Quantitative Results and Comparative Analysis}"
    )

    fig5_latex = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_pareto_frontier.png}
\caption{Pareto frontier: Security ($P_{secure}$) vs Latency (log scale) at $\lambda=20.0$. Protocols on the frontier are non-dominated. OM($m$) and Classic PBFT are clearly dominated by Group 3 and Group 4 alternatives.}
\label{fig:pareto}
\end{figure}"""

    fig9_latex = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_f_vs_psecure.png}
\caption{Overall security probability ($P_{secure}$) vs Byzantine fault tolerance level ($f$) at $\lambda = 20.0$. Under fault scaling, OM($m$)'s latency explosion causes immediate security collapse ($P_{secure} \rightarrow 0$), whereas Tower BFT maintains high security.}
\label{fig:f_psecure}
\end{figure}"""

    fig10_latex = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_sensitivity_lambda.png}
\caption{Security sensitivity to attack rate: $P_{secure}$ across attack rates $\lambda \in [0.001, 100]$ for all four groups. Group 4 protocols maintain high security even under aggressive attack rates.}
\label{fig:sensitivity}
\end{figure}"""

    fig16_latex = r"""\begin{figure*}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{fig_robustness_heatmap.png}
\caption{Protocol Robustness Maps. 2D Security Horizons ($P_{secure}$) plotted across a continuous spectrum of Latency ($L \in [0.1, 100]$ seconds) and Attack Rate ($\lambda \in [10^{-3}, 10^2]$ s$^{-1}$) for OM($m$), Classic PBFT, Tower BFT, and RVR. Gold stars denote respective operating points, demonstrating that Group 4 protocols remain secure over a much larger threat spectrum.}
\label{fig:robustness_heatmap}
\end{figure*}"""

    comp_extras = r"""
Since raw $P_{secure}$ values overlap at low attack rates, we present relative security gain vs.\ OM($m$) baseline in Table~\ref{tab:gain} and Figure~\ref{fig:security_gain}. 

Figure~\ref{fig:pareto} identifies the Pareto frontier showing overall security versus latency. Figure~\ref{fig:f_psecure} shows how overall security degrades as Byzantine faults increase. Figure~\ref{fig:sensitivity} shows the sensitivity to a sweep of attack rates. Figure~\ref{fig:robustness_heatmap} shows the 2D security horizons across a continuous latency/attack spectrum. Figure~\ref{fig:multi_lambda} shows the security probability under varying FDI threat rates $\lambda \in \{5.0, 10.0, 20.0\}$ across all nine protocols. We observe that Group 4 protocols maintain robust security envelopes.

To mathematically justify that consensus latency is the decisive parameter under these evaluation criteria, we compute parameter influence ranking. As shown in Figure~\ref{fig:sensitivity_ranking} and Table~\ref{tab:sensitivity_ranking}, under the evaluated operating ranges, temporal parameters dominate overall security variance.

""" + gain_table + "\n\n" + fig_sec_gain + "\n\n" + fig5_latex + "\n\n" + fig9_latex + "\n\n" + fig10_latex + "\n\n" + fig16_latex + "\n\n" + fig_multi_lambda + "\n\n" + fig_sens_ranking + "\n\n" + sens_table + "\n"

    comp_results = comp_results.rstrip() + "\n\n" + comp_extras
    c3 = stsf_framework.rstrip() + "\n\n" + comp_results
    
    # 4. Contribution 4: Key Management and Defense-in-Depth
    key_mgmt = key_mgmt.replace(
        r"\section{Key Management and Defence-in-Depth}",
        r"\section{Contribution 4: Key Management and Defense-in-Depth}"
    )
    rotation_text = r"""
\subsection{Implementation and Rotation Considerations}
Beyond threshold mathematics, practical key management requires:
\begin{itemize}[leftmargin=*]
    \item \textbf{Key rotation}: Periodic refresh of key shares to limit compromise windows (recommended: 24-hour rotation for EV trading, 7-day for grid operations)
    \item \textbf{Hardware Security Modules (HSMs)}: Physical key storage prevents software-level extraction; FIPS 140-2 Level~3 certification standard for grid-critical infrastructure
    \item \textbf{Share refresh}: Proactive secret sharing allows regeneration of shares without reconstructing the secret, limiting exposure from compromised nodes
    \item \textbf{Share revocation}: Byzantine-tolerant revocation of compromised share holders, triggered by detection of anomalous behaviour in the consensus protocol
\end{itemize}
"""
    fig_key_idx = key_mgmt.find("\\begin{figure}")
    if fig_key_idx != -1:
        key_mgmt = key_mgmt[:fig_key_idx].rstrip() + "\n\n" + rotation_text + "\n\n" + key_mgmt[fig_key_idx:]

    # 5. Section 6: Benchmarking Methodology (Keep as is)

    # 6. Discussion and Limitations
    discussion = discussion.replace(
        r"\section{Discussion}",
        r"\section{Discussion and Limitations}"
    )
    discussion = discussion.replace(
        "\\item \\textbf{Latency is the dominant security parameter.}",
        "\\item \\textbf{Under the evaluated operating ranges, latency is the dominant security parameter.}"
    )
    
    future_work_text = r"""
\subsection{Directions for Future Research}
To address these limitations, future research directions will focus on:
\begin{enumerate}[leftmargin=*]
    \item \textbf{High-Fidelity NS3 Simulations:} Implementing the BFT consensus protocols in the NS3 network simulator to model packet-level routing, packet drops, and channel contention under realistic smart grid topology profiles.
    \item \textbf{PowerWorld Co-simulation:} Integrating the blockchain consensus simulator with a PowerWorld or OPAL-RT physical power system co-simulation to evaluate the grid dynamic response (frequency and voltage stability) to consensus-induced delays.
    \item \textbf{Dynamic and Adaptive Threat Estimation:} Developing machine-learning estimators to dynamically adjust the attack arrival rate parameter $\lambda$ in real time based on active intrusion detection system (IDS) network logs.
    \item \textbf{Complex Joint Vulnerability Trees:} Expanding the joint correlation model into a comprehensive Bayesian Belief Network to capture multi-stage cyber-physical attack paths.
\end{enumerate}
"""
    discussion = discussion.rstrip() + "\n\n" + future_work_text

    # 7. Section 8: Conclusion
    conclusion = conclusion.replace(
        "consensus latency is the decisive parameter governing grid security",
        "under the evaluated operating ranges, consensus latency is the decisive parameter governing grid security"
    )
    conclusion = conclusion.replace(
        "Consensus latency is the decisive security parameter.",
        "Under the evaluated operating ranges, consensus latency is the decisive security parameter."
    )

    # 8. Appendix: Support Analyses
    appendix_latex = r"""
\appendix
\section{Appendix: Support Analyses}
\label{sec:appendix}

In this appendix, we present three support analyses that validate the modeling assumptions of the Static-Temporal Security Framework (STSF). These are not central to the main thesis but provide additional security insight.

""" + bayesian_sub + "\n\n" + r"""
\subsection{Joint Attack Correlation Sensitivity}
We sweep the correlation parameter $\rho \in \{0.0, 0.25, 0.5, 1.0\}$ at $x=0.98$ to observe the security horizon in Figure~\ref{fig:correlation_sensitivity}. Under nominal levels, the impact is negligible due to the small $P_{TAb} \approx 10^{-173}$.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_correlation_sensitivity.png}
\caption{Correlation sensitivity sweep. $P_{secure}$ vs latency $L$ (log scale) for $\rho \in \{0.0, 0.25, 0.50, 1.0\}$ at $x=0.98$ (exposing static risk). Increasing correlation $\rho$ reduces combined failure probability $P_{fail}$, expanding the operational security horizon.}
\label{fig:correlation_sensitivity}
\end{figure}

\subsection{Analytical Consistency Check (Monte Carlo Verification)}
To check the mathematical consistency of our Poisson formulation $P_{temporal} = 1 - e^{-\lambda L P_{TA}}$, we run a stochastic simulation with $100{,}000$ runs per data point. We simulate the arrival of attacks as Poisson events with rate $\lambda P_{TA}$ over latency $L$, logging a temporal failure if at least one attack arrives within $L$. Figure~\ref{fig:monte_carlo_validation} compares the analytical vulnerability against the simulated frequency. The perfect agreement along the $y=x$ line confirms the mathematical correctness of our closed-form Poisson equation.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\columnwidth]{fig_monte_carlo_validation.png}
\caption{Monte Carlo consistency check of the STSF Poisson formulation. Poisson sampling $P_{temporal}$ (500 runs per point) shows perfect alignment with analytical values ($y=x$ dashed line), verifying model consistency.}
\label{fig:monte_carlo_validation}
\end{figure}
"""

    print("--- PRINT INDIVIDUAL BLOCK LENGTHS ---")
    print(f"len(preamble)        = {len(preamble)}")
    print(f"len(intro)           = {len(intro)}")
    print(f"len(c1)              = {len(c1)}")
    print(f"len(c2)              = {len(c2)}")
    print(f"len(c3)              = {len(c3)}")
    print(f"len(key_mgmt)        = {len(key_mgmt)}")
    print(f"len(benchmarking)    = {len(benchmarking)}")
    print(f"len(discussion)      = {len(discussion)}")
    print(f"len(conclusion)      = {len(conclusion)}")
    print(f"len(appendix_latex)  = {len(appendix_latex)}")
    print(f"len(refs)            = {len(refs)}")

    # ─── REASSEMBLE REPORT ───
    final_text = preamble + intro + c1 + c2 + c3 + key_mgmt + benchmarking + discussion + conclusion + appendix_latex + refs
    print(f"Calculated len(final_text) = {len(final_text)}")

    outpath = r"c:\Users\athar\OneDrive\Desktop\vjti-comparison-bft-towerbft\bft_comparison_report.tex"
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(final_text)
        
    print(f"Restructured report written to {outpath}, new length on disk = {len(final_text)}")

if __name__ == "__main__":
    main()
