# Author: Acer Zhang
# Datetime:2020/1/31 21:15
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import time
import json
from typing import List, Dict


def req_time_id(short_YMD: bool = False, short_HMS: bool = False):
    """
    获取当前时间
    :return:
    """
    pack = "None"
    if short_YMD:
        pack = time.strftime("%Y-%m-%d", time.localtime())
    elif short_HMS:
        pack = time.strftime("%H-%M-%S", time.localtime())
    else:
        pack = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    return pack


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


class GLog:
    dict = {}

    def __init__(self, gpack_path: str, item_heads: dict, file_name: str = None):
        self.item_heads = item_heads
        if file_name is None:
            file_name = req_time_id()
        file_path = os.path.join(gpack_path, file_name) + ".gpack"
        self.exists = os.path.exists(file_path)
        self.file = open(file_path, "a+", encoding="utf-8")
        self._creat_heads()

    def _creat_heads(self):
        if self.exists:
            for i, head in enumerate(self.item_heads.keys()):
                self.dict[head] = None
        else:
            pack = ["|" + req_time_id(short_YMD=True) + "\t|\t", "|Massage\t|\t"]
            for i, head in enumerate(self.item_heads.keys()):
                self.dict[head] = None
                pack.append("|" + str(head) + "\t|\t") if i != len(self.item_heads) - 1 else \
                    pack.append("|" + str(head) + "\t|\n")
            self.file.writelines(pack)

    def write_log(self, items: dict, massage: str = "None"):
        pre_dict = dict(self.dict)
        pack = [req_time_id(short_HMS=True) + "\t", massage + "\t"]
        pre_dict.update(items)
        for i, item in enumerate(pre_dict.items()):
            if item[1] is None:
                item = "None"
            pack.append(str(item) + "\t") if i != len(pre_dict) - 1 else pack.append(str(item) + "\n")
        self.file.writelines(pack)

    def close(self):
        self.file.close()
