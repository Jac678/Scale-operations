# import tkinter as tk
# from tkinter import ttk, messagebox, simpledialog
# import subprocess
# import os
# import sys
# import platform

# class SSHTerminalManager:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("SSH终端管理器")
#         self.root.geometry("800x600")
#         self.root.resizable(True, True)
        
#         # 设置中文字体支持
#         self.setup_fonts()
        
#         # 终端配置
#         self.terminal_count = 5
#         self.ssh_user = "hello"
#         self.ssh_ip = "192.168.1.87"
#         self.ssh_password = ""
#         self.script_prefix = "video2gs_"
#         self.working_dir = "/data/ycy/"
#         self.env_command = "mamba activate 3dgs"
        
#         # 路径配置列表
#         self.path_configs = []
        
#         # 创建UI
#         self.create_widgets()
#         self.generate_path_configs()
        
#     def setup_fonts(self):
#         """设置支持中文的字体"""
#         if platform.system() == "Windows":
#             default_font = ("SimHei", 10)
#         elif platform.system() == "Darwin":  # macOS
#             default_font = ("Heiti TC", 10)
#         else:  # Linux
#             default_font = ("WenQuanYi Micro Hei", 10)
            
#         self.root.option_add("*Font", default_font)
    
#     def create_widgets(self):
#         """创建UI组件"""
#         # 创建主框架
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # SSH配置区域
#         ssh_frame = ttk.LabelFrame(main_frame, text="SSH连接配置", padding="10")
#         ssh_frame.pack(fill=tk.X, pady=5)
        
#         # SSH配置网格
#         ssh_grid = ttk.Frame(ssh_frame)
#         ssh_grid.pack(fill=tk.X)
        
#         ttk.Label(ssh_grid, text="用户名:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
#         self.ssh_user_var = tk.StringVar(value=self.ssh_user)
#         ttk.Entry(ssh_grid, textvariable=self.ssh_user_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
#         ttk.Label(ssh_grid, text="服务器IP:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
#         self.ssh_ip_var = tk.StringVar(value=self.ssh_ip)
#         ttk.Entry(ssh_grid, textvariable=self.ssh_ip_var, width=20).grid(row=0, column=3, padx=5, pady=5)
        
#         ttk.Label(ssh_grid, text="密码:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
#         self.ssh_password_var = tk.StringVar(value=self.ssh_password)
#         ttk.Entry(ssh_grid, textvariable=self.ssh_password_var, show="*", width=20).grid(row=0, column=5, padx=5, pady=5)
        
#         ttk.Label(ssh_grid, text="终端数量:").grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
#         self.terminal_count_var = tk.StringVar(value=str(self.terminal_count))
#         ttk.Combobox(ssh_grid, textvariable=self.terminal_count_var, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], width=5).grid(row=0, column=7, padx=5, pady=5)
        
#         # 脚本配置区域
#         script_frame = ttk.LabelFrame(main_frame, text="脚本配置", padding="10")
#         script_frame.pack(fill=tk.X, pady=5)
        
#         script_grid = ttk.Frame(script_frame)
#         script_grid.pack(fill=tk.X)
        
#         ttk.Label(script_grid, text="脚本前缀:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
#         self.script_prefix_var = tk.StringVar(value=self.script_prefix)
#         ttk.Entry(script_grid, textvariable=self.script_prefix_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
#         ttk.Label(script_grid, text="工作目录:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
#         self.working_dir_var = tk.StringVar(value=self.working_dir)
#         ttk.Entry(script_grid, textvariable=self.working_dir_var, width=30).grid(row=0, column=3, padx=5, pady=5)
        
#         ttk.Label(script_grid, text="环境命令:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
#         self.env_command_var = tk.StringVar(value=self.env_command)
#         ttk.Entry(script_grid, textvariable=self.env_command_var, width=30).grid(row=0, column=5, padx=5, pady=5)
        
