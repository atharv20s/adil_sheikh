import re
import shutil

def polish_paper():
    paper_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(paper_path, "r", encoding="utf-8") as f:
        content = f.read()

    # -------------------------------------------------------------
    # 1. Shorten overly verbose subsection titles (Point 8)
    # -------------------------------------------------------------
    content = content.replace(
        "\\subsection{Evolution of EV-to-Grid Energy Trading}",
        "\\subsection{V2G Energy Trading Paradigm}"
    )
    content = content.replace(
        "\\subsection{Advanced Metering Infrastructure (AMI) Integration}",
        "\\subsection{AMI Telemetry Infrastructure}"
    )
    content = content.replace(
        "\\subsection{Engineering Foundations: Detailed Review of Sheikh et al.'s Framework}",
        "\\subsection{Foundational EV Trading Benchmark}"
    )
    content = content.replace(
        "\\subsection{Cybersecurity Challenges \\& Research Gap}",
        "\\subsection{Cybersecurity Gaps in Centralized Control}"
    )
    content = content.replace(
        "\\subsection{Sensor Count Dominance Critique}",
        "\\subsection{Sensor Scaling Vulnerability Analysis}"
    )
    content = content.replace(
        "\\subsection{Justification and Causal Analysis of the 12 Cyber-Physical Attacks}",
        "\\subsection{Cyber-Physical Threat Taxonomy}"
    )
    content = content.replace(
        "\\subsection{Quantitative Security Comparison Using Sheikh's Four-Component Model}",
        "\\subsection{Static Security Evaluation}"
    )

    # -------------------------------------------------------------
    # 2. Reduce repetition of "170 orders of magnitude" (Point 7)
    # -------------------------------------------------------------
    # Replace repeated instances with varied scholarly phrases
    count = 0
    def replace_170(match):
        nonlocal count
        count += 1
        if count == 1:
            return match.group(0) # Keep first mention exact
        elif count == 2:
            return "a static security improvement of ~170 orders of magnitude under the baseline formulation"
        elif count == 3:
            return "substantial static vulnerability suppression under STSF assumptions"
        elif count == 4:
            return "orders-of-magnitude security gain under the analytical cryptosystem model"
        else:
            return "significant static security gain"

    content = re.sub(r'(170 orders of magnitude|170 orders-of-magnitude|approximately 170 orders of magnitude)', replace_170, content, flags=re.IGNORECASE)

    # -------------------------------------------------------------
    # 3. Soften self-promotional wording (Point 12)
    # -------------------------------------------------------------
    content = content.replace("novel Static--Temporal Security Framework", "Static--Temporal Security Framework")
    content = content.replace("novel framework", "framework")
    content = content.replace("revolutionary", "transformative")
    content = content.replace("groundbreaking", "analytical")

    # -------------------------------------------------------------
    # 4. Enhance Section Transitions (Point 13)
    # -------------------------------------------------------------
    sec2_bridge = r"""
\subsection{Transition to Decentralized Security Framework}
While the analytical formulations in this section establish the baseline vulnerability of centralized grid architectures ($P_{\text{secure}}^{\text{no\_BC}} \le 0.026$), the following section investigates how introducing permissioned Byzantine Fault Tolerant (BFT) consensus modifies these probabilistic boundaries and mitigates coordinator-centric single points of failure.
"""
    if "\\subsection{Transition to Decentralized Security Framework}" not in content:
        pos = content.find("\\section{With Blockchain Security Evaluation (Decentralized BFT Architecture)}")
        if pos != -1:
            content = content[:pos] + sec2_bridge + "\n\n" + content[pos:]

    sec3_bridge = r"""
\subsection{Transition to Static--Temporal Security Framework}
The preceding analysis confirms that BFT consensus provides substantial static security gains against physical and cyber-attacks. However, in operational smart grid environments, consensus validation is not instantaneous. Section~\ref{sec:stsf} introduces the Static--Temporal Security Framework (STSF) to model how validation latency creates dynamic vulnerability exposure windows under continuous Poisson attack traffic.
"""
    if "\\subsection{Transition to Static--Temporal Security Framework}" not in content:
        pos = content.find("\\section{Static--Temporal Security Framework}")
        if pos == -1:
            pos = content.find("\\section{Static-Temporal Security Framework}")
        if pos != -1:
            content = content[:pos] + sec3_bridge + "\n\n" + content[pos:]

    # -------------------------------------------------------------
    # 5. Strengthen Conclusion (Point 15)
    # -------------------------------------------------------------
    strong_conclusion = r"""
\subsection{Conclusion A: Architectural Insights and Security Gains}
This study has demonstrated that transitioning from centralized EV-to-grid energy trading architectures to permissioned BFT blockchain consensus resolves critical coordinator single-points-of-failure ($P_{\text{SPOF}}: 1.0 \to 10^{-10}$) and neutralizes unverified data injection. Under static model assumptions, consensus verification introduces substantial security gains, suppressing baseline compromise probabilities from $P_{\text{TA}} \approx 0.005$ to $P_{\text{TAb}} \approx 10^{-173}$.

\subsection{Conclusion B: Operational Principles for Future Smart Grids}
Our findings yield three fundamental principles for next-generation cyber-physical distribution grids:
\begin{enumerate}[leftmargin=*]
    \item \textbf{Latency Controls Realized Security:} Consensus speed is a security parameter. Pipelined sub-second consensus engines (e.g., Tower BFT, RVR) preserve over 92\% of static cryptosystem gains ($P_{\text{secure}} \ge 0.927$), whereas high-latency classical protocols lose up to 99\% under active attack traffic.
    \item \textbf{Hardware Key Protection is Critical:} Threshold signature schemes (Shamir, MPC) are essential to prevent validator key theft from undermining consensus integrity.
    \item \textbf{Future Research Horizons:} Future research should extend the STSF framework by modeling multi-stage correlated attack sequences using dynamic Copula processes and validating performance on hardware-in-the-loop (HIL) 5G smart grid testbeds.
\end{enumerate}
"""
    # Replace existing conclusion subsections with strengthened version
    conc_start = content.find("\\section{Conclusion}")
    if conc_start != -1:
        bib_start = content.find("\\section*{Data and Code Availability}")
        if bib_start == -1:
            bib_start = content.find("\\begin{thebibliography}")
        if bib_start != -1:
            content = content[:conc_start] + "\\section{Conclusion}\n\\label{sec:conclusion}\n" + strong_conclusion + "\n\n" + content[bib_start:]

    # Save output to both files
    with open(paper_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Master IEEE Transactions polish successfully applied!")

if __name__ == "__main__":
    polish_paper()
