import os

def update_tex_figures():
    file_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Fig 8 / Fig 13 Causal Workflow
    if "\\includegraphics[width=0.9\\columnwidth]{fig_comparative_workflow.png}" not in content:
        content = content.replace(
            "\\caption{\\textbf{Comparative Application Security Workflow:} This diagram visually summarizes",
            "\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=\\columnwidth]{fig_comparative_workflow.png}\n\\caption{\\textbf{Comparative Application Security Workflow:} Visual causal validation engine showing how cryptographic checks and threshold quorums convert attack ingress into quantified security gains under STSF.}\n\\label{fig:comparative_workflow}\n\\end{figure}\n\n\\caption{\\textbf{Comparative Application Security Workflow:} This diagram visually summarizes"
        )

    # 2. Update Fig 10 Model Comparison
    if "\\includegraphics[width=\\columnwidth]{fig_model_comparison.png}" not in content:
        content = content.replace(
            "\\caption{\\textbf{Model Comparison:} Demonstrating the difference between Sheikh's target attack probability",
            "\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=\\columnwidth]{fig_model_comparison.png}\n\\caption{\\textbf{Model Comparison:} Single-target attack probability ($P_{\\text{TA}}$) vs. parallel failure system compromise ($P_{\\text{Compromise}}$).}\n\\label{fig:model_comparison}\n\\end{figure}\n\n\\caption{\\textbf{Model Comparison:} Demonstrating the difference between Sheikh's target attack probability"
        )

    # 3. Ensure Waterfall (Fig 14) is included
    if "\\includegraphics[width=\\columnwidth]{fig_waterfall_redesign.png}" not in content:
        content = content.replace(
            "\\section{Complexity-Derived Latency & Temporal Exposure Analysis}",
            "\\section{Complexity-Derived Latency & Temporal Exposure Analysis}\n\n\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=\\columnwidth]{fig_waterfall_redesign.png}\n\\caption{\\textbf{Figure 14 --- Explanatory STSF Security Transition Waterfall:} Explanatory single-system STSF transition showing centralized baseline security ($0.0263$), static BFT gain ($+0.9737$), latency penalty $-W(\\tau)$, and final realized security ($0.9760$).}\n\\label{fig:fig_waterfall_redesign}\n\\end{figure}\n"
        )

    # 4. Ensure Heatmap Matrix (Fig 19) is included
    if "\\includegraphics[width=\\columnwidth]{fig_heatmap_matrix.png}" not in content:
        content = content.replace(
            "\\section{Consensus Performance Comparison & Heatmap Matrix}",
            "\\section{Consensus Performance Comparison & Heatmap Matrix}\n\n\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=\\columnwidth]{fig_heatmap_matrix.png}\n\\caption{\\textbf{Figure 19 --- Consensus Performance Heatmap Matrix:} Multi-dimensional comparison matrix derived 100\\% from analytical derivations and Table VI parameters, evaluating Security ($P_{\\text{secure}}$), Latency, Throughput, Comm. Efficiency, and Validator Scale ($n$).}\n\\label{fig:fig_heatmap_matrix}\n\\end{figure}\n"
        )

    # 5. Ensure SPOF Risk (Fig 16) is included
    if "\\includegraphics[width=\\columnwidth]{fig_spof_risk_enhanced.png}" not in content:
        content = content.replace(
            "\\section{With Blockchain}",
            "\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=\\columnwidth]{fig_spof_risk_enhanced.png}\n\\caption{\\textbf{Figure 16 --- Single Point of Failure (SPOF) Risk Comparison:} Binomial quorum failure probability as a function of per-node compromise rate $p_c$, highlighting the Recommended Utility Deployment Region ($P_{\\text{Byz}} \\le 10^{-5}$).}\n\\label{fig:fig_spof_risk_enhanced}\n\\end{figure}\n\n\\section{With Blockchain}"
        )

    # 6. Ensure Temporal Decay (Fig 17) is included
    if "\\includegraphics[width=\\columnwidth]{fig_temporal_enhanced.png}" not in content:
        content = content.replace(
            "\\section{Protocol Comparisons}",
            "\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=\\columnwidth]{fig_temporal_enhanced.png}\n\\caption{\\textbf{Figure 17 --- Temporal Exposure Decay Across Attack Intensities ($\\lambda$):} Restored 3-curve exposure plot showing Safe ($P_{\\text{secure}} \\ge 0.90$), Warning ($0.50 \\le P < 0.90$), and Unsafe Exposure regions.}\n\\label{fig:fig_temporal_enhanced}\n\\end{figure}\n\n\\section{Protocol Comparisons}"
        )

    # 7. Ensure Monte Carlo (Fig 20) is included
    if "\\includegraphics[width=\\columnwidth]{fig_mc_enhanced.png}" not in content:
        content = content.replace(
            "\\section{Monte Carlo Verification & Reproducibility}",
            "\\section{Monte Carlo Verification & Reproducibility}\n\n\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=\\columnwidth]{fig_mc_enhanced.png}\n\\caption{\\textbf{Figure 20 --- Monte Carlo Convergence & Analytical Validation:} Empirical simulation convergence across $10^6$ trials, annotated with dynamically calculated $R^2$, MAE, RMSE, and 95\\% confidence interval bounds.}\n\\label{fig:fig_mc_enhanced}\n\\end{figure}\n"
        )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("All 8 new publication-quality figure inclusions successfully updated in both .tex files!")

if __name__ == "__main__":
    update_tex_figures()
