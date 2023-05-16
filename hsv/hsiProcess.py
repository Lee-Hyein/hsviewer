
import pandas as pd 
import numpy as np 
from loguru import logger
import cv2 
from scipy.signal import savgol_filter
from util.hsi import getWavelength

df = pd.DataFrame(pd.read_excel('/Users/hyein/Documents/workspace/hsviewer-1/final beta coff202303.xlsx'))


# def hsiProcess(hsi, hdr_path):
#     logger.info("Processing")
#     x_smooth = preprocessing(hsi, hdr_path)
#     models = df.columns[:6]
#     positive_value = None  # 변수 초기화
#     if len(getWavelength(hdr_path)) == 51:
#         portable_row = df[df.iloc[:, 7].notna()].index
#         for model in models:
#             coef = df.loc[portable_row, model]
#             processed_value = np.dot(x_smooth, coef)
#             positive_value = np.clip(processed_value, a_min=0, a_max=None)
#     elif len(getWavelength(hdr_path)) == 150:
#         for model in models:
#             coef = df[model]
#             processed_value = np.dot(x_smooth, coef)
#             positive_value = np.clip(processed_value, a_min=0, a_max=None)
    
#     if positive_value is not None:
#         average_value = round(np.mean(positive_value), 2)
#         min_value = round(np.min(positive_value), 2)
#         max_value = round(np.max(positive_value), 2)
#         return average_value, min_value, max_value, positive_value
#     else:
#         raise ValueError("Wavelength not recognized")
    
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



# def hsiProcess(hsiImage):
#     logger.info("Processing")
#     image = hsiImage.asarray()
#     print(image.shape)
#     result = {}
#     snv_data = (image - np.mean(image) / np.std(image))
#     X_smooth_1 = savgol_filter(snv_data, 3, polyorder = 1, deriv=1)
#     for model in models: 
#         modelValues = csv_df[model].to_numpy()
#         modelValues = modelValues.astype(float)
#         processedValues = np.dot(X_smooth_1, modelValues)
#         result[models[model]] = processedValues
#     return result

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

# a = cube thr = 0.31 
# def ave_ndvi(a,thr):
#     ndvi_arr=np.zeros(len(a[:][0])*len(a[0][:]))
#     aa=a.reshape((len(a[:][0])*len(a[0][:]),a.shape[2]))
#     thr_count=0
    
#     for i in range((len(a[:][0])*len(a[0][:]))):
#         ndvi_arr[i]=get_ndvi2(aa[i])
#         if ndvi_arr[i] > thr:
#             thr_count=thr_count+1
        
#     #hr_ratio=thr_count/(len(a[:][0])*len(a[0][:])
#     ave=np.mean(ndvi_arr)
#     #print("average ndvi value of ROI is", ave)
#     #print("ratio of pixels recognized as plants by NDVI is", thr_count/(len(a[:][0])*len(a[0][:])) )
#     return ave, thr_count/(len(a[:][0])*len(a[0][:]))
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
    # Define a new array and populate it with the corrected data  
    # output_data = np.zeros_like(hsiImage)
    # for i in range(hsiImage.shape[0]):
    #     # Apply correction
    #     output_data[i,:] = (hsiImage[i,:] - np.mean(hsiImage[i,:])) / np.std(hsiImage[i,:])
 
    # return output_data

# def normalization(ndvi_mask, data):
#     min_value = hsiProcess(data[1])
#     max_value = hsiProcess(data[2])
#     positive_value = hsiProcess(data[3])
    
#     norm = cv2.normalize(positive_value, np.zeros_like(positive_value),0,255,cv2.NORM_MINMAX)
#     norm2 = cv2.normalize(norm, np.zeros_like(norm), 0,1, cv2.NORM_MINMAX)
#     maskedimg = cv2.bitwise_and(norm2, norm2, mask=ndvi_mask.astype(np.uint8))
#     norm_res = (positive_value - np.min(positive_value))/(np.max(positive_value)-np.min(positive_value))*(max_value-min_value)+min_value
def normalization(data):
    #results = hsiProcess(data, hdr)
    
    
    min_value = data[1]
    max_value = data[2]
    positive_value = data[3]
    
    # norm = cv2.normalize(positive_value, np.zeros_like(positive_value), 0, 255, cv2.NORM_MINMAX)
    # norm2 = cv2.normalize(norm, np.zeros_like(norm), 0, 1, cv2.NORM_MINMAX)
    # maskedimg = cv2.bitwise_and(norm2, norm2, mask=ndvi_mask.astype(np.uint8))
    norm_res = (positive_value - np.min(positive_value))/(np.max(positive_value)-np.min(positive_value))*(max_value-min_value)+min_value

    return norm_res

    
