import torch
from torchvision import datasets, models, transforms
import torch.nn as nn
from torch.utils import data
import time
import os
import cv2
import glob
import numpy as np
import cv2 as cv2
import threading as threading
from PIL import Image




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


class_names =['Good','Bad']
model_ft = models.resnet18(pretrained=True)
num_ftrs = model_ft.fc.in_features
# Here the size of each output sample is set to 2.
# Alternatively, it can be generalized to nn.Linear(num_ftrs, len(class_names)).
model_ft.fc = nn.Linear(num_ftrs, len(class_names))
device = torch.device("cuda")
model_ft = model_ft.to(device)


model_ft.load_state_dict(torch.load('content.model'))
model_ft = model_ft.to(device)
model_ft.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])



    

gstreamer_pipeline(flip_method=0)
video = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
print("vefore capture")
#video = cv2.VideoCapture(0)
avgTime=[]
if video.isOpened():
    i=0
    while i<10000 :
        i+=1
        ret_val,img = video.read()
        #Transforms, then GBR to RGB, to pytorch tensor then to PIL Image 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#Might be unecessary
        img = Image.fromarray(img)
        img_t = transform(img)
        batch_t = torch.unsqueeze(img_t, 0)
        

        seconds = time.time()

        output = model_ft(batch_t.to('cuda'))
        _, preds = torch.max(output, 1)

        avgTime.append(time.time()-seconds)
        print(class_names[preds])
        try : 
            ret, jpeg = cv2.imencode('.jpg', img)
        except:
            pass

print(1/(np.sum(avgTime[1:])/len(avgTime[1:])))









