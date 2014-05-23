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

if form.getvalue('save'):
   erfolg = kreuzclient.f_save(form.getvalue(save))
   if erfolg == True:
      print('<meta http-equiv="refresh" content="15; URL=index.html">') 
      print('</head>')
      print('<body>')
      print('<h2>Hello Word! This is a test</h2>')
      print('<p>Konfiguration erfolgreich unter dem Namen '+form.getvalue('save')+'.cfg gespeichert</p>')
   else:
      print('</head>')
      print('<body>')
      print('<h2>Hello Word! This is a test</h2>')
      print('<p>Speichern nicht erfolgreich</p>')
      print('<p>Erneut versuchen? Speichername muss mindestens 4 Zeichen enthalten. Es sind nur Buchstaben und Zahlen zulaessig</p>')
      print('<form action="webcross-save.py" method="post" accept-charset="ISO-8859-1">')
      print("<p>Speichername:</br><input name='save' type='text' size='30' maxlength='30'></p>")
      print('<input type="submit" value=" Absenden ">')
      print("</form>")
else:
   print('</head>')
   print('<body>')
   print('<h2>Hello Word! This is a test</h2>')
   print('<p>Speichern der aktuellen Konfiguration der Kreuzschiene unter eingegebenen Namen. Name muss mindestens 4 Zeichen enthalten. Es sind nur Buchstaben und Zahlen zulaessig</p>')
   print('<form action="webcross-save.py" method="post" accept-charset="ISO-8859-1">')
   print("<p>Speichername:</br><input name='save' type='text' size='30' maxlength='30'></p>")
   print('<input type="submit" value=" Absenden ">')
   print("</form>")

print('</body>')
print('</html>')
kreuzclient.end()

