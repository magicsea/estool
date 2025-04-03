import os  
import shutil  
  
# 指定文件夹A和文件夹B的路径  
# folder_a = 'C:/迅雷下载/es/Roms'  # 替换为您的文件夹A路径  
# folder_b = 'C:/迅雷下载/es/trom'  # 替换为您的文件夹B路径  
 
def transMedia(folder_a, folder_b,log_func):
    # 在目标文件夹B下创建download_media文件夹  
    download_media_dir = os.path.join(folder_b, 'downloaded_media')  
    if not os.path.exists(download_media_dir):  
        os.makedirs(download_media_dir)  

    # 遍历文件夹A下的所有子文件夹中的media文件夹  
    for root, dirs, files in os.walk(folder_a):  
        if 'media' in dirs:  
            media_dir = os.path.join(root, 'media')  

            # 保留media文件夹的父文件夹名称  
            parent_folder_name = os.path.basename(os.path.dirname(media_dir))  

            # 在download_media文件夹下创建和media父文件夹同名的文件夹  
            target_parent_folder = os.path.join(download_media_dir, parent_folder_name)  
            if not os.path.exists(target_parent_folder):  
                os.makedirs(target_parent_folder)  

            # 在每个子文件夹中都创建covers, videos, marquees三个文件夹  
            for subdir in ['covers', 'videos', 'marquees']:  
                os.makedirs(os.path.join(target_parent_folder, subdir), exist_ok=True)  

            # 递归遍历media文件夹及其子文件夹  
            def process_media_files(media_dir, target_parent_folder):  
                for root, dirs, files in os.walk(media_dir):  
                    for item in files:  
                        item_path = os.path.join(root, item)  
                        base_name, ext = os.path.splitext(os.path.basename(item_path).lower())  

                        if base_name in ['boxfront', 'logo', 'video']:  
                            # 获取相对于media文件夹的路径  
                            relative_path = os.path.relpath(root, media_dir)  
                            if relative_path == '.':  
                                # 如果在media文件夹的根目录下，直接使用parent_folder_name  
                                subdir_name = parent_folder_name  
                            else:  
                                # 如果在media的子文件夹下，使用子文件夹名称  
                                subdir_name = os.path.basename(relative_path)  

                            # 重命名文件，保留扩展名  
                            new_name = f"{subdir_name}{ext}"  
                            target_subdir = os.path.join(target_parent_folder, {  
                                'boxfront': 'covers',  
                                'logo': 'marquees',  
                                'video': 'videos'  
                            }[base_name])  
                            new_path = os.path.join(target_subdir, new_name)  

                            # 复制文件  
                            shutil.copy2(item_path, new_path)  
                            log_func(f"Copied {item_path} to {new_path}")  

            # 调用递归函数处理media文件夹  
            process_media_files(media_dir, target_parent_folder)  

    log_func("All files have been copied.")

