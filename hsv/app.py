import functools
import pathlib

from loguru import logger
from PySide6 import QtCore, QtGui, QtWidgets

from __main__ import *
from hsiView import hsiView
from roiListWidget import RoiListWidget, RoiListSingleRectItemWidget 

from util import hsi, ui, image
#import ai
import hsiProcess

import cv2
import numpy as np 
import matplotlib.pyplot as plt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(
        self,
        qApp, 
        appName, 
        config=None
    ):
        super(MainWindow, self).__init__()
        self.settings = QtCore.QSettings("hyper", "hyper")
        self.appName = appName
        self.qApp = qApp

        self.openedFileDict = {}

        self.initUI() 

        self.hsiView.SingleRectCreated.connect(self.onSingleRectCreated)
        self.hsiView.SingleRectCreated.connect(self.onSingleRectRemoved)
        self.threadpool = QtCore.QThreadPool()

        logger.info(f"Hello, {self.appName}")



    def initUI(self):
        windowSize = self.settings.value("window/size", QtCore.QSize(600, 500))
        windowPosition = self.settings.value("window/position", QtCore.QPoint(0, 0))
        windowState = self.settings.value("window/state", QtCore.QByteArray())
        
        self.resize(windowSize)
        self.move(windowPosition)
        self.restoreState(windowState)

        buildAction = functools.partial(ui.buildAction, self)
        exitAction = buildAction(
            self.tr("&Exit"), 
            self.qApp.quit, 
            None,
            None, 
            self.tr(f"Exit {self.appName}")
        )

        openHSIAction = buildAction(
            self.tr("&Open HSI File"),
            self.openHSI,
            None,
            None,
            self.tr("Open HSI(Hyper Spectral Image)"),
        )

        loadModelAction = buildAction(
            self.tr("&Load Model"), 
            None, 
            None, 
            None, 
            self.tr("Load AI model for Hyper Spectral Image")
        )

        saveAction = buildAction(
            self.tr("&Save Result"), 
            None, 
            None, 
            None, 
            self.tr("Save Result")
        )

        closeHSIAction = buildAction(
            self.tr("&Close HSI File"), 
            self.closeHSI, 
            None, 
            None, 
            self.tr("Load AI model for Hyper Spectral Image")
        )

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&File')

        fileMenu.addAction(openHSIAction)
        fileMenu.addSeparator()
        fileMenu.addAction(closeHSIAction)
        fileMenu.addAction(exitAction)  

        self.statusBar().showMessage('Ready')

        self.hsiView = hsiView(self)
        self.setCentralWidget(self.hsiView)

        self.roiDock = QtWidgets.QDockWidget(self.tr("Processed Image List"), self)
        self.roiDock.setObjectName("RoiList")
        self.roiDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.roiDock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable) 

        self.roiListView = RoiListWidget()
        self.roiDock.setWidget(self.roiListView)
        
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.roiDock)

        self.show()
        self.update()

    def makeRightImage(self, modelName, image, average, min, max, normalize=False):
        item = QtWidgets.QListWidgetItem(self.roiListView)
        self.roiListView.addItem(item)
        imageNormalized1 = cv2.normalize(image, np.zeros_like(image),0,255,cv2.NORM_MINMAX) 
        thumbnail = cv2.applyColorMap(imageNormalized1.astype(np.uint8),cv2.COLORMAP_JET)
        thumbnail = cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB)

        row = RoiListSingleRectItemWidget('', modelName, average, min, max, self.roiListView, thumbnail, image)
        item.setSizeHint(row.minimumSizeHint())
        self.roiListView.setItemWidget(item, row)
        row = self.roiListView.itemWidget(item) 

    def openHSI(self, targetHdrPath: pathlib.Path = None):
        if type(targetHdrPath) is str or type(targetHdrPath) is type(pathlib.Path): 
            targetHdrPath = pathlib.Path(targetHdrPath)
        else: 
            defaultFilePath = pathlib.Path("~/")
            targetHdrPath = pathlib.Path(
                str(
                    QtWidgets.QFileDialog.getOpenFileName(
                        self,
                        self.tr("Open .hdr File"), 
                        str(defaultFilePath), 
                        'HDR files (*.hdr)'
                    )[0]
                )
            )
        
        if targetHdrPath.with_suffix('.raw').exists():
            targetRawOrHsiPath = targetHdrPath.with_suffix('.raw')
        elif targetHdrPath.with_suffix('.hsi').exists(): 
            targetRawOrHsiPath = targetHdrPath.with_suffix('.hsi')
        elif targetHdrPath.with_suffix('.cue').exists(): 
            targetRawOrHsiPath = targetHdrPath.with_suffix('.cue')
        else: 
            QtWidgets.QMessageBox.information(
            self,
            self.tr("Error"), 
            f"No .raw or .hsi or .cue pair for {str(targetHdrPath)}.", 
            QtWidgets.QMessageBox.Ok
            )
            return
        logger.info(f"opening {targetHdrPath.name} & {targetRawOrHsiPath.name}")
        
        hsiImage, rgbImage = hsi.loadImage(targetHdrPath,targetRawOrHsiPath)
        qImage = image.convertCvImage2qImage(rgbImage)
        
        self.hsiView.setImage(QtGui.QPixmap(qImage))

        self.openedFileDict['rawOrHsi'] = targetRawOrHsiPath 
        self.openedFileDict['hdr'] = targetHdrPath 
        self.openedFileDict['rgbArr'] = rgbImage
        self.openedFileDict['hsiArr'] = hsiImage

        wavelength = hsi.getWavelength(self.openedFileDict['hdr'])
        res = hsiProcess.hsiProcess(self.openedFileDict['hsiArr'], self.openedFileDict['hdr']) 
        ndviMask = hsiProcess.ndviMaskProcess(self.openedFileDict['hsiArr'], self.openedFileDict['hdr'])
        for k, v in res.items(): 
            normalizedImage = hsiProcess.normalization(v)
            average = v[0]
            min = v[1]
            max = v[2]
            self.makeRightImage(k ,normalizedImage, average, min, max, True)

        
    def onSingleRectCreated(self, rectItem: QtWidgets.QGraphicsRectItem):
        image = self.openedFileDict['rgbArr']
        x, y, w, h = rectItem.rect().getRect()
        x1 = int(x)
        x2 = int(x + w)
        y1 = int(y)
        y2 = int(y + h) 
        rgbRoi = image[y1:y2, x1:x2,:]
        item = self.addRoiSingleRectItem(rectItem, rgbRoi)

        hsiRoi = self.openedFileDict['hsiArr'][y1:y2, x1:x2]
        worker = ai.AiWorker(hsiRoi, item)
        worker.signal.inferenceFinished.connect(self.onInferenceFinished)
        self.threadpool.start(worker)

    def onInferenceFinished(self, resDict, item: QtWidgets.QListWidgetItem): 
        logger.info(f'Inference result : {resDict}, {item}') 
        row = self.roiListView.itemWidget(item)
        maxKey = max(resDict, key=resDict.get)
        row.setTitle(f" {maxKey} ({resDict[maxKey]:.3f})")


    def addRoiSingleRectItem(self, rectItem, rectImage): 
        item = QtWidgets.QListWidgetItem(self.roiListView)
        self.roiListView.addItem(item)
        row = RoiListSingleRectItemWidget('id', 'Inferencing...',self.roiListView, rectImage)
        item.setSizeHint(row.minimumSizeHint())
        self.roiListView.setItemWidget(item, row)
        return item

    def onSingleRectRemoved(self, item):
        pass 

    def onDragMode(self): 
        self.hsiView.setImageDragMode(True) 
        self.singleRectanglePointerAction.setChecked(False)

    def onSingleRectangleMode(self): 
        if self.hsiView._mode == self.hsiView.MODE_SINGLE_RECT:          
            self.hsiView.setSingleRectangleMode(False)
        else:
            self.hsiView.setSingleRectangleMode(True)

    def closeHSI(self): 
        closingFileName = self.openedFileDict['rawOrHsi'].name
        logger.info(f"closing {closingFileName}")

        self.hsiView.setImage(None)
        
        self.openedFileDict.clear()
        self.roiListView.clear() 

        self.singleRectanglePointerAction.setDisabled(True)
        self.singleRectanglePointerAction.setChecked(False)
        self.normalPointerAction.setDisabled(True)


        #self.singleRectanglePointerAction.
        #QtGui.QAction().setChecked



    def closeEvent(self, event):
        logger.info(f"Exiting {self.appName} Goodbye.")
        self.settings.setValue("window/size", self.size())
        self.settings.setValue("window/position", self.pos())
        self.settings.setValue("window/state", self.saveState())
