
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QFile, QTextStream
import scipy.io
from scipy import signal
import numpy as np

import pandas as pd
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import csv
import os

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
          uic.loadUi('layout.ui', self)
          self.setWindowIcon(QtGui.QIcon('Images/MainIcon.png'))
          self.setWindowTitle("Realtime-signal-viewer")
         # Apply Aqya stylesheet
          self.apply_stylesheet("ManjaroMix.qss")

          self.xAxis1 = [0]
          self.yAxis1 = [0]
          self.xAxis2 = [0]
          self.yAxis2 = [0]
          self.pauseFlag1 = False
          self.pauseFlag2 = False
          self.pauseFlagLink=False
          self.isLinked = False
          self.cineSpeed1 = 0
          self.cineSpeed2 = 0
          self.SignalChannelArr = []
          tmpList = [modules.SignalChannel()]
          self.SignalChannelArr.append(tmpList)
          tmpList = [modules.SignalChannel()]
          self.SignalChannelArr.append(tmpList)
          self.playPauseLinkBtn.hide()
          self.zoomInLinkBtn.hide()
          self.zoomOutLinkBtn.hide()
          self.rewindLinkBtn.hide()
          self.isSyncingX = False
          self.about_clicked = False 
          connector.__init__connectors__(self)
          


      def apply_stylesheet(self, stylesheet_path):
        """
        This function reads a Qt StyleSheet from a file and applies it to the
        calling QWidget. The Qt StyleSheet (QSS) allows you to define the
        appearance and styling of Qt widgets.

        Parameters:
        - self (QWidget): The calling QWidget instance to apply the stylesheet to.
        - stylesheet_path (str): The path to the QSS stylesheet file to be applied.

        Returns:
        This function does not return any values.
        """
        stylesheet = QFile(stylesheet_path)
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(stylesheet)
            qss = stream.readAll()
            self.setStyleSheet(qss)
        else:
            print(f"Failed to open stylesheet file: {stylesheet_path}")


      def browse(self,choosenGraph,choosenGraphIndex):
            """
            Open a file dialog to select a data file and trigger a function to process it.

            This function opens a file dialog that allows the user to choose a data file
            (typically in the formats .txt, .csv, or .xls). If a file is selected, it
            then calls the 'openFile' function to process and load the data from the
            chosen file.

            Parameters:
            - self: The calling object instance.
            - choosenGraph (QWidget): The widget representing the chosen graph.
            - choosenGraphIndex (int): An index representing the selected graph.

            Returns:
            This function does not return any values.
            """
            self.fileName = QFileDialog.getOpenFileName(None,"Open a File","./",filter="Raw Data(*.txt *.csv *.xls)" )
            if self.fileName[0]:
                 self.openFile(self.fileName[0],choosenGraph,choosenGraphIndex)   


      def openFile(self, path:str,choosenGraph, choosenGraphIndex):
            """
            Open and process a data file, and load its content into the selected graph.

            This function opens and processes a data file located at the given 'path'. The
            data is expected to be in formats such as .csv, .txt, or .xls. It reads the
            time and amplitude data from the file, associates it with the specified graph,
            and updates the corresponding channel.

            Parameters:
            - self: The calling object instance.
            - path (str): The file path to the data file to be opened and processed.
            - choosenGraph (QWidget): The widget representing the chosen graph.
            - choosenGraphIndex (int): An index representing the selected graph.

            Returns:
            This function does not return any values.
            """
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


      def signalInitialization(self,choosenGraph,choosenGraphIndex,isRewinding):
            """
            Initialize the graph with signal data and configure real-time plotting.

            This function is responsible for setting up the selected graph (choosenGraph)
            for signal data visualization. It configures real-time plotting and initializes
            various parameters for the specified graph.

            Parameters:
            - self: The calling object instance.
            - choosenGraph (QWidget): The widget representing the chosen graph for signal
              data visualization.
            - choosenGraphIndex (int): An index representing the selected graph.
            - isRewinding (bool): A boolean indicating whether the graph is being rewound or not.

            Returns:
            This function does not return any values.
            """
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
               self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].label = "Channel "+str(selectedChannelIndex+1)
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

  


      def  signalPlotting(self,choosenGraph,choosenGraphIndex):
           """
           Plot real-time signal data on the selected graph.

           This function is responsible for updating and plotting real-time signal data on
           the chosen graph. It retrieves time and amplitude data from the associated channels
           and updates the graph with the latest data points.

           Parameters:
           - self: The calling object instance.
           - choosenGraph (QWidget): The widget representing the chosen graph for signal data
               visualization.
           - choosenGraphIndex (int): An index representing the selected graph.

           Returns:
           This function does not return any values.
           """
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
                self.plotGraph1.setXRange(self.getLongestSignal(0,self.pointsPlotted1)-0.1,self.getLongestSignal(0,self.pointsPlotted1))
           elif choosenGraphIndex == 1:
                self.pointsPlotted2 += 5
                self.plotGraph2.setXRange(self.getLongestSignal(1,self.pointsPlotted2)-0.1,self.getLongestSignal(1,self.pointsPlotted2))    
           for channelIdx in range(len(self.SignalChannelArr[choosenGraphIndex])):
                  if self.SignalChannelArr[choosenGraphIndex][channelIdx].path != "null":
                       if choosenGraphIndex == 0:
                              if len(self.SignalChannelArr[choosenGraphIndex][channelIdx].time) > self.pointsPlotted1:
                              
                                    self.SignalChannelArr[choosenGraphIndex][channelIdx].graph.setData(self.xAxis1[channelIdx], self.yAxis1[channelIdx], pen=self.SignalChannelArr[choosenGraphIndex][channelIdx].getColor(), name=self.SignalChannelArr[choosenGraphIndex][channelIdx].label) 

                       elif choosenGraphIndex == 1:
                               if len(self.SignalChannelArr[choosenGraphIndex][channelIdx].time) > self.pointsPlotted2:
                              
                                    self.SignalChannelArr[choosenGraphIndex][channelIdx].graph.setData(self.xAxis2[channelIdx], self.yAxis2[channelIdx], pen=self.SignalChannelArr[choosenGraphIndex][channelIdx].getColor(), name=self.SignalChannelArr[choosenGraphIndex][channelIdx].label)   
                      

      def DynamicSignalUpdate(self, choosenGraphIndex, selectedChannelIndex,  isChangingColor = False):
           """
           Update the dynamic signal data as { hide state / Color change } on the selected graph.

           This function is responsible for updating the dynamic signal data on the selected
           graph upon checking the visibility and color of each channel's data, and updates the
           graph accordingly.

           Parameters:
           - self: The calling object instance.
           - choosenGraphIndex (int): An index representing the selected graph.
           - selectedChannelIndex (int): An index representing the selected channel.
           - isChangingColor (bool): A boolean indicating whether the color is changing.

           Returns:
           This function does not return any values.
           """
           for Index in range(len(self.SignalChannelArr[choosenGraphIndex])):
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
                   ######################################################################      
                    if len(self.SignalChannelArr[choosenGraphIndex][Index].time) > currentpointsPlotted and isChangingColor == False:
                         self.SignalChannelArr[choosenGraphIndex][Index].graph.setData(
                              currentXAxis[Index], currentYAxis[Index], pen=self.SignalChannelArr[choosenGraphIndex][Index].getColor(), name=self.SignalChannelArr[choosenGraphIndex][Index].label, skipFiniteCheck=True)
                    elif len(self.SignalChannelArr[choosenGraphIndex][Index].time) <= currentpointsPlotted  and isChangingColor == True:
                         self.SignalChannelArr[choosenGraphIndex][Index].graph.setData(
                              currentXAxis[Index], currentYAxis[Index], pen=self.SignalChannelArr[choosenGraphIndex][Index].getColor(), name=self.SignalChannelArr[choosenGraphIndex][Index].label, skipFiniteCheck=True)
                    elif len(self.SignalChannelArr[choosenGraphIndex][Index].time) > currentpointsPlotted  and isChangingColor == True:
                         self.SignalChannelArr[choosenGraphIndex][Index].graph.setData(
                              currentXAxis[Index], currentYAxis[Index], pen=self.SignalChannelArr[choosenGraphIndex][Index].getColor(), name=self.SignalChannelArr[choosenGraphIndex][Index].label, skipFiniteCheck=True)     
      
      
      
      
      def linkGraphs(self):
           """
           Link the two graphs when the button is clicked

           This function is used to link the two graphs together by calling the rewindSignal function 
           on the two graphs, it disables the buttons of the two graphs as well.

           Parameters:
           - self: The calling object instance.

           Returns:
           This function doesn't return any values.
           """
           if self.isLinked == True :
                         self.isLinked = False

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
                         self.linkGraphsButton.setText("Link Graphs")

                         self.playPauseLinkBtn.hide()
                         self.zoomInLinkBtn.hide()
                         self.zoomOutLinkBtn.hide()
                         self.rewindLinkBtn.hide()

                         self.plotGraph1.getViewBox().sigXRangeChanged.disconnect(self.synchronizeXGraph1)
                         self.plotGraph2.getViewBox().sigXRangeChanged.disconnect(self.synchronizeXGraph2)  

                         icon = QtGui.QIcon()
                         icon.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        # self.playPauseLinkBtn1.setIcon(icon)
                        # self.playPauseLinkBtn2.setIcon(icon)

                         self.plotGraph1.getViewBox().enableAutoRange(axis = self.plotGraph1.getViewBox().XAxis, enable=True)
                         self.plotGraph2.getViewBox().enableAutoRange(axis = self.plotGraph2.getViewBox().XAxis, enable=True)
                         self.plotGraph1.getViewBox().enableAutoRange(axis = self.plotGraph1.getViewBox().YAxis, enable=True)
                         self.plotGraph2.getViewBox().enableAutoRange(axis = self.plotGraph2.getViewBox().YAxis, enable=True)
 

                         return
           if ( self.isSignalFound(0) == False)  or (self.isSignalFound(1) == False):
                    if self.isLinked:
                        self.isLinked = False
                    QtWidgets.QMessageBox.warning(self,"Operation Failed","You can't link the two graphs if one of them is empty")
                    return
           self.isLinked = True
           icon = QtGui.QIcon()
           icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
           self.playPauseLinkBtn.setIcon(icon)
           icon.addPixmap(QtGui.QPixmap("Images/unlink.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
           self.linkGraphsButton.setIcon(icon)
           self.linkGraphsButton.setText("Unlink Graphs")

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

           self.playPauseLinkBtn.show()
           self.zoomInLinkBtn.show()
           self.zoomOutLinkBtn.show()
           self.rewindLinkBtn.show()

           self.rewindSignal(self.plotGraph1,0)
           self.rewindSignal(self.plotGraph2,1)
           
           self.plotGraph1.getViewBox().sigXRangeChanged.connect(self.synchronizeXGraph1)
           self.plotGraph2.getViewBox().sigXRangeChanged.connect(self.synchronizeXGraph2)
           


      def playPauseLink(self,playPauseBtn,playPauseBtn1,playPauseBtn2):
             """
             Pause/Play the two graphs when the they are linked

             This function is called when the two graphs are linked to pause or play them together,
             it calls the pauseGraph function twice once for each graph of them . 

             parameters:
             - self: The calling object instance.
             - PlayPauseBtn: Instance of the calling button
             - playPauseBtn1: The button of the first graph
             - playPauseBtn2: The button of the second graph

             Returns:
             This function doesn't return any parameters.
             """
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
            """
            Zoom the two graphs in when they are linked

            This function is used to Zoom the two graphs in when the zoomin button is clicked 

            Parameters:
            - self: The calling object instance.
            - graph1: The Plotwidget of the first graph
            - graph2: The Plotwidget of the second graph

            Returns:     
            This function doesn't return any values.
            """
            self.zoomSignalIn(graph1)
            self.zoomSignalIn(graph2)

      def zoomOutLink(self,graph1,graph2):
            """
            Zoom the two graphs out when they are linked

            This function is used to Zoom the two graphs out when the zoomout button is clicked 

            Parameters:
            - self: The calling object instance.
            - graph1: The Plotwidget of the first graph
            - graph2: The Plotwidget of the second graph

            Returns:
            This function doesn't return any values.
            """
            self.zoomSignalOut(graph1)
            self.zoomSignalOut(graph2)
      
      def rewindLink(self,graph1,graph2):
            """
            Rewind the two graphs together when linked

            This function is used to rewind the two graphs when the rewind button is clicked,
            it calls the rewindSignal function, it also resets the view of the two graphs.

            Parameters:
            - self: The calling object instance.
            - graph1: The Plotwidget of the first graph
            - graph2: The Plotwidget of the second graph

             Returns:
             This function doesn't return any parameters.
            """
            self.plotGraph1.getViewBox().sigXRangeChanged.disconnect(self.synchronizeXGraph1)
            self.plotGraph2.getViewBox().sigXRangeChanged.disconnect(self.synchronizeXGraph2)  
            self.plotGraph1.getViewBox().enableAutoRange(axis = self.plotGraph1.getViewBox().XAxis, enable=True)
            self.plotGraph2.getViewBox().enableAutoRange(axis = self.plotGraph2.getViewBox().XAxis, enable=True)
            self.plotGraph1.getViewBox().enableAutoRange(axis = self.plotGraph1.getViewBox().YAxis, enable=True)
            self.plotGraph2.getViewBox().enableAutoRange(axis = self.plotGraph2.getViewBox().YAxis, enable=True)
            self.rewindSignal(graph1,0)
            self.rewindSignal(graph2,1)
            self.plotGraph1.getViewBox().sigXRangeChanged.connect(self.synchronizeXGraph1)
            self.plotGraph2.getViewBox().sigXRangeChanged.connect(self.synchronizeXGraph2)
           

      def zoomSignalIn(self,choosengraph):
          """
          Zoom the selected graph in

          This function is used to zoom the selected graph in when the zoom in button is clicked

          parameters:
          - self: The calling object instance.
          - choosengraph: the graph in which we want to zoom in

          Return:
          This function doesn't return any value.
          """
          choosengraph.plotItem.getViewBox().scaleBy((0.5, 0.5))


      def zoomSignalOut(self,choosengraph):
          """
          Zoom the selected graph out

          This function is used to zoom the selected graph out when the zoom out button is clicked

          parameters:
          - self: The calling object instance.
          - choosengraph: the graph in which we want to zoom out

          Return:
          This function doesn't return any value.
          """ 
          choosengraph.plotItem.getViewBox().scaleBy((2, 2))


      def setSignalChannelColor(self,choosenGraphIndex):
           """
           sets the color of the signal

           This function is used to set the color of a signal, it also calls the  DynamicSignalUpdate function which updates the state of the color

           parameters:
           - self: The calling object instance.
           - choosenGraphIndex: the index of the graph whether it is 1 or 2

           Returns:
           This function doesn't return any value.
           """
           selectedChannelIndex = 0
           if choosenGraphIndex == 0:
                 selectedChannelIndex = modules.choosenChannelGraph1
           elif choosenGraphIndex == 1:
                      selectedChannelIndex = modules.choosenChannelGraph2
           self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].setColor(QColorDialog.getColor().name())
           self.DynamicSignalUpdate(choosenGraphIndex,selectedChannelIndex,True)

      def addNewChannel(self,choosenChannelList,choosenGraphIndex):
            """
            Add new channels to a certain graph

            This function is used to add new channels to the selected graph

            parameters:
            - self: The calling object instance.
            - choosenChannelList: Whether it is the channel list of the first or the second graph
            - choosenGraphIndex: Whether it graph 1 or graph 2

            Returns:
            This function doesn't return any value.
            """
            _translate = QtCore.QCoreApplication.translate
            choosenChannelList.addItem(_translate("MainWindow", "Channel "+str(len(self.SignalChannelArr[choosenGraphIndex])+1)))
            if choosenGraphIndex == 0:
                  self.xAxis1.append(0)
                  self.yAxis1.append(0)
            elif choosenGraphIndex == 1:
                  self.xAxis2.append(0)
                  self.yAxis2.append(0)   
            self.SignalChannelArr[choosenGraphIndex].append(modules.SignalChannel())



      def pauseGraph(self,playpauseButton,choosenGraphIndex):
           """
           pause/play the graph

           This function is used to pause/play the signal when the play/pause button is clicked in a certain graph,

           parameters:
           - self: The calling object instance.
           - playpauseButton: the instance of the button 
           - choosenGraphIndex: Whether it is graph 1 or graph 2

           Returns:
           This function doesn't return any value. 
           """
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
                



      def rewindSignal(self,choosengraph,choosenGraphIndex):
             '''
             Rewinds/Restarts the signals on a PlotWidget of a certain graph

             This function Restarts all the signals on a specific PlotWidget or Graph on the application

             params:
             - self: The calling object instance.
             - choosengraph: The PlotWidget instance (Graph1 or Graph2 Objects)
             - choosenGraphIndex: This is an index argument that is given to know which Graph
               the rewind signal is called to Restart the signals

              Returns:
              This function does not return any values.
             '''
             selectedChannelIndex = 0
             icon = QtGui.QIcon()
             if choosenGraphIndex == 0:
                      selectedChannelIndex = modules.choosenChannelGraph1
                      icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                      self.playPauseBtn1.setIcon(icon)
                    
             elif choosenGraphIndex == 1:
                      selectedChannelIndex = modules.choosenChannelGraph2
                      icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                      self.playPauseBtn2.setIcon(icon)
             if self.isLinked == True:
                   self.playPauseLinkBtn.setIcon(icon)
             choosengraph.clear()
             self.resetGraphsZooming()
             self.signalInitialization(choosengraph,choosenGraphIndex,True)
             self.DynamicSignalUpdate(choosenGraphIndex,0,False)
             

  
      
      def hideSignal(self,checked,choosenGraphIndex):
             '''
               Hide the signal or Plot plotted on the graph.

               This function Hides the plotted signal or plot on the PlotWidget 
               It hides specific channels depending on the choosen channel in each graph
               and whether the hide box is checked on the first graph or the second graph controls.

               params:
                    - self: The calling object instance.
                    - checked: This is a boolean value that is passed 1 if the hide check box is true 
                    and passed 0 if the hide checkbox is unchecked.
                    - choosenGraphIndex: This is a variable that holds the index of the graph to perform the function on

               returns:
                    This function does not return any values.
             '''
             selectedChannelIndex = 0
             if choosenGraphIndex == 0:
                 selectedChannelIndex = modules.choosenChannelGraph1
             elif choosenGraphIndex == 1:
                      selectedChannelIndex = modules.choosenChannelGraph2
             self.SignalChannelArr[choosenGraphIndex][selectedChannelIndex].hiddenFlag = checked
             self.DynamicSignalUpdate(choosenGraphIndex,selectedChannelIndex,False)

      def getLongestSignal(self,choosenGraphIndex,pointsPlotted):
            ans = -1
            for channedlIndex in range(len(self.SignalChannelArr[choosenGraphIndex])):
                  if self.SignalChannelArr[choosenGraphIndex][channedlIndex].path !="null":
                        ans = max(ans , self.SignalChannelArr[choosenGraphIndex][channedlIndex].time[pointsPlotted-1])
            return ans      
                  
             
      def speedSlider(self,choosenGraphIndex):
           '''
               Changes the speed of the plotting of each graph

               This function changes the interval between the time Plotting happens
               The lower the time --> The faster the graph plots
               This function is customized so that it works customized to each speed slider (graph1 and graph2 controls)

          params:
              - self: The calling object instance.
              -  choosenGraphIndex:: This is a variable that holds the index of the graph to perform the function on.

          returns:
                    This function has no return values
          '''
           if choosenGraphIndex == 0:           
               self.cineSpeed1= self.horizontalSlider.value()
               self.startTime1.setInterval(200-self.cineSpeed1)
           else: 
               self.cineSpeed2 = self.speedSlider2.value()
               self.startTime2.setInterval(200-self.cineSpeed2)    


      def editChannelName(self,label,choosenGraphIndex):
               '''
                    Edits the name of each Channel in the respective graph

                    This function edits the name of the channel with the label typed
                    by the user on the QlineEdit and it also changes the name of the legend of that signal channel
                    customized to each graph. The function gets called when LineEdit is returned.

                    Params:
                         - self: The calling object instance.
                         - label: its a parameter that is passed to the function that contains the text of the QLineEdit
                         - choosenGraphIndex: This is a variable that holds the index of the graph to perform the function on.

                    returns:
                         This function has no return values
               '''
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
                                

      def isSignalFound(self,choosenGraphIndex):
            '''
            Check if Signals are Found in a Specific Graph

            This function checks if there are any signals found in a specific graph, identified by the given `choosenGraphIndex`. It iterates through the signal channels within the graph and checks if any of them have a non-null path, indicating the presence of a signal.

            Parameters:
                    - self: The instance of the class where this method is defined.
                    - choosenGraphIndex: An index argument specifying the graph to be checked for signal presence.

            Returns:
                    True if at least one signal is found in the specified graph; otherwise, False.

            '''
            for channelIndex in range(len(self.SignalChannelArr[choosenGraphIndex])):
                  if self.SignalChannelArr[choosenGraphIndex][channelIndex].path != "null":
                        return True
            return False   

      def synchronizeXGraph1(self):
        '''
          Synchronize X-axis Range for Graph1

          This function synchronizes the X-axis range of Graph1 with Graph2. It disconnects the X-range changed signal to avoid recursion,
            sets the X-axis range of Graph2 based on Graph1, and then reconnects the signal.

          If the X-axis range of Graph1 changes, this function will automatically adjust Graph2 to match it.

          Note:
          - Make sure to call this function when Graph1's X-axis range should be synchronized with Graph2.
          - Ensure that the `isSyncingX` flag is set to `False` when calling this function.

          Parameters:
               - self: The instance of the class where this method is defined.
         '''
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
        '''
          Synchronize X-axis Range for Graph2

          This function synchronizes the X-axis range of Graph2 with Graph1. It disconnects the X-range changed signal to avoid recursion, 
          sets the X-axis range of Graph1 based on Graph2, and then reconnects the signal.

          If the X-axis range of Graph2 changes, this function will automatically adjust Graph1 to match it.

          Note:
          - Make sure to call this function when Graph2's X-axis range should be synchronized with Graph1.
          - Ensure that the `isSyncingX` flag is set to `False` when calling this function.

          Parameters:
               - self: The instance of the class where this method is defined.

          Returns:
               This function does not have any returns
        '''
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
          '''
          Capture and Export a Graph to an Image

          This function captures and exports the specified graph (either Graph1 or Graph2) to an image file (PNG format by default). It creates an exporter to capture the graph scene, sets the export filename, and exports the graph.

          Note:
               - Ensure that the necessary exporter module (e.g., exporters.ImageExporter) is available.
               - The captured image will be saved as 'graph_capture.png' in the current working directory by default.

          Parameters:
               - self: The instance of the class where this method is defined.
               - targetGraph: An integer (0 for Graph1, 1 for Graph2) indicating the target graph to capture.
          
          Returns:
               This function does not have any return values
          
          '''
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
            '''
               Move a Signal Between the two Graphs

               This function moves a signal from one graph (Graph1 or Graph2) to the other graph, specified by `choosenGraphIndex`.
                 It performs the necessary operations to transfer the signal,
                 including creating a new signal in the target graph, 
                 Adding the channel in the combo box and changing the Legend accordingly, 
                 and rewinding the signals in the target graph.

               Parameters:
                    - self: The instance of the class where this method is defined.
                    - choosenGraphIndex: An integer (0 for Graph1, 1 for Graph2) indicating the target graph where the signal will be moved.

               Returns:
               This function does not have any return values
            '''
            if choosenGraphIndex == 0 :
                  currentMovedSignalIndex = modules.choosenChannelGraph1 
                  currentMovedSignal = self.SignalChannelArr[choosenGraphIndex][currentMovedSignalIndex]
                  self.SignalChannelArr[1].append(modules.SignalChannel())
                  self.SignalChannelArr[1][-1].setData(time = currentMovedSignal.time,amplitude = currentMovedSignal.amplitude, hiddenFlag =currentMovedSignal.hiddenFlag
                  , label =  currentMovedSignal.label, color =  currentMovedSignal.color, path =  currentMovedSignal.path)
                  
                  _translate = QtCore.QCoreApplication.translate
                  self.channelList1.removeItem(currentMovedSignalIndex)
                  self.channelList2.addItem(_translate("MainWindow",self.SignalChannelArr[1][-1].label))


                  self.plotGraph1.removeItem(currentMovedSignal.graph)
                  self.SignalChannelArr[choosenGraphIndex].pop(currentMovedSignalIndex)
                  if modules.choosenChannelGraph1 > 0:
                        modules.choosenChannelGraph1 = modules.choosenChannelGraph1 -1
                        self.channelList1.setCurrentIndex(modules.choosenChannelGraph1)
                  if len( self.SignalChannelArr[choosenGraphIndex]) == 0:
                         self.addNewChannel(self.channelList1,choosenGraphIndex)

                  self.xAxis2.append(0)
                  self.yAxis2.append(0)
                  self.Legend2 = self.plotGraph2.addLegend()
                  self.rewindSignal(self.plotGraph2,1)
            elif choosenGraphIndex == 1:
                  currentMovedSignalIndex = modules.choosenChannelGraph2
                  currentMovedSignal = self.SignalChannelArr[choosenGraphIndex][currentMovedSignalIndex]
                  self.SignalChannelArr[0].append(modules.SignalChannel())
                  self.SignalChannelArr[0][-1].setData(time = currentMovedSignal.time,amplitude = currentMovedSignal.amplitude, hiddenFlag =currentMovedSignal.hiddenFlag
                  , label =  currentMovedSignal.label, color =  currentMovedSignal.color, path =  currentMovedSignal.path)

                  _translate = QtCore.QCoreApplication.translate
                  self.channelList2.removeItem(currentMovedSignalIndex)
                  self.channelList1.addItem(_translate("MainWindow", self.SignalChannelArr[0][-1].label))

                  self.plotGraph2.removeItem(currentMovedSignal.graph)
                  self.SignalChannelArr[choosenGraphIndex].pop(currentMovedSignalIndex)
                  if modules.choosenChannelGraph2 >0:
                         modules.choosenChannelGraph2 = modules.choosenChannelGraph2-1
                         self.channelList1.setCurrentIndex(modules.choosenChannelGraph2)
                  if len( self.SignalChannelArr[choosenGraphIndex]) == 0:
                         self.addNewChannel(self.channelList2,choosenGraphIndex)

                  self.xAxis1.append(0)
                  self.yAxis1.append(0)
                  self.Legend1 = self.plotGraph1.addLegend()
                  self.rewindSignal(self.plotGraph1,0)



      def resetGraphsZooming(self):
                  '''
                    Reset Zooming for Both Graphs

                    This function resets the zooming for both Graph1 and Graph2. 
                    It enables the auto range for both X and Y axes in both graphs, effectively resetting the zoom levels.

                    Parameters:
                         - self: The instance of the class where this method is defined.

                    Returns:
                         This function does not return any value
                  '''
                  self.plotGraph1.getViewBox().enableAutoRange(axis = self.plotGraph1.getViewBox().XAxis, enable=True)
                  self.plotGraph2.getViewBox().enableAutoRange(axis = self.plotGraph2.getViewBox().XAxis, enable=True)
                  self.plotGraph1.getViewBox().enableAutoRange(axis = self.plotGraph1.getViewBox().YAxis, enable=True)
                  self.plotGraph2.getViewBox().enableAutoRange(axis = self.plotGraph2.getViewBox().YAxis, enable=True)
 
      def calculatePlotStatistics(self, targetGraph):
          '''
          Calculate Plot Statistics

          This function calculates statistical measures (mean, median, mode, and standard deviation) for the signal amplitudes 
          in the specified graph (Graph1 or Graph2) And makes a Table using a library called Reportlab-Platypus. The statistics are 
          calculated using a library usually from an array. These statistics are dynamically appended to the Table with each row 
          coressponding to a specific channel

          Lastly, the Table is styled with the preferred styling.


          Parameters:
          - self: The instance of the class where this method is defined.
          - targetGraph: An integer (0 for Graph1, 1 for Graph2) specifying the target graph for statistics calculation.

          Returns:
               A table containing the calculated statistics, suitable for presentation in a PDF report.
          '''
          
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
          
  
      def exportReportPdf(self, graphNumber):
          '''
          Export a PDF Report with an image of the plotgraph and statistics for the graph and its corresponding channels

          This function generates and exports a PDF report that includes key information about signal insights.
          The report comprises a title, the selected graph information, a captured plot, and a table of statistics.
          You can choose whether to generate the report for Graph1 or Graph2
          based on the `graphNumber` parameter which is passed by each export button.

          Parameters:
               - self: The instance of the class where this method is defined.
               - graphNumber: An integer (0 for Graph1, 1 for Graph2) indicating the target graph for the report.

          Returns:
              This function does not return any value
          '''

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
          pdf.drawImage(plotImg, 35, 500, width=550, height=400 / aspect_ratio)
          statistics_table = self.calculatePlotStatistics(graphNumber)
          statistics_table.wrapOn(pdf, 0, 0)
          statistics_table.drawOn(pdf, 60, 200)  
          QtWidgets.QMessageBox.information(self,"Report Created","Congrats, PDF is successfully created")
          pdf.save()

      def showAboutDialog(self):
               about_text = "Our project introduces a robust desktop application created with Python and Qt.\n\nTasked with developing a Multi-Port, Multi-Channel Signal Viewer, this software brings real-time data visualization to the forefront of intensive care units (ICUs) and beyond.\n\nWith features allowing users to load and simultaneously display various medical signals, customize the view, and even generate comprehensive reports, our application empowers healthcare professionals and signal analysis enthusiasts.\n\nExperience the future of signal monitoring with ease and precision through our innovative, user-friendly solution.\n\n Thank you for using our Application \n\n Our Team:\n Youssef Ashraf \n Mourad Magdy\n Ziad El Meligy \n Mariam Ahmed\n\n SBME 25"
               QMessageBox.about(self, "About", about_text)    
               self.about_clicked = True 



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
