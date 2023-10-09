
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

          self.xAxis1 = [0]
          self.yAxis1 = [0]
          self.xAxis2 = [0]
          self.yAxis2 = [0]
         # self.PlotterWindowProp = modules.PlotterWindow()
          self.pauseFlag1 = False
          self.pauseFlag2 = False
          self.holdHorizontalFlag1 = False
          self.holdVerticalFlag1 = False
          self.cineSpeed1 = 0
          self.cineSpeed2 = 0
          self.SignalChannelArr = []
          tmpList = [modules.SignalChannel()]
          self.SignalChannelArr.append(tmpList)
          tmpList = [modules.SignalChannel()]
          self.SignalChannelArr.append(tmpList)
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
      def browse(self,choosenGraph,choosenGraphIndex):
            self.fileName = QFileDialog.getOpenFileName(None,"Open a File","./",filter="Raw Data(*.txt *.csv *.xls *.hea *.dat)" )
            if self.fileName[0]:
                 self.openFile(self.fileName[0],choosenGraph,choosenGraphIndex)   

      # open the file from directory : a+m
      def openFile(self, path:str,choosenGraph, choosenGraphIndex):
            timeArr, amplitudeArr = [],[]
            length = len(path)
            fileExtentsion = path[length-3:]
            if fileExtentsion == "csv" or fileExtentsion == "txt" or fileExtentsion == "xls":
               with open(path, 'r') as file:
                csv_data = csv.reader(file, delimiter=',')
                for row in csv_data:
                      timeArr.append(float(row[0]))
                      amplitudeArr.append(float(row[1]))

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)     

            if choosenGraphIndex == 0:
                       self.SignalChannelArr[0][modules.choosenChannelGraph1].path = path
                       if self.SignalChannelArr[0][0].path == "null":
                              QtWidgets.QMessageBox.warning(self,"Channel 1 in Graph 1 is Empty","Please use channel 1 first")
                              return
                       self.SignalChannelArr[0][modules.choosenChannelGraph1].time =  timeArr
                       self.SignalChannelArr[0][modules.choosenChannelGraph1].amplitude = amplitudeArr
                       self.Legend1 = choosenGraph.addLegend()
                       self.playPauseBtn1.setIcon(icon)

            elif choosenGraphIndex == 1:
                       self.SignalChannelArr[1][modules.choosenChannelGraph2].path = path
                       if self.SignalChannelArr[1][0].path == "null":
                              QtWidgets.QMessageBox.warning(self,"Channel 1 in Graph 2 is Empty","Please use channel 1 first")
                              return
                       self.SignalChannelArr[1][modules.choosenChannelGraph2].time =  timeArr
                       self.SignalChannelArr[1][modules.choosenChannelGraph2].amplitude = amplitudeArr
                       self.Legend2 = choosenGraph.addLegend()
                       self.playPauseBtn2.setIcon(icon)

            self.signalInitialization(choosenGraph,choosenGraphIndex,False)


      # initialize plotting: a+m
      def signalInitialization(self,choosenGraph,choosenGraphIndex,isRewinding):
            selectedChannelIndex = 0
            if choosenGraphIndex == 0:
                 selectedChannelIndex = modules.choosenChannelGraph1
            elif choosenGraphIndex == 1:
                      selectedChannelIndex = modules.choosenChannelGraph2
            if isRewinding == False:           
               self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].graph = choosenGraph.plot(
                    name="Channel "+str(selectedChannelIndex+1) ,
                    pen={'color': self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].getColor(), 'width': 1}
               )
            else:
                 for channelIndex in range(len(self.SignalChannelArr[choosenGraphIndex])):
                      if self.SignalChannelArr[choosenGraphIndex][channelIndex].path !="null":     
                              self.SignalChannelArr[choosenGraphIndex][channelIndex].graph = choosenGraph.plot(
                         name="Channel "+str(channelIndex+1) ,
                         pen={'color': self.SignalChannelArr[choosenGraphIndex][channelIndex].getColor(), 'width': 1}
                    )
            choosenGraph.showGrid(x= True, y= True)
            maxTime,minTime,maxAmp,minAmp = 0,0,0,0
            for i in range(len(self.SignalChannelArr[choosenGraphIndex])):
                 if len(self.SignalChannelArr[choosenGraphIndex][i].time):
                      if len(self.SignalChannelArr[choosenGraphIndex][i].time )> maxTime:
                            maxTime = len(self.SignalChannelArr[choosenGraphIndex][i].time)
                 if len(self.SignalChannelArr[choosenGraphIndex][i].time):
                      if len(self.SignalChannelArr[choosenGraphIndex][i].time )< minTime:
                            minTime = len(self.SignalChannelArr[choosenGraphIndex][i].time)
                 if len(self.SignalChannelArr[choosenGraphIndex][i].amplitude):
                      if max(self.SignalChannelArr[choosenGraphIndex][i].amplitude ) > maxAmp:
                            maxAmp = max(self.SignalChannelArr[choosenGraphIndex][i].amplitude)           

                 if len(self.SignalChannelArr[choosenGraphIndex][i].amplitude):
                      if min(self.SignalChannelArr[choosenGraphIndex][i].amplitude ) < minAmp:
                            minAmp = min(self.SignalChannelArr[choosenGraphIndex][i].amplitude)           
                            
            choosenGraph.plotItem.setLimits(
             xMin=minTime, xMax=maxTime, yMin=minAmp, yMax=maxAmp     
            )   
            # self.minAmp = minAmp
            # self.maxAmp = maxAmp
            self.pauseFlag1 = False
            self.pauseFlag2 = False

            if choosenGraphIndex == 0:
                   self.minSignalAmp1 = len(self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].amplitude)
                   self.pointsPlotted1 = 0
                   self.startTime1 = QtCore.QTimer()
                   self.startTime1.setInterval(200-self.cineSpeed1)
                   self.startTime1.timeout.connect(lambda:self.signalPlotting(choosenGraph,choosenGraphIndex))
                   self.startTime1.start()
            if choosenGraphIndex == 1:
                   self.minSignalAmp2 = len(self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].amplitude)    
                   self.pointsPlotted2 = 0
                   self.startTime2 = QtCore.QTimer()
                   self.startTime2.setInterval(200-self.cineSpeed2)
                   self.startTime2.timeout.connect(lambda:self.signalPlotting(choosenGraph,choosenGraphIndex))
                   self.startTime2.start()
         #   self.pointsPlotted = 0
        #    self.startTime = QtCore.QTimer()
           # self.startTime.setInterval(200-self.cineSpeed)
         #   self.startTime.timeout.connect(self.signalPlotting)
         #   self.startTime.start()
  


      # draw plot: a+m
      def  signalPlotting(self,choosenGraph,choosenGraphIndex):
           for channelIdx in range(len(self.SignalChannelArr[choosenGraphIndex])):
                if self.SignalChannelArr[choosenGraphIndex][channelIdx].path !="null":
                     if choosenGraphIndex == 0:
                           self.xAxis1[channelIdx] = self.SignalChannelArr[choosenGraphIndex][channelIdx].time[:self.pointsPlotted1]
                           self.yAxis1[channelIdx] = self.SignalChannelArr[choosenGraphIndex][channelIdx].amplitude[:self.pointsPlotted1]

                     elif choosenGraphIndex == 1:
                         self.xAxis2[channelIdx] = self.SignalChannelArr[choosenGraphIndex][channelIdx].time[:self.pointsPlotted2]
                         self.yAxis2[channelIdx] = self.SignalChannelArr[choosenGraphIndex][channelIdx].amplitude[:self.pointsPlotted2]
           
           if choosenGraphIndex == 0:
                self.pointsPlotted1 += 5
           elif choosenGraphIndex == 1:
                self.pointsPlotted2 += 5
           #if self.minSignalAmp < self.pointsPlotted:
           #     self.startTime.stop()

           for channelIdx in range(len(self.SignalChannelArr[choosenGraphIndex])):
                  if self.SignalChannelArr[choosenGraphIndex][channelIdx].path != "null":
                       if choosenGraphIndex == 0:
                              if len(self.SignalChannelArr[choosenGraphIndex][channelIdx].time) > self.pointsPlotted1:
                              # print(self.SignalChannelArr[channelIdx].getColor())
                                    self.SignalChannelArr[choosenGraphIndex][channelIdx].graph.setData(self.xAxis1[channelIdx], self.yAxis1[channelIdx], pen=self.SignalChannelArr[choosenGraphIndex][channelIdx].getColor(), name=self.SignalChannelArr[choosenGraphIndex][channelIdx].label) 

                       elif choosenGraphIndex == 1:
                               if len(self.SignalChannelArr[choosenGraphIndex][channelIdx].time) > self.pointsPlotted2:
                              # print(self.SignalChannelArr[channelIdx].getColor())
                                    self.SignalChannelArr[choosenGraphIndex][channelIdx].graph.setData(self.xAxis2[channelIdx], self.yAxis2[channelIdx], pen=self.SignalChannelArr[choosenGraphIndex][channelIdx].getColor(), name=self.SignalChannelArr[choosenGraphIndex][channelIdx].label)   
                      

      # plot state show/hide : a+m
      def DynamicSignalUpdate(self, choosenGraphIndex, selectedChannelIndex,  isChangingColor = False):
           for Index in range(len(self.SignalChannelArr[choosenGraphIndex])):
               
             # if self.SignalChannelArr[Index].path != "null" and len(self.SignalChannelArr[Index].time) > self.pointsPlotted:
               if self.SignalChannelArr[choosenGraphIndex][Index].path != "null" :
                    if self.SignalChannelArr[choosenGraphIndex][Index].hiddenFlag == True:
                         self.SignalChannelArr[choosenGraphIndex][Index].graph.hide()
                    else:
                         self.SignalChannelArr[choosenGraphIndex][Index].graph.show()
                   ######################################################################
                    if choosenGraphIndex == 0:
                          currentpointsPlotted = self.pointsPlotted1
                          currentXAxis = self.xAxis1
                          currentYAxis = self.yAxis1 
                    elif choosenGraphIndex == 1:
                          currentpointsPlotted = self.pointsPlotted2
                          currentXAxis = self.xAxis2
                          currentYAxis = self.yAxis2 
                   ##################################################       
                    if len(self.SignalChannelArr[choosenGraphIndex][Index].time) > currentpointsPlotted and isChangingColor == False:
                         self.SignalChannelArr[choosenGraphIndex][Index].graph.setData(
                              currentXAxis[Index], currentYAxis[Index], pen=self.SignalChannelArr[choosenGraphIndex][Index].getColor(), name=self.SignalChannelArr[choosenGraphIndex][Index].label, skipFiniteCheck=True)
                    elif len(self.SignalChannelArr[choosenGraphIndex][Index].time) <= currentpointsPlotted  and isChangingColor == True:
                         self.SignalChannelArr[choosenGraphIndex][Index].graph.setData(
                              currentXAxis[Index], currentYAxis[Index], pen=self.SignalChannelArr[choosenGraphIndex][Index].getColor(), name=self.SignalChannelArr[choosenGraphIndex][Index].label, skipFiniteCheck=True)
                    elif len(self.SignalChannelArr[choosenGraphIndex][Index].time) > currentpointsPlotted  and isChangingColor == True:
                         self.SignalChannelArr[choosenGraphIndex][Index].graph.setData(
                              currentXAxis[Index], currentYAxis[Index], pen=self.SignalChannelArr[choosenGraphIndex][Index].getColor(), name=self.SignalChannelArr[choosenGraphIndex][Index].label, skipFiniteCheck=True)     

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


      # edit the signal color : done
      def setSignalChannelColor(self,choosenGraphIndex):
           selectedChannelIndex = 0
           if choosenGraphIndex == 0:
                 selectedChannelIndex = modules.choosenChannelGraph1
           elif choosenGraphIndex == 1:
                      selectedChannelIndex = modules.choosenChannelGraph2
           self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].setColor(QColorDialog.getColor().name())
           self.DynamicSignalUpdate(choosenGraphIndex,selectedChannelIndex,True)

      def addNewChannel(self,choosenChannelList,choosenGraphIndex):
            _translate = QtCore.QCoreApplication.translate
           # self.channelList1.setItemText(modules.choosenChannel+1, )
            choosenChannelList.addItem(_translate("MainWindow", "Channel "+str(len(self.SignalChannelArr[choosenGraphIndex])+1)))
         #   modules.choosenChannel+=1
            if choosenGraphIndex == 0:
                  self.xAxis1.append(0)
                  self.yAxis1.append(0)
            elif choosenGraphIndex == 1:
                  self.xAxis2.append(0)
                  self.yAxis2.append(0)   
            self.SignalChannelArr[choosenGraphIndex].append(modules.SignalChannel())



      # play / pause func   : ziad
         # dont forget to change the icon 
      def pauseGraph(self,playpauseButton,choosenGraphIndex):
           icon = QtGui.QIcon()
           if choosenGraphIndex == 0:
               self.pauseFlag1 ^= True
               if self.pauseFlag1 == True :
                     icon.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                     playpauseButton.setIcon(icon)
                     self.startTime1.stop()
               else: 
                    icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    playpauseButton.setIcon(icon)
                    self.startTime1.start() 
           elif choosenGraphIndex == 1:
               self.pauseFlag2 ^= True
               if self.pauseFlag2 == True :
                     icon.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                     playpauseButton.setIcon(icon)
                     self.startTime2.stop()
               else: 
                    icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    playpauseButton.setIcon(icon)
                    self.startTime2.start() 
                



      # rewind 
      def rewindSignal(self,choosengraph,choosenGraphIndex):
             selectedChannelIndex = 0
             icon = QtGui.QIcon()
             if choosenGraphIndex == 0:
                      selectedChannelIndex = modules.choosenChannelGraph1
                      icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                      self.playPauseBtn1.setIcon(icon)
                    #  self.startTime1.stop()
             elif choosenGraphIndex == 1:
                      selectedChannelIndex = modules.choosenChannelGraph2
                      icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                      self.playPauseBtn2.setIcon(icon)
                    #  self.startTime2.stop()
             choosengraph.clear()
             #for channelIndex in range(len(self.SignalChannelArr[choosengraph])):
             self.signalInitialization(choosengraph,choosenGraphIndex,True)
             

  
      
      # show / hide function  : Mask
      def hideSignal(self,checked,choosenGraphIndex):
             selectedChannelIndex = 0
             if choosenGraphIndex == 0:
                 selectedChannelIndex = modules.choosenChannelGraph1
             elif choosenGraphIndex == 1:
                      selectedChannelIndex = modules.choosenChannelGraph2
             self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].hiddenFlag = checked
             self.DynamicSignalUpdate(choosenGraphIndex,selectedChannelIndex,False)
      # speed slider function 

      def speedSlider(self,choosenGraphIndex):
           if choosenGraphIndex == 0:           
               self.cineSpeed1= self.horizontalSlider.value()
               self.startTime1.setInterval(200-self.cineSpeed1)
           else: 
               self.cineSpeed2 = self.speedSlider2.value()
               self.startTime2.setInterval(200-self.cineSpeed2)    

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



      def editChannelName(self,label,choosenGraphIndex):
             # self.SignalChannelArr[modules.choosenChannel].label = name
             # self.Legend.getLabel(self.SignalChannelArr[modules.choosenChannel].graph).setText(name)
               selectedChannelIndex = 0
               if choosenGraphIndex == 0:
                      selectedChannelIndex = modules.choosenChannelGraph1
                      if self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].path == "null":
                              QtWidgets.QMessageBox.warning(self,"Operation Failed","You can't edit channel name before browsing a file, browse a file first")
                              return
                      currentLegend = self.Legend1
               elif choosenGraphIndex == 1:
                      selectedChannelIndex = modules.choosenChannelGraph2
                      if self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].path == "null":
                              QtWidgets.QMessageBox.warning(self,"Operation Failed","You can't edit channel name before browsing a file, browse a file first")
                              return
                      currentLegend = self.Legend2

               self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].label = label
               if self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].path !="null":
                    currentLegend.removeItem(self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].graph)
                    currentLegend.addItem(self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].graph, label)


      # Link 2 channles sim



      # export the report to pdf





def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
