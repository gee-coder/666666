# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# Attention Scoring Neural Networks

import numpy as np
import paddle.fluid as fluid
import paddle.fluid.layers as layers
from ERNIE.ERNIE_Tiny import ErnieModel, ErnieConfig

SMOOTH_SCORE = 1
CLASSIFY_NUM = 11

SMOOTH_SCALE = 0.8


def _gt_score_loss(net_out, target_label):
    # 转换格式
    net_out = np.array(net_out).reshape(-1, CLASSIFY_NUM)
    target_label = np.array(target_label).reshape(-1, CLASSIFY_NUM)
    # 生成梯度模版
    d_out = np.zeros_like(target_label)
    # 获取标签索引 label_index即为标签在独热码中下标
    label_index = np.argmax(target_label, axis=1)
    out_index = np.argmax(net_out, 1)
    # 遍历每组数据
    for sample_id in range(label_index.shape[0]):
        # 若在网络输出在合理区间，则不严重惩罚
        if label_index[sample_id] in [i for i in
                                      range(out_index[sample_id] - SMOOTH_SCORE,
                                            out_index[sample_id] + SMOOTH_SCORE + 1)]:
            # 计算标注梯度
            target_label[sample_id][:] = -1.
            target_label[sample_id][max(0, label_index[sample_id] - SMOOTH_SCORE):min(CLASSIFY_NUM, label_index[
                sample_id] + SMOOTH_SCORE)] = SMOOTH_SCALE
            d_out[sample_id] = net_out[sample_id] - target_label[sample_id]
            for index in range(max(0, label_index[sample_id] - SMOOTH_SCORE),
                               min(CLASSIFY_NUM, label_index[sample_id] + SMOOTH_SCORE)):
                if d_out[sample_id][index] > 0:
                    d_out[sample_id][index] = 0.
        else:
            d_out[sample_id] = net_out[sample_id] - target_label[sample_id]
    # # 获取置信度
    # out_score = net_out * target_label
    # out_score = out_score[out_score > 0]
    # # 计算损失
    # cost = -np.average(np.log(out_score))
    # return cost
    return d_out


def _backward_gt_score(net_out, target_label, ret_loss, d_higher):
    ret_loss = np.array(ret_loss).reshape(-1, 11)
    #  = np.power(np.e, ret_loss)
    d_out = ret_loss
    return d_higher * d_out, 0


class KeaNN:
    conf_path = None

    def __init__(self):
        self.layers_out = None
        self.confidence = None
        self.clock = True

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
        r_model = ErnieModel(r_src_ids,
                             r_position_ids,
                             r_sentence_ids,
                             task_ids=None,
                             input_mask=r_input_mask,
                             config=conf)
        r_pool_feature = r_model.get_pooled_output()
        l_pool_feature.stop_gradient = self.clock
        r_pool_feature.stop_gradient = self.clock
        # l_pool_feature = layers.fc(l_pool_feature,128)
        # r_pool_feature = layers.fc(r_pool_feature,128)
        out = layers.fc([l_pool_feature, r_pool_feature], 128)
        out = layers.fc(out, 32)
        self.layers_out = layers.fc(out, 11, name="kea_out")
        self.confidence = layers.softmax(self.layers_out)
        layers_out = layers.argmax(self.layers_out, axis=1)
        return layers_out

    def req_cost(self, program, score):
        score = fluid.one_hot(score, CLASSIFY_NUM)
        loss = program.current_block().create_var(name="cosnn_loss_tmp", dtype="float32", shape=[1])
        layers.py_func(func=_gt_score_loss,
                       x=[self.layers_out, score],
                       out=loss,
                       backward_func=_backward_gt_score)
        # loss = layers.cross_entropy(self.layers_out, score)
        return layers.mean(loss)

# debug
# import paddle.fluid as fluid
# data = fluid.data(name="test1", shape=[-1, 128, 1], dtype="int64")
# data2 = fluid.data(name="test2", shape=[-1, 128, 1], dtype="float32")
# s = fluid.data(name="test3", shape=[1], dtype="float32")
# net = CSNN()
# net.conf_path = r"D:\a13\server-python/ERNIE/ernie_tiny_config.json"
# a = net.define_network(data, data, data, data2, data, data, data, data2)
