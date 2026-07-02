import os
import re

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界'

def get_logo_path(html_path):
    """计算从 HTML 文件到 assets/images/logo.png 的相对路径"""
    rel_dir = os.path.dirname(os.path.relpath(html_path, BASE_DIR))
    if rel_dir == '':
        return 'assets/images/logo.png'
    depth = len(rel_dir.split(os.sep))
    return '../' * depth + 'assets/images/logo.png'

total = 0
for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d not in ['assets', '.git', '锦鲤界-backup']]
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fp:
                content = fp.read()
            
            if '🎏' not in content:
                continue
            
            logo_path = get_logo_path(path)
            # 替换导航栏中的 logo
            content = content.replace(
                '<span class="koi-icon">🎏</span>',
                '<img class="koi-icon" src="%s" alt="锦鲤界">' % logo_path
            )
            
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(content)
            
            total += 1

print('Updated %d HTML files' % total)
