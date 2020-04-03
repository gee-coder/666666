# Author: Acer Zhang
# Datetime:2020/2/1 15:06
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import traceback
import random
from typing import List
import logging as log

import paddlehub as hub
import numpy as np
from scripts.servers import Client
from scripts.nlp_tool import add_separator_in_words, transform_data2id

INIT_DATA = False  # 控制预处理临时文件生成的全局变量，谨慎修改！


def _check_score(sample_text: str, keys: list):
    score = 0
    weight = 1 / len(keys)
    for key in keys:
        key = "".join(key)
        if key in sample_text:
            score += weight
    return score


class DataEnhancement:
    """
    数据集增强类
    """
    # 0-5权重值
    word_weight_l = {
        "f": 5.,
        "i": 5.,
        "s": 5.,
        "n": 4.,
        "u": 0.,
        "w": 0.,
        "b": 5.,
        "j": 0.,
        "vn": 3.,
        "nz": 5.,
        "nr": 5.,
        "ns": 5.,
        "nt": 5.,
        "nrt": 5.,
        "nw": 5.,
        "PER": 5.,
        "LOC": 5.,
        "ROG": 5.,
        "TIME": 5.,
        "eng": 5.,
        "other": 0.5}
    # 数据分组数量
    data_group = 5
    # 随机池
    pool = dict()
    # 统计字典
    key_dict = {}
    # 结果池
    now_data = []

    def __init__(self, key_data: List[str], key_n_data: List[str], key_word_data: List[str],
                 key_word_n_data: List[str]):
        """
        Example:
        :param key_data: 答案分词数据 ['答案1', '答案2',...]
        :param key_n_data: 答案分词词性数据 ['答案1词性', '答案2词性',...]
        :param key_word_data:  给分点分词数据 ['不是|只有|一个|装货|点', '和|一个|卸货|点|的|线路|安排']
        :param key_word_n_data:  给分点分词词性数据 ['v|v|m|vn|n', 'c|m|vn|n|u|n|vn']
        """
        self.key_word_data = []
        self.key_word_n_data = []
        for key_words, key_ns in zip(key_word_data, key_word_n_data):
            key_words = key_words.split("| | | |一| | | |")
            key_ns = key_ns.split("|x|x|x|m|x|x|x|")
            tmp1 = []
            tmp2 = []
            for key_word, key_n in zip(key_words, key_ns):
                tmp1.append(key_word.replace("\n", "").split("|"))
                tmp2.append(key_n.replace("|w", "").replace("\n", "").split("|"))
            self.key_word_data.append(tmp1)
            self.key_word_n_data.append(tmp2)

        key_data = [i.replace("\n", "").split("|") for i in key_data]
        key_n_data = [i.replace("\n", "").split("|") for i in key_n_data]  # 去掉换行符
        self.key_data = key_data
        self.key_n_data = key_n_data

        self.generate_dict()

    def generate_dict(self):
        for keys, ns in zip(self.key_data, self.key_n_data):
            for k, n in zip(keys, ns):
                if k not in self.key_dict:
                    self.key_dict[k] = 1
                else:
                    self.key_dict[k] += 1
                if n not in self.pool:
                    self.pool[n] = set()
                self.pool[n].add(k)

    def n_limit_tactics(self, index: int):
        """窗口法计算分值"""
        keys = self.key_word_data[index]
        keys_n = self.key_word_n_data[index]
        # 生成窗口得分
        count = []
        for key_id, key_n in enumerate(keys_n):
            len_key = len(key_n)

            if len_key < 2:
                # 短词直接替换策略
                # 第 N 个得分点 - 窗口开始点 - 窗口结束点 , 分数
                count.append((str(key_id) + "-" + str(0) + "-" + str(len_key), 5))
            else:
                # 长句窗口循环策略
                for num in range(3):
                    # 3次窗口循环
                    if len_key < num + 1:
                        break
                    for i in range(len_key - num + 1):
                        # 窗口循环
                        score = 0
                        for k in key_n[i:i + num + 1]:
                            # 计算窗口内分数
                            score += self.word_weight_l[k] if k in self.word_weight_l else self.word_weight_l["other"]
                        if score >= 5:
                            # 第 N 个得分点 - 窗口开始点 - 窗口结束点 , 分数
                            count.append((str(key_id) + "-" + str(i) + "-" + str(i + num + 1), score))
        # 准备替换得分点
        keys_group = {}  # 该组内为已经替换好的得分点信息
        for info, _ in count:
            info = [int(i) for i in info.split("-")]
            key = keys[info[0]]
            key_n = keys_n[info[0]]
            ori_word = ""
            new_word = ""
            for k, n in zip(key[info[1]:info[2]], key_n[info[1]:info[2]]):
                try:
                    tmp = list(self.pool[n])
                    if k in tmp:
                        tmp.remove(k)
                except KeyError:
                    continue
                if len(tmp) == 0:
                    continue
                else:
                    rand = random.randint(0, len(tmp) - 1)
                    ori_word += k
                    new_word += tmp[rand]

            if info[0] not in keys_group:
                keys_group[info[0]] = []
            keys_group[info[0]].append((ori_word, new_word))

        # 进行替换并计算分数
        ori_sample_data = "|".join(self.key_data[index])
        if len(keys_group) > 0:
            done_text = []
            key_list = [rand_id for rand_id in keys_group.keys() if len(keys_group[rand_id]) > 0]
            for id_0 in range(len(key_list) + 1):
                # 遍历所有分值可能，id_0代表需要替换的个数
                rand_list = random.sample(key_list, id_0)
                sample_text = ori_sample_data.replace("|", "")
                for i in rand_list:
                    tmp = keys_group[i]
                    rand = random.randint(0, len(tmp) - 1)
                    tmp = tmp[rand]
                    if tmp[0] in sample_text:
                        sample_text = sample_text.replace(tmp[0], tmp[1], 1)
                score = _check_score(sample_text, keys)
                done_text.append((sample_text, score * 10))
        else:
            done_text = [(ori_sample_data.replace("|", ""), 10)]
        self.now_data = done_text

    def req_data(self, index: int, method: classmethod = n_limit_tactics):
        """
        获取数据
        :param index: 索引号
        :param method: 方法
        :return: [(模拟答案, 分数), ...]
        [('不是只有一个...', 10), ('不是只有一个装货...', 5.0), ...]
        """

        method(self, index)
        return self.now_data

    def __len__(self):
        return len(self.key_data)


