# Author: Acer Zhang
# Datetime:2020/2/25 10:43
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from scripts.servers import Server

if __name__ == '__main__':
    server = Server(port=6889, use_gpu=True)
    server.start_ernie_tiny()
