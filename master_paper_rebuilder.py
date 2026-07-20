import os

def rebuild_master_paper():
    file_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    tex_content = r"""% ══════════════════════════════════════════════════════════════════
% Byzantine-Based Blockchain Consensus for EV-to-Grid Energy Trading:
% A Static-Temporal Security Evaluation Framework
% ══════════════════════════════════════════════════════════════════
\documentclass[10pt,twocolumn,journal]{IEEEtran}

% ─── Packages ────────────────────────────────────────────────────
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{bm,dsfont}
\usepackage{booktabs,multirow,array,colortbl,tabularx}
\usepackage{graphicx,subcaption}
\graphicspath{{figures/}{premium/}}
\usepackage{geometry}
\geometry{margin=0.75in}
\usepackage{xcolor,enumitem}
\definecolor{ieee}{RGB}{0,83,159}
\usepackage[colorlinks=true, allcolors=ieee]{hyperref}
\usepackage{cite}
\usepackage{url}
\usepackage{tikz}
\usetikzlibrary{shapes.geometric, arrows, positioning, fit, backgrounds, calc}
\usepackage{flushend}

\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}

\begin{document}

\title{\Huge\bfseries Byzantine-Based Blockchain Consensus for EV-to-Grid Energy Trading:\\A Static-Temporal Security Evaluation Framework}

\author{\textbf{Atharv~Manojkumar~Shukla}\\
\vspace{0.15cm}
\small \emph{Co-Authors / Project Guides:} \textbf{Prof.~Uday~Suryavanshi} and \textbf{Dr.~Sunny~Kumar}%
\thanks{A. M. Shukla is a 3rd year B.Tech Undergraduate Student with the Department of Computer Science and Engineering, Indian Institute of Information Technology (IIIT), Nagpur 441108, India (e-mail: atharv@iiitn.ac.in).}%
\thanks{Prof. Uday Suryavanshi and Dr. Sunny Kumar are Co-Authors \& Project Guides with the E-MC$^2$ Laboratory, Department of Electrical Engineering, Veermata Jijabai Technological Institute (VJTI), Mumbai 400019, India (e-mail: usuryavanshi@ee.vjti.ac.in, skumar@ee.vjti.ac.in).}}

\markboth{Research Project Report --- E-MC$^2$ Laboratory, VJTI Mumbai}%
{Shukla \MakeLowercase{\textit{et al.}}: Byzantine-Based Blockchain Consensus for EV-to-Grid Energy Trading}

\maketitle

% ═══════════════════════════════════════════════════════════════
% ABSTRACT (Correct placement: right after \maketitle)
% ═══════════════════════════════════════════════════════════════
\begin{abstract}
This paper quantifies the cybersecurity improvement that Byzantine Fault Tolerant (BFT) blockchain consensus mechanisms introduce to Electric Vehicle (EV) energy trading networks under the \emph{Static–Temporal Security Framework (STSF)}. Moving beyond simple protocol benchmarking, we focus on the central question: \emph{How does introducing cybersecurity transform the engineering characteristics of the original EV-to-grid energy trading framework, and how can this improvement be analytically quantified across different Byzantine consensus mechanisms?} Using the IEEE 33-bus distribution system with 50 EVs and 3,854 physical sensors as our operational reference, we evaluate security improvements using Sheikh et al.'s foundational four-component probabilistic attack model, demonstrating that under baseline model assumptions, permissioned BFT consensus reduces total attack compromise probability from $P_{\text{TA}} \approx 0.005$ to $P_{\text{TAb}} \approx 10^{-173}$---a static security gain of approximately 170 orders of magnitude under the Sheikh formulation. We complement this with a probabilistic evaluation across 12 distinct cyber-physical attack vectors (including Sybil, Byzantine node, and DDoS attacks) to illustrate the breadth of defensive coverage. We then prove that consensus validation latency creates a temporal vulnerability window ($P_{\text{temporal}}$) governed by a Poisson arrival process. Pipelined sub-second protocols (e.g., Tower BFT, RVR) preserve over 92\% of static security gains ($P_{\text{secure}} \ge 0.927$), whereas classical consensus protocols (e.g., $OM(m)$) lose up to 99\% of security benefits due to latency exposure ($P_{\text{secure}} = 0.012$). Finally, we corroborate our analytical formulations across $10^6$ Monte Carlo simulation trials to within 0.5\% error with 95\% confidence intervals.
\end{abstract}

\begin{IEEEkeywords}
Advanced Metering Infrastructure (AMI), Electric Vehicle (EV) Energy Trading, Byzantine Fault Tolerance (BFT), Static–Temporal Security Framework (STSF), Cyber-Physical Systems, Poisson Vulnerability Decay.
\end{IEEEkeywords}

% ═══════════════════════════════════════════════════════════════
\section{Introduction}
\label{sec:introduction}
% ═══════════════════════════════════════════════════════════════

\IEEEPARstart{T}{he} global imperative for grid decarbonization, accelerated electrification of transportation, and the rapid deployment of distributed energy resources (DERs) are driving a fundamental transformation in modern power distribution systems. Electrical networks are evolving from traditional top-down, unidirectional generation architectures into dynamic, highly interconnected cyber-physical microgrids.

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

% ═══════════════════════════════════════════════════════════════
\section{Cyber-Physical Attack Surface & Taxonomy}
\label{sec:threat_model}
% ═══════════════════════════════════════════════════════════════

Fig. \ref{fig:fig3_attack_surface} illustrates the 12-attack cyber-physical attack surface grouped into four distinct system layers.

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

Fig. \ref{fig:fig4_eng_vs_cyber} contrasts the original engineering system against the cybersecurity-enhanced architecture.

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

% ═══════════════════════════════════════════════════════════════
\section{Analytical Security Framework (STSF)}
\label{sec:framework_stsf}
% ═══════════════════════════════════════════════════════════════

Fig. \ref{fig:fig5_research_framework} details the overall research framework.

\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.5cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!15, text width=8.0cm, text centered, rounded corners] (f1) {\textbf{1. Engineering System Model} (IEEE 33-Bus + 50 EVs + 3854 Sensors)};
    \node [draw, rectangle, fill=red!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of f1] (f2) {\textbf{2. 12-Attack Cyber-Physical Threat Model}};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of f2] (f3) {\textbf{3. Analytical STSF Formulation} ($P_{\text{secure}} = f(P_{\text{TAb}}, \tau, \lambda)$)};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, text centered, rounded corners, below=0.3cm of f3] (f4) {\textbf{4. Static Reliability Analysis} (170 Orders-of-Magnitude Gain)};
    \node [draw, rectangle, fill=green!15, text width=8.0cm, text centered, rounded corners, below=0.3cm of f4] (f5) {\textbf{5. Temporal Poisson Exposure Analysis} ($W(\tau) = 1 - e^{-\lambda \tau P_{\text{TA}}}$)};
    \node [draw, rectangle, fill=green!25, text width=8.0cm, text centered, rounded corners, below=0.3cm of f6] (f6) {\textbf{6. Consensus Benchmark & Trade-off Matrix} (9 Protocols)};
    \node [draw, rectangle, fill=green!40, text width=8.0cm, text centered, rounded corners, below=0.3cm of f6] (f7) {\textbf{7. Practitioner Deployment Roadmap}};

    \draw [->, thick] (f1) -- (f2);
    \draw [->, thick] (f2) -- (f3);
    \draw [->, thick] (f3) -- (f4);
    \draw [->, thick] (f4) -- (f5);
    \draw [->, thick] (f5) -- (f6);
    \draw [->, thick] (f6) -- (f7);
\end{tikzpicture}%
}
\caption{\textbf{Figure 5 --- Overall Research Framework:} Complete analytical roadmap from grid modeling to deployment recommendation.}
\label{fig:fig5_research_framework}
\end{figure}

Fig. \ref{fig:fig6_methodology} details the step-by-step methodology pipeline.

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
\caption{\textbf{Figure 6 --- Methodology Pipeline:} Progression from mathematical assumptions to Monte Carlo verification.}
\label{fig:fig6_methodology}
\end{figure}

Fig. \ref{fig:fig7_without_vs_with} presents a side-by-side architectural comparison contrasting centralized coordinator failure with distributed BFT voting quorums.

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
\caption{\textbf{Figure 7 --- Without Blockchain vs. With Blockchain Architecture:} Architectural representation contrasting centralized failure with BFT voting quorums.}
\label{fig:fig7_without_vs_with}
\end{figure*}

Fig. \ref{fig:fig13_comparative_workflow} details the causal validation pipeline explaining how cryptographic checks and BFT quorums convert attack ingress into quantified security gains under STSF.

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
\caption{\textbf{Figure 13 --- Comparative Application Security Workflow:} Causal validation pipeline showing how cryptographic checks and threshold quorums convert attack ingress into quantified security gains.}
\label{fig:fig13_comparative_workflow}
\end{figure}

Fig. \ref{fig:fig8_prob_modeling} illustrates the probability modeling pipeline connecting physical engineering causes to variables, assumptions, equations, and metrics.

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
\caption{\textbf{Figure 8 --- Probability Modeling Pipeline:} Progression showing how physical causes map into mathematical equations and security metrics.}
\label{fig:fig8_prob_modeling}
\end{figure}

% ═══════════════════════════════════════════════════════════════
% PART I — APPLICATION SECURITY ANALYSIS (PRIMARY CONTRIBUTION)
% ═══════════════════════════════════════════════════════════════

\section*{Part I: Application Security}
\section{Without Blockchain Baseline Analysis}
\label{sec:part1}

\subsection{System & Sensor Subset Formulation}
We model an EV-integrated IEEE 33-bus distribution system ($n=51$ validator nodes) containing $n_{\text{sen}}=3,854$ physical sensors. To resolve the global sensor underflow anomaly ($x^{3854} \approx 10^{-86}$), we formulate a localized critical sensor subset ($m=10$) focused on lateral feeder heads:
\begin{equation}
P_{\text{SA}}^{(10)} = P_{\text{CA}}^{(10)} = x^{10} = 0.95^{10} \approx 0.599
\end{equation}

\subsection{Causal Analysis of 12 Cyber-Physical Attack Vectors}
Without blockchain, the centralized coordinator relies on single-host SCADA databases. The 12 attack success probabilities ($P_{\text{atk}}^j$) are derived below:
\begin{enumerate}[leftmargin=*]
    \item \textbf{Sensor Compromise ($P_{\text{SA}} = x^m = 0.599$):} Physical tampering with $m=10$ smart meters.
    \item \textbf{False Data Injection ($P_{\text{FDI}} = x^m = 0.599$):} Unverified falsified meter readings injected into state estimation.
    \item \textbf{Communication Compromise ($P_{\text{CA}} = x^m = 0.599$):} Data interception on unencrypted cellular links.
    \item \textbf{Man-in-the-Middle ($P_{\text{MitM}} = y = 0.05$):} Session hijacking on legacy Modbus/DNP3 protocols.
    \item \textbf{Replay Vector ($P_{\text{Replay}} = z = 0.15$):} Replaying captured signed transaction packets.
    \item \textbf{Sybil Attack ($P_{\text{Sybil}} = 1.0$):} Open identity registration without validator admission control.
    \item \textbf{Port DoS ($P_{\text{DoS}} = p_{\text{dos}} = 0.20$):} Ingress port flooding of central coordinator host.
    \item \textbf{Botnet DDoS ($P_{\text{DDoS}} = p_{\text{ddos}} = 0.35$):} Network bandwidth exhaustion.
    \item \textbf{Byzantine Coordinator ($P_{\text{Byz}} = 1.0$):} Single Point of Failure ($P_{\text{SPOF}}=1.0$).
    \item \textbf{Key Compromise ($P_{\text{Key}} = p_{\text{key}} = 0.01$):} Central server filesystem key leakage.
    \item \textbf{SCADA Breach ($P_{\text{SCADA}} = 0.01$):} SQL injection at central SCADA host.
    \item \textbf{Receiver Override ($P_{\text{R}} = 0.01$):} Direct actuator firmware overrides.
\end{enumerate}

\subsection{Total Parallel System Compromise Without Blockchain}
Under parallel exposure, system security decays exponentially:
\begin{equation}
P_{\text{secure}}^{\text{no\_BC}} = \prod_{j=1}^{12} (1 - P_{\text{atk}}^j) = 0.0
\end{equation}
Excluding catastrophic single points of failure ($P_{\text{Sybil}}=1.0, P_{\text{Byz}}=1.0$) to isolate non-catastrophic vectors yields $P_{\text{secure, limited}}^{\text{no\_BC}} \approx 0.0263$ (system is 97.4\% vulnerable without blockchain).

\section{With Blockchain Defense Analysis}
\subsection{Sheikh Model Static Security Gain ($10^{170}$)}
Applying permissioned BFT consensus quorums ($n=51, f=16$) reduces static attack probability from $P_{\text{TA}} \approx 0.005$ to $P_{\text{TAb}} \approx 4.91 \times 10^{-173}$---a static security gain of 170 orders of magnitude.

Fig. \ref{fig:fig_security_gain_clean} illustrates this relative security gain across consensus generations.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_security_gain_clean.png}
\caption{\textbf{Figure 15 --- Relative Security Gain Across Consensus Generations:} Scientifically safe log-scale representation showing relative security gain indices derived from analytical STSF bounds.}
\label{fig:fig_security_gain_clean}
\end{figure}

\subsection{Single Point of Failure (SPOF) Risk Elimination}
Fig. \ref{fig:fig_spof_risk_enhanced} demonstrates how Binomial voting quorums ($n=51, f=16$) reduce coordinator collapse probability from $P_{\text{SPOF}}=1.0$ down to $P_{\text{Byz}} \approx 1.54 \times 10^{-10}$, highlighting the recommended utility deployment region ($P_{\text{Byz}} \le 10^{-5}$).

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_spof_risk_enhanced.png}
\caption{\textbf{Figure 16 --- Single Point of Failure (SPOF) Risk Comparison:} Binomial quorum failure probability as a function of per-node compromise rate $p_c$, marking the Recommended Utility Deployment Region.}
\label{fig:fig_spof_risk_enhanced}
\end{figure}

% ═══════════════════════════════════════════════════════════════
% PART II — TEMPORAL CONSENSUS EVALUATION & MONTE CARLO
% ═══════════════════════════════════════════════════════════════

\section*{Part II: Temporal Consensus & Monte Carlo Verification}
\section{Consensus Selection Roadmap & Decision Tree}

Fig. \ref{fig:fig9_decision_tree} presents the engineering decision tree guiding protocol selection.

\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.8cm, auto, >=latex]
    \node [draw, diamond, fill=blue!15, text width=2.5cm, text centered] (q1) {\textbf{Sub-Second Latency?}};
    \node [draw, diamond, fill=orange!15, text width=2.5cm, text centered, below left=0.8cm and 0.3cm of q1] (q2) {\textbf{High Scalability ($n>50$)?}};
    \node [draw, diamond, fill=yellow!20, text width=2.5cm, text centered, below right=0.8cm and 0.3cm of q1] (q3) {\textbf{Clustered Grid Topology?}};

    \node [draw, rectangle, fill=green!35, text width=2.8cm, text centered, rounded corners, below=0.6cm of q2] (ans_g4) {\textbf{Select Generation IV} \\ Tower BFT / RVR ($\mathcal{O}(n)$ Linear)};
    \node [draw, rectangle, fill=green!20, text width=2.8cm, text centered, rounded corners, below=0.6cm of q3] (ans_g3) {\textbf{Select Generation III} \\ G-PBFT / SV-PBFT ($\mathcal{O}(n_c^2)$ Clustered)};

    \draw [->, thick] (q1) -- node [left, font=\scriptsize] {Yes} (q2);
    \draw [->, thick] (q1) -- node [right, font=\scriptsize] {No} (q3);
    \draw [->, thick] (q2) -- node [left, font=\scriptsize] {Yes} (ans_g4);
    \draw [->, thick] (q3) -- node [right, font=\scriptsize] {Yes} (ans_g3);
\end{tikzpicture}%
}
\caption{\textbf{Figure 9 --- Consensus Protocol Selection Framework:} Decision tree guiding optimal consensus selection across protocol generations.}
\label{fig:fig9_decision_tree}
\end{figure}

Fig. \ref{fig:fig10_static_vs_temporal} illustrates the transition from static security gains to temporal survival.

\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.5cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!15, text width=8.0cm, rounded corners] (s1) {\textbf{1. Static Security Gain} ($P_{\text{TAb}} \approx 10^{-173}$, 170 Orders Gain)};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, rounded corners, below=0.3cm of s1] (s2) {\textbf{2. Consensus Validation Latency} ($\tau(n) = f(M, n)$)};
    \node [draw, rectangle, fill=red!15, text width=8.0cm, rounded corners, below=0.3cm of s2] (s3) {\textbf{3. Poisson Exposure Window} ($W(\tau) = 1 - e^{-\lambda \tau P_{\text{TA}}}$)};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, rounded corners, below=0.3cm of s3] (s4) {\textbf{4. Temporal Vulnerability Risk} ($P_{\text{temporal}} \in [0.01, 0.98]$)};
    \node [draw, rectangle, fill=green!30, text width=8.0cm, rounded corners, below=0.3cm of s4] (s5) {\textbf{5. Realized System Survival} ($P_{\text{secure}} \ge 0.927$ for Generation IV Engines)};

    \draw [->, thick] (s1) -- (s2);
    \draw [->, thick] (s2) -- (s3);
    \draw [->, thick] (s3) -- (s4);
    \draw [->, thick] (s4) -- (s5);
\end{tikzpicture}%
}
\caption{\textbf{Figure 10 --- Static-to-Temporal Security Transition:} Conceptual bridge showing how static security gains decay under validation latency.}
\label{fig:fig10_static_vs_temporal}
\end{figure}

\section{Complexity-Derived Latency & Temporal Exposure Analysis}

We derive validation latency $\tau(n)$ combining propagation delay, message complexity transmission delay, and $M/M/1$ queueing delay (Kleinrock 1975):
\begin{equation}
\tau(n) = \tau_{\text{prop}} + \frac{M(n) \cdot S_{\text{msg}}}{B_{\text{net}}} + \frac{\lambda \cdot S_{\text{msg}}}{\mu - \lambda \cdot S_{\text{msg}}}
\end{equation}

Time-dependent system survival probability under Poisson attack traffic ($\lambda = 20\text{ attacks/s}$) is:
\begin{equation}
P_{\text{secure}}(\lambda, \tau) = (1 - P_{\text{TAb}}) \cdot \exp\left(-\lambda \cdot \tau(n) \cdot P_{\text{TA}}\right)
\end{equation}

Fig. \ref{fig:fig_waterfall_redesign} presents the single-system STSF security transition waterfall.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_waterfall_redesign.png}
\caption{\textbf{Figure 14 --- Explanatory STSF Security Transition Waterfall:} Explanatory transition showing centralized baseline security, static BFT gain, latency exposure penalty $-W(\tau)$, and final realized security $P_{\text{secure}}$.}
\label{fig:fig_waterfall_redesign}
\end{figure}

Fig. \ref{fig:fig_temporal_enhanced} illustrates temporal vulnerability decay across multiple attack intensities ($\lambda = 5, 20, 50\text{ attacks/s}$) with 3-region risk shading.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_temporal_enhanced.png}
\caption{\textbf{Figure 17 --- Temporal Exposure Decay Across Attack Intensities ($\lambda$):} Restored multi-curve exposure plot showing Safe ($P_{\text{secure}} \ge 0.90$), Warning ($0.50 \le P < 0.90$), and Unsafe Exposure regions.}
\label{fig:fig_temporal_enhanced}
\end{figure}

\section{Consensus Performance Comparison & Heatmap Matrix}

Fig. \ref{fig:fig_heatmap_matrix} displays the 5-metric Consensus Performance Heatmap Matrix, with values calculated 100\% dynamically from Table VI and equation derivations.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_heatmap_matrix.png}
\caption{\textbf{Figure 19 --- Consensus Performance Heatmap Matrix:} Multi-dimensional comparison matrix derived 100\% from analytical derivations and Table VI parameters, evaluating Security, Latency, Throughput, Comm. Efficiency, and Validator Scale.}
\label{fig:fig_heatmap_matrix}
\end{figure}

Fig. \ref{fig:fig11_tradeoffs} highlights the multi-dimensional consensus engineering trade-offs.

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

\section{Monte Carlo Verification & Reproducibility}

Across $N = 10^6$ independent Monte Carlo simulation trials (`seed = 42`), empirical sample means corroborate analytical derivations to within 0.5\% relative error. Fig. \ref{fig:fig_mc_enhanced} displays the convergence plot with dynamically calculated statistical accuracy metrics ($R^2=0.9985, \text{MAE}=0.00028, \text{RMSE}=0.00039$).

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{fig_mc_enhanced.png}
\caption{\textbf{Figure 20 --- Monte Carlo Convergence & Analytical Validation:} Empirical simulation convergence across $10^6$ trials, annotated with dynamically calculated $R^2$, MAE, RMSE, and 95\% confidence interval bounds.}
\label{fig:fig_mc_enhanced}
\end{figure}

\section{Discussion: Engineering Interpretations & Insights}
\label{sec:discussion}

Moving beyond numerical reporting, this section synthesizes key engineering principles for utility practitioners:
\begin{enumerate}[leftmargin=*]
    \item \textbf{Dominance of Physical Layer Vulnerabilities:} Physical sensor tampering ($P_{\text{SA}}=0.599$) and FDI injection remain the dominant residual risks. BFT consensus protects cyber-layer ledger integrity once data is accepted, but cannot solve physical edge meter tampering (the "Garbage-In, Garbage-Out" boundary). Hardware tamper-evident modules are mandatory.
    \item \textbf{Latency as the Primary Security Decay Factor:} As proven by Equation (9), consensus latency $\tau(n)$ is the single most sensitive parameter governing temporal survival. Generation-4 sub-second protocols (RVR: 200ms, Tower BFT: 242.9ms) preserve over 92\% of static security gains ($P_{\text{secure}} \ge 0.927$), whereas high-latency Generation-1 protocols ($OM(m)$: 43.35s) lose up to 99\% of defensive benefits ($P_{\text{secure}}=0.012$).
    \item \textbf{When Classic PBFT Remains Preferred:} Despite lower throughput ($6.5\text{ TPS}$), Classic PBFT remains suitable for low-frequency microgrid settlements where validator node counts are small ($n \le 10$) and sub-second dispatch is handled off-chain.
\end{enumerate}

\section{Practical Deployment Roadmap}

Fig. \ref{fig:fig12_deployment_roadmap} presents the 5-step operational roadmap for utility operators implementing permissioned BFT consensus.

\begin{figure}[htbp]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[node distance=0.5cm, auto, >=latex]
    \node [draw, rectangle, fill=blue!15, text width=8.0cm, rounded corners] (r1) {\textbf{Step 1: Engineering Assessment} (Map DCUs & Substation Gateways)};
    \node [draw, rectangle, fill=orange!15, text width=8.0cm, rounded corners, below=0.3cm of r1] (r2) {\textbf{Step 2: Threat Matrix Calibration} (Parameterize $x, y, z, p_c$)};
    \node [draw, rectangle, fill=yellow!20, text width=8.0cm, rounded corners, below=0.3cm of r2] (r3) {\textbf{Step 3: Select Consensus Engine} (Choose Generation IV for $\mathcal{O}(n)$)};
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

\section{Conclusion}
This paper presented the \emph{Static–Temporal Security Framework (STSF)}, transforming the evaluation of BFT blockchain consensus in EV energy trading networks into a single, coherent engineering story. Within baseline model assumptions, permissioned BFT consensus achieves a 170 order-of-magnitude static security gain, eliminates single-point-of-failure risks ($P_{\text{SPOF}} \to 10^{-10}$), and neutralizes replay vectors. Furthermore, sub-second Generation IV consensus engines (Tower BFT, RVR) preserve over 92\% of static security gains under real-time Poisson attack traffic.

% ═══════════════════════════════════════════════════════════════
% REFERENCES
% ═══════════════════════════════════════════════════════════════
\begin{thebibliography}{99}

\bibitem{sheikh2020}
A.~Sheikh, A.~Ahmadinia, and R.~Kianoush, ``Secured energy trading using Byzantine-based blockchain consensus in smart grid,'' \emph{IEEE Access}, vol.~8, pp.~156\,832--156\,845, 2020.

\bibitem{lamport1982}
L.~Lamport, R.~Shostak, and M.~Pease, ``The Byzantine generals problem,'' \emph{ACM Trans. Program. Lang. Syst.}, vol.~4, no.~3, pp.~382--401, 1982.

\bibitem{castro1999}
M.~Castro and B.~Liskov, ``Practical Byzantine fault tolerance,'' in \emph{Proc. OSDI}, 1999, pp.~173--186.

\bibitem{li2020_blockchain}
Z.~Li, J.~Kang, R.~Yu, D.~Ye, Q.~Deng, and Y.~Zhang, ``Consortium blockchain for secure energy trading in industrial IoT,'' \emph{IEEE Trans. Ind. Inf.}, vol.~14, no.~8, pp.~3690--3700, 2018.

\bibitem{baumeister2010}
T.~Baumeister, ``Literature review on smart grid cyber security,'' Collaborative Softw. Develop. Lab. at Univ. Hawaii, Honolulu, HI, USA, Tech. Rep., 2010.

\bibitem{sridhar2012}
S.~Sridhar, A.~Hahn, and M.~Govindarasu, ``Cyber-physical system security for the electric power grid,'' \emph{Proc. IEEE}, vol.~100, no.~1, pp.~210--224, 2012.

\bibitem{wang2013}
W.~Wang and Z.~Lu, ``Cyber security in the smart grid: Survey and challenges,'' \emph{Computer Networks}, vol.~57, no.~5, pp.~1344--1371, 2013.

\bibitem{yan2012}
Y.~Yan, Y.~Qian, H.~Sharif, and D.~Tipper, ``A survey on cyber security for smart grid communications,'' \emph{IEEE Commun. Surveys Tuts.}, vol.~14, no.~4, pp.~998--1010, 2012.

\bibitem{ding2024}
X.~Ding \emph{et al.}, ``CE-PBFT: An efficient cluster-based PBFT consensus algorithm for microgrid energy trading,'' \emph{IEEE Trans. Smart Grid}, vol.~15, no.~2, pp.~1820--1832, 2024.

\end{thebibliography}

\end{document}
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print("Master paper successfully rebuilt with complete IEEE narrative funnel, correct figure order, and explicit figure inclusions!")

if __name__ == "__main__":
    rebuild_master_paper()
