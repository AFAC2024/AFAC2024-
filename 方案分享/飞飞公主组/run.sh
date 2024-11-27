#!/bin/bash

# 定义虚拟环境名称
ENV_NAME="my_env"

# 创建conda环境
conda create -n $ENV_NAME python=3.10.13 -y

# 初始化conda
if conda init; then
    echo "conda 初始化成功"
else
    echo "conda 初始化失败，请检查 conda 配置"
    exit 1
fi

# 重新加载 shell 配置文件
source ~/.bashrc

# 激活conda环境
if conda activate $ENV_NAME; then
    echo "已进入conda环境 $ENV_NAME"
else
    echo "激活环境失败，请检查 conda 配置"
    exit 1
fi

echo "正在安装LLaMa Factory"

# 克隆仓库
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git

# 进入仓库目录
cd LLaMA-Factory

# 安装依赖
pip install -e ".[torch,metrics]"

pip install tqdm python-docx

cp data/dataset_info.json LLaMA-Factory/data

cp data/finance_maodun.json LLaMA-Factory/data

# 输出训练信息
echo "开始使用LLaMa Factory进行训练"

llamafactory-cli train ../data/train_qwen2_7b_finance_maodun.yaml

llamafactory-cli export ../data/merge_finance_maodun.yaml

cd ../finance_maodun

python mainplus.py
