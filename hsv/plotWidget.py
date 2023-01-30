from PySide6 import QtWidgets, QtGui, QtCore
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import pyplot as plt
from matplotlib import cm 
import random 

class WidgetPlot(QtWidgets.QWidget):
    def __init__(self, imageData = None, title=None, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.canvas = PlotCanvas(self, width=10, height=8, image=imageData, title=title)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100, image=None, title=None):
        fig = plt.Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.image = image
        self.title = title
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, 
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        #data = [random.random() for i in range(250)]
        ax = self.figure.add_subplot(111)
        cor_map = ax.imshow(self.image, cmap=cm.jet)
        self.figure.colorbar(cor_map)
        ax.set_title(self.title)
        self.draw()