#         # 路径配置区域
#         path_frame = ttk.LabelFrame(main_frame, text="脚本路径配置", padding="10")
#         path_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
#         # 路径配置表格
#         columns = ("script_name", "input_dir", "output_dir")
#         self.path_tree = ttk.Treeview(path_frame, columns=columns, show="headings")
        
#         # 设置列标题
#         self.path_tree.heading("script_name", text="脚本名称")
#         self.path_tree.heading("input_dir", text="INPUT_DIR")
#         self.path_tree.heading("output_dir", text="OUTPUT_DIR")
        
#         # 设置列宽
#         self.path_tree.column("script_name", width=150)
#         self.path_tree.column("input_dir", width=300)
#         self.path_tree.column("output_dir", width=300)
        
#         # 添加滚动条
#         scrollbar = ttk.Scrollbar(path_frame, orient=tk.VERTICAL, command=self.path_tree.yview)
#         self.path_tree.configure(yscroll=scrollbar.set)
        
#         # 布局表格和滚动条
#         self.path_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
#         # 按钮区域
#         button_frame = ttk.Frame(main_frame)
#         button_frame.pack(fill=tk.X, pady=10)
        
#         ttk.Button(button_frame, text="刷新配置", command=self.refresh_configs).pack(side=tk.LEFT, padx=5)
#         ttk.Button(button_frame, text="自动填充示例路径", command=self.fill_example_paths).pack(side=tk.LEFT, padx=5)
#         ttk.Button(button_frame, text="启动所有终端", command=self.start_all_terminals).pack(side=tk.RIGHT, padx=5)
    
#     def generate_path_configs(self):
#         """生成路径配置列表"""
#         # 清空现有数据
#         for item in self.path_tree.get_children():
#             self.path_tree.delete(item)
            
#         self.path_configs = []
#         count = int(self.terminal_count_var.get())
        
#         for i in range(1, count + 1):
#             script_name = f"{self.script_prefix_var.get()}{i}.sh"
#             self.path_configs.append({
#                 "script_name": script_name,
#                 "input_dir": "",
#                 "output_dir": ""
#             })
#             self.path_tree.insert("", tk.END, values=(script_name, "", ""))
        
#         # 绑定双击事件用于编辑
#         self.path_tree.bind("<Double-1>", self.edit_cell)
    
#     def edit_cell(self, event):
#         """编辑表格单元格"""
#         region = self.path_tree.identify_region(event.x, event.y)
#         if region != "cell":
#             return
            
#         column = int(self.path_tree.identify_column(event.x).replace("#", "")) - 1
#         item = self.path_tree.identify_row(event.y)
#         row = self.path_tree.index(item)
        
#         if row < 0 or row >= len(self.path_configs):
#             return
            
#         # 获取当前值
#         current_value = self.path_tree.item(item, "values")[column]
        
#         # 请求用户输入新值
#         new_value = simpledialog.askstring(
#             "编辑路径", 
#             f"请输入{self.path_tree.heading(f'#{column+1}')['text']}",
#             initialvalue=current_value
#         )
        
#         if new_value is not None:
#             # 更新表格
#             values = list(self.path_tree.item(item, "values"))
#             values[column] = new_value
#             self.path_tree.item(item, values=values)
            
#             # 更新配置数据
#             config_key = ["script_name", "input_dir", "output_dir"][column]
#             self.path_configs[row][config_key] = new_value
    
#     def refresh_configs(self):
#         """刷新配置列表"""
#         self.generate_path_configs()
#         messagebox.showinfo("提示", "配置已刷新")
    
#     def fill_example_paths(self):
#         """填充示例路径"""
#         count = int(self.terminal_count_var.get())
        
#         for i in range(count):
#             item = self.path_tree.get_children()[i]
#             script_index = i + 1
            
#             input_dir = f"/data/input/set{script_index}"
#             output_dir = f"/data/output/result{script_index}"
            
