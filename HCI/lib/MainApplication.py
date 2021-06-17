# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainApplication.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from json import loads
from ui.Ui_MainApplication import Ui_MainApplication
from lib.QtVideoPlayer import QtVideoPlayer
from lib.QtWindowsDevicePortal import QtWindowsDevicePortal
from lib.QtRecordSession import QtRecordSession
from lib.LabelManager import LabelManager
from lib.QtLabelManager import QtLabelManager
from lib.QtRecordViewer import QtRecordViewer
from lib.GlFrameDisplayer import GlFrameDisplayer
from lib.LabelObject import LabelObject
from lib.MeshObject import MeshObject

class MainApplication(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        
        QtWidgets.QMainWindow.__init__(self, parent)
        
        self.ui = Ui_MainApplication()
        self.ui.setupUi(self)
        
        self.mainWidget = None
        
        self.layout = QtWidgets.QVBoxLayout()
        self.ui.main.setLayout(self.layout)
        
        
    def new(self):
        
        print("new")
        if self.mainWidget: self.mainWidget.deleteLater()
        self.mainWidget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        self.ui.LogoSherbrooke.setVisible(False)
        self.ui.LogoGphy.setVisible(False)

        wdp = QtWindowsDevicePortal()
        layout.addWidget(wdp)
        
        recordSession = QtRecordSession()
        recordSession.setWdp(wdp)
        layout.addWidget(recordSession)
        print(recordSession)
        
        self.mainWidget.setLayout(layout)
        self.layout.addWidget(self.mainWidget)
        
    
        
    def open(self):
        
        print("open")
        self.ui.LogoSherbrooke.setVisible(False)
        
        file, _ = QtWidgets.QFileDialog.getOpenFileName()
        
        with open(file, mode="r") as datafile:
            data = loads(datafile.read())
            
        if self.mainWidget: self.mainWidget.deleteLater()
        self.mainWidget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        self.mainWidget.setLayout(layout)

        container1 = QtWidgets.QWidget()
        container1.layout = QtWidgets.QVBoxLayout()
        container1.setLayout(container1.layout)
        qtVideoPlayer = QtVideoPlayer(data["video"])
        qtLabelManager = QtLabelManager(self)

        width, height = qtVideoPlayer.core.WIDTH, qtVideoPlayer.core.HEIGHT
        args = ((width, height), data, qtLabelManager.manager)

        print(data["video"])
        print(str(width) + " " + str(height))

        rv = QtRecordViewer(args)
   
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        rv.setSizePolicy(sizePolicy)
        qtVideoPlayer.frameUpdate.connect(rv.receive)
        container1.layout.addWidget(rv)
        container1.layout.addWidget(qtVideoPlayer)
        layout.addWidget(container1)


        container2 = QtWidgets.QWidget()
        container2.layout = QtWidgets.QVBoxLayout()
        container2.setLayout(container2.layout)
   
        qtLabelManager.canvas = rv
        print(qtLabelManager.canvas)
    
        container2.layout.addWidget(qtLabelManager)
        layout.addWidget(container2)
        
        self.mainWidget.setLayout(layout)
        self.layout.addWidget(self.mainWidget)
    
        
    def exit(self):
        
        print("exit")
        QtCore.QCoreApplication.instance().quit()



    #Action d'ouverture de la boite de dialogue pour parcourir dans les fichiers (Partie Image).
    # def openImage(self):
    #     self.pathImg = QtWidgets.QFileDialog.getOpenFileName(self, 'Ouvrir une image', 'QDir.homePath()','Image Files(*.png *.jpg *.bmp)')
    #     print(self.pathImg[0])
    #     if self.pathImg[0]:
    #         self.ui.Img.setPixmap(QtGui.QPixmap(self.pathImg[0])) 
            

    # #Action d'ouverture de la boite de dialogue pour parcourir dans les fichiers (Partie Video).
    # def openVideo(self):
    #     self.pathVideo = QtWidgets.QFileDialog.getOpenFileName(self, 'Ouvrir une video', 'QDir.homePath()','Video Files(*.mov *.mp4 *.avi)')
    #     self.VideoPlayer = QtVideoPlayer(self.pathVideo[0])
    #     self.ui.VBoxVideo.addWidget(self.VideoPlayer)
    #     self.VideoPlayer.frameUpdate.connect(self.showFrame)

    # #Méthode permettant de lancer la vidéo
    # def showFrame(self, frame): 
    #     data, width, height = frame.tobytes(), frame.shape[1], frame.shape[0]
    #     image = QtGui.QImage(data, width, height, QtGui.QImage.Format_BGR888)
    #     pixmap = QtGui.QPixmap(image)
    #     self.ui.LabelVideo.setPixmap(pixmap)
    #     self.ui.LabelVideo.setScaledContents(True)

    @staticmethod
    def run(config):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        GlobalFrame = MainApplication()
        GlobalFrame.show()
        sys.exit(app.exec_())
        
        
if __name__ == "__main__":
    
    from config import *
    from compiler import *
    
    GlFrameDisplayer.SHADERS = CONFIG["shaders"]
    MeshObject.SHADERS = CONFIG["shaders"]
    LabelObject.SHADERS = CONFIG["shaders"]
    #QtRecordSession.VIDEOPATH = CONFIG["rec_video"]
    
    MainApplication.run(CONFIG)

