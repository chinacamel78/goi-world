import os
import re

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界'

def get_pic_path(html_path):
    rel = os.path.relpath(html_path, BASE_DIR)
    parts = rel.replace(chr(92), '/').split('/')
    if len(parts) >= 2:
        module = parts[0]
        rest = '/'.join(parts[1:])
        pic_path = rest.replace('.html', '.png')
        depth = len(parts) - 1
        prefix = '../' * depth
        return prefix + 'pic/' + module + '/' + pic_path
    return None

def get_prompt_path(html_path):
    rel = os.path.relpath(html_path, BASE_DIR)
    parts = rel.replace(chr(92), '/').split('/')
    if len(parts) >= 2:
        module = parts[0]
        rest = '/'.join(parts[1:])
        prompt_path = rest.replace('.html', '.prompt.txt')
        depth = len(parts) - 1
        prefix = '../' * depth
        return prefix + 'pic/' + module + '/' + prompt_path
    return None

def process_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'ai-art-section' in content:
        return False
    
    pic_path = get_pic_path(html_path)
    if not pic_path:
        return False
    
    prompt_path = get_prompt_path(html_path)
    
    img_html = """
    <div class="ai-art-section">
      <h3 class="section-title">
        <span class="icon">🎨</span>
        <span>AI Art</span>
      </h3>
      <div style="text-align: center; margin: 2rem 0;">
        <img src=""" + pic_path + """ alt="AI Art" class="ai-art-image" style="max-width: 100%; border-radius: 16px; border: 1px solid var(--border-glow); box-shadow: 0 0 30px rgba(0, 240, 255, 0.1);">
        <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 1rem;">
          <a href=""" + prompt_path + """ style="color: var(--cyan-primary);" download>Download AI Prompt</a> — Use this prompt in Midjourney, DALL-E, or Stable Diffusion to generate a real AI image.
        </p>
      </div>
    </div>
"""
    
    if '<div class="divider"></div>' in content:
        parts = content.split('<div class="divider"></div>', 1)
        if len(parts) == 2:
            new_content = parts[0] + '<div class="divider"></div>' + img_html + parts[1]
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in ['assets', '.git', '锦鲤界-backup', 'pic']]
        for f in files:
            if f.endswith('.html') and f != 'index.html':
                html_path = os.path.join(root, f)
                if process_html(html_path):
                    count += 1
    
    print('Inserted AI art sections into %d HTML files' % count)

if __name__ == '__main__':
    main()
