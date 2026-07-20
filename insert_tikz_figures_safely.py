import os

def insert_figures():
    file_path = "intrusion_detection_bft_paper.tex"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Preamble tikz package addition
    if "\\usepackage{tikz}" not in content:
        content = content.replace(
            "\\usepackage{url}",
            "\\package_placeholder"
        ).replace(
            "\\package_placeholder",
            "\\usepackage{url}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes.geometric, arrows, positioning, fit, backgrounds, calc}"
        )

    # TikZ Definitions
    fig1_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.7cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!10, text width=6.5cm, text centered, rounded corners] (g1) {\textbf{1. Traditional Grid} \\ One-way Power Flow, Centralized Generation};
    \node [draw, rectangle, fill=blue!20, text width=6.5cm, text centered, rounded corners, below=0.3cm of g1] (g2) {\textbf{2. Smart Grid} \\ Bidirectional Telemetry, Automated Meter Reading};
    \node [draw, rectangle, fill=blue!30, text width=6.5cm, text centered, rounded corners, below=0.3cm of g2] (g3) {\textbf{3. Advanced Metering Infrastructure (AMI)} \\ Real-time Demand Response, High-Frequency Telemetry};
    \node [draw, rectangle, fill=orange!20, text width=6.5cm, text centered, rounded corners, below=0.3cm of g3] (g4) {\textbf{4. EV Integration (V2G)} \\ Mobile Energy Storage, Distributed Prosumer Trading};
    \node [draw, rectangle, fill=green!20, text width=6.5cm, text centered, rounded corners, below=0.3cm of g4] (g5) {\textbf{5. P2P Energy Trading} \\ Direct EV-to-Grid Settlement, Dynamic Tariffs};
    \node [draw, rectangle, fill=green!35, text width=6.5cm, text centered, rounded corners, below=0.3cm of g5] (g6) {\textbf{6. Cyber-Physical Energy Trading (STSF)} \\ Proactive BFT Validation Layer, Fault-Tolerant Grid};

    \draw [->, thick] (g1) -- (g2);
    \draw [->, thick] (g2) -- (g3);
    \draw [->, thick] (g3) -- (g4);
    \draw [->, thick] (g4) -- (g5);
    \draw [->, thick] (g5) -- (g6);
