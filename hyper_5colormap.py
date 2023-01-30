import enum
from tkinter import font
#%%
import cv2
import numpy as np 
import spectral.io.envi as envi
from datetime import datetime
import time
from spectral import *
from matplotlib import image
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as matplot
import matplotlib.colors as colors
import matplotlib.cbook as cbook
from matplotlib import cm

img_hsi = envi.open('C:/Users/leehy/Documents/workspace/hyper/13-15/20210915183043001001_00000000_vnir.hdr', 
'C:/Users/leehy/Documents/workspace/hyper/13-15/20210915183043001001_00000000_vnir.hsi')
save_rgb('rgb2.jpg', img_hsi, [65, 36, 14])

img = cv2.imread('./rgb2.jpg')
size=16
x0, y0, w, h = -1,-1,-1,-1 

plt.imshow(img + 75)
plt.show()


#%%
hsi_arr = np.array(img_hsi[0,0,])
row = int(img.shape[0])
column = int(img.shape[1])
#result = []

def caluate_dot(model):
    result = []

    csv_df = pd.read_csv("beta-coefficient_value.csv")
    df = pd.DataFrame(csv_df)
    col_one_arr = df[model].to_numpy()[1:]
    
    for i in range(row):
        for j in range(column):
            hsi_arr = np.array(img_hsi[i,j,])
            dot = np.dot(hsi_arr, col_one_arr.astype(np.float))
            result.append(dot)
    return result


models = ['Y1/PC_05 (X-Variables)', 'Y2/PC_06 (X-Variables)', 'Y4/PC_06 (X-Variables)', 
            'Y5/PC_06 (X-Variables)', 'Y6/PC_09 (X-Variables)']

for idx, model in enumerate(models):
    res_model = caluate_dot(model)
    np_result = np.asarray(res_model)
    trans_result = (np_result.reshape(row, column))
    trans_result = (trans_result - np.min(trans_result))/(np.max(trans_result) - np.min(trans_result))
    cor_map = plt.imshow(trans_result, cmap=cm.jet)
    plt.colorbar(cor_map)
    plt.title(model, fontsize=9)
    plt.show()
