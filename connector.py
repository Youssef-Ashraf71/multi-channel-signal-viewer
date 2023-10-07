from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSlider, QTextEdit, QFileDialog, QScrollBar, QComboBox, QCheckBox, QScrollBar, QLCDNumber, QLineEdit

import main
import modules


def __init__connectors__(self):
      self.browseBtn1.clicked.connect(self.browse)

      self.channelList1 = self.findChild(QComboBox, "channelList1")
      self.channelList1.currentIndexChanged.connect(lambda:modules.setChoosenChannel(self.channelList1.currentIndex()))

      self.checkbox1 = self.findChild(QCheckBox,"checkBox1")
      self.checkbox1.stateChanged.connect(lambda: main.MainWindow.hideSignal(self,self.checkbox1.isChecked()))

      self.selectColorBtn1 = self.findChild(QPushButton,"selectColorBtn1")
      self.selectColorBtn1.clicked.connect(lambda:main.MainWindow.setSignalChannelColor(self))

      self.playPauseBtn1 = self.findChild(QPushButton,"playPauseBtn1")
      self.playPauseBtn1.clicked.connect(lambda:main.MainWindow.pauseGraph(self))

      self.pushButton = self.findChild(QPushButton,"pushButton")
      self.pushButton.clicked.connect(lambda: main.MainWindow.exportReportPdf(self))