import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
import threading

class GifConverterApp:
    def __init__(self, root):
        self.root = root
        
        # 定义语言包
        self.languages = {
            'cn': {
                'title': "GIF转JPEG工具",
                'gif_file': "GIF文件：",
                'output_dir': "输出目录：",
                'frame_interval': "帧间隔：",
                'browse': "浏览",
                'start': "开始转换",
                'ready': "准备就绪",
                'processing': "正在处理第 {} 帧，共 {} 帧",
                'complete': "转换完成！共处理了 {} 帧",
                'error': "错误",
                'error_select': "请选择GIF文件和输出目录",
                'error_interval': "请输入有效的帧间隔（必须为正整数）",
                'complete_msg': "GIF转换完成！",
                'switch_lang': "Switch to English"
            },
            'en': {
                'title': "GIF to JPEG Converter",
                'gif_file': "GIF File:",
                'output_dir': "Output Directory:",
                'frame_interval': "Frame Interval:",
                'browse': "Browse",
                'start': "Start Convert",
                'ready': "Ready",
                'processing': "Processing frame {} of {}",
                'complete': "Completed! Processed {} frames",
                'error': "Error",
                'error_select': "Please select GIF file and output directory",
                'error_interval': "Please enter valid frame interval (must be positive integer)",
                'complete_msg': "GIF conversion completed!",
                'switch_lang': "切换到中文"
            }
        }
        
        self.current_lang = 'cn'  # 默认中文
        self.root.title(self.languages[self.current_lang]['title'])
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        
        # 设置默认字体大小和样式
        style = ttk.Style()
        style.configure('.',  font=('Microsoft YaHei UI', 11))
        style.configure('TButton', font=('Microsoft YaHei UI', 11))
        style.configure('TLabel', font=('Microsoft YaHei UI', 11))
        style.configure('TEntry', font=('Microsoft YaHei UI', 11))
        
        # 配置根窗口的网格权重，使主框架居中
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主框架的网格权重
        for i in range(6):  # 根据行数配置
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):  # 根据列数配置
            main_frame.grid_columnconfigure(i, weight=1)
        
        # 添加语言切换按钮
        self.lang_btn = ttk.Button(main_frame, text=self.languages[self.current_lang]['switch_lang'], 
                                 command=self.switch_language)
        self.lang_btn.grid(row=6, column=0, columnspan=3, pady=10)
        
        # GIF文件选择
        self.file_label = ttk.Label(main_frame, text=self.languages[self.current_lang]['gif_file'])
        self.file_label.grid(row=0, column=0, sticky=tk.E, pady=5)
        self.gif_path = tk.StringVar()
        self.gif_entry = ttk.Entry(main_frame, textvariable=self.gif_path, width=50)
        self.gif_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_gif_btn = ttk.Button(main_frame, text=self.languages[self.current_lang]['browse'], 
                                       command=self.browse_gif)
        self.browse_gif_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # 输出目录选择
        self.output_label = ttk.Label(main_frame, text=self.languages[self.current_lang]['output_dir'])
        self.output_label.grid(row=1, column=0, sticky=tk.E, pady=5)
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_output_btn = ttk.Button(main_frame, text=self.languages[self.current_lang]['browse'], 
                                          command=self.browse_output)
        self.browse_output_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # 帧间隔设置
        self.interval_label = ttk.Label(main_frame, text=self.languages[self.current_lang]['frame_interval'])
        self.interval_label.grid(row=2, column=0, sticky=tk.E, pady=5)
        self.interval = tk.StringVar(value="1")
        interval_entry = ttk.Entry(main_frame, textvariable=self.interval, width=10)
        interval_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, pady=20)
        
        # 状态标签
        self.status_var = tk.StringVar(value=self.languages[self.current_lang]['ready'])
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, columnspan=3)
        
        # 转换按钮
        self.convert_btn = ttk.Button(main_frame, text=self.languages[self.current_lang]['start'], 
                                    command=self.start_conversion)
        self.convert_btn.grid(row=5, column=0, columnspan=3, pady=20)

    def switch_language(self):
        # 切换语言
        self.current_lang = 'en' if self.current_lang == 'cn' else 'cn'
        
        # 更新所有文本
        self.root.title(self.languages[self.current_lang]['title'])
        self.file_label.config(text=self.languages[self.current_lang]['gif_file'])
        self.output_label.config(text=self.languages[self.current_lang]['output_dir'])
        self.interval_label.config(text=self.languages[self.current_lang]['frame_interval'])
        self.browse_gif_btn.config(text=self.languages[self.current_lang]['browse'])
        self.browse_output_btn.config(text=self.languages[self.current_lang]['browse'])
        self.convert_btn.config(text=self.languages[self.current_lang]['start'])
        self.lang_btn.config(text=self.languages[self.current_lang]['switch_lang'])
        if self.status_var.get() == self.languages['cn' if self.current_lang == 'en' else 'en']['ready']:
            self.status_var.set(self.languages[self.current_lang]['ready'])

    def browse_gif(self):
        filename = filedialog.askopenfilename(filetypes=[("GIF文件", "*.gif")])
        if filename:
            self.gif_path.set(filename)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def start_conversion(self):
        if not self.gif_path.get() or not self.output_path.get():
            messagebox.showerror(self.languages[self.current_lang]['error'], 
                               self.languages[self.current_lang]['error_select'])
            return
            
        try:
            interval = int(self.interval.get())
            if interval < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror(self.languages[self.current_lang]['error'], 
                               self.languages[self.current_lang]['error_interval'])
            return
            
        self.convert_btn.configure(state='disabled')
        thread = threading.Thread(target=self.convert_gif)
        thread.start()

    def convert_gif(self):
        try:
            output_dir = os.path.join(self.output_path.get(), 'gif_output')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            with Image.open(self.gif_path.get()) as gif:
                # 获取总帧数
                frames = 0
                try:
                    while True:
                        frames += 1
                        gif.seek(gif.tell() + 1)
                except EOFError:
                    pass
                
                # 计算实际会保存的帧数
                interval = int(self.interval.get())
                total_frames_to_save = (frames + interval - 1) // interval
                
                # 重置到第一帧
                gif.seek(0)
                
                # 开始转换
                base_name = os.path.splitext(os.path.basename(self.gif_path.get()))[0]
                frame_count = 0
                saved_frames = 0
                
                self.progress['maximum'] = frames
                
                try:
                    while True:
                        if frame_count % interval == 0:
                            current = gif.convert('RGB')
                            output_path = os.path.join(output_dir, f"{base_name}_{saved_frames:04d}.jpg")
                            current.save(output_path, "JPEG", quality=95)
                            saved_frames += 1
                            self.status_var.set(self.languages[self.current_lang]['processing'].format(saved_frames, total_frames_to_save))
                            
                        frame_count += 1
                        self.progress['value'] = frame_count
                        self.root.update_idletasks()
                        gif.seek(gif.tell() + 1)
                except EOFError:
                    pass
                
            self.status_var.set(self.languages[self.current_lang]['complete'].format(saved_frames))
            messagebox.showinfo(self.languages[self.current_lang]['title'], 
                              self.languages[self.current_lang]['complete_msg'])
            
        except Exception as e:
            messagebox.showerror(self.languages[self.current_lang]['error'], str(e))
            
        finally:
            self.convert_btn.configure(state='normal')
            self.progress['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = GifConverterApp(root)
    root.mainloop() 