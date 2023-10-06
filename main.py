
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

class MainWindow(QtWidgets.QMainWindow):

        # Mainwindow constructor
      def __init__(self, *args, **kwargs):
          super(MainWindow, self).__init__(*args, **kwargs)
          uic.loadUi('beta.ui', self)
          self.setWindowIcon(QtGui.QIcon('Images/MainIcon.png'))
          self.setWindowTitle("Realtime-signal-viewer")
          self.xAxis = [0,0,0]
          self.yAxis = [0,0,0]




      # browse function to open directory : a+m
      

      # open the file from directory : a+m


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
