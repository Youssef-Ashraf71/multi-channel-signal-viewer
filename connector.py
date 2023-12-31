from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSlider, QTextEdit, QFileDialog, QScrollBar, QComboBox, QCheckBox, QScrollBar, QLCDNumber, QLineEdit , QMenu , QAction
from pyqtgraph import PlotWidget


import main
import modules


def __init__connectors__(self):

#---------------------------------------------------------------------------------------
      # Graph 1
      self.browseBtn1.clicked.connect(lambda:(self.browse(self.plotGraph1,0)))

      self.channelList1 = self.findChild(QComboBox, "channelList1")
      self.channelList1.currentIndexChanged.connect(lambda:modules.setChoosenChannel(self,self.channelList1.currentIndex(),0 ))

      self.checkBox1 = self.findChild(QCheckBox,"checkBox1")
      self.checkBox1.setChecked(True);
      self.checkBox1.stateChanged.connect(lambda: main.MainWindow.hideSignal(self,self.checkBox1.isChecked(),0))

      self.selectColorBtn1 = self.findChild(QPushButton,"selectColorBtn1")
      self.selectColorBtn1.clicked.connect(lambda:main.MainWindow.setSignalChannelColor(self,0))

      self.playPauseBtn1 = self.findChild(QPushButton,"playPauseBtn1")
      self.playPauseBtn1.clicked.connect(lambda:main.MainWindow.pauseGraph(self,self.playPauseBtn1,0))

      self.rewindBtn1 = self.findChild(QPushButton,"rewindBtn1")
      self.rewindBtn1.clicked.connect(lambda:main.MainWindow.rewindSignal(self,self.plotGraph1,0))

      self.zoomInBtn1 = self.findChild(QPushButton,"zoomInBtn1")
      self.zoomInBtn1.clicked.connect(lambda:main.MainWindow.zoomSignalIn(self,self.plotGraph1))
      self.zoomOutBtn1 = self.findChild(QPushButton,"zoomOutBtn1")
      self.zoomOutBtn1.clicked.connect(lambda:main.MainWindow.zoomSignalOut(self,self.plotGraph1))

      self.lineEdit = self.findChild(QLineEdit,"lineEdit")
      self.lineEdit.returnPressed.connect(lambda:main.MainWindow.editChannelName(self,self.lineEdit.text(),0))

      # temp using export btn to add more channels
      self.pushButton = self.findChild(QPushButton,"pushButton")
      self.pushButton.clicked.connect(lambda:main.MainWindow.addNewChannel(self,self.channelList1,0))

      self.horizontalSlider = self.findChild(QSlider,"horizontalSlider")
      self.horizontalSlider.sliderReleased.connect(lambda:main.MainWindow.speedSlider(self,0))

      
# ------------------------------------------------------------------------------------------------------------
# Graph2 
      self.browseBtn2.clicked.connect(lambda:(self.browse(self.plotGraph2,1)))

      self.channelList2 = self.findChild(QComboBox, "channelList2")
      self.channelList2.currentIndexChanged.connect(lambda:modules.setChoosenChannel(self,self.channelList2.currentIndex(),1))

      self.graphIndex = self.findChild(QCheckBox,"checkBox2")
      self.checkBox2.setChecked(True);
      self.checkBox2.stateChanged.connect(lambda: main.MainWindow.hideSignal(self,self.checkBox2.isChecked(),1))

      self.selectColorBtn2 = self.findChild(QPushButton,"selectColorBtn2")
      self.selectColorBtn2.clicked.connect(lambda:main.MainWindow.setSignalChannelColor(self,1))

      self.playPauseBtn2 = self.findChild(QPushButton,"playPauseBtn2")
      self.playPauseBtn2.clicked.connect(lambda:main.MainWindow.pauseGraph(self,self.playPauseBtn2,1))

      self.rewindBtn2 = self.findChild(QPushButton,"rewindBtn2")
      self.rewindBtn2.clicked.connect(lambda:main.MainWindow.rewindSignal(self,self.plotGraph2,1))

      self.zoomInBtn2 = self.findChild(QPushButton,"zoomInBtn2")
      self.zoomInBtn2.clicked.connect(lambda:main.MainWindow.zoomSignalIn(self,self.plotGraph2))
      self.zoomOutBtn2 = self.findChild(QPushButton,"zoomOutBtn2")
      self.zoomOutBtn2.clicked.connect(lambda:main.MainWindow.zoomSignalOut(self,self.plotGraph2))

      self.lineEdit2 = self.findChild(QLineEdit,"lineEdit2")
      self.lineEdit2.returnPressed.connect(lambda:main.MainWindow.editChannelName(self,self.lineEdit2.text(),1))

      self.addNewChannel2 = self.findChild(QPushButton,"addNewChannel2")
      self.addNewChannel2.clicked.connect(lambda:main.MainWindow.addNewChannel(self,self.channelList2,1))

      self.speedSlider2 = self.findChild(QSlider,"speedSlider2")
      self.speedSlider2.sliderReleased.connect(lambda:main.MainWindow.speedSlider(self,1))


