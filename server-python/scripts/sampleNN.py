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


def sample_gru_layer(fc):
    hid_dim = 300
    stacked_num = 3
    tmp = fc
    for i in range(1, stacked_num + 1):
        tmp = fluid.layers.dynamic_gru(
            input=tmp, size=hid_dim // 3, is_reverse=(i % 2) == 0)
        tmp = fluid.layers.fc(input=tmp, size=hid_dim)
    return tmp


class SampleNN:
    def __init__(self, mode: int = 1):
        self.mode = mode

    def main_network(self, sentence_input, keyword_input, sentence_n_input, keyword_n_input, virtual_input):
        hid_dim = 300

        sentence_input = fluid.embedding(input=sentence_input, size=[3096, 100], is_sparse=True)
        keyword_input = fluid.embedding(input=keyword_input, size=[3096, 100], is_sparse=True)
        virtual_input = fluid.embedding(input=virtual_input, size=[3096, 100], is_sparse=True)
        sentence_n_input = fluid.embedding(input=sentence_n_input, size=[32, 100], is_sparse=True)
        keyword_n_input = fluid.embedding(input=keyword_n_input, size=[32, 100], is_sparse=True)

        fc1 = fluid.layers.fc(input=sentence_input, size=hid_dim)
        fc2 = fluid.layers.fc(input=sentence_n_input, size=hid_dim)
        fc3 = fluid.layers.fc(input=keyword_input, size=hid_dim)
        fc4 = fluid.layers.fc(input=keyword_n_input, size=hid_dim)
        fc5 = fluid.layers.fc(input=virtual_input, size=hid_dim)
        a_out1 = sample_gru_layer(fc1)
        a_out2 = sample_gru_layer(fc2)
        b_out1 = sample_gru_layer(fc3)
        b_out2 = sample_gru_layer(fc4)
        c_out = sample_gru_layer(fc5)

        fc_a = fluid.layers.fc(input=[a_out1, a_out2], size=300)
        fc_a = sample_gru_layer(fc_a)
        fc_b = fluid.layers.fc(input=[b_out1, b_out2], size=300)
        fc_b = sample_gru_layer(fc_b)
        fc_a = fluid.layers.sequence_pool(input=fc_a, pool_type='max')
        fc_b = fluid.layers.sequence_pool(input=fc_b, pool_type='max')
        fc_c = fluid.layers.sequence_pool(input=c_out, pool_type='max')

        tmp = fluid.layers.fc(input=[fc_a, fc_b, fc_c], size=200, act='relu')
        tmp = fluid.layers.fc(input=tmp, size=50)
        tmp = fluid.layers.fc(input=tmp, size=10)
        # tmp = fluid.layers.batch_norm(tmp)
        prediction = fluid.layers.fc(input=tmp, size=1, act="tanh")

        return prediction

# # debug
# data = fluid.data(name="test", shape=[-1], dtype="int64", lod_level=1)
# SampleNN().main_network(data)
