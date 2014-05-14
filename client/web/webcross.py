#!/usr/bin/python

import cgi,cgitb
from tcp_switch_client import kreuz_tcp_client

kreuzclient = kreuz_tcp_client()
daten = kreuzclient.f_get_data()
laenge = kreuzclient.f_get_length()
kreuzclient.end()

print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>Kreuzschien</title>')
print('</head>')
print('<body>')
print('<h2>Hello Word! This is a test</h2>')
print('<form action="webcross.py" method="post" accept-charset="ISO-8859-1">')
print("<table>\n<tr>\n<th>OUTPUT</th>\n")
i = 0
while i < laenge:
      print("<th> "+daten[2][i]+"</th>")
      i = i + 1
print("<tr>")
i = 0
while i < laenge:
      print("<tr><td>"+daten[1][i]+"</td>")
      j = 0
      while j < laenge:
            print("<td><input type='radio' name='out"+str(i)+"' value='"+str(j)+"' ")
            if j == daten[0][j]:
               print("checked")
            print("></td>")
            j = j + 1
      print("</tr>")
      i = i + 1
print("</th>")
print('</body>')
print('</html>')
