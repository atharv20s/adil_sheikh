import re

def fix_captions_and_refs():
    paper_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(paper_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Soften wording in Abstract
    content = content.replace(
        "We then prove that consensus validation latency creates",
        "We then analytically demonstrate that consensus validation latency creates"
    )

    # 2. Remove manual hardcoded numbers inside \caption{\textbf{Figure X --- ...}}
    # Replaces '\caption{\textbf{Figure 0 --- Title:} Body}' with '\caption{\textbf{Title:} Body}'
    content = re.sub(r'\\caption\{\\textbf\{Figure \d+ [—\-]+ ([^}]+)\}:', r'\\caption{\\textbf{\1}:', content)
    content = re.sub(r'\\caption\{\\textbf\{Figure \d+: ([^}]+)\}:', r'\\caption{\\textbf{\1}:', content)

    # Clean up any remaining manual 'Figure X ---' prefixes in captions
    content = re.sub(r'\\caption\{\\textbf\{Figure \d+ --- ([^}]+)\}', r'\\caption{\\textbf{\1}}', content)

    # 3. Ensure all \ref{} calls point to existing labels
    content = content.replace("Section~\\ref{sec:verification}", "Section~\\ref{sec:results_discussion}")
    content = content.replace("Section~\\ref{sec:temporal_benchmarking}", "Section~\\ref{sec:stsf}")

    # Save to both files
    with open(paper_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Captions cleaned! Hardcoded Figure X prefixes removed and Abstract wording softened.")

if __name__ == "__main__":
    fix_captions_and_refs()
