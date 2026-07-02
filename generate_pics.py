#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为锦鲤界所有页面生成AI图像提示词和占位图
"""

import os
import re
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界'
PIC_DIR = os.path.join(BASE_DIR, 'pic')

# 赛博修仙风格配色
COLORS = {
    'bg': '#0a0e1a',
    'border': '#00f0ff',
    'gold': '#ffd700',
    'text': '#e0f0ff',
    'dim': '#5a7a8a',
}

# 基础AI图像提示词模板
PROMPT_TEMPLATES = {
    'world': {
        'base': 'Epic cyber-xianxia fantasy scene, (sacred koi fish swimming through digital code streams), cyan and gold neon lights, dark mysterious background with binary code falling like rain, ancient Chinese runes glowing in holographic blue, cinematic lighting, ultra detailed, 8k quality, concept art, artstation trending',
    },
    'characters': {
        'base': 'Portrait of a cultivator character, cyber-xianxia style, glowing spirit aura, holographic data streams around body, traditional Chinese robes with circuit patterns, cyan and gold color palette, ethereal lighting, anime style, ultra detailed, 8k, character concept art',
    },
    'locations': {
        'base': 'Vast sacred cultivation location, cyber-xianxia architecture, ancient Chinese buildings merged with holographic technology, floating islands in digital mist, cyan and gold lighting, mysterious atmosphere, cinematic composition, ultra detailed, 8k, environment concept art',
    },
    'techniques': {
        'base': 'Dynamic visualization of algorithm magic, glowing energy lines forming data structures, ancient Chinese talisman merging with digital code, cyan and gold lightning effects, power burst, action scene, ultra detailed, 8k, special effects art',
    },
    'artifacts': {
        'base': 'Sacred magical artifact, glowing with cyber-xianxia energy, intricate mechanical details mixed with ancient Chinese jade carvings, floating in air with holographic aura, cyan and gold lighting, product photography style, ultra detailed, 8k, prop concept art',
    },
    'story': {
        'base': 'Dramatic scene from a cultivation story, two young cultivators facing each other, epic battle or intimate moment, cyber-xianxia world background, emotional lighting, cinematic composition, movie still, ultra detailed, 8k, storyboard art',
    },
    'side-stories': {
        'base': 'Adventurous scene in a fantasy training ground, young cultivators practicing magic, beautiful landscape with ancient Chinese architecture, vibrant colors, hopeful atmosphere, anime style, ultra detailed, 8k, illustration art',
    },
    'philosophy': {
        'base': 'Abstract visualization of cultivation wisdom, mind expanding into cosmic knowledge, glowing neural pathways, ancient Chinese calligraphy floating in digital space, golden enlightenment rays, meditation scene, ultra detailed, 8k, visionary art',
    },
}

def extract_title(html_path):
    """从HTML文件中提取标题"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 hero-title
    match = re.search(r'<h1 class="hero-title">(.*?)</h1>', content, re.DOTALL)
    if match:
        title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        return title
    
    # 提取 title 标签
    match = re.search(r'<title>(.*?) —', content)
    if match:
        return match.group(1).strip()
    
    return os.path.basename(html_path).replace('.html', '')

def extract_description(html_path):
    """从HTML文件中提取描述"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'<p class="hero-subtitle">(.*?)</p>', content, re.DOTALL)
    if match:
        desc = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        return desc
    
    return ''

def generate_prompt(module, title, desc):
    """根据模块和标题生成AI图像提示词"""
    base = PROMPT_TEMPLATES.get(module, PROMPT_TEMPLATES['world'])['base']
    
    # 根据标题提取关键词增强提示词
    keywords = title.replace(' ', ', ').replace('_', ', ').replace('-', ', ')
    
    # 构建完整提示词
    prompt = f"""{base}

Specific subject: {title}
Context: {desc}

Enhanced details: {keywords}, glowing with spiritual energy, intricate patterns, mysterious atmosphere, high quality, masterpiece

