import sys
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

class WorldSpaceCanvas:
    def __init__(self, dpi):
        self.dpi =  dpi
        my_line_width = self.dpi/(1024*32)
        self.figure = plt.figure(figsize=(4, 4), dpi=int(self.dpi), facecolor=(1,1,1), edgecolor=(0,0,0))
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(aspect="equal", adjustable="box")
        self.axis.axis("equal")
        self.axis.axes.xaxis.set_ticklabels([])
        self.axis.axes.yaxis.set_ticklabels([])
        self.navigation_toolbar = NavigationToolbar(self.canvas, None)

    def loadImage(self, file_path=""):
        tile_img = mpimg.imread("Content\\Tilesets\\PrtCave.png", format='png')
        self.axis.imshow(tile_img)

    def getCanvas(self):
        return self.canvas
    
    def drawTest(self):
        plot = self.axis.scatter(100, 100, label="Label", color="#000000", alpha=0.5, picker=True)
    
    def update(self):
        self.canvas.draw()