#!/usr/bin/env python

import socket

class kreuz_tcp_client:

    def __init__(self,ip='127.0.0.1',port=4242):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 4242
        self.BUFFER_SIZE = 1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.TCP_IP, self.TCP_PORT))
        self.length = -1
        self.output = []
        self.outputname = []
        self.inputname = []
        ergebnis = self.f_get_data()
        self.output = ergebnis[0]
        self.outputname = ergebnis[1]
        self.inputname = ergebnis[2]

    def f_get_length(self):
        return self.length

    def f_get_data(self):
        self.sock.send("GET:DATA:".encode('UTF-8'))
        data = self.sock.recv(self.BUFFER_SIZE)
        datastr = data.decode(encoding='UTF-8',errors='ignore')
        splitted = datastr.split(':')
        output = []
        outputname = []
        inputname = []
        if len(splitted)>3:
            anzahl = int(splitted[2])
        else:
            return False
        if self.length == -1:
            self.length = anzahl
        i = 0
        while i < self.length:
              output.append(0)
              outputname.append('out_'+str(i))
              inputname.append('in_'+str(i))
              i = i + 1
        if anzahl != self.length:
            return False
        if len(splitted)<((self.length*3)+3):
            return False
        i = 0
        while i < self.length:
            output[i] = splitted[3+i]
            outputname[i] = splitted[(i+self.length)+3]
            inputname[i] = splitted[i+(self.length*2)+3]
            i = i + 1
        return [output,outputname,inputname]

    def f_set_output_name(self,number,name):
        print("set output name")
        if int(number) > self.length:
            return False
        sendstr = "SET:PORT:O"+str(number)+":"+name
        self.sock.send(sendstr.encode('UTF-8'))
        data = self.sock.recv(self.BUFFER_SIZE)
        datastr = data.decode(encoding='UTF-8',errors='ignore')
        splitted = datastr.split(':')
        if splitted[0] == "NACK":
            return False
        ergebnis = self.f_get_data()
        self.outputname = ergebnis[1]
        return True

    def f_set_input_name(self,number,name):
        print("set input name")
        if int(number) > self.length:
            return False
        sendstr = "SET:PORT:I"+str(number)+":"+name
        self.sock.send(sendstr.encode('UTF-8'))
        data = self.sock.recv(self.BUFFER_SIZE)
        datastr = data.decode(encoding='UTF-8',errors='ignore')
        splitted = datastr.split(':')
        if splitted[0] == "NACK":
            return False
        ergebnis = self.f_get_data()
        self.inputname = ergebnis[2]
        return True

    def f_set_output(self,outnum,innum):
        print("set output input")
        if int(outnum) > self.length or int(innum) > self.length:
            return False
        sendstr = "SET:PORT:O"+str(outnum)+":I"+str(innum)
        self.sock.send(sendstr.encode('UTF-8'))
        data = self.sock.recv(self.BUFFER_SIZE)
        datastr = data.decode(encoding='UTF-8',errors='ignore')
        splitted = datastr.split(':')
        if splitted[0] == "NACK":
            return False
        ergebnis = self.f_get_data()
        self.output = ergebnis[0]
        return True

    def f_update(self):
        ergebnis = self.f_get_data()
        self.output = ergebnis[0]
        self.outputname = ergebnis[1]
        self.inputname = ergebnis[2]
        return True

    def f_load(self,name):
        print("load config")
        sendstr = "SET:LOAD:"+str(name)
        self.sock.send(sendstr.encode('UTF-8'))
        data = self.sock.recv(self.BUFFER_SIZE)
        datastr = data.decode(encoding='UTF-8',errors='ignore')
        splitted = datastr.split(':')
        if splitted[0] == "NACK":
            return False
        self.f_update()
        return True

    def f_save(self,name):
        print("save config")
        sendstr = "SET:SAVE:"+str(name)
        self.sock.send(sendstr.encode('UTF-8'))
        data = self.sock.recv(self.BUFFER_SIZE)
        datastr = data.decode(encoding='UTF-8',errors='ignore')
        splitted = datastr.split(':')
        if splitted[0] == "NACK":
            return False
        return True

    def f_get_config(self):
        print("get config names")
        sendstr = "GET:CONFIG:"
        self.sock.send(sendstr.encode('UTF-8'))
        data = self.sock.recv(self.BUFFER_SIZE)
        return "test"

    def f_lock(self,locker):
        print("lock/unlock")
        sendstr = "SET:LOCK:"+str(locker)
        self.sock.send(sendstr.encode('UTF-8'))
        data = self.sock.recv(self.BUFFER_SIZE)
        return True

    def end(self):
        self.sock.close()

if __name__ == '__main__':
    print("start client")
