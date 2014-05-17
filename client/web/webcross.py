#!/usr/bin/python

import cgi,cgitb
from tcp_switch_client import kreuz_tcp_client

#print("init")
kreuzclient = kreuz_tcp_client()
#print("hole daten")
daten = kreuzclient.f_get_data()
#print("anzahl")
laenge = kreuzclient.f_get_length()

cgitb.enable(display=1, logdir="/tmp/")
form = cgi.FieldStorage()

print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>Kreuzschien</title>')
print('</head>')
print('<body>')
print('<h2>Hello Word! This is a test</h2>')

if form.getvalue('length'):
    #print(laenge)
    #print(form.getvalue('length'))
    if str(laenge) == form.getvalue('length'):
        #print("gleich lang")
        i = 0
        while i < laenge:
            #print(daten[0][i])
            #print(form.getvalue('out'+str(i)))
            if daten[0][i] != form.getvalue('out'+str(i)):
                print('<p>update port '+str(daten[1][i])+' to '+str(form.getvalue('out'+str(i)))+'</p>')
                kreuzclient.f_set_output(i,int(form.getvalue('out'+str(i))))
            i = i + 1

daten = kreuzclient.f_get_data()

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
            if j == int(daten[0][i]):
               print("checked")
            print("></td>")
            j = j + 1
      print("</tr>")
      i = i + 1
print("</th>")
print("</table>")
print('<input type="hidden" name="length" value="'+str(laenge)+'">')
print('<input type="submit" value=" Absenden ">')
print("</form>")
print('</body>')
print('</html>')
kreuzclient.end()

