
import time
import serial
import binascii


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
          config = self.f_read_config("default.cfg")
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
          return "none"

      def f_open_net_server(self):
          print("open network port")

if __name__ == '__main__':
   kreuz = kreuzschiene()
   kreuz.f_read_status()
   kreuz.f_set_output(0,10)
   kreuz.f_set_output(0,5)
   kreuz.end()

