# Author: Acer Zhang
# Datetime:2020/1/29 22:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
from typing import List


def add_separator_in_words(words: List[str]) -> str:
    """
    为分词数据增加分隔符
    :param words:List[str] 输入数据
    :return:str 分割后字符串数据

    Example:
    '今天|天气|怎么样' = add_separator_in_list(['今天', '天气', '怎么样'])
    """
    container = "|".join(words).replace("|\n", "")
    return container


def keyword2label(keyword_data: List[str], server: classmethod):
    """
    关键字转标签
    :param keyword_data: 关键字数据
    :param server: 转换关键字方法
    :return: label_data:List[str], mask_data:List[str] 标签数据, 蒙版数据

    Example:
    from sentence2words import server
    input: keyword2label(["今天 天气很好 赞", "今天 天气很好 赞"], server)
    output: ([['今天', '天气', '很好', '赞'], ['今天', '天气', '很好', '赞']], [[2, 1, 1, 2], [2, 1, 1, 2]])
    """
    label_data = []
    mask_data = []
    for keywords in keyword_data:
        keywords = keywords.split(" ")
        labels = []
        masks = []
        for keyword in keywords:
            tmp = server([keyword])[0][0].split("|")
            labels += tmp
            masks += [1] * len(tmp) if len(tmp) != 1 else [2]
        label_data.append(labels)
        mask_data.append(masks)
    return label_data, mask_data
