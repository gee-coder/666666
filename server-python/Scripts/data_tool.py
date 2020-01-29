# Author: Acer Zhang
# Datetime:2020/1/29 22:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os


def add_separator_in_list(input_list: list, pop=False):
    end_index = -1
    if pop:
        end_index = -2
    return [text + "|" for text in input_list[:end_index]] + [input_list[end_index]]

