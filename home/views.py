# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .wifiForm import WifiForm
from subprocess import run,PIPE,Popen
import sys

def homePageView(request):
    
    #if request.method =='POST':
    if True:
        form = WifiForm(request.POST)

        print("before the if button")

        if('bt_next_wifi' in request.POST):
            #print("juste after the if")
            if form.is_valid():
                wifiName=form.cleaned_data['ssid']
                pwd= form.cleaned_data['password']

                print('-------------------------------------')
 #               proc = Popen (['nmcli', 'd','|', 'grep', '-o', '\'Ho.*\'','|', 'xargs', '-t', '-n1', 'sudo', 'nmcli', 'connection', 'down'])
 #maybe write the IDs to a file so that the server can shutdown
                proc = Popen(['sudo','nmcli','dev','wifi','connect',wifiName,"password",pwd])#TODO : SHOW THE USER THE ERROR IF NECESSARY
                print(proc)
   
            
                response = redirect('/pictureTaker/')#Demo
                return response#Demo
    form = WifiForm()
    return render(request,'form.html',{'form':form})
# Create your views here.
