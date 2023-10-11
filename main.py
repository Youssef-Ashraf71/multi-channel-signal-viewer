
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


from PyQt5.QtGui import QPixmap
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Frame
from reportlab.lib.pagesizes import A4, landscape
import pyqtgraph.exporters as exporters
from PIL import Image
import statistics
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Image as PlatypusImage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas



class MainWindow(QtWidgets.QMainWindow):

        # Mainwindow constructor
      def __init__(self, *args, **kwargs):
          super(MainWindow, self).__init__(*args, **kwargs)
          uic.loadUi('beta.ui', self)
          self.setWindowIcon(QtGui.QIcon('Images/MainIcon.png'))
          self.setWindowTitle("Realtime-signal-viewer")
         # Apply Aqya stylesheet
          self.apply_stylesheet("MacOS.qss")

          self.xAxis1 = [0]
          self.yAxis1 = [0]
          self.xAxis2 = [0]
          self.yAxis2 = [0]
         # self.PlotterWindowProp = modules.PlotterWindow()
          self.pauseFlag1 = False
          self.pauseFlag2 = False
          self.pauseFlagLink=False
          self.isLinked = False
          self.holdHorizontalFlag1 = False
          self.holdVerticalFlag1 = False
          self.cineSpeed1 = 0
          self.cineSpeed2 = 0
          self.SignalChannelArr = []
          tmpList = [modules.SignalChannel()]
          self.SignalChannelArr.append(tmpList)
          tmpList = [modules.SignalChannel()]
          self.SignalChannelArr.append(tmpList)
          self.playPauseLinkBtn.setEnabled(False)
          self.zoomInLinkBtn.setEnabled(False)
          self.zoomOutLinkBtn.setEnabled(False)
          self.rewindLinkBtn.setEnabled(False)
          self.isSyncingX = False
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
                       if self.SignalChannelArr[0][modules.choosenChannelGraph1].path != "null":
                              QtWidgets.QMessageBox.warning(self,"Error browsing the file","Please add a new channel, selected channel is already in use")
                              return   
                       self.SignalChannelArr[0][modules.choosenChannelGraph1].path = path
                       if self.SignalChannelArr[0][0].path == "null":
                              QtWidgets.QMessageBox.warning(self,"Channel 1 in Graph 1 is Empty","Please use channel 1 first")
                              return
                       self.SignalChannelArr[0][modules.choosenChannelGraph1].time =  timeArr
                       self.SignalChannelArr[0][modules.choosenChannelGraph1].amplitude = amplitudeArr
                       self.Legend1 = choosenGraph.addLegend()
                       self.playPauseBtn1.setIcon(icon)

            elif choosenGraphIndex == 1:
                       if self.SignalChannelArr[1][modules.choosenChannelGraph2].path != "null":
                              QtWidgets.QMessageBox.warning(self,"Error browsing the file","Please add a new channel, selected channel is already in use")
                              return  
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
             #  self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].label = "Channel "+str(selectedChannelIndex+1)
            else:
                 for channelIndex in range(len(self.SignalChannelArr[choosenGraphIndex])):
                      if self.SignalChannelArr[choosenGraphIndex][channelIndex].path !="null":     
                              self.SignalChannelArr[choosenGraphIndex][channelIndex].graph = choosenGraph.plot(
                         name=self.SignalChannelArr[choosenGraphIndex][channelIndex].label ,
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
      
      
      
      
      def linkGraphs(self,isChecked):
           if self.linkGraphsCheckBox.isChecked() == False :
                         self.playPauseBtn1.setEnabled(True)
                         self.playPauseBtn2.setEnabled(True)
                         self.zoomInBtn1.setEnabled(True)
                         self.zoomInBtn2.setEnabled(True)
                         self.zoomOutBtn1.setEnabled(True)
                         self.zoomOutBtn2.setEnabled(True)
                         self.rewindBtn1.setEnabled(True)
                         self.rewindBtn2.setEnabled(True)
                         self.horizontalSlider.setEnabled(True)
                         self.speedSlider2.setEnabled(True)
                         self.playPauseLinkBtn.setEnabled(False)
                         self.zoomInLinkBtn.setEnabled(False)
                         self.zoomOutLinkBtn.setEnabled(False)
                         self.rewindLinkBtn.setEnabled(False)  
                         self.plotGraph1.getViewBox().sigXRangeChanged.disconnect(self.synchronizeXGraph1)
                         self.plotGraph2.getViewBox().sigXRangeChanged.disconnect(self.synchronizeXGraph2)
                         icon = QtGui.QIcon()
                         icon.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                         self.playPauseLinkBtn.setIcon(icon)
                         return
           if self.SignalChannelArr[0][0].path == "null" or self.SignalChannelArr[1][0].path == "null":
                    if isChecked:
                         self.linkGraphsCheckBox.setChecked(False)
                    QtWidgets.QMessageBox.warning(self,"Operation Failed","You can't link the two graphs if one of them is empty")
                    return
           icon = QtGui.QIcon()
           icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
           self.playPauseLinkBtn.setIcon(icon)
           self.playPauseBtn1.setEnabled(False)
           self.playPauseBtn2.setEnabled(False)
           self.zoomInBtn1.setEnabled(False)
           self.zoomInBtn2.setEnabled(False)
           self.zoomOutBtn1.setEnabled(False)
           self.zoomOutBtn2.setEnabled(False)
           self.rewindBtn1.setEnabled(False)
           self.rewindBtn2.setEnabled(False)
           self.horizontalSlider.setEnabled(False)
           self.speedSlider2.setEnabled(False)

           self.playPauseLinkBtn.setEnabled(True)
           self.zoomInLinkBtn.setEnabled(True)
           self.zoomOutLinkBtn.setEnabled(True)
           self.rewindLinkBtn.setEnabled(True)
           self.rewindSignal(self.plotGraph1,0)
           self.rewindSignal(self.plotGraph2,1)
           
           self.plotGraph1.getViewBox().sigXRangeChanged.connect(self.synchronizeXGraph1)
           self.plotGraph2.getViewBox().sigXRangeChanged.connect(self.synchronizeXGraph2)
           
          #  self.isLinked = isChecked


      def playPauseLink(self,playPauseBtn,playPauseBtn1,playPauseBtn2):
             icon = QtGui.QIcon()
             self.pauseFlagLink ^= True
             if self.pauseFlagLink == True :
                     icon.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                     playPauseBtn.setIcon(icon)
                   
             else:
                    icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    playPauseBtn.setIcon(icon)
          

             self.pauseGraph(playPauseBtn1,0)
             self.pauseGraph(playPauseBtn2,1)


      def zoomInLink(self,graph1,graph2):
            self.zoomSignalIn(graph1)
            self.zoomSignalIn(graph2)

      def zoomOutLink(self,graph1,graph2):
            self.zoomSignalOut(graph1)
            self.zoomSignalOut(graph2)
      
      def rewindLink(self,graph1,graph2):
            self.rewindSignal(graph1,0)
            self.rewindSignal(graph2,1)

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
          #  self.SignalChannelArr[choosenGraphIndex][-1].label = "Channel" + str(len(self.SignalChannelArr[choosenGraphIndex])+1)
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
             print("ana hena ya homar")
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
          #  val = self.xAxisScrollBar1.value()
          #  xmax = np.ceil(self.data[0][-1+self.vsize-self.psize+val])-1
          #  xmin = xmax-self.vsize
          #  self.plot_widget.setXRange(xmin, xmax)
          pass
     
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
               if choosenGraphIndex == 0:
                    self.channelList1.setItemText(selectedChannelIndex,label)
               elif choosenGraphIndex == 1:
                     self.channelList2.setItemText(selectedChannelIndex,label)
                                


     #  def synchronizeXGraph1(self,graph1,graph2):
     #      #  graph2.getViewBox().blockSignals(True)  # Block signals temporarily to avoid recursion
     #       graph2.getViewBox().setXRange(*graph1.getViewBox().viewRange()[0])
     #      #  graph2.getViewBox().blockSignals(False)  # Unblock signals
          

     #  def synchronizeXGraph2(self,graph1,graph2):
     #         graph1.getViewBox().setXRange(*graph2.getViewBox().viewRange()[0])
     #         graph1.getViewBox().blockSignals(False)  # Unblock signals

      def synchronizeXGraph1(self):
        if not self.isSyncingX:
            # Disconnect the signals to avoid recursion
            self.plotGraph2.getViewBox().sigXRangeChanged.disconnect(self.synchronizeXGraph2)
            
            # Set the X-axis range of graph2 based on graph1
            xRange = self.plotGraph1.getViewBox().viewRange()[0]
            self.isSyncingX = True
            self.plotGraph2.getViewBox().setXRange(*xRange)
            self.isSyncingX = False
            
            # Reconnect the signal
            self.plotGraph2.getViewBox().sigXRangeChanged.connect(self.synchronizeXGraph2)

      def synchronizeXGraph2(self):
        if not self.isSyncingX:
            # Disconnect the signals to avoid recursion
            self.plotGraph1.getViewBox().sigXRangeChanged.disconnect(self.synchronizeXGraph1)
            
            # Set the X-axis range of graph1 based on graph2
            xRange = self.plotGraph2.getViewBox().viewRange()[0]
            self.isSyncingX = True
            self.plotGraph1.getViewBox().setXRange(*xRange)
            self.isSyncingX = False
            
            # Reconnect the signal
            self.plotGraph1.getViewBox().sigXRangeChanged.connect(self.synchronizeXGraph1)

      # export the report to pdf
      def captureGraphImage(self, targetGraph):
          # Create an exporter to capture the graph
          if (targetGraph == 0):
               exporter = exporters.ImageExporter(self.plotGraph1.scene())
          elif(targetGraph == 1):
               exporter = exporters.ImageExporter(self.plotGraph2.scene())
          

          # Set the file suffix to specify the export type
          exporter.params.fileSuffix = 'png'

          # Set the filename
          export_filename = 'graph_capture.png'

          # Export the graph to the specified filename
          exporter.export(export_filename)

      def moveSignal(self,choosenGraphIndex):
            if choosenGraphIndex == 0 :
                  currentMovedSignalIndex = modules.choosenChannelGraph1
                  print("Graph 1 ",currentMovedSignalIndex)
                  currentMovedSignal = self.SignalChannelArr[choosenGraphIndex][currentMovedSignalIndex]
                  self.SignalChannelArr[1].append(modules.SignalChannel())
                  self.SignalChannelArr[1][-1].setData(time = currentMovedSignal.time,amplitude = currentMovedSignal.amplitude, hiddenFlag =currentMovedSignal.hiddenFlag
                  , label =  currentMovedSignal.label, color =  currentMovedSignal.color, path =  currentMovedSignal.path)
                  
                  _translate = QtCore.QCoreApplication.translate
                  self.channelList1.removeItem(currentMovedSignalIndex)
                  self.channelList2.addItem(_translate("MainWindow",self.SignalChannelArr[1][-1].label))


                  self.plotGraph1.removeItem(currentMovedSignal.graph)
                  self.SignalChannelArr[choosenGraphIndex].pop(currentMovedSignalIndex)
                  if len( self.SignalChannelArr[choosenGraphIndex]) == 0:
                         self.addNewChannel(self.channelList1,choosenGraphIndex)
                  if modules.choosenChannelGraph1 > 0:
                        modules.choosenChannelGraph1-=1
                  self.xAxis2.append(0)
                  self.yAxis2.append(0)
                  self.Legend2 = self.plotGraph2.addLegend()
                  self.rewindSignal(self.plotGraph2,1)
            elif choosenGraphIndex == 1:
                  currentMovedSignalIndex = modules.choosenChannelGraph2
                  print("Graph 2 ",currentMovedSignalIndex)
                  currentMovedSignal = self.SignalChannelArr[choosenGraphIndex][currentMovedSignalIndex]
                  self.SignalChannelArr[0].append(modules.SignalChannel())
                  self.SignalChannelArr[0][-1].setData(time = currentMovedSignal.time,amplitude = currentMovedSignal.amplitude, hiddenFlag =currentMovedSignal.hiddenFlag
                  , label =  currentMovedSignal.label, color =  currentMovedSignal.color, path =  currentMovedSignal.path)

                  _translate = QtCore.QCoreApplication.translate
                  self.channelList2.removeItem(currentMovedSignalIndex)
                  self.channelList1.addItem(_translate("MainWindow", self.SignalChannelArr[0][-1].label))

                  self.plotGraph2.removeItem(currentMovedSignal.graph)
                  self.SignalChannelArr[choosenGraphIndex].pop(currentMovedSignalIndex)
                  if len( self.SignalChannelArr[choosenGraphIndex]) == 0:
                         self.addNewChannel(self.channelList2,choosenGraphIndex)
                  if modules.choosenChannelGraph2 >0:
                        modules.choosenChannelGraph2-=1
                  self.xAxis1.append(0)
                  self.yAxis1.append(0)
                  self.Legend1 = self.plotGraph1.addLegend()
                  self.rewindSignal(self.plotGraph1,0)

      def calculatePlotStatistics(self, targetGraph):
          
          #data
          amplitudes = []
          meanValues = []
          medianValues = []
          modeValues = []
          standardDeviations = []
          channelsNumbers = []
          channelLabels = []

          if targetGraph == 0:
               # selectedChannelIndex = modules.choosenChannelGraph1
               for Index in range(len(self.SignalChannelArr[0])):
                    if self.SignalChannelArr[targetGraph][Index].path != "null":
                         amplitudes.append(self.SignalChannelArr[targetGraph][Index].amplitude)
                         channelsNumbers.append(Index)
                         channelLabels.append(self.SignalChannelArr[targetGraph][Index].label)

                     
          elif targetGraph == 1:
               # selectedChannelIndex = modules.choosenChannelGraph2
               for  Index in range(len(self.SignalChannelArr[targetGraph])):
                    if self.SignalChannelArr[targetGraph][Index].path != "null":
                         amplitudes.append(self.SignalChannelArr[targetGraph][Index].amplitude)
                         channelsNumbers.append(Index)
                         channelLabels.append(self.SignalChannelArr[targetGraph][Index].label)


          for index, dataset in enumerate(amplitudes):
               if dataset:
                    meanValues.append(statistics.mean(dataset))
                    medianValues.append(statistics.median(dataset))
                    modeValues.append(statistics.mode(dataset))
                    standardDeviations.append(statistics.stdev(dataset))
               else:
                    meanValues.append("N/A")
                    medianValues.append("N/A")
                    modeValues.append("N/A")
                    standardDeviations.append("N/A")

                    # Create a table to display statistics
          tableData = []
          tableData.append(["signal", "Channel number", "Mean", "Median", "Mode", "Standard Deviation"])

          for label, channel, mean, median, mode, std_dev in zip(channelLabels, channelsNumbers, meanValues, medianValues, modeValues, standardDeviations):
               tableData.append([ label, channel+1, round(mean,4), round(median,4), round(mode,4), round(std_dev,4)])
               # TABLE STYLE    
          style = TableStyle([
          ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),  # Light gray background for the header row
          ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),      # Black text color for the header row
          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
          ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
          ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
          ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
          ('GRID', (0, 0), (-1, -1), 1, colors.black)
          ])
          table = Table(tableData)
          table.setStyle(style)

          return table
          
  
     # export the report to pdf
      def exportReportPdf(self, graphNumber):

          fileName = 'Report.pdf'
          title = 'Signals Insights'
          if(graphNumber == 0):
                selectedGraph = 'Report for Graph 1'
          if(graphNumber == 1):
                selectedGraph = 'Report for Graph 2'                
          
          # Capture the plot and get the file path

          self.captureGraphImage(graphNumber)
          
          pdf = canvas.Canvas(fileName, pagesize=letter )
          
          pdf.setFont("Helvetica", 24)

          pdf.drawCentredString(290, 720, title)

          pdf.drawAlignedString(260, 670, selectedGraph)

          majorLogoPath = './Images/logo-major.png'
          collegeLogoPath = './Images/collegeLogo.jpg'
          
          major_logo = ImageReader(majorLogoPath)
          college_logo = ImageReader(collegeLogoPath)
          
          # Add logos to the PDF
          pdf.drawImage(major_logo, 10, 725, width=112, height=45)
          pdf.drawImage(college_logo, 525, 705, width=70, height=70)
          
          # Open the image file
          image = Image.open('graph_capture.png')
          # Get the size (width and height) of the image
          image_width, image_height = image.size
          aspect_ratio = image_width / image_height
          # Close the image file
          image.close()
          
          plotImg = ImageReader('graph_capture.png')
          pdf.drawImage(plotImg, 35, 500, width=550, height=550 / aspect_ratio)
          statistics_table = self.calculatePlotStatistics(graphNumber)
          statistics_table.wrapOn(pdf, 0, 0)
          statistics_table.drawOn(pdf, 60, 400)  
          
          pdf.save()




def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
