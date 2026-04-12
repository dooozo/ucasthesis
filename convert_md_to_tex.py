import re
import sys

def markdown_to_latex(md_text):
    """转换Markdown为LaTeX"""
    
    # 替换章节标题
    tex = re.sub(r'^# (.+)$', r'\\chapter{\1}\\label{chap:\1}', md_text, flags=re.MULTILINE)
    tex = re.sub(r'^## (.+)$', r'\\section{\1}\\label{sec:\1}', tex, flags=re.MULTILINE)
    tex = re.sub(r'^### (.+)$', r'\\subsection{\1}', tex, flags=re.MULTILINE)
    tex = re.sub(r'^#### (.+)$', r'\\subsubsection{\1}', tex, flags=re.MULTILINE)
    
    # 替换粗体
    tex = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', tex)
    
    # 替换斜体
    tex = re.sub(r'(?<!\*)\*(.+?)\*(?!\*)', r'\\textit{\1}', tex)
    
    # 替换行内代码
    tex = re.sub(r'`(.+?)`', r'\\texttt{\1}', tex)
    
    # 替换数学公式（显示模式）- $$ ... $$
    tex = re.sub(r'\$\$\n(.+?)\n\$\$', r'\n\\[\n\1\n\\]\n', tex, flags=re.DOTALL)
    
    # 替换数学公式（行内）- $ ... $ (但不替换 $$)
    tex = re.sub(r'(?<!\$)\$([^$\n]+)\$(?!\$)', r'$\1$', tex)
    
    return tex

# 读取原始Markdown
with open('/Users/bytedance/paper/0412md/1/00-全文合并.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# 转换
tex_content = markdown_to_latex(md_content)

# 添加LaTeX开头与结尾包装
full_tex = tex_content

# 输出
with open('Tex/Chap_Main_Content.tex', 'w', encoding='utf-8') as f:
    f.write(full_tex)

print('✓ Converted to Tex/Chap_Main_Content.tex')
