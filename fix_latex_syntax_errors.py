import re

def fix_latex_errors():
    paper_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(paper_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace unescaped & in section/subsection/subsubsection titles
    content = content.replace("\\subsection{Cybersecurity Challenges & Research Gap}", "\\subsection{Cybersecurity Challenges \\& Research Gap}")
    content = content.replace("Key Management and Defense-in-Depth", "Key Management and Defense-in-Depth")
    content = content.replace("Application & Control Layer Attacks", "Application \\& Control Layer Attacks")
    content = content.replace("Consensus & Identity Layer Attacks", "Consensus \\& Identity Layer Attacks")
    content = content.replace("Data and Code Availability", "Data and Code Availability")
    content = content.replace("Data & Code Availability", "Data \\& Code Availability")
    content = content.replace("Data and Code Availability Statement", "Data and Code Availability Statement")

    # Fix unescaped & in TikZ nodes or headings
    content = content.replace("Metering & SCADA", "Metering \\& SCADA")
    content = content.replace("Consensus & Identity", "Consensus \\& Identity")
    content = content.replace("Physical & Sensor", "Physical \\& Sensor")
    content = content.replace("Results and Discussion", "Results and Discussion")

    # Fix nested figure tags if any
    content = re.sub(r'\\begin\{figure\}\[htbp\]\s*\\centering\s*\\includegraphics\[width=0.9\\columnwidth\]\{fig_model_comparison\.png\}\s*\\begin\{figure\}\[htbp\]', 
                     r'\\begin{figure}[htbp]', content)

    # Save to both files
    with open(paper_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("LaTeX syntax errors fixed! All unescaped ampersands replaced with \\&.")

if __name__ == "__main__":
    fix_latex_errors()
