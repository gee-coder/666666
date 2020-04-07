# Author: Acer Zhang
# Datetime:2020/1/31 18:38
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import time
import logging as log

import paddle.fluid as fluid
import numpy as np
from paddle_serving_client.io import save_model as save_serving_model

from scripts.CSNN import CSNN
from scripts.preprocess import reader
from scripts.os_tool import GLog

# config
FREEZE_MODE = False  # 冻结模式
LOAD_PREVAR = False  # 是否读取预训练模型
LOAD_CHECKPOINT = False  # 是否读取存档点
USE_CUDA = False
NONE_PRE = True
ROOT_PATH = r"D:\a13\module"
ERNIE_CONF_PATH = os.path.join(ROOT_PATH, "ERNIE/ernie_tiny_config.json")
DATA_CSV = os.path.join(ROOT_PATH, "example_data/nonpre_data.csv")
# VARS_PATH = os.path.join(ROOT_PATH, "pre_params")
VARS_PATH = os.path.join(ROOT_PATH, "ERNIE/params")
SAVE_INFER_MODEL_DIR = os.path.join(ROOT_PATH, "infer.model")
SAVE_SERVING_MODEL_DIR = os.path.join(ROOT_PATH, "serving")
F_NUM = 3
RANDOM_SEED = 2

config = {
    "EPOCHE_NUM": 1000,
    "BATCH_SIZE": 2,
    "BOUNDARIES": [30, 200, 500, 1000, 3000],
    "LR_STEPS": [0.01, 0.001, 0.0001, 0.00001, 0.000005, 0.000001]
}

log.basicConfig(level=log.DEBUG,
                format='%(asctime)s: %(message)s')

# environment
place = fluid.CUDAPlace(0) if USE_CUDA else fluid.CPUPlace()
controller = fluid.Executor(place)

# network
start_up_program = fluid.Program()
train_program = fluid.Program()
train_program.random_seed = RANDOM_SEED
with fluid.program_guard(train_program, start_up_program):
    ori_input_ids = fluid.data("ori_input_ids", shape=[-1, 128, 1], dtype="int64")
    ori_position_ids = fluid.data("ori_position_ids", shape=[-1, 128, 1], dtype="int64")
    ori_segment_ids = fluid.data("ori_segment_ids", shape=[-1, 128, 1], dtype="int64")
    ori_input_mask = fluid.data("ori_input_mask", shape=[-1, 128, 1], dtype="float32")
    # ori_sentence = fluid.data("ori_sentence", shape=[-1, 1], dtype="int64", lod_level=1)
    input_ids = fluid.data("input_ids", shape=[-1, 128, 1], dtype="int64")
    position_ids = fluid.data("position_ids", shape=[-1, 128, 1], dtype="int64")
    segment_ids = fluid.data("segment_ids", shape=[-1, 128, 1], dtype="int64")
    input_mask = fluid.data("input_mask", shape=[-1, 128, 1], dtype="float32")
    # sentence = fluid.data("sentence", shape=[-1, 1], dtype="int64", lod_level=1)

    scores_label = fluid.data("scores", shape=[-1, 1], dtype="int64")

    csnn = CSNN()
    csnn.conf_path = ERNIE_CONF_PATH
    net = csnn.define_network(ori_input_ids, ori_position_ids, ori_segment_ids, ori_input_mask, input_ids, position_ids,
                              segment_ids, input_mask)

    # create
    loss = csnn.req_cost(train_program, scores_label)
    val_program = train_program.clone(for_test=True)
    # create loss

    learning_rate = fluid.layers.piecewise_decay(config["BOUNDARIES"], config["LR_STEPS"])  # case1, Tensor

    optimizer = fluid.optimizer.Adam(learning_rate=learning_rate,
                                     regularization=fluid.regularizer.L2Decay(regularization_coeff=0.01))
    optimizer.minimize(loss)

# feed data
train_reader = reader(DATA_CSV, is_none_pre=NONE_PRE)
val_reader = reader(DATA_CSV, is_none_pre=NONE_PRE, is_val=True)
train_reader = fluid.io.batch(fluid.io.shuffle(train_reader, buf_size=1024), batch_size=config["BATCH_SIZE"])
val_reader = fluid.io.batch(val_reader, batch_size=config["BATCH_SIZE"])
feed_list = ["ori_input_ids", "ori_position_ids", "ori_segment_ids", "ori_input_mask", "input_ids", "position_ids",
             "segment_ids", "input_mask", "scores"]
train_feeder = fluid.DataFeeder(feed_list=feed_list,
                                place=place,
                                program=train_program)
val_feeder = fluid.DataFeeder(feed_list=feed_list,
                              place=place,
                              program=train_program)

# init log
config["val_acc"] = None
config["seed"] = None
log1 = GLog(gpack_path=ROOT_PATH + "/log", item_heads=config, file_name="train_log2", new_file=True)
FIRST_FLAG = False
DATA_NUM = 0


