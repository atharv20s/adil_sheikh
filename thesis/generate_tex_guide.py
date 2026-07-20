import os
import glob

# Ensure we pull the list of pngs from the correct directory relative to root
all_pngs = sorted(glob.glob('../figures/*.png'))

def extract_concept(basename):
    clean = basename.replace('.png', '').replace('fig_', '').replace('fig', '')
    clean = ''.join([c for c in clean if not c.isdigit() or c == '_'])
    clean = clean.lstrip('_')
    
    parts = clean.split('_')
    title = ' '.join(parts).title()
    
    if 'Vs' in title:
        x_y = title.split(' Vs ')
        if len(x_y) == 2:
            return title, x_y[0], x_y[1]
    
    return title, title + " Metric", "Time / Baseline Parameter"

with open('figure_generation_guide.tex', 'w', encoding='utf-8') as f:
    f.write('\\documentclass[11pt, a4paper]{article}\n')
    f.write('\\usepackage[margin=1in]{geometry}\n')
    f.write('\\usepackage{graphicx}\n')
    # ADDED GRAPHICSPATH SO IT FINDS THE IMAGES!
    f.write('\\graphicspath{{../figures/}}\n') 
    f.write('\\usepackage{amsmath, amssymb}\n')
    f.write('\\usepackage{float}\n')
    f.write('\\usepackage[utf8]{inputenc}\n')
    f.write('\\title{Exhaustive Thesis Figure Generation Guide}\n')
    f.write('\\author{Automatically Generated Reference}\n')
    f.write('\\begin{document}\n')
    f.write('\\maketitle\n')
    f.write('\\tableofcontents\n')
    f.write('\\clearpage\n\n')
    
    for png in all_pngs:
        basename = os.path.basename(png)
        title, y_ax, x_ax = extract_concept(basename)
        
        if basename == 'fig_1_architecture.png':
            title = 'AMI Architecture Comparison'
            desc = 'Contrasts a reactive centralized IDS (left) with a proactive distributed BFT blockchain (right).'
            eq = 'Architectural block diagram (No mathematical equations)'
        elif basename == 'fig_9_attack_graph.png':
            title = 'Twelve-Attack Threat Vector Graph'
            desc = 'Maps the progression of the Twelve-Attack Model defined in your thesis.'
            eq = 'Directed Graph mapping attack propagation paths'
        elif basename == 'fig_8_blockchain_arch.png':
            title = 'BFT Blockchain Topology'
            desc = 'A network topology diagram showing how a smart meter client submits a transaction to a mempool.'
            eq = 'Ring topology graph'
        elif basename == 'fig_4_radar_comparison.png':
            title = 'Consensus Radar Comparison'
            desc = 'A multi-dimensional qualitative comparison between Reactive IDS, PBFT, Tower BFT, and RVR.'
            eq = 'Normalized Polar Plot representation'
        else:
            desc = f'This plot visualizes \\textbf{{{y_ax.replace("_", "\\_")}}} as a function of \\textbf{{{x_ax.replace("_", "\\_")}}}.'
            if 'Latency' in title:
                eq = r"\[ L_{total} = L_{net} + L_{consensus} \]"
            elif 'Prob' in title or 'Psecure' in title or 'Vulnerability' in title or 'Risk' in title:
                eq = r"\[ P_{Byz} = \sum_{i=f+1}^{n} \binom{n}{i} p_c^i (1-p_c)^{n-i} \]" + "\n" + r"\[ P_{temporal} = 1 - e^{-\lambda L P_{TA}} \]"
            elif 'Energy' in title or 'Message' in title:
                eq = r"\[ E_{total} = E_{tx} + E_{rx} + E_{crypto} \]"
            elif 'Heatmap' in title or 'Pareto' in title:
                eq = r"\[ P_{secure} = \max( \text{Security} ) \quad \text{s.t.} \quad L_{total} \le L_{max} \]"
            else:
                eq = 'Empirical baseline calculation from simulation data.'

        f.write(f'\\section{{{title.replace("_", "\\_")}}}\n')
        f.write(f'\\textbf{{File:}} \\texttt{{{basename.replace("_", "\\_")}}} \\\\\n')
        f.write(f'\\textbf{{Concept/Origin:}} {desc} \\\\\n')
        f.write(f'\\textbf{{Equations/Framework:}} \n{eq}\n\\vspace{{0.5cm}}\n')
        
        f.write('\\begin{figure}[H]\n')
        f.write('    \\centering\n')
        # USING ONLY BASENAME NOW AS REQUESTED BY USER!
        f.write(f'    \\includegraphics[width=0.75\\textwidth]{{{basename}}}\n')
        f.write('\\end{figure}\n')
        f.write('\\clearpage\n\n')
        
    f.write('\\end{document}\n')

print("LaTeX guide perfectly regenerated!")
