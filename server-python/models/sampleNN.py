# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddle.fluid as fluid


class SampleNN:
    def __init__(self, mode: int = 1):
        self.mode = mode

    def main_network(self, lod_data):
        emb = fluid.embedding(input=lod_data, size=[512, 100], is_sparse=True)
        print(emb.shape)
        x = fluid.layers.fc(input=emb, size=512 * 3)
        hidden = fluid.layers.dynamic_gru(input=x, size=512)
        print(hidden.shape)


data = fluid.data(name="test", shape=[-1], dtype="int64", lod_level=1)
SampleNN().main_network(data)

