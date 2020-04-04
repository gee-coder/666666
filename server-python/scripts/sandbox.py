# Author: Acer Zhang
# Datetime:2020/4/4 19:15
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddlehub as hub
import paddle.fluid as fluid

module = hub.Module(name="ernie_tiny")

text_transform = hub.reader.ClassifyReader(
    dataset=None,
    vocab_path=module.get_vocab_path(),
    max_seq_len=128,
    sp_model_path=module.get_spm_path(),
    word_dict_path=module.get_word_dict_path())


def read(ori_key: str, sample: str):
    ori_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[[ori_key]])()
    ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask = [i for i in ori_outs][0][0]
    transform_outs = text_transform.data_generator(batch_size=1, phase="predict", data=[[sample]])()
    input_ids, position_ids, segment_ids, input_mask = [i for i in transform_outs][0][0]
    return ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
           position_ids, segment_ids, input_mask


def in_sandbox(data_args):
    ori_input_ids = fluid.data("ori_input_ids", shape=[-1, 128, 1], dtype="int64")
    ori_position_ids = fluid.data("ori_position_ids", shape=[-1, 128, 1], dtype="int64")
    ori_segment_ids = fluid.data("ori_segment_ids", shape=[-1, 128, 1], dtype="int64")
    ori_input_mask = fluid.data("ori_input_mask", shape=[-1, 128, 1], dtype="float32")
    input_ids = fluid.data("input_ids", shape=[-1, 128, 1], dtype="int64")
    position_ids = fluid.data("position_ids", shape=[-1, 128, 1], dtype="int64")
    segment_ids = fluid.data("segment_ids", shape=[-1, 128, 1], dtype="int64")
    input_mask = fluid.data("input_mask", shape=[-1, 128, 1], dtype="float32")
    feed_list = ["ori_input_ids", "ori_position_ids", "ori_segment_ids", "ori_input_mask", "input_ids", "position_ids",
                 "segment_ids", "input_mask"]
    feeder = fluid.DataFeeder(place=fluid.CPUPlace(), feed_list=feed_list)
    reader_out = read(data_args["inpA"], data_args["inpB"])
    return [reader_out], feeder


def out_sandbox(results, data_args):
    lines = []
    for dt in results:
        score = dt.tolist()[0]
        lines.append({"score": score})
    return lines
