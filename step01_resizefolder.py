# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 13:02:57 2020

@author: ilias.amri
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

import skimage
from skimage import data
from skimage.color import rgb2hsv
from skimage import io
from skimage.transform import rescale, resize, downscale_local_mean
from os.path import dirname, basename, isfile, join
from skimage.filters import threshold_otsu
from skimage.io import imsave
import glob

#DONE :TH files are read and iterated over 
#TODO :create the folders

resultFolder= glob.glob(join( "res","*.jpg"))
modules = glob.glob(join( "pictures"))
compRatio = int(input("Please input the output size division (2 would mean to divide the legnth and height by 2) : "))
nbrClass = 0
classes = []
try : 
    os.mkdir("cleaned")#To check
except : 
    pass

try :
    os.mkdir(os.path.join("./","cleaned","val"))#To check
except : 
    pass

try : 
    os.mkdir(os.path.join("./","cleaned","train"))#To check
except : 
    pass


for root, dirs, files in os.walk(".//pictures", topdown=False):
   for name in dirs:
#      print(os.path.join(root, name))
      try : 
          os.mkdir((os.path.join("./","cleaned","train",name)))#To check

      except :
          pass
      try : 
          os.mkdir((os.path.join("./","cleaned","val",name)))#To check

      except :
          pass
      classes.append(name)
      nbrClass +=1

      #      os.mkdir("val")#To finish
i = 0
for name in classes:
    modules = glob.glob(os.path.join(root, name,"*.jpg"))   
    counter = 1            
    for imstr in modules:
        filename = os.path.join(imstr)
        image = io.imread(filename)
        image = resize(image, (image.shape[0] // compRatio, image.shape[1] // compRatio),anti_aliasing=True) 

        if (counter<(0.8*len(modules))):      

            print("I will save in ")
            print(os.path.join("./","cleaned","train",name,str(counter)+"aa.jpg"))
            nameFile = os.path.join("./","cleaned","train",name,str(counter)+"aa.jpg")
            imsave(nameFile,image)


        else :

            print("ill save in ")
            print(os.path.join("./","cleaned","val",name,str(counter)+"aa.jpg"))
            nameFile = os.path.join("./","cleaned","val",name,str(counter)+"aa.jpg")
            imsave(nameFile,image)

        counter+=1;
        '''

              nameFile = os.path.join(root,name,str(i)+"aa.jpg")
              
              imsave(nameFile,image)
              i+=1;'''
            
            #RGB part
            