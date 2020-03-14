# Author: Acer Zhang
# Datetime:2020/3/10 22:28
# Copyright belongs to the author.
# Please indicate the source for reprinting.


import paddle.fluid as fluid

a = fluid.data(name="a", shape=[1], dtype="int64")
data = fluid.layers.fill_constant(shape=[1], value=0, dtype='int64')
fluid.layers.Print(data)

place = fluid.CPUPlace()
exe = fluid.Executor(place)

exe.run(feed={"a": 1})
