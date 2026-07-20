import os

def merge_narrative_into_full_paper():
    file_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Expanded IEEE Introduction & Section I-C to I-G
    expanded_intro = r"""\IEEEPARstart{T}{he} global imperative for grid decarbonization, accelerated electrification of transportation, and the rapid deployment of distributed energy resources (DERs) are driving a fundamental transformation in modern power distribution systems. Electrical networks are evolving from traditional top-down, unidirectional generation architectures into dynamic, highly interconnected cyber-physical microgrids.

\subsection{Evolution of EV-to-Grid Energy Trading}
In modern smart distribution grids, Electric Vehicles (EVs) no longer act as passive electrical loads. Operating as mobile energy storage systems (ESS) under Vehicle-to-Grid (V2G) paradigms, EVs provide critical grid ancillary services, including peak shaving, frequency regulation, and local voltage stabilization. Peer-to-Peer (P2P) energy trading allows EV prosumers to directly monetize excess battery capacity by trading energy credits with neighboring grid consumers, relieving thermal stress on substation transformers during peak demand hours. Fig. \ref{fig:fig1_evolution} illustrates the operational progression from traditional power networks to cyber-physical P2P markets.

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
\caption{\textbf{Figure 1 --- Evolution of EV-to-Grid Energy Trading:} Operational transition from traditional one-way power distribution to cyber-physical BFT-secured P2P energy trading.}
\label{fig:fig1_evolution}
\end{figure}

\subsection{Advanced Metering Infrastructure (AMI) Integration}
The digital backbone enabling P2P energy trading is Advanced Metering Infrastructure (AMI). AMI integrates smart meters, data concentrator units (DCUs), bidirectional cellular/mesh communication networks, and Meter Data Management Systems (MDMS). High-frequency meter telemetry feeds directly into SCADA state estimation algorithms to ensure feeder voltage limits remain within safe limits ($0.95 \le V \le 1.05\text{ p.u.}$).

\subsection{Engineering Foundations: Detailed Review of Sheikh et al.'s Framework}
To establish a concrete operational benchmark, this work builds upon the foundational engineering framework proposed by Sheikh et al.~\cite{sheikh2020}. Sheikh et al.\ formulated a P2P EV energy trading model mapped onto an IEEE 33-bus distribution system (33 buses, 32 lateral branches, peak demand of $3,715\text{ kW}$) populated by 50 EV prosumers. Their framework detailed the physical power flow equations, transaction bidding workflows, and hardware telemetry requirements across $3,854$ physical sensors. 

While Sheikh et al.\ introduced a basic 4-component probabilistic security model ($P_{\text{TA}}$) to evaluate target attack probabilities, their analysis treated system security primarily as a static property. The original engineering framework assumed trusted coordinator execution, leaving several critical cyber-physical questions unaddressed:
\begin{enumerate}[leftmargin=*]
    \item \emph{Coordinator Single Point of Failure (SPOF):} The central coordinator MDMS node represents a single point of failure ($P_{\text{SPOF}}=1.0$).
    \item \emph{Zero Byzantine Resilience:} Centralized SCADA databases cannot detect or reject corrupt dispatch commands if the coordinator node itself acts maliciously ($f=0$).
    \item \emph{Sensor Count Dominance Anomaly:} Evaluating global sensor counts ($n_{\text{sen}}=3,854$) under power models ($x^{3854}$) causes underflow errors ($\approx 10^{-86}$), masking local sensor vulnerabilities.
\end{enumerate}

\subsection{Cybersecurity Challenges & Research Gap}
Fig. \ref{fig:fig2_workflow_no_cyber} illustrates the operational data flow of the baseline centralized energy trading system without dedicated cybersecurity protection, highlighting these critical coordinator vulnerabilities.

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

The overarching research gap addressed in this paper is the lack of a unified framework that quantifies how introducing permissioned Byzantine Fault Tolerant (BFT) consensus transforms centralized engineering characteristics and how consensus validation latency creates dynamic vulnerability exposure windows.

\subsection{Research Questions (RQs)}
To bridge this research gap, we formulate three central research questions:
\begin{quote}
\textbf{RQ1:} \emph{How much does introducing BFT blockchain consensus improve the application-layer security of an EV energy trading network compared to its centralized baseline?} \\
\textbf{RQ2:} \emph{How does consensus validation latency ($\tau$) create temporal vulnerability exposure windows under continuous Poisson attack traffic?} \\
\textbf{RQ3:} \emph{Which consensus protocol generation optimizes the multi-dimensional trade-off between security gain, throughput, latency, and communication overhead?}
\end{quote}

\subsection{Key Scientific Contributions}
Relative to Sheikh et al.~\cite{sheikh2020}, the core contributions of this work are:
\begin{itemize}[leftmargin=*]
    \item \textbf{Localized Critical Sensor Subset Model ($m=10$):} Resolves global sensor underflow by isolating critical bus sensor subsets, restoring mathematical sensitivity.
    \item \textbf{Novel Static–Temporal Security Framework (STSF):} Couples static cryptosystem compromise bounds with dynamic consensus exposure latency ($P_{\text{secure}}$).
    \item \textbf{Comprehensive 12-Attack Vector Taxonomy:} Formulates explicit success models across 12 cyber-physical attack vectors under centralized vs. BFT architectures.
    \item \textbf{Consensus Selection Decision Roadmap:} Evaluates 9 BFT consensus algorithms across 4 generations, corroborating derivations across $10^6$ Monte Carlo simulation trials.
\end{itemize}

\subsection{Paper Roadmap}
Fig. \ref{fig:fig0_paper_roadmap} details the overarching structural organization of this paper.

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

    # Remove Fig 0 if it was placed before Abstract
    if "\\label{fig:fig0_paper_roadmap}" in content:
        fig0_start = content.find("\\begin{figure}[htbp]\n\\centering\n\\resizebox{\\columnwidth}{!}{\n\\begin{tikzpicture}[node distance=0.55cm, auto, >=latex]\n    \\node [draw, rectangle, fill=blue!15, text width=8.0cm, text centered, rounded corners] (r1) {\\textbf{1. EV-to-Grid Energy Trading Domain}")
        if fig0_start != -1 and fig0_start < content.find("\\begin{abstract}"):
            fig0_end = content.find("\\end{figure}", fig0_start) + len("\\end{figure}")
            content = content[:fig0_start] + content[fig0_end:]

    # Replace Section I Introduction block with expanded IEEE funnel
    intro_start = content.find("\\section{Introduction}")
    if intro_start != -1:
        # Find where Section II or Part I starts
        sec2_start = content.find("\\section{Cyber-Physical Attack Surface")
        if sec2_start == -1:
            sec2_start = content.find("\\section{Without Blockchain}")
        if sec2_start == -1:
            sec2_start = content.find("\\section*{Part I:")

        if sec2_start != -1:
            content = content[:intro_start] + "\\section{Introduction}\n\\label{sec:introduction}\n" + expanded_intro + "\n\n" + content[sec2_start:]

    # Update figure references to use the upgraded PNG filenames
    content = content.replace("fig_security_gain.png", "fig_security_gain_clean.png")
    content = content.replace("fig_spof_risk.png", "fig_spof_risk_enhanced.png")
    content = content.replace("fig_waterfall_redesign.png", "fig_waterfall_redesign.png")
    content = content.replace("comparison_radar.png", "fig_heatmap_matrix.png")
    content = content.replace("fig_monte_carlo_validation.png", "fig_mc_enhanced.png")

    # Standardize Generation terminology
    content = content.replace("Group 1", "Generation I").replace("Group 2", "Generation II").replace("Group 3", "Generation III").replace("Group 4", "Generation IV")
    content = content.replace("Group I", "Generation I").replace("Group II", "Generation II").replace("Group III", "Generation III").replace("Group IV", "Generation IV")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully merged IEEE Transactions narrative into the full paper! Total lines: {len(content.splitlines())}")

if __name__ == "__main__":
    merge_narrative_into_full_paper()
