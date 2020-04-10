# Author: Acer Zhang
# Datetime:2020/4/10 20:13
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import requests
import json

input_dict = {"inp_id": "test",
              "text_a": "入库作业管理有：收货；组盘和注册；上架",
              "text_b": "入库作业管理有：收货；组盘和注册；上架"}

url = "http://127.0.0.1:8866/predict/kea"
headers = {"Content-Type": "application/json"}
r = requests.post(url=url, headers=headers, data=json.dumps(input_dict))

print(json.dumps(r.json(), indent=4, ensure_ascii=False))
