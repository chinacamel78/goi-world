import os
import re

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界'

def get_logo_path(html_path):
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
            
            # 替换所有 🎏 emoji 为 img 标签
            # 模式1: 导航栏 logo
            content = content.replace(
                '<span class="koi-icon">🎏</span>',
                '<img class="koi-icon" src="%s" alt="锦鲤界">' % logo_path
            )
            
            # 模式2: 面包屑链接中的 🎏 锦鲤界
            content = content.replace(
                '>🎏 锦鲤界</a>',
                '><img src="%s" alt="锦鲤界" style="height:1.5rem;vertical-align:middle;"></a>' % logo_path
            )
            
            # 模式3: 标题中的 🎏
            content = content.replace(
                '🎏 锦鲤界',
                '<img src="%s" alt="锦鲤界" style="height:2.5rem;vertical-align:middle;margin-right:0.5rem;">锦鲤界' % logo_path
            )
            content = content.replace(
                '🎏 世界观',
                '<img src="%s" alt="世界观" style="height:2.5rem;vertical-align:middle;margin-right:0.5rem;">世界观' % logo_path
            )
            content = content.replace(
                '🎏 人物',
                '<img src="%s" alt="人物" style="height:2.5rem;vertical-align:middle;margin-right:0.5rem;">人物' % logo_path
            )
            content = content.replace(
                '🎏 地点',
                '<img src="%s" alt="地点" style="height:2.5rem;vertical-align:middle;margin-right:0.5rem;">地点' % logo_path
            )
            content = content.replace(
                '🎏 教学理念',
                '<img src="%s" alt="教学理念" style="height:2.5rem;vertical-align:middle;margin-right:0.5rem;">教学理念' % logo_path
            )
            
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(content)
            
            total += 1

print('Updated %d HTML files' % total)
