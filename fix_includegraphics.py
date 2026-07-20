import os
import re

files_to_fix = [
    r'thesis\thesis_main.tex',
    r'thesis\figure_generation_guide.tex'
]

for filepath in files_to_fix:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace \includegraphics[...]{figures/file.png} -> \includegraphics[...]{file.png}
        content = re.sub(r'\\includegraphics\[(.*?)\]\{(\.\./)*figures/([^}]+)\}', r'\\includegraphics[\1]{\3}', content)
        
        # In case there are includes without optional arguments: \includegraphics{figures/file.png}
        content = re.sub(r'\\includegraphics\{(\.\./)*figures/([^}]+)\}', r'\\includegraphics{\2}', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed {filepath}")
    else:
        print(f"Not found: {filepath}")
