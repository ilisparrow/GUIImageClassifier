# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .models import PictureTaker
from .models import CatLearning
from subprocess import run,PIPE,Popen
from os.path import dirname, basename, isfile, join
import cv2 as cv2
import threading as threading 
from django.views.decorators.http import require_http_methods
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.http import HttpResponse 




def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
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

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


cam = VideoCamera()


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


#@gzip
def livefeed(request):
    #sudo service nvargus-daemon restart#Needs to be executed to be sure to restart the video daemon

    stream = StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    if not (stream == None):
        return stream
    else :
        return HttpResponse('Wainting for device')



# Create your views here.
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

        #TODO 
    if(request.POST.get('bt_delLearningCats')):
        print(request.POST)
        try :
            nameCat = request.POST.get('tb_LearningCats')
            CatLearning.objects.filter(name=nameCat).delete()
        except : 
            Print("Error")
    for item in ls : 
        if(request.POST.get("dynButton")==item.name):
            #TODO inside the dynamic button event
            proc = Popen(['mkdir',"./pictures/"+item.name])
            #try : 
                #os.mkdir((os.path.join("./",item.name)))
            #    os.mkdir((os.path.join("/home","svision","webInterface","conf","pictures",item.name)))
            #except :
            #    print("ERROR: Couldn't create folder")
            #print(proc)
            print(item.name)

    return render(request, "pictureTaker.html",context)


def PictureTakerViewSecond(request):
    context ={}
    #ls = CatLearning(request.POST)
    for item in CatLearning.objects.all():
        print(item.name)
    return render(request, "PictureTakerViewSecond.html",context)





