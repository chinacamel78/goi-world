#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import glob

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设'
OUTPUT_DIR = os.path.join(BASE_DIR, '锦鲤界')
MD_DIR = os.path.join(BASE_DIR, '01-文本内容（Markdown）')

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — 锦鲤界</title>
  <link rel="stylesheet" href="{css_path}assets/css/koi-world.css">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
</head>
<body>
  <canvas id="particles-canvas"></canvas>
  <div class="koi-swim"></div><div class="koi-swim"></div><div class="koi-swim"></div>
  <nav class="nav-bar">
    <a href="{home_path}index.html" class="nav-logo"><span class="koi-icon">🎏</span><span>锦鲤界</span></a>
    <ul class="nav-links">
      <li><a href="{home_path}world/index.html">世界观</a></li>
      <li><a href="{home_path}characters/index.html">人物</a></li>
      <li><a href="{home_path}locations/index.html">地点</a></li>
      <li><a href="{home_path}techniques/index.html">功法</a></li>
      <li><a href="{home_path}artifacts/index.html">法宝</a></li>
      <li><a href="{home_path}story/index.html">主线</a></li>
      <li><a href="{home_path}side-stories/index.html">支线</a></li>
      <li><a href="{home_path}philosophy/index.html">理念</a></li>
    </ul>
  </nav>
  <div class="page-container">
    <div class="breadcrumb"><a href="{home_path}index.html">锦鲤界</a> <span class="separator">/</span> {breadcrumbs} <span class="current">{page_name}</span></div>
    <section class="hero-section"><h1 class="hero-title">{hero_title}</h1><p class="hero-subtitle">{hero_subtitle}</p></section>
    <div class="divider"></div>
    <section class="section fade-in"><div class="content-body">{content}</div></section>
    <div class="divider"></div>
    <section class="section fade-in" style="text-align:center;padding:2rem;"><p style="color:var(--text-muted);font-size:0.9rem;"><a href="{home_path}index.html" style="color:var(--cyan-primary);text-decoration:none;">返回锦鲤界总览</a></p></section>
  </div>
  <script src="{css_path}assets/js/koi-world.js"></script>
