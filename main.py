
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas

import scipy.io
from scipy import signal
import numpy as np

import pandas as pd
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import csv
import os

from fpdf import FPDF
from wfdb.io.record import rdrecord
import wfdb

import modules

class MainWindow(QtWidgets.QMainWindow):

        # Mainwindow constructor
      def __init__(self, *args, **kwargs):
          super(MainWindow, self).__init__(*args, **kwargs)
          uic.loadUi('beta.ui', self)
          self.setWindowIcon(QtGui.QIcon('Images/MainIcon.png'))
          self.setWindowTitle("Realtime-signal-viewer")
          self.xAxis = [0,0,0]
          self.yAxis = [0,0,0]
          self.pointsToAppend = 0
          self.PlotterWindowProp = modules.PlotterWindow()
          self.PauseToggleVar = False
          self.HoldVarH = False
          self.HoldVarV = False
          self.SignalChannelArr = []
          for i in range(3):
               self.SignalChannelArr.append(modules.SignalChannel())
          4
          # params
          self.pushButton_2.clicked.connect(self.browse)
          # 
          self.channel1Signal = pg.PlotCurveItem()
          self.channel1TimeReadings = [0,0]
          self.channel1AmplitudeReadings = [0,0]
          self.channel1PlottedXCoordinates = []
          self.channel1PlottedYCoordinates = []
          self.isChannel1Open, self.isChannel2Open, self.isChannel3Open = False, False, False
          self.isChannel1Shown, self.isChannel2Shown, self.isChannel3Shown = False, False, False
          

      # browse function to open directory : a+m
      def browse(self):
            self.fileName = QFileDialog.getOpenFileName(None,"Open a File","./",filter="Raw Data(*.txt *.csv *.xls *.hea *.dat)" )
            if self.fileName[0]:
                 self.openFile(self.fileName[0])   

      # open the file from directory : a+m
      def openFile(self, path:str):
            timeArr, amplitudeArr = [],[]
            length = len(path)
            fileExtentsion = path[length-3:]
            if fileExtentsion == "csv" or fileExtentsion == "txt" or fileExtentsion == "xls":
               with open(path, 'r') as file:
                csv_data = csv.reader(file, delimiter=',')
                for row in csv_data:
                      timeArr.append(float(row[0]))
                      amplitudeArr.append(float(row[1]))

            self.SignalChannelArr[modules.choosenChannel].time =  timeArr
            self.SignalChannelArr[modules.choosenChannel].amplitude = amplitudeArr
            self.plotSignal()


      # initialize plotting: a+m




      # draw plot: a+m


      # plot state show/hide : a+m
      

      # Zoom in Func  : Mask


      # Zoom out Func : Mask

      # edit the signal color : Mask

      # play / pause func   : ziad
         # dont forget to change the icon 

      # show / hide function  : Mask

      # speed slider function 

      # scroll in x dir

      # scroll in y dir 

      # naming the channel


      # Link 2 channles sim


      # rewind 
      


      # export the report to pdf





def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
