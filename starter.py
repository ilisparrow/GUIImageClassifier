from subprocess import run,PIPE,Popen
import sys
from os.path import expanduser
import datetime
import time

time.sleep(30)#To put back
log= open('/home/svision/iboDigital.log', 'a')

log.write("It worked!\n" + str(datetime.datetime.now())+"\n")


#The first step is to deactive any hot spot

out = run(['nmcli', 'd'],shell=False,stdout=PIPE)

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
    log.write('already Connected');
    #If so, start the server


    out = run(['ifconfig'],shell=False,stdout=PIPE)
    outServer = out.stdout.decode('utf-8')
    ipAdress = ''
    outServerWordList = outServer.split()
    i = 0

    for word in outServerWordList:
        i+=1
        if 'inet' in word:
            ipAdress = outServerWordList[i]
            break;
    log.write("The Ip adress for launching the server  is :"+ ipAdress)
    out = run(['python3', '/home/svision/webInterface/conf/manage.py', 'runserver', ipAdress+':'+str(8000)],shell=False,stdout=PIPE)
    log.write(str(datetime.datetime.now())+":"+out.stdout.decode('utf-8'))
    print(str(datetime.datetime.now())+":"+out.stdout.decode('utf-8'))








else:

    wifiFileExists = False
    cred = ''

    try:
        f = open("/home/svision/wifi.mdp", "r")
        cred = f.read()
        print(f.read()) 
        wifiFileExists  = True
    except:
        print("wifi file not found")
        log.write(str(datetime.datetime.now())+": Wifi file not found \n")
    

    try :
        list_of_words = cred.split("\n")

        wifiName = list_of_words[0]
        pwd = list_of_words[1]
    except:
        print("Password not found")
        log.write(str(datetime.datetime.now())+": password not found \n")


    out = run(['sudo','nmcli','dev','wifi','connect',wifiName,"password",pwd],shell=False,stdout=PIPE)
    if "successfully" in out.stdout.decode('utf-8') : 
        log.write(str(datetime.datetime.now())+": Not previously connected, but now connected to Internet");

        out = run(['ifconfig'],shell=False,stdout=PIPE)
        outServer = out.stdout.decode('utf-8')
        ipAdress = ''
        outServerWordList = outServer.split()
        i = 0

        for word in outServerWordList:
            i+=1
            if 'inet' in word:
                ipAdress = outServerWordList[i]
                break;
        log.write("The Ip adress for launching the server  is :"+ ipAdress)
        out = run(['python3', '/home/svision/webInterface/conf/manage.py', 'runserver', ipAdress+':'+str(8000)],shell=False,stdout=PIPE)
        log.write(str(datetime.datetime.now())+":"+out.stdout.decode('utf-8'))
        print(str(datetime.datetime.now())+":"+out.stdout.decode('utf-8'))



      
    else:
        #If not, start the hotspot
        out = run(['sudo', 'nmcli', 'dev', 'wifi', 'hotspot', 'ifname', 'wlan0', 'ssid', 'svisionWifi', 'password', '\"ibodigital\"'],shell=False,stdout=PIPE)
        log.write(str(datetime.datetime.now())+': Hotspot created');

        

        #Once the Hotspot is started, we launch the server
        out = run(['ifconfig'],shell=False,stdout=PIPE)
        outServer = out.stdout.decode('utf-8')
        ipAdress = ''
        outServerWordList = outServer.split()
        i = 0

        for word in outServerWordList:
            i+=1
            if 'inet' in word:
                ipAdress = outServerWordList[i]
                break;
        log.write("The Ip adress for launching the server  is :"+ ipAdress)
        out = run(['python3', '/home/svision/webInterface/conf/manage.py', 'runserver', ipAdress+':'+str(8000)],shell=False,stdout=PIPE)
        log.write(str(datetime.datetime.now())+":"+out.stdout.decode('utf-8'))
        print(str(datetime.datetime.now())+":"+out.stdout.decode('utf-8'))


log.close()
