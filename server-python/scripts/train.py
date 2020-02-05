# Author: Acer Zhang
# Datetime:2020/1/31 18:38
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddle.fluid as fluid
import numpy as np

from sampleNN import SampleNN
from scripts.preprocess import reader

# config
use_cuda = False
data_csv_path = r"D:\a13\server-python\example_data\demo_data.csv"
index_gpack_path = r"D:\a13\server-python\example_data\index.gpack"
# environment

place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
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
train_reader = reader(data_csv_path, index_gpack_path, debug=False)
val_reader = reader(data_csv_path, index_gpack_path, debug=False, is_val=True)
train_reader = fluid.io.batch(fluid.io.shuffle(train_reader, buf_size=1024), batch_size=32)
val_reader = fluid.io.batch(val_reader, batch_size=32)
train_feeder = fluid.DataFeeder(feed_list=['sentence', "keyword", "virtual", "scores"], place=place,
                                program=train_program)
val_feeder = fluid.DataFeeder(feed_list=['sentence', "keyword", "virtual", "scores"], place=place,
                              program=train_program)


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
    return "\t|loss:{:4f}".format(loss_info), "\t|Accuracy:{:.4f} %".format(acc * 100)


controller.run(start_up_program)
for epoch in range(20):
    train_info = controller_process(train_program, train_reader, train_feeder)
    val_info = controller_process(val_program, val_reader, val_feeder)
    print("|TRAIN|\t|Epoch:", epoch, train_info[0], train_info[1], "|\t\t|VAL|", val_info[1])
