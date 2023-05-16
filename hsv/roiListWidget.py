from PySide6 import QtWidgets, QtGui, QtCore
import util 

import plotWidget 

class RoiListSingleRectItemWidget(QtWidgets.QWidget): 
    def __init__(self, id, title, average, min, max, parent=None, imageThumbnail=None, imageData=None):
        super(RoiListSingleRectItemWidget, self).__init__(parent)

        self.row = QtWidgets.QVBoxLayout()

        self.setLayout(self.row)

        self.rectItem : QtWidgets.QGraphicsRectItem = None
        self.imageThumbnail = imageThumbnail
        self.imageData = imageData
        self.imageQLabel = QtWidgets.QLabel() 
        self.id = id
        self.title = title 
        self.titleLabel = QtWidgets.QLabel(title)
        self.average = average
        self.min = min
        self.max = max
        self.detailButton = QtWidgets.QPushButton("Detail")

        self.row.addWidget(self.titleLabel,0,)
        self.row.addWidget(self.imageQLabel, 2, QtCore.Qt.AlignHCenter)
        self.row.addWidget(self.detailButton)
        self.plotWidget = None 

        self.row.setSpacing(8)

        if self.imageThumbnail is not None: 
            qImage = util.image.convertCvImage2qImage(imageThumbnail)
            pixmap = QtGui.QPixmap(qImage)
            pixmapHeight = int(self.height() * 5)
            pixmap = pixmap.scaled(pixmapHeight, pixmapHeight,
                                   QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) 
            self.imageQLabel.setPixmap(pixmap)

        self.detailButton.clicked.connect(self.showPlotWidget)
        
    def setTitle(self, title): 
        self.titleLabel.setText(title)
    
    def setAverage(self, average):
        self.average.setText

    def showPlotWidget(self):
        self.plotWidget = plotWidget.WidgetPlot(imageData = self.imageData ,title = self.title, average = self.average, min = self.min, max=self.max)
        self.plotWidget.resize(650, 600)
        self.plotWidget.show()

class RoiListWidget(QtWidgets.QListWidget): 
    pass