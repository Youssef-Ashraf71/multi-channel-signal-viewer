
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from PyQt5.QtWidgets import *


import pandas as pd
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import csv
import os

import wfdb
import main


choosenChannelGraph1 = 0
choosenChannelGraph2 = 0

def setChoosenChannel(self,index,graphIndex):
        global choosenChannelGraph1
        global choosenChannelGraph2
        if graphIndex == 0:
            choosenChannelGraph1 = index
            if choosenChannelGraph1 < 0 or choosenChannelGraph1 > len(self.SignalChannelArr[graphIndex])-1:
                  return
            self.checkBox1.setChecked(self.SignalChannelArr[graphIndex][choosenChannelGraph1].hiddenFlag)
            self.lineEdit.clear()
        if graphIndex == 1:
              choosenChannelGraph2 = index    
              if choosenChannelGraph2 < 0 or choosenChannelGraph2 > len(self.SignalChannelArr[graphIndex])-1:
                  return
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


            

