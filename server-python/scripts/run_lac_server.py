# Author: Acer Zhang
# Datetime:2020/2/24 14:32
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from scripts.servers import Server

if __name__ == '__main__':
    server = Server(use_gpu=True)
    server.add_lac_server()
    server.start_servers(debug=True)
