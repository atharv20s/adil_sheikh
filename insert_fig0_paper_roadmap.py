import os

def add_paper_roadmap():
    fig0_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.55cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!15, text width=8.0cm, text centered, rounded corners] (r1) {\textbf{1. EV-to-Grid Energy Trading Domain} \\ Electric Vehicle Integration, AMI Telemetry \& Prosumer Market};
    \node [draw, rectangle, fill=red!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of r1] (r2) {\textbf{2. Original Engineering System Limitations} \\ Centralized Coordinator SPOF ($P_{\text{SPOF}}=1.0$), Zero Byzantine Fault Tolerance};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of r2] (r3) {\textbf{3. 12-Attack Cyber-Physical Threat Taxonomy} \\ Physical, Communication, Application \& Consensus Layer Attack Vectors};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, text centered, rounded corners, below=0.3cm of r3] (r4) {\textbf{4. Static-Temporal Security Framework (STSF)} \\ Analytical Formulation: Static Cryptosystem Gain ($10^{170}$) + Poisson Latency Exposure};
    \node [draw, rectangle, fill=green!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of r4] (r5) {\textbf{5. Consensus Mechanism Performance Comparison} \\ Evaluating 9 Protocols across Throughput, Latency, Overhead \& $P_{\text{secure}}$};
    \node [draw, rectangle, fill=green!35, text width=8.0cm, text centered, rounded corners, below=0.3cm of r5] (r6) {\textbf{6. Practitioner Deployment Roadmap & Engineering Insights} \\ Operational Selection Decision Tree \& 5-Step Smart Grid Implementation};

    \draw [->, thick] (r1) -- (r2);
    \draw [->, thick] (r2) -- (r3);
    \draw [->, thick] (r3) -- (r4);
    \draw [->, thick] (r4) -- (r5);
    \draw [->, thick] (r5) -- (r6);
\end{tikzpicture}%
}
\caption{\textbf{Figure 0 --- Paper Roadmap:} Methodological flow chart guiding reviewers through the paper's overarching engineering narrative and structural organization.}
\label{fig:fig0_paper_roadmap}
\end{figure}
"""

    for file_path in ["intrusion_detection_bft_paper.tex", "intrusion_detection_bft_paper_restructured.tex"]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "\\label{fig:fig0_paper_roadmap}" not in content:
            content = content.replace(
                "\\maketitle\n\n%",
                "\\maketitle\n\n" + fig0_tikz + "\n\n%"
            )
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Paper roadmap inserted into {file_path}")

if __name__ == "__main__":
    add_paper_roadmap()
