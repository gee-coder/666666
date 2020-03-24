# Author: Acer Zhang
# Datetime:2020/3/19 11:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import numpy as np

acc = dict((i, []) for i in range(3))
tmp = np.array([0.1, 0., 0.2])
acc[0].append((len(tmp[tmp <= 0 * 0.1 + 0.1]) - len(tmp[tmp <= 0 * 0.1])) / len(tmp))
print(acc)
