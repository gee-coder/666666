# Author: Acer Zhang
# Datetime:2020/1/31 18:38
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddle.fluid as fluid
import numpy

from models.sampleNN import SampleNN
from scripts.preprocess import reader

# config
use_cuda = False

# environment

place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
controller = fluid.Executor(place)

# network
start_up_program = fluid.Program()
train_program = fluid.Program()
with fluid.program_guard(train_program, start_up_program):
    sentence_input = fluid.data("sentence", shape=[-1], dtype="int64", lod_level=1)
    keyword_input = fluid.data("keyword", shape=[-1], dtype="int64", lod_level=1)
    scores_label = fluid.data("scores", shape=[-1, 1], dtype="float32")
    net = SampleNN().main_network(sentence_input)
    cost = fluid.layers.square_error_cost(net, scores_label)
    loss = fluid.layers.mean(cost)
    optimizer = fluid.optimizer.Adam(learning_rate=0.001)
    optimizer.minimize(loss)

# feed data
train_feeder = fluid.io.batch(fluid.io.shuffle(reader, buf_size=1024), batch_size=32)
feeder = fluid.DataFeeder(feed_list=['sentence', 'scores'], place=place, program=train_program)
# train_reader = fluid.io.batch(reader, batch_size=32)

# start train
controller.run(start_up_program)
for epoch in range(5):
    for i, data in enumerate(train_feeder()):
        info = controller.run(program=train_program,
                              feed=data,
                              fetch_list=[loss])
        print(i, info)
