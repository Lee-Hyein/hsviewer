import spectral
import pathlib 
import cv2
import numpy as np 
import re

original_band = [42, 28, 6]
portable_band  = [30, 34, 20]

def getWavelength(file_path):
    pattern = r"(?i)wavelength\s*=\s*\{([\s0-9,.]+)\}"
    with open(file_path, "r") as file:
        envi_text = file.read()
    match = re.search(pattern, envi_text, flags=re.DOTALL)
    if match:
        wavelengths = match.group(1)
        wavelengths = [float(x) for x in re.findall(r"[\d.]+", wavelengths)]
        return(wavelengths)
    else:
        raise ValueError("Wavelengths not found in the file")

def loadImage(hdrPath, hsiOrRawPath):
    hsiImage = spectral.io.envi.open(str(hdrPath),
                                     str(hsiOrRawPath))
    if len(getWavelength(hdrPath)) == 51:
        rgbImage = spectral.get_rgb(hsiImage, portable_band)
        rgbImage = (255*rgbImage).astype(np.uint8)
        rgbImage = rgbImage + 60
    else:
        rgbImage = spectral.get_rgb(hsiImage, original_band)
        rgbImage = (255*rgbImage).astype(np.uint8)
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