#             # 更新表格
#             self.path_tree.item(item, values=(
#                 self.path_configs[i]["script_name"],
#                 input_dir,
#                 output_dir
#             ))
            
#             # 更新配置数据
#             self.path_configs[i]["input_dir"] = input_dir
#             self.path_configs[i]["output_dir"] = output_dir
    
#     def get_terminal_command(self, index):
#         """获取终端启动命令"""
#         config = self.path_configs[index]
#         script_index = index + 1
        
#         # 检查配置是否完整
#         if not config["input_dir"] or not config["output_dir"]:
#             messagebox.showerror("错误", f"请填写第{script_index}个脚本的路径配置")
#             return None
            
#         # 获取配置参数
#         user = self.ssh_user_var.get()
#         ip = self.ssh_ip_var.get()
#         password = self.ssh_password_var.get()
#         script_name = config["script_name"]
#         work_dir = self.working_dir_var.get()
#         env_cmd = self.env_command_var.get()
        
#         # 生成expect脚本内容
#         expect_script = f'''
#             spawn ssh {user}@{ip}
#             expect "password:"
#             send "{password}\r"
#             expect "{user}@*"
            
#             send "{env_cmd}\r"
#             expect "(*) {user}@*"
#             send "cd {work_dir}\r"
#             expect "(*) {user}@*:{work_dir}"
            
#             send "echo 请修改 {script_name} 中的路径...\r"
#             send "echo 当前预设路径:\r"
#             send "echo INPUT_DIR={config["input_dir"]}\r"
#             send "echo OUTPUT_DIR={config["output_dir"]}\r"
#             send "sleep 2\r"
            
#             send "vim {script_name}\r"
#             expect eof
            
#             send "./{script_name}\r"
#             interact
#         '''
        
#         # 根据操作系统选择终端命令 - 修复了引号转义问题
#         system = platform.system()
#         # 使用三引号和适当的转义处理引号
#         script_arg = 'expect -c \'{}\''.format(expect_script.replace('\n', ' ').replace('\'', '\\\''))
        
#         if system == "Linux":
#             # 检查是否有gnome-terminal或konsole
#             if self.command_exists("gnome-terminal"):
#                 return f"gnome-terminal --title 'SSH 终端 {script_index} ({script_name})' -- bash -c '{script_arg}'"
#             elif self.command_exists("konsole"):
#                 return f"konsole --title 'SSH 终端 {script_index} ({script_name})' -e 'bash -c {script_arg}'"
#             else:
#                 messagebox.showerror("错误", "未找到支持的终端模拟器 (需要 gnome-terminal 或 konsole)")
#                 return None
                
#         elif system == "Darwin":  # macOS
#             return f'''osascript -e 'tell application "Terminal" to do script "{script_arg}"' '''
            
#         elif system == "Windows":
#             # Windows 下使用 PowerShell
#             return f'''powershell -Command "Start-Process cmd -ArgumentList '/c, {script_arg}'"'''
            
#         else:
#             messagebox.showerror("错误", f"不支持的操作系统: {system}")
#             return None
    
#     def command_exists(self, cmd):
#         """检查命令是否存在"""
#         try:
#             subprocess.check_output(f"which {cmd}", shell=True, stderr=subprocess.STDOUT)
#             return True
#         except subprocess.CalledProcessError:
#             return False
    
#     def start_all_terminals(self):
#         """启动所有终端"""
#         # 验证基本配置
#         if not self.ssh_user_var.get() or not self.ssh_ip_var.get() or not self.ssh_password_var.get():
#             messagebox.showerror("错误", "请填写完整的SSH连接信息")
#             return
            
#         # 启动每个终端
#         for i in range(len(self.path_configs)):
#             cmd = self.get_terminal_command(i)
#             if cmd:
#                 try:
#                     subprocess.Popen(cmd, shell=True)
#                 except Exception as e:
#                     messagebox.showerror("错误", f"启动终端 {i+1} 失败: {str(e)}")
        
