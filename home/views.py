# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .wifiForm import WifiForm
from subprocess import run,PIPE,Popen
import sys

def homePageView(request):
    
    #if request.method =='POST':
    if('bt_skip' in request.POST):
        response = redirect('/pictureTaker/')#Demo
        return response#Demo
    if('bt_reset' in request.POST):

        proc = Popen(['sudo','rm','/home/svision/wifi.mdp'])#Deletes the wifiy
        proc = Popen(['sudo','rm','/home/svision/wevInterface/conf/rawData.zip'])#Deletes the wifiy
        proc = Popen(['sudo','rm','/home/svision/wevInterface/conf/'])#Deletes the wifiy
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
   
            
                response = redirect('/pictureTaker/')#Demo
                return response#Demo
    form = WifiForm()
    return render(request,'form.html',{'form':form})
# Create your views here.
