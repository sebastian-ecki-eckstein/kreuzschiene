#!/usr/bin/env python

import socket
from kreuzschiene_vt1616 import kreuzschiene

class kreuz_tcp_server:

      def f_analyse(self,data,conn):
          print("analyse data")
          command = data.split(':')
          print(command)
          if command[0] == "SET":
             if command[1] == "LOCK":
                print("lock/unlock device")
                if self.lock == "":
                   self.lock = str(command[2]).rstrip()
                   conn.send("ACK:LOCK:LOCK".encode('UTF-8'))
                else:
                   if self.lock == str(command[2]).rstrip():
                      self.lock == ""
                      conn.send("ACK:LOCK:UNLOCK".encode('UTF-8'))
                   else:
                      conn.send("NACK:LOCK:LOCK".encode('UTF-8'))
          if command[0] == "SET" and self.lock == "":
             if command[1] == "PORT":
                print("set port")
                if command[2][0]=="O" and command[3][0]=="I":
                   print("set output to input")
                   if self.kreuz.f_set_output(int(command[2][1:]),int(command[3][1:])):
                       backstr = "ACK:PORT:O"
                   else:
                       backstr = "NACK:PORT:0"
                   backstr=backstr+str(int(command[2][1:])).zfill(2)+":I"+str(int(command[3][1:])).zfill(2)+"\r\n"
                   conn.send(backstr.encode('UTF-8'))
             if command[1] == "NAME":
                print("set name")
                if command[2][0]=="O":
                   print("set output name")
                   if self.kreuz.f_set_output_name(int(command[2][1:]),str(command[3]).rstrip()):
                      backstr = "ACK:NAME:O"
                   else:
                       backstr = "NACK:NAME:O"
                   backstr = backstr+str(int(command[2][1:])).zfill(2)+":"+str(command[3]).rstrip()+"\r\n"
                   conn.send(backstr.encode('UTF-8'))
                if command[2][0]=="I":
                   print("set input name")
                   if self.kreuz.f_set_input_name(int(command[2][1:]),str(command[3]).rstrip()):
                       backstr = "ACK:NAME:I"
                   else:
                       backstr = "NACK:NAME:I"
                   backstr=backstr+str(int(command[2][1:])).zfill(2)+":"+str(command[3]).rstrip()+"\r\n"
                   conn.send(backstr.encode('UTF-8'))
             if command[1] == "SAVE":
                print("save config")
                if self.kreuz.f_write_config(str(command[2]).rstrip()):
                   backstr = "ACK:SAVE:"+str(command[2]).rstrip()
                else:
                   backstr = "NACK:SAVE:"+str(command[2]).rstrip()
                conn.send(backstr.encode('UTF-8'))
             if command[1] == "LOAD":
                print("load config")
                if self.kreuz.f_read_config(str(command[2]).rstrip()):
                   backstr = "ACK:LOAD:"+str(command[2]).rstrip()
                else:
                   backstr = "NACK:LOAD:"+str(command[2]).rstrip()
                conn.send(backstr.encode('UTF-8'))
          if command[0] == "SET" and command[1] != "LOCK" and self.lock != "":
             conn.send("NACK:LOCK:LOCK")
          if command[0] == "GET":
             if command[1] == "DATA":
                print("get data")
                daten = self.kreuz.f_get_data()
                datenstring = "ACK:DATA:" + str(daten[3]) + ":"
                i = 0
                while i < daten[3]:
                    datenstring = datenstring + str(daten[0][i]) + ":"
                    i = i + 1
                i = 0
                while i < daten[3]:
                    datenstring = datenstring + str(daten[1][i]) + ":"
                    i = i + 1
                i = 0
                while i < daten[3]:
                    datenstring = datenstring + str(daten[2][i]) + ":"
                    i = i + 1
                print(datenstring)
                conn.send(datenstring.encode('UTF-8'))
             if command[1] == "CONFIG":
                print("get config files")
                config = self.kreuz.f_get_config()
                conn.send("ACK:DATA:"+config)

      def __init__(self,ip='127.0.0.1',port=4242):
          self.TCP_IP = ip
          self.TCP_PORT = port
          self.BUFFER_SIZE = 1024
          self.lock = ""

          self.kreuz = kreuzschiene()
          
          self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.sock.bind((self.TCP_IP, self.TCP_PORT))
          self.sock.listen(5)

      def f_listen_forever(self):
          conn, addr = self.sock.accept()
          print('Connection address: %s', addr)
          self.f_analyse("GET:DATA:",conn)
          while 1:
                data = conn.recv(self.BUFFER_SIZE)
                #if not data: break
                datastr = data.decode(encoding='UTF-8',errors='ignore')
                self.f_analyse(datastr,conn)
          conn.close()
          self.kreuz.end()

if __name__ == '__main__':
   con = kreuz_tcp_server('',4242)
   con.f_listen_forever()
