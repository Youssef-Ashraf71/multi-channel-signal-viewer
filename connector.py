from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSlider, QTextEdit, QFileDialog, QScrollBar, QComboBox, QCheckBox, QScrollBar, QLCDNumber, QLineEdit

import main
import modules


def __init__connectors__(self):
      self.browseBtn1.clicked.connect(self.browse)

      self.channelList1 = self.findChild(QComboBox, "channelList1")
      self.channelList1.currentIndexChanged.connect(lambda:modules.setChoosenChannel(self.channelList1.currentIndex(), self))

      self.checkBox1 = self.findChild(QCheckBox,"checkBox1")
      self.checkBox1.stateChanged.connect(lambda: main.MainWindow.hideSignal(self,self.checkBox1.isChecked()))

      self.selectColorBtn1 = self.findChild(QPushButton,"selectColorBtn1")
      self.selectColorBtn1.clicked.connect(lambda:main.MainWindow.setSignalChannelColor(self))

      self.playPauseBtn1 = self.findChild(QPushButton,"playPauseBtn1")
      self.playPauseBtn1.clicked.connect(lambda:main.MainWindow.pauseGraph(self))

      self.rewindBtn1 = self.findChild(QPushButton,"rewindBtn1")
      self.rewindBtn1.clicked.connect(lambda:main.MainWindow.rewindSignal(self))

      self.zoomInBtn1 = self.findChild(QPushButton,"zoomInBtn1")
      self.zoomInBtn1.clicked.connect(lambda:main.MainWindow.zoomSignalIn(self))
      self.zoomOutBtn1 = self.findChild(QPushButton,"zoomOutBtn1")
      self.zoomOutBtn1.clicked.connect(lambda:main.MainWindow.zoomSignalOut(self))

      self.lineEdit = self.findChild(QLineEdit,"lineEdit")
      self.lineEdit.returnPressed.connect(lambda:main.MainWindow.editChannelName(self,self.lineEdit.text()))
# temp using export btn to add more channels
      self.pushButton = self.findChild(QPushButton,"pushButton")
      self.pushButton.clicked.connect(lambda:main.MainWindow.addNewChannel(self))

      # the actual export button >:(
      self.reportBtn = self.findChild(QPushButton,"reportBtn")
      self.reportBtn.clicked.connect(lambda: main.MainWindow.exportReportPdf(self))