# ------------------------------------------------------------------------------------------------------------
# Link
      self.linkGraphsButton = self.findChild(QPushButton, "linkGraphsButton")
      self.linkGraphsButton.clicked.connect(lambda:main.MainWindow.linkGraphs(self))

      self.playPauseLinkBtn = self.findChild(QPushButton,"playPauseLinkBtn")
      self.playPauseLinkBtn.clicked.connect(lambda:main.MainWindow.playPauseLink(self,self.playPauseLinkBtn,self.playPauseBtn1,self.playPauseBtn2))

      self.zoomInLinkBtn = self.findChild(QPushButton,"zoomInLinkBtn")
      self.zoomInLinkBtn.clicked.connect(lambda:main.MainWindow.zoomInLink(self,self.plotGraph1,self.plotGraph2))

      self.zoomOutLinkBtn = self.findChild(QPushButton,"zoomOutLinkBtn")
      self.zoomOutLinkBtn.clicked.connect(lambda:main.MainWindow.zoomOutLink(self,self.plotGraph1,self.plotGraph2))

      self.rewindLinkBtn = self.findChild(QPushButton,"rewindLinkBtn")
      self.rewindLinkBtn.clicked.connect(lambda:main.MainWindow.rewindLink(self,self.plotGraph1,self.plotGraph2))

      self.exportButton1 = self.findChild(QPushButton, "exportButton1")
      self.exportButton1.clicked.connect(lambda:main.MainWindow.captureGraphImage(self, 0))

      self.exportButton2 = self.findChild(QPushButton, "exportButton2")
      self.exportButton2.clicked.connect(lambda:main.MainWindow.captureGraphImage(self, 1))



#---------------------------------------------------------------------------------------
# Plot Widgets
      self.plotGraph1=self.findChild(PlotWidget,'plotGraph1')
      self.plotGraph2=self.findChild(PlotWidget,'plotGraph2')


#---------------------------------------------------------------------------------------
# Export Buttons
      self.moveToGraph2 = self.findChild(QPushButton,"moveToGraph2")
      self.moveToGraph2.clicked.connect(lambda:main.MainWindow.moveSignal(self,0))
      self.moveToGraph1 = self.findChild(QPushButton,"moveToGraph1")
      self.moveToGraph1.clicked.connect(lambda:main.MainWindow.moveSignal(self,1))
      self.exportReportButton = self.findChild(QPushButton,"exportReportButton")
      self.exportReportButton.clicked.connect(lambda:main.MainWindow.exportReportPdf(self,0))


#---------------------------------------------------------------------------------------
# About Section
      self.menuAbout = self.findChild(QMenu, "menuAbout")
      aboutAction = QAction("About this Application", self)
      aboutAction.triggered.connect(lambda: main.MainWindow.showAboutDialog(self))
      self.menuAbout.addAction(aboutAction)