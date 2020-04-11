# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import paddle.fluid as fluid
import paddlehub as hub
from paddlehub.module.module import moduleinfo, serving


@moduleinfo(
    name="kea",
    version="6.3",
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
        place = fluid.CUDAPlace(int(gpu_index)) if gpu_index else fluid.CPUPlace()
        self.exe = fluid.Executor(place)
        self.model = fluid.io.load_inference_model(model_path, self.exe)

    def kea_reader(self, ori_key: str, sample: str):
        ori_outs = self.text_transform.data_generator(batch_size=1, phase="predict", data=[[ori_key]])()
        ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask = [i for i in ori_outs][0][0]
        transform_outs = self.text_transform.data_generator(batch_size=1, phase="predict", data=[[sample]])()
        input_ids, position_ids, segment_ids, input_mask = [i for i in transform_outs][0][0]
        return ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, \
               position_ids, segment_ids, input_mask

    @serving
    def kea_server(self, inp_id, text_a, text_b):
        feed = self.kea_reader(text_a, text_b)
        # Create feed list
        feeder = dict((n, d) for n, d in zip(self.model[1], feed))
        outs = self.exe.run(self.model[0], feed=feeder, fetch_list=self.model[2])
        score = outs[0][0]
        confidence = outs[1][0]
        confidence = confidence[max(0, score - 1): min(score + 1, 11)].tolist()
        confidence = sum(confidence)
        ret = {"id": str(inp_id),
               "score": str(score),
               "confidence": "{:.2f}%".format(confidence * 100)}
        return ret


if __name__ == "__main__":
    senta = Kea()
    input_dict = {"id": "test",
                  "text_a": "入库作业管理有：收货；组盘和注册；上架",
                  "text_b": "入库作业管理有：收货；组盘和注册；上架"}
    results = senta.kea_server(input_dict["id"], input_dict["text_a"], input_dict["text_b"])
    print(results)
