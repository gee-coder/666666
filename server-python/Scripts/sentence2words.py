# Author: Acer Zhang
# Datetime:2020/1/29 21:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import argparse
import time

import paddlehub as hub

from data_tool import add_separator_in_list

parser = argparse.ArgumentParser()

parser.add_argument("--input_file", '--f', default=None, type=str, help="待转换文件路径")
parser.add_argument("--out_file", '--o',
                    default="./out_" + str(time.strftime("%Y-%m-%d-%H-%M", time.localtime())) + ".csv",
                    type=str,
                    help="转换后文件输出路径")
parser.add_argument("--server", '--s', default=None, type=str, help="待转换文件路径")

args = parser.parse_args()

lac = hub.Module(name="lac")
if args.server:
    data = [args.server]
else:
    with open(args.input_file, "r", encoding="utf-8") as input_file:
        data = input_file.readlines()

inputs = {"text": data}
results = lac.lexical_analysis(data=inputs)

with open(args.out_file, "w", encoding="utf-8") as output_file:
    for result in results:
        words = add_separator_in_list(result['word'], pop=True)
        tags = add_separator_in_list(result['tag'])
        output_file.writelines(words + [","] + tags + ["\n"])
