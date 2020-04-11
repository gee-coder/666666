# Python预测环境部署

## 一、目录结构
```
│ hub_server_infer.py   Hub Module测试示例
├─HubModule HubModule主目录-民用级部署方案
│  │  dict.wordseg.pickle   词典文件
│  │  module.py     ERNIE-Tiny网络结构
│  │  spm_cased_simp_sampled.model  分词模型
│  │  vocab.txt     字典文件
│  │  __init__.py   初始化信息
│  └─infer.model    预测模型
└─PaddleServing 企业级部署方案
    ├─serving.config    服务端配置信息
    └─serving.model 服务端模型

```
## 二、环境依赖
Python 3.7 x64

CPU依赖：

pip包：paddlepaddle==1.7.1 paddlehub==1.6.1

GPU依赖(可选)：

CUDA开发环境10.0(严格版本号)、CUDNN7.6

pip包：paddlepaddle-gpu==1.7.1.post107 paddlehub==1.6.1

**相同pip包以最后一次安装版本为准，若在安装GPU依赖的pip包后安装CPU版本，即使pip list显示拥有GPU环境，但仍为CPU环境。**

Paddlepaddle安装说明请参考：

`https://www.paddlepaddle.org.cn/install/quick`

PaddleHub快速安装指令：

在终端/CMD中键入`pip install paddlehub==1.6.1`

## 三、Kea Module部署

### 1、安装Module
打开终端/CMD，键入以下指令：

`hub install [HubModule主目录所在路径]`

Example:

`hub install D:/server-python/HubModule`

最终出现`Successfully installed kea`即可视为安装成功。

其中`kea`即为主观题评分模型。

### 2、Kea模型安装检测

打开终端/CMD，键入以下指令：

`python [HubModule主目录中module.py文件所在路径]`

Example:

`python D:/server-python/HubModule/module.py`

最终出现类似`{'id': 'test', 'score': '10', '(confidence': '25.93%'}`字样，即可视为测试成功。

### 3、启动Kea预测服务器

打开终端/CMD，键入以下指令：

`hub serving start -m kea`

最终出现`* Running on http://0.0.0.0:8866/ (Press CTRL+C to quit)`即可视为启动成功。

```
--modules/-m 	模型名，此处必须为Kea
--port/-p 	服务端口，默认为8866
--use_gpu 	使用GPU进行预测，必须安装paddlepaddle-gpu
--use_multiprocess 	是否启用并发方式，默认为单进程方式(Window系统不支持并发)
```

## 四、Python客户端测试

### 1、数据规则约束

`input_dict`为需要传入的数据，其中`inp_id`为ID号，负责标注当前数据顺序，str格式无其它要求。`text_a`为标准答案数据，`text_a`为学生作答数据。

### 2、请求URL地址

`url地址为 http://[主机名]:[端口号]/predict/kea"`

默认主机名为127.0.0.1，端口号为8866。

Example: `url = "http://127.0.0.1:8866/predict/kea"`

### 3、设置请求头

因PaddleHub最新版开发者贡献模型约束，自主开发模型需要增加请求头：`"Content-Type": "application/json"`。

### 4、完整Python客户端调用示例

```python
import requests
import json

input_dict = {"inp_id": "test",
              "text_a": "入库作业管理有：收货；组盘和注册；上架",
              "text_b": "入库作业管理有：收货；组盘和注册；上架"}

url = "http://127.0.0.1:8866/predict/kea"
headers = {"Content-Type": "application/json"}
r = requests.post(url=url, headers=headers, data=json.dumps(input_dict))

print(json.dumps(r.json(), indent=4, ensure_ascii=False))
```
