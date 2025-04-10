import os  
import xml.etree.ElementTree as ET  
from datetime import datetime  
from xml.dom import minidom 

def read_metadata(file_path):  
    """读取metadata.pegasus.txt文件并返回game, file, description的字典列表"""  
    name = ""
    games = []  
    try:  
        with open(file_path, 'r', encoding='utf-8') as f:  
            for line in f:  
                line = line.strip()  
                if not line or line.startswith('#'):  
                    continue  
                parts = line.split(':')  
                if len(parts) == 2 and parts[0].strip().lower() in ['collection']:  
                    name = parts[1].strip()
                if len(parts) == 2 and parts[0].strip().lower() in ['game', 'file', 'description','developer','sort-by']:  
                    games.append({parts[0].strip().lower(): parts[1].strip()})  
    except Exception as e:  
        print(f"Error reading {file_path}: {e}")  
        return []  
      
    # 合并成一个字典，假设每个game只有一行对应的file和description  
    merged_games = []  
    current_game = None  
    for game_info in games:  
        if 'game' in game_info:  
            if current_game:  
                merged_games.append(current_game)  
            current_game = {'game': game_info['game']}  
        if 'file' in game_info and current_game:  
            current_game['file'] = game_info['file']  
        if 'description' in game_info and current_game:  
            current_game['description'] = game_info['description']  
        if 'developer' in game_info and current_game:  
            current_game['developer'] = game_info['developer']  
        if 'sort-by' in game_info and current_game:  
            current_game['sort-by'] = game_info['sort-by']  
    if current_game:  
        merged_games.append(current_game)  
    #print("read_metadata:",name)
    return merged_games,name  
  
def create_gamelist_xml(games, target_folder, subdirectories,collection_dir,folders, log_func):  
    """创建gamelist.xml文件"""
    print("create_gamelist_xml:",subdirectories,collection_dir,folders)
    root = ET.Element("gameList")  
    for folder in folders:  
        game_elem = ET.SubElement(root, "folder")  
        ET.SubElement(game_elem, "path").text = "./" + folder.get('path', "")
        ET.SubElement(game_elem, "name").text =  folder.get('name', "")      

    for game in games:  
        game_elem = ET.SubElement(root, "game")  
        # 如果collection_dir不为空，将path前要加上collection_dir
        if collection_dir:
            path_elem = ET.SubElement(game_elem, "path").text = "./"+game.get('platform', "") +"/"+ game.get('file', "")
        else:
            path_elem = ET.SubElement(game_elem, "path").text = "./" + game.get('file', "")

        #path_elem = ET.SubElement(game_elem, "path").text ="./" + game.get('file', "")  
        name_elem = ET.SubElement(game_elem, "name").text = game.get('game', "")
        desc_elem = ET.SubElement(game_elem, "desc").text = game.get('description', "")  
        ET.SubElement(game_elem, "developer").text = game.get('developer', "")  
        ET.SubElement(game_elem, "sortname").text =  game.get('sort-by', "")  
        playcount_elem = ET.SubElement(game_elem, "playcount").text = "1"    
        lastplayed_elem = ET.SubElement(game_elem, "lastplayed").text = "" 

    # 使用minidom正确格式化XML
    xml_str = ET.tostring(root, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ')
    
    # 移除空行
    lines = pretty_xml.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    pretty_xml = '\n'.join(non_empty_lines)
    
    log_func(f"正在处理子目录: {subdirectories}")
    target_subfolder = os.path.join(target_folder, 'gamelists', subdirectories)   
    os.makedirs(target_subfolder, exist_ok=True)  
    xml_file_path = os.path.join(target_subfolder, 'gamelist.xml')  
    print("create_gamelist_xml write:",xml_file_path)
    with open(xml_file_path, 'w', encoding='utf-8') as f:  
        f.write(pretty_xml)  
 
def list_subdirectories(path):  
    """  
    列出指定路径下的所有子文件夹名称  
    """  
    subdirectories = []  
    for root, dirs, files in os.walk(path):  
        for name in dirs: 
            subdirectories.append(name)  
    return subdirectories 
    
# 指定文件夹A的路径和目标文件夹的路径  
# source_folder = 'C:/迅雷下载/es/Roms'  # 替换为你的文件夹A的路径  
# target_folder = 'C:/迅雷下载/es/trom'  # 替换为你的目标文件夹的路径  

def transName(source_folder, target_folder, log_func=None):
    # 获取所有子目录
    subdirs = list_subdirectories(source_folder)
    collections = {}  # 存储合集目录信息
    
    # 第一次遍历：收集所有平台和合集信息
    for root, dirs, files in os.walk(source_folder):
        if 'metadata.pegasus.txt' in files:
            metadata_path = os.path.join(root, 'metadata.pegasus.txt')
            games , metaName = read_metadata(metadata_path)
        
            if games:
                parent_dir = os.path.dirname(root)
                platform_name = os.path.basename(root)
                print("read_metadata111:",root,dirs,parent_dir,platform_name)
                # 判断是否是合集目录
                is_collection = parent_dir != source_folder
                
                if is_collection:
                    collection_name = os.path.basename(parent_dir)
                    if collection_name not in collections:
                        collections[collection_name] = {
                            'path': parent_dir,
                            'games': [],
                            'folders': []
                        }
                    print("add new collection:",collection_name,parent_dir,platform_name,metaName)
                    # collections[collection_name]['games'].extend(games)
                    for item in games:
                        #print("range item:",item)
                        item['platform'] = platform_name
                        #print("range item2:",item)
                        collections[collection_name]['games'].append(item)
                    collections[collection_name]['folders'].append({'path':platform_name,'name':metaName})
                else:
                    # 普通平台目录立即处理
                    create_gamelist_xml(games, target_folder, platform_name, "",[], log_func)
    
    # 第二次遍历：处理所有合集目录
    for collection_name, collection_data in collections.items():
        print("make gamelist collection:", collection_name, collection_data['path'], target_folder)
        create_gamelist_xml(
            collection_data['games'], 
            target_folder, 
            collection_name,
            collection_name, 
            collection_data['folders'],
            log_func
        )