\end{tikzpicture}%
}
\caption{\textbf{Figure 1 --- Evolution of EV-to-Grid Energy Trading:} Illustrating the operational transition from traditional one-way power distribution to cyber-physical BFT-secured P2P energy trading.}
\label{fig:fig1_evolution}
\end{figure}
"""

    fig2_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.6cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!15, text width=1.8cm, text centered, rounded corners] (ev) {\textbf{1. EV Prosumer}};
    \node [draw, rectangle, fill=blue!25, text width=1.8cm, text centered, rounded corners, right=0.4cm of ev] (sm) {\textbf{2. Smart Meter}};
    \node [draw, rectangle, fill=orange!20, text width=1.8cm, text centered, rounded corners, right=0.4cm of sm] (comm) {\textbf{3. Network Comm.}};
    \node [draw, rectangle, fill=red!20, text width=1.8cm, text centered, rounded corners, right=0.4cm of comm] (coord) {\textbf{4. Central Coordinator}};

    \node [draw, rectangle, fill=red!30, text width=4.0cm, text centered, rounded corners, below=0.5cm of coord] (scada) {\textbf{5. Central SCADA / MDMS}};
    \node [draw, rectangle, fill=green!20, text width=4.0cm, text centered, rounded corners, left=0.6cm of scada] (grid) {\textbf{6. Physical Grid Control}};

    \draw [->, thick] (ev) -- (sm);
    \draw [->, thick] (sm) -- (comm);
    \draw [->, thick] (comm) -- (coord);
    \draw [->, thick] (coord) -- (scada);
    \draw [->, thick] (scada) -- (grid);

    \node [draw, rectangle, dashed, red!80!black, fill=red!5, text width=8.0cm, text centered, below=0.4cm of scada] (vun) {\textbf{Critical Engineering Vulnerabilities (Without Cybersecurity):} \\ (1) Absolute SPOF ($P_{\text{SPOF}}=1.0$), (2) Zero Byzantine Tolerance ($f=0$), \\ (3) Unverified Data Injection, (4) Central Key File Leakage Risk};
\end{tikzpicture}%
}
\caption{\textbf{Figure 2 --- Engineering Workflow (Without Cybersecurity):} Operational data flow in centralized energy trading highlighting single points of failure and coordinator vulnerabilities.}
\label{fig:fig2_workflow_no_cyber}
\end{figure}
"""

    fig3_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.5cm, auto, >=latex]
    \node [draw, rectangle, fill=red!15, text width=8.2cm, rounded corners] (phys) {\textbf{1. Physical Layer Attacks} \\ $\bullet$ Sensor Compromise ($P_{\text{SA}}$) \quad $\bullet$ Receiver/Actuator Override ($P_{\text{R}}$)};
    \node [draw, rectangle, fill=orange!15, text width=8.2cm, rounded corners, below=0.3cm of phys] (comm) {\textbf{2. Communication Layer Attacks} \\ $\bullet$ Comm. Hijack ($P_{\text{CA}}$) \quad $\bullet$ Man-in-the-Middle ($P_{\text{MitM}}$) \quad $\bullet$ Replay Vector ($P_{\text{Replay}}$) \\ $\bullet$ Port DoS ($P_{\text{DoS}}$) \quad $\bullet$ Botnet DDoS ($P_{\text{DDoS}}$)};
    \node [draw, rectangle, fill=yellow!20, text width=8.2cm, rounded corners, below=0.3cm of comm] (app) {\textbf{3. Application & Control Layer Attacks} \\ $\bullet$ SCADA Breach ($P_{\text{SCADA}}$) \quad $\bullet$ Private Key Compromise ($P_{\text{Key}}$) \quad $\bullet$ False Data Injection ($P_{\text{FDI}}$)};
    \node [draw, rectangle, fill=green!20, text width=8.2cm, rounded corners, below=0.3cm of app] (cons) {\textbf{4. Consensus & Identity Layer Attacks} \\ $\bullet$ Sybil Identity Spoofing ($P_{\text{Sybil}}$) \quad $\bullet$ Byzantine Node Collusion ($P_{\text{Byz}}$)};

    \draw [->, thick] (phys) -- (comm);
    \draw [->, thick] (comm) -- (app);
    \draw [->, thick] (app) -- (cons);
\end{tikzpicture}%
}
\caption{\textbf{Figure 3 --- Cyber Attack Surface Taxonomy:} Structuring 12 cyber-physical attack vectors across Physical, Communication, Application, and Consensus layers.}
\label{fig:fig3_attack_surface}
\end{figure}
"""

    fig4_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.6cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!10, text width=6.5cm, text centered, rounded corners] (e1) {\textbf{Original Engineering System} \\ Centralized Metering \& SCADA Dispatch};
    \node [draw, rectangle, fill=red!10, text width=6.5cm, text centered, rounded corners, below=0.3cm of e1] (e2) {\textbf{Engineering Limitations} \\ Single Point of Failure ($P_{\text{SPOF}}=1.0$), Zero Byzantine Tolerance};
    \node [draw, rectangle, fill=yellow!20, text width=6.5cm, text centered, rounded corners, below=0.3cm of e2] (e3) {\textbf{Cybersecurity Layer (STSF)} \\ Proactive Validation \& Threshold Cryptography};
    \node [draw, rectangle, fill=green!15, text width=6.5cm, text centered, rounded corners, below=0.3cm of e3] (e4) {\textbf{Blockchain Consensus Engine} \\ Distributed Validator Quorums ($n=51, f=16$)};
    \node [draw, rectangle, fill=green!30, text width=6.5cm, text centered, rounded corners, below=0.3cm of e4] (e5) {\textbf{Improved Trust & Grid Reliability} \\ 170 Orders-of-Magnitude Gain, $P_{\text{SPOF}} \to 10^{-10}$};

    \draw [->, thick] (e1) -- (e2);
    \draw [->, thick] (e2) -- (e3);
    \draw [->, thick] (e3) -- (e4);
    \draw [->, thick] (e4) -- (e5);
\end{tikzpicture}%
}
\caption{\textbf{Figure 4 --- Engineering vs. Cybersecurity:} Architectural transformation showing how integrating a BFT validation layer resolves centralized engineering limitations.}
\label{fig:fig4_eng_vs_cyber}
\end{figure}
"""

    fig5_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.5cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!15, text width=8.0cm, text centered, rounded corners] (f1) {\textbf{1. Engineering System Model} (IEEE 33-Bus + 50 EVs + 3854 Sensors)};
    \node [draw, rectangle, fill=red!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of f1] (f2) {\textbf{2. 12-Attack Cyber-Physical Threat Model}};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of f2] (f3) {\textbf{3. Analytical STSF Formulation} ($P_{\text{secure}} = f(P_{\text{TAb}}, \tau, \lambda)$)};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, text centered, rounded corners, below=0.3cm of f3] (f4) {\textbf{4. Static Reliability Analysis} (170 Orders-of-Magnitude Gain)};
    \node [draw, rectangle, fill=green!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of f4] (f5) {\textbf{5. Temporal Poisson Exposure Analysis} ($W(\tau) = 1 - e^{-\lambda \tau P_{\text{TA}}}$)};
    \node [draw, rectangle, fill=green!25, text width=8.0cm, text centered, rounded corners, below=0.3cm of f5] (f6) {\textbf{6. Consensus Benchmark & Trade-off Matrix} (9 Protocols)};
    \node [draw, rectangle, fill=green!40, text width=8.0cm, text centered, rounded corners, below=0.3cm of f6] (f7) {\textbf{7. Practitioner Deployment Roadmap}};

    \draw [->, thick] (f1) -- (f2);
    \draw [->, thick] (f2) -- (f3);
    \draw [->, thick] (f3) -- (f4);
    \draw [->, thick] (f4) -- (f5);
    \draw [->, thick] (f5) -- (f6);
    \draw [->, thick] (f6) -- (f7);
