# Author: Acer Zhang
# Datetime:2020/4/7 19:56
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# Author: Acer Zhang
# Datetime:2020/4/4 17:13
# Copyright belongs to the author.
# Please indicate the source for reprinting.

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
def reader(ori_key: list, sample: list):
    def generate():
        for k, s in zip(ori_key, sample):
            ori_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[[k]])()
            ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask = [i for i in ori_outs][0][0]
            transform_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[[s]])()
            input_ids, position_ids, segment_ids, input_mask = [i for i in transform_outs][0][0]
            yield ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
                  position_ids, segment_ids, input_mask

    return generate


if __name__ == '__main__':
    print("开始进行推理")
    # 生成对应数据 第一个参数为标准答案，第二个参数为学生答案
    # Example: feed = reader(["标准答案"], ["学生答案"])
    # feed = reader(["配送模式：自营配送模式；共同配送模式；第三方配送。"], ["共同配送模式；第三方配送"])
    inp_a = "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。"
    inp_b0 = " poJ"
    inp_b1 = "  "
    inp_b2 = "货场货位编号"
    inp_b3 = "储位编码包括：货场货位编号。"
    inp_b4 = "储位编码包括：库房编号、货架上的货位编号、货场货位编号。"
    inp_b5 = "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。"
    reader_obj = reader([inp_a] * 6, [inp_b0, inp_b1, inp_b2, inp_b3, inp_b4, inp_b5])
    # Create feed list
    infer_reader = fluid.io.batch(reader_obj, batch_size=128)
    infer_feeder = fluid.DataFeeder(feed_list=feed_list,
                                    place=place,
                                    program=program)
    for data in infer_reader():
        outs = exe.run(program, feed=infer_feeder.feed(data), fetch_list=fetch_list)
        for i in range(len(outs[0])):
            score = outs[0][i]
            confidence = outs[1][i]
            # confidence = confidence[max(0, score - 1): min(score + 1, 11)].tolist()
            confidence = sum(confidence)
            print(i, "预测结果", score, "/10分", "\t置信度{:.2f}%".format(min(confidence * 100, 100)))
