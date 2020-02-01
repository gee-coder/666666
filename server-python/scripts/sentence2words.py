# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from typing import List

import paddlehub as hub

from nlp_tool import add_separator_in_words
from os_tool import req_time_id

lac = hub.Module(name="lac")


def shell(input_file_path: str, out_file_path: str):
    """
    句子转分词
    :param input_file_path: 待转分词的数据
    :param out_file_path: 输出文件路径
    """
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        data = input_file.readlines()

    inputs = {"text": data}
    results = lac.lexical_analysis(data=inputs)

    with open(out_file_path, "w", encoding="utf-8") as output_file:
        for result in results:
            words = add_separator_in_words(result['word'])
            tags = add_separator_in_words(result['tag'])
            output_file.writelines(words + "," + tags + "\n")


def server(ori_text: List[str]):
    """
    分词服务
    :param ori_text: List[str] 原始文本
    :return: List[(word, feature)] 分词后的文本以及词性
    Example:
    (['今天|天气|怎么样'], ['TIME|n|r']) = server(["今天天气怎么样"])
    """

    inputs = {"text": ori_text}
    results = lac.lexical_analysis(data=inputs)
    words = [add_separator_in_words(result['word']) for result in results]
    tags = [add_separator_in_words(result['tag']) for result in results]
    return words, tags
