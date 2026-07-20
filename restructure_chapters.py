import re

with open('thesis/thesis_main.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert Chapters 1-5 before Threat Model
chapters_1_5 = r'''\chapter{Introduction}
\label{ch:introduction}
% TODO: Introduction content

\chapter{Research Framework}
\label{ch:research_framework}
% TODO: Research Framework content

\chapter{AMI Background}
\label{ch:ami_background}
% TODO: AMI Background content

\chapter{IDS Background}
\label{ch:ids_background}
% TODO: IDS Background content

\chapter{Blockchain Background}
\label{ch:blockchain_background}
% TODO: Blockchain Background content

'''
content = content.replace(r'\chapter{Threat Model}', chapters_1_5 + r'\chapter{Threat Model}')

# 2. Rename Security Framework to Security Mathematics
content = content.replace(r'\chapter{Security Framework}', r'\chapter{Security Mathematics}')
content = content.replace(r'\label{ch:security_framework}', r'\label{ch:security_mathematics}')

# 3. Split Consensus Mathematics
consensus_math_header = r'''\chapter{Consensus Mathematics}
\label{ch:consensus_mathematics}

This chapter details the formal mathematical algorithms and models underlying the consensus mechanisms evaluated in this research.

'''
content = content.replace(r'\section{Classic PBFT}', consensus_math_header + r'\section{Classic PBFT}')

# 4. Insert Design Decisions before Experimental Design
design_decisions = r'''\chapter{Design Decisions}
\label{ch:design_decisions}
% TODO: Design Decisions content

'''
content = content.replace(r'\chapter{Experimental Design}', design_decisions + r'\chapter{Experimental Design}')

# 5. Insert Verification & Validation before Results
vv = r'''\chapter{Verification \& Validation}
\label{ch:verification_validation}
% TODO: Verification and Validation content

'''
content = content.replace(r'\chapter{Results}', vv + r'\chapter{Results}')

with open('thesis/thesis_main.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Restructured chapters successfully.")
