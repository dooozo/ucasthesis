#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert Markdown content to LaTeX for thesis template."""

import re
import os
from pathlib import Path

def escape_latex(text):
    """Escape special LaTeX characters."""
    # Order matters: escape backslash first
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def convert_md_to_tex(md_content):
    """Convert markdown to LaTeX."""
    tex_content = md_content
    
    # Handle headings
    tex_content = re.sub(r'^# (.+)$', r'\\chapter{\1}', tex_content, flags=re.MULTILINE)
    tex_content = re.sub(r'^## (.+)$', r'\\section{\1}', tex_content, flags=re.MULTILINE)
    tex_content = re.sub(r'^### (.+)$', r'\\subsection{\1}', tex_content, flags=re.MULTILINE)
    tex_content = re.sub(r'^#### (.+)$', r'\\subsubsection{\1}', tex_content, flags=re.MULTILINE)
    
    # Handle bold
    tex_content = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', tex_content)
    
    # Handle italic
    tex_content = re.sub(r'\*(.+?)\*', r'\\textit{\1}', tex_content)
    tex_content = re.sub(r'_(.+?)_', r'\\textit{\1}', tex_content)
    
    # Handle inline code
    tex_content = re.sub(r'`([^`]+)`', r'\\texttt{\1}', tex_content)
    
    # Handle code blocks
    tex_content = re.sub(
        r'```([a-z]*)\n(.*?)```',
        r'\\begin{lstlisting}[language=\1]\n\2\\end{lstlisting}',
        tex_content,
        flags=re.DOTALL
    )
    
    # Handle lists
    lines = tex_content.split('\n')
    in_list = False
    new_lines = []
    
    for line in lines:
        if re.match(r'^\s*[-*]\s+', line):
            if not in_list:
                new_lines.append('\\begin{itemize}')
                in_list = True
            item_text = re.sub(r'^\s*[-*]\s+', '', line)
            new_lines.append(f'  \\item {item_text}')
        else:
            if in_list and line.strip():
                new_lines.append('\\end{itemize}')
                in_list = False
            new_lines.append(line)
    
    if in_list:
        new_lines.append('\\end{itemize}')
    
    tex_content = '\n'.join(new_lines)
    
    # Handle math mode (basic)
    tex_content = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', tex_content, flags=re.DOTALL)
    tex_content = re.sub(r'\$(.+?)\$', r'\\(\1\\)', tex_content)
    
    # Handle line breaks
    tex_content = tex_content.replace('---', '\\hrule')
    
    return tex_content

def main():
    md_file = Path('/Users/bytedance/paper/0412md/1/00-全文合并.md')
    output_file = Path('/Users/bytedance/paper/0412md/thesis-template/Tex/Chap_Main_Content.tex')
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to LaTeX
    tex_content = convert_md_to_tex(md_content)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(tex_content)
    
    print(f"Converted {md_file} to {output_file}")
    print(f"Output size: {len(tex_content)} characters")

if __name__ == '__main__':
    main()
