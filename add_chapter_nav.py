#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界'

MODULES = ['world', 'characters', 'locations', 'techniques', 'artifacts', 'story', 'side-stories', 'philosophy']

def get_relative_path(from_path, to_path):
    """计算从 from_path 到 to_path 的相对路径"""
    from_parts = from_path.replace('\\', '/').split('/')
    to_parts = to_path.replace('\\', '/').split('/')
    
    # 找到共同前缀
    common = 0
    for i in range(min(len(from_parts), len(to_parts))):
        if from_parts[i] == to_parts[i]:
            common += 1
        else:
            break
    
    # 从 from_path 到共同前缀，需要 "../"
    up_levels = len(from_parts) - common - 1
    rel_parts = ['..'] * up_levels if up_levels > 0 else []
    
    # 从共同前缀到 to_path
    rel_parts.extend(to_parts[common:])
    
    return '/'.join(rel_parts) if rel_parts else to_parts[-1]

def build_nav_html(prev_path, next_path, current_path):
    """构建悬浮导航 HTML"""
    if prev_path:
        rel = get_relative_path(current_path, prev_path)
        prev_html = '<a href="%s" class="prev-btn">上一章</a>' % rel
    else:
        prev_html = '<span class="prev-btn disabled">上一章</span>'
    
    if next_path:
        rel = get_relative_path(current_path, next_path)
        next_html = '<a href="%s" class="next-btn">下一章</a>' % rel
    else:
        next_html = '<span class="next-btn disabled">下一章</span>'
    
    return '<div class="chapter-nav">\n  %s\n  %s\n</div>' % (prev_html, next_html)

def process_module(module_name):
    """处理单个模块，添加章节导航"""
    module_dir = os.path.join(BASE_DIR, module_name)
    if not os.path.exists(module_dir):
        return 0
    
    # 收集所有非 index.html 的 HTML 文件
    files = []
    for root, dirs, filenames in os.walk(module_dir):
        for f in filenames:
            if f.endswith('.html') and f != 'index.html':
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, BASE_DIR).replace('\\', '/')
                files.append(rel_path)
    
    # 按文件路径排序
    files.sort()
    
    # 为每个文件添加导航
    count = 0
    for i, current_path in enumerate(files):
        prev_path = files[i - 1] if i > 0 else None
        next_path = files[i + 1] if i < len(files) - 1 else None
        
        full_path = os.path.join(BASE_DIR, current_path)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果已有导航，先移除
        content = re.sub(r'<div class="chapter-nav">.*?</div>\s*', '', content, flags=re.DOTALL)
        
        nav_html = build_nav_html(prev_path, next_path, current_path)
        
        # 在 </body> 之前插入导航
        if '</body>' in content:
            content = content.replace('</body>', nav_html + '\n</body>')
        else:
            content = content + '\n' + nav_html
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        count += 1
    
    return count

def main():
    total = 0
    for module in MODULES:
        count = process_module(module)
        total += count
        print('Module %s: %d files processed' % (module, count))
    
    print('\nTotal: %d files processed' % total)

if __name__ == '__main__':
    main()
