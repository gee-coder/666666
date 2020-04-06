# Author: Acer Zhang
# Datetime:2020/4/4 17:13
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from typing import List

import paddlehub as hub
import paddle.fluid as fluid

DATA_CSV = r"D:\a13\server-python\example_data/val.csv"
MODEL_PATH = r"D:\a13\server-python\model\infer.model"
VOCAB_PATH = r"D:\a13\server-python\ERNIE\vocab.txt"
SP_MODEL_PATH = r"D:\a13\server-python\ERNIE/spm_cased_simp_sampled.model"
WORD_DICT_PATH = r"D:\a13\server-python\ERNIE/dict.wordseg.pickle"

data = {"OriKey": [], "VirtualKey": [], "score": []}
with open(DATA_CSV, "r", encoding="utf-8") as f:
    csv = f.readlines()
    for sample in csv:
        infos = sample.split(",")
        for n, info in zip(data.keys(), infos):
            data[n].append(info.replace("\n", ""))

text_transform = hub.reader.ClassifyReader(
    dataset=None,
    vocab_path=VOCAB_PATH,
    max_seq_len=128,
    sp_model_path=SP_MODEL_PATH,
    word_dict_path=WORD_DICT_PATH)


def reader(ori_key: List[str], sample: List[str]):
    ori_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[ori_key])()
    ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask = [i for i in ori_outs][0][0]
    transform_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[sample])()
    input_ids, position_ids, segment_ids, input_mask = [i for i in transform_outs][0][0]
    return ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
           position_ids, segment_ids, input_mask


place = fluid.CPUPlace()
exe = fluid.Executor(place)
program, feed_list, fetch_list = fluid.io.load_inference_model(MODEL_PATH, exe)

feeder = dict()
print("开始进行推理\nID\t推理效果\t推理结果\t人工得分")
count = 0
data_num = len(data["OriKey"])
for sample_id in range(data_num):

    # load data
    feed = reader([data["OriKey"][sample_id]], [data["VirtualKey"][sample_id]])
    # Create feed list
    feeder = dict((n, d) for n, d in zip(feed_list, feed))
    outs = exe.run(program, feed=feeder, fetch_list=fetch_list)
    error = abs(outs[0][0] - int(data["score"][sample_id]))
    score_info = "T" if error <= 2 else "F"
    count += 1 if score_info == "T" else 0
    print(sample_id, "\t ", score_info, "\t ", outs[0][0], "\t ", data["score"][sample_id])
print("该批次准确率：{:-2f}".format(count / data_num))
