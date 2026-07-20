import re

def expand_paper():
    paper_path = "ids_to_bft_blockchain_ami_security.tex"
    thesis_path = "thesis/thesis_main.tex"
    
    with open(paper_path, "r", encoding="utf-8") as f:
        paper = f.read()
        
    with open(thesis_path, "r", encoding="utf-8") as f:
        thesis = f.read()
        
    # 1. Update Graphics Path
    paper = paper.replace(
        "\\graphicspath{{./images/}}",
        "\\graphicspath{{./premium/}{./figures/}{../figures/}}"
    )
    if "\\graphicspath" not in paper:
        paper = paper.replace(
            "\\begin{document}",
            "\\usepackage{graphicx}\n\\graphicspath{{./premium/}{./figures/}{../figures/}}\n\\begin{document}"
        )
        
    # 2. Extract 12-attack Threat Model from Thesis (Chapter 6)
    threat_model_match = re.search(r"\\chapter\{Threat Model\}.*?(?=\\chapter\{)", thesis, re.DOTALL)
    if threat_model_match:
        threat_model = threat_model_match.group(0)
        # Convert chapter to section
        threat_model = threat_model.replace("\\chapter{Threat Model}", "\\subsection{Expanded Threat Model: 12 Cyber-Physical Attack Vectors}")
        threat_model = threat_model.replace("\\section{", "\\subsubsection{")
        threat_model = threat_model.replace("\\subsection{", "\\paragraph{")
        
        # Replace existing list in paper
        paper_threat_match = re.search(r"\\subsection\{Threat Model: 12 Cyber-Physical Attack Vectors\}.*?(?=\\subsection\{Sensor Count Dominance Critique\})", paper, re.DOTALL)
        if paper_threat_match:
            paper = paper.replace(paper_threat_match.group(0), threat_model + "\n\n")

    # 3. Add Premium Figures
    # Replace architecture figure
    paper = paper.replace(
        "\\includegraphics[width=0.9\\columnwidth]{fig_architecture_comparison.png}",
        "\\includegraphics[width=\\columnwidth]{fig_1_architecture.pdf}"
    )
    
    # 4. Insert Consensus Taxonomy (G1-G4) before Discussion
    taxonomy_match = re.search(r"\\chapter\{Consensus Protocols for AMI\}.*?(?=\\chapter\{)", thesis, re.DOTALL)
    if taxonomy_match:
        taxonomy = taxonomy_match.group(0)
        taxonomy = taxonomy.replace("\\chapter{Consensus Protocols for AMI}", "\\section{Evolutionary Taxonomy of BFT Protocols (G1-G4)}")
        taxonomy = taxonomy.replace("\\section{", "\\subsection{")
        taxonomy = taxonomy.replace("\\subsection{", "\\subsubsection{")
        
        # Insert before Discussion
        paper = paper.replace("\\section{Discussion}", taxonomy + "\n\n\\section{Discussion}")

    # 5. Insert Temporal Model Derivation
    temporal_match = re.search(r"\\section\{Temporal Vulnerability Window\}.*?(?=\\section\{)", thesis, re.DOTALL)
    if temporal_match:
        temporal = temporal_match.group(0)
        temporal = temporal.replace("\\section{", "\\subsection{")
        temporal = temporal.replace("\\subsection{", "\\subsubsection{")
        
        paper_temporal_match = re.search(r"\\subsection\{Temporal Security Model\}.*?(?=\\subsection\{Algorithmic Evaluation Procedure\})", paper, re.DOTALL)
        if paper_temporal_match:
            paper = paper.replace(paper_temporal_match.group(0), "\\subsection{Temporal Security Model}\n" + temporal + "\n\n")

    # 6. Insert Radar Comparison Figure into Discussion
    radar_fig = """
\\begin{figure}[htbp]
\\centering
\\includegraphics[width=\\columnwidth]{fig_4_radar_comparison.pdf}
\\caption{Multi-dimensional radar evaluation of IDS vs. BFT approaches.}
\\label{fig:radar_comparison}
\\end{figure}
"""
    paper = paper.replace("\\subsection{Architectural Paradigm Shift (RQ1)}", radar_fig + "\n\\subsection{Architectural Paradigm Shift (RQ1)}")

    # 7. Insert Latency Figure into Results
    latency_fig = """
\\begin{figure}[htbp]
\\centering
\\includegraphics[width=\\columnwidth]{fig_7_latency_comparison.pdf}
\\caption{Consensus latency comparison highlighting sub-second finality of Tower BFT.}
\\label{fig:latency_comparison}
\\end{figure}
"""
    paper = paper.replace("\\subsection{Temporal Security Results}", "\\subsection{Temporal Security Results}\n" + latency_fig)

    with open("ids_to_bft_blockchain_ami_security.tex", "w", encoding="utf-8") as f:
        f.write(paper)
    print("Paper expanded successfully.")

if __name__ == "__main__":
    expand_paper()
