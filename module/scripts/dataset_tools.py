# Author: Acer Zhang
# Datetime:2020/4/13 22:13
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import random
from typing import List


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

class DatasetEqual:
    score_pool = None
    key_pool = dict()
    vkey_pool = dict()
    extreme_rate = 3

    def __init__(self, csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            data = f.readlines()
        for sample in data:
            pass

    def _add_zero(self):
        pass

    def _shuffe_word(self):
        pass

    def _replace_near(self):
        pass
