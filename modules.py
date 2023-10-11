
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from PyQt5.QtWidgets import *

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
import main


choosenChannelGraph1 = 0
choosenChannelGraph2 = 0

def setChoosenChannel(self,index,graphIndex):
        global choosenChannelGraph1
        global choosenChannelGraph2
        if graphIndex == 0:
            choosenChannelGraph1 = index
            self.checkBox1.setChecked(self.SignalChannelArr[graphIndex][choosenChannelGraph1].hiddenFlag)
            self.lineEdit.clear()
        if graphIndex == 1:
              choosenChannelGraph2 = index    
              self.checkBox2.setChecked(self.SignalChannelArr[graphIndex][choosenChannelGraph2].hiddenFlag)
              self.lineEdit2.clear() 
 

class SignalChannel:
      def __init__(self,time = [] , amplitude = [] ,hiddenFlag = False , label="N/A", color= 0xffff00 , path="null"):
            self.graph = PlotWidget()
            self.time = time
            self.amplitude = amplitude
            self.hiddenFlag = hiddenFlag
            self.color = color
            self.label = label
            self.path = path
            
            
            
            
   #   def getChoosenSignal(self):
         #    return choosenChannel   
             
      def getColor(self):
             return self.color
      
      
      def setColor(self,color):
            old = self.color
            if color == "#000000":
                  self.color = old
            else:
                  self.color = color 

      def setData(self,time,amplitude,hiddenFlag, color, label, path):
            self.time = time
            self.amplitude = amplitude
            self.hiddenFlag = hiddenFlag
            self.color = color
            self.label = label
            self.path = path            


            

class PlotterWindow:
    def __init__(self, YAxisRange=(0, 1), XAxisRange=(-1, 1), CineSpeed=1.0):
        self.YAxisRange = YAxisRange  # Tuple containing min/max ranges
        self.XAxisRange = XAxisRange

        self.CineSpeed = 50

    def UpdateCineSpeed(self, Input):
        self.CineSpeed = (50) / (Input/100)
        #MainWindow.timer = QtCore.QTimer()
        # MainWindow.timer.setInterval(100*self.CineSpeed)
