# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import argparse
import time
from typing import List

import paddlehub as hub

from nlp_tool import add_separator_in_words

parser = argparse.ArgumentParser()

parser.add_argument("--input_file", '--f', default=None, type=str, help="待转换文件所在位置")
parser.add_argument("--out_file", '--o',
                    default="./out_" + str(time.strftime("%Y-%m-%d-%H-%M", time.localtime())) + ".csv",
                    type=str,
                    help="转换后文件输出路径")
parser.add_argument("--shell_server", '--s', default=None, type=str, help="单条语句模式(服务端, 仅传入字符串)")

args = parser.parse_args()
lac = hub.Module(name="lac")


def shell():
    if args.server:
        data = [args.server]
    else:
        with open(args.input_file, "r", encoding="utf-8") as input_file:
            data = input_file.readlines()

    inputs = {"text": data}
    results = lac.lexical_analysis(data=inputs)

    with open(args.out_file, "w", encoding="utf-8") as output_file:
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


if __name__ == '__main__':
    shell()
