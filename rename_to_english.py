#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量将中文文件名重命名为英文，并更新所有 HTML 中的链接
"""
import os
import re
import shutil

BASE_DIR = r'D:/Data/-= AI/20260700 - 锦鲤宗宗门建设/01 - IP建设/锦鲤界'

# 中文到英文的映射（手动维护的常用词映射）
CN_TO_EN = {
    '两界战争总纲': 'world-war-overview',
    '灵码界设定': 'lingma-world-setting',
    '锦鲤宗宗旨': 'koi-sect-purpose',
    '核心冲突': 'core-conflict',
    '天赋体系总纲': 'talent-system-overview',
    '世界观': 'world',
    '人物': 'characters',
    '地点': 'locations',
    '功法': 'techniques',
    '法宝': 'artifacts',
    '主线': 'story',
    '支线': 'side-stories',
    '理念': 'philosophy',
    '总纲': 'overview',
    '基础功法': 'basic-techniques',
    '进阶功法': 'advanced-techniques',
    '高阶功法': 'elite-techniques',
    '基础法宝': 'basic-artifacts',
    '进阶法宝': 'advanced-artifacts',
    '高阶法宝': 'elite-artifacts',
    '阶段一': 'stage-1',
    '阶段二': 'stage-2',
    '阶段三': 'stage-3',
    '阶段四': 'stage-4',
    '阶段五': 'stage-5',
    '阶段六': 'stage-6',
    '阶段七': 'stage-7',
    '阶段八': 'stage-8',
    '灵气初引诀': 'spirit-introduction',
    '岔路抉择术': 'path-choice',
    '吐纳周天功': 'circulation-breath',
    '百穴储灵阵': 'meridian-storage',
    '字符流转法': 'char-stream',
    '分身化影术': 'clone-shadow',
    '镜花水月步': 'mirror-water-step',
    '灵气聚合体': 'spirit-aggregate',
    '灵气引丝术': 'spirit-thread',
    '万象容器诀': 'universal-container',
    '穷举乾坤术': 'exhaustive-search',
    '照本宣科功': 'template-copy',
    '当下最优禅': 'greedy-choice',
    '前因后果诀': 'cause-effect',
    '折半藏龙术': 'binary-search',
    '灵力翻倍增': 'spirit-double',
    '灵气聚气术': 'spirit-accumulate',
    '灵力波动法': 'spirit-wave',
    '毫厘算盘': 'precise-abacus',
    '幽径探龙诀': 'deep-path-dragon',
    '涟漪寻源法': 'ripple-source',
    '洪水漫延术': 'flood-fill',
    '吐纳归元诀': 'breath-return',
    '择极而取术': 'extreme-select',
    '插针入缝法': 'insert-needle',
    '统计归位术': 'counting-sort',
    '子问题涅槃经': 'subproblem-nirvana',
    '芥子纳须弥诀': 'mustard-seed',
    '区间守望阵': 'interval-guard',
    '阵图绘制术': 'graph-draw',
    '质数天书': 'prime-book',
    '血脉溯源法': 'bloodline-trace',
    '筛灵网': 'sieve-spirit',
    '组合乾坤术': 'combination-universe',
    '数基转换诀': 'base-convert',
    '灵峰堆叠术': 'peak-stack',
    '树状灵蕨': 'tree-fern',
    '字典灵树': 'dict-tree',
    '哈希灵瓮': 'hash-urn',
    '优先灵钵': 'priority-bowl',
    '并查罗盘': 'union-find',
    '线段守望塔': 'segment-watchtower',
    '单调灵尺': 'monotone-ruler',
    '双端灵桥': 'deque-bridge',
    '分形归元术': 'fractal-return',
    '分形斩': 'fractal-slash',
    '灵峰崩塌诀': 'peak-collapse',
    '分桶归位术': 'bucket-sort',
    '分而治之诀': 'divide-conquer',
    '扫线探阵术': 'sweep-line',
    '化繁为简诀': 'simplify',
    '记忆回光术': 'memory-recall',
    'pruning灵刃': 'pruning-blade',
    '双向涟漪术': 'bidirectional-ripple',
    '逐层探渊术': 'layer-probe',
    '灵觉引导术': 'spirit-guide',
    'KMP灵针': 'kmp-needle',
    '回文镜像术': 'palindrome-mirror',
    '步步为营术': 'step-camp',
    '弹性探路术': 'elastic-probe',
    '队列探路术': 'queue-probe',
    '全图推演术': 'full-graph-deduce',
    '蔓延连山术': 'spread-mountain',
    '先易后难术': 'easy-first',
    '拓扑排阵术': 'topo-sort',
    '一笔画阵术': 'one-stroke',
    '阴阳判阵术': 'yin-yang-judge',
    '强连聚气术': 'strong-connect',
    '断脉寻术': 'disconnected-seek',
    '树脉诊断术': 'tree-diagnosis',
    '树脉差分术': 'tree-diff',
    '血脉倍增术': 'bloodline-double',
    '集阵控制术': 'set-control',
    '图影同构术': 'graph-isomorphism',
    '插头连通术': 'plug-connect',
    '斜率加速术': 'slope-accelerate',
    '四边不等术': 'quad-inequality',
    '单调加速术': 'monotone-accelerate',
    '位置判定术': 'position-judge',
    '界尺量天功': 'boundary-measure',
    '凸界天罡罩': 'convex-hull',
    '半平面交阵术': 'half-plane-intersect',
    '旋转卡壳术': 'rotating-calipers',
    '扫线探阵术': 'sweep-line-geo',
    '圆界交阵术': 'circle-intersect',
    '三维量天术': '3d-measure',
    '曼哈顿连山术': 'manhattan-mountain',
    '时频转生咒': 'fft-transform',
    '数论转生咒': 'number-theory-transform',
    '原根天书': 'primitive-root',
    '大步小步术': 'baby-step-giant-step',
    '狄利克雷合阵术': 'dirichlet-convolution',
    '莫比乌斯反演术': 'mobius-inversion',
    'Burnside对称术': 'burnside-symmetry',
    '斯特林分阵术': 'stirling-partition',
    'Prüfer树码术': 'prufer-code',
    '线性基阵术': 'linear-basis',
    '矩阵树定理': 'matrix-tree',
    'Nim取石术': 'nim-game',
    'Sprague-Grundy术': 'sprague-grundy',
    '概率天书': 'probability-book',
    '贝叶斯推断术': 'bayesian-inference',
    '马尔可夫链术': 'markov-chain',
    '单纯形优化术': 'simplex-optimize',
    '信息熵天书': 'information-entropy',
    '描述复杂度术': 'descriptive-complexity',
    '通讯复杂度术': 'communication-complexity',
    '构造创世术': 'construct-creation',
    '平衡规划术': 'balance-plan',
    '离线回溯术': 'offline-rollback',
    '分块灵阵术': 'block-spirit',
    '分而治之诀': 'divide-conquer-advanced',
    '数组锁链': 'array-chain',
    '链表灵蛇': 'list-snake',
    '栈山盾': 'stack-shield',
    '队列长河': 'queue-river',
    '洛谷灵牌': 'luogu-spirit',
    '玲珑编译盏': 'compiler-lantern',
    '万象调试镜': 'debug-mirror',
    '代码玉简': 'code-jade',
    '防御罗盘': 'defense-compass',
    'STL万象容器': 'stl-container',
    '二叉仙树': 'binary-tree',
    '主席时光殿': 'chairman-time',
    '后缀轮回盘': 'suffix-reincarnation',
    '网络运河图': 'network-canal',
    '可持久化字典': 'persistent-dict',
    'AC猎字符阵': 'ac-automaton',
    'LCT灵树': 'lct-tree',
    'k维灵树': 'kdtree',
    '虚灵树': 'virtual-tree',
    '左偏灵堆': 'leftist-heap',
    '二项灵堆': 'binomial-heap',
    '时光字典树': 'time-trie',
    '扩展灵针': 'extend-needle',
    '运河分流策': 'canal-diversion',
    '树形连山术': 'tree-mountain',
    '二态判定术': '2sat-judge',
    '基环灵树': 'base-ring-tree',
    '通用姻缘术': 'general-marriage',
    '匈牙利姻缘术': 'hungarian-marriage',
    'KM最优姻缘术': 'km-optimal-marriage',
    '双主角人设': 'dual-protagonist',
    '主线剧情大纲': 'main-story-outline',
    '锦鲤成长之路': 'koi-growth-path',
    '锦鲤之路': 'koi-path',
    '双主角版': 'dual-protagonist-edition',
    '灵根觉醒': 'spirit-root-awakening',
    '欢喜冤家': 'happy-enemy',
    '祖传原理图': 'ancestral-principle',
    '翻转课堂': 'flipped-classroom',
    '同名阴影': 'same-name-shadow',
    '演武场初战': 'arena-first-battle',
    '燃香计时': 'incense-timer',
    'GESP战场': 'gesp-battlefield',
    '赛后复盘': 'post-match-review',
    '二分与直觉的冲突': 'binary-intuition-conflict',
    'DFS的至暗时刻': 'dfs-dark-moment',
    '深夜对练': 'late-night-practice',
    'CSP-J破阵': 'csp-j-breakthrough',
    'DP的瓶颈': 'dp-bottleneck',
    '速成诱惑': 'quick-temptation',
    '信任危机': 'trust-crisis',
    '救赎之路': 'redemption-path',
    'CSP-S扛劫': 'csp-s-tribulation',
    '堕渊者的镜像之战': 'fallen-mirror-battle',
    '研经阁的火花': 'study-tower-spark',
    'NOIP前夜': 'noip-eve',
    '信任的考试': 'trust-exam',
    '心动': 'heartbeat',
    '新队友': 'new-teammate',
    '嫉妒的考试': 'jealousy-exam',
    '云澈的坦诚': 'yunce-honesty',
    '合道之战': 'dao-unity-battle',
    '正面对决': 'head-on-battle',
    '两个锦瑟': 'two-jinse',
    '赛前的情报': 'pre-match-intel',
    '捷径的诱惑': 'shortcut-temptation',
    '考场上的抉择': 'exam-choice',
    '真相大白': 'truth-revealed',
    '同样的选择': 'same-choice',
    '不同的答案': 'different-answer',
    '终极降临': 'ultimate-arrival',
    '表白': 'confession',
    '终极战场': 'ultimate-battlefield',
    '共存': 'coexistence',
    '传承': 'inheritance',
    '堕渊者的redemption': 'fallen-redemption',
    '锦瑟': 'jinse',
    '萧鲤': 'xiaoli',
    '堕渊者': 'fallen-one',
    '暗黑鲤鱼帮': 'dark-koi-gang',
    'TBOIer': 'tboier',
    '灵码真人': 'lingma-master',
    '开心真人': 'kaixin-master',
    '启元真人': 'qiyuan-master',
    '齐鲁真人': 'qilu-master',
    '静渊真人': 'jingyuan-master',
    '邓长老': 'deng-elder',
    '刘长老': 'liu-elder',
    '板栗师姐': 'banli-senior',
    '口天师兄': 'koutian-senior',
    '锦鲤池': 'koi-pond',
    '灵码头': 'spirit-dock',
    '藏经阁': 'scripture-tower',
    '魔法森林': 'magic-forest',
    '传送阵': 'teleport-array',
    '炼丹房': 'alchemy-room',
    '防御阵法': 'defense-formation',
    '疗愈院': 'healing-hall',
    '闭关洞府': 'seclusion-cave',
    '天机阁': 'celestial-tower',
    '血脉堂': 'bloodline-hall',
    '天道榜': 'heaven-rank',
    '祖传原理图': 'ancestral-diagram',
    '乾坤大挪移': 'universe-shift',
    '降维打击': 'dimension-strike',
    '现代学习方法映射': 'modern-learning-map',
    'Camel的函数组': 'camel-function-group',
    '魔法森林': 'magic-forest-task',
    '糖果罐': 'candy-jar',
    '追逐锦鲤': 'chase-koi',
    '三人行': 'three-person',
    '节俭的帮主': 'frugal-leader',
    '学堂建设规划': 'school-planning',
    '暗黑鲤鱼帮防御弱点': 'dark-koi-weakness',
    '防御': 'defense',
    '酷刑': 'torture',
    '膜拜': 'worship',
    '优待精英弟子': 'elite-preferential',
    '预选精英弟子': 'elite-preselect',
    '甄选精英弟子': 'elite-select',
    '疗愈精英弟子': 'elite-healing',
    '列队': 'line-up',
    '裂变': 'fission',
    '挑战': 'challenge',
    '逃脱': 'escape',
    '比赛': 'competition',
    '试炼': 'trial',
    '连接': 'connection',
    '收集': 'collection',
    '雪白堂': 'snow-white-hall',
    '锦里街': 'jinli-street',
}

def pinyin_name(name):
    """将中文文件名转为英文/拼音"""
    # 先去除扩展名
    ext = ''
    if '.' in name:
        ext = name[name.rfind('.'):]
        name = name[:name.rfind('.')]
    
    # 去除常见前缀数字
    prefix = ''
    m = re.match(r'^(\d+[-_])', name)
    if m:
        prefix = m.group(1)
        name = name[len(prefix):]
    
    # 去除常见的编号前缀（如 C-01_）
    m2 = re.match(r'^([A-Z]-\d+[-_])', name)
    if m2:
        prefix = m2.group(1)
        name = name[len(prefix):]
    
    # 查找映射
    if name in CN_TO_EN:
        return prefix + CN_TO_EN[name] + ext
    
    # 如果没有映射，尝试用拼音库
    try:
        from pypinyin import lazy_pinyin
        py = lazy_pinyin(name)
        return prefix + '-'.join(py) + ext
    except ImportError:
        # 如果 pypinyin 不可用，直接返回原文件名（但去除中文）
        # 用 UUID 或简单替换
        safe = re.sub(r'[^\w\-]', '', name)
        if not safe:
            safe = 'item'
        return prefix + safe + ext

def collect_all_files():
    """收集所有需要重命名的文件"""
    html_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # 跳过 assets
        if 'assets' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
    return html_files

def main():
    # 检查是否有 pypinyin
    has_pypinyin = False
    try:
        import pypinyin
        has_pypinyin = True
        print("Using pypinyin for Chinese name conversion")
    except ImportError:
        print("pypinyin not available, using manual mapping")
    
    files = collect_all_files()
    print(f"Found {len(files)} HTML files to process")
    
    # 第一遍：构建映射表
    rename_map = {}  # old_path -> new_path
    for old_path in files:
        rel = os.path.relpath(old_path, BASE_DIR)
        parts = rel.split(os.sep)
        
        # 转换每个目录名和文件名
        new_parts = []
        for part in parts:
            # 检查目录名是否包含中文
            if re.search(r'[\u4e00-\u9fff]', part):
                new_part = pinyin_name(part)
            else:
                new_part = part
            new_parts.append(new_part)
        
        new_rel = os.path.join(*new_parts)
        new_path = os.path.join(BASE_DIR, new_rel)
        rename_map[old_path] = new_path
    
    print(f"Built rename map for {len(rename_map)} files")
    
    # 创建所有新目录
    for new_path in rename_map.values():
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
    
    # 第二遍：读取所有 HTML 内容，替换链接
    # 先建立反向映射：old_rel -> new_rel
    old_to_new_rel = {}
    for old_path, new_path in rename_map.items():
        old_rel = os.path.relpath(old_path, BASE_DIR).replace('\\', '/')
        new_rel = os.path.relpath(new_path, BASE_DIR).replace('\\', '/')
        old_to_new_rel[old_rel] = new_rel
    
    # 处理每个文件
    for old_path, new_path in rename_map.items():
        with open(old_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换所有 href 和 src 中的链接
        # 策略：在文件中搜索所有包含中文路径的 href
        for old_rel, new_rel in old_to_new_rel.items():
            # 替换 href="..." 中的路径
            content = content.replace('href="' + old_rel + '"', 'href="' + new_rel + '"')
            content = content.replace("href='" + old_rel + "'", "href='" + new_rel + "'")
            # 替换 href="../..." 中的路径
            # 这里需要更复杂的处理，先简化
        
        # 写入新文件
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # 第三遍：删除旧文件
    for old_path in rename_map.keys():
        if os.path.exists(old_path) and old_path not in rename_map.values():
            os.remove(old_path)
    
    # 清理空目录
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        if 'assets' not in root:
            for d in dirs:
                dir_path = os.path.join(root, d)
                if os.path.exists(dir_path) and not os.listdir(dir_path):
                    os.rmdir(dir_path)
    
    print("Rename complete!")
    
    # 验证
    new_files = collect_all_files()
    print(f"After rename: {len(new_files)} HTML files")
    
    # 检查是否还有中文文件名
    has_cn = False
    for f in new_files:
        rel = os.path.relpath(f, BASE_DIR)
        if re.search(r'[\u4e00-\u9fff]', rel):
            has_cn = True
            print(f"  Still has CN: {rel}")
    
    if not has_cn:
        print("All files renamed to English successfully!")

if __name__ == '__main__':
    main()
