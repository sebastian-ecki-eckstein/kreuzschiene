
import time
import serial


class kreuzschiene:

      def f_detect_ser(self):
          print "detect serial port"
          self.ser = serial.Serial(port=0, baudrate=19200, timeout=1, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)
          print self.ser.name
          self.f_generate_matrix()

      def f_generate_matrix(self):
          print "generate output, input matrix"
          ABFRAGE="\xc0\x00"
          self.ser.write(ABFRAGE)
          s = self.ser.read(200)
          print s
          self.length = 10
          self.output = []
          self.outputname = []
          for x in range(0, self.length):
              self.output.append(x)
              self.outputname.append("none")
              self.f_set_output(x,0)
          return TRUE

      def __init__(self):
          print "init"
          self.f_detect_ser()
          config = self.f_read_config("default.cfg"):
          if config != "none":
             print "schreibe neue config solange bis config = zustand"
          self.f_open_net_server()

      def f_read_status(self):
          print "read"
          ABFRAGE="\xc0\x00"
          self.ser.write(ABFRAGE)
          s = self.ser.read(self.length)
          print s

      def f_set_output(self, output, input):
          print "set output"

      def end(self):
          self.ser.close()

      def f_read_config(self,name):
          print "read config"
          return "none"

      def f_open_net_server(self):
          print "open network port"

if __name__ == '__main__':
   kreuz = kreuzschiene()
   kreuz.f_read_status()
   kreuz.end()

