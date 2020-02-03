# Author: Acer Zhang
# Datetime:2020/2/1 15:06
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import random
from typing import List, Tuple

import numpy as np

from nlp_tool import transform_data2id
from os_tool import load_json_file


class DataEnhancement:
    """
    数据集增强-机器打分类
    """
    # 0-5权重值
    word_weight = {"nz": 5,
                   "n": 4,
                   "vn": 3,
                   "u": 0,
                   "w": 0,
                   "other": 0.5}
    # 数据分组数量
    data_group = 5
    # 随机池
    pool = dict()
    # 统计字典
    key_dict = {}
    # 结果池
    now_data = []

    def __init__(self, key_data: List[str], key_word_data: List[str], key_word_n_data: List[str],
                 random_limit: Tuple[float] = (0.5, 1.)):
        """
        Example:
        :param key_data: ['答案1', '答案2',...]
        :param key_word_data:  ['不是|只有|一个|装货|点', '和|一个|卸货|点|的|线路|安排']
        :param key_word_n_data:  ['v|v|m|vn|n', 'c|m|vn|n|u|n|vn']
        :param random_limit:
        """
        key_word_data = [i.split("|") for i in key_word_data]
        key_word_n_data = [i.split("|") for i in key_word_n_data]
        self.key_word_n_data = key_word_n_data
        self.key_data = key_data
        self.key_word_data = key_word_data
        self.generate_dict()

    def generate_dict(self):
        for keys, ns in zip(self.key_data, self.key_word_n_data):
            for k, n in zip(keys, ns):
                if k not in self.key_dict:
                    self.key_dict[k] = 1
                else:
                    self.key_dict[k] += 1
                if n not in self.pool:
                    self.pool[n] = set()
                self.pool[n].add(k)

    def replace(self):
        pass

    def n_limit_tactics(self, keys, keys_n):
        """窗口法计算分值"""
        keys = [i.split("|") for i in keys]
        keys_n = [i.split("|") for i in keys_n]
        count = []
        for key_id, key_n in enumerate(keys_n):
            len_key = len(key_n)
            for num in range(3):
                # 3次窗口循环
                if len_key < num + 1:
                    break
                for i in range(len_key - num + 1):
                    # 窗口循环
                    score = 0
                    for k in key_n[i:i + num + 1]:
                        # 计算窗口内分数
                        score += self.word_weight[k] if k in self.word_weight else self.word_weight["other"]
                    if score >= 5:
                        count.append((str(key_id) + "-" + str(i) + "-" + str(i + num), score))
        

    def req_data(self, index: int, method: classmethod = n_limit_tactics):
        return 0


a = DataEnhancement(["1"], ['不是|只有|一个|装货|点', '和|一个|卸货|点|的|线路|安排'], ['v|v|m|vn|n', 'c|m|vn|n|u|n|vn'])
print(a.n_limit_tactics(['不是|只有|一个|装货|点', '和|一个|卸货|点|的|线路|安排'], ['v|v|m|vn|n', 'c|m|vn|n|u|n|vn']))
pass


def reader(data_csv, word_dict_file):
    """
    数据生成器
    :param data_csv: csv所在位置
    :param word_dict_file: 词典文件
    :return:
    """
    word_dict = load_json_file(word_dict_file)

    def train():
        with open(data_csv, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            line = line.split(",")
            assert len(line) == 7, "数据格式-字段数量有误"
            score = int(line[2]) / 10
            line.pop(2)
            key_words_id = transform_data2id([line[2]], word_dict)
            keyword_words_id = transform_data2id([line[4]], word_dict)
            # key, keyword,key_words, key_n, keyword_words, keyword_n = line
            key_words_id = np.array(key_words_id).astype("int64")
            keyword_words_id = np.array(keyword_words_id).astype("int64")
            score = np.array(score).reshape([1]).astype("float32")
            yield key_words_id, keyword_words_id, score

    return train

# reader(r"D:\a13\server-python\example_data\demo_data.csv", r"D:\a13\server-python\example_data\index.gpack")
