# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# Attention Scoring Neural Networks

import numpy as np
import paddle.fluid as fluid
import paddle.fluid.layers as layers
from ERNIE.ERNIE_Tiny import ErnieModel

ignore_loss_max = 0.15


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


class CSNN:

    def __init__(self):
        self.layers_out = None

    def define_network(self, l_src_ids, l_position_ids, l_sentence_ids, l_input_mask,
                       r_src_ids, r_position_ids, r_sentence_ids, r_input_mask):
        with fluid.unique_name.guard('L'):
            l_model = ErnieModel(l_src_ids, l_position_ids, l_sentence_ids, l_input_mask)
            l_pool_feature = l_model.get_pooled_output()
        with fluid.unique_name.guard('R'):
            r_model = ErnieModel(r_src_ids, r_position_ids, r_sentence_ids, r_input_mask)
            r_pool_feature = r_model.get_pooled_output()
        sim = layers.cos_sim(l_pool_feature, r_pool_feature)
        self.layers_out = layers.fc(sim, 1, name="csnn_out")
        return self.layers_out

    def req_cost(self, program, score):
        loss = program.current_block().create_var(name="cosnn_loss_tmp", dtype="float32", shape=[1])
        layers.py_func(func=_gt_score_loss,
                       x=[self.layers_out, score],
                       out=loss,
                       backward_func=_backward_gt_score)
        return layers.mean(loss)

# # debug
# import paddle.fluid as fluid
#
# data = fluid.data(name="test", shape=[-1, 1024], dtype="float32", lod_level=1)
# s = fluid.data(name="test2", shape=[1], dtype="float32")
# net = ASNN()
# net.define_network(data, data, data, data, data)
# net.req_cost(s)
