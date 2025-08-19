#!/bin/bash

# 检查是否提供了密码参数
if [ $# -ne 1 ]; then
    echo "使用方法: $0 <ssh_password>"
    exit 1
fi

SSH_PASSWORD=$1
SSH_USER="hello"
SSH_IP="192.168.1.87"
NUM_TERMINALS=5

# 循环创建并打开多个终端
for ((i=1; i<=NUM_TERMINALS; i++)); do
    # 判断当前系统使用的终端模拟器
    if command -v gnome-terminal &> /dev/null; then
        # GNOME桌面环境
        gnome-terminal --title="SSH Terminal $i" -- bash -c "
            # 自动输入密码登录SSH
            expect -c '
                spawn ssh $SSH_USER@$SSH_IP
                expect \"password: \"
                send \"$SSH_PASSWORD\r\"
                expect \"$SSH_USER@*\"
                send \"mamba activate 3dgs\r\"
                expect \"(3dgs) $SSH_USER@*\"
                send \"cd /data/ycy/\r\"
                expect \"(3dgs) $SSH_USER@*:/data/ycy\"
                send \"vim video2gs_1.sh\r\"
                interact
            '
        "
    elif command -v konsole &> /dev/null; then
        # KDE桌面环境
        konsole --title "SSH Terminal $i" -e bash -c "
            expect -c '
                spawn ssh $SSH_USER@$SSH_IP
                expect \"password: \"
                send \"$SSH_PASSWORD\r\"
                expect \"$SSH_USER@*\"
                send \"mamba activate 3dgs\r\"
                expect \"(3dgs) $SSH_USER@*\"
                send \"cd /data/ycy/\r\"
                expect \"(3dgs) $SSH_USER@*:/data/ycy\"
                send \"vim video2gs_1.sh\r\"
                interact
            '
        "
    else
        echo "不支持的终端环境，请手动安装gnome-terminal或konsole"
        exit 1
    fi
    
    # 稍微延迟一下，避免同时打开多个终端导致系统卡顿
    sleep 0.5
done
