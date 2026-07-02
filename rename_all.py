#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import shutil
from pypinyin import lazy_pinyin

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界'

def to_pinyin(text):
    """将中文转为拼音，小写，用连字符连接"""
    result = []
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            py = lazy_pinyin(char)
            result.extend(py)
        elif char.isalnum() or char in '_-.':
            result.append(char.lower() if char.isalpha() else char)
        else:
            result.append('-')
    
    joined = ''.join(result)
    joined = re.sub(r'-+', '-', joined)
    joined = joined.strip('-')
    return joined

def get_new_name(path):
    """为路径生成新的英文名称"""
    basename = os.path.basename(path)
    if '.' in basename and not basename.startswith('.'):
        name, ext = basename.rsplit('.', 1)
        new_name = to_pinyin(name) + '.' + ext
    else:
        new_name = to_pinyin(basename)
    return new_name

def collect_all_items():
    """收集所有文件和目录（排除assets和.git）"""
    items = []
    for root, dirs, files in os.walk(BASE_DIR):
        # 跳过不需要处理的目录
        dirs_to_remove = []
        for d in dirs:
            if d in ['assets', '.git', '锦鲤界-backup']:
                dirs_to_remove.append(d)
        for d in dirs_to_remove:
            dirs.remove(d)
        
        # 收集目录
        for d in dirs:
            dir_path = os.path.join(root, d)
            items.append(('dir', dir_path))
        
        # 收集文件
        for f in files:
            file_path = os.path.join(root, f)
            items.append(('file', file_path))
    
    return items

def main():
    print("=== Starting rename ===\n")
    
    items = collect_all_items()
    print(f"Found {len(items)} items to process")
    
    rename_map = {}
    
    for item_type, old_path in items:
        rel_path = os.path.relpath(old_path, BASE_DIR)
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', rel_path))
        
        if not has_chinese:
            continue
        
        parts = rel_path.split(os.sep)
        new_parts = []
        for part in parts:
            if re.search(r'[\u4e00-\u9fff]', part):
                new_part = get_new_name(part)
                if not new_part:
                    new_part = 'item'
            else:
                new_part = part
            new_parts.append(new_part)
        
        new_rel_path = os.path.join(*new_parts)
        new_path = os.path.join(BASE_DIR, new_rel_path)
        rename_map[old_path] = new_path
    
    print(f"Items to rename: {len(rename_map)}")
    
    # Sort by depth (deepest first)
    sorted_items = sorted(rename_map.items(), key=lambda x: x[0].count(os.sep), reverse=True)
    
    # Create all new directories first
    for old_path, new_path in sorted_items:
        if os.path.isdir(old_path):
            os.makedirs(new_path, exist_ok=True)
    
    # Process files
    for old_path, new_path in sorted_items:
        if os.path.isfile(old_path):
            with open(old_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace all Chinese paths in content
            for old_ref, new_ref in rename_map.items():
                old_rel = os.path.relpath(old_ref, BASE_DIR).replace('\\', '/')
                new_rel = os.path.relpath(new_ref, BASE_DIR).replace('\\', '/')
                
                content = content.replace('href="' + old_rel + '"', 'href="' + new_rel + '"')
                content = content.replace("href='" + old_rel + "'", "href='" + new_rel + "'")
                content = content.replace('src="' + old_rel + '"', 'src="' + new_rel + '"')
                content = content.replace("src='" + old_rel + "'", "src='" + new_rel + "'")
            
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    # Remove old files
    for old_path, new_path in sorted_items:
        if os.path.isfile(old_path) and old_path != new_path:
            os.remove(old_path)
    
    # Remove old directories
    for old_path, new_path in sorted_items:
        if os.path.isdir(old_path) and old_path != new_path:
            try:
                os.rmdir(old_path)
            except OSError:
                pass
    
    # Verify
    print("\n=== Verification ===")
    remaining_cn = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for d in dirs:
            if d in ['assets', '.git', '锦鲤界-backup']:
                continue
            if re.search(r'[\u4e00-\u9fff]', d):
                remaining_cn += 1
                print(f"  CN dir: {d}")
        for f in files:
            if re.search(r'[\u4e00-\u9fff]', f):
                remaining_cn += 1
                print(f"  CN file: {f}")
    
    if remaining_cn == 0:
        print("All filenames renamed successfully!")
    else:
        print(f"Warning: {remaining_cn} Chinese items remaining")
    
    # Verify links
    print("\n=== Link verification ===")
    issues = []
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                matches = re.findall(r'href=["\'](.*?)["\']', content)
                for m in matches:
                    if re.search(r'[\u4e00-\u9fff]', m):
                        issues.append((os.path.relpath(path, BASE_DIR), m))
    
    if issues:
        print(f"Warning: {len(issues)} Chinese links remaining")
        for filepath, href in issues[:5]:
            print(f"  {filepath}: {href}")
    else:
        print("All links updated successfully!")
    
    # Count
    html_count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith('.html'):
                html_count += 1
    
    print(f"\nTotal HTML files: {html_count}")

if __name__ == '__main__':
    main()
