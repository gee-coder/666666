# Author: Acer Zhang
# Datetime:2020/1/29 22:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
from typing import List


def add_separator_in_list(input_list: List[str]) -> str:
    """
    为分词数据增加分隔符
    :param input_list:List[str] 输入数据
    :return:str 分割后字符串数据
    Example:
    '今天|天气|怎么样' = add_separator_in_list(['今天', '天气', '怎么样'])
    """
    container = "|".join(input_list).replace("|\n", "")
    return container
