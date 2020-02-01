# Author: Acer Zhang
# Datetime:2020/1/31 21:15
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import time
import json


def req_time_id():
    """
    获取当前时间
    :return:
    """
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def load_json_file(json_file_path: str):
    """
    将json文件读取为dict对象
    :param json_file_path:json文件路径
    :return:json数据的dict形式
    """
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = f.read()
    return json.loads(data, encoding="utf-8")


def generate_json_file(dict_data: dict, json_save_path: str, file_name: str = ""):
    """
    生成json文件
    :param dict_data: 字典数据
    :param json_save_path: 保存json文件的路径
    :param file_name: 文件标识名

    Example:
    generate_json_file({1:"a"},"./",file_name="word_index")
    this method can generate a file, which name like "JsonGPack-word_index-{Now Time}.gpack"
    """
    data = json.dumps(dict_data, ensure_ascii=False)
    with open(os.path.join(json_save_path, "JsonGPack-" + file_name + req_time_id() + ".gpack"),
              "w", encoding="utf-8") as f:
        f.write(data)
