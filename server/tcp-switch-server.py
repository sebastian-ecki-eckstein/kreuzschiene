#!/usr/bin/env python

import socket
import kreuzschiene from kreuzschiene-vt1616.py

class kreuz_tcp_server:

      def f_analyse(self,data,conn):
          print("analyse data")
          command = data.split(':')
          print(command)
          if command[0] == "SET":
             if command[1] == "LOCK":
                print("lock/unlock device")
                if self.lock == "":
                   self.lock = str(chomp(command[2]))
                   conn.send("ACK:LOCK:LOCK")
                else:
                   if self.lock == str(chomp(command[2])):
                      self.lock == ""
                      conn.send("ACK:LOCK:UNLOCK")
                   else:
                      conn.send("NACK:LOCK:LOCK")
          if command[0] == "SET" and self.lock == "":
             if command[1] == "PORT":
                print("set port")
                if command[2][0]=="O" and command[3][0]=="I":
                   print("set output to input")
                   if self.kreuz.f_set_output(int(command[2][1:]),int(command[3][1:])):
                      conn.send("ACK:PORT:O"+str(int(command[2][1:])).zfill(2)+":I"+str(int(command[3][1:])).zfill(2)+"\r\n")
                   else:
                      conn.send("NACK:PORT:O"+str(int(command[2][1:])).zfill(2)+":I"+str(int(command[3][1:])).zfill(2)+"\r\n")
             if command[1] == "NAME":
                print("set name")
                if command[2][1]=="O":
                   print("set output name")
                   if self.kreuz.f_set_output_name(int(command[2][1:]),str(chomp(command[3]))):
                      conn.send("ACK:NAME:O"++str(int(command[2][1:])).zfill(2)+":str(chomp(command[3]))+"\r\n")
                   else:
                      conn.send("NACK:NAME:O"++str(int(command[2][1:])).zfill(2)+":str(chomp(command[3]))+"\r\n")
                if command[2][1]=="I":
                   print("set input name")
                   if self.kreuz.f_set_input_name(int(command[2][1:]),str(chomp(command[3]))):
                      conn.send("ACK:NAME:I"++str(int(command[2][1:])).zfill(2)+":str(chomp(command[3]))+"\r\n")
                   else:
                      conn.send("NACK:NAME:I"++str(int(command[2][1:])).zfill(2)+":str(chomp(command[3]))+"\r\n")
             if command[1] == "SAVE":
                print("save config")
                if self.kreuz.f_write_config(str(chomp(command[2]))):
                   conn.send("ACK:SAVE:"+str(chomp(command[2])))
                else:
                   conn.send("NACK:SAVE:"+str(chomp(command[2])))
             if command[1] == "LOAD":
                print("load config")
                if self.kreuz.f_read_config(str(chomp(command[2]))):
                   conn.send("ACK:LOAD:"+str(chomp(command[2])))
                else:
                   conn.send("NACK:LOAD:"+str(chomp(command[2])))
          if command[0] == "SET" and command[1] != "LOCK" and self.lock != "":
             conn.send("NACK:LOCK:LOCK")
          if command[0] == "GET":
             if command[1] == "DATA":
                print("get data")
                daten = self.kreuz.f_get_data()
                conn.send("ACK:DATA:"+daten[0]+":"+daten[1]+":"+daten[2])
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
          print 'Connection address:', addr
          self.f_analyse("GET:DATA:",conn)
          while 1:
                data = conn.recv(self.BUFFER_SIZE)
                #if not data: break
                self.f_analyse(data,conn)
          conn.close()
          self.kreuz.end()

if __name__ == '__main__':
   con = kreuz_tcp_server()
   con.f_listen_forever()
