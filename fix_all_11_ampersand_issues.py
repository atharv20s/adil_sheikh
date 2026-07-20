import os

def fix_all_ampersands():
    paper_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(paper_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replacements for unescaped ampersands in text/TikZ
    content = content.replace("Roadmap & Engineering", "Roadmap \\& Engineering")
    content = content.replace("Trust & Grid", "Trust \\& Grid")
    content = content.replace("Engineering & Threat", "Engineering \\& Threat")
    content = content.replace("Synthesis & Engineering", "Synthesis \\& Engineering")
    content = content.replace("Engineering Assessment} (Map DCUs & Substation Gateways)", "Engineering Assessment} (Map DCUs \\& Substation Gateways)")
    content = content.replace("Production Deployment & Monitoring", "Production Deployment \\& Monitoring")

    # Fix multiline equations that had & without \begin{split}
    eq1_old = r"""\begin{equation}
P_{secure}^{no\_BC} &= (1-0.599)^3(1-0.05)(1-0.15)(1-1)\\
&\quad \times (1-0.2)(1-0.35)(1-1)(1-0.01)^3
\end{equation}"""

    eq1_new = r"""\begin{equation}
\begin{split}
P_{secure}^{no\_BC} &= (1-0.599)^3(1-0.05)(1-0.15)(1-1)\\
&\quad \times (1-0.2)(1-0.35)(1-1)(1-0.01)^3
\end{split}
\end{equation}"""

    eq2_old = r"""\begin{equation}
P_{secure, limited}^{no\_BC} &= (1-0.599)^3(1-0.05)(1-0.15)\\
&\quad \times (1-0.2)(1-0.35)(1-0.01)^3 \\
&\approx 0.026
\end{equation}"""

    eq2_new = r"""\begin{equation}
\begin{split}
P_{secure, limited}^{no\_BC} &= (1-0.599)^3(1-0.05)(1-0.15)\\
&\quad \times (1-0.2)(1-0.35)(1-0.01)^3 \\
&\approx 0.026
\end{split}
\end{equation}"""

    content = content.replace(eq1_old, eq1_new)
    content = content.replace(eq2_old, eq2_new)

    with open(paper_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("All 11 ampersand and equation split issues fixed!")

if __name__ == "__main__":
    fix_all_ampersands()
