# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddle.fluid as fluid


class SampleNN:
    def __init__(self, mode: int = 1):
        self.mode = mode

    def stacked_lstm_net(self, data, input_dim, class_dim, emb_dim, hid_dim, stacked_num):
        # 计算词向量
        emb = fluid.embedding(
            input=data, size=[input_dim, emb_dim], is_sparse=True)

        # 第一层栈
        # 全连接层
        fc1 = fluid.layers.fc(input=emb, size=hid_dim)
        # lstm层
        lstm1, cell1 = fluid.layers.dynamic_lstm(input=fc1, size=hid_dim)

        inputs = [fc1, lstm1]

        # 其余的所有栈结构
        for i in range(2, stacked_num + 1):
            fc = fluid.layers.fc(input=inputs, size=hid_dim)
            lstm, cell = fluid.layers.dynamic_lstm(
                input=fc, size=hid_dim, is_reverse=(i % 2) == 0)
            inputs = [fc, lstm]

        # 池化层
        fc_last = fluid.layers.sequence_pool(input=inputs[0], pool_type='max')
        lstm_last = fluid.layers.sequence_pool(input=inputs[1], pool_type='max')

        # 全连接层，softmax预测
        prediction = fluid.layers.fc(
            input=[fc_last, lstm_last], size=class_dim, act='sigmoid')

        return prediction

    def main_network(self, lod_data):
        # emb = fluid.embedding(input=lod_data, size=[3096, 100], is_sparse=True)

        conv_4 = self.stacked_lstm_net(lod_data, 3000, 1, 100, 100, 100)
        return conv_4

# # debug
# data = fluid.data(name="test", shape=[-1], dtype="int64", lod_level=1)
# SampleNN().main_network(data)
