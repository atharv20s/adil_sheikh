import os

def enhance_sections():
    file_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Section II title for maximum visual clarity
    content = content.replace(
        "\\section{Without Blockchain}",
        "\\section{Without Blockchain Baseline Security Evaluation (Centralized Architecture)}"
    )

    # 2. Update Section III title for maximum visual clarity
    content = content.replace(
        "\\section{With Blockchain}",
        "\\section{With Blockchain Security Evaluation (Decentralized BFT Architecture)}"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Enhanced Section II and Section III headers across both tex files!")

if __name__ == "__main__":
    enhance_sections()
