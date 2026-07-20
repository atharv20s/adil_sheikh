import os

def update_paper_and_readme():
    paper_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"
    readme_path = "README.md"

    # 1. Update Paper (.tex files)
    with open(paper_path, "r", encoding="utf-8") as f:
        content = f.read()

    code_avail_sec = r"""
\section*{Data and Code Availability}
To facilitate open-science reproducibility and future research extensions in Byzantine-tolerant smart grid security, all analytical models, Python figure generation scripts, LaTeX manuscript source files, and simulation artifacts evaluated in this study are publicly available on GitHub at: \url{https://github.com/atharv20s/adil_sheikh}.
"""

    if "\\section*{Data and Code Availability}" not in content:
        pos = content.find("\\begin{thebibliography}")
        if pos != -1:
            content = content[:pos] + code_avail_sec + "\n\n" + content[pos:]

    with open(paper_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Added Data & Code Availability section to both tex files!")

    # 2. Update README.md
    readme_content = """# Byzantine-Based Blockchain Consensus for EV-to-Grid Energy Trading: A Static-Temporal Security Evaluation Framework (STSF)

[![IEEE Transactions Standards](https://img.shields.io/badge/IEEE-Transactions_Standard-00539F?style=for-the-badge&logo=ieee&logoColor=white)](https://github.com/atharv20s/adil_sheikh)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

## 📌 Executive Summary
This repository contains the complete analytical framework, Python figure generation scripts, Monte Carlo simulation code, and IEEE Transactions LaTeX source code for the research paper:

> **"Byzantine-Based Blockchain Consensus for EV-to-Grid Energy Trading: A Static-Temporal Security Evaluation Framework"**

### 👥 Authors & Institutional Affiliations
* **Atharv Manojkumar Shukla** — *3rd Year B.Tech Student*, Department of Computer Science and Engineering, Indian Institute of Information Technology (IIIT), Nagpur.
* **Prof. Uday Suryavanshi** — *Project Guide & Co-Author*, E-MC² Laboratory, Department of Electrical Engineering, Veermata Jijabai Technological Institute (VJTI), Mumbai.
* **Dr. Sunny Kumar** — *Project Guide & Co-Author*, E-MC² Laboratory, Department of Electrical Engineering, Veermata Jijabai Technological Institute (VJTI), Mumbai.

---

## 🎯 Key Scientific Contributions
1. **Without Blockchain Baseline Evaluation ($P_{\text{secure}}^{\text{no\_BC}} = 0.0$):**
   * Formulates an IEEE 33-bus distribution grid with 50 EVs ($n=51$) and 3,854 physical sensors.
   * Proves that under a series reliability model across 12 cyber-physical attack vectors, centralized systems suffer **97.4% structural compromise** ($P_{\text{secure, limited}}^{\text{no\_BC}} \approx 0.026$) due to single-points-of-failure ($P_{\text{SPOF}}=1.0$).

2. **Quantified Static Security Gain ($\approx 170$ Orders of Magnitude):**
   * Extends Sheikh et al.'s 4-component probabilistic model, demonstrating that BFT consensus reduces attack probability from $P_{\text{TA}} \approx 0.005$ to $P_{\text{TAb}} \approx 10^{-173}$.

3. **Poisson Latency Exposure Framework ($P_{\text{temporal}}$):**
   * Models the temporal decay of static security as a Poisson arrival process governed by validation latency $L$.
   * Pipelined sub-second protocols (e.g., **Tower BFT**, **RVR**) preserve over 92% of security benefits ($P_{\text{secure}} \ge 0.927$), whereas classical protocols (e.g., $OM(m)$) lose up to 99% ($P_{\text{secure}} = 0.012$).

---

## 📁 Repository Structure
```
.
├── intrusion_detection_bft_paper.tex         # Master IEEE Transactions LaTeX Manuscript (1,400+ lines)
├── intrusion_detection_bft_paper_restructured.tex # Synced Backup LaTeX Manuscript
├── build_block_by_block_diagrams.py          # Pure Python 300 DPI Block-by-Block Diagram Generator
├── generate_publication_quality_figures.py    # Python Matplotlib High-Res Plot Generator
├── figures/                                  # 300 DPI Publication PNG Figures & Vector Graphics
│   ├── fig_comparative_workflow.png
│   ├── fig_model_comparison.png
│   ├── fig_paper_roadmap.png
│   ├── fig_waterfall_redesign.png
│   ├── fig_heatmap_matrix.png
│   ├── fig_security_gain_clean.png
│   ├── fig_spof_risk_enhanced.png
│   ├── fig_temporal_enhanced.png
│   └── fig_mc_enhanced.png
└── README.md                                 # Project Documentation & Reproducibility Guide
```

---

## 🛠️ How to Reproduce Figures & Compile LaTeX
### 1. Generate All 300 DPI Figures
```bash
python build_block_by_block_diagrams.py
python generate_publication_quality_figures.py
```

### 2. Compile Master IEEE LaTeX Manuscript
Use `pdflatex` or `latexmk`:
```bash
pdflatex intrusion_detection_bft_paper.tex
bibtex intrusion_detection_bft_paper
pdflatex intrusion_detection_bft_paper.tex
pdflatex intrusion_detection_bft_paper.tex
```

---

## 📞 Contact & Collaboration
For research inquiries, dataset requests, or future collaborations:
* **GitHub Repository:** [https://github.com/atharv20s/adil_sheikh](https://github.com/atharv20s/adil_sheikh)
* **Lead Author Email:** atharv@iiitn.ac.in
* **WhatsApp Contact:** **+91 9324396434**

---
*Developed at E-MC² Laboratory, Department of Electrical Engineering, VJTI Mumbai & IIIT Nagpur.*
"""

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("Updated README.md with comprehensive documentation and WhatsApp contact info!")

if __name__ == "__main__":
    update_paper_and_readme()
