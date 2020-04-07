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

SMOOTH_GRAIN = 0.1
SMOOTH_SCALE = (CLASSIFY_NUM - SMOOTH_GRAIN) / (SMOOTH_SCORE * 2 + 1)


def _gt_score_loss(net_out, target_label):
    # 转换格式
    net_out = np.array(net_out).reshape(-1, CLASSIFY_NUM)
    target_label = np.array(target_label).reshape(-1, CLASSIFY_NUM)
    # 生成梯度模版
    d_out = np.zeros_like(target_label)
    # 获取标签索引
    label_index = np.argmax(target_label, axis=1)
    out_index = np.argmax(net_out, 1)
    # 遍历每组数据
    for sample_id in range(label_index.shape[0]):
        # 若在网络输出在合理区间，则不严重惩罚
        if label_index[sample_id] in [i for i in
                                      range(out_index[sample_id] - SMOOTH_SCORE,
                                            out_index[sample_id] + SMOOTH_SCORE + 1)]:
            # 计算标注梯度
            d_out[sample_id] = net_out[sample_id] - target_label[sample_id]
            # 对在平滑区域内梯度进行重新计算
            for index in range(label_index[sample_id] - SMOOTH_SCORE, label_index[sample_id] + SMOOTH_SCORE):
                # 过滤掉索引外的标签
                if 0 < index < CLASSIFY_NUM:
                    # 如果为主标签，则严重惩罚
                    tmp_scale = SMOOTH_SCALE if index != label_index[sample_id] else SMOOTH_SCALE + SMOOTH_GRAIN
                    # 重新计算梯度
                    tmp_grad = net_out[sample_id][label_index[sample_id]] - (target_label[sample_id][
                                                                                 label_index[sample_id]] * tmp_scale)
                    # 防止反向惩罚
                    d_out[sample_id][index] = tmp_grad if tmp_grad < 0 else 0.

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


def kea_layer(ipt_a, ipt_b):
    def input_layers(ipt):
        emb = layers.embedding(ipt, [50006, 1024], is_sparse=True)
        tmp_f = layers.fc(emb, 300)
        tmp_b = layers.fc(emb, 300)
        tmp_f = layers.dynamic_gru(tmp_f, 100)
        tmp_b = layers.dynamic_gru(tmp_b, 100, is_reverse=True)
        tmp = layers.fc([tmp_b, tmp_f], 300)
        tmp = layers.fc(tmp, 128)
        tmp = layers.sequence_pool(tmp, "max")
        return tmp

    def conv_layers(ipt):
        emb = layers.embedding(ipt, [50006, 1024], is_sparse=True)
        tmp_f = layers.sequence_conv(emb, 32, act="relu")
        tmp_f = layers.sequence_conv(tmp_f, 64, act="relu")
        tmp_f = layers.sequence_conv(tmp_f, 128, act="relu")
        tmp_f = layers.sequence_conv(tmp_f, 256, act="relu")
        tmp_f = layers.sequence_conv(tmp_f, 512, act="relu")
        tmp = layers.fc(tmp_f, 300)
        tmp = layers.fc(tmp, 128)
        tmp = layers.sequence_pool(tmp, "max")
        return tmp

    ra_a = input_layers(ipt_a)
    ra_b = input_layers(ipt_b)
    rb_a = conv_layers(ipt_a)
    rb_b = conv_layers(ipt_b)
    sim_a = layers.fc([ra_a, ra_b], 32)
    sim_b = layers.fc([rb_a, rb_b], 32)
    # out = layers.fc([sim_a, sim_b], 11, act="softmax")
    out = layers.fc([sim_a, sim_b], 32)
    return out


def keb_layer(ipt_a, ipt_b):
    def tmp_layers(ipt):
        tmp = layers.fc(ipt, 128)
        tmp = layers.fc(tmp, 64)
        return tmp

    tmp_a = tmp_layers(ipt_a)
    tmp_b = tmp_layers(ipt_b)
    out = layers.fc([tmp_a, tmp_b], 32)
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
        r_model = ErnieModel(r_src_ids,
                             r_position_ids,
                             r_sentence_ids,
                             task_ids=None,
                             input_mask=r_input_mask,
                             config=conf)
        r_pool_feature = r_model.get_pooled_output()

        # word_feature = kea_layer(ori_sentence, sentence)
        # sentence_sim = keb_layer(l_pool_feature, r_pool_feature)
        # out = layers.fc([word_feature, sentence_sim], 32)
        out = layers.fc([l_pool_feature, r_pool_feature], 28, name="csnn")
        self.layers_out = layers.fc(out, 11, name="csnn_out")
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
