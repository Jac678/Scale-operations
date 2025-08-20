import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import os
import sys
import platform
import threading
from tkinter import font
import time

class SSHTerminalManager:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH终端批量管理器")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 确保中文显示正常
        self.setup_fonts()
        
        # 配置参数
        self.ssh_user = "hello"
        self.ssh_ip = "192.168.1.87"
        self.ssh_password = ""
        self.terminal_count = 3
        self.script_prefix = "video2gs_"
        self.working_dir = "/data/ycy/"
        self.env_command = "mamba activate 3dgs"
        
        # 脚本内容模板
        self.script_template = '''#!/bin/bash

# 设置默认值
CUDA_VISIBLE_DEVICES=1
INPUT_DIR="/home/btl/桌面/Video_0807/A_0807.mp4"
OUTPUT_DIR="/home/btl/桌面/Test_01/"
# INPUT_DIR="x_video/normal_video.mp4"
# OUTPUT_DIR="x_video/"
OUT_NUM=1
OVERLAP=10
# SINGLE,AUTO 两种模式
CAMREA_MODEL="SINGLE"
# OPENCV（推荐）,SIMPLE_PINHOLE
IMAGE_OPSIONS="SIMPLE_PINHOLE"
random_number=$(head -20 /dev/urandom | cksum | cut -c 1-4)
# 输入是否为全景图
FOVIMAGE="no"
# 是否使用loftr
USE_LOFTR="no"

if [ "$USE_LOFTR" == "yes" ]; then
  NO_LOFTR=""
else
  NO_LOFTR="--noloftr"
fi

# 打印参数
echo "全景图处理: $FOVIMAGE"
echo "输入目录: $INPUT_DIR"
echo "输出目录: $OUTPUT_DIR"
echo "输出编号: $OUT_NUM"
echo "是否使用loftr: $USE_LOFTR "
echo "Camera Model: $CAMREA_MODEL"
echo "Image Options: $IMAGE_OPSIONS"
echo "随机端口：$random_number"
echo "CUDA 设备: $CUDA_VISIBLE_DEVICES"

# 等待用户确认
read -p "按Ctrl-C结束脚本,按回车键继续运行脚本..."

# 创建文件夹
mkdir -p "$OUTPUT_DIR"

# 视频抽帧
if [ $FOVIMAGE == "yes" ]; then
  V2I_P="$OUTPUT_DIR/360images"
else
  V2I_P="$OUTPUT_DIR/input"
fi
if [ -d "$V2I_P" ]; then
  read -p "视频已抽帧，是否删除重新抽帧？(y/n): " DELETE_360FOLDER
  if [ "$DELETE_360FOLDER" == "y" ]; then
    rm -rf "$V2I_P"
    mkdir -p "$V2I_P"
    ffmpeg -i "$INPUT_DIR" -f image2 -r 1 -qscale:v 2 "$V2I_P/IMG_%03d.jpg"
  else
    echo "跳过视频抽帧。"
  fi
else
  mkdir -p "$V2I_P"
  ffmpeg -i "$INPUT_DIR" -f image2 -r 1 -qscale:v 2 "$V2I_P/IMG_%03d.jpg"
fi

# 转换全景图
if [ "$FOVIMAGE" == "yes" ]; then
  if [ -d "$OUTPUT_DIR/input" ]; then
    read -p "目录 \"$OUTPUT_DIR/input\" 已存在。是否删除重新转换全景图？(y/n): " DELETE_INPUTFOLDER
    if [ "$DELETE_INPUTFOLDER" == "y" ]; then
      rm -rf "$OUTPUT_DIR/input"
      mkdir -p "$OUTPUT_DIR/input"
      /mnt/tzn/cubeMap/build/panorama2CubeMap "$OUTPUT_DIR/360images/" "$OUTPUT_DIR/input/"
    else
      echo "跳过此步骤。"
    fi
  else
    mkdir -p "$OUTPUT_DIR/input"
    /mnt/tzn/cubeMap/build/panorama2CubeMap "$OUTPUT_DIR/360images/" "$OUTPUT_DIR/input/"
  fi
fi

# 激活环境
# conda activate 3dgs

# 高斯重建
GS_OUTPUT_DIR="$OUTPUT_DIR/output/$OUT_NUM"
CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES python "/home/btl/桌面/Relightable 3D Gaussian/convert.py" -s $OUTPUT_DIR
CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES python "/home/btl/桌面/Relightable 3D Gaussian/Relightable3DGaussian/train.py" -s $OUTPUT_DIR -m $GS_OUTPUT_DIR  --port $random_number 
echo "输出目录: $GS_OUTPUT_DIR"
'''
        
        # 路径配置列表
        self.path_configs = []
        for i in range(1, self.terminal_count + 1):
            self.path_configs.append({
                "script_name": f"{self.script_prefix}{i}.sh",
                "input_dir": f"/home/btl/桌面/Video_0807/A_0807_{i}.mp4",
                "output_dir": f"/home/btl/桌面/Test_0{i}/"
            })
        
        # 创建UI
        self.create_widgets()
        
        # 标记是否正在执行任务
        self.is_working = False
    
    def setup_fonts(self):
        """设置字体以确保中文正常显示"""
        default_font = font.nametofont("TkDefaultFont")
        if platform.system() == "Linux":
            default_font.configure(family="WenQuanYi Micro Hei", size=10)
        elif platform.system() == "Windows":
            default_font.configure(family="SimHei", size=10)
        elif platform.system() == "Darwin":  # macOS
            default_font.configure(family="Heiti TC", size=10)
        self.root.option_add("*Font", default_font)
    
    def create_widgets(self):
        """创建UI组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建状态标签
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="#666")
        status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # SSH配置区域
        ssh_frame = ttk.LabelFrame(main_frame, text="SSH连接配置", padding="10")
        ssh_frame.pack(fill=tk.X, pady=(0, 15))
        
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
        
        # 路径配置区域
        path_frame = ttk.LabelFrame(main_frame, text="脚本路径配置", padding="10")
        path_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 路径配置表格说明
        desc_label = ttk.Label(path_frame, text="双击单元格编辑路径")
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
        
        # 填充表格数据
        for config in self.path_configs:
            self.path_tree.insert("", tk.END, values=(
                config["script_name"],
                config["input_dir"],
                config["output_dir"]
            ))
        
        # 绑定双击事件用于编辑
        self.path_tree.bind("<Double-1>", self.edit_cell)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 创建按钮
        self.start_btn = ttk.Button(button_frame, text="启动所有终端", command=self.start_all_terminals)
        self.start_btn.pack(side=tk.RIGHT, padx=5)
        
        self.generate_btn = ttk.Button(button_frame, text="生成脚本", command=self.generate_scripts)
        self.generate_btn.pack(side=tk.RIGHT, padx=5)
    
    def set_status(self, message):
        """更新状态标签"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def edit_cell(self, event):
        """编辑表格单元格 - 优化响应速度"""
        if self.is_working:
            messagebox.showinfo("提示", "正在执行任务，请稍后再试")
            return
            
        region = self.path_tree.identify_region(event.x, event.y)
        if region != "cell":
            return
            
        try:
            column = int(self.path_tree.identify_column(event.x).replace("#", "")) - 1
            item = self.path_tree.identify_row(event.y)
            row = self.path_tree.index(item)
            
            if row < 0 or row >= len(self.path_configs):
                return
                
            # 获取当前值
            current_value = self.path_tree.item(item, "values")[column]
            
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
        except Exception as e:
            messagebox.showerror("错误", f"编辑失败: {str(e)}")
    
    def generate_scripts(self):
        """生成5个脚本文件 - 在后台线程执行"""
        if self.is_working:
            messagebox.showinfo("提示", "正在执行任务，请稍后再试")
            return
            
        # 启动后台线程执行生成脚本的任务
        self.is_working = True
        self.generate_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        self.set_status("正在生成脚本...")
        
        thread = threading.Thread(target=self._generate_scripts_background)
        thread.daemon = True
        thread.start()
    
    def _generate_scripts_background(self):
        """后台生成脚本文件"""
        try:
            for i, config in enumerate(self.path_configs):
                # 更新状态
                self.set_status(f"正在生成脚本 {i+1}/{len(self.path_configs)}...")
                
                script_name = config["script_name"]
                input_dir = config["input_dir"]
                output_dir = config["output_dir"]
                
                # 替换脚本中的INPUT_DIR和OUTPUT_DIR
                script_content = self.script_template.replace(
                    'INPUT_DIR="/home/btl/桌面/Video_0807/A_0807.mp4"',
                    f'INPUT_DIR="{input_dir}"'
                ).replace(
                    'OUTPUT_DIR="/home/btl/桌面/Test_01/"',
                    f'OUTPUT_DIR="{output_dir}"'
                )
                
                # 保存脚本文件
                with open(script_name, 'w') as f:
                    f.write(script_content)
                
                # 赋予执行权限
                os.chmod(script_name, 0o755)
                
                # 短暂延迟，避免资源竞争
                time.sleep(0.1)
            
            # 生成完成，更新UI
            self.root.after(0, lambda: messagebox.showinfo("成功", "已生成5个脚本文件"))
            self.set_status("脚本生成完成")
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"生成脚本失败: {str(e)}"))
            self.set_status(f"生成脚本失败: {str(e)}")
        finally:
            # 恢复UI状态
            self.root.after(0, lambda: self.generate_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL))
            self.is_working = False
    
    def get_terminal_command(self, index):
        """获取终端启动命令"""
        config = self.path_configs[index]
        script_index = index + 1
        
        # 获取配置参数
        user = self.ssh_user_var.get()
        ip = self.ssh_ip_var.get()
        password = self.ssh_password_var.get()
        script_name = config["script_name"]
        work_dir = self.working_dir
        env_cmd = self.env_command
        
        # 验证配置
        if not user or not ip or not password:
            return None, "请填写完整的SSH连接信息"
        
        # 生成expect脚本内容
        expect_script = f'''
            spawn ssh {user}@{ip}
            expect "password:"
            send "{password}\\r"
            expect "{user}@*"
            
            send "{env_cmd}\\r"
            expect "\\(\\*\\) {user}@*"
            send "cd {work_dir}\\r"
            expect "\\(\\*\\) {user}@*:{work_dir}"
            
            # 检查脚本是否存在，如果不存在则提示
            send "if [ ! -f "{script_name}" ]; then echo "脚本 {script_name} 不存在"; sleep 5; fi\\r"
            expect "(*) {user}@*"
            
            send "vim {script_name}\\r"
            interact
        '''
        
        # 根据操作系统选择终端命令
        system = platform.system()
        script_arg = 'expect -c \'{}\''.format(expect_script.replace('\n', ' ').replace('\'', '\\\''))
        
        if system == "Linux":
            # 检查是否有gnome-terminal或konsole
            if self.command_exists("gnome-terminal"):
                cmd = f"gnome-terminal --title 'SSH 终端 {script_index} ({script_name})' -- bash -c '{script_arg}'"
            elif self.command_exists("konsole"):
                cmd = f"konsole --title 'SSH 终端 {script_index} ({script_name})' -e 'bash -c {script_arg}'"
            elif self.command_exists("xterm"):
                cmd = f"xterm -T 'SSH 终端 {script_index} ({script_name})' -e 'bash -c {script_arg}'"
            else:
                return None, "未找到支持的终端模拟器 (需要 gnome-terminal, konsole 或 xterm)"
        elif system == "Darwin":  # macOS
            cmd = f'''osascript -e 'tell application "Terminal" to do script "{script_arg}"' '''
        elif system == "Windows":
            cmd = f'''powershell -Command "Start-Process cmd -ArgumentList '/c, {script_arg}'"'''
        else:
            return None, f"不支持的操作系统: {system}"
            
        return cmd, None
    
    def command_exists(self, cmd):
        """检查命令是否存在"""
        try:
            subprocess.check_output(f"which {cmd}", shell=True, stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def start_all_terminals(self):
        """启动所有终端 - 在后台线程执行"""
        if self.is_working:
            messagebox.showinfo("提示", "正在执行任务，请稍后再试")
            return
            
        # 检查是否安装了expect
        if not self.command_exists("expect"):
            messagebox.showerror("错误", "未安装expect工具，请先安装：\nUbuntu/Debian: sudo apt install expect\nCentOS/RHEL: sudo yum install expect\nmacOS: brew install expect")
            return
        
        # 先询问是否要生成脚本
        generate_first = messagebox.askyesno("确认", "是否先生成/更新脚本文件？")
        if generate_first:
            # 同步生成脚本
            self._generate_scripts_background()
            # 等待生成完成
            while self.is_working:
                time.sleep(0.1)
                self.root.update_idletasks()
        
        # 启动后台线程执行启动终端的任务
        self.is_working = True
        self.generate_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        self.set_status("正在启动终端...")
        
        thread = threading.Thread(target=self._start_all_terminals_background)
        thread.daemon = True
        thread.start()
    
    def _start_all_terminals_background(self):
        """后台启动所有终端"""
        success_count = 0
        error_messages = []
        
        for i in range(len(self.path_configs)):
            # 更新状态
            self.set_status(f"正在启动终端 {i+1}/{len(self.path_configs)}...")
            
            cmd, error = self.get_terminal_command(i)
            if error:
                error_messages.append(f"终端 {i+1}: {error}")
                continue
                
            if cmd:
                try:
                    subprocess.Popen(cmd, shell=True)
                    success_count += 1
                    # 延迟一下，避免同时启动多个终端导致系统卡顿
                    time.sleep(0.5)
                except Exception as e:
                    error_messages.append(f"启动终端 {i+1} 失败: {str(e)}")
        
        # 更新UI显示结果
        self.root.after(0, lambda: self._show_start_result(success_count, error_messages))
        
        # 恢复UI状态
        self.set_status(f"已启动 {success_count} 个终端")
        self.root.after(0, lambda: self.generate_btn.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL))
        self.is_working = False
    
    def _show_start_result(self, success_count, errors):
        """显示启动结果"""
        if success_count > 0:
            result_msg = f"已成功启动 {success_count} 个终端会话"
            if errors:
                result_msg += "\n\n错误信息:\n" + "\n".join(errors)
            messagebox.showinfo("启动结果", result_msg)
        else:
            messagebox.showerror("启动失败", "所有终端启动失败:\n" + "\n".join(errors))

if __name__ == "__main__":
    # 确保中文显示正常
    root = tk.Tk()
    app = SSHTerminalManager(root)
    root.mainloop()

