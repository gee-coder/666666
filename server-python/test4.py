# Author: Acer Zhang
# Datetime:2020/3/19 11:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import numpy as np

SMOOTH_SCORE = 2
CLASSIFY = 6
# label
target_label = np.array([[0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0]])
# out
# b = np.array([[0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0]])
net_out = np.array([[0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1]])

# d_out = np.zeros_like(target_label)
# label_index = np.argmax(target_label, axis=1)
# out_index = np.argmax(net_out, 1)
# for sample_id in range(label_index.shape[0]):
#     if label_index[sample_id] in [i for i in
#                                   range(out_index[sample_id] - SMOOTH_SCORE, out_index[sample_id] + SMOOTH_SCORE + 1)]:
#         print(target_label[sample_id][label_index[sample_id]], "index", sample_id, label_index[sample_id], "pass")
#         d_out[sample_id] = net_out[sample_id] - target_label[sample_id]
#         for index in range(label_index[sample_id] - SMOOTH_SCORE, label_index[sample_id] + SMOOTH_SCORE):
#             if 0 < index < CLASSIFY:
#                 d_out[sample_id][index] = 0.
#     else:
#         d_out[sample_id] = net_out[sample_id] - target_label[sample_id]
print(d_out)
