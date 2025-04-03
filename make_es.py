import os  
import xml.etree.ElementTree as ET  
from datetime import datetime  
from xml.dom import minidom 
import tkinter as tk
from tkinter import filedialog
import subprocess
import configparser
from pathlib import Path
# 修改导入语句
from transName import transName 
from transMedia import transMedia

def create_gui():
    """创建图形用户界面"""
    root = tk.Tk()
    root.title("天马G资源转换工具")
    
    # 创建日志框架
    log_frame = tk.Frame(root)
    log_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
    
    # 日志文本框
    log_text = tk.Text(log_frame, height=10, state='disabled')
    log_text.pack(fill='both', expand=True)
    
    # 滚动条
    scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
    scrollbar.pack(side='right', fill='y')
    log_text['yscrollcommand'] = scrollbar.set
    
    # 日志输出函数
    # 在文件顶部添加
    def log_message(message):
        log_text.configure(state='normal')
        log_text.insert('end', message + '\n')
        log_text.configure(state='disabled')
        log_text.see('end')
    
    # 读取配置文件
    config = configparser.ConfigParser()
    config_file = Path(os.path.join(os.getcwd(), "config.ini"))
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:  # 添加utf-8编码
            config.read_file(f)
    else:
        # 创建配置文件
        config['PATHS'] = {}
        with open(config_file, 'w', encoding='utf-8') as f:  # 添加utf-8编码
            config.write(f)
    
    # 源路径选择
    tk.Label(root, text="源Roms路径:").grid(row=0, column=0, padx=5, pady=5)
    source_entry = tk.Entry(root, width=50)
    source_entry.grid(row=0, column=1, padx=5, pady=5)
    if config.has_option('PATHS', 'source_path'):
        source_entry.insert(0, config['PATHS']['source_path'])
    tk.Button(root, text="浏览", command=lambda: [source_entry.delete(0, tk.END), source_entry.insert(0, filedialog.askdirectory())]).grid(row=0, column=2, padx=5, pady=5)
    
    # 目标路径选择
    tk.Label(root, text="目标Roms路径:").grid(row=1, column=0, padx=5, pady=5)
    target_entry = tk.Entry(root, width=50)
    target_entry.grid(row=1, column=1, padx=5, pady=5)
    if config.has_option('PATHS', 'target_path'):
        target_entry.insert(0, config['PATHS']['target_path'])
    tk.Button(root, text="浏览", command=lambda: [target_entry.delete(0, tk.END), target_entry.insert(0, filedialog.askdirectory())]).grid(row=1, column=2, padx=5, pady=5)
    
    # 修改执行按钮函数
    def execute_scripts():
        source_path = source_entry.get()
        target_path = target_entry.get()
        if source_path and target_path:
            log_message("开始执行转换...")
            try:
                # 传入日志函数
                transName(source_path, target_path, log_message)
                log_message("------gamelist转换完成------")
                transMedia(source_path, target_path, log_message)
                log_message("------media转换完成------")
                log_message("所有转换完成！")
            except Exception as e:
                log_message(f"错误: {str(e)}")
                tk.messagebox.showerror("错误", f"执行出错: {str(e)}")
        else:
            tk.messagebox.showerror("错误", "请先选择源文件夹和目标文件夹")
    
    tk.Button(root, text="执行脚本", command=execute_scripts).grid(row=2, column=1, pady=10)
    
    # 窗口关闭时保存配置
    def on_closing():
        config['PATHS'] = {
            'source_path': source_entry.get(),
            'target_path': target_entry.get()
        }
        with open(config_file, 'w', encoding='utf-8') as f:  # 添加utf-8编码
            config.write(f)
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    create_gui()

# 导出函数
__all__ = ['log_message']