# 文件说明
```
|-- run.sh                                 # 配置环境训练脚本
|-- readme.md                              # 项目说明
|-- finance_maodun/
    |-- roundb                             # B榜的数据
    |-- requirements.txt                   # 需要的环境依赖
    |-- main.py                            # 程序入口
    |-- llm.py                             # 调用大语言模型
    |-- template.py                        # 存放prompt语句

|-- data/
    |-- train_qwen2_7b_finance_maodun.yaml # lora微调的配置文件
    |-- dataset_info.json                  # lora微调的配置文件
    |-- finance_maodun.json                # 微调训练数据集
    |-- merge_finance_maodun.yaml          # 合并lora的配置文件
    |-- result.json                        # 个人运行后得到的最终结果
    |-- training_loss.png                  # 个人训练时的损失曲线
|-- LLaMA-Factory/                         # lora微调的工具仓库
    ...
|-- models/
    |-- qwen2-7b-instruct                  # qwen2原始模型（下载后放入此处）
    |-- qwen2-7b-instruct-finance-maodun   # lora微调后的qwen2模型
```
# 运行方法

### 1.下载`qwen2-7b-instruct`模型，然后命名为`qwen2-7b-instruct`放入`models`文件夹下。下载方式有两种：
1. 使用hugging-face镜像下载
切换到finance文件夹下然后运行下面的命令：
```
pip install -U huggingface_hub
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download --resume-download Qwen/Qwen2-7B-Instruct models/qwen2-7b-instruct
```
2. 直接在网盘链接中下载：<https://disk.pku.edu.cn/link/AAE52359C6FF1C41829C3F0C8467031EC5>(提取码：Z7AC)
### 2.加载B榜数据集
B榜数据集放在`finance_maodun/roundb`文件夹下（已经放好了）

### 3. 运行`run.sh`（创建虚拟环境，下载LLaMA-Factory，微调模型）
```
chmod +x run.sh
./run.sh
```
运行成功后会生成`models/qwen2-7b-instruct-finance-maodun`模型文件。


`run.sh`脚本可能运行错误，此时可以把脚本中的命令逐个在命令行运行。

### 4. 切换工作目录为`finance_maodun`
```
cd finance_maodun
```
### 5. 运行`main.py`得到预测结果
`main.py`的参数如下：
```
model_path   # 微调后的模型路径，需要将上一步得到的模型路径填入（需要更改）
input_folder # B榜文件夹，默认为roundb（不需要更改）
output_file  # 识别结果保存文件，默认为result.json（不需要更改）
```


