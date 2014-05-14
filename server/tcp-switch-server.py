#!/usr/bin/env python

import socket

class kreuz_tcp_server:

      def f_analyse(self,data,conn):
          print("analyse data")
          command = data.split(':')
          print(command)
          if command[0] == "SET":
             if command[1] == "PORT":
                print("set port")
                if command[2][0]=="O" and command[3][0]=="I":
                   print("set output to input")
                   conn.send("ACK:PORT:O"+str(int(command[2][1:])).zfill(2)+":I"+str(int(command[3][1:])).zfill(2)+"\r\n")
             if command[1] == "NAME":
                print("set name")
                if command[2][1]=="O":
                   print("set output name")
                   #chomp name
                if command[2][1]=="I":
                   print("set input name")
                   #chomp name
             if command[1] == "SAVE":
                print("save config")
             if command[1] == "LOAD":
                print("load config")
             if command[1] == "LOCK":
                print("lock/unlock device")
          if command[0] == "GET":
             print("get data")

      def __init__(self):
          self.TCP_IP = '127.0.0.1'
          self.TCP_PORT = 4242
          self.BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
          
          self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.sock.bind((self.TCP_IP, self.TCP_PORT))
          self.sock.listen(5)

      def f_listen_forever(self):
          conn, addr = self.sock.accept()
          print 'Connection address:', addr
          self.f_analyse("GET",conn)
          while 1:
                data = conn.recv(self.BUFFER_SIZE)
                #if not data: break
                self.f_analyse(data,conn)
          conn.close()

if __name__ == '__main__':
   con = kreuz_tcp_server()
   con.f_listen_forever()
