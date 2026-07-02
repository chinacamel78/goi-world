import os
import re
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界'
PIC_DIR = os.path.join(BASE_DIR, 'pic')

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_cyber_art(title, output_path, width=1024, height=576):
    """生成赛博修仙风格的艺术图"""
    # 深色背景
    img = Image.new('RGB', (width, height), '#0a0e1a')
    draw = ImageDraw.Draw(img)
    
    # 随机种子确保同标题生成相同图片
    random.seed(title)
    
    # 1. 渐变背景
    for y in range(height):
        ratio = y / height
        r = int(10 + ratio * 5)
        g = int(14 + ratio * 10)
        b = int(26 + ratio * 15)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 2. 随机光晕效果
    num_glows = random.randint(3, 6)
    for _ in range(num_glows):
        cx = random.randint(100, width - 100)
        cy = random.randint(100, height - 100)
        max_r = random.randint(80, 200)
        color = random.choice([
            (0, 240, 255),   # cyan
            (255, 215, 0),   # gold
            (153, 102, 255), # purple
            (0, 255, 128),   # green
        ])
        for r in range(max_r, 0, -2):
            alpha = int(30 * (1 - r / max_r))
            if alpha > 0:
                rr = max(0, min(255, color[0] + alpha))
                gg = max(0, min(255, color[1] + alpha))
                bb = max(0, min(255, color[2] + alpha))
                draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(rr, gg, bb))
    
    # 3. 绘制线条网格
    line_color = (0, 240, 255, 30)
    for i in range(0, width, 80):
        draw.line([(i, 0), (i, height)], fill=(0, 30, 40), width=1)
    for i in range(0, height, 80):
        draw.line([(0, i), (width, i)], fill=(0, 30, 40), width=1)
    
    # 4. 绘制粒子/星星
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(100, 255)
        color = random.choice([
            (0, brightness, brightness),
            (brightness, brightness, 0),
            (brightness, brightness, brightness),
        ])
        draw.ellipse([x, y, x+size, y+size], fill=color)
    
    # 5. 绘制波浪线
    for wave_idx in range(3):
        y_base = height // 2 + (wave_idx - 1) * 80
        points = []
        for x in range(0, width, 5):
            y = y_base + math.sin(x * 0.01 + wave_idx * 2) * 30 + math.sin(x * 0.03) * 10
            points.append((x, int(y)))
        if len(points) > 1:
            color = random.choice([(0, 240, 255), (255, 215, 0), (153, 102, 255)])
            for i in range(len(points) - 1):
                alpha = int(150 * (1 - abs(i - len(points)/2) / (len(points)/2)))
                if alpha > 20:
                    c = (max(0, min(255, color[0] + alpha - 150)),
                         max(0, min(255, color[1] + alpha - 150)),
                         max(0, min(255, color[2] + alpha - 150)))
                    draw.line([points[i], points[i+1]], fill=c, width=2)
    
    # 6. 绘制边框发光
    border_width = 3
    for i in range(border_width):
        draw.rectangle([i, i, width-1-i, height-1-i], outline=(0, 240, 255), width=1)
    
    # 7. 角落装饰
    corner_size = 40
    for x, y in [(0, 0), (width-corner_size, 0), (0, height-corner_size), (width-corner_size, height-corner_size)]:
        draw.rectangle([x, y, x+6, y+6], fill=(255, 215, 0))
    
    # 8. 绘制标题文字
    try:
        font_large = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 48)
        font_small = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 标题处理
    display_title = title[:12] if len(title) > 12 else title
    
    # 计算文字位置
    bbox = draw.textbbox((0, 0), display_title, font=font_large)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2 - 30
    
    # 文字发光效果
    for offset in range(8, 0, -2):
        glow_color = (0, 240, 255, int(50 - offset * 5))
        draw.text((x, y), display_title, fill=(0, 100, 120), font=font_large)
    
    # 主文字
    draw.text((x, y), display_title, fill=(255, 215, 0), font=font_large)
    
    # 副标题
    sub_text = "Cyber-Xianxia World"
    bbox = draw.textbbox((0, 0), sub_text, font=font_small)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    y = height - 80
    draw.text((x, y), sub_text, fill=(0, 200, 220), font=font_small)
    
    # 9. 添加模糊效果使光晕更柔和
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # 保存
    img.save(output_path, 'PNG', quality=95)
    return output_path

def regenerate_all_pics():
    """重新生成所有图片"""
    count = 0
    for root, dirs, files in os.walk(PIC_DIR):
        for f in files:
            if f.endswith('.png'):
                pic_path = os.path.join(root, f)
                # 从文件名提取标题
                title = os.path.splitext(f)[0]
                title = re.sub(r'^[a-z]-\d+[-_]', '', title, flags=re.IGNORECASE)
                title = re.sub(r'^[a-z]-', '', title, flags=re.IGNORECASE)
                title = re.sub(r'[-_]', ' ', title)
                title = title.strip()
                
                generate_cyber_art(title, pic_path)
                count += 1
                
                if count % 50 == 0:
                    print(f'Generated {count} images...')
    
    print(f'\nTotal regenerated: {count} images')

if __name__ == '__main__':
    regenerate_all_pics()
