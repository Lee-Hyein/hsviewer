
import pandas as pd 
import numpy as np 
from loguru import logger
import cv2 
from scipy.signal import savgol_filter
from util.hsi import getWavelength

df = pd.DataFrame(pd.read_excel('/Users/hyein/Documents/workspace/hsviewer-1/final beta coff202303.xlsx'))

    
def hsiProcess(hsi, hdr_path):
    logger.info("Processing")
    x_smooth = preprocessing(hsi, hdr_path)
    models = df.columns[:6]
    result = {}  # 결과를 저장할 딕셔너리

    if len(getWavelength(hdr_path)) == 51:
        portable_row = df[df.iloc[:, 7].notna()].index
        for model in models:
            coef = df.loc[portable_row, model]
            processed_value = np.dot(x_smooth, coef)
            positive_value = np.clip(processed_value, a_min=0, a_max=None)
            result[model] = (round(np.mean(positive_value), 2),
                             round(np.min(positive_value), 2),
                             round(np.max(positive_value), 2),
                             positive_value)
    elif len(getWavelength(hdr_path)) == 150:
        for model in models:
            coef = df[model]
            processed_value = np.dot(x_smooth, coef)
            positive_value = np.clip(processed_value, a_min=0, a_max=None)
            result[model] = (round(np.mean(positive_value), 2),
                             round(np.min(positive_value), 2),
                             round(np.max(positive_value), 2),
                             positive_value)
    else:
        raise ValueError("Wavelength not recognized")

    return result

def ndviMaskProcess(hsiImage,hdrPath):
    res = get_ndvi2(hsiImage, hdrPath)
    return res

def get_ndvi2(data, path): 
    if len(getWavelength(path))==51:
        ndvi_image = (data[:,:,41]-data[:,:,27])/(data[:,:,41]+data[:,:,27])
        ret, ndvi_image = cv2.threshold(ndvi_image,0.6, 1, cv2.THRESH_BINARY)
    else:
        ndvi_image = (data[:,:,89]-data[:,:,60])/(data[:,:,89]+data[:,:,60])
        ret, ndvi_image = cv2.threshold(ndvi_image,0.6, 1, cv2.THRESH_BINARY)
    print(ndvi_image)
    return ndvi_image


def preprocessing(data, hdr):
    get_plant_region = get_ndvi2(data, hdr)  
    indices = np.argwhere(get_plant_region == 1.)
    zero_arr = np.zeros(data.shape)
    
    for i in range(len(indices)):
        zero_arr[indices[i][0], indices[i][1], :] = data[indices[i][0], indices[i][1], :]

    def SNV_fn(coor):
        snv = (coor - np.mean(coor)) / np.std(coor)
        return snv

    for i in range(len(indices)):
        coor = zero_arr[indices[i][0], indices[i][1], :]
        zero_arr[indices[i][0], indices[i][1], :] = SNV_fn(coor)

    x_smooth = savgol_filter(zero_arr, 3, polyorder=2, deriv=1)
    
    return x_smooth

def normalization(data):
    min_value = data[1]
    max_value = data[2]
    positive_value = data[3]
    
    norm_res = (positive_value - np.min(positive_value))/(np.max(positive_value)-np.min(positive_value))*(max_value-min_value)+min_value

    return norm_res

    
