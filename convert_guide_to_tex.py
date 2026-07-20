import os
import re

md_path = 'C:/Users/athar/.gemini/antigravity-ide/brain/d5e1e49c-89e5-42a7-9d5f-9a3c86ccddd3/figure_generation_guide.md'
tex_path = 'figure_generation_guide.tex'

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# LaTeX Header
tex = []
tex.append(r'\documentclass[11pt, a4paper]{article}')
tex.append(r'\usepackage[margin=1in]{geometry}')
tex.append(r'\usepackage{graphicx}')
tex.append(r'\usepackage{amsmath, amssymb}')
tex.append(r'\usepackage{hyperref}')
tex.append(r'\usepackage{float}')
tex.append(r'\title{Exhaustive Thesis Figure Generation Guide}')
tex.append(r'\author{Automatically Generated Reference}')
tex.append(r'\date{\today}')
tex.append(r'\begin{document}')
tex.append(r'\maketitle')
tex.append(r'This document explains every single diagram generated across all scripts in the repository, with specific context extracted directly from the source code.')
tex.append(r'\tableofcontents')
tex.append(r'\clearpage')

# We split the markdown by "### "
sections = md_content.split('### ')

for sec in sections[1:]: # Skip the first preamble part
    lines = sec.strip().split('\n')
    title = lines[0].strip()
    
    tex.append(r'\section{' + title.replace('_', '\\_') + '}')
    
    # Extract filename
    file_match = re.search(r'\*\*File:\*\* ([^]+)', sec)
    if file_match:
        filename = file_match.group(1)
        tex.append(r'\textbf{File:} \texttt{' + filename.replace('_', '\\_') + r'} \\')
    
    # Extract Concept
    concept_match = re.search(r'\*\*Concept/Origin:\*\* (.*?)(?:\n|\*|$)', sec)
    if concept_match:
        concept = concept_match.group(1).replace('_', '\\_').replace('%', '\\%').replace('&', '\\&')
        tex.append(r'\textbf{Concept/Origin:} ' + concept + r' \\')
        
    # Extract Equations
    eq_match = re.search(r'\*\*Equations/Framework:\*\* \n(.*?)(?:\n---|$)', sec, re.DOTALL)
    if eq_match:
        eq = eq_match.group(1).strip()
        # Equations are already wrapped in , leave them as is for latex
        tex.append(r'\textbf{Equations/Framework:}')
        tex.append(eq)
        tex.append(r'\vspace{0.5cm}')

    # Extract image path
    img_match = re.search(r'!\[.*?\]\(file:///(.*?)\)', sec)
    if img_match:
        img_path = img_match.group(1)
        # We can just use the local 'figures' directory since we copied them from there!
        if file_match:
            local_img = 'figures/' + file_match.group(1)
            tex.append(r'\begin{figure}[H]')
            tex.append(r'    \centering')
            tex.append(r'    \includegraphics[width=0.75\textwidth]{' + local_img + '}')
            tex.append(r'\end{figure}')
    
    tex.append(r'\clearpage')

tex.append(r'\end{document}')

with open(tex_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(tex))

print("LaTeX file generated successfully!")
