
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


# ******NEW IMPORTS for the export function******
from PyQt5.QtGui import QPixmap
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Frame
from reportlab.lib.pagesizes import A4, landscape
import pyqtgraph.exporters as exporters
from PIL import Image




class MainWindow(QtWidgets.QMainWindow):

        # Mainwindow constructor
      def __init__(self, *args, **kwargs):
          super(MainWindow, self).__init__(*args, **kwargs)
          uic.loadUi('beta.ui', self)
          self.setWindowIcon(QtGui.QIcon('Images/MainIcon.png'))
          self.setWindowTitle("Realtime-signal-viewer")
         # Apply Aqya stylesheet
          self.apply_stylesheet("Aqua.qss")

          self.xAxis = [0,0,0]
          self.yAxis = [0,0,0]
         # self.PlotterWindowProp = modules.PlotterWindow()
          self.pauseFlag1 = False
          self.holdHorizontalFlag1 = False
          self.holdVerticalFlag1 = False

          self.SignalChannelArr = []
          for i in range(3):
               self.SignalChannelArr.append(modules.SignalChannel())

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
            self.signalInitialization()


      # initialize plotting: a+m
      def signalInitialization(self):
            self.SignalChannelArr[modules.choosenChannel].graph = self.plotGraph1.plot(
                 name="Channel "+str(modules.choosenChannel+1) ,
<<<<<<< Updated upstream
                 pen = self.SignalChannelArr[modules.choosenChannel].getColor(),
||||||| Stash base
                 pen = pg.mkPen(color= self.colorMap(float(modules.choosenChannel))),
=======
                 pen = pg.mkPen(color = 0),
>>>>>>> Stashed changes
            )
            self.plotGraph1.showGrid(x= True, y= True)
            maxTime,minTime,maxAmp,minAmp = 0,0,0,0
            for i in range(3):
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
           for channelIdx in range(3):
                if self.SignalChannelArr[channelIdx].path !="null":
                     self.xAxis[channelIdx] = self.SignalChannelArr[channelIdx].time[:self.pointsPlotted]
                     self.yAxis[channelIdx] = self.SignalChannelArr[channelIdx].amplitude[:self.pointsPlotted]
           
           self.pointsPlotted += 5
           if self.minSignalAmp < self.pointsPlotted:
                self.startTime.stop()

           for channelIdx in range(3):
                  if self.SignalChannelArr[channelIdx].path != "null":
                       if len(self.SignalChannelArr[channelIdx].time) > self.pointsPlotted:
                              # print(self.SignalChannelArr[channelIdx].getColor())
<<<<<<< Updated upstream
                               self.SignalChannelArr[channelIdx].graph.setData(self.xAxis[0], self.yAxis[channelIdx], pen=self.SignalChannelArr[channelIdx].getColor(), name="name") 
||||||| Stash base
                               self.SignalChannelArr[channelIdx].graph.setData(self.xAxis[0], self.yAxis[channelIdx],  pen = pg.mkPen(color= self.colorMap(float(modules.choosenChannel)))) 
=======
                               self.SignalChannelArr[channelIdx].graph.setData(self.xAxis[0], self.yAxis[channelIdx],  pen = pg.mkPen(color = 1)) 
>>>>>>> Stashed changes

      # plot state show/hide : a+m
      def DynamicSignalUpdate(self):
           for Index in range(3):
               if self.SignalChannelArr[Index].path != "null" and len(self.SignalChannelArr[Index].time) > self.pointsPlotted:
                    if self.SignalChannelArr[Index].hiddenFlag == True:
                         self.SignalChannelArr[Index].graph.hide()
                    else:
                         self.SignalChannelArr[Index].graph.show()

                    self.SignalChannelArr[Index].graph.setData(
                         self.xAxis[0], self.yAxis[Index], pen=self.SignalChannelArr[Index].getColor(), name=self.SignalChannelArr[Index].label, skipFiniteCheck=True)
           

      # Zoom in Func  : Mask


      # Zoom out Func : Mask

      # edit the signal color : Mask
      def setSignalChannelColor(self):
           self.SignalChannelArr[modules.choosenChannel].setColor(QColorDialog.getColor().name())
           self.DynamicSignalUpdate()
