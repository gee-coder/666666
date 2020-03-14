# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# Attention Scoring Neural Networks

import numpy as np
import paddle.fluid.layers as layers
import paddle.fluid.initializer as parm_init
from paddle.fluid.param_attr import ParamAttr


def fc_with_name(ipt, fc_size: int, name: str, act: str = None, is_test: bool = False):
    lr = 1.0 if is_test else 0
    tmp = layers.fc(input=ipt,
                    size=fc_size,
                    param_attr=ParamAttr(name=name + '_fc_w_', learning_rate=lr),
                    bias_attr=ParamAttr(name=name + '_fc_b_', learning_rate=lr),
                    act=act)
    return tmp


def out_layers(ipt, name: str, is_test: bool = False):
    tmp = ipt
    # tmp = fc_with_name(tmp, 128, name + "_out1_", act="relu", is_test=is_test)
    tmp = fc_with_name(tmp, 32, name + "_out2_", act="relu", is_test=is_test)
    tmp = fc_with_name(tmp, 1, name + "_out3_", act="tanh", is_test=is_test)
    return tmp


def count_loss(ipt_a, ipt_b):
    a = np.array(ipt_a)
    b = np.array(ipt_b)
    cost = np.abs(a - b) - 1
    cost = np.round(cost, 1)
    loss = np.mean(cost)
    return loss


def key_attention(ipt_a, ipt_b, ipt_c):
    sim_ab = layers.cos_sim(ipt_a, ipt_b)
    sim_cb = layers.cos_sim(ipt_a, ipt_c)
    out = layers.fc([sim_ab, sim_cb], 2, act="softmax")
    out = layers.slice(out, axes=[1], starts=[0], ends=[1])
    return out


class ASNN:
    a_out = None
    c_out = None
    out = None

    def __init__(self, mode: int = 1, fc_size: int = 300):
        self.mode = mode
        self.hidden_size = fc_size
        self.k_size = 100

    def sample_gru_layer(self, ipt, concat_fc=None, if_pool=False):
        fc_f = layers.fc(input=ipt, size=self.hidden_size)
        fc_b = layers.fc(input=ipt, size=self.hidden_size)
        gru_f = layers.dynamic_gru(input=fc_f, size=self.hidden_size // 3)
        gru_b = layers.dynamic_gru(input=fc_b, size=self.hidden_size // 3, is_reverse=True)
        out = layers.fc([gru_f, gru_b], concat_fc) if concat_fc else [gru_f, gru_b]
        if if_pool:
            p_out = layers.sequence_pool(out, "max")
            return out, p_out
        return out

    def classify_sim(self, ipt_a, ipt_b, ipt_c):
        _, gru_vec_a = self.sample_gru_layer(ipt_a, 100, True)
        _, gru_vec_b = self.sample_gru_layer(ipt_b, 100, True)
        _, gru_vec_c = self.sample_gru_layer(ipt_c, 100, True)
        out = key_attention(gru_vec_a, gru_vec_b, gru_vec_c)
        return out

    def define_network(self, ori_key_vec, virtual_input_vec, key_f_vec, key_word_f_vec, virtual_input_f_vec):
        """
        :param ori_key_vec: 原始答案VEC
        :param virtual_input_vec: 模拟输入VEC
        :param key_f_vec: 原始答案分词VEC
        :param key_word_f_vec: 答案关键字分词VEC
        :param virtual_input_f_vec: 模拟输入分词VEC
        :return:
        """

        # # classify_sim
        # self.mode = "cs"
        # cs_out = self.classify_sim(key_f_vec, key_word_f_vec, virtual_input_f_vec)
        # # 语义融合
        # cos_sim = layers.cos_sim(ori_key_vec, virtual_input_vec)
        # self.out = layers.fc(layers.elementwise_mul(cs_out, cos_sim), 1)

        # kea V4

        # ipt
        layer_a1, layer_p_a1 = self.sample_gru_layer(key_f_vec, 100, True)
        layer_b1, layer_p_b1 = self.sample_gru_layer(key_word_f_vec, 100, True)
        layer_c1, layer_p_c1 = self.sample_gru_layer(virtual_input_f_vec, 100, True)
        # Road Main
        layer_w_rm1 = layers.fc([layer_p_a1, layer_p_b1], 3)
        # Road A
        sim_ab1 = layers.cos_sim(layer_p_a1, layer_p_a1)
        sim_cb1 = layers.cos_sim(layer_p_c1, layer_p_a1)
        out_sim_ra2 = layers.fc([sim_ab1, sim_cb1], 1, act="tanh")
        # layer_ab_ra1 = layers.elementwise_mul(layer_p_a1, layer_p_b1)
        # layer_cb_ra1 = layers.elementwise_mul(layer_p_c1, layer_p_b1)
        # out_sim_ra3 = layers.cos_sim(layer_ab_ra1, layer_cb_ra1)
        # Road B
        out_sim_rb = key_attention(layer_p_a1, layer_p_b1, layer_p_c1)
        # Road C
        out_sim_rc1 = layers.cos_sim(ori_key_vec, virtual_input_vec)
        # Road Out
        layer_out_abc = layers.concat([out_sim_ra2, out_sim_rb, out_sim_rc1], axis=1)
        layer_mul_abc = layers.elementwise_mul(layer_w_rm1, layer_out_abc)
        self.out = layers.reduce_sum(layer_mul_abc, dim=1, keep_dim=True)

        return self.out

    def req_cost(self, score):
        cost = layers.smooth_l1(self.out, score)
        loss = layers.mean(cost)
        return loss

# # debug
# import paddle.fluid as fluid
#
# data = fluid.data(name="test", shape=[-1, 1024], dtype="float32", lod_level=1)
# s = fluid.data(name="test2", shape=[1], dtype="float32")
# net = ASNN()
# net.define_network(data, data, data, data, data)
# net.req_cost(s)
