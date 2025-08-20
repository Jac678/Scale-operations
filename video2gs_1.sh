#!/bin/bash

# 设置默认值
CUDA_VISIBLE_DEVICES=1
INPUT_DIR="/data/sjy/data/25.4.1gsc/IMG_1363.MOV"
OUTPUT_DIR="/data/zh/25.4.1gsc"
OUT_NUM=0
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
CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES python /data/ycy/3DGS/convert.py -s $OUTPUT_DIR
CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES python /data/ycy/3DGS/train.py -s $OUTPUT_DIR -m $GS_OUTPUT_DIR  --port $random_number --save_iterations 30000
echo "输出目录: $GS_OUTPUT_DIR"

