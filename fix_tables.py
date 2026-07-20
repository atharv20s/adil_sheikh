import sys
import re

with open('intrusion_detection_bft_paper.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace \begin{table}[...] with \begin{table*}[t]
# But we should be careful not to replace \begin{table*} if it already exists.
# We can use regex to find \begin{table} followed optionally by [...]
content = re.sub(r'\\begin\{table\}(?:\[.*?\])?', r'\\begin{table*}[t]', content)

# Replace \end{table} with \end{table*}
content = content.replace(r'\end{table}', r'\end{table*}')

# Fix any accidental \begin{table*}*} or similar just in case
content = content.replace(r'\begin{table*}*[t]', r'\begin{table*}[t]')
content = content.replace(r'\end{table*}*', r'\end{table*}')

with open('intrusion_detection_bft_paper.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced all table environments with table* to prevent column overlap.")