# a = DataEnhancement(["不是|只有|一个|装货|点|和|一个|卸货|点|的|线路|安排", "仓库|一般|只|做|外观|检验|和|尺寸|精度|检验|两种|。"],
#                     ['v|v|m|vn|n|c|m|vn|n|u|n|vn', 'n|ad|d|v|n|vn|c|n|n|vn|nz'],
#                     ['不是|只有|一个|装货|点| |和|一个|卸货|点|的|线路|安排', "外观| |检验| |尺寸|精度| |检验"],
#                     ['v|v|m|vn|n|w|c|m|vn|n|u|n|vn', "n|w|vn|w|n|n|w|vn"])
# print(a.req_data(0))
# pass

client1 = Client(server_addr="127.0.0.1:6888", jb=True)

log.info("\033[0;32m Load vocab...")
text_transform = hub.reader.ClassifyReader(
    dataset=None,
    vocab_path=r"D:\a13\server-python\ERNIE\vocab.txt",
    max_seq_len=128,
    sp_model_path=r"D:\a13\server-python\ERNIE/spm_cased_simp_sampled.model",
    word_dict_path=r"D:\a13\server-python\ERNIE/dict.wordseg.pickle")
log.info("\033[0;32m Load vocab ready")
log.info("\033[0;32m load cache dataset ipt")


def reader(data_csv: str, is_val: bool = False, is_none_pre: bool = True, train_rate: float = 0.8):
    """
    数据生成器
    :param is_none_pre: 启动无增强方案，不推荐在FineTune时设置为False启动增强！
    数据集格式
    True  答案，模拟答案
    False 答案，模拟答案，分数
    :param data_csv: csv所在位置
    :param is_val: 是否返回为测试集
    :param train_rate: 训练集比例
    :return: reader对象
    """

    with open(data_csv, "r", encoding="utf-8") as f:
        lines = f.readlines()
    data = [[] for _ in range(3)]
    for id_, line in enumerate(lines):
        line = line.split(",")
        for item_id, item in enumerate(line):
            data[item_id].append(item)

    def generate():
        if is_none_pre is False:
            # 分词处理
            key_n_f_data, key_f_data = client1.run_jb_client(data[0])
            key_word_n_f_data, key_word_f_data = client1.run_jb_client(data[1], add_n_black=True)
            key_n_f_data = add_separator_in_words(key_n_f_data)
            key_f_data = add_separator_in_words(key_f_data)
            key_word_n_f_data = add_separator_in_words(key_word_n_f_data)
            key_word_f_data = add_separator_in_words(key_word_f_data)
            data_enhancement = DataEnhancement(key_data=key_f_data,
                                               key_n_data=key_n_f_data,
                                               key_word_data=key_word_f_data,
                                               key_word_n_data=key_word_n_f_data)
            all_index_list = [i for i in range(len(data_enhancement))]
            train_list = all_index_list[:int(len(data_enhancement) * train_rate)]
            val_list = all_index_list[int(len(data_enhancement) * train_rate):]
            # 选择数据集
            index_list = val_list if is_val else train_list
            # 开始递归
            for index in index_list:
                ori_key = data[0][index]
                samples = data_enhancement.req_data(index)
                ipt_keys = [[i[0]] for i in samples]
                ipt_scores = [i[1] for i in samples]
                ori_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[[ori_key]])()
                ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask = [i for i in ori_outs][0][0]
                ori_sentence = ori_input_ids[ori_input_ids > 0]
                transform_outs = text_transform.data_generator(batch_size=1, phase="predict", data=ipt_keys)()
                for score, transform_out in zip(ipt_scores, transform_outs):
                    input_ids, position_ids, segment_ids, input_mask = transform_out[0]
                    score = np.array(score).astype("int64").reshape(1, 1)
                    sentence = input_ids[input_ids > 0]
                    yield ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
                          position_ids, segment_ids, input_mask, ori_sentence, sentence, score

        else:
            all_index_list = [i for i in range(len(data[0]))]
            train_list = all_index_list[:int(len(data[0]) * train_rate)]
            val_list = all_index_list[int(len(data[0]) * train_rate):]
            # 选择数据集
            index_list = val_list if is_val else train_list
            for index in index_list:
                ori_key = data[0][index]
                sample = data[1][index]
                score = data[2][index]
                ori_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[[ori_key]])()
                ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask = [i for i in ori_outs][0][0]
                transform_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[[sample]])()
                input_ids, position_ids, segment_ids, input_mask = [i for i in transform_outs][0][0]
                ori_sentence = ori_input_ids[ori_input_ids > 0]
                sentence = input_ids[input_ids > 0]
                score = np.array(score).astype("int64").reshape(1, 1)
                yield ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
                      position_ids, segment_ids, input_mask, ori_sentence, sentence, score

    return generate
# reader(r"D:\a13\server-python\example_data\dgdata.csv")
