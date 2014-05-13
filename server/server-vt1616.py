
import time
import serial
import binascii
import xml.dom.minidom as dom
import os.path

directory = "/home/ecki/kreuzschiene/config/"

class kreuzschiene:

      def f_detect_ser(self):
          print("detect serial port")
          self.ser = serial.Serial(port="/dev/ttyUSB0", baudrate=19200, timeout=1, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)
          print(self.ser.name)
          self.f_generate_matrix()

      def f_generate_matrix(self):
          print("generate output, input matrix")
          bytestring = self.f_read_status()
          parsed = self.f_parse(bytestring)
          self.length = parsed[0]
          for i in range(self.length):
              self.output.append(0)
          parsed = self.f_parse_status(bytestring)
          self.f_compare_output(parsed)
          return True

      def f_compare_output(self,parsed):
          if len(parsed) != len(self.output):
              print("arrays nicht gleich lang")
              return False
          if parsed == self.output:
              print("arrays sind gleich")
              return True
          else:
              print("speichere output")
              self.output = parsed
              return True
          
      def f_parse(self,bytestring):
          bytear = []
          for byte in bytestring:
              bytear.append(byte)
              #print(byte)
          j=0
          i=0
          while i < (len(bytear)):
              if bytear[i] == 160:
                 if bytear[i + 1]==j:
                    j = j + 1
              i = i + 1
          #print(j)
          return[j,bytear]

      def f_parse_status(self,bytestring):
          output = self.f_parse(bytestring)
          byte = output[1]
          j = output[0]
          if j != self.length:
              print("anzahl ports in status passt nicht")
              return False
          output = []
          i = 0
          while i < self.length:
              output.append(byte[3 * i + 2])
              i = i + 1
          return output

      def __init__(self):
          print("init")
          self.length = 0
          self.output = []
          self.f_detect_ser()
          config = self.f_read_config("default")
          if config != "none":
             print("schreibe neue config solange bis config = zustand")
          self.f_open_net_server()

      def f_read_status(self):
          print("read")
          ABFRAGE=b'\xc0\x00'
          self.ser.write(ABFRAGE)
          if self.length == 0:
              self.length=200
          s = self.ser.read(self.length*3 + 2)
          #print(s)
          return s

      def f_set_output(self, destination, source):
          print("set output")
          if self.output[destination] == source:
              print("schon gesetzt")
              return True
          # \xa0\xoutput\xinput
          #bytestring = str(160) + str(0) + str(0)
          bytestring = b'\xa0'
          if destination < self.length:
              convertb = bytes([destination])
              #print("dest")
              #print(convertb)
          else:
              print("ausgang nicht einstellbar")
              return False
          bytestring = bytestring + convertb
          if source < self.length:
              convertb = bytes([source])
              #print("source")
              #print(convertb)
          else:
              print("input nicht vorhanden")
              return False
          bytestring = bytestring + convertb
          #print(bytestring)
          self.ser.write(bytestring)
          s = self.ser.read(200)
          #print(s)
          status = self.f_read_status()
          #print(status)
          byte = self.f_parse_status(status)
          if byte[destination]==source:
              print("erfolgreich gesetzt")
              self.f_compare_output(byte)
              return True
          else:
              return False

      def end(self):
          self.ser.close()

      def f_read_config(self,name):
          print("read config")
          configfile = directory+name+".cfg"
          #print(configfile)
          if os.path.isfile(configfile):
             outlist = []
             inlist = []
             print("read config file")
             baum = dom.parse(configfile)
             erstesKind = baum.firstChild
             for eintrag in baum.firstChild.childNodes:
                 if eintrag.nodeName == "output":
                    #print(eintrag.getAttribute("id"))
                    outlist.append(int(eintrag.getAttribute("id")))
                    #print(eintrag.getAttribute("expr"))
                    inlist.append(int(eintrag.getAttribute("expr")))
             #print(outlist)
             #print(inlist)
             ergebnis = self.f_sort_lists(outlist,inlist)
             #print(ergebnis[0])
             #print(ergebnis[1])
             #print(ergebnis[2])
             if ergebnis[2] != self.length:
                 print("config file hat nicht richtige anzahl output")
                 return False
             else:
                 i = 0
                 while i < self.length:
                     self.f_set_output(i,ergebnis[1][i])
                     i = i + 1
                 return True
          else:
             print("no configfile found")
             return "none"

      def f_write_config(self,name):
          print("write config")
          configfile = open(directory+name+".cfg",'w')
          configfile.write("<kreuzschiene>\n")
          i = 0
          while i < self.length:
              configfile.write("  <output id='"+str(i)+"' expr='"+str(self.output[i])+"'/>\n")
              i = i + 1
          configfile.write("</kreuzschiene>\n")
          configfile.close()
          return True

      def f_sort_lists(self,outlist,inlist):
          if len(outlist) != len(inlist):
              print("nicht sortierbar")
              return False
          i = 0
          while i < len(outlist):
                k = i
                j = i
                while k < len(outlist):
                      if outlist[j] > outlist[k]:
                         j = k
                      k = k + 1
                iners = inlist[i]
                inlist[i] = inlist[j]
                inlist[j] = iners
                outers = outlist[i]
                outlist[i] = outlist[j]
                outlist[j] = outers
                i = i + 1
          return [outlist,inlist,i]

      def f_open_net_server(self):
          print("open network port")

if __name__ == '__main__':
   kreuz = kreuzschiene()
   kreuz.f_read_config("test")
   kreuz.end()

