# Author: Acer Zhang
# Datetime:2020/3/19 11:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddlehub as hub

# Load ernie pretrained model
module = hub.Module(name="ernie_tiny")
inputs, outputs, program = module.context(trainable=True, max_seq_len=128)

# Must feed all the tensor of ernie's module need
input_ids = inputs["input_ids"]
position_ids = inputs["position_ids"]
segment_ids = inputs["segment_ids"]
input_mask = inputs["input_mask"]

print(input_ids)