# Author: Acer Zhang
# Datetime:2020/1/31 18:38
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

import paddle.fluid as fluid
import numpy as np

from scripts.sampleNN import SampleNN
from scripts.preprocess import reader
from scripts.os_tool import GLog

# config
USE_CUDA = False
ROOT_PATH = r"D:\a13\server-python"
DATA_CSV = os.path.join(ROOT_PATH, "example_data/demo_data.csv")
INDEX_GPACK = os.path.join(ROOT_PATH, "example_data/index.gpack")
config = {
    "EPOCHE_NUM": 20,
    "BATCH_SIZE": 4
}

# environment

place = fluid.CUDAPlace(0) if USE_CUDA else fluid.CPUPlace()
controller = fluid.Executor(place)

# network
start_up_program = fluid.Program()
train_program = fluid.Program()
with fluid.program_guard(train_program, start_up_program):
    sentence_input = fluid.data("sentence", shape=[-1], dtype="int64", lod_level=1)
    keyword_input = fluid.data("keyword", shape=[-1], dtype="int64", lod_level=1)
    virtual_input = fluid.data("virtual", shape=[-1], dtype="int64", lod_level=1)
    scores_label = fluid.data("scores", shape=[-1, 1], dtype="float32")
    net = SampleNN().main_network(sentence_input, keyword_input, virtual_input)
    # fluid.layers.Print(net)

    cost = fluid.layers.square_error_cost(net, scores_label)
    loss = fluid.layers.mean(cost)
    val_program = train_program.clone(for_test=True)
    optimizer = fluid.optimizer.Adam(learning_rate=0.001)
    optimizer.minimize(loss)

# feed data
train_reader = reader(DATA_CSV, INDEX_GPACK, debug=False)
val_reader = reader(DATA_CSV, INDEX_GPACK, debug=False, is_val=True)
train_reader = fluid.io.batch(fluid.io.shuffle(train_reader, buf_size=1024), batch_size=config["BATCH_SIZE"])
val_reader = fluid.io.batch(val_reader, batch_size=config["BATCH_SIZE"])
train_feeder = fluid.DataFeeder(feed_list=['sentence', "keyword", "virtual", "scores"], place=place,
                                program=train_program)
val_feeder = fluid.DataFeeder(feed_list=['sentence', "keyword", "virtual", "scores"], place=place,
                              program=train_program)

# init log
config["val_acc"] = None
config["seed"] = None
log = GLog(gpack_path=r"D:\a13\server-python\config", item_heads=config, file_name="train_log")


# define train
def controller_process(program, data_reader, feeder):
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
    acc = [np.average(np.abs(np.array(i) - np.array(ii)).flatten()) for i, ii in zip(infos["out"], infos["label"])]
    acc = 1 - sum(acc) / len(acc)
    return "\t|loss:{:4f}".format(loss_info), "\t|Accuracy:{:.4f} %".format(acc * 100), acc


val_acc = 0
controller.run(start_up_program)
for epoch in range(config["EPOCHE_NUM"]):
    train_info = controller_process(train_program, train_reader, train_feeder)
    val_info = controller_process(val_program, val_reader, val_feeder)
    print("|TRAIN|\t|Epoch:", epoch, train_info[0], train_info[1], "|\t\t|VAL|", val_info[1])
    val_acc += val_info[2]

config["seed"] = train_program.random_seed
config["val_acc"] = val_acc / config["EPOCHE_NUM"]
log.write_log(config, massage="训练参数")
print("\n==========END==========\n|VAL Avg Accuracy:\t{:.4f} %".format(config["val_acc"] * 100))
