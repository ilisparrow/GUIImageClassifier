from subprocess import run,PIPE,Popen
import sys
from os.path import expanduser
import datetime
import time

time.sleep(30)
file = open('/home/svision/iboDigital.log', 'w')

file.write("It worked!\n" + str(datetime.datetime.now()))


#The first step is to deactive any hot spot

out = run(['nmcli', 'd'],shell=False,stdout=PIPE)#,'|', 'grep', '-o', '\'Ho.*\'','|', 'xargs', '-t', '-n1', 'sudo', 'nmcli', 'connection', 'down'],shell=False,stdout=PIPE)
stringOuput = out.stdout.decode('utf-8')

hotspotName = ''
list_of_words = stringOuput.split()
for word in list_of_words:
    if 'Hotspot' in word:
        hotspotName = word
print(hotspotName)
out = run(['sudo', 'nmcli', 'connection', 'down',hotspotName],shell=False,stdout=PIPE)
#The second step is to check if it is already connected to a wired connection or a wifi
#proc = Popen(['nmcli', 'd', '|', 'grep', '-o', '\'connected*\''])
if "connected" in stringOuput:
    print('Already connected ! Starting server...')
    file.write('already Connected');
    #If so, start the server
    #TODO: Start server

else:
    #If not, start the hotspot
    out = run(['sudo', 'nmcli', 'dev', 'wifi', 'hotspot', 'ifname', 'wlan0', 'ssid', 'svisionWifi', 'password', '\"ibodigital\"'],shell=False,stdout=PIPE)
    file.write('Hotspot created');
    #TODO: Start server
file.close()
