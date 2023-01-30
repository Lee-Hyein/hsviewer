import spectral
import pathlib 
import cv2
import numpy as np 

band = [42, 28, 6]

def loadImage(hdrPath, hsiOrRawPath):
    hsiImage = spectral.io.envi.open(str(hdrPath),
                                     str(hsiOrRawPath))
    rgbImage = spectral.get_rgb(hsiImage, band)

    rgbImage = (255*rgbImage).astype(np.uint8)
    # brightness 
    rgbImage = rgbImage + 30 
    #rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
    return (hsiImage, rgbImage)

def get_ndvi2(a):
    ndvi=(a[89]-a[60])/(a[89]+a[60])
    return ndvi

def ave_ndvi(a,thr):
    ndvi_arr=np.zeros(len(a[:][0])*len(a[0][:]))
    aa=a.reshape((len(a[:][0])*len(a[0][:]),a.shape[2]))
    thr_count=0
    for i in range((len(a[:][0])*len(a[0][:]))):
        ndvi_arr[i]=get_ndvi2(aa[i])
        if ndvi_arr[i] > thr:
            thr_count=thr_count+1  
    #hr_ratio=thr_count/(len(a[:][0])*len(a[0][:])
    ave=np.mean(ndvi_arr)
    return ave, thr_count/(len(a[:][0])*len(a[0][:]))