import os
import sys
import io
import shutil
import shutil
import shutil
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

def copy_file(source_path, target_dir, path_info):
    """
    复制文件到目标目录，处理多级目录并修改文件名
    
    参数:
        source_path: 源文件的完整路径
        target_dir: 目标目录
        path_info: 包含路径信息的字符串，用于创建目录和修改文件名
    """
    if os.path.exists(source_path):
        # 提取多级目录和文件名前缀
        path_dirs = os.path.dirname(path_info.lstrip('./'))
        file_prefix = os.path.splitext(os.path.basename(path_info))[0]
        
        # 创建多级目录
        target_sub_dir = os.path.join(target_dir, path_dirs)
        if not os.path.exists(target_sub_dir):
            os.makedirs(target_sub_dir)
        
        # 构建目标文件路径
        target_file_name = f"{file_prefix}{os.path.splitext(os.path.basename(source_path))[1]}"
        target_file_path = os.path.join(target_sub_dir, target_file_name)
        
        # 复制文件
        shutil.copy2(source_path, target_file_path)

def transAbnRom(src_dir, target_dir, log_func, progress_callback=None):
    print("transAbROM:", src_dir)
    # 目标目录创建downloaded_media目录，检查存在
    downloaded_media_dir = os.path.join(target_dir, 'downloaded_media')
    if not os.path.exists(downloaded_media_dir):
        os.makedirs(downloaded_media_dir)
    
    gamelists = find_and_read_gamelists(src_dir)
    # 遍历每个游戏/文件夹的内容
    for i, (path, contents) in enumerate(gamelists.items()):

        platname = os.path.basename(path)
        # 复制gamelist.xml到目标目录的gamelists/{平台}目录下,目录不存在则创建
        gamelists_dir = os.path.join(target_dir, 'gamelists', platname)
        if not os.path.exists(gamelists_dir):
            os.makedirs(gamelists_dir)
        src_gamelist_path = os.path.join(path, 'gamelist.xml')
        target_gamelist_path = os.path.join(gamelists_dir, 'gamelist.xml')
        if os.path.exists(src_gamelist_path):
            shutil.copy2(src_gamelist_path, target_gamelist_path)

        # 尝试在downloaded_media下创建目录平台，如果不存在则创建
        platform_dir = os.path.join(downloaded_media_dir, platname)
        if not os.path.exists(platform_dir):
            os.makedirs(platform_dir)
        # 在平台目录下创建covers, marquees, videos目录
        covers_dir = os.path.join(platform_dir, 'covers')
        marquees_dir = os.path.join(platform_dir, 'marquees')
        videos_dir = os.path.join(platform_dir, 'videos')
        for dir_path in [covers_dir, marquees_dir, videos_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        # 遍历每个游戏/文件夹的内容
        for content in contents:
            # 提取path、name、image、marquee和video
            path_info = content.get('path', '')

            # 把image文件复制到downloaded_media\{平台}\covers目录下
            if content.get('image'):
                image_path = os.path.join(path, content['image'].lstrip('./'))
                copy_file(image_path, covers_dir, path_info)

            # 把marquee文件复制到downloaded_media\{平台}\marquees目录下
            if content.get('marquee'):
                marquee_path = os.path.join(path, content['marquee'].lstrip('./'))
                copy_file(marquee_path, marquees_dir, path_info)

            # 把video文件复制到downloaded_media\{平台}\videos目录下
            if content.get('video'):
                video_path = os.path.join(path, content['video'].lstrip('./'))
                copy_file(video_path, videos_dir, path_info)

    log_func("All abn files have been processed.")

