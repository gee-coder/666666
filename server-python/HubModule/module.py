# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import paddle.fluid as fluid
import paddlehub as hub
from paddlehub.module.module import moduleinfo, serving


def load_json(info):
    ids = []
    k = []
    vk = []
    if "inp_data" in info:
        info = info["inp_data"]
    for sample in info:
        ids.append(sample["answerId"])
        k.append(sample["standardAnswer"])
        vk.append(sample["answer"])
    return ids, k, vk


@moduleinfo(
    name="kea",
    version="6.4",
    summary="All copyrighted by Acer Zhang",
    author="Acer Zhang",
    author_email="zhangacer@foxmail.com",
    type="nlp/classify")
class Kea(hub.Module):
    def _initialize(self, gpu_index=None, model_path=None):
        """
        initialize with the necessary elements
        """
        self.module_name = 'kea'
        # 预测模型路径
        if not model_path:
            model_path = os.path.join(self.directory, "infer.model")
        # 字典路径
        vocab_path = os.path.join(self.directory, "vocab.txt")
        # 分词模型路径
        sp_model_path = os.path.join(self.directory, "spm_cased_simp_sampled.model")
        # 词典路径
        word_dict_path = os.path.join(self.directory, "dict.wordseg.pickle")

        # 数据转换器
        self.text_transform = hub.reader.ClassifyReader(
            dataset=None,
            vocab_path=vocab_path,
            max_seq_len=128,
            sp_model_path=sp_model_path,
            word_dict_path=word_dict_path)
        self.place = fluid.CUDAPlace(int(gpu_index)) if gpu_index else fluid.CPUPlace()
        self.exe = fluid.Executor(self.place)
        self.model = fluid.io.load_inference_model(model_path, self.exe)

    def reader(self, ori_key: list, sample: list):
        def generate():
            for k, s in zip(ori_key, sample):
                ori_outs = self.text_transform.data_generator(batch_size=1, phase="predict", data=[[k]])()
                ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask = [i for i in ori_outs][0][0]
                transform_outs = self.text_transform.data_generator(batch_size=1, phase="predict", data=[[s]])()
                input_ids, position_ids, segment_ids, input_mask = [i for i in transform_outs][0][0]
                yield ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
                      position_ids, segment_ids, input_mask

        return generate

    @serving
    def kea_server(self, inp_data):
        ids, k, vk = load_json(inp_data)
        infer_reader = fluid.io.batch(self.reader(k, vk), batch_size=128)
        infer_feeder = fluid.DataFeeder(feed_list=self.model[1],
                                        place=self.place,
                                        program=self.model[0])
        # Create feed list
        now_id = 0
        ret = []
        for data in infer_reader():
            outs = self.exe.run(self.model[0], feed=infer_feeder.feed(data), fetch_list=self.model[2])
            for i in range(len(outs[0])):
                score = outs[0][i]
                confidence = outs[1][i]
                confidence = sum(confidence)
                mini_ret = {"answerId": str(ids[now_id]),
                            "systemScore": int(score),
                            "confidence": "{:.2f}%".format(confidence * 100)}
                ret.append(mini_ret)
                now_id += 1
        return ret


if __name__ == "__main__":
    kea = Kea()
    input_dict = {"inp_data": [
        {
            "answerId": "5ea6bb708737b66cd217d7b0",
            "standardAnswer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
            "answer": " poJ",
        },
        {
            "answerId": "5ea6bb708737b66cd217d7b1",
            "standardAnswer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
            "answer": "  ",
        },
        {
            "answerId": "5ea6bb708737b66cd217d7b2",
            "standardAnswer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
            "answer": "货场货位编号",
        },
        {
            "answerId": "5ea6bb708737b66cd217d7b3",
            "standardAnswer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
            "answer": "储位编码包括：库房编号、库房内货位编号、货架上的货位编号、货场货位编号。",
        }
    ]}
    results = kea.kea_server(input_dict)
    print(results)
