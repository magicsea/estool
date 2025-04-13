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
    
    # 添加字典存储合集文件
    collection_files = {}
    
    # 处理每个media文件夹
    for media_dir in media_dirs:
        parent_folder_name = os.path.basename(os.path.dirname(media_dir))
        parent_parent_name = os.path.basename(os.path.dirname(os.path.dirname(media_dir)))
        
        # 判断是否是平台集合目录
        platform_dir = os.path.dirname(media_dir)
        parent_dir = os.path.dirname(platform_dir)
        is_collection = parent_dir != folder_a
        
        if is_collection:
            # 将合集文件暂存到字典中
            if parent_parent_name not in collection_files:
                collection_files[parent_parent_name] = []
                
            # 收集当前平台的所有媒体文件
            for root, dirs, files in os.walk(media_dir):
                for item in files:
                    item_path = os.path.join(root, item)
                    base_name, ext = os.path.splitext(os.path.basename(item_path).lower())
                    
                    if base_name in ['boxfront', 'logo', 'video']:
                        relative_path = os.path.relpath(root, media_dir)
                        subdir_name = parent_folder_name if relative_path == '.' else os.path.basename(relative_path)
                        
                        new_name = f"{subdir_name}{ext}"
                        collection_files[parent_parent_name].append({
                            'item_path': item_path,
                            'base_name': base_name,
                            'new_name': new_name,
                            'platform_name': parent_folder_name
                        })
                        processed_files += 1
        else:
            # 普通平台目录处理
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
                    
                    if base_name in ['boxfront', 'box_front', 'logo', 'video']:
                        relative_path = os.path.relpath(root, media_dir)
                        subdir_name = parent_folder_name if relative_path == '.' else os.path.basename(relative_path)
                        
                        new_name = f"{subdir_name}{ext}"
                        target_subdir = os.path.join(target_parent_folder, {
                            'boxfront': 'covers',
                            'box_front': 'covers',
                            'logo': 'marquees',
                            'video': 'videos'
                        }[base_name])
                        new_path = os.path.join(target_subdir, new_name)
                        print("copy platform file: ",item_path,new_path)
                        shutil.copy2(item_path, new_path)
                        processed_files += 1
                        
                        # 每处理10个文件更新一次进度
                        if processed_files % 10 == 0:
                            if progress_callback:
                                progress_callback(processed_files, total_files,subdir_name)
                            time.sleep(0.01)  # 短暂释放GIL锁
    
    # 统一处理合集目录
    for collection_name, files in collection_files.items():
        print("copy collection:",collection_name)
        collection_dir = os.path.join(download_media_dir, collection_name)
        if not os.path.exists(collection_dir):
            os.makedirs(collection_dir)
        
        # 创建子目录
        for subdir in ['covers', 'videos', 'marquees']:
            os.makedirs(os.path.join(collection_dir, subdir), exist_ok=True)
        
        # 复制文件
        for file_info in files:
            target_subdir = os.path.join(collection_dir, {
                'boxfront': 'covers',
                'logo': 'marquees',
                'video': 'videos'
            }[file_info['base_name']])
            
            # 创建平台子目录
            platform_subdir = os.path.join(target_subdir, file_info['platform_name'])
            os.makedirs(platform_subdir, exist_ok=True)
            
            new_path = os.path.join(platform_subdir, file_info['new_name'])

            print("copy collection file: ",file_info['item_path'],new_path)
            shutil.copy2(file_info['item_path'], new_path)
            
            # 更新进度
            if processed_files % 10 == 0 and progress_callback:
                progress_callback(processed_files, total_files, file_info['platform_name'])
                time.sleep(0.01)
    
    log_func("All files have been copied.")

