from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSlider, QTextEdit, QFileDialog, QScrollBar, QComboBox, QCheckBox, QScrollBar, QLCDNumber, QLineEdit

import main
import modules


def __init__connectors__(self):

      # Graph 1
      self.browseBtn1.clicked.connect(lambda:(self.browse(self.plotGraph1,0)))

      self.channelList1 = self.findChild(QComboBox, "channelList1")
      self.channelList1.currentIndexChanged.connect(lambda:modules.setChoosenChannel(self.channelList1.currentIndex(), self))

      self.checkBox1 = self.findChild(QCheckBox,"checkBox1")
      self.checkBox1.stateChanged.connect(lambda: main.MainWindow.hideSignal(self,self.checkBox1.isChecked(),0))

      self.selectColorBtn1 = self.findChild(QPushButton,"selectColorBtn1")
      self.selectColorBtn1.clicked.connect(lambda:main.MainWindow.setSignalChannelColor(self,0))

      self.playPauseBtn1 = self.findChild(QPushButton,"playPauseBtn1")
      self.playPauseBtn1.clicked.connect(lambda:main.MainWindow.pauseGraph(self,self.playPauseBtn1,0))

      self.rewindBtn1 = self.findChild(QPushButton,"rewindBtn1")
      self.rewindBtn1.clicked.connect(lambda:main.MainWindow.rewindSignal(self,self.plotGraph1))

      self.zoomInBtn1 = self.findChild(QPushButton,"zoomInBtn1")
      self.zoomInBtn1.clicked.connect(lambda:main.MainWindow.zoomSignalIn(self,self.plotGraph1))
      self.zoomOutBtn1 = self.findChild(QPushButton,"zoomOutBtn1")
      self.zoomOutBtn1.clicked.connect(lambda:main.MainWindow.zoomSignalOut(self,self.plotGraph1))

      self.lineEdit = self.findChild(QLineEdit,"lineEdit")
      self.lineEdit.returnPressed.connect(lambda:main.MainWindow.editChannelName(self,self.lineEdit.text(),0))

      # temp using export btn to add more channels
      self.pushButton = self.findChild(QPushButton,"pushButton")
      self.pushButton.clicked.connect(lambda:main.MainWindow.addNewChannel(self,self.channelList1))

      self.horizontalSlider = self.findChild(QSlider,"horizontalSlider")
      self.horizontalSlider.sliderReleased.connect(lambda:main.MainWindow.speedSlider(self))

      self.xAxisScrollBar1 = self.findChild(QScrollBar, "xAxisScrollBar1")
      self.xAxisScrollBar1.sliderMoved.connect(lambda: main.MainWindow.xScrollMove(self))

      self.yAxisScrollBar1 = self.findChild(QScrollBar, "yAxisScrollBar1")
      self.yAxisScrollBar1.sliderMoved.connect(lambda: main.MainWindow.yScrollMove(self))

# ------------------------------------------------------------------------------------------------------------
# Graph2 
      self.browseBtn2.clicked.connect(lambda:(self.browse(self.plotGraph2,1)))

      self.channelList2 = self.findChild(QComboBox, "channelList2")
      self.channelList2.currentIndexChanged.connect(lambda:modules.setChoosenChannel(self.channelList2.currentIndex(), self))

      self.checkBox2 = self.findChild(QCheckBox,"checkBox2")
      self.checkBox2.stateChanged.connect(lambda: main.MainWindow.hideSignal(self,self.checkBox2.isChecked(),1))

      self.selectColorBtn2 = self.findChild(QPushButton,"selectColorBtn2")
      self.selectColorBtn2.clicked.connect(lambda:main.MainWindow.setSignalChannelColor(self,1))

      self.playPauseBtn2 = self.findChild(QPushButton,"playPauseBtn2")
      self.playPauseBtn2.clicked.connect(lambda:main.MainWindow.pauseGraph(self,self.playPauseBtn2,1))

      self.rewindBtn2 = self.findChild(QPushButton,"rewindBtn2")
      self.rewindBtn2.clicked.connect(lambda:main.MainWindow.rewindSignal(self,self.plotGraph2))

      self.zoomInBtn2 = self.findChild(QPushButton,"zoomInBtn2")
      self.zoomInBtn2.clicked.connect(lambda:main.MainWindow.zoomSignalIn(self,self.plotGraph2))
      self.zoomOutBtn2 = self.findChild(QPushButton,"zoomOutBtn2")
      self.zoomOutBtn2.clicked.connect(lambda:main.MainWindow.zoomSignalOut(self,self.plotGraph2))

      self.lineEdit2 = self.findChild(QLineEdit,"lineEdit2")
      self.lineEdit2.returnPressed.connect(lambda:main.MainWindow.editChannelName(self,self.lineEdit2.text(),1))

      self.addNewChannel2 = self.findChild(QPushButton,"addNewChannel2")
      self.addNewChannel2.clicked.connect(lambda:main.MainWindow.addNewChannel(self,self.channelList2))

      self.speedSlider2 = self.findChild(QSlider,"speedSlider2")
      self.speedSlider2.sliderReleased.connect(lambda:main.MainWindow.speedSlider(self))

      self.xAxisScrollBar2 = self.findChild(QScrollBar, "xAxisScrollBar1")
      self.xAxisScrollBar2.sliderMoved.connect(lambda: main.MainWindow.xScrollMove(self))

      self.yAxisScrollBar2 = self.findChild(QScrollBar, "yAxisScrollBar1")
      self.yAxisScrollBar2.sliderMoved.connect(lambda: main.MainWindow.yScrollMove(self))

