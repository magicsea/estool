import os  
import xml.etree.ElementTree as ET  
from datetime import datetime  
from xml.dom import minidom 

def read_metadata(file_path):  
    """读取metadata.pegasus.txt文件并返回game, file, description的字典列表"""  
    games = []  
    try:  
        with open(file_path, 'r', encoding='utf-8') as f:  
            for line in f:  
                line = line.strip()  
                if not line or line.startswith('#'):  
                    continue  
                parts = line.split(':')  
                if len(parts) == 2 and parts[0].strip().lower() in ['game', 'file', 'description']:  
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
    if current_game:  
        merged_games.append(current_game)  
    return merged_games  
  
def create_gamelist_xml(games, target_folder, subdirectories,log_func):  
    """创建gamelist.xml文件"""
    root = ET.Element("gameList")  
    for game in games:  
        game_elem = ET.SubElement(root, "game")  
        path_elem = ET.SubElement(game_elem, "path").text ="./" + game.get('file', "")  
        name_elem = ET.SubElement(game_elem, "name").text = game.get('game', "")
        desc_elem = ET.SubElement(game_elem, "desc").text = game.get('description', "")  
        playcount_elem = ET.SubElement(game_elem, "playcount").text = "1"    
        lastplayed_elem = ET.SubElement(game_elem, "lastplayed").text = "" 
               
      
    xml_str = ET.tostring(root, encoding='utf8', method='xml')
    xml_str = xml_str.decode('utf8')
    
    log_func(f"正在处理子目录: {subdirectories}")  # 替换原来的print语句
    target_subfolder = os.path.join(target_folder, 'gamelists', subdirectories)   
    os.makedirs(target_subfolder, exist_ok=True)  
    xml_file_path = os.path.join(target_subfolder, 'gamelist.xml')  
    with open(xml_file_path, 'w', encoding='utf-8') as f:  
        f.write(xml_str)  
 
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
    # 指定文件夹A的路径和目标文件夹的路径
    # source_folder = 'C:/迅雷下载/es/Roms'  # 替换为你的文件夹A的路径
    # target_folder = 'C:/迅雷下载/es/trom'  # 替换为你的目标文件夹的路径
    xml_declaration = '<?xml version="1.0"?>\n'  
    subdirs = list_subdirectories(source_folder)
    i = 0
    # 遍历文件夹A下的所有子文件夹  
    for root, dirs, files in os.walk(source_folder):
        if 'metadata.pegasus.txt' in files:  
            metadata_path = os.path.join(root, 'metadata.pegasus.txt')
            games = read_metadata(metadata_path)
            
            if games:  
                create_gamelist_xml(games, target_folder, subdirs[i],log_func)
                i += 1
    
    #log_func(f"正在处理子目录: {subdirectories}")  # 使用传入的日志函数

