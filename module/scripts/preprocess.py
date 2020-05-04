# Author: Acer Zhang
# Datetime:2020/2/1 15:06
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import random
import logging as log

import paddlehub as hub
import numpy as np

from scripts.dataset_tools import DataEnhancement
from scripts.servers import Client
from scripts.nlp_tool import add_separator_in_words

INIT_DATA = False  # 控制预处理临时文件生成的全局变量，谨慎修改！

client1 = Client(server_addr="127.0.0.1:6888", jb=True)

log.info("\033[0;32m Load vocab...")
text_transform = hub.reader.ClassifyReader(
    dataset=None,
    vocab_path=r"D:\a13\module\ERNIE\vocab.txt",
    max_seq_len=128,
    sp_model_path=r"D:\a13\module\ERNIE/spm_cased_simp_sampled.model",
    word_dict_path=r"D:\a13\module\ERNIE/dict.wordseg.pickle")
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
                transform_outs = text_transform.data_generator(batch_size=1, phase="predict", data=ipt_keys)()
                for score, transform_out in zip(ipt_scores, transform_outs):
                    input_ids, position_ids, segment_ids, input_mask = transform_out[0]
                    score = np.array(score).astype("int64").reshape(1, 1)
                    yield ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
                          position_ids, segment_ids, input_mask, score

        else:
            all_index_list = [i for i in range(len(data[0]))]
            train_list = all_index_list[:int(len(data[0]) * train_rate)]
            val_list = all_index_list[int(len(data[0]) * train_rate):]
            # 选择数据集
            index_list = val_list if is_val else train_list
            for index in index_list:
                zero_data = random.randint(0, 10)
                ori_key = data[0][index]
                if zero_data > 0 or is_val is True:
                    # 若随机到0分数据，则对其进行随机答案处理，测试时不考虑该数据
                    sample = data[1][index]
                    score = data[2][index]
                else:
                    random_index = random.randint(0, len(index_list) - 1)
                    sample = data[1][random_index]
                    score = data[2][index] if random_index == index else 0

                ori_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[[ori_key]])()
                ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask = [i for i in ori_outs][0][0]
                transform_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[[sample]])()
                input_ids, position_ids, segment_ids, input_mask = [i for i in transform_outs][0][0]
                score = np.array(score).astype("int64").reshape(1, 1)
                yield ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
                      position_ids, segment_ids, input_mask, score

    return generate
# reader(r"D:\a13\server-python\example_data\dgdata.csv")