\end{tikzpicture}%
}
\caption{\textbf{Figure 5 --- Overall Research Framework:} Complete analytical roadmap from engineering grid modeling to practical deployment recommendation.}
\label{fig:fig5_research_framework}
\end{figure}
"""

    fig6_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.5cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!10, text width=8.0cm, rounded corners] (m1) {\textbf{1. Engineering & Threat Assumptions} ($x=0.95, m=10, p_c=0.05$)};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, rounded corners, below=0.3cm of m1] (m2) {\textbf{2. Closed-Form Probability Derivation} (Binomial Quorums \& $M/M/1$)};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, rounded corners, below=0.3cm of m2] (m3) {\textbf{3. Parameter Sensitivity Sweeps} ($x \in [0.90, 0.999], \lambda \in [1, 100]$)};
    \node [draw, rectangle, fill=green!20, text width=8.0cm, rounded corners, below=0.3cm of m3] (m4) {\textbf{4. Statistically Rigorous Monte Carlo Verification} ($10^6$ Trials)};
    \node [draw, rectangle, fill=green!35, text width=8.0cm, rounded corners, below=0.3cm of m4] (m5) {\textbf{5. Scholarly Synthesis & Engineering Principles}};

    \draw [->, thick] (m1) -- (m2);
    \draw [->, thick] (m2) -- (m3);
    \draw [->, thick] (m3) -- (m4);
    \draw [->, thick] (m4) -- (m5);
\end{tikzpicture}%
}
\caption{\textbf{Figure 6 --- Methodology Pipeline:} Methodological progression from mathematical assumptions to Monte Carlo verification.}
\label{fig:fig6_methodology}
\end{figure}
"""

    fig7_tikz = r"""
\begin{figure*}[t]
\centering
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[node distance=0.8cm, auto, >=latex]
    % Panel A: Without Blockchain
    \node [draw, rectangle, fill=red!10, text width=7.5cm, minimum height=4.5cm, rounded corners] (panelA) {};
    \node [font=\bfseries, color=red!80!black, anchor=north west] at (panelA.north west) {\quad Panel A: Centralized Architecture (Without Blockchain)};
    \node [draw, rectangle, fill=red!25, text width=6.5cm, text centered, rounded corners, yshift=0.5cm] at (panelA.center) (c_coord) {\textbf{Central Coordinator / MDMS} \\ Single Point of Failure ($P_{\text{SPOF}}=1.0$) \\ Unverified Telemetry Ingestion};
    \node [draw, rectangle, fill=red!40, text width=6.5cm, text centered, rounded corners, below=0.5cm of c_coord] (c_fail) {\textbf{Attack Compromise Success} \\ $P_{\text{Compromise}} = 0.974$ \quad ($P_{\text{Sybil}}=1.0, P_{\text{Byz}}=1.0$)};
    \draw [->, ultra thick, red!80!black] (c_coord) -- (c_fail);

    % Panel B: With Blockchain
    \node [draw, rectangle, fill=green!10, text width=9.0cm, minimum height=4.5cm, rounded corners, right=1.0cm of panelA] (panelB) {};
    \node [font=\bfseries, color=green!60!black, anchor=north west] at (panelB.north west) {\quad Panel B: Distributed BFT Architecture (With Blockchain)};
    \node [draw, rectangle, fill=green!25, text width=8.0cm, text centered, rounded corners, yshift=0.5cm] at (panelB.center) (b_nodes) {\textbf{Distributed Validator Network ($n=51, f=16$)} \\ $2f+1$ Multi-Signature Voting Quorums \\ Threshold Secret Sharing \& PoH Timestamps};
    \node [draw, rectangle, fill=green!40, text width=8.0cm, text centered, rounded corners, below=0.5cm of b_nodes] (b_succ) {\textbf{Proactive Attack Rejection} \\ $P_{\text{TAb}} \approx 10^{-173}$ (170 Orders Gain), $P_{\text{SPOF}} \to 10^{-10}$};
    \draw [->, ultra thick, green!60!black] (b_nodes) -- (b_succ);
\end{tikzpicture}%
}
\caption{\textbf{Figure 7 --- Without Blockchain vs. With Blockchain Architecture:} Comparative architectural representation contrasting centralized coordinator failure with distributed BFT voting quorums.}
\label{fig:fig7_without_vs_with}
\end{figure*}
"""

    fig8_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.5cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!15, text width=8.0cm, rounded corners] (p1) {\textbf{1. Physical Engineering Cause} (Physical Meter Tampering / Network Sniffing)};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, rounded corners, below=0.3cm of p1] (p2) {\textbf{2. Model Variables} (Sensor Accuracy $x$, Local Subset $m$, Fault Bound $f$)};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, rounded corners, below=0.3cm of p2] (p3) {\textbf{3. Operational Assumptions} (Independent Compromise Rate $p_c=0.05$)};
    \node [draw, rectangle, fill=green!15, text width=8.0cm, rounded corners, below=0.3cm of p3] (p4) {\textbf{4. Closed-Form Derivation} ($P_{\text{Byz}} = \sum_{k=f+1}^n \binom{n}{k} p_c^k (1-p_c)^{n-k}$)};
    \node [draw, rectangle, fill=green!35, text width=8.0cm, rounded corners, below=0.3cm of p4] (p5) {\textbf{5. Security Metric Output} ($P_{\text{secure}}(\lambda, \tau) = (1-P_{\text{TAb}}) e^{-\lambda \tau P_{\text{TA}}}$)};

    \draw [->, thick] (p1) -- (p2);
    \draw [->, thick] (p2) -- (p3);
    \draw [->, thick] (p3) -- (p4);
    \draw [->, thick] (p4) -- (p5);
