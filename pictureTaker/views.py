# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .models import PictureTaker
from .models import CatLearning
from .models import State
from subprocess import run,PIPE,Popen
from os.path import dirname, basename, isfile, join
import cv2 as cv2
import threading as threading 
from django.views.decorators.http import require_http_methods
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.http import HttpResponse 
import math



def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_jpg(self):
        image = self.frame
        ret, jpg = cv2.imencode('.jpg', image)
        return image#Was jpg 

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


cam = VideoCamera()
global frameCount
frameCount =0

def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def frames(_time,_path,_camera):
    i=0
    frameCount=0
    if _time > 5:
        _time=5
 #   elif _time<1:
 #       _time=1

    while i<(_time*60*30/4):
        frame = cam.get_jpg()
        cv2.imwrite("./pictures/"+str(_path)+"/"+str(_path)+str(i)+".jpg",frame)
        i+=1
        frameCount+=1
    

def livefeed(request):
    #sudo service nvargus-daemon restart#TODO Needs to be executed to be sure to restart the video daemon

    proc = Popen(['sudo','service','nvargus-daemon','restart'])
    stream = StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    if not (stream == None):
        return stream
    else :
        return HttpResponse('Wainting for device')



def PictureTakerView(request):

    page = PictureTaker(request.POST)
    ls = CatLearning.objects.all()
    context ={"liste":ls}
    

    nbInputs=0
    if(request.POST.get('bt_addLearningCats')):
        inputValidBool = False
        try :
            nameCat = request.POST.get('tb_LearningCats') 
            inputValidBool = True
            print("Input valid")
        except:
            print("Input excpected")

        if inputValidBool and not(nameCat == '') :
            ajout = CatLearning(name=nameCat)
            ajout.save()
            response = redirect('/pictureTaker/')
            return response

    if(request.POST.get('bt_livefeed')):
        response = redirect('/livefeed/')
        return response
    if(request.POST.get('bt_delLearningCats')):
        try :
            nameCat = request.POST.get('tb_LearningCats')
            CatLearning.objects.filter(name=nameCat).delete()
        except : 
            Print("Error")
    if(request.POST.get('bt_setTime')):
        request.session.flush()
        request.session['time']=request.POST.get('tb_recTime')


    for item in ls : 
        if(request.POST.get("dynButton")==item.name):
            #TODO Inside the dyn btn, Todo  : ADD fodler and record
            CatLearning.objects.filter(name=item.name)

            try:
                proc = Popen(['rm','./pictures/'+str(item.name),'-r'])
                print('folder removed')
            except:
                print("Nothing to remove")


            try : 
                proc = Popen(['mkdir','./pictures/'+str(item.name)])
            except:
                pass
            #takes a picture and saves it
            proc = Popen(['sudo','service','nvargus-daemon','restart'])
            frames(float(request.session.get('time')),item.name,VideoCamera())


            response = redirect('/pictureTaker/')
            return response
#Event when clicked on Delete
        if(request.POST.get(item.name)):
            try:
                proc = Popen(['rm','./pictures/'+str(item.name),'-r'])
                print('folder removed')
            except:
                print("Nothing to remove")


            try :
                CatLearning.objects.filter(name=item.name).delete()
                response = redirect('/pictureTaker/')
                return response

            except : 
                Print("Error could not delete category")
            
    if('bt_upload' in request.POST):
        out = run(['python3','/home/svision/webInterface/conf/upload.py'],shell=False,stdout=PIPE)
    if(request.POST.get('bt_process')):
        print("PROCESSING")
        out = run(['python3','/home/svision/webInterface/conf/step00_augmentation.py'],shell=False,stdout=PIPE)

        out = run(['python3','/home/svision/webInterface/conf/step01_resizefolder.py'],shell=False,stdout=PIPE)
        proc = Popen(['zip','rawData.zip','cleaned','-r'])
        print("DONE")
        #TODO redirect to new page
    #context["frames"] =frameCount/int(math.floor(float(request.session.get('time')*60*30))) 
    context["recTime"]=  request.session.get('time')
    return render(request, "pictureTaker.html",context)


def PictureTakerViewSecond(request):
    context ={}
    #ls = CatLearning(request.POST)
    for item in CatLearning.objects.all():
        print(item.name)
    return render(request, "PictureTakerViewSecond.html",context)