# define train
def controller_process(program, data_reader, feeder):
    global FIRST_FLAG, DATA_NUM
    infos = {"loss": [], "out": [], "label": []}
    for i, data in enumerate(data_reader()):
        info = controller.run(program=program,
                              feed=feeder.feed(data),
                              fetch_list=[loss, net, scores_label])
        try:
            infos["loss"].append(info[0][0])
            infos["out"].append(info[1].tolist())
            infos["label"].append(info[2].tolist())
        except Exception as e:
            print("sum loss error:", e)

    loss_info = sum(infos["loss"]) / len(infos["loss"])
    avg_error = []
    acc = dict((i, []) for i in range(F_NUM))
    for i, ii in zip(infos["out"], infos["label"]):
        tmp = np.array(i).reshape(-1) - np.array(ii).reshape(-1)
        tmp = np.abs(tmp)
        avg_error.append(np.average(tmp))
        for f in range(F_NUM):
            acc[f].append((len(tmp[tmp <= f]) - len(tmp[tmp <= f - 1])) / len(tmp))
    avg_error = sum(avg_error) / len(avg_error)
    for i in acc.keys():
        acc[i] = sum(acc[i]) / len(acc[i])
    if FIRST_FLAG is False:
        DATA_NUM = len(infos["loss"]) * config["BATCH_SIZE"] / 0.8
        log.info("\033[1;31m|TRAIN_DATA_NUM|\t|" + str(DATA_NUM) + "\033[0m")
        FIRST_FLAG = True
    msg = "\t|GARD:{:.4f}".format(loss_info) + "\t|Avg Error Rate:{:.4f} %".format(
        avg_error * 10)
    sum_acc = 0
    for i in acc.keys():
        if i <= 2:
            sum_acc += acc[i]
        msg += "\t|K" + str(i) + ":{:.2f}%".format(acc[i] * 100)
    msg += "\t|F2:{:.2f}%".format(sum_acc * 100)
    return msg, sum_acc


controller.run(start_up_program)
load_params_num = []
load_flag = False


# 读取参数模型
def if_exist(var):
    if os.path.exists(os.path.join(VARS_PATH, var.name)):
        load_params_num.append(1)
    return os.path.exists(os.path.join(VARS_PATH, var.name))


# 读取模型参数
if LOAD_PREVAR:
    log.info(msg="\033[1;31m从" + VARS_PATH + "中读取参数\033[0m")
    fluid.io.load_vars(controller, VARS_PATH, main_program=train_program, predicate=if_exist)
    log.info(msg="\033[1;31m读取" + str(len(load_params_num)) + "组参数，若参数量低于100，请检查配置文件 \033[0m")
elif LOAD_CHECKPOINT:
    load_flag = True
    log.info(msg="\033[1;31m从" + VARS_PATH + "中读取存档点\033[0m")
    fluid.io.load_persistables(controller, VARS_PATH, main_program=train_program)
    log.info(msg="\033[1;31m已读取存档点参数\033[0m")

# 冻结模式
if FREEZE_MODE:
    assert load_flag, "未读取存档点参数，无法冻结模型"
    log.info(msg="\033[1;31m开始修剪网络进行冻结\033[0m")
    fluid.io.save_inference_model(dirname=SAVE_INFER_MODEL_DIR,
                                  feeded_var_names=feed_list[:-1],
                                  target_vars=[net],
                                  executor=controller,
                                  main_program=train_program)
    save_serving_model(server_model_folder=SAVE_SERVING_MODEL_DIR + ".model",
                       client_config_folder=SAVE_SERVING_MODEL_DIR + ".config",
                       feed_var_dict={"ori_input_ids": ori_input_ids,
                                      "ori_position_ids": ori_position_ids,
                                      "ori_segment_ids": ori_segment_ids,
                                      "ori_input_mask": ori_input_mask,
                                      "input_ids": input_ids,
                                      "position_ids": position_ids,
                                      "segment_ids": segment_ids,
                                      "input_mask": input_mask},
                       fetch_var_dict={"score": net},
                       main_program=train_program)
    log.info(msg="\033[1;31m冻结完毕，单机预测模型被保存在" + SAVE_INFER_MODEL_DIR + "\033[0m")
    log.info(msg="\033[1;31m冻结完毕，Serving文件被保存在" + SAVE_INFER_MODEL_DIR + "(2组：预测模型+配置文件)\033[0m")
    exit("Done!")

val_acc = 0
max_val_acc = 0.
for epoch in range(config["EPOCHE_NUM"]):
    train_info, _ = controller_process(train_program, train_reader, train_feeder)
    start_time = time.time()
    val_info, val_acc = controller_process(val_program, val_reader, val_feeder)
    avg_sample = (time.time() - start_time) / (DATA_NUM * 0.2)
    log.info("\033[1;35m|EPOCH:" + str(epoch) + "\t|SAMPLE TIME:{:.6f}/s".format(avg_sample) + "\033[0m")
    log.info("\033[1;34m|TRAIN:" + train_info + "\033[0m")
    log.info("\033[1;34m|VAL:" + val_info + "\033[0m")
    if max_val_acc < val_acc:
        max_val_acc = val_acc
        fluid.io.save_persistables(controller, "./save_params", main_program=train_program)

config["seed"] = train_program.random_seed
config["val_acc"] = "{:.4f} %".format(val_acc / config["EPOCHE_NUM"] * 100)

log1.write_log(config, message="V3")
log.info("\033[1;33m训练结束\033[0m")