\end{tikzpicture}%
}
\caption{\textbf{Figure 8 --- Probability Modeling Pipeline:} Systematic progression showing how physical causes map into mathematical equations and security metrics.}
\label{fig:fig8_prob_modeling}
\end{figure}
"""

    fig9_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.8cm, auto, >=latex]
    \node [draw, diamond, fill=blue!15, text width=2.5cm, text centered] (q1) {\textbf{Sub-Second Latency?}};
    \node [draw, diamond, fill=orange!15, text width=2.5cm, text centered, below left=0.8cm and 0.3cm of q1] (q2) {\textbf{High Scalability ($n>50$)?}};
    \node [draw, diamond, fill=yellow!20, text width=2.5cm, text centered, below right=0.8cm and 0.3cm of q1] (q3) {\textbf{Clustered Grid Topology?}};

    \node [draw, rectangle, fill=green!35, text width=2.8cm, text centered, rounded corners, below=0.6cm of q2] (ans_g4) {\textbf{Select G4 Protocol} \\ Tower BFT / RVR ($\mathcal{O}(n)$ Linear)};
    \node [draw, rectangle, fill=green!20, text width=2.8cm, text centered, rounded corners, below=0.6cm of q3] (ans_g3) {\textbf{Select G3 Protocol} \\ G-PBFT / SV-PBFT ($\mathcal{O}(n_c^2)$ Clustered)};

    \draw [->, thick] (q1) -- node [left, font=\scriptsize] {Yes} (q2);
    \draw [->, thick] (q1) -- node [right, font=\scriptsize] {No} (q3);
    \draw [->, thick] (q2) -- node [left, font=\scriptsize] {Yes} (ans_g4);
    \draw [->, thick] (q3) -- node [right, font=\scriptsize] {Yes} (ans_g3);
\end{tikzpicture}%
}
\caption{\textbf{Figure 9 --- Consensus Protocol Selection Framework:} Engineering decision tree guiding optimal protocol selection for smart grid AMI deployments.}
\label{fig:fig9_decision_tree}
\end{figure}
"""

    fig10_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.5cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!15, text width=8.0cm, rounded corners] (s1) {\textbf{1. Static Security Gain} ($P_{\text{TAb}} \approx 10^{-173}$, 170 Orders Gain)};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, rounded corners, below=0.3cm of s1] (s2) {\textbf{2. Consensus Validation Latency} ($\tau(n) = f(M, n)$)};
    \node [draw, rectangle, fill=red!15, text width=8.0cm, rounded corners, below=0.3cm of s2] (s3) {\textbf{3. Poisson Exposure Window} ($W(\tau) = 1 - e^{-\lambda \tau P_{\text{TA}}}$)};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, rounded corners, below=0.3cm of s3] (s4) {\textbf{4. Temporal Vulnerability Risk} ($P_{\text{temporal}} \in [0.01, 0.98]$)};
    \node [draw, rectangle, fill=green!30, text width=8.0cm, rounded corners, below=0.3cm of s4] (s5) {\textbf{5. Realized System Survival} ($P_{\text{secure}} \ge 0.927$ for G4 Engines)};

    \draw [->, thick] (s1) -- (s2);
    \draw [->, thick] (s2) -- (s3);
    \draw [->, thick] (s3) -- (s4);
    \draw [->, thick] (s4) -- (s5);
