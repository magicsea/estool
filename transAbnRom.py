import os
import sys
import io
import xml.etree.ElementTree as ET  

# 确保stdout存在且可访问
if sys.stdout and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
else:
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')

def parse_gamelist_xml(gamelist_path):
    """
    解析gamelist.xml文件，提取指定元素
    
    参数:
        gamelist_path: gamelist.xml文件路径
        
    返回:
        list: 包含提取元素的字典列表
    """
    game_items = []
    try:
        # 尝试多种编码方式
        for encoding in ['utf-8', 'gbk', 'utf-16']:
            try:
                with open(gamelist_path, 'r', encoding=encoding) as f:
                    tree = ET.parse(f)
                break
            except UnicodeDecodeError:
                continue
        
        root = tree.getroot()
        
        # 遍历所有game和folder元素
        for element in root.findall('*'):
            item = {}
            
            # 提取path
            path = element.find('path')
            if path is not None:
                item['path'] = path.text
            
            # 提取name
            name = element.find('name')
            if name is not None:
                item['name'] = name.text
            
            # 提取image
            image = element.find('image')
            if image is not None:
                item['image'] = image.text
            
            # 提取marquee
            marquee = element.find('marquee')
            if marquee is not None:
                item['marquee'] = marquee.text
            
            # 提取video
            video = element.find('video')
            if video is not None:
                item['video'] = video.text
            
            game_items.append(item)
            
    except ET.ParseError as e:
        print(f"解析 {gamelist_path} 失败: {str(e)}")
    except Exception as e:
        print(f"读取 {gamelist_path} 时出错: {str(e)}")
    
    return game_items

def find_and_read_gamelists(src_dir):
    """
    遍历src_dir目录，找出所有包含gamelist.xml的目录并读取内容
    
    参数:
        src_dir: 要搜索的根目录
        
    返回:
        list: 包含所有gamelist.xml解析结果的列表
    """
    gamelist_contents = {}
    
    # 遍历目录树
    for root, dirs, files in os.walk(src_dir):
        if 'gamelist.xml' in files:
            print(f"find gamelist.xml: {root}")
            gamelist_path = os.path.join(root, 'gamelist.xml')
            parsed_items = parse_gamelist_xml(gamelist_path)
            gamelist_contents[root] = parsed_items
    
    return gamelist_contents

def transAbnRom(src_dir, target_dir, log_func, progress_callback=None):
    print("transAbROM:",src_dir)
    gamelists = find_and_read_gamelists(src_dir)
    # 遍历每个游戏/文件夹的内容
    for i, (path, contents) in enumerate(gamelists.items()):
        # 遍历每个游戏/文件夹的内容
        for content in contents:
            # 提取path、name、image、marquee和video
            print(f"第{i+1}个游戏/文件夹信息,dir:{path}")
            print(f"path: {content.get('path', '')}")
            print(f"name: {content.get('name', '')}")
            print(f"image: {content.get('image', '')}")
            print(f"marquee: {content.get('marquee', '')}")
            print(f"video: {content.get('video', '')}")
            print("-" * 50)
    

    log_func("All abn files have been processed.")

