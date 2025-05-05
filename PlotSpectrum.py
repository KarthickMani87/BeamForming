from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
import time

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        w, h = 800, 600
        
        x_axis_min_range = 0
        x_axis_max_range = 6       
        y_axis_min_range = 0
        y_axis_max_range = 100

       
        
        lg0 = QtGui.QLinearGradient(w/2, 0, w/2, h) #(cx, cy, radius, fx, fy)
        lg0.setColorAt(0, pg.mkColor('#ffffff'))
        lg0.setColorAt(0.5, pg.mkColor('#0eeee0'))
        backgroundbrush = QtGui.QBrush(lg0) #qBrush with the gradient

        lg1 = QtGui.QLinearGradient(w/2, 0, w/2, h) #(xstart, ystart, xstop, ystop)
        lg1.setColorAt(0, pg.mkColor('#000000'))
        lg1.setColorAt(1, pg.mkColor('#ffffff'))
        pen = QtGui.QPen(lg1, 0.2) #qPen with this gradient        
        
        pg.setConfigOption('background', backgroundbrush)
        #pg.setConfigOption('foreground', 'k')
        
        self.graphWidget = pg.GraphicsWindow()
        #self.setCentralWidget(self.graphWidget)
        self.graphWidget.resize(1024, 768)


        #QtGui.QApplication.setGraphicsSystem('raster')

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]




        self.AddPlot = self.graphWidget.addPlot(title="Plot 1");
        self.CurvePlot = self.AddPlot.plot(hour, temperature, pen=pen)
        
        self.AddPlot.showGrid(x=True, y=True)


        self.AddPlot.setYRange(y_axis_min_range, y_axis_max_range)


        self.AddPlot.setXRange(x_axis_min_range, x_axis_max_range)        
        
        #while True:        
        #    self.UpdateAxisData();
            #time.sleep(2);
            

    def UpdateAxisData(self):
        hour = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        temperature = [46, 47, 48, 49, 50, 51, 52, 53, 54, 55]    
        #self.CurvePlot.setData(hour, temperature);

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    #main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()