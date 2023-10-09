
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QFile, QTextStream
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
import connector


class MainWindow(QtWidgets.QMainWindow):

        # Mainwindow constructor
      def __init__(self, *args, **kwargs):
          super(MainWindow, self).__init__(*args, **kwargs)
          uic.loadUi('beta.ui', self)
          self.setWindowIcon(QtGui.QIcon('Images/MainIcon.png'))
          self.setWindowTitle("Realtime-signal-viewer")
         # Apply Aqya stylesheet
          self.apply_stylesheet("Aqua.qss")

          self.xAxis = [0,0,0,0,0,0,0,0,0,0]
          self.yAxis = [0,0,0,0,0,0,0,0,0,0]
         # self.PlotterWindowProp = modules.PlotterWindow()
          self.pauseFlag1 = False
          self.pauseFlag2=False
          self.holdHorizontalFlag1 = False
          self.holdVerticalFlag1 = False
          self.cineSpeed = 0
          self.SignalChannelArr = []
          self.SignalChannelArr.append(modules.SignalChannel())
         # for i in range(3):
           #    self.SignalChannelArr.append(modules.SignalChannel())
          # params
          # self.browseBtn1.clicked.connect(self.browse)
          connector.__init__connectors__(self)
          # 
      def apply_stylesheet(self, stylesheet_path):
        # Read the QSS stylesheet from the file
        stylesheet = QFile(stylesheet_path)
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(stylesheet)
            qss = stream.readAll()
            self.setStyleSheet(qss)
        else:
            print(f"Failed to open stylesheet file: {stylesheet_path}")

      # browse function to open directory : a+m
      def browse(self,choosengraph):
            self.fileName = QFileDialog.getOpenFileName(None,"Open a File","./",filter="Raw Data(*.txt *.csv *.xls *.hea *.dat)" )
            if self.fileName[0]:
                 self.openFile(self.fileName[0],choosengraph)   

      # open the file from directory : a+m
      def openFile(self, path:str,choosengraph):
            timeArr, amplitudeArr = [],[]
            length = len(path)
            fileExtentsion = path[length-3:]
            if fileExtentsion == "csv" or fileExtentsion == "txt" or fileExtentsion == "xls":
               with open(path, 'r') as file:
                csv_data = csv.reader(file, delimiter=',')
                for row in csv_data:
                      timeArr.append(float(row[0]))
                      amplitudeArr.append(float(row[1]))
            self.SignalChannelArr[modules.choosenChannel].path = path
            if self.SignalChannelArr[0].path == "null":
                    QtWidgets.QMessageBox.warning(self,"Channel 1 is Empty","Please use channel 1 first")
                    return
            self.SignalChannelArr[modules.choosenChannel].time =  timeArr
            self.SignalChannelArr[modules.choosenChannel].amplitude = amplitudeArr
            self.Legend = choosengraph.addLegend()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
          #   if(choosengraph=="plotGraph1"):
            self.playPauseBtn1.setIcon(icon)
          #   else:
            self.playPauseBtn2.setIcon(icon)

            self.signalInitialization(choosengraph)


      # initialize plotting: a+m
      def signalInitialization(self,choosengraph):
            self.SignalChannelArr[modules.choosenChannel].graph = choosengraph.plot(
                 name="Channel "+str(modules.choosenChannel+1) ,
                 pen={'color': self.SignalChannelArr[modules.choosenChannel].getColor(), 'width': 1}
            )
            choosengraph.showGrid(x= True, y= True)
            maxTime,minTime,maxAmp,minAmp = 0,0,0,0
            for i in range(len(self.SignalChannelArr)):
                 if len(self.SignalChannelArr[i].time):
                      if len(self.SignalChannelArr[i].time )> maxTime:
                            maxTime = len(self.SignalChannelArr[i].time)
                 if len(self.SignalChannelArr[i].time):
                      if len(self.SignalChannelArr[i].time )< minTime:
                            minTime = len(self.SignalChannelArr[i].time)
                 if len(self.SignalChannelArr[i].amplitude):
                      if max(self.SignalChannelArr[i].amplitude ) > maxAmp:
                            maxAmp = max(self.SignalChannelArr[i].amplitude)           

                 if len(self.SignalChannelArr[i].amplitude):
                      if min(self.SignalChannelArr[i].amplitude )< minAmp:
                            minAmp = min(self.SignalChannelArr[i].amplitude)           
                            
            choosengraph.plotItem.setLimits(
             xMin=minTime, xMax=maxTime, yMin=minAmp, yMax=maxAmp     
            )   
            # self.minAmp = minAmp
            # self.maxAmp = maxAmp
            self.minSignalAmp = len(self.SignalChannelArr[modules.choosenChannel].amplitude)
            self.pointsPlotted = 0
            self.startTime = QtCore.QTimer()
            self.startTime.setInterval(200-self.cineSpeed)
            self.startTime.timeout.connect(self.signalPlotting)
            self.startTime.start()
  


      # draw plot: a+m
      def  signalPlotting(self):
           for channelIdx in range(len(self.SignalChannelArr)):
                if self.SignalChannelArr[channelIdx].path !="null":
                     self.xAxis[channelIdx] = self.SignalChannelArr[channelIdx].time[:self.pointsPlotted]
                     self.yAxis[channelIdx] = self.SignalChannelArr[channelIdx].amplitude[:self.pointsPlotted]
           
           self.pointsPlotted += 5
           #if self.minSignalAmp < self.pointsPlotted:
           #     self.startTime.stop()

           for channelIdx in range(len(self.SignalChannelArr)):
                  if self.SignalChannelArr[channelIdx].path != "null":
                       if len(self.SignalChannelArr[channelIdx].time) > self.pointsPlotted:
                              # print(self.SignalChannelArr[channelIdx].getColor())
                               self.SignalChannelArr[channelIdx].graph.setData(self.xAxis[self.getLongestSignal()], self.yAxis[channelIdx], pen=self.SignalChannelArr[channelIdx].getColor(), name=self.SignalChannelArr[channelIdx].label) 

      # plot state show/hide : a+m
      def DynamicSignalUpdate(self, isChangingColor = False):
           for Index in range(len(self.SignalChannelArr)):
               
             # if self.SignalChannelArr[Index].path != "null" and len(self.SignalChannelArr[Index].time) > self.pointsPlotted:
               if self.SignalChannelArr[Index].path != "null" :
                    if self.SignalChannelArr[Index].hiddenFlag == True:
                         self.SignalChannelArr[Index].graph.hide()
                    else:
                         self.SignalChannelArr[Index].graph.show()
                    if len(self.SignalChannelArr[Index].time) > self.pointsPlotted and isChangingColor == False:
                         self.SignalChannelArr[Index].graph.setData(
                              self.xAxis[self.getLongestSignal()], self.yAxis[Index], pen=self.SignalChannelArr[Index].getColor(), name=self.SignalChannelArr[Index].label, skipFiniteCheck=True)
                    elif len(self.SignalChannelArr[Index].time) <= self.pointsPlotted  and isChangingColor == True:
                         self.SignalChannelArr[Index].graph.setData(
                              self.xAxis[Index], self.yAxis[Index], pen=self.SignalChannelArr[Index].getColor(), name=self.SignalChannelArr[Index].label, skipFiniteCheck=True)
                    elif len(self.SignalChannelArr[Index].time) > self.pointsPlotted  and isChangingColor == True:
                         self.SignalChannelArr[Index].graph.setData(
                              self.xAxis[self.getLongestSignal()], self.yAxis[Index], pen=self.SignalChannelArr[Index].getColor(), name=self.SignalChannelArr[Index].label, skipFiniteCheck=True)     

      def getLongestSignal(self):
           ans, index = 0,0
           for channelIndex in range(len(self.SignalChannelArr)):
                if len(self.SignalChannelArr[channelIndex].time) > ans and self.SignalChannelArr[channelIndex].path != "null":
                     index = channelIndex
                     ans = len(self.SignalChannelArr[channelIndex].time)
           return index     
      # Zoom in Func  : Mask
      def zoomSignalIn(self,choosengraph):
          choosengraph.plotItem.getViewBox().scaleBy((0.5, 0.5))
      # Zoom out Func : Mask
      def zoomSignalOut(self,choosengraph):
          choosengraph.plotItem.getViewBox().scaleBy((2, 2))


      # edit the signal color : Mask
      def setSignalChannelColor(self):
           self.SignalChannelArr[modules.choosenChannel].setColor(QColorDialog.getColor().name())
           self.DynamicSignalUpdate(True)
      def addNewChannel(self,choosenChannelList):
            _translate = QtCore.QCoreApplication.translate
           # self.channelList1.setItemText(modules.choosenChannel+1, )
            choosenChannelList.addItem(_translate("MainWindow", "Channel "+str(len(self.SignalChannelArr)+1)))
         #   modules.choosenChannel+=1
            self.SignalChannelArr.append(modules.SignalChannel())



      # play / pause func   : ziad
         # dont forget to change the icon 
      def pauseGraph(self,playpauseButton,graph):
           if graph=="graph1":
               self.pauseFlag1 ^= True
               icon = QtGui.QIcon()
               if self.pauseFlag1 == True :
                     icon.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                     playpauseButton.setIcon(icon)
                     self.startTime.stop()
               else: 
                    icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    playpauseButton.setIcon(icon)
                    self.startTime.start() 
           else:
               self.pauseFlag2 ^= True
               icon = QtGui.QIcon()
               if self.pauseFlag2 == True :
                     icon.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                     playpauseButton.setIcon(icon)
                     self.startTime.stop()
               else: 
                    icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    playpauseButton.setIcon(icon)
                    self.startTime.start() 
                



      # rewind 
      def rewindSignal(self,choosengraph):
          # print("ana morad",self.SignalChannelArr[modules.choosenChannel].path)
           choosengraph.clear()
          # print("ana ashf",self.SignalChannelArr[modules.choosenChannel].path)
          # icon = QtGui.QIcon()
           #icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
           #self.playPauseBtn1.setIcon(icon)
           for i in range(len(self.SignalChannelArr)):
                modules.choosenChannel = i
            #    print(self.SignalChannelArr[modules.choosenChannel].path,"iter:",i)
                self.signalInitialization()
  
      
      # show / hide function  : Mask
      def hideSignal(self,checked):
             self.SignalChannelArr[modules.choosenChannel].hiddenFlag = checked
             self.DynamicSignalUpdate(False)
      # speed slider function 

      def speedSlider(self):
           
           self.cineSpeed= self.horizontalSlider.value()
           self.startTime.setInterval(200-self.cineSpeed)

      # scroll in x dir
      def xScrollMove(self):
           val = self.xAxisScrollBar1.value()
           xmax = np.ceil(self.data[0][-1+self.vsize-self.psize+val])-1
           xmin = xmax-self.vsize
           self.plot_widget.setXRange(xmin, xmax)
     
      # scroll in y dir 
      def yScrollMove(self):
           pass
      # naming the channel
      def editChannelName(self,name):
             # self.SignalChannelArr[modules.choosenChannel].label = name
             # self.Legend.getLabel(self.SignalChannelArr[modules.choosenChannel].graph).setText(name)
               channel_index = modules.choosenChannel
               self.SignalChannelArr[channel_index].label = name
               if self.SignalChannelArr[channel_index].path !="null":
                    self.Legend.removeItem(self.SignalChannelArr[channel_index].graph)
                    self.Legend.addItem(self.SignalChannelArr[channel_index].graph, name)


      # Link 2 channles sim



      # export the report to pdf





def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
