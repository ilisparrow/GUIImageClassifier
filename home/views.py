# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .wifiForm import WifiForm
from subprocess import run,PIPE,Popen
import sys

def homePageView(request):
    
    if request.method =='POST':

        form = WifiForm(request.POST)

        if form.is_valid():
            wifiName=form.cleaned_data['ssid']
            pwd= form.cleaned_data['password']
           # out = run([sys.executable,'/home/pi/webInterface/conf/abc.py'],shell=False,stdout=PIPE)
#            proc = Popen(['sudo','ls'])
            print('---------------')
            out = run(['python3','/home/pi/webInterface/conf/wifiConnector.py',wifiName,pwd],shell=False,stdout=PIPE)
            #proc = Popen(['sudo','cp','/home/pi/webInterface/conf/interfaces','/etc/network'])#TOUNCOMMENT
            #proc = Popen(['sudo', '/etc/init.d/networking','restart'])
            #proc = Popen(['sudo', 'dhclient', 'wlan0'])#TOCHECK
            print('YEAH!!!!!!!')
            
            response = redirect('/pictureTaker/')#Demo
            return response#Demo
    form = WifiForm()
    return render(request,'form.html',{'form':form})
# Create your views here.
