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

if form.getvalue('load'):
    #print(laenge)
    #print(form.getvalue('length'))
    kreuzclient.f_load(form.getvalue('load'))
    print('<meta http-equiv="refresh" content="15; URL=index.html">') 
    print('</head>')
    print('<body>')
    print('<h2>Hello Word! This is a test</h2>')
    print("<p>die Konfiguration wird geladen, sie werden gleich weiter geleitet<p>")
else:
    print('</head>')
    print('<body>')
    print('<h2>Hello Word! This is a test</h2>')

    daten = kreuzclient.f_get_data()
    config = kreuzclient.f_get_config()

    print('<form action="webcross-load.py" method="post" accept-charset="ISO-8859-1">')
    print("<select name='load' size='1'>")
    i = 0
    while i < len(config):
        print("<option value='"+config[i]+"'>"+config[i]+".cfg</option>")
        i = i + 1
    print('<input type="submit" value=" Absenden ">')
    print("</form>")
print('</body>')
print('</html>')
kreuzclient.end()

