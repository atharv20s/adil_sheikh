import os

def clean_duplicates():
    file_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove Fig 0 if present before abstract
    abs_pos = content.find("\\begin{abstract}")
    fig0_pos = content.find("\\label{fig:fig0_paper_roadmap}")
    if fig0_pos != -1 and fig0_pos < abs_pos:
        # Find the start of figure before fig0_pos
        fig_start = content.rfind("\\begin{figure}", 0, fig0_pos)
        fig_end = content.find("\\end{figure}", fig0_pos) + len("\\end{figure}")
        content = content[:fig_start] + content[fig_end:]

    # Ensure Fig 0 is placed after Section I-G
    if "\\label{fig:fig0_paper_roadmap}" not in content:
        content = content.replace(
            "\\subsection{Paper Roadmap}",
            "\\subsection{Paper Roadmap}\nFig. \\ref{fig:fig0_paper_roadmap} details the overarching structural organization of this paper."
        )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Cleaned up duplicate figure declarations! Total lines: {len(content.splitlines())}")

if __name__ == "__main__":
    clean_duplicates()
