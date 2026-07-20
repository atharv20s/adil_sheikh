import re
import os

def polish_thesis():
    thesis_path = "thesis/thesis_main.tex"
    
    with open(thesis_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Standardize Names back to the correct ones
    # Since I incorrectly changed everything to "Prof. Adil Sheikh", I will change it back.
    content = content.replace(
        "Prof.\\ Adil Sheikh",
        "Prof.\\ Uday Suryavanshi \\& Dr.\\ Sunny Kumar"
    )
    content = content.replace(
        "Professor Adil Sheikh",
        "Prof. Uday Suryavanshi \\& Dr. Sunny Kumar"
    )
    content = content.replace(
        "Prof. Adil Sheikh",
        "Prof. Uday Suryavanshi \\& Dr. Sunny Kumar"
    )
    # The previous script successfully replaced "Athar Nakhuda" with "Atharv Manojkumar Shukla",
    # so we don't need to change it back. But we'll just ensure it's uniform.
    content = content.replace(
        "Athar Nakhuda",
        "Atharv Manojkumar Shukla"
    )
    
    with open(thesis_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Thesis names standardized successfully.")

if __name__ == "__main__":
    polish_thesis()
