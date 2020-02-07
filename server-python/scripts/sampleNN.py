# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddle.fluid as fluid
import paddle.fluid.initializer as parm_init


def parm_msra():
    param = fluid.ParamAttr(
        initializer=parm_init.MSRA(),
        learning_rate=0.5,
        regularizer=fluid.regularizer.L2Decay(1.0),
        trainable=True)
    return param


class SampleNN:
    def __init__(self, mode: int = 1):
        self.mode = mode

    def sample_layer(self, fc):
        hid_dim = 400
        stacked_num = 3
        # lstm层
        lstm1, cell1 = fluid.layers.dynamic_lstm(input=fc, size=hid_dim)

        inputs = [fc, lstm1]

        # 其余的所有栈结构
        for i in range(2, stacked_num + 1):
            fc = fluid.layers.fc(input=inputs, size=hid_dim)
            lstm, cell = fluid.layers.dynamic_lstm(
                input=fc, size=hid_dim, is_reverse=(i % 2) == 0)
            inputs = [fc, lstm]

        # 池化层
        fc_last = fluid.layers.sequence_pool(input=inputs[0], pool_type='max')
        lstm_last = fluid.layers.sequence_pool(input=inputs[1], pool_type='max')
        final = fluid.layers.fc(input=[fc_last, lstm_last], size=hid_dim)
        return final

    def sample_layer2(self, fc):
        hid_dim = 300
        stacked_num = 3
        # gru层
        gru = fluid.layers.dynamic_gru(input=fc, size=hid_dim // 3)
        # 其余的所有栈结构
        tmp = gru
        for i in range(2, stacked_num + 1):
            tmp = fluid.layers.fc(input=tmp, size=hid_dim)
            tmp = fluid.layers.dynamic_gru(
                input=tmp, size=hid_dim // 3, is_reverse=(i % 2) == 0)

        # 池化层
        fc_last = fluid.layers.sequence_pool(input=tmp, pool_type='max')
        final = fluid.layers.fc(input=fc_last, size=hid_dim)
        return final

    def main_network(self, sentence_input, keyword_input, virtual_input):
        hid_dim = 300

        sentence_input = fluid.embedding(input=sentence_input, size=[3096, 100], is_sparse=True)
        keyword_input = fluid.embedding(input=keyword_input, size=[3096, 100], is_sparse=True)
        virtual_input = fluid.embedding(input=virtual_input, size=[3096, 100], is_sparse=True)
        # 第一层栈
        # 全连接层
        fc1 = fluid.layers.fc(input=sentence_input, size=hid_dim)
        fc2 = fluid.layers.fc(input=keyword_input, size=hid_dim)
        fc3 = fluid.layers.fc(input=virtual_input, size=hid_dim)
        final1 = self.sample_layer2(fc1)
        final2 = self.sample_layer2(fc2)
        final3 = self.sample_layer2(fc3)
        # 全连接层，softmax预测
        tmp = fluid.layers.fc(input=[final1, final2, final3], size=200, act='relu')
        # tmp = fluid.layers.fc(input=tmp, size=50, act="relu", param_attr=parm_msra())
        # tmp = fluid.layers.fc(input=tmp, size=10, act="relu", param_attr=parm_msra())
        # tmp = fluid.layers.batch_norm(tmp)
        prediction = fluid.layers.fc(input=tmp, size=1, act="tanh")

        return prediction

# # debug
# data = fluid.data(name="test", shape=[-1], dtype="int64", lod_level=1)
# SampleNN().main_network(data)
