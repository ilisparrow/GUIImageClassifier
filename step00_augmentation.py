from imgaug import augmenters as iaa
import glob 
import os
import imgaug as ia
from skimage import io
from skimage.io import imsave
import random as rd


for root, dirs, files in os.walk(".//pictures", topdown=False):
	for name in dirs:
		#print(name)
		modules = glob.glob(os.path.join(".","pictures",name,"*.jpg"))   
		for imstr in modules:
#			print(imstr)
			rdm=rd.random()
			if rdm >0.9:
				filename = os.path.join(imstr)
				image = io.imread(filename)

				seq = iaa.Sequential([iaa.Sometimes(1,iaa.Cutout(nb_iterations=(1, 7), size=0.1,fill_mode="constant", cval=0)),iaa.Sometimes(0.3,iaa.Crop(percent=(0, 0.2))),iaa.Sometimes(0.7,iaa.GaussianBlur(sigma=(0, 0.1))),iaa.LinearContrast((0.5, 2)),iaa.Sometimes(0.7,iaa.AdditiveGaussianNoise(loc=0, scale=(0.0,0.2*255), per_channel=0.5))], random_order=True) 
				images_aug = seq(image=image)
				imsave(imstr,images_aug)
			else:
				os.remove(imstr)
