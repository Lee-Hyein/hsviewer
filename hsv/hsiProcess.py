
import pandas as pd 
import numpy as np 
from loguru import logger
import cv2 
from scipy.signal import savgol_filter

csv_df = pd.read_csv('C:/Users/leehy/Documents/workspace/hsviewer/Method-8_beta-coefficient_value.csv')
# csv_df = pd.read_csv('beta-coefficient_value.csv')
# df = pd.DataFrame(csv_df)
# print(df)
models = ['Y1/PC_05 (X-Variables)', 'Y2/PC_06 (X-Variables)', 'Y4/PC_07 (X-Variables)', 
            'Y5/PC_06 (X-Variables)', 'Y8/PC_07 (X-Variables)']

# models = ['Y1/PC_05 (X-Variables)', 'Y2/PC_06 (X-Variables)', 'Y4/PC_06 (X-Variables)', 
#             'Y5/PC_06 (X-Variables)', 'Y6/PC_09 (X-Variables)']

def hsiProcess(hsiImage):
    logger.info("Processing")
    image = hsiImage.asarray()
    print(image.shape)
    result = {}
    snv_data = (image - np.mean(image) / np.std(image))
    X_smooth_1 = savgol_filter(snv_data, 3, polyorder = 1, deriv=1)
    for model in models: 
        modelValues = csv_df[model].to_numpy()
        modelValues = modelValues.astype(float)
        processedValues = np.dot(X_smooth_1, modelValues)
        result[model] = processedValues
    return result

def ndviMaskProcess(hsiImage):
    res = get_ndvi2(hsiImage)
    return res

def get_ndvi2(a): 
    ndvi_image = (a[:,:,89]-a[:,:,60])/(a[:,:,89]+a[:,:,60])
    ret, ndvi_image = cv2.threshold(ndvi_image,0.6, 1, cv2.THRESH_BINARY)
    print(ndvi_image)
    return ndvi_image

# a = cube thr = 0.31 
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
    #print("average ndvi value of ROI is", ave)
    #print("ratio of pixels recognized as plants by NDVI is", thr_count/(len(a[:][0])*len(a[0][:])) )
    return ave, thr_count/(len(a[:][0])*len(a[0][:]))

def snv(hsiImage):
  
    # Define a new array and populate it with the corrected data  
    output_data = np.zeros_like(hsiImage)
    for i in range(hsiImage.shape[0]):
        # Apply correction
        output_data[i,:] = (hsiImage[i,:] - np.mean(hsiImage[i,:])) / np.std(hsiImage[i,:])
 
    return output_data