--ar 16:9 --v 6 --style raw
"""
    return prompt

def generate_placeholder(title, output_path, width=800, height=450):
    """生成风格化的占位图"""
    # 创建深色背景
    img = Image.new('RGB', (width, height), color=COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # 绘制边框光效
    border_width = 3
    for i in range(border_width):
        draw.rectangle(
            [i, i, width-1-i, height-1-i],
            outline=COLORS['border'],
            width=1
        )
    
    # 绘制角落装饰
    corner_size = 30
    for x, y in [(0, 0), (width-corner_size, 0), (0, height-corner_size), (width-corner_size, height-corner_size)]:
        draw.rectangle([x, y, x+5, y+5], fill=COLORS['gold'])
    
    # 绘制渐变光晕（模拟）
    for r in range(100, 0, -5):
        alpha = int(20 - r * 0.15)
        if alpha > 0:
            draw.ellipse([width//2-r, height//2-r, width//2+r, height//2+r], 
                         outline=f'#{alpha:02x}{alpha+50:02x}{alpha+100:02x}')
    
    # 绘制文字
    try:
        # 尝试使用系统字体
        font_large = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 36)
        font_small = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 绘制标题
    title = title[:30] if len(title) > 30 else title
    
    # 计算文字位置（居中）
    bbox = draw.textbbox((0, 0), title, font=font_large)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2 - 20
    
    # 绘制文字阴影
    draw.text((x+2, y+2), title, fill='#000000', font=font_large)
    # 绘制文字
    draw.text((x, y), title, fill=COLORS['gold'], font=font_large)
    
    # 绘制提示文字
    sub_text = "AI Generated Image Placeholder"
    bbox = draw.textbbox((0, 0), sub_text, font=font_small)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    y = height - 60
    draw.text((x, y), sub_text, fill=COLORS['dim'], font=font_small)
    
    # 保存图片
    img.save(output_path, 'PNG')
    return output_path

def process_module(module_name):
    """处理单个模块"""
    module_dir = os.path.join(BASE_DIR, module_name)
    pic_module_dir = os.path.join(PIC_DIR, module_name)
    
    if not os.path.exists(module_dir):
        return 0
    
    count = 0
    for root, dirs, files in os.walk(module_dir):
        for f in files:
            if f.endswith('.html') and f != 'index.html':
                html_path = os.path.join(root, f)
                
                # 获取相对路径（从模块目录开始）
                rel_dir = os.path.relpath(os.path.dirname(html_path), module_dir)
                
                # 构建 pic 目录中的输出路径
                if rel_dir == '.':
                    output_dir = pic_module_dir
                else:
                    output_dir = os.path.join(pic_module_dir, rel_dir)
                os.makedirs(output_dir, exist_ok=True)
                
                # 输出文件名
                basename = os.path.splitext(f)[0]
                img_path = os.path.join(output_dir, basename + '.png')
                prompt_path = os.path.join(output_dir, basename + '.prompt.txt')
                
                # 提取标题和描述
                title = extract_title(html_path)
                desc = extract_description(html_path)
                
                # 生成提示词
                prompt = generate_prompt(module_name, title, desc)
                with open(prompt_path, 'w', encoding='utf-8') as fp:
                    fp.write(prompt)
                
                # 生成占位图
                generate_placeholder(title, img_path)
                
                count += 1
    
    return count

def main():
    print("=== Generating AI prompts and placeholder images ===\n")
    
    total = 0
    for module in ['world', 'characters', 'locations', 'techniques', 'artifacts', 'story', 'side-stories', 'philosophy']:
        count = process_module(module)
        total += count
        print(f"Module {module}: {count} prompts + images generated")
    
    print(f"\n=== Total: {total} prompts and placeholder images generated ===")
    print(f"Output directory: {PIC_DIR}")
    print("\nUsage:")
    print("1. Each .prompt.txt contains a Midjourney/Stable Diffusion prompt")
    print("2. Each .png is a placeholder image showing the layout position")
    print("3. Use the prompts in Midjourney/DALL-E/Stable Diffusion to generate real images")
    print("4. Replace the .png files with your generated AI images")

if __name__ == '__main__':
    main()
