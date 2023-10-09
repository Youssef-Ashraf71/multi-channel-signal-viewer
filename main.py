
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
          self.apply_stylesheet("Aqua.qss")

          self.xAxis = [0,0,0,0,0,0,0,0,0,0]
          self.yAxis = [0,0,0,0,0,0,0,0,0,0]
         # self.PlotterWindowProp = modules.PlotterWindow()
          self.pauseFlag1 = False
          self.holdHorizontalFlag1 = False
          self.holdVerticalFlag1 = False

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
            self.SignalChannelArr[modules.choosenChannel].path = path
            if self.SignalChannelArr[0].path == "null":
                    QtWidgets.QMessageBox.warning(self,"Channel 1 is Empty","Please use channel 1 first")
                    return
            self.SignalChannelArr[modules.choosenChannel].time =  timeArr
            self.SignalChannelArr[modules.choosenChannel].amplitude = amplitudeArr
            self.Legend = self.plotGraph1.addLegend()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.playPauseBtn1.setIcon(icon)
            self.signalInitialization()


      # initialize plotting: a+m
      def signalInitialization(self):
            self.SignalChannelArr[modules.choosenChannel].graph = self.plotGraph1.plot(
                 name="Channel "+str(modules.choosenChannel+1) ,
                 pen={'color': self.SignalChannelArr[modules.choosenChannel].getColor(), 'width': 1005}
            )
            self.plotGraph1.showGrid(x= True, y= True)
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
                            
            self.plotGraph1.plotItem.setLimits(
             xMin=minTime, xMax=maxTime, yMin=minAmp, yMax=maxAmp     
            )   
            # self.minAmp = minAmp
            # self.maxAmp = maxAmp
            self.minSignalAmp = len(self.SignalChannelArr[modules.choosenChannel].amplitude)
            self.pointsPlotted = 0
            self.startTime = QtCore.QTimer()
            self.startTime.setInterval(250)
            self.startTime.timeout.connect(self.signalPlotting)
            self.startTime.start()
  


      # draw plot: a+m
      def  signalPlotting(self):
           for channelIdx in range(len(self.SignalChannelArr)):
                if self.SignalChannelArr[channelIdx].path !="null":
                     self.xAxis[channelIdx] = self.SignalChannelArr[channelIdx].time[:self.pointsPlotted]
                     self.yAxis[channelIdx] = self.SignalChannelArr[channelIdx].amplitude[:self.pointsPlotted]
           
           self.pointsPlotted += 5
           if self.minSignalAmp < self.pointsPlotted:
                self.startTime.stop()

           for channelIdx in range(len(self.SignalChannelArr)):
                  if self.SignalChannelArr[channelIdx].path != "null":
                       if len(self.SignalChannelArr[channelIdx].time) > self.pointsPlotted:
                              # print(self.SignalChannelArr[channelIdx].getColor())
                               self.SignalChannelArr[channelIdx].graph.setData(self.xAxis[0], self.yAxis[channelIdx], pen=self.SignalChannelArr[channelIdx].getColor(), name="name") 

      # plot state show/hide : a+m
      def DynamicSignalUpdate(self):
           for Index in range(len(self.SignalChannelArr)):
               if self.SignalChannelArr[Index].path != "null" and len(self.SignalChannelArr[Index].time) > self.pointsPlotted:
                    if self.SignalChannelArr[Index].hiddenFlag == True:
                         self.SignalChannelArr[Index].graph.hide()
                    else:
                         self.SignalChannelArr[Index].graph.show()

                    self.SignalChannelArr[Index].graph.setData(
                         self.xAxis[0], self.yAxis[Index], pen=self.SignalChannelArr[Index].getColor(), name=self.SignalChannelArr[Index].label, skipFiniteCheck=True)
           

      # Zoom in Func  : Mask
      def zoomSignalIn(self):
          self.plotGraph1.plotItem.getViewBox().scaleBy((0.5, 0.5))
      # Zoom out Func : Mask
      def zoomSignalOut(self):
          self.plotGraph1.plotItem.getViewBox().scaleBy((2, 2))


      # edit the signal color : Mask
      def setSignalChannelColor(self):
           self.SignalChannelArr[modules.choosenChannel].setColor(QColorDialog.getColor().name())
           self.DynamicSignalUpdate()
      def addNewChannel(self):
            _translate = QtCore.QCoreApplication.translate
           # self.channelList1.setItemText(modules.choosenChannel+1, )
            self.channelList1.addItem(_translate("MainWindow", "Channel "+str(len(self.SignalChannelArr)+1)))
          #   modules.choosenChannel+=1
            self.SignalChannelArr.append(modules.SignalChannel())



      # play / pause func   : ziad
         # dont forget to change the icon 
      def pauseGraph(self):
           self.pauseFlag1 ^= True
           icon = QtGui.QIcon()
           if self.pauseFlag1 == True :
                icon.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.playPauseBtn1.setIcon(icon)
                self.startTime.stop()
           else: 
                 icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                 self.playPauseBtn1.setIcon(icon)
                 self.startTime.start() 



      # rewind 
      def rewindSignal(self):
           print("ana morad",self.SignalChannelArr[modules.choosenChannel].path)
           self.plotGraph1.clear()
           print("ana ashf",self.SignalChannelArr[modules.choosenChannel].path)
          # icon = QtGui.QIcon()
           #icon.addPixmap(QtGui.QPixmap("Images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
           #self.playPauseBtn1.setIcon(icon)
           for i in range(len(self.SignalChannelArr)):
                modules.choosenChannel = i
                print(self.SignalChannelArr[modules.choosenChannel].path,"iter:",i)
                self.signalInitialization()
  
      
      # show / hide function  : Mask
      def hideSignal(self,checked):
             self.SignalChannelArr[modules.choosenChannel].hiddenFlag = checked
             self.DynamicSignalUpdate()
      # speed slider function 

      # scroll in x dir

      # scroll in y dir 

      # naming the channel
      def editChannelName(self,name):
             # self.SignalChannelArr[modules.choosenChannel].label = name
             # self.Legend.getLabel(self.SignalChannelArr[modules.choosenChannel].graph).setText(name)
               channel_index = modules.choosenChannel
               self.SignalChannelArr[channel_index].label = name
               self.Legend.removeItem(self.SignalChannelArr[channel_index].graph)
               self.Legend.addItem(self.SignalChannelArr[channel_index].graph, name)


      # Link 2 channles sim

      def captureGraphImage(self):
      # Create an exporter to capture the graph
       exporter = exporters.ImageExporter(self.plotGraph1.scene())

      # Set the file suffix to specify the export type
       exporter.params.fileSuffix = 'png'

      # Set the filename
       export_filename = 'graph_capture.png'

          # Export the graph to the specified filename
       exporter.export(export_filename)



      def calculatePlotStatistics(self):
          
          #data
          amplitudes = []
          meanValues = []
          medianValues = []
          modeValues = []
          standardDeviations = []
          channelsNumbers = []
          channelLabels = []

          for Index in range(len(self.SignalChannelArr)):
               if (self.SignalChannelArr[Index].path != "null"):
                    amplitudes.append(self.SignalChannelArr[Index].amplitude)
                    channelsNumbers.append(Index)
                    channelLabels.append(self.SignalChannelArr[Index].label)

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

          for label, channel, mean, median, mode, std_dev in zip(
               channelLabels, channelsNumbers, meanValues, medianValues, modeValues, standardDeviations
          ):
               tableData.append([ label, channel+1, mean, median, mode, std_dev])


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
      def exportReportPdf(self):

          fileName = 'Report.pdf'
          documentTitle = 'Signal Insights Report'
          title = 'Signals Insights'          
          
          # Capture the plot and get the file path
          self.captureGraphImage()
          
          pdf = canvas.Canvas(fileName, pagesize=letter )
          
          pdf.setFont("Helvetica", 24)

          pdf.drawCentredString(290, 720, title)
          
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
          
          statistics_table = self.calculatePlotStatistics()
          statistics_table.wrapOn(pdf, 0, 0)
          statistics_table.drawOn(pdf, 60, 400)  # Adjust the position as needed
          
          pdf.save()



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
