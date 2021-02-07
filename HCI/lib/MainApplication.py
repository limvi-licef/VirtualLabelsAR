# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainApplication.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
sys.path.append(os.getcwd()+"/lib")
from compiler import *
from ui.Ui_MainApplication import Ui_MainApplication
from lib.QtVideoPlayer import QtVideoPlayer
from lib.QtWindowsDevicePortal import QtWindowsDevicePortal

class MainApplication(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainApplication()
        self.ui.setupUi(self)



    #Action d'ouverture de la boite de dialogue pour parcourir dans les fichiers (Partie Image).
    def openImage(self):
        self.pathImg = QtWidgets.QFileDialog.getOpenFileName(self, 'Ouvrir une image', 'QDir.homePath()','Image Files(*.png *.jpg *.bmp)')
        print(self.pathImg[0])
        if self.pathImg[0]:
            self.ui.Img.setPixmap(QtGui.QPixmap(self.pathImg[0])) 
            

    #Action d'ouverture de la boite de dialogue pour parcourir dans les fichiers (Partie Video).
    def openVideo(self):
        self.pathVideo = QtWidgets.QFileDialog.getOpenFileName(self, 'Ouvrir une video', 'QDir.homePath()','Video Files(*.mov *.mp4 *.avi)')
        self.VideoPlayer = QtVideoPlayer(self.pathVideo[0])
        self.ui.VBoxVideo.addWidget(self.VideoPlayer)
        self.VideoPlayer.frameUpdate.connect(self.showFrame)

    #Méthode permettant de lancer la vidéo
    def showFrame(self, frame): 
        data, width, height = frame.tobytes(), frame.shape[1], frame.shape[0]
        image = QtGui.QImage(data, width, height, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(image)
        self.ui.LabelVideo.setPixmap(pixmap)
        self.ui.LabelVideo.setScaledContents(True)

    @staticmethod
    def test(config):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        GlobalFrame = MainApplication()
        GlobalFrame.show()
        sys.exit(app.exec_())

