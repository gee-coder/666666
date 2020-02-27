# Author: Acer Zhang
# Datetime:2020/2/24 11:31
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import time
import os
import requests
import json
from typing import List

import jieba
import jieba.posseg as pseg
from paddlehub.serving.bert_serving import bs_client


class Server:
    def __init__(self, port: int = 6888, use_gpu: bool = False, gpu_index: int = 0, use_multiprocess: bool = False):
        """
        Server服务类
        :param port: 指定第一个端口，其它服务端口号依次加1
        :param use_gpu: 是否使用GPU加速
        :param gpu_index: 设置使用第几块GPU卡
        :param use_multiprocess: 是否使用并来发提升速度
        """
        self.server_list = []
        self.port = port
        use_gpu = " --use_gpu --gpu " + str(gpu_index) if use_gpu else " "
        use_multiprocess = " --use_multiprocess " + str(use_multiprocess).lower() if use_multiprocess else ""
        self.command = "hub serving start" + \
                       " --port " + str(port) + \
                       use_gpu + \
                       " " + use_multiprocess + \
                       " --modules"
        self.bert_command = "hub serving start bert_service" + \
                            " --port " + str(port) + \
                            use_gpu + \
                            " " + use_multiprocess + \
                            " --modules ernie_tiny"

    def add_lac_server(self, version: str = None):
        command = " lac"
        if version:
            command += "==" + version
        self.command += command

    def start_ernie_tiny(self, version: str = None):
        command = "==" + version if version else ""
        cmd = os.popen(self.bert_command + command)
        print(cmd.read())

    def start_servers(self, debug=False):
        cmd = os.popen(self.command)
        if debug:
            print(self.command)
        print(cmd.read())


class Client:
    def __init__(self, server_addr: str = "127.0.0.1:6888", ernie_tiny=False, lac=False, jb=False):
        if ernie_tiny:
            self.ernie_tiny = bs_client.BSClient(module_name="ernie_tiny", server=server_addr)
        if lac:
            self.lac = "http://" + server_addr + "/predict/text/lac"
        if jb:
            self.use_paddle = True
            jieba.enable_paddle()

    def send_to_ernie_tiny_client(self, inp: list):
        """
        :param ["a", "b",...]
        :return: [[1x1024], [1x1024], ...]
        """
        return self.ernie_tiny.get_result(input_text=inp)

    def send_to_lac_client(self, inp: list):
        """
        :param ["aaa", "bbb", ...]
        :return: [[a,a,a], [b,b,b], ...], [[an,an,an], [bn,bn,bn], ...]
        """
        r = requests.post(url=self.lac, data={"text": inp})
        all_tags = []
        all_words = []
        for i in r.json()["results"]:
            all_tags.append(i["tag"])
            all_words.append(i["word"])
        return all_tags, all_words

    def run_jb_client(self, inp: list):
        """
        :param ["aaa", "bbb", ...]
        :return: [[a,a,a], [b,b,b], ...], [[an,an,an], [bn,bn,bn], ...]
        """
        all_tags = []
        all_words = []
        for i in inp:
            outs = pseg.cut(i, use_paddle=self.use_paddle)
            words = []
            ns = []
            for w, n in outs:
                words.append(w)
                ns.append(n)
            all_words.append(words)
            all_tags.append(ns)
        return all_tags, all_words

# client = Client(lac=True)
# tmp = client.send_to_lac_client(["天气真的好"])
# print(tmp)
