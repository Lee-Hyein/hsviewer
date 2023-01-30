from PySide6 import QtGui
import numpy as np 

def convertCvImage2qImage(image):
    height, width = image.shape[0], image.shape[1] 
    channel = image.shape[2] if len(image.shape) == 3 else 1 
    image = np.ascontiguousarray(image)
    qImage = QtGui.QImage(image.data, width, height, width * channel,
                            QtGui.QImage.Format_RGB888)
    return qImage
