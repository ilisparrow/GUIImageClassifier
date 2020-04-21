# -*- coding: utf-8 -*-

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


proc = Popen(['sudo','service','nvargus-daemon','restart'])
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
        return image 

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

    while i<(_time*60*(10/3)*30/4):
        frame = cam.get_jpg()
        cv2.imwrite("./pictures/"+str(_path)+"/"+str(_path)+str(i)+".jpg",frame)
        i+=1
        frameCount+=1
    

def livefeed(request):

    stream = StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    if not (stream == None):
        return stream
    else :
        return HttpResponse('Wainting for device')


def PictureTakerView(request):

    page = PictureTaker(request.POST)
    ls = CatLearning.objects.all()
    context ={"liste":ls}

    context["OutMessage"]=''


    nbInputs=0
    if(request.POST.get('bt_addLearningCats')):
        inputValidBool = False
        try :
            nameCat = request.POST.get('tb_LearningCats') 
            inputValidBool = True
            print("Input valid")
        except:
            pass

        if inputValidBool and not(nameCat == '') :
            ajout = CatLearning(name=nameCat)
            ajout.save()
            request.session["OutMessage"]="Category added."
            request.session["messageColor"]="green"
            print(context["OutMessage"])
            response = redirect('/pictureTaker/')
            return response

        else: 
            request.session["OutMessage"]="Input incorrect"
            request.session["messageColor"]="red"

    if(request.POST.get('bt_livefeed')):
        response = redirect('/livefeed/')
        return response

    if(request.POST.get('bt_delLearningCats')):
        try :
            nameCat = request.POST.get('tb_LearningCats')
            CatLearning.objects.filter(name=nameCat).delete()
        except : 
            Print("Error")#TODO Verifier supp dossier
    if(request.POST.get('bt_setTime')):
        #request.session.flush()
        request.session['time']=request.POST.get('tb_recTime')
        request.session["OutMessage"]="New record time set correctly"
        request.session["messageColor"]="green"


    for item in ls : 
        if(request.POST.get("dynButton")==item.name):
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
            #proc = Popen(['sudo','service','nvargus-daemon','restart'])
            frames(float(request.session.get('time')),item.name,cam)

            request.session["OutMessage"]="Pictures captured"
            request.session["messageColor"]="green"

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
                request.session["OutMessage"]="Category deleted successfully"
                request.session["messageColor"]="green"

                response = redirect('/pictureTaker/')
                return response

            except : 
                Print("Error could not delete category")
                request.session["OutMessage"]="Error Deleting the category"
                request.session["messageColor"]="red"

            
    if('bt_upload' in request.POST):
        proc = Popen(['rm','/home/svision/webInterface/conf/rawData.zip'])
        out = run(['python3','/home/svision/webInterface/conf/step02_upload.py'],shell=False,stdout=PIPE)
        print(out.stdout.decode('utf-8'))
        if "successful" in out.stdout.decode('utf-8') : 

            request.session["OutMessage"]="Upload successful"
            request.session["messageColor"]="green"

            response = redirect('/pictureTaker/')
            return response

        else:

            request.session["OutMessage"]="Upload failed, please try again."
            request.session["messageColor"]="red"


    if(request.POST.get('bt_process')):
        print("Data processing")

        out = run(['python3','/home/svision/webInterface/conf/step00_augmentation.py'],shell=False,stdout=PIPE)
        out = run(['python3','/home/svision/webInterface/conf/step01_resizefolder.py'],shell=False,stdout=PIPE)
        proc = Popen(['zip','rawData.zip','cleaned','-r'])

        request.session["OutMessage"]="Data Processing done, you can upload the files"
        request.session["messageColor"]="green"

        response = redirect('/pictureTaker/')
        return response

    context["OutMessage"]=request.session.get("OutMessage")
    context["messageColor"]=request.session.get("messageColor")
    context["recTime"]=  request.session.get('time')

    return render(request, "pictureTaker.html",context)


def PictureTakerViewSecond(request):
    context ={}
    #ls = CatLearning(request.POST)
    for item in CatLearning.objects.all():
        print(item.name)
    return render(request, "PictureTakerViewSecond.html",context)







