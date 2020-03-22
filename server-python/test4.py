# Author: Acer Zhang
# Datetime:2020/3/19 11:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddle.fluid as f

p1 = f.Program()
p2 = f.Program()

with f.program_guard(p1):
    a = f.data("a", [1], "int64")
    a1 = f.layers.fill_constant([1], "int64", 1, out=a)
    f.layers.Print(a)

with f.program_guard(p2):
    b = f.data("a", [1], "int64")
    b1 = f.layers.fill_constant([1], "int64", 2, out=b)
    f.layers.Print(b)

exe = f.Executor(f.CPUPlace())

exe.run(p1)
exe.run(p2)
with f.program_guard(p1):
    f.layers.Print(a)
exe.run(p1)
