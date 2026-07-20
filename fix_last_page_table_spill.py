import os

def fix_table_spill():
    file_path = "intrusion_detection_bft_paper.tex"
    restructured_path = "intrusion_detection_bft_paper_restructured.tex"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add flushend package if not present
    if "\\usepackage{flushend}" not in content:
        content = content.replace(
            "\\usepackage{tikz}",
            "\\usepackage{tikz}\n\\usepackage{flushend}"
        )

    # 2. Find Table A, B, C blocks
    table_a_start = content.find("\\begin{table*}[t]\n\\caption{Table A:")
    table_c_end = content.find("\\end{table*}", content.find("\\caption{Table C:")) + len("\\end{table*}")

    if table_a_start != -1 and table_c_end != -1:
        tables_block = content[table_a_start:table_c_end]
        # Remove tables from current position
        content = content[:table_a_start] + content[table_c_end:]
        
        # Change [t] to [htbp] for better placement flexibility
        tables_block = tables_block.replace("\\begin{table*}[t]", "\\begin{table*}[htbp]")

        # Insert tables block earlier at Section V Protocol Comparisons
        sec5_pos = content.find("\\section{Protocol Comparisons}")
        if sec5_pos != -1:
            insert_pos = content.find("\n", sec5_pos) + 1
            content = content[:insert_pos] + "\n" + tables_block + "\n\n" + content[insert_pos:]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(restructured_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Table spill fixed! Tables moved earlier and flushend balance enabled!")

if __name__ == "__main__":
    fix_table_spill()
