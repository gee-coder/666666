# Author: Acer Zhang
# Datetime:2020/2/1 15:06
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import numpy as np

from nlp_tool import transform_data2id
from os_tool import load_json_file


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
