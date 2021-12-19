# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simpleImageEditor.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import os
import sys
from tugce import openImage


class SimpleImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.source_image = None
        self.target_image = None
        self.setGeometry(0, 0, 1366, 768) #xpos, ypos, width, height
        self.setWindowTitle('Simple Image Editor')
        self.setStyleSheet("background-color: rgb(210, 210, 210);")
        self.centerOnScreen()
        self.setupUi()

    def centerOnScreen (self):
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        print(resolution.width())
        print(self.frameSize().height())
        self.move((resolution.width() // 2) - (self.frameSize().width() // 2),
                (resolution.height() // 2) - (self.frameSize().height() // 2))

    def setupUi(self):
        self.setObjectName("MainWindow")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QExampleLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 550, 620))
        self.label.move(50, 74)
        self.label.setText("Source Image")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setFont(QFont('Arial', 20))
        self.label.setStyleSheet("background-color: rgb(64, 64, 64);")
        self.sourcePixmap = None

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 550, 620))
        self.label_2.setText("Target Image")
        self.label_2.move(766, 74)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
       
        self.label.setFont(QFont('Arial', 20))
        self.label_2.setObjectName("label_2")
        self.targetPixmap = None
        self.label_2.setStyleSheet("background-color: rgb(64, 64, 64);")
        self.setCentralWidget(self.centralwidget)

        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setToolTip("Change Color Balance")
        self.button1.setGeometry(QtCore.QRect(0, 0, 100, 20))

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

     
        #crop part
        self.actionCrop = QtWidgets.QAction(self)
        self.actionCrop.setObjectName("actionCrop")
        self.actionCrop.triggered.connect(self.bastim)


 
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
    def bastim(self):
        return print('bastim')

    
    def browse_files(self):
        print(os.getcwd())
        fname = QFileDialog.getOpenFileName(self, "Open file", os.getcwd(), 'Images (*.png *.xmp *.jpg *.jpeg *.tiff *.gif)')
        self.sourcePixmap = QPixmap(fname[0])
        self.sourcePixmap = self.sourcePixmap.scaled(331*2, 291*2, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(self.sourcePixmap)




    def check_source_image(self):
        if isinstance(self.source_image, type(None)):
            self.show_popup('There is no source image')

    def show_popup(self, error_text):
        msg = QMessageBox()
        msg.setText(error_text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        
class QExampleLabel (QtWidgets.QLabel):
    def __init__(self, parentQWidget = None):
        super(QExampleLabel, self).__init__(parentQWidget)
    
        self.initUI()

    def initUI (self):
        self.setPixmap(QtGui.QPixmap('input.png'))

    def mousePressEvent (self, eventQMouseEvent):
        self.originQPoint = eventQMouseEvent.pos()
        self.currentQRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, QtCore.QSize()))
        self.currentQRubberBand.show()

    def mouseMoveEvent (self, eventQMouseEvent):
        self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())

    def mouseReleaseEvent (self, eventQMouseEvent):
        self.currentQRubberBand.hide()
        currentQRect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        print('burdayim:', currentQRect)

if __name__ == "__main__":
    

    app = QApplication(sys.argv)
    MainWindow = SimpleImageEditor()

    MainWindow.show()
    sys.exit(app.exec_())
