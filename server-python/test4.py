# Author: Acer Zhang
# Datetime:2020/3/19 11:00
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import logging as log
import os

from scripts.os_tool import req_time_id
ROOT_PATH = r"D:\a13\server-python"
log.basicConfig(level=log.DEBUG,
                format='%(asctime)s: %(message)s',
                filename=os.path.join(ROOT_PATH, "config/" + req_time_id()))
