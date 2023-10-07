# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beta.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1127, 777)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.GraphLayout1 = QtWidgets.QVBoxLayout()
        self.GraphLayout1.setObjectName("GraphLayout1")
        self.channelHeaderLayout1 = QtWidgets.QVBoxLayout()
        self.channelHeaderLayout1.setObjectName("channelHeaderLayout1")
        self.graphLabel1 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.graphLabel1.setFont(font)
        self.graphLabel1.setObjectName("graphLabel1")
        self.channelHeaderLayout1.addWidget(self.graphLabel1)
        self.ControlButtonsLayout1 = QtWidgets.QSplitter(self.centralwidget)
        self.ControlButtonsLayout1.setOrientation(QtCore.Qt.Horizontal)
        self.ControlButtonsLayout1.setObjectName("ControlButtonsLayout1")
        self.playPauseBtn1 = QtWidgets.QPushButton(self.ControlButtonsLayout1)
        self.playPauseBtn1.setEnabled(True)
        self.playPauseBtn1.setMaximumSize(QtCore.QSize(50, 16777215))
        self.playPauseBtn1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playPauseBtn1.setIcon(icon)
        self.playPauseBtn1.setObjectName("playPauseBtn1")
        self.zoomInBtn1 = QtWidgets.QPushButton(self.ControlButtonsLayout1)
        self.zoomInBtn1.setMaximumSize(QtCore.QSize(50, 16777215))
        self.zoomInBtn1.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomInBtn1.setIcon(icon1)
        self.zoomInBtn1.setObjectName("zoomInBtn1")
        self.zoomOutBtn1 = QtWidgets.QPushButton(self.ControlButtonsLayout1)
        self.zoomOutBtn1.setMaximumSize(QtCore.QSize(50, 16777215))
        self.zoomOutBtn1.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Images/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomOutBtn1.setIcon(icon2)
        self.zoomOutBtn1.setObjectName("zoomOutBtn1")
        self.rewindBtn1 = QtWidgets.QPushButton(self.ControlButtonsLayout1)
        self.rewindBtn1.setMaximumSize(QtCore.QSize(50, 16777215))
        self.rewindBtn1.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Images/rewind.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rewindBtn1.setIcon(icon3)
        self.rewindBtn1.setObjectName("rewindBtn1")
        self.channelHeaderLayout1.addWidget(self.ControlButtonsLayout1)
        self.GraphLayout1.addLayout(self.channelHeaderLayout1)
        spacerItem = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.GraphLayout1.addItem(spacerItem)
        self.plotGridLayout1 = QtWidgets.QGridLayout()
        self.plotGridLayout1.setObjectName("plotGridLayout1")
        self.yAxisScrollBar1 = QtWidgets.QScrollBar(self.centralwidget)
        self.yAxisScrollBar1.setOrientation(QtCore.Qt.Vertical)
        self.yAxisScrollBar1.setObjectName("yAxisScrollBar1")
        self.plotGridLayout1.addWidget(self.yAxisScrollBar1, 0, 1, 1, 1)
        self.plotGraph1 = PlotWidget(self.centralwidget)
        self.plotGraph1.setObjectName("plotGraph1")
        self.plotGridLayout1.addWidget(self.plotGraph1, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.plotGridLayout1.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.xAxisScrollBar1 = QtWidgets.QScrollBar(self.centralwidget)
        self.xAxisScrollBar1.setOrientation(QtCore.Qt.Horizontal)
        self.xAxisScrollBar1.setObjectName("xAxisScrollBar1")
        self.plotGridLayout1.addWidget(self.xAxisScrollBar1, 1, 0, 1, 2)
        self.GraphLayout1.addLayout(self.plotGridLayout1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.GraphLayout1.addWidget(self.label)
        self.graphControls1 = QtWidgets.QSplitter(self.centralwidget)
        self.graphControls1.setOrientation(QtCore.Qt.Vertical)
        self.graphControls1.setObjectName("graphControls1")
        self.splitter = QtWidgets.QSplitter(self.graphControls1)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.selectChannelLabel1 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.selectChannelLabel1.setFont(font)
        self.selectChannelLabel1.setObjectName("selectChannelLabel1")
        self.horizontalLayout.addWidget(self.selectChannelLabel1)
        self.channelList1 = QtWidgets.QComboBox(self.widget)
        self.channelList1.setObjectName("channelList1")
        self.channelList1.addItem("")
        self.channelList1.addItem("")
        self.channelList1.addItem("")
        self.horizontalLayout.addWidget(self.channelList1)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.selectColorBtn1 = QtWidgets.QPushButton(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.selectColorBtn1.setFont(font)
        self.selectColorBtn1.setObjectName("selectColorBtn1")
        self.horizontalLayout_2.addWidget(self.selectColorBtn1)
        self.checkBox1 = QtWidgets.QCheckBox(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox1.setFont(font)
        self.checkBox1.setObjectName("checkBox1")
        self.horizontalLayout_2.addWidget(self.checkBox1)
        self.widget2 = QtWidgets.QWidget(self.splitter)
        self.widget2.setObjectName("widget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.widget2)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.widget3 = QtWidgets.QWidget(self.splitter)
        self.widget3.setObjectName("widget3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.browseBtn1 = QtWidgets.QPushButton(self.widget3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.browseBtn1.setFont(font)
        self.browseBtn1.setObjectName("browseBtn1")
        self.verticalLayout.addWidget(self.browseBtn1)
        self.pushButton = QtWidgets.QPushButton(self.widget3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.GraphLayout1.addWidget(self.graphControls1)
        self.verticalLayout_2.addLayout(self.GraphLayout1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1127, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen = QtWidgets.QMenu(self.menuFile)
        self.menuOpen.setObjectName("menuOpen")
        self.menuGraph_1 = QtWidgets.QMenu(self.menuOpen)
        self.menuGraph_1.setObjectName("menuGraph_1")
        self.menuGraph_2 = QtWidgets.QMenu(self.menuOpen)
        self.menuGraph_2.setObjectName("menuGraph_2")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setShortcut("")
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionChannel_3 = QtWidgets.QAction(MainWindow)
        self.actionChannel_3.setObjectName("actionChannel_3")
        self.actionChannel_4 = QtWidgets.QAction(MainWindow)
        self.actionChannel_4.setObjectName("actionChannel_4")
        self.actionChannel_5 = QtWidgets.QAction(MainWindow)
        self.actionChannel_5.setObjectName("actionChannel_5")
        self.actionChannel_6 = QtWidgets.QAction(MainWindow)
        self.actionChannel_6.setObjectName("actionChannel_6")
        self.actionChannel_7 = QtWidgets.QAction(MainWindow)
        self.actionChannel_7.setObjectName("actionChannel_7")
        self.actionChannel_8 = QtWidgets.QAction(MainWindow)
        self.actionChannel_8.setObjectName("actionChannel_8")
        self.menuGraph_1.addAction(self.actionChannel_3)
        self.menuGraph_1.addAction(self.actionChannel_4)
        self.menuGraph_1.addAction(self.actionChannel_5)
        self.menuGraph_2.addAction(self.actionChannel_6)
        self.menuGraph_2.addAction(self.actionChannel_7)
        self.menuGraph_2.addAction(self.actionChannel_8)
        self.menuOpen.addAction(self.menuGraph_1.menuAction())
        self.menuOpen.addAction(self.menuGraph_2.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.menuOpen.menuAction())
        self.menuFile.addAction(self.actionSave_As)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.graphLabel1.setText(_translate("MainWindow", "Graph 1"))
        self.label.setText(_translate("MainWindow", "Graph 1 - Controls"))
        self.selectChannelLabel1.setText(_translate("MainWindow", "Select Channel:"))
        self.channelList1.setItemText(0, _translate("MainWindow", "Channel 1"))
        self.channelList1.setItemText(1, _translate("MainWindow", "Channel 2"))
        self.channelList1.setItemText(2, _translate("MainWindow", "Channel 3"))
        self.selectColorBtn1.setText(_translate("MainWindow", "Select Color"))
        self.checkBox1.setText(_translate("MainWindow", "Hide "))
        self.label_2.setText(_translate("MainWindow", "Edit channel name:"))
        self.browseBtn1.setText(_translate("MainWindow", "Browse file"))
        self.pushButton.setText(_translate("MainWindow", "Export"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOpen.setTitle(_translate("MainWindow", "Open"))
        self.menuGraph_1.setTitle(_translate("MainWindow", "Graph 1"))
        self.menuGraph_2.setTitle(_translate("MainWindow", "Graph 2"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSave_As.setText(_translate("MainWindow", "Exit"))
        self.actionChannel_3.setText(_translate("MainWindow", "Channel 1"))
        self.actionChannel_4.setText(_translate("MainWindow", "Channel 2"))
        self.actionChannel_5.setText(_translate("MainWindow", "Channel 3"))
        self.actionChannel_6.setText(_translate("MainWindow", "Channel 1"))
        self.actionChannel_7.setText(_translate("MainWindow", "Channel 2"))
        self.actionChannel_8.setText(_translate("MainWindow", "Channel 3"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
