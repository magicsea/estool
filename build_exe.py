import PyInstaller.__main__
import os
import shutil

# 打包配置
APP_NAME = 'ES转换工具'
SCRIPT_FILE = 'make_es.py'
ICON_FILE = None  # 可以设置为图标路径，如'icon.ico'
DIST_DIR = 'dist'
BUILD_DIR = 'build'
WORK_DIR = os.getcwd()

# 清理旧构建目录
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

# PyInstaller参数
params = [
    '--name=%s' % APP_NAME,
    '--onefile',
    '--windowed',  # 不显示控制台窗口
    '--clean',
    '--distpath=%s' % DIST_DIR,
    '--workpath=%s' % BUILD_DIR,
]

# 添加图标
if ICON_FILE and os.path.exists(ICON_FILE):
    params.append('--icon=%s' % ICON_FILE)

# 添加数据文件（包含所有依赖模块）
params.extend([
    '--add-data', 'transAbnRom.py;.',
    '--add-data', 'transName.py;.', 
    '--add-data', 'transMedia.py;.'
])

# 添加脚本文件
params.append(SCRIPT_FILE)

# 执行打包
PyInstaller.__main__.run(params)

print(f"打包完成！可执行文件位于: {os.path.join(WORK_DIR, DIST_DIR, APP_NAME)}")