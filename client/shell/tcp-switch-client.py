#!/usr/bin/env python

import socket

class kreuz_tcp_client:

    def __init__(self,ip='127.0.0.1',port=4242):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 4242
        self.BUFFER_SIZE = 1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((TCP_IP, TCP_PORT))

    def end(self):
        self.sock.close()

if __name__ == '__main__':
    print("start client")
