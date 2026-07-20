import os

def update_paper_texts():
    fig13_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.55cm, auto, >=latex]
    \node [draw, rectangle, fill=red!15, text width=8.0cm, text centered, rounded corners] (w1) {\textbf{1. Cyber-Physical Attack Vector Ingress} \\ FDI, MitM, Replay, DoS, Sybil, Byzantine Node Infiltration};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of w1] (w2) {\textbf{2. Proactive Cryptographic Hash Verification} \\ SHA-256 Payload Integrity Check \& Nonce Timestamping};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, text centered, rounded corners, below=0.3cm of w2] (w3) {\textbf{3. Distributed BFT Consensus Engine} \\ Multi-Validator Voting Quorums ($n=51, f=16$)};
    \node [draw, rectangle, fill=green!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of w3] (w4) {\textbf{4. Multi-Signature Quorum Validation} \\ Threshold Signature Verification \& Shamir Secret Recovery};
    \node [draw, rectangle, fill=green!25, text width=8.0cm, text centered, rounded corners, below=0.3cm of w4] (w5) {\textbf{5. Residual Vulnerability Window Reduction} \\ Sub-Second Exposure Window ($W(\tau) < 0.024$)};
    \node [draw, rectangle, fill=green!40, text width=8.0cm, text centered, rounded corners, below=0.3cm of w5] (w6) {\textbf{6. Quantified Security Improvement (STSF Framework)} \\ 170 Orders Static Gain, $P_{\text{secure}} \ge 0.927$, $P_{\text{SPOF}} \to 10^{-10}$};

    \draw [->, thick] (w1) -- (w2);
    \draw [->, thick] (w2) -- (w3);
    \draw [->, thick] (w3) -- (w4);
    \draw [->, thick] (w4) -- (w5);
    \draw [->, thick] (w5) -- (w6);
\end{tikzpicture}%
}
\caption{\textbf{Figure 13 --- Comparative Application Security Workflow:} Causal validation pipeline showing how cryptographic checks, distributed consensus, and threshold quorums convert attack ingress into quantified security gains under STSF.}
\label{fig:fig13_comparative_workflow}
\end{figure}
"""

    for file_path in ["intrusion_detection_bft_paper.tex", "intrusion_detection_bft_paper_restructured.tex"]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update Fig 13 if present or replace placeholder
        if "\\label{fig:fig13_comparative_workflow}" in content:
            content = content.replace(
                content[content.find("\\begin{figure}[htbp]\n\\centering\n\\resizebox{\\columnwidth}{!}{\n\\begin{tikzpicture}[node distance=0.6cm, auto, >=latex]\n    \\node [draw, rectangle, fill=red!15"):content.find("\\label{fig:fig13_comparative_workflow}\n\\end{figure}") + len("\\label{fig:fig13_comparative_workflow}\n\\end{figure}")],
                fig13_tikz.strip()
            )
        else:
            content = content.replace(
                "\\subsection{Comparative Analysis: Without Blockchain vs With Blockchain}",
                fig13_tikz + "\n\\subsection{Comparative Analysis: Without Blockchain vs With Blockchain}"
            )

        # Standardize Generation terminology
        content = content.replace("Group 1", "Generation I").replace("Group 2", "Generation II").replace("Group 3", "Generation III").replace("Group 4", "Generation IV")
        content = content.replace("Group I", "Generation I").replace("Group II", "Generation II").replace("Group III", "Generation III").replace("Group IV", "Generation IV")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Updated TikZ and generation terminology in {file_path}")

if __name__ == "__main__":
    update_paper_texts()
