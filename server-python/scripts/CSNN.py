# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# Attention Scoring Neural Networks

import numpy as np
import paddle.fluid.layers as layers
from ERNIE.ERNIE_Tiny import ErnieModel, ErnieConfig

ignore_loss_max = 0.05


def _gt_score_loss(out_score, target_loss):
    out_score = np.array(out_score)
    target_loss = np.array(target_loss)
    cost = np.square(out_score - target_loss)
    cost[cost < np.square(ignore_loss_max)] = 0.
    return cost


def _backward_gt_score(out_score, target_score, loss, d_higher):
    out_score = np.array(out_score)
    target_score = np.array(target_score)
    d_higher = np.array(d_higher)
    d_out = 2 * (out_score - target_score)
    d_out[abs(d_out) < ignore_loss_max * 2] = 0.
    return d_higher * d_out, 0


def kea_layer(ipt_a, ipt_b):
    def tmp_layers(ipt):
        tmp = layers.fc(ipt, 512)
        tmp = layers.fc(tmp, 128)
        return tmp

    conv_a = tmp_layers(ipt_a)
    conv_b = tmp_layers(ipt_b)
    div = layers.elementwise_div(conv_b, conv_a)
    return div


def keb_layer(ipt_a, ipt_b):
    def tmp_layers(ipt):
        tmp = layers.fc(ipt, 512)
        tmp = layers.fc(tmp, 128)
        return tmp

    conv_a = tmp_layers(ipt_a)
    conv_b = tmp_layers(ipt_b)
    div = layers.cos_sim(conv_b, conv_a)
    out = layers.fc(div, 1)
    return out


class CSNN:
    conf_path = None

    def __init__(self):
        self.layers_out = None

    def define_network(self, l_src_ids, l_position_ids, l_sentence_ids, l_input_mask,
                       r_src_ids, r_position_ids, r_sentence_ids, r_input_mask):
        conf = ErnieConfig(self.conf_path)
        l_model = ErnieModel(l_src_ids,
                             l_position_ids,
                             l_sentence_ids,
                             task_ids=None,
                             input_mask=l_input_mask,
                             config=conf)
        l_pool_feature = l_model.get_pooled_output()
        l_seq_feature = l_model.get_sequence_output()
        r_model = ErnieModel(r_src_ids,
                             r_position_ids,
                             r_sentence_ids,
                             task_ids=None,
                             input_mask=r_input_mask,
                             config=conf)
        r_pool_feature = r_model.get_pooled_output()
        r_seq_feature = r_model.get_sequence_output()

        word_feature_div = kea_layer(l_seq_feature, r_seq_feature)
        sentence_sim = keb_layer(l_pool_feature, r_pool_feature)
        self.layers_out = layers.fc([word_feature_div, sentence_sim], 1, name="csnn_out")
        return self.layers_out

    def req_cost(self, program, score):
        loss = program.current_block().create_var(name="cosnn_loss_tmp", dtype="float32", shape=[1])
        layers.py_func(func=_gt_score_loss,
                       x=[self.layers_out, score],
                       out=loss,
                       backward_func=_backward_gt_score)
        return layers.mean(loss)

# debug
# import paddle.fluid as fluid
# data = fluid.data(name="test1", shape=[-1, 128, 1], dtype="int64")
# data2 = fluid.data(name="test2", shape=[-1, 128, 1], dtype="float32")
# s = fluid.data(name="test3", shape=[1], dtype="float32")
# net = CSNN()
# net.conf_path = r"D:\a13\server-python/ERNIE/ernie_tiny_config.json"
# a = net.define_network(data, data, data, data2, data, data, data, data2)