</body></html>'''

def simple_md_to_html(text):
    text = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', text, flags=re.DOTALL)
    text = re.sub(r'^#{6} (.+)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
    text = re.sub(r'^#{5} (.+)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
    text = re.sub(r'^#{4} (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^#{3} (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^#{2} (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', text, flags=re.MULTILINE)
    text = re.sub(r'^- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.+</li>\n)+', r'<ul>\g<0></ul>', text, flags=re.DOTALL)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    paragraphs = text.split('\n\n')
    out = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<') and not p.startswith('```'):
            p = f'<p>{p}</p>'
        out.append(p)
    return '\n\n'.join(out)

def md_to_html(md_text):
    if HAS_MARKDOWN:
        try:
            return markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
        except Exception:
            pass
    return simple_md_to_html(md_text)

def generate_single(md_path, out_path, title, hero_title, hero_subtitle, breadcrumbs, page_name, depth):
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()
    html = md_to_html(md)
    css_path = '../' * depth if depth > 0 else ''
    home_path = '../' * depth if depth > 0 else ''
    result = HTML_TEMPLATE.format(
        title=title, css_path=css_path, home_path=home_path,
        breadcrumbs=breadcrumbs, page_name=page_name,
        hero_title=hero_title, hero_subtitle=hero_subtitle, content=html
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result)

def generate_module(module_dir, out_module_dir, module_name, icon, depth=1):
    items = []
    for root, dirs, files in os.walk(module_dir):
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            md_path = os.path.join(root, f)
            rel = os.path.relpath(md_path, module_dir)
            out_rel = rel.replace('.md', '.html')
            out_path = os.path.join(out_module_dir, out_rel)
            
            with open(md_path, 'r', encoding='utf-8') as fp:
                first_line = fp.readline().strip()
            title = first_line.lstrip('#').strip() or f.replace('.md', '')
            title = re.sub(r'[\*\`]', '', title)
            
            rel_depth = depth + rel.count(os.sep)
            bc = f'<a href="{module_name}/index.html">{module_name}</a> <span class="separator">/</span>'
            
            generate_single(md_path, out_path, title, f'{icon} {title}', 
                          f'{module_name} - {title}', bc, title, rel_depth)
            
            href = out_rel.replace('.md', '.html').replace('\\', '/')
            items.append({'href': href, 'title': title, 'desc': title[:50], 'icon': icon, 'tags': []})
    
    cards = []
    for item in items:
        card = f'<a href="{item["href"]}" class="card"><div class="card-glow"></div><span class="card-icon">{item["icon"]}</span><h3 class="card-title">{item["title"]}</h3><p class="card-desc">{item["desc"]}</p></a>'
        cards.append(card)
    
    css_path = '../' * depth if depth > 0 else ''
    home_path = '../' * depth if depth > 0 else ''
    index_html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{module_name} - 锦鲤界</title>
<link rel="stylesheet" href="{css_path}assets/css/koi-world.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
</head><body>
<canvas id="particles-canvas"></canvas><div class="koi-swim"></div><div class="koi-swim"></div><div class="koi-swim"></div>
<nav class="nav-bar"><a href="{home_path}index.html" class="nav-logo"><span class="koi-icon">🎏</span><span>锦鲤界</span></a>
<ul class="nav-links"><li><a href="{home_path}world/index.html">世界观</a></li><li><a href="{home_path}characters/index.html">人物</a></li><li><a href="{home_path}locations/index.html">地点</a></li><li><a href="{home_path}techniques/index.html">功法</a></li><li><a href="{home_path}artifacts/index.html">法宝</a></li><li><a href="{home_path}story/index.html">主线</a></li><li><a href="{home_path}side-stories/index.html">支线</a></li><li><a href="{home_path}philosophy/index.html">理念</a></li></ul></nav>
<div class="page-container">
<div class="breadcrumb"><a href="{home_path}index.html">锦鲤界</a> <span class="separator">/</span> <span class="current">{module_name}</span></div>
<section class="hero-section"><h1 class="hero-title">{icon} {module_name}</h1><p class="hero-subtitle">共 {len(items)} 项内容</p></section>
<div class="divider"></div>
<section class="section fade-in"><div class="card-grid">{''.join(cards)}</div></section>
<div class="divider"></div>
<section class="section fade-in" style="text-align:center;padding:2rem;"><p style="color:var(--text-muted);font-size:0.9rem;"><a href="{home_path}index.html" style="color:var(--cyan-primary);text-decoration:none;">返回锦鲤界总览</a></p></section>
</div>
<script src="{css_path}assets/js/koi-world.js"></script>
</body></html>'''
    
    os.makedirs(out_module_dir, exist_ok=True)
    with open(os.path.join(out_module_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    return len(items)

def main():
    print("Batch generating all remaining modules\n")
    
    count = generate_module(os.path.join(MD_DIR, '04-功法'), os.path.join(OUTPUT_DIR, 'techniques'), '功法', '⚡', depth=1)
    print(f"Techniques: {count} pages")
    
    count = generate_module(os.path.join(MD_DIR, '05-法宝'), os.path.join(OUTPUT_DIR, 'artifacts'), '法宝', '🔮', depth=1)
    print(f"Artifacts: {count} pages")
    
    count = generate_module(os.path.join(MD_DIR, '06-主线剧情'), os.path.join(OUTPUT_DIR, 'story'), '主线剧情', '📖', depth=1)
    print(f"Story: {count} pages")
    
    count = generate_module(os.path.join(MD_DIR, '07-支线剧情'), os.path.join(OUTPUT_DIR, 'side-stories'), '支线剧情', '🔍', depth=1)
    print(f"Side stories: {count} pages")
    
    total = 0
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            if f.endswith('.html'):
                total += 1
    
    print(f"\nTotal HTML pages: {total}")

if __name__ == '__main__':
    main()
