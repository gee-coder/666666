# Author: Acer Zhang
# Datetime:2020/3/10 22:28
# Copyright belongs to the author.
# Please indicate the source for reprinting.


import numpy as np

a = np.array([2, 3])
a[-a <= 2] = 0.5
print(a.reshape(-1))
