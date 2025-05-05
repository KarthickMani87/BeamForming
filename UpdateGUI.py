#matplotlib.use('Qt5Agg')
import sys
import threading
import time

from PyQt5 import QtCore, QtWidgets, QtGui

import pyqtgraph as pg
import multiprocessing

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def update_plot(QuGUIData, AddPlot, CurvePlot):
    print("update_plot")
    
    while True:
    #    QuGUIData.get();
        time.sleep(3)
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        CurvePlot.setData(hour, temperature)
        print("UpdateAgain");
    # Drop off the first y element, append a new one.
    #ydata = ydata[1:] + [random.randint(0, 10)]
    #canvas.axes.cla()  # Clear the canvas.
    #canvas.axes.plot(xdata, ydata, 'ko', 'r')
    # Trigger the canvas to update and redraw.
    #canvas.draw()

def GUIProcess(QuGUIData):

    app = QtWidgets.QApplication(sys.argv)

    w, h = 800, 600;
    
    x_axis_min_range = 0
    x_axis_max_range = 6       
    y_axis_min_range = 0
    y_axis_max_range = 100    
    
    hour = [1,2,3,4,5,6,7,8,9,10]
    temperature = [30,32,34,32,33,31,29,32,35,45]    

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
    
    graphWidget = pg.GraphicsWindow()
    #setCentralWidget(graphWidget)
    graphWidget.resize(1024, 768)



    AddPlot = graphWidget.addPlot(title="Plot 1");
    CurvePlot = AddPlot.plot(hour, temperature, pen=pen)
    
    AddPlot.showGrid(x=True, y=True)


    AddPlot.setYRange(y_axis_min_range, y_axis_max_range)

    AddPlot.setXRange(x_axis_min_range, x_axis_max_range)
    
    GUIThread = threading.Thread(target=update_plot, args=(QuGUIData, AddPlot, CurvePlot, ));
    GUIThread.daemon = True
    GUIThread.start();      

    sys.exit(app.exec_())