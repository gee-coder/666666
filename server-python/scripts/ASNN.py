# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# Attention Scoring Neural Networks

import paddle.fluid as fluid
import paddle.fluid.initializer as parm_init
from paddle.fluid.param_attr import ParamAttr


def parm_msra():
    param = fluid.ParamAttr(
        initializer=parm_init.MSRA(),
        learning_rate=0.5,
        regularizer=fluid.regularizer.L2Decay(1.0),
        trainable=True)
    return param


def fc_with_name(ipt, fc_size: int, name: str, act: str = None, is_test: bool = False):
    lr = 1.0 if is_test else 0
    tmp = fluid.layers.fc(input=ipt,
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


class ASNN:
    a_out = None
    c_out = None
    out = None

    def __init__(self, mode: int = 1, fc_size: int = 300):
        self.mode = mode
        self.hidden_size = fc_size
        self.k_size = 100

    def sample_gru_layer(self, ipt, concat_fc=None, if_pool=False):
        fc_f = fluid.layers.fc(input=ipt, size=self.hidden_size)
        fc_b = fluid.layers.fc(input=ipt, size=self.hidden_size)
        gru_f = fluid.layers.dynamic_gru(input=fc_f, size=self.hidden_size // 3)
        gru_b = fluid.layers.dynamic_gru(input=fc_b, size=self.hidden_size // 3, is_reverse=True)
        out = fluid.layers.fc([gru_f, gru_b], concat_fc) if concat_fc else [gru_f, gru_b]
        if if_pool:
            out = fluid.layers.sequence_pool(out, "max")
        return out

    def classify_sim(self, ipt_a, ipt_b, ipt_c):
        gru_vec_a = self.sample_gru_layer(ipt_a, 100, True)
        gru_vec_b = self.sample_gru_layer(ipt_b, 100, True)
        gru_vec_c = self.sample_gru_layer(ipt_c, 100, True)
        sim_ab = fluid.layers.cos_sim(gru_vec_a, gru_vec_b)
        sim_cb = fluid.layers.cos_sim(gru_vec_c, gru_vec_b)
        out = fluid.layers.fc([sim_ab, sim_cb], 2, act="softmax")
        out = fluid.layers.slice(out, axes=[1], starts=[0], ends=[2])
        return out

    def kec_nn(self, ipt_a, ipt_b, ipt_c):
        gru_vec_a = self.sample_gru_layer(ipt_a)
        gru_vec_c = self.sample_gru_layer(ipt_c)
        gru_proj_a = fluid.layers.fc(gru_vec_a, size=self.k_size)
        gru_proj_c = fluid.layers.fc(gru_vec_c, size=self.k_size)

    def keyword_extraction_with_attention(self, ipt, w, name: str):
        # V3
        kea = fc_with_name(ipt, self.k_size, name + "_kea")
        pool = fluid.layers.sequence_pool(input=kea, pool_type='max')
        kea = fluid.layers.elementwise_mul(pool, w)
        return kea

    def attention(self, ipt_a, ipt_b, name: str):
        # V3
        ipt_a = fluid.layers.sequence_conv(ipt_a, 32)
        ipt_b = fluid.layers.sequence_conv(ipt_b, 32)
        pool = fluid.layers.sequence_pool(input=ipt_a, pool_type='max')
        pool_b = fluid.layers.sequence_pool(input=ipt_b, pool_type='max')
        kea2 = fc_with_name([pool, pool_b], self.k_size, name + "_kw2", "softmax")
        return kea2

    def define_network(self, ori_key_vec, virtual_input_vec, key_f_vec, key_word_f_vec, virtual_input_f_vec):
        """
        :param ori_key_vec: 原始答案VEC
        :param virtual_input_vec: 模拟输入VEC
        :param key_f_vec: 原始答案分词VEC
        :param key_word_f_vec: 答案关键字分词VEC
        :param virtual_input_f_vec: 模拟输入分词VEC
        :return:
        """
        # # V3
        # # 双向GRU网络
        # a_gru1 = self.sample_gru_layer(key_f_vec)
        # b_gru1 = self.sample_gru_layer(key_word_f_vec)
        # c_gru1 = self.sample_gru_layer(virtual_input_f_vec)
        # # 注意力机制A
        # a_attention_w2 = self.attention(a_gru1, b_gru1, "a2")
        # c_attention_w2 = self.attention(c_gru1, b_gru1, "c2")
        # a_kea4 = self.keyword_extraction_with_attention(a_gru1, a_attention_w2, "k")
        # c_kea4 = self.keyword_extraction_with_attention(c_gru1, c_attention_w2, "k")
        # # 语义融合
        # cos_sim = fluid.layers.cos_sim(ori_key_vec, virtual_input_vec)
        # c_vec5 = fluid.layers.elementwise_mul(c_kea4, cos_sim)
        #
        # # 输出层
        # self.a_out = out_layers(a_kea4, "a_out")
        # self.c_out = out_layers(c_vec5, "c_out", is_test=True)
        # return self.c_out

        # classify_sim
        self.mode = "cs"
        cs_out = self.classify_sim(key_f_vec, key_word_f_vec, virtual_input_f_vec)
        # 语义融合
        cos_sim = fluid.layers.cos_sim(ori_key_vec, virtual_input_vec)
        self.out = fluid.layers.fc(fluid.layers.elementwise_mul(cs_out, cos_sim), 1)

        return self.out

    def req_cost(self, score):
        if self.mode == "V3":
            a_score = fluid.layers.ones_like(self.a_out)
            cost_a = fluid.layers.square_error_cost(self.a_out, a_score)
            cost_c = fluid.layers.square_error_cost(self.c_out, score)
            cost = cost_a * 0.5 + cost_c * 0.5
            loss = fluid.layers.mean(cost)
            return loss
        elif self.mode == "cs":
            cost = fluid.layers.smooth_l1(self.out, score)
            loss = fluid.layers.mean(cost)
            return loss

# debug
# data = fluid.data(name="test", shape=[-1, 1024], dtype="float32", lod_level=1)
# s = fluid.data(name="test2", shape=[1], dtype="float32")
# net = ASNN()
# net.define_network(data, data, data, data, data)
# net.req_cost(s)
