# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddle.fluid as fluid


class SampleNN:
    def __init__(self, mode: int = 1):
        self.mode = mode

    def main_network(self, lod_data):
        emb = fluid.embedding(input=lod_data, size=[3096, 100], is_sparse=True)
        conv_3 = fluid.nets.sequence_conv_pool(
            input=emb,
            num_filters=200,
            filter_size=3,
            act="tanh",
            pool_type="sqrt")
        conv_4 = fluid.nets.sequence_conv_pool(
            input=emb,
            num_filters=200,
            filter_size=4,
            act="tanh",
            pool_type="sqrt")
        prediction = fluid.layers.fc(
            input=[conv_3, conv_4], size=1, act="sigmoid")

        return prediction

# # debug
# data = fluid.data(name="test", shape=[-1], dtype="int64", lod_level=1)
# SampleNN().main_network(data)
