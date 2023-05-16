from PySide6 import QtWidgets, QtGui, QtCore
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import pyplot as plt
from matplotlib import cm 
import random 
from mpl_toolkits.axes_grid1 import make_axes_locatable

class WidgetPlot(QtWidgets.QWidget):
    def __init__(self, imageData = None, title=None, average=None, min=None, max=None, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.canvas = PlotCanvas(self, width=10, height=8, image=imageData, title=title, average=average, min=min, max=max)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=15, height=10, dpi=100, image=None, title=None, average=None, min=None, max=None):
        fig = plt.Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.image = image
        self.title = title
        self.average = average
        self.min = min
        self.max = max
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, 
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        #data = [random.random() for i in range(250)]
        ax1 = self.figure.add_subplot(1,2,2)
        ax2 = self.figure.add_subplot(1,2,1)
        ax2.axis('off')
        ax2.text(0.05, 0.3, f'average value: {self.average}', horizontalalignment='left', verticalalignment='bottom')
        ax2.text(0.05, 0.25, f'minimum value: {self.min}', horizontalalignment='left', verticalalignment='bottom')
        ax2.text(0.05, 0.2, f'maximum value: {self.max}', horizontalalignment='left', verticalalignment='bottom')
        cor_map = ax1.imshow(self.image, cmap=cm.jet)
        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        self.figure.colorbar(cor_map, cax=cax)
        ax1.set_title(self.title)
        self.draw()
