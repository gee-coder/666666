# Author: Acer Zhang
# Datetime:2020/4/7 19:56
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# Author: Acer Zhang
# Datetime:2020/4/4 17:13
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from typing import List

import numpy as np
import paddlehub as hub
import paddle.fluid as fluid

# 预测模型路径
MODEL_PATH = r"D:\a13\module\model\infer.model"
# 字典路径
VOCAB_PATH = r"D:\a13\module\ERNIE\vocab.txt"
# 分词模型路径
SP_MODEL_PATH = r"D:\a13\module\ERNIE/spm_cased_simp_sampled.model"
# 词典路径
WORD_DICT_PATH = r"D:\a13\module\ERNIE/dict.wordseg.pickle"

# 数据转换器
text_transform = hub.reader.ClassifyReader(
    dataset=None,
    vocab_path=VOCAB_PATH,
    max_seq_len=128,
    sp_model_path=SP_MODEL_PATH,
    word_dict_path=WORD_DICT_PATH)

# 载入模型
place = fluid.CPUPlace()
exe = fluid.Executor(place)
program, feed_list, fetch_list = fluid.io.load_inference_model(MODEL_PATH, exe)


# 转换函数
def reader(ori_key: List[str], sample: List[str]):
    ori_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[ori_key])()
    ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask = [i for i in ori_outs][0][0]
    transform_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[sample])()
    input_ids, position_ids, segment_ids, input_mask = [i for i in transform_outs][0][0]
    return ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
           position_ids, segment_ids, input_mask


if __name__ == '__main__':
    print("开始进行推理")
    # 生成对应数据 第一个参数为标准答案，第二个参数为学生答案
    # Example: feed = reader(["标准答案"], ["学生答案"])
    # feed = reader(["配送模式：自营配送模式；共同配送模式；第三方配送。"], ["共同配送模式；第三方配送"])
    inp_a = "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。"
    # inp_b = "货场货位编号"
    inp_b = "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。"
    feed = reader([inp_a], [inp_b])
    # Create feed list
    feeder = dict((n, d) for n, d in zip(feed_list, feed))
    outs = exe.run(program, feed=feeder, fetch_list=fetch_list)
    score = outs[0][0]
    confidence = outs[1][0]
    confidence = confidence[max(0, score - 1): min(score + 1, 11)].tolist()
    confidence = sum(confidence)
    print("预测结果", score, "/10分", "\t置信度{:.2f}%".format(confidence * 100))
