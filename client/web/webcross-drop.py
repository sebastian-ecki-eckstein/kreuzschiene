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
print('<title>Kreuzschiene Matrix Anzeige</title>')
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

print('<form action="webcross-drop.py" method="post" accept-charset="ISO-8859-1">')
print("<table>\n<tr>\n<th>OUTPUT</th>\n")
print("<th>OUTPUT</th><th>INPUT</th>")
print("<tr>")
i = 0
while i < laenge:
      print("<tr><td>"+daten[1][i]+"</td>")
      print("<td><select name='out"+str(i)+"' size='1'>")
      j = 0
      while j < laenge:
            print("<option value='"+str(j)+"'")
            if j == int(daten[0][i]):
               print(" selected")
            print(">"+daten[2][j]+"</option>")
            j = j + 1
      print("</td>")
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

