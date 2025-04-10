import os  
import xml.etree.ElementTree as ET  
from datetime import datetime  
from xml.dom import minidom 
import tkinter as tk
from tkinter import filedialog, messagebox  # 添加messagebox导入
import subprocess
import configparser
from pathlib import Path
import threading  # 添加线程支持
import queue  # 添加队列支持
import time
# 修改导入语句
from transName import transName 
from transMedia import transMedia
from transAbnRom import transAbnRom
def create_gui():
    """创建图形用户界面"""
    root = tk.Tk()
    root.title("天马转换ES工具")
    
    # 创建日志框架
    log_frame = tk.Frame(root)
    log_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
    
    # 日志文本框
    log_text = tk.Text(log_frame, height=10, state='disabled')
    log_text.pack(side='left', fill='both', expand=True)  # 修改为左侧
    
    # 滚动条
    scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
    scrollbar.pack(side='right', fill='y')  # 保持右侧
    log_text['yscrollcommand'] = scrollbar.set
    
    # 创建消息队列
    message_queue = queue.Queue()
    
    # 日志输出函数
    def log_message(message):
        message_queue.put(message)
    
    # 处理消息队列的函数
    # 修改process_message_queue函数，缩短检查间隔
    def process_message_queue():
        try:
            while True:
                message = message_queue.get_nowait()
                log_text.configure(state='normal')
                log_text.insert('end', message + '\n')
                log_text.configure(state='disabled')
                log_text.see('end')
                message_queue.task_done()
        except queue.Empty:
            pass
        finally:
            # 缩短检查间隔到50毫秒
            root.after(50, process_message_queue)
    
    # 启动消息处理
    process_message_queue()
    
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
            log_message("开始执行天马转换...")
            
            # 禁用执行按钮，防止重复点击
            execute_button = root.nametowidget('.!button3')  # 获取执行按钮
            execute_button.config(state='disabled')
            
            # 在单独的线程中执行耗时操作
            def run_conversion():
                try:
                    # 传入日志函数
                    transName(source_path, target_path, log_message)
                    log_message("------gamelist转换完成------")
                    
                    # 修改transMedia调用，添加进度反馈
                    def progress_callback(current, total,currDir):
                        log_message(f"处理媒体文件中:{current}/{total}  {currDir}")
                        time.sleep(0.01)  # 短暂释放GIL锁
                    
                    transMedia(source_path, target_path, log_message, progress_callback)
                    log_message("------media转换完成------")
                    log_message("所有转换完成！")
                    # 在主线程中重新启用按钮
                    root.after(0, lambda: execute_button.config(state='normal'))
                except Exception as e:
                    error_msg = f"错误: {str(e)}"
                    log_message(error_msg)
                    # 修复：在lambda中不要引用外部的e变量，而是使用已捕获的error_msg
                    root.after(0, lambda: [
                        messagebox.showerror("错误", f"执行出错: {str(e)}"),
                        execute_button.config(state='normal')
                    ])
            
            # 启动转换线程
            threading.Thread(target=run_conversion, daemon=True).start()
        else:
            messagebox.showerror("错误", "请先选择源文件夹和目标文件夹")
    
    def execute_abn_scripts():
        source_path = source_entry.get()
        target_path = target_entry.get()
        if source_path and target_path:
            log_message("开始执行abn转换...")
            
            # 禁用执行按钮，防止重复点击
            execute_button = root.nametowidget('.!button3')  # 获取执行按钮
            execute_button.config(state='disabled')
            
            # 在单独的线程中执行耗时操作
            def run_conversion():
                try:
                    
                    def progress_callback(current, total,currDir):
                        log_message(f"处理媒体文件中:{current}/{total}  {currDir}")
                        time.sleep(0.01)  # 短暂释放GIL锁
                    
                    transAbnRom(source_path, target_path, log_message, progress_callback)
                    log_message("------media转换完成------")
                    log_message("所有转换完成！")
                    # 在主线程中重新启用按钮
                    root.after(0, lambda: execute_button.config(state='normal'))
                except Exception as e:
                    error_msg = f"错误: {str(e)}"
                    log_message(error_msg)
                    # 修复：在lambda中不要引用外部的e变量，而是使用已捕获的error_msg
                    root.after(0, lambda: [
                        messagebox.showerror("错误", f"执行出错: {str(e)}"),
                        execute_button.config(state='normal')
                    ])
            
            # 启动转换线程
            threading.Thread(target=run_conversion, daemon=True).start()
        else:
            messagebox.showerror("错误", "请先选择源文件夹和目标文件夹")
    
    # 执行按钮
    tk.Button(root, text="ABN转ES", command=execute_abn_scripts).grid(row=2, column=2, pady=10)
    
    tk.Button(root, text="天马转ES", command=execute_scripts).grid(row=2, column=0, pady=10)
    
    # 添加GitHub链接
    def open_github():
        import webbrowser
        webbrowser.open("https://github.com/magicsea/estool")
    
    github_link = tk.Label(root, text="by github.com/magicsea/estool", fg="blue", cursor="hand2")
    github_link.grid(row=4, column=0, columnspan=3, pady=5)
    github_link.bind("<Button-1>", lambda e: open_github())

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