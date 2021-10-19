# -*- coding: utf-8 -*-


############################################################################################
# Packages
from PyQt5 import QtCore, QtGui, QtWidgets
from numpy import ndarray

# Ui
#from compiler import *
from ui.Ui_VideoPlayer import Ui_VideoPlayer

# Lib
from lib.VideoPlayer import VideoPlayer


############################################################################################
class QtVideoPlayer(QtWidgets.QWidget):

    
    # Qt signal
    frameUpdate = QtCore.pyqtSignal(int, ndarray)
    
    
    ########################################################################################
    def __init__(self, filename, parent=None, refresh=int(1000/30)):
        
        """
            Constructor.
            
            @param filename: str, path to video
            @param parent: Qt widget
            @param refresh: int, refresh period in millisecond
        """

        print ("[QtVideoPlayer::__init__] Called")

        # constructors
        QtWidgets.QWidget.__init__(self, parent)        
        self.core = VideoPlayer(filename).interface(self)
        
        # setup ui
        self.ui = Ui_VideoPlayer()
        self.ui.setupUi(self)
        
        # set the refresh timer and set the time slider
        self._setRefresh(refresh)
        self.ui.timeSlider.setMaximum(int(self.core.TIME)-1)

        print("[QtVideoPlayer::__init__] End")
        
    ########################################################################################
    def _setRefresh(self, t):
        
        """
            Create the refresh timer.
            
            @param t: int, millisecond period for timer
        """
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(t)
        
        
    ########################################################################################
    def update(self):
        
        """
            Inherited from QWidgets.
        """
        
        # call QWidget inherited method
        QtWidgets.QWidget.update(self)
        
        # get a frame from the VideoPlayer object
        _, frame = self.read()
        if _:
            # send signal
            n = self.core.getFrameNumber()
            self.frameUpdate.emit(n, frame)
            
            # update video time
            m, s = map(lambda n: str(n).zfill(2), self.core.getRecordTime(mode=2))
            self.ui.timeLabel.setText(f"{m}:{s}")
            
            # update slider position
            v = int(self.core.getRecordTime(mode=1))
            self.ui.timeSlider.setValue(v)
        
        
    ########################################################################################
    @staticmethod
    def test(config):
        
        import sys
        import cv2
        
        
        # display a fram in a QLabel from numpy array
        def showFrame(n, frame):
            
            # get frame info
            data, width, height = frame.tobytes(), frame.shape[1], frame.shape[0]
            
            # convert numpy array to QImage then convert to QPixmap which is displayable in QLabel
            image = QtGui.QImage(data, width, height, QtGui.QImage.Format_BGR888)
            pixmap = QtGui.QPixmap(image)
            root.label.setPixmap(pixmap)
            
            
        # dynamicaly create a video player and an associated QLabel for displaying frames
        def openVideo():
            
            # delete button
            layout.removeWidget(openButton)
            openButton.deleteLater()
            
            # create QLabel
            root.label = QtWidgets.QLabel()
            layout.addWidget(root.label)
            
            # create the video player
            qtVideoPlayer = QtVideoPlayer(config["video"])
            qtVideoPlayer.frameUpdate.connect(showFrame)
            layout.addWidget(qtVideoPlayer)
            
        
        # create application and main widget
        app = QtWidgets.QApplication(sys.argv)
        root = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        # add the open button
        openButton = QtWidgets.QPushButton("Open video")
        openButton.clicked.connect(openVideo)
        layout.addWidget(openButton)
        
        # config the main widget and render
        root.setLayout(layout)
        root.setWindowTitle("QtVideoPlayer")
        root.show()
        sys.exit(app.exec_())
        
        
if __name__ == "__main__":
    
    from config import *
    
    QtVideoPlayer.test(CONFIG)