#         messagebox.showinfo("提示", f"已启动 {len(self.path_configs)} 个终端会话")

# if __name__ == "__main__":
#     # 检查是否安装了expect
#     try:
#         subprocess.check_output("which expect", shell=True, stderr=subprocess.STDOUT)
#     except subprocess.CalledProcessError:
#         print("错误: 未安装expect工具，请先安装。")
#         print("Ubuntu/Debian: sudo apt install expect")
#         print("CentOS/RHEL: sudo yum install expect")
#         print("macOS: brew install expect")
#         sys.exit(1)
        
#     root = tk.Tk()
#     app = SSHTerminalManager(root)
#     root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import os
import sys
import platform
from tkinter import font

class SSHTerminalManager:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH终端管理器")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        # 设置主题颜色
        self.colors = {
            "primary": "#2563eb",       # 主色调：蓝色
            "primary_light": "#3b82f6", # 亮一点的蓝色
            "primary_dark": "#1d4ed8",  # 深一点的蓝色
            "secondary": "#10b981",     # 辅助色：绿色
            "background": "#f8fafc",    # 背景色：浅灰
            "card": "#ffffff",          # 卡片背景：白色
            "text": "#1e293b",          # 文本颜色：深灰
            "text_light": "#64748b",    # 次要文本：中灰
            "border": "#e2e8f0",        # 边框颜色：浅灰
            "success": "#10b981",       # 成功色：绿色
            "error": "#ef4444",         # 错误色：红色
        }
        
        # 配置样式
        self.setup_styles()
        
        # 终端配置
        self.terminal_count = 5
        self.ssh_user = "hello"
        self.ssh_ip = "192.168.1.87"
        self.ssh_password = ""
        self.script_prefix = "video2gs_"
        self.working_dir = "/data/ycy/"
        self.env_command = "mamba activate 3dgs"
        
        # 路径配置列表
        self.path_configs = []
        
        # 创建UI
        self.create_widgets()
        self.generate_path_configs()
        
        # 添加窗口图标
        try:
            self.root.iconbitmap(default="")  # 可以替换为实际图标路径
        except:
            pass  # 忽略图标设置错误
    
    def setup_styles(self):
        """设置界面样式"""
        # 配置全局字体
        default_font = font.nametofont("TkDefaultFont")
        if platform.system() == "Windows":
            default_font.configure(family="SimHei", size=10)
        elif platform.system() == "Darwin":  # macOS
            default_font.configure(family="Heiti TC", size=10)
        else:  # Linux
            default_font.configure(family="WenQuanYi Micro Hei", size=10)
        self.root.option_add("*Font", default_font)
        
        # 设置背景色
        self.root.configure(bg=self.colors["background"])
        
        # 创建自定义样式
        self.style = ttk.Style()
        
        # 配置主题
        self.style.theme_use("clam")
        
        # 配置框架样式
        self.style.configure("TFrame", background=self.colors["background"])
        
        # 配置标签样式
        self.style.configure("TLabel", 
                            background=self.colors["background"],
                            foreground=self.colors["text"])
        
        # 配置标签框架样式
        self.style.configure("TLabelFrame",
                            background=self.colors["background"],
                            foreground=self.colors["text"])
        self.style.configure("TLabelFrame.Label",
                            font=("default", 10, "bold"),
                            padding=(5, 2, 5, 5))
        
        # 配置按钮样式
        self.style.configure("TButton",
                            background=self.colors["primary"],
                            foreground="white",
                            padding=(10, 5),
                            font=("default", 10, "bold"))
        self.style.map("TButton",
                      background=[("active", self.colors["primary_dark"]),
                                 ("pressed", self.colors["primary_dark"])],
                      foreground=[("active", "white"),
                                 ("pressed", "white")])
        
        # 配置输入框样式
        self.style.configure("TEntry",
                            fieldbackground=self.colors["card"],
                            bordercolor=self.colors["border"],
                            focusthickness=2,
                            focuscolor=self.colors["primary"],
                            padding=5)
        
        # 配置下拉框样式
        self.style.configure("TCombobox",
                            fieldbackground=self.colors["card"],
                            background=self.colors["card"],
                            bordercolor=self.colors["border"],
                            focusthickness=2,
                            focuscolor=self.colors["primary"])
        
        # 配置表格样式
        self.style.configure("Treeview",
                            background=self.colors["card"],
                            foreground=self.colors["text"],
                            fieldbackground=self.colors["card"],
                            bordercolor=self.colors["border"],
                            rowheight=25)
        self.style.configure("Treeview.Heading",
                            background=self.colors["primary"],
                            foreground="white",
                            font=("default", 10, "bold"),
                            padding=5)
        self.style.map("Treeview",
                      background=[("selected", self.colors["primary_light"])],
                      foreground=[("selected", "white")])
        
        # 配置滚动条样式
        self.style.configure("Vertical.TScrollbar",
                            background=self.colors["border"],
                            troughcolor=self.colors["background"],
                            arrowcolor=self.colors["text"])
    
    def create_widgets(self):
        """创建UI组件"""
        # 创建主框架并添加内边距
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加标题
        title_label = ttk.Label(main_frame, 
                               text="SSH终端管理器", 
                               font=("default", 16, "bold"),
                               foreground=self.colors["primary"])
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        # SSH配置区域 - 添加阴影效果的卡片
        ssh_card = ttk.Frame(main_frame, padding="15")
        ssh_card.pack(fill=tk.X, pady=(0, 15))
        ssh_card.configure(style="Card.TFrame")
        self.add_card_effect(ssh_card)
        
        ssh_frame = ttk.LabelFrame(ssh_card, text="SSH连接配置", padding="10")
        ssh_frame.pack(fill=tk.X)
        
        # SSH配置网格
        ssh_grid = ttk.Frame(ssh_frame)
        ssh_grid.pack(fill=tk.X)
        
        ttk.Label(ssh_grid, text="用户名:").grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.ssh_user_var = tk.StringVar(value=self.ssh_user)
        ttk.Entry(ssh_grid, textvariable=self.ssh_user_var, width=20).grid(row=0, column=1, padx=5, pady=10)
        
        ttk.Label(ssh_grid, text="服务器IP:").grid(row=0, column=2, padx=5, pady=10, sticky=tk.W)
        self.ssh_ip_var = tk.StringVar(value=self.ssh_ip)
        ttk.Entry(ssh_grid, textvariable=self.ssh_ip_var, width=20).grid(row=0, column=3, padx=5, pady=10)
        
        ttk.Label(ssh_grid, text="密码:").grid(row=0, column=4, padx=5, pady=10, sticky=tk.W)
        self.ssh_password_var = tk.StringVar(value=self.ssh_password)
        ttk.Entry(ssh_grid, textvariable=self.ssh_password_var, show="*", width=20).grid(row=0, column=5, padx=5, pady=10)
        
        ttk.Label(ssh_grid, text="终端数量:").grid(row=0, column=6, padx=5, pady=10, sticky=tk.W)
        self.terminal_count_var = tk.StringVar(value=str(self.terminal_count))
        ttk.Combobox(ssh_grid, textvariable=self.terminal_count_var, 
                    values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], 
                    width=5).grid(row=0, column=7, padx=5, pady=10)
        
        # 脚本配置区域
        script_card = ttk.Frame(main_frame, padding="15")
        script_card.pack(fill=tk.X, pady=(0, 15))
        self.add_card_effect(script_card)
        
        script_frame = ttk.LabelFrame(script_card, text="脚本配置", padding="10")
        script_frame.pack(fill=tk.X)
        
        script_grid = ttk.Frame(script_frame)
        script_grid.pack(fill=tk.X)
        
        ttk.Label(script_grid, text="脚本前缀:").grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.script_prefix_var = tk.StringVar(value=self.script_prefix)
        ttk.Entry(script_grid, textvariable=self.script_prefix_var, width=20).grid(row=0, column=1, padx=5, pady=10)
        
        ttk.Label(script_grid, text="工作目录:").grid(row=0, column=2, padx=5, pady=10, sticky=tk.W)
        self.working_dir_var = tk.StringVar(value=self.working_dir)
        ttk.Entry(script_grid, textvariable=self.working_dir_var, width=30).grid(row=0, column=3, padx=5, pady=10)
        
        ttk.Label(script_grid, text="环境命令:").grid(row=0, column=4, padx=5, pady=10, sticky=tk.W)
        self.env_command_var = tk.StringVar(value=self.env_command)
        ttk.Entry(script_grid, textvariable=self.env_command_var, width=30).grid(row=0, column=5, padx=5, pady=10)
        
        # 路径配置区域
        path_card = ttk.Frame(main_frame, padding="15")
        path_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.add_card_effect(path_card)
        
        path_frame = ttk.LabelFrame(path_card, text="脚本路径配置", padding="10")
        path_frame.pack(fill=tk.BOTH, expand=True)
        
        # 路径配置表格说明
        desc_label = ttk.Label(path_frame, 
                             text="双击单元格编辑路径", 
                             foreground=self.colors["text_light"],
                             font=("default", 9))
        desc_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 路径配置表格
        columns = ("script_name", "input_dir", "output_dir")
        self.path_tree = ttk.Treeview(path_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.path_tree.heading("script_name", text="脚本名称")
        self.path_tree.heading("input_dir", text="INPUT_DIR")
        self.path_tree.heading("output_dir", text="OUTPUT_DIR")
        
        # 设置列宽
        self.path_tree.column("script_name", width=150, anchor=tk.W)
        self.path_tree.column("input_dir", width=300, anchor=tk.W)
        self.path_tree.column("output_dir", width=300, anchor=tk.W)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(path_frame, orient=tk.VERTICAL, command=self.path_tree.yview)
        self.path_tree.configure(yscroll=scrollbar.set)
        
        # 布局表格和滚动条
        self.path_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 创建按钮容器，使按钮之间有更多空间
        btn_container = ttk.Frame(button_frame)
        btn_container.pack(fill=tk.X)
        
        ttk.Button(btn_container, text="刷新配置", command=self.refresh_configs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_container, text="自动填充示例路径", command=self.fill_example_paths).pack(side=tk.LEFT, padx=5)
        
        # 启动按钮使用强调色
        start_btn = ttk.Button(btn_container, text="启动所有终端", command=self.start_all_terminals)
        start_btn.pack(side=tk.RIGHT, padx=5)
        start_btn.configure(style="Accent.TButton")
        self.style.configure("Accent.TButton", background=self.colors["secondary"])
        self.style.map("Accent.TButton",
                      background=[("active", "#059669"), ("pressed", "#059669")])
    
    def add_card_effect(self, widget):
        """为组件添加卡片效果"""
        if platform.system() == "Linux":
            # Linux下添加边框和阴影效果
            widget.configure(relief=tk.RAISED, borderwidth=1)
            widget.configure(style="Card.TFrame")
            self.style.configure("Card.TFrame", 
                                background=self.colors["card"],
                                bordercolor=self.colors["border"])
        else:
            # 其他系统简化处理
            widget.configure(relief=tk.SOLID, borderwidth=1)
            widget.configure(style="Card.TFrame")
            self.style.configure("Card.TFrame", 
                                background=self.colors["card"],
                                bordercolor=self.colors["border"])
    
    def generate_path_configs(self):
        """生成路径配置列表"""
        # 清空现有数据
        for item in self.path_tree.get_children():
            self.path_tree.delete(item)
            
        self.path_configs = []
        count = int(self.terminal_count_var.get())
        
        for i in range(1, count + 1):
            script_name = f"{self.script_prefix_var.get()}{i}.sh"
            self.path_configs.append({
                "script_name": script_name,
                "input_dir": "",
                "output_dir": ""
            })
            self.path_tree.insert("", tk.END, values=(script_name, "", ""))
        
        # 绑定双击事件用于编辑，添加动画效果
        self.path_tree.bind("<Double-1>", self.edit_cell)
        self.path_tree.bind("<Enter>", lambda e: self.on_enter(e))
        self.path_tree.bind("<Leave>", lambda e: self.on_leave(e))
    
    def on_enter(self, event):
        """鼠标进入表格时的效果"""
        region = self.path_tree.identify_region(event.x, event.y)
        if region == "cell":
            self.root.config(cursor="hand2")
    
    def on_leave(self, event):
        """鼠标离开表格时的效果"""
        self.root.config(cursor="")
    
    def edit_cell(self, event):
        """编辑表格单元格，添加动画效果"""
        region = self.path_tree.identify_region(event.x, event.y)
        if region != "cell":
            return
            
        column = int(self.path_tree.identify_column(event.x).replace("#", "")) - 1
        item = self.path_tree.identify_row(event.y)
        row = self.path_tree.index(item)
        
        if row < 0 or row >= len(self.path_configs):
            return
            
        # 获取当前值
        current_value = self.path_tree.item(item, "values")[column]
        
        # 高亮显示正在编辑的行
        self.path_tree.selection_set(item)
        
        # 请求用户输入新值
        new_value = simpledialog.askstring(
            "编辑路径", 
            f"请输入{self.path_tree.heading(f'#{column+1}')['text']}",
            initialvalue=current_value
        )
        
        if new_value is not None:
            # 更新表格
            values = list(self.path_tree.item(item, "values"))
            values[column] = new_value
            self.path_tree.item(item, values=values)
            
            # 更新配置数据
            config_key = ["script_name", "input_dir", "output_dir"][column]
            self.path_configs[row][config_key] = new_value
        
        # 取消选中状态
        self.path_tree.selection_remove(item)
    
    def refresh_configs(self):
        """刷新配置列表，添加动画效果"""
        # 添加刷新动画
        self.root.config(cursor="wait")
        self.root.update()
        
        self.generate_path_configs()
        
        # 恢复光标并显示提示
        self.root.config(cursor="")
        self.show_notification("配置已刷新")
    
    def fill_example_paths(self):
        """填充示例路径"""
        count = int(self.terminal_count_var.get())
        
        for i in range(count):
            item = self.path_tree.get_children()[i]
            script_index = i + 1
            
            input_dir = f"/data/input/set{script_index}"
            output_dir = f"/data/output/result{script_index}"
            
            # 更新表格
            self.path_tree.item(item, values=(
                self.path_configs[i]["script_name"],
                input_dir,
                output_dir
            ))
            
            # 更新配置数据
            self.path_configs[i]["input_dir"] = input_dir
            self.path_configs[i]["output_dir"] = output_dir
        
        self.show_notification("已填充示例路径")
    
    def show_notification(self, message, is_error=False):
        """显示通知消息"""
        # 创建临时通知窗口
        notification = tk.Toplevel(self.root)
        notification.overrideredirect(True)  # 无边框
        notification.attributes("-topmost", True)
        
        # 计算位置（底部中央）
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - 150
        y = self.root.winfo_y() + self.root.winfo_height() - 80
        notification.geometry(f"300x50+{x}+{y}")
        
        # 设置样式
        bg_color = self.colors["error"] if is_error else self.colors["primary"]
        notification.configure(bg=bg_color)
        
        # 添加消息
        label = ttk.Label(notification, 
                         text=message, 
                         background=bg_color,
                         foreground="white",
                         font=("default", 10, "bold"))
        label.pack(expand=True)
        
        # 3秒后自动关闭
        self.root.after(3000, notification.destroy)
    
    def get_terminal_command(self, index):
        """获取终端启动命令"""
        config = self.path_configs[index]
        script_index = index + 1
        
        # 检查配置是否完整
        if not config["input_dir"] or not config["output_dir"]:
            self.show_notification(f"请填写第{script_index}个脚本的路径配置", is_error=True)
            return None
            
        # 获取配置参数
        user = self.ssh_user_var.get()
        ip = self.ssh_ip_var.get()
        password = self.ssh_password_var.get()
        script_name = config["script_name"]
        work_dir = self.working_dir_var.get()
        env_cmd = self.env_command_var.get()
        
        # 生成expect脚本内容
        expect_script = f'''
            spawn ssh {user}@{ip}
            expect "password:"
            send "{password}\r"
            expect "{user}@*"
            
            send "{env_cmd}\r"
            expect "(*) {user}@*"
            send "cd {work_dir}\r"
            expect "(*) {user}@*:{work_dir}"
            
            send "echo 请修改 {script_name} 中的路径...\r"
            send "echo 当前预设路径:\r"
            send "echo INPUT_DIR={config["input_dir"]}\r"
            send "echo OUTPUT_DIR={config["output_dir"]}\r"
            send "sleep 2\r"
            
            send "vim {script_name}\r"
            expect eof
            
            send "./{script_name}\r"
            interact
        '''
        
        # 根据操作系统选择终端命令
        system = platform.system()
        script_arg = 'expect -c \'{}\''.format(expect_script.replace('\n', ' ').replace('\'', '\\\''))
        
        if system == "Linux":
            # 检查是否有gnome-terminal或konsole
            if self.command_exists("gnome-terminal"):
                return f"gnome-terminal --title 'SSH 终端 {script_index} ({script_name})' -- bash -c '{script_arg}'"
            elif self.command_exists("konsole"):
                return f"konsole --title 'SSH 终端 {script_index} ({script_name})' -e 'bash -c {script_arg}'"
            else:
                self.show_notification("未找到支持的终端模拟器 (需要 gnome-terminal 或 konsole)", is_error=True)
                return None
                
        elif system == "Darwin":  # macOS
            return f'''osascript -e 'tell application "Terminal" to do script "{script_arg}"' '''
            
        elif system == "Windows":
            # Windows 下使用 PowerShell
            return f'''powershell -Command "Start-Process cmd -ArgumentList '/c, {script_arg}'"'''
            
        else:
            self.show_notification(f"不支持的操作系统: {system}", is_error=True)
            return None
    
    def command_exists(self, cmd):
        """检查命令是否存在"""
        try:
            subprocess.check_output(f"which {cmd}", shell=True, stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def start_all_terminals(self):
        """启动所有终端"""
        # 验证基本配置
        if not self.ssh_user_var.get() or not self.ssh_ip_var.get() or not self.ssh_password_var.get():
            self.show_notification("请填写完整的SSH连接信息", is_error=True)
            return
            
        # 添加加载动画
        self.root.config(cursor="wait")
        self.root.update()
            
        # 启动每个终端
        success_count = 0
        for i in range(len(self.path_configs)):
            cmd = self.get_terminal_command(i)
            if cmd:
                try:
                    subprocess.Popen(cmd, shell=True)
                    success_count += 1
                except Exception as e:
                    self.show_notification(f"启动终端 {i+1} 失败: {str(e)}", is_error=True)
        
        # 恢复光标
        self.root.config(cursor="")
        
        if success_count > 0:
            self.show_notification(f"已成功启动 {success_count} 个终端会话")
        else:
            self.show_notification("启动终端失败，请检查配置", is_error=True)

if __name__ == "__main__":
    # 检查是否安装了expect
    try:
        subprocess.check_output("which expect", shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("错误: 未安装expect工具，请先安装。")
        print("Ubuntu/Debian: sudo apt install expect")
        print("CentOS/RHEL: sudo yum install expect")
        print("macOS: brew install expect")
        sys.exit(1)
        
    root = tk.Tk()
    app = SSHTerminalManager(root)
    root.mainloop()
