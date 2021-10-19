# -*- coding: UTF-8 -*-

# Form implementation generated from reading ui file 'MainApplication.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from json import loads

from PyQt5 import QtCore, QtWidgets, QtGui

from lib.GlFrameDisplayer import GlFrameDisplayer
from lib.LabelObject import LabelObject
from lib.MeshObject import MeshObject
from lib.QtRecordSession import QtRecordSession
from lib.QtRecordViewer import QtRecordViewer
from lib.QtVideoPlayer import QtVideoPlayer
from lib.QtWindowsDevicePortal import QtWindowsDevicePortal
from ui.Ui_MainApplication import Ui_MainApplication
from lib.LabelManager import LabelManager
from lib.DataManager import DataManager
from lib.Server import Server
import os

#from compiler import *

import threading


class MainApplication(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        
        QtWidgets.QMainWindow.__init__(self, parent)
        
        self.ui = Ui_MainApplication()
        self.ui.setupUi(self)
        
        self.mainWidget = None
        
        self.layout = QtWidgets.QVBoxLayout()

        widgetCentral = QtWidgets.QWidget()
        #self.m_widgetCentralLayout = QtWidgets.QHBoxLayout()
        self.m_widgetCentralLayout = QtWidgets.QStackedLayout()
        widgetCentral.setLayout(self.m_widgetCentralLayout)

        self.m_wMainMenu = QtWidgets.QWidget()
        self.m_wNew = QtWidgets.QWidget()
        self.m_lNew = QtWidgets.QVBoxLayout()
        self.m_wNew.setLayout(self.m_lNew)

        self.m_wOpen = QtWidgets.QWidget()
        self.m_lOpen = QtWidgets.QHBoxLayout()
        self.m_wOpen.setLayout(self.m_lOpen)
        self.m_bNew = False # to know if the widget has already been initialized for the "new" menu
        self.m_bOpen = False # Same as previous but the "open" menu

        self.m_widgetCentralLayout.addWidget(self.m_wMainMenu)
        self.m_widgetCentralLayout.addWidget(self.m_wNew)
        self.m_widgetCentralLayout.addWidget(self.m_wOpen)

        self.layout.addWidget(widgetCentral, 2)

        # Building the main menu
        self.m_lMainMenu = QtWidgets.QHBoxLayout()
        self.m_wMainMenu.setLayout(self.m_lMainMenu)



        wRecording = QtWidgets.QWidget()
        lRecording = QtWidgets.QVBoxLayout()
        wRecording.setLayout(lRecording)

        bRecording = QtWidgets.QPushButton()
        bRecording.setIcon(QtGui.QIcon("./icons/Recording.png"))
        bRecording.setText("Démarrer un \n nouvel enregistrement")
        bRecording.setMaximumWidth(300)
        bRecording.clicked.connect(self.new)

        bOpen = QtWidgets.QPushButton()
        bOpen.setIcon(QtGui.QIcon("./icons/Open.png"))
        bOpen.setText("Ajouter des étiquettes \n sur un enregistrement existant")
        bOpen.setMaximumWidth(300)
        bOpen.clicked.connect(self.open)

        self.m_lMainMenu.addStretch()
        self.m_lMainMenu.addWidget(bRecording)
        self.m_lMainMenu.addStretch()
        self.m_lMainMenu.addWidget(bOpen)
        self.m_lMainMenu.addStretch()

        # Building the bottom part of the interface containing the logos
        widgetBottom = QtWidgets.QWidget()
        widgetBottomLayout = QtWidgets.QHBoxLayout()
        widgetBottom.setLayout(widgetBottomLayout)

        widgetLogoUdS = QtWidgets.QLabel()
        logoUdS = QtGui.QPixmap("./icons/universiteLogo.png")
        widgetLogoUdS.setPixmap(logoUdS.scaledToHeight(75))

        widgetLogoUPoitiers = QtWidgets.QLabel()
        logoUPoitiers = QtGui.QPixmap("./icons/LogoGphy.jpg")
        widgetLogoUPoitiers.setPixmap(logoUPoitiers.scaledToHeight(75))

        widgetBottomLayout.addStretch()
        widgetBottomLayout.addWidget(widgetLogoUdS)
        widgetBottomLayout.addWidget(widgetLogoUPoitiers)

        self.layout.addStretch()
        self.layout.addWidget(widgetBottom)

        self.ui.main.setLayout(self.layout)

        self.m_server = Server()
        self.m_server.run()
        
        
    def new(self):

        if (self.m_bNew == False):
            print("[MainApplication.new] Called")

            wdp = QtWindowsDevicePortal()
            self.m_lNew.addWidget(wdp)

            recordSession = QtRecordSession()
            recordSession.setWdp(wdp)
            self.m_lNew.addWidget(recordSession)

            self.m_bNew = True

        self.m_widgetCentralLayout.setCurrentWidget(self.m_wNew)
    
        
    def open(self):
        if (self.m_bOpen == False):
            file, _ = QtWidgets.QFileDialog.getOpenFileName()
            fileinfo = QtCore.QFileInfo(file)

            if (file != ""):
                with open(file, mode="r") as datafile:
                    data = loads(datafile.read())

                # Building the GUI
                container1 = QtWidgets.QWidget()
                container1.layout = QtWidgets.QVBoxLayout()
                container1.setLayout(container1.layout)

                qtVideoPlayer = QtVideoPlayer(fileinfo.dir().path() + "/" + data["video"])
                dataManager = DataManager(data)
                labelManager = LabelManager(dataManager)
                qtLabelManager = labelManager.setUI(parent=self)

                width, height = qtVideoPlayer.core.WIDTH, qtVideoPlayer.core.HEIGHT

                rv = QtRecordViewer(width, height, labelManager, dataManager)

                # UI building
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                rv.setSizePolicy(sizePolicy)
                qtVideoPlayer.frameUpdate.connect(rv.receive)
                container1.layout.addWidget(rv)
                container1.layout.addWidget(qtVideoPlayer)

                container2 = QtWidgets.QWidget()
                container2.layout = QtWidgets.QVBoxLayout()
                container2.setLayout(container2.layout)

                qtLabelManager.canvas = rv

                container2.layout.addWidget(qtLabelManager)

                self.m_lOpen.addWidget(container2)
                self.m_lOpen.addWidget(container1,2)

                # Loading labels - if any
                baseFilePathForLabelsFile = os.path.splitext(fileinfo.filePath())[0] # Get the filepath without the extension
                labelsFilePath = baseFilePathForLabelsFile + ".labels"
                labelManager.initFromFile(pathToFile=labelsFilePath)
                self.m_server.updatePathLabelsFile(labelsFilePath)

                self.m_bOpen = True

                self.m_widgetCentralLayout.setCurrentWidget(self.m_wOpen)
                print ("[MainApplication::Open] Done")
            else:
                print("[MainApplication::open] Info - No file opened")
        else:
            self.deleteChildrenWidgets(self.m_wOpen)
            self.m_widgetCentralLayout.setCurrentWidget(self.m_wOpen)
            self.m_bOpen = False
            self.open()
            print ("[MainApplication::Open] Cannot load a new video for now. Please restart the application to load a new video")


    def deleteChildrenWidgets(self, widget):
        while (self.m_lOpen.count() > 0):

            temp = self.m_lOpen.takeAt(0)
            print(str(type(temp)))
            if (type(temp) == QtWidgets.QWidgetItem):
                temp.widget().hide() # for now widgets are "hidden". Not the cleanest way.
        
    def exit(self):
        
        print("[MainApplication:exit] Called")
        self.m_server.stop()
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
        print ("[MainApplication::run] Exiting application")
        sys.exit(app.exec_())
        
        
if __name__ == "__main__":
    
    #from config_template import *
    from config import *

    GlFrameDisplayer.SHADERS = CONFIG["shaders"]
    MeshObject.SHADERS = CONFIG["shaders"]
    #LabelObject.SHADERS = CONFIG["shaders"]
    #QtRecordSession.VIDEOPATH = CONFIG["rec_video"]

    print(CONFIG)

    MainApplication.run(CONFIG)

