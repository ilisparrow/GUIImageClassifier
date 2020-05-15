# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .wifiForm import WifiForm
from .models import Cameras
from subprocess import run,PIPE,Popen
import sys

def homePageView(request):
    #ls = Cameras.objects.all().delete()
    ls = Cameras.objects.all()
    context ={"liste":ls}

    if('bt_camera' in request.POST):
            inputValidBool = False
            try :
                nameCat = request.POST.get('tb_ip') 
                inputValidBool = True
                print("Input valid")
            except:
                pass

            if inputValidBool and not(nameCat == '') :
                ajout = Cameras(name=nameCat)
                ajout.save()
                print(ls)
                response = redirect('/')
                return response

    if('bt_next' in request.POST):
        print("Saving the Ip to a file")
        f= open("ipadresses.save","w+")
        for i in ls:
            f.write(i.name)
            f.write("\n")

        f.close() 
        response = redirect('/setup/')#Demo
        return response#Demo



    #if request.method =='POST':
    if('bt_skip' in request.POST):
        response = redirect('/setup/')#Demo
        return response#Demo

    for item in ls : 

        print("\n")
        print("Remove : "+item.name)
        print("\n")
        print(request.POST)

        if(request.POST.get("bt_goto")=="Go to : "+item.name):
            response = redirect('https://iliasamri.com')#TODO : change with camera's adress, l'adress se trouve ici item.name 
            return response#

        if(item.name in request.POST):
            Cameras.objects.filter(name=item.name).delete()
            response = redirect('/') 
            return response

    if('bt_reset' in request.POST):

        Cameras.objects.all().delete()
        CatLearning.objects.all().delete()

        proc = Popen(['sudo','rm','/home/svision/wifi.mdp'])#Deletes the wifiy
        proc = Popen(['sudo','rm','/home/svision/ipadresses.save'])#Deletes the wifiy
        proc = Popen(['sudo','rm','/home/svision/wevInterface/conf/rawData.zip'])#Deletes the wifiy
        proc = Popen(['sudo','rm','-r','/home/svision/wevInterface/conf/cleaned'])#Deletes the wifiy

        return response#Demo
    if True:
        form = WifiForm(request.POST)

        print("before the if button")

        if('bt_next_wifi' in request.POST):
            #print("juste after the if")
            if form.is_valid():
                wifiName=form.cleaned_data['ssid']
                pwd= form.cleaned_data['password']

                print('-------------------------------------')
                f = open("/home/svision/wifi.mdp", "w")
                f.write(wifiName+"\n"+pwd)
                f.close()

                #open and read the file after the appending:
                #proc = Popen(['sudo','nmcli','dev','wifi','connect',wifiName,"password",pwd])#TODO : SHOW THE USER THE ERROR IF NECESSARY
                proc = Popen(['sudo','reboot','-h','now'])#Reboots the software to connect to wifi
                #print(proc)
   
            
                response = redirect('/setup/')#Demo
                return response#Demo
    form = WifiForm()
    return render(request,'form.html',context)
# Create your views here.
#TODO : CHeck that it's a IP adress in the IP field
#TODO : CHeck that two adresses are not the same