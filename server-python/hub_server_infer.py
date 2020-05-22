# Author: Acer Zhang
# Datetime:2020/4/10 20:13
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import requests
import json

input_dict = {"inp_data": [
    {
        "answerId": "5ea6bb708737b66cd217d7b0",
        "standardAnswer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
        "answer": " poJ",
    },
    {
        "answerId": "5ea6bb708737b66cd217d7b1",
        "standardAnswer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
        "answer": "  ",
    },
    {
        "answerId": "5ea6bb708737b66cd217d7b2",
        "standardAnswer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
        "answer": "货场货位编号",
    },
    {
        "answerId": "5ea6bb708737b66cd217d7b3",
        "standardAnswer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
        "answer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
    }
]}

url = "http://127.0.0.1:8866/predict/kea"
headers = {"Content-Type": "application/json"}
r = requests.post(url=url, headers=headers, data=json.dumps(input_dict))

print(json.dumps(r.json(), indent=4, ensure_ascii=False))
