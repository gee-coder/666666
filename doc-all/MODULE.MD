# 主观题评分模型--Kea模型文档

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

### 1、模型思想

该模型借助深度学习框架PaddlePaddle进行实现，其自研表现在设计深度学习损失函数Kea(Key experience around)，而非对语义模型进行设计。该设计可以轻松使用不同类型的语义表示模型/backbone，以达到跨语言、类型的主观题的高性能预测能力。模型设计聚焦于以下方面：

>1、自研无监督数据增强模块：仅需150条监督数据即可实现95%高准确率。  
>2、可更换式模块化backbone：兼容ERNIE、BERT等语义表示模型，多国语言均可支持。  
>3、自研高泛化能力Kea损失函数：解决因监督数据标注不准确而导致过拟合等问题。  
>4、快速企业级部署能力：提供工业级PaddleServing、民用级HubServing支持，提高落地效率。  
>5、完美适配国产框架，避免因外部政策干预而终止模型服务。

### 2、算法思想

####2.1 无监督数据增强
借助可更换分词技术：Paddle-LAC、Jieba(Paddle)，针对标准答案中名词、专属名词等属性文字进行Mask。对已经Mask后的数据进行以下两种方式处理：
>1、窗口法随机替换Mask对象以生成监督数据集，供主要模型网络监督训练使用。  
>2、提供给语义表示模型ERNIE，使其预训练该类型数据。

其中数据生成策略为自主设计，其代码保存在`script/preprocess.py`

Example:
```
-分词-使用LAC进行分词
物流金字塔是物流设计的一大工作 -> 物流金字塔|是|物流设计|的|一大|工作

-生成监督数据集-
机器标注分值，方便神经网络初始化预训练模型参数。
->物流金字塔|是|物流设计|的|一大|工作 10分
->物流管理|是|物流设计|的|一大|工作 5分
->物流金字塔|是|物流预测|的|一大|工作 6分
->物流管理|是|物流预测|的|一大|工作 0分

-Mask转换-
使ERNIE对Mask进行推理，得到最接近的feature map。
->Mask|是|Mask|的|一大|工作

```
####2.2 ERNIE-Tiny
该算法为国产开源语义表示模型，在模型中承担backbone角色。本模型可以更换backbone为准确率更高的ERNIE-Base，也可以更换为英文模型BART，默认使用轻量级模型ERNIE-Tiny。

>ERNIE Tiny 主要通过模型结构压缩和模型蒸馏的方法，将 ERNIE 2.0 Base 模型进行压缩。特点和优势如下：(1) 采用 3 层 transformer 结构，线性提速 4 倍;（2) 模型加宽隐层参数，从 ERNIE 2.0 的 768 扩展到 1024；(3) 缩短输入文本的序列长度，降低计算复杂度，模型首次采用中文 subword 粒度输入，长度平均缩短 40%；(4) ERNIE Tiny 在训练中扮演学生角色，利用模型蒸馏的方式在 Transformer 层和 Prediction 层学习教师模型 ERNIE 2.0 模型对应层的分布和输出; 综合优化能带来4.3倍的预测提速，具有更高的工业落地能力。

##### ERNIE Pre-Training 任务
![](https://raw.githubusercontent.com/PaddlePaddle/ERNIE/develop/.metas/ernie2.0_model.png)  

_其中ERNIE-Tiny开源代码由Paddle提供_

####2.3 Kea损失函数
为解决人工标注的label可能存在不稳定情况，设计出特殊的损失函数Kea，也是该评分系统的算法核心。

传统的交叉熵损失函数，通过计算 Net Out 与 Target Label 的差值作为反向传播的梯度大小，但这样的梯度并不能很好反映真实的误差，举例如下：
>"今天天气很好"->7分  

教师A、B、C对该句子打分

>"今天天气很好"->7分  梯度为0+  
>"今天天气很好"->8分  梯度为1-  
>"今天天气很好"->1分  梯度为1-  

可以看出，在这种情况下8分与1分的梯度值均为较高水平。实际上"今天天气很好"在6-8分之内均符合标准，评分标准模糊的情况下不应使临近分数也拥有较高梯度。

Kea损失函数为了平滑临近标签梯度，提供了以下三种方案：

##### 2.3.1 临近平滑法
>若 Net Out Top1命中Target Label以及其临近1单位Label，则分别计算这3个单位的剪去均值后的梯度。

优势：有效减少过拟合、误差在2分以内的准确率可达94.8%。
缺点：误差为2的数据占比较高。

##### 2.3.2 洋葱平滑法
>若 Net Out Top1命中Target Label以及其临近1单位Label，则分别计算这3个单位的梯度，其中对Target Label位置进行额外的惩罚。  

优势：0误差数据占比较高、置信度总体水平较高、误差在2分以内的准确率可达89.8%。
缺点：泛化能力稍弱。

##### 2.3.3 加权平滑法
>若 Net Out Top1命中Target Label以及其临近1单位Label，计算其中权值分别计算这3个单位梯度。  

优势：0、1误差数据占比较高、误差在2分以内的准确率可达92.6%。
缺点：置信度水平一般。

##3、网络结构

![](https://github.com/GitHuplus/666666/blob/master/doc-all/%E7%BD%91%E7%BB%9C%E7%BB%93%E6%9E%84%E5%9B%BE.png)

##4、开始Finetune
###4.1数据准备
###4.2设置Finetune参数
###4.3执行训练
###4.4导出模型
###4.5执行评估
###4.6制作HubServing