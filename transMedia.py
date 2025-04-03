import os
import shutil
import time

def transMedia(folder_a, folder_b, log_func, progress_callback=None):
    # 在目标文件夹B下创建download_media文件夹
    download_media_dir = os.path.join(folder_b, 'downloaded_media')
    if not os.path.exists(download_media_dir):
        os.makedirs(download_media_dir)

    # 先收集所有media文件夹路径
    media_dirs = []
    for root, dirs, files in os.walk(folder_a):
        if 'media' in dirs:
            media_dirs.append(os.path.join(root, 'media'))
    
    total_files = 0
    processed_files = 0
    
    # 预计算总文件数
    for media_dir in media_dirs:
        for root, dirs, files in os.walk(media_dir):
            total_files += len(files)
    
    # 处理每个media文件夹
    for media_dir in media_dirs:
        parent_folder_name = os.path.basename(os.path.dirname(media_dir))
        target_parent_folder = os.path.join(download_media_dir, parent_folder_name)
        
        if not os.path.exists(target_parent_folder):
            os.makedirs(target_parent_folder)
        
        # 创建子目录
        for subdir in ['covers', 'videos', 'marquees']:
            os.makedirs(os.path.join(target_parent_folder, subdir), exist_ok=True)
        
        # 处理媒体文件
        for root, dirs, files in os.walk(media_dir):
            for item in files:
                item_path = os.path.join(root, item)
                base_name, ext = os.path.splitext(os.path.basename(item_path).lower())
                
                if base_name in ['boxfront', 'logo', 'video']:
                    relative_path = os.path.relpath(root, media_dir)
                    subdir_name = parent_folder_name if relative_path == '.' else os.path.basename(relative_path)
                    
                    new_name = f"{subdir_name}{ext}"
                    target_subdir = os.path.join(target_parent_folder, {
                        'boxfront': 'covers',
                        'logo': 'marquees',
                        'video': 'videos'
                    }[base_name])
                    new_path = os.path.join(target_subdir, new_name)
                    
                    shutil.copy2(item_path, new_path)
                    processed_files += 1
                    
                    # 每处理10个文件更新一次进度
                    if processed_files % 10 == 0:
                        if progress_callback:
                            progress_callback(processed_files, total_files,subdir_name)
                        time.sleep(0.01)  # 短暂释放GIL锁
    
    log_func("All files have been copied.")

