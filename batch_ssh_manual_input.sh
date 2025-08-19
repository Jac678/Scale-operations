#!/bin/bash
# 批量SSH登录，手动输入路径后运行脚本的脚本

# 检查参数是否正确
if [ $# -ne 1 ]; then
    echo "使用方法: $0 <ssh_password>"
    exit 1
fi

# 配置参数
SSH_PASSWORD="$1"
SSH_USER="hello"
SSH_IP="192.168.1.87"
NUM_TERMINALS=5
BASE_SCRIPT="video2gs"
WORK_DIR="/data/ycy"

# 检查终端类型
if ! command -v gnome-terminal &> /dev/null && ! command -v konsole &> /dev/null; then
    echo "错误：未检测到支持的终端模拟器（需要gnome-terminal或konsole）"
    exit 1
fi

# 批量创建终端并执行操作
for ((i=1; i<=NUM_TERMINALS; i++)); do
    SCRIPT_NUM=$i
    SCRIPT_FILE="${BASE_SCRIPT}_${SCRIPT_NUM}.sh"
    
    # 根据终端类型选择命令
    if command -v gnome-terminal &> /dev/null; then
        TERMINAL_CMD="gnome-terminal --title 'SSH Terminal $i (编辑 $SCRIPT_FILE)' -- bash -c"
    else
        TERMINAL_CMD="konsole --title 'SSH Terminal $i (编辑 $SCRIPT_FILE)' -e bash -c"
    fi

    # 执行终端命令
    $TERMINAL_CMD "
        # 使用expect自动处理SSH登录
        expect -c '
            spawn ssh $SSH_USER@$SSH_IP
            expect \"password: \"
            send \"$SSH_PASSWORD\r\"
            expect \"$SSH_USER@*\"
            
            # 激活环境并进入工作目录
            send \"mamba activate 3dgs\r\"
            expect \"(3dgs) $SSH_USER@*\"
            send \"cd $WORK_DIR\r\"
            expect \"(3dgs) $SSH_USER@*:$WORK_DIR\"
            
            # 提示用户即将编辑的文件
            send \"echo 即将编辑 $SCRIPT_FILE...\r\"
            send \"echo 请修改 INPUT_DIR 和 OUTPUT_DIR 后保存退出\r\"
            send \"echo 修改完成后将自动运行脚本...\r\"
            send \"sleep 2\r\"
            
            # 编辑对应脚本（等待用户手动修改）
            send \"vim $SCRIPT_FILE\r\"
            expect eof  # 等待用户完成vim操作并退出
            
            # 用户完成编辑后，运行脚本
            send \"echo 开始运行 $SCRIPT_FILE...\r\"
            send \"./$SCRIPT_FILE\r\"
            interact  # 保持终端交互，查看运行结果
        '
    " &  # 后台运行终端，避免阻塞
    
    # 延迟创建，防止资源竞争
    sleep 1
done

echo "已启动${NUM_TERMINALS}个终端，每个终端将："
echo "1. 自动登录到 $SSH_USER@$SSH_IP"
echo "2. 打开对应的 video2gs_X.sh 文件"
echo "3. 等待你手动修改 INPUT_DIR 和 OUTPUT_DIR"
echo "4. 保存退出Vim后自动运行脚本"
