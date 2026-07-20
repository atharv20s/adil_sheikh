import re

def check_ampersands():
    with open("intrusion_detection_bft_paper.tex", "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_alignment = False
    issues = []

    for idx, line in enumerate(lines, 1):
        if "\\begin{tabular" in line or "\\begin{align" in line or "\\begin{split" in line:
            in_alignment = True
        if "\\end{tabular" in line or "\\end{align" in line or "\\end{split" in line:
            in_alignment = False
            continue

        if not in_alignment:
            matches = re.findall(r'(?<!\\)&', line)
            if matches:
                issues.append((idx, line.strip()))

    print(f"Total unescaped ampersand issues outside tabular/align/split: {len(issues)}")
    for line_num, text in issues:
        print(f"Line {line_num}: {text}")

if __name__ == "__main__":
    check_ampersands()