<<<<<<< Updated upstream
||||||| Stash base

      def colorMap(self,float):
           # making up a set of different colors, so that each new graph will be assigned a color
            numberOfColors = 50
            #creating a color map (rainbow) with 50 colors
            colorsMap = cm.rainbow(np.linspace(0, 1, numberOfColors))
            #get a color based on the channel of the signal
            colorOfSignal = colorsMap[modules.choosenChannel % numberOfColors]
            return colorOfSignal   


      
=======

      def colorMap(self,float):
           # making up a set of different colors, so that each new graph will be assigned a color
            numberOfColors = 10
            #creating a color map (rainbow) with 50 colors
            colorsMap = cm.rainbow(np.linspace(0, 1, numberOfColors))
            #get a color based on the channel of the signal
            colorOfSignal = colorsMap[float(modules.choosenChannel+1 % numberOfColors)]
            return colorOfSignal   


      
>>>>>>> Stashed changes
      # play / pause func   : ziad
         # dont forget to change the icon 
      def pauseGraph(self):
           self.pauseFlag1 ^= True
           if self.pauseFlag1 == True :
                self.startTime.stop()
           else: 
                 self.startTime.start()     
      # show / hide function  : Mask
      def hideSignal(self,checked):
             self.SignalChannelArr[modules.choosenChannel].hiddenFlag = checked
             self.DynamicSignalUpdate()
      # speed slider function 

      # scroll in x dir

      # scroll in y dir 

      # naming the channel


      # Link 2 channles sim


      # rewind 
      


     #  # graph screenshot
     #  def capturePlot(self):
     #      # Create a QPixmap to capture the plot
     #      plot_pixmap = QPixmap(self.plotGraph1.size())
     #      self.plotGraph1.render(plot_pixmap)

     #      # Get the directory where the script is located
     #      script_dir = os.path.dirname(__file__)
          
     #      # Specify the path to save the captured plot in the script's directory
     #      file_path = os.path.join(script_dir, 'captured_plot.png')
     #      plot_pixmap.save(file_path, 'PNG')
     #      return file_path  # Return the file path of the captured plot
          
    
      def captureGraphImage(self):
      # Create an exporter to capture the graph
       exporter = exporters.ImageExporter(self.plotGraph1.scene())

      # Set the file suffix to specify the export type (e.g., 'png')
       exporter.params.fileSuffix = 'png'

      # Set the filename
       export_filename = 'graph_capture.png'

      # Export the graph to the specified filename
       exporter.export(export_filename)

  
  
     # export the report to pdf
      def exportReportPdf(self):

          # setting up the pdf           
          fileName = 'Report.pdf'
          documentTitle = 'Report'
          title = 'Signals Insights'

          pdf = canvas.Canvas(fileName, pagesize=letter)
          pdf.setTitle(documentTitle)

          # Title and Set the font and font size
          pdf.setFont("Helvetica", 24)

          pdf.drawCentredString(290, 720, title)

          # creating a frame using platypus
          padding = dict(
          leftPadding=72,
          rightPadding=72,
          topPadding=72,
          bottomPadding=18)

          # Add an logos to the PDF
          majorLogo = ImageReader('./Images/logo-major.png')
          pdf.drawImage(majorLogo, 10, 725, 112, 45 )
          collegeLogo = ImageReader('./Images/collegeLogo.jpg')
          pdf.drawImage(collegeLogo, 525, 705, 70, 70 )

          # Capture the plot and get the file path
          self.captureGraphImage()

          # editing the image size and it's position on the report
          
          # Open the image file
          image = Image.open('graph_capture.png')

          # Get the size (width and height) of the image
          image_width, image_height = image.size

          aspect_ratio = image_width / image_height

          # Close the image file (optional, but recommended)
          image.close()

          print(f'Image width: {image_width}, Image height: {image_height}')

          pdf.drawImage('graph_capture.png', 35, 500 , 550, 550/aspect_ratio )


          pdf.save()

          
          

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
