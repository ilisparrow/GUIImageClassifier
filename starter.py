#!/usr/bin/env python3
from subprocess import run,PIPE,Popen
import os
import sys
from os.path import expanduser
import datetime
import time


time.sleep(30)#To put back




def launchServer():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    #execute_from_command_line(['manage.py','runserver',str(str(_ipAdress)+':'+str(8000))])
    execute_from_command_line(['manage.py','runserver','0.0.0.0:8000'])




log= open('/home/svision/iboDigital.log', 'a')

log.write("Nex launch :\n" + str(datetime.datetime.now())+"\n")


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


    #out = run(['ifconfig'],shell=False,stdout=PIPE)
    '''    outServer = out.stdout.decode('utf-8')
    ipAdress = ''
    outServerWordList = outServer.split()
    i = 0

    for word in outServerWordList:
        i+=1
        if '192' in word:
            ipAdress = outServerWordList[i]
            break;
    '''
    log.write("\n Launching the server")
    #out = run(['python3', '/home/svision/webInterface/conf/manage.py', 'runserver', ipAdress+':'+str(8000)],shell=True,stdout=PIPE)
    #out = run(str('python3 /home/svision/webInterface/conf/manage.py runserver '+ ipAdress+':'+str(8000)),shell=True,stdout=PIPE)
    #out = run(['/home/svision/webInterface/conf/test.bash'],shell=True,stdout=PIPE)
    launchServer()
    log.write('\n'+str(datetime.datetime.now())+":Server Launched")








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
        log.write("The Ip adress for launching the server  is : "+ ipAdress)
        launchServer(ipAdress)
        log.write('\n'+str(datetime.datetime.now())+":Server Launched")



      
    else:
        #If not, start the hotspot
        out = run(['sudo', 'nmcli', 'dev', 'wifi', 'hotspot', 'ifname', 'wlan0', 'ssid', 'svisionWifi', 'password', '\"ibodigital\"'],shell=False,stdout=PIPE)
        log.write(str(datetime.datetime.now())+': Hotspot created');

        

        #Once the Hotspot is started, we launch the server
        '''
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
        '''
        log.write("Launching the server : ")
        launchServer()
        log.write('\n'+str(datetime.datetime.now())+":Server Launched")


log.close()
