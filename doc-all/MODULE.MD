# 主观题评分模型

## 一、目录结构
```
module[工作目录] 需要设置为Sources Root
|─config 配置文件所在目录
|─ERNIE ERNIE目录
│  │  dict.wordseg.pickle   词典文件
│  │  ERNIE_Tiny.py         ERNIE-Tiny网络结构
│  │  ernie_tiny_config.json    ERNIE-Tiny配置文件
│  │  spm_cased_simp_sampled.model  分词模型
│  │  transformer_encoder.py    Encoder结构
│  │  vocab.txt     字典文件
│  ├─params ERNIE参数文件
|─example_data  数据集目录
│      data.csv 无分数标注的无监督数据集
│      dgdata.csv   检查程序数据集
│      nonpre_data.csv  MINI监督数据集
│      nonpre_data850_12.csv    无监督生成训练集+交叉验证集
│      non_train_data_val.csv   无监督评估集
├─log
├─model
│  │  94.8params.zip    验证集94.8% CheckPoint
│  │  infer.model.zip   预测模型文件
│  │  serving.config.zip    PaddleServing配置文件
│  │  serving.model.zip     PaddleServing模型文件
│  │
│  └─infer.model    预测模型解压后目录
├─scripts   脚本程序
│  │  CSNN.py   主要神经网络结构以及自定义OP
│  │  infer.py  单条预测脚本
│  │  nlp_tool.py   NLP处理工具集
│  │  ori_data2tsv.py   TSV数据生成脚本
│  │  os_tool.py    系统级脚本合集
│  │  preprocess.py 预处理以及Reader脚本
│  │  run_ernie_tiny_server.py  ERNIE向量服务器启动脚本
│  │  run_lac_server.py     LAC服务启动脚本
│  │  sandbox.py    沙箱脚本
│  │  sentence2normal.py 归一化脚本
│  │  sentence2words.py 分词脚本
│  │  servers.py    服务器生成类
│  │  train.py  训练主程序
│  │  val.py    评估脚本
```
## 二、环境依赖
```
Python3.7 x64
-------------
paddlepaddle==1.7.1
paddlehub==1.6.0
jieba==0.42.1
其余依赖项随PaddlePaddle安装而安装
```
上述依赖安装方法：
1、安装PaddlePaddle

`https://www.paddlepaddle.org.cn/install/quick`

2、安装PaddleHub和jieba:

`pip install paddlehub==1.6.0 jieba==0.42.1`

##三、设计思想