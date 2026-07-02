#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成锦鲤界 HTML 页面
从 Markdown 内容生成赛博修仙风格的可视化网页
"""

import os
import re
import glob

# 尝试导入 markdown 库，失败则使用简单转换
try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设'
OUTPUT_DIR = os.path.join(BASE_DIR, '锦鲤界')
MD_DIR = os.path.join(BASE_DIR, '01-文本内容（Markdown）')

# HTML 模板
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
  <div class="koi-swim"></div>
  <div class="koi-swim"></div>
  <div class="koi-swim"></div>

  <nav class="nav-bar">
    <a href="{home_path}index.html" class="nav-logo">
      <span class="koi-icon">🎏</span>
      <span>锦鲤界</span>
    </a>
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
    <div class="breadcrumb">
      <a href="{home_path}index.html">🎏 锦鲤界</a>
      <span class="separator">›</span>
      {breadcrumbs}
      <span class="current">{page_name}</span>
    </div>

    <section class="hero-section">
      <h1 class="hero-title">{hero_title}</h1>
      <p class="hero-subtitle">{hero_subtitle}</p>
    </section>

    <div class="divider"></div>

    <section class="section fade-in">
      <div class="content-body">
{content}
      </div>
    </section>

    <div class="divider"></div>

    <section class="section fade-in" style="text-align: center; padding: 2rem;">
      <p style="color: var(--text-muted); font-size: 0.9rem;">
        <a href="{home_path}index.html" style="color: var(--cyan-primary); text-decoration: none;">← 返回锦鲤界总览</a>
      </p>
    </section>
  </div>

  <script src="{css_path}assets/js/koi-world.js"></script>
</body>
</html>'''


def md_to_html(md_text):
    """将 Markdown 转换为 HTML"""
    if HAS_MARKDOWN:
        try:
            return markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
        except Exception:
            pass
    return simple_md_to_html(md_text)


def simple_md_to_html(md_text):
    """简单的 Markdown 到 HTML 转换"""
    text = md_text
    
    # 代码块
    text = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', text, flags=re.DOTALL)
    
    # 标题
    text = re.sub(r'^#{6} (.+)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
    text = re.sub(r'^#{5} (.+)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
    text = re.sub(r'^#{4} (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^#{3} (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^#{2} (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # 粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # 斜体
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # 引用
    text = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', text, flags=re.MULTILINE)
    
    # 表格（简化处理）
    lines = text.split('\n')
    in_table = False
    table_html = []
    result = []
    
    for line in lines:
        if line.startswith('|') and '|' in line[1:]:
            if not in_table:
                in_table = True
                table_html = ['<table class="data-table">']
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(c.replace('-', '').replace(' ', '') == '' for c in cells):
                continue  # 跳过分隔行
            row = '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
            table_html.append(row)
        else:
            if in_table:
                table_html.append('</table>')
                result.append('\n'.join(table_html))
                in_table = False
                table_html = []
            result.append(line)
    
    if in_table:
        table_html.append('</table>')
        result.append('\n'.join(table_html))
    
    text = '\n'.join(result)
    
    # 段落
    paragraphs = text.split('\n\n')
    new_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<') and not p.startswith('```'):
            p = f'<p>{p}</p>'
        new_paragraphs.append(p)
    text = '\n\n'.join(new_paragraphs)
    
    return text


def generate_page(md_path, output_path, title, hero_title, hero_subtitle, breadcrumbs, page_name, depth=0):
    """生成单个 HTML 页面"""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = md_to_html(md_content)
    
    # 计算相对路径
    css_path = '../' * depth if depth > 0 else ''
    home_path = '../' * depth if depth > 0 else ''
    
    html = HTML_TEMPLATE.format(
        title=title,
        css_path=css_path,
        home_path=home_path,
        breadcrumbs=breadcrumbs,
        page_name=page_name,
        hero_title=hero_title,
        hero_subtitle=hero_subtitle,
        content=html_content
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path


def generate_module_index(module_name, module_path, output_dir, items, depth=0):
    """生成模块索引页面"""
    title = f"{module_name} — 锦鲤界"
    hero_title = f"🎏 {module_name}"
    hero_subtitle = f"探索锦鲤宗的{module_name}，共 {len(items)} 项内容"
    
    css_path = '../' * depth if depth > 0 else ''
    home_path = '../' * depth if depth > 0 else ''
    
    cards_html = []
    for item in items:
        card = f'''
        <a href="{item['href']}" class="card">
          <div class="card-glow"></div>
          <span class="card-icon">{item.get('icon', '📄')}</span>
          <h3 class="card-title">{item['title']}</h3>
          <p class="card-desc">{item.get('desc', '')}</p>
          {''.join(f'<span class="card-tag">{tag}</span>' for tag in item.get('tags', []))}
        </a>'''
        cards_html.append(card)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="{css_path}assets/css/koi-world.css">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
</head>
<body>
  <canvas id="particles-canvas"></canvas>
  <div class="koi-swim"></div>
  <div class="koi-swim"></div>
  <div class="koi-swim"></div>

  <nav class="nav-bar">
    <a href="{home_path}index.html" class="nav-logo">
      <span class="koi-icon">🎏</span>
      <span>锦鲤界</span>
    </a>
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
    <div class="breadcrumb">
      <a href="{home_path}index.html">🎏 锦鲤界</a>
      <span class="separator">›</span>
      <span class="current">{module_name}</span>
    </div>

    <section class="hero-section">
      <h1 class="hero-title">{hero_title}</h1>
      <p class="hero-subtitle">{hero_subtitle}</p>
    </section>

    <div class="divider"></div>

    <section class="section fade-in">
      <div class="card-grid">
        {''.join(cards_html)}
      </div>
    </section>

    <div class="divider"></div>

    <section class="section fade-in" style="text-align: center; padding: 2rem;">
      <p style="color: var(--text-muted); font-size: 0.9rem;">
        <a href="{home_path}index.html" style="color: var(--cyan-primary); text-decoration: none;">← 返回锦鲤界总览</a>
      </p>
    </section>
  </div>

  <script src="{css_path}assets/js/koi-world.js"></script>
</body>
</html>'''
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    """主生成函数"""
    print("=== 开始生成锦鲤界网页 ===\n")
    
    # 1. 世界观模块
    print("生成 世界观...")
    world_files = [
        ('01-两界战争总纲.md', '两界战争总纲', '灵码界与两界战争的起源', '两界战争总纲'),
        ('02-灵码界设定.md', '灵码界设定', '灵码界的地理与规则', '灵码界设定'),
        ('03-锦鲤宗宗旨.md', '锦鲤宗宗旨', '锦鲤宗的使命与理念', '锦鲤宗宗旨'),
        ('04-核心冲突.md', '核心冲突', '碳基与硅基的终极对抗', '核心冲突'),
        ('05-天赋体系总纲.md', '天赋体系总纲', '五脉灵根、十二天赋灵纹、五道修炼法门', '天赋体系总纲'),
    ]
    
    world_items = []
    for filename, title, desc, page_name in world_files:
        md_path = os.path.join(MD_DIR, '01-世界观', filename)
        if os.path.exists(md_path):
            output_path = os.path.join(OUTPUT_DIR, 'world', filename.replace('.md', '.html'))
            generate_page(md_path, output_path, title, f'🌌 {title}', desc, 
                         '<a href="world/index.html">世界观</a> <span class="separator">›</span>', page_name, depth=1)
            world_items.append({'href': filename.replace('.md', '.html'), 'title': title, 'desc': desc, 'icon': '📜', 'tags': []})
    
    generate_module_index('世界观', 'world', os.path.join(OUTPUT_DIR, 'world'), world_items, depth=1)
    
    # 2. 人物模块
    print("生成 人物...")
    char_items = []
    
    # 宗主
    master_files = [
        ('01-宗主/01-灵码真人.md', '灵码真人', '锦鲤宗宗主', '👑'),
    ]
    # 长老
    elder_files = [
        ('02-长老会/01-开心真人.md', '开心真人', '成长老', '👴'),
        ('02-长老会/02-启元真人.md', '启元真人', '冯长老', '👴'),
        ('02-长老会/03-齐鲁真人.md', '齐鲁真人', '朱长老', '👴'),
        ('02-长老会/04-静渊真人.md', '静渊真人', '胡长老', '👴'),
        ('02-长老会/05-邓长老.md', '邓长老', '认知心理', '👵'),
        ('02-长老会/06-刘长老.md', '刘长老', '工程实践', '👴'),
    ]
    # 弟子
    disciple_files = [
        ('03-弟子代表/01-板栗师姐.md', '板栗师姐', '锦鲤长公主', '👸'),
        ('03-弟子代表/02-口天师兄.md', '口天师兄', '破境真人', '👨'),
        ('03-弟子代表/01-外门/萧鲤.md', '萧鲤', '双主角之一', '👨'),
    ]
    # 反派
    villain_files = [
        ('04-反派/01-逻辑中枢0.md', '逻辑中枢0', '硅基首领', '🤖'),
        ('04-反派/02-堕渊者.md', '堕渊者', '暗黑锦鲤', '👿'),
        ('04-反派/03-暗黑鲤鱼帮.md', '暗黑鲤鱼帮', '反派组织', '⛓️'),
        ('04-反派/04-TBOIer.md', 'TBOIer', '硅基叛徒', '💾'),
    ]
    
    all_char_files = [('01-宗主', f) for f in master_files] + [('02-长老会', f) for f in elder_files] + [('03-弟子代表', f) for f in disciple_files] + [('04-反派', f) for f in villain_files]
    
    for subdir, (rel_path, title, desc, icon) in all_char_files:
        md_path = os.path.join(MD_DIR, '02-人物', rel_path)
        if os.path.exists(md_path):
            output_path = os.path.join(OUTPUT_DIR, 'characters', os.path.basename(rel_path).replace('.md', '.html'))
            generate_page(md_path, output_path, title, f'{icon} {title}', desc,
                         '<a href="characters/index.html">人物</a> <span class="separator">›</span>', title, depth=1)
            char_items.append({'href': os.path.basename(rel_path).replace('.md', '.html'), 'title': title, 'desc': desc, 'icon': icon, 'tags': []})
    
    generate_module_index('人物', 'characters', os.path.join(OUTPUT_DIR, 'characters'), char_items, depth=1)
    
    # 3. 地点模块
    print("生成 地点...")
    location_files = [
        ('01-锦鲤池.md', '锦鲤池', '灵根觉醒之地', '🌊'),
        ('02-灵码头.md', '灵码头', '弟子接收处', '⚓'),
        ('03-藏经阁.md', '藏经阁', '功法典籍', '📚'),
        ('04-魔法森林.md', '魔法森林', '实战修炼', '🌲'),
        ('05-传送阵.md', '传送阵', '快速移动', '✨'),
        ('06-炼丹房.md', '炼丹房', '丹药炼制', '⚗️'),
        ('07-防御阵法.md', '防御阵法', '抵御外敌', '🛡️'),
        ('08-疗愈院.md', '疗愈院', '医疗救治', '💊'),
        ('09-闭关洞府.md', '闭关洞府', '高强度修炼', '⛰️'),
        ('10-天机阁.md', '天机阁', '监测情报', '🔭'),
        ('11-血脉堂.md', '血脉堂', '双亲认知提升', '👨‍👩‍👧'),
        ('12-天道榜.md', '天道榜', '弟子排名', '📊'),
    ]
    
    loc_items = []
    for filename, title, desc, icon in location_files:
        md_path = os.path.join(MD_DIR, '03-地点', filename)
        if os.path.exists(md_path):
            output_path = os.path.join(OUTPUT_DIR, 'locations', filename.replace('.md', '.html'))
            generate_page(md_path, output_path, title, f'{icon} {title}', desc,
                         '<a href="locations/index.html">地点</a> <span class="separator">›</span>', title, depth=1)
            loc_items.append({'href': filename.replace('.md', '.html'), 'title': title, 'desc': desc, 'icon': icon, 'tags': []})
    
    generate_module_index('地点', 'locations', os.path.join(OUTPUT_DIR, 'locations'), loc_items, depth=1)
    
    # 4. 教学理念模块
    print("生成 教学理念...")
    philo_files = [
        ('01-祖传原理图.md', '祖传原理图', '可视化教学', '📐'),
        ('02-乾坤大挪移.md', '乾坤大挪移', '时空权衡', '⚖️'),
        ('03-降维打击.md', '降维打击', '化繁为简', '📉'),
        ('04-现代学习方法映射.md', '现代学习方法映射', '学习方法', '🧠'),
    ]
    
    philo_items = []
    for filename, title, desc, icon in philo_files:
        md_path = os.path.join(MD_DIR, '08-教学理念', filename)
        if os.path.exists(md_path):
            output_path = os.path.join(OUTPUT_DIR, 'philosophy', filename.replace('.md', '.html'))
            generate_page(md_path, output_path, title, f'{icon} {title}', desc,
                         '<a href="philosophy/index.html">理念</a> <span class="separator">›</span>', title, depth=1)
            philo_items.append({'href': filename.replace('.md', '.html'), 'title': title, 'desc': desc, 'icon': icon, 'tags': []})
    
    generate_module_index('教学理念', 'philosophy', os.path.join(OUTPUT_DIR, 'philosophy'), philo_items, depth=1)
    
    print(f"\n=== 生成完成 ===")
    print(f"总览页面: {OUTPUT_DIR}/index.html")
    print(f"世界观: {len(world_items)} 页")
    print(f"人物: {len(char_items)} 页")
    print(f"地点: {len(loc_items)} 页")
    print(f"教学理念: {len(philo_items)} 页")


if __name__ == '__main__':
    main()