\end{tikzpicture}%
}
\caption{\textbf{Figure 10 --- Static-to-Temporal Security Transition:} Conceptual bridge showing how static security gains decay under consensus validation latency.}
\label{fig:fig10_static_vs_temporal}
\end{figure}
"""

    fig11_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.6cm, auto, >=latex]
    \node [draw, circle, fill=blue!20, minimum size=1.8cm, text centered] (sec) {\textbf{Security}};
    \node [draw, circle, fill=green!20, minimum size=1.8cm, text centered, right=1.2cm of sec] (lat) {\textbf{Latency}};
    \node [draw, circle, fill=orange!20, minimum size=1.8cm, text centered, below=1.0cm of sec] (tps) {\textbf{Throughput}};
    \node [draw, circle, fill=yellow!25, minimum size=1.8cm, text centered, right=1.2cm of tps] (cost) {\textbf{Comm. Cost}};

    \draw [<->, ultra thick, ieee] (sec) -- (lat);
    \draw [<->, ultra thick, ieee] (sec) -- (tps);
    \draw [<->, ultra thick, ieee] (lat) -- (cost);
    \draw [<->, ultra thick, ieee] (tps) -- (cost);
    \draw [<->, ultra thick, ieee] (sec) -- (cost);
    \draw [<->, ultra thick, ieee] (lat) -- (tps);
\end{tikzpicture}%
}
\caption{\textbf{Figure 11 --- Consensus Engineering Trade-offs:} Multi-dimensional trade-off matrix illustrating interdependencies between security, latency, throughput, and communication cost.}
\label{fig:fig11_tradeoffs}
\end{figure}
"""

    fig12_tikz = r"""
\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.5cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!15, text width=8.0cm, rounded corners] (r1) {\textbf{Step 1: Engineering Assessment} (Map DCUs & Substation Gateways)};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, rounded corners, below=0.3cm of r1] (r2) {\textbf{Step 2: Threat Matrix Calibration} (Parameterize $x, y, z, p_c$)};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, rounded corners, below=0.3cm of r2] (r3) {\textbf{Step 3: Select Consensus Engine} (Choose Tower BFT / RVR for $\mathcal{O}(n)$)};
    \node [draw, rectangle, fill=green!20, text width=8.0cm, rounded corners, below=0.3cm of r3] (r4) {\textbf{Step 4: Configure Validator Quorums} (Set $n=51, f=16$, HSM Keys)};
    \node [draw, rectangle, fill=green!35, text width=8.0cm, rounded corners, below=0.3cm of r4] (r5) {\textbf{Step 5: Production Deployment & Monitoring} (HIL 5G Testbed Verification)};

    \draw [->, thick] (r1) -- (r2);
    \draw [->, thick] (r2) -- (r3);
    \draw [->, thick] (r3) -- (r4);
    \draw [->, thick] (r4) -- (r5);
\end{tikzpicture}%
}
\caption{\textbf{Figure 12 --- Practical Deployment Roadmap:} Step-by-step guidance for utility practitioners deploying permissioned BFT consensus.}
\label{fig:fig12_deployment_roadmap}
\end{figure}
"""

    # Safe Anchor Replacements (Inserting TikZ diagrams into exact spots in text)
    content = content.replace(
        "The modernization of electrical grids into cyber-physical smart distribution networks has enabled bidirectional energy and data flows.",
        "The modernization of electrical grids into cyber-physical smart distribution networks has enabled bidirectional energy and data flows. Fig. \\ref{fig:fig1_evolution} illustrates the evolutionary transition of EV energy trading architectures.\n" + fig1_tikz
    )

    content = content.replace(
        "\\subsection{System Model}",
        fig2_tikz + "\n\\subsection{System Model}"
    )

    content = content.replace(
        "\\subsection{Justification and Causal Analysis of the 12 Cyber-Physical Attacks}",
        fig3_tikz + "\n\\subsection{Justification and Causal Analysis of the 12 Cyber-Physical Attacks}"
    )

    content = content.replace(
        "\\subsection{Comparative Analysis: Without Blockchain vs With Blockchain}",
        fig4_tikz + "\n\\subsection{Comparative Analysis: Without Blockchain vs With Blockchain}"
    )

    content = content.replace(
        "\\end{itemize}\n\n% ═══════════════════════════════════════════════════════════════\n% PART I — APPLICATION SECURITY ANALYSIS",
        "\\end{itemize}\n\n" + fig5_tikz + "\n\n% ═══════════════════════════════════════════════════════════════\n% PART I — APPLICATION SECURITY ANALYSIS"
    )

    content = content.replace(
        "\\section{Probability Analysis: Expected Value vs. System Compromise}",
        fig6_tikz + "\n\\section{Probability Analysis: Expected Value vs. System Compromise}"
    )

    content = content.replace(
        "\\section{With Blockchain}",
        fig7_tikz + "\n\\section{With Blockchain}"
    )

    content = content.replace(
        "\\subsection{Blockchain Security Extensions \\& Application Causal Chain}",
        fig8_tikz + "\n\\subsection{Blockchain Security Extensions \\& Application Causal Chain}"
    )

    content = content.replace(
        "\\section*{Part II: Temporal Consensus & Monte Carlo Verification}",
        "\\section*{Part II: Temporal Consensus & Monte Carlo Verification}\n" + fig9_tikz
    )

    content = content.replace(
        "\\section{Complexity-Derived Latency & Poisson Attack Model}",
        fig10_tikz + "\n\\section{Complexity-Derived Latency & Poisson Attack Model}"
    )

    content = content.replace(
        "\\section{Monte Carlo Verification & Reproducibility}",
        fig11_tikz + "\n\\section{Monte Carlo Verification & Reproducibility}"
    )

    content = content.replace(
        "\\section{Conclusion}",
        fig12_tikz + "\n\\section{Conclusion}"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open("intrusion_detection_bft_paper_restructured.tex", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully inserted all 12 TikZ figures! New total lines: {len(content.splitlines())}")

if __name__ == "__main__":
    insert_figures()
