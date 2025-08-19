#!/bin/bash
# 自动生成的SSH批量操作脚本
# 生成时间: 2025/8/19 11:41:47

# 配置参数
SSH_PASSWORD="ABCabc123"
SSH_USER="hello"
SSH_IP="192.168.1.87"
NUM_TERMINALS=5
BASE_SCRIPT="video2gs_"
WORK_DIR="/data/ycy/"
ENV_COMMAND="mamba activate 3dgs"

# 检查依赖
if ! command -v expect &> /dev/null; then
    echo "错误：未安装expect工具，请先安装"
    exit 1
fi

if ! command -v gnome-terminal &> /dev/null && ! command -v konsole &> /dev/null; then
    echo "错误：未检测到支持的终端模拟器"
    exit 1
fi

# 目录配置
declare -a INPUT_DIRS=(
    "/data/shz/0710_Video/600x400x280_Gray.mp4"
    "/data/shz/0715_Video/Video/400x300x270.mp4"
    "/data/shz/0716_Video/DaBZ_0716.mp4"
    "/data/shz/0718_Video/Sanjiao/Sanjiao_001.mp4"
    "/data/shz/0721_Video/0721_SJ.mp4"
)

declare -a OUTPUT_DIRS=(
    "/data/shz/0710_Video/600x400x280/"
    "/data/shz/0715_Video/Video/400x300x270/"
    "/data/shz/0716_Video/DaBZ/"
    "/data/shz/0718_Video/Sanjiao/Sanjiao/"
    "/data/shz/0721_Video/0721/"
)

# 启动终端会话
for ((i=1; i<=NUM_TERMINALS; i++)); do
    SCRIPT_NUM=$i
    INPUT_DIR="${INPUT_DIRS[$i-1]}"
    OUTPUT_DIR="${OUTPUT_DIRS[$i-1]}"
    SCRIPT_FILE="${BASE_SCRIPT}${SCRIPT_NUM}.sh"
    
    # 选择终端类型
    if command -v gnome-terminal &> /dev/null; then
        TERMINAL_CMD="gnome-terminal --title 'SSH Terminal $i ($SCRIPT_FILE)' -- bash -c"
    else
        TERMINAL_CMD="konsole --title 'SSH Terminal $i ($SCRIPT_FILE)' -e bash -c"
    fi

    # 执行终端命令
    $TERMINAL_CMD "
        expect -c '
            spawn ssh $SSH_USER@$SSH_IP
            expect "password: "
            send "$SSH_PASSWORD"
            expect "$SSH_USER@*"
            
            # 激活环境并进入工作目录
            send "$ENV_COMMAND"
            expect "(*) $SSH_USER@*"
            send "cd $WORK_DIR"
            expect "(*) $SSH_USER@*:$WORK_DIR"
            
            # 提示信息
            send "echo 正在编辑 $SCRIPT_FILE..."
            send "echo 请确认或修改以下路径："
            send "echo INPUT_DIR: $INPUT_DIR"
            send "echo OUTPUT_DIR: $OUTPUT_DIR"
            send "sleep 3"
            
            # 编辑脚本
            send "vim $SCRIPT_FILE"
            expect eof  # 等待用户完成编辑
            
            # 运行脚本
            send "echo 开始运行 $SCRIPT_FILE..."
            send "./$SCRIPT_FILE"
            interact
        '
    " &
    
    sleep 1
done

echo "已启动所有 $NUM_TERMINALS 个终端会话"
