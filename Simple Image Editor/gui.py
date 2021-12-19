from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QPushButton
import os
import sys
from filters import *

class SimpleImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.source_image = None
        self.target_image = None
        self.setGeometry(0, 0, 1366, 768) #xpos, ypos, width, height
        self.setWindowTitle('Simple Image Editor')
        self.setStyleSheet("background-color: rgb(210, 210, 210);")
        self.setStyleSheet("")

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

        self.sourceImageLabel = CroppedImageLabel(self.centralwidget)
        self.sourceImageLabel.setGeometry(QtCore.QRect(0, 0, 550, 620))
        self.sourceImageLabel.move(50, 74)
        self.sourceImageLabel.setObjectName("sourceImageLabel")
        self.sourceImageLabel.setStyleSheet("background-color: rgb(64, 64, 64);")
        self.sourcePixmap = None

        self.targetImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.targetImageLabel.setGeometry(QtCore.QRect(0, 0, 550, 620))
        self.targetImageLabel.move(766, 74)
        self.targetImageLabel.setObjectName("targetImageLabel")
        self.targetImagePixmap = None
        self.targetImageLabel.setStyleSheet("background-color: rgb(64, 64, 64);")
        self.setCentralWidget(self.centralwidget)

        self.blurImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.blurImageButton.setToolTip("Open Image")
        self.blurImageButton.setGeometry(QtCore.QRect(246, 34, 158, 30))
        self.blurImageButton.setText("Open Image")
        self.blurImageButton.clicked.connect(self.browseFiles)

        self.blurImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.blurImageButton.setToolTip("Save Image")
        self.blurImageButton.setGeometry(QtCore.QRect(962, 34, 158, 30))
        self.blurImageButton.setText("Save Image")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Blur")
        self.openImage.setGeometry(QtCore.QRect(605, 74, 158, 30))
        self.openImage.setText("Blur")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Deblur")
        self.openImage.setGeometry(QtCore.QRect(605, 119, 158, 30))
        self.openImage.setText("Deblur")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Grayscale")
        self.openImage.setGeometry(QtCore.QRect(605, 164, 158, 30))
        self.openImage.setText("Grayscale")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Crop")
        self.openImage.setGeometry(QtCore.QRect(605, 209, 158, 30))
        self.openImage.setText("Crop")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Flip")
        self.openImage.setGeometry(QtCore.QRect(605, 254, 158, 30))
        self.openImage.setText("Flip")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Mirror")
        self.openImage.setGeometry(QtCore.QRect(605, 299, 158, 30))
        self.openImage.setText("Mirror")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Rotate")
        self.openImage.setGeometry(QtCore.QRect(605, 344, 158, 30))
        self.openImage.setText("Rotate")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Reverse the Color")
        self.openImage.setGeometry(QtCore.QRect(605, 389, 158, 30))
        self.openImage.setText("Reverse the Color")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Change Color Balance")
        self.openImage.setGeometry(QtCore.QRect(605, 434, 158, 30))
        self.openImage.setText("Change Color Balance")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Adjust Brightness")
        self.openImage.setGeometry(QtCore.QRect(605, 479, 158, 30))
        self.openImage.setText("Adjust Brightness")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Adjust Contrast")
        self.openImage.setGeometry(QtCore.QRect(605, 524, 158, 30))
        self.openImage.setText("Adjust Contrast")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Adjust Saturation")
        self.openImage.setGeometry(QtCore.QRect(605, 569, 158, 30))
        self.openImage.setText("Adjust Saturation")
        
        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Add Noise")
        self.openImage.setGeometry(QtCore.QRect(605, 614, 158, 30))
        self.openImage.setText("Add Noise")

        self.openImage = QtWidgets.QPushButton(self.centralwidget)
        self.openImage.setToolTip("Detect Edges")
        self.openImage.setGeometry(QtCore.QRect(605, 659, 158, 30))
        self.openImage.setText("Detect Edges")
        
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        #crop part

        # self.actionCrop.triggered.connect(self.bastim)

        QtCore.QMetaObject.connectSlotsByName(self)


    def browseFiles(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", os.getcwd(), 'Images (*.png *.xmp *.jpg *.jpeg *.tiff *.gif)')
        self.sourceImagePixmap =  QtGui.QPixmap(fname[0])
        self.sourceImagePixmap = self.sourceImagePixmap.scaled(550, 620, QtCore.Qt.KeepAspectRatio)
        self.sourceImageLabel.setPixmap(self.sourceImagePixmap)

    def checkSourceImage(self):
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

        
class CroppedImageLabel (QtWidgets.QLabel):
    def __init__(self, parentQWidget = None):
        super(CroppedImageLabel, self).__init__(parentQWidget)
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