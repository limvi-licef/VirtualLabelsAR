# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from lib.VideoPlayer import VideoPlayer
from ui.Ui_VideoPlayer import Ui_VideoPlayer
from numpy import ndarray

        
class QtVideoPlayer(QtWidgets.QWidget):

    
    frameUpdate = QtCore.pyqtSignal(ndarray)
        
        
    def __init__(self, filename, parent=None, refresh=int(1000/30)):
        
        QtWidgets.QWidget.__init__(self, parent)
        
        VideoPlayer(filename).interface(self)
        
        self.ui = Ui_VideoPlayer()
        self.ui.setupUi(self)
        
        self.setRefresh(refresh)
        self.ui.timeSlider.setMaximum(int(self.videoPlayer.TIME)-1)
        
        
    def setRefresh(self, t):
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(t)
        
        
    def update(self):
        QtWidgets.QWidget.update(self)
        _, frame = self.read()
        if _:
            self.frameUpdate.emit(frame)
            
            m, s = map(lambda n: str(n).zfill(2), self.videoPlayer.getRecordTime(mode=2))
            self.ui.timeLabel.setText(f"{m}:{s}")
            
            v = int(self.videoPlayer.getRecordTime(mode=1))
            self.ui.timeSlider.setValue(v)
        
        
    @staticmethod
    def test(config):
        
        import sys
        import cv2
        
        def showFrame(frame):
            
            data, width, height = frame.tobytes(), frame.shape[1], frame.shape[0]
            image = QtGui.QImage(data, width, height, QtGui.QImage.Format_BGR888)
            pixmap = QtGui.QPixmap(image)
            root.label.setPixmap(pixmap)
            
            
        def openVideo():
            
            layout.removeWidget(openButton)
            openButton.deleteLater()
            
            root.label = QtWidgets.QLabel()
            layout.addWidget(root.label)
            
            qtVideoPlayer = QtVideoPlayer(config["video"])
            qtVideoPlayer.frameUpdate.connect(showFrame)
            layout.addWidget(qtVideoPlayer)
            
        
        app = QtWidgets.QApplication(sys.argv)
        root = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        openButton = QtWidgets.QPushButton("Open video")
        openButton.clicked.connect(openVideo)
        layout.addWidget(openButton)
        
        root.setLayout(layout)
        root.setWindowTitle("QtVideoPlayer")
        root.show()
        app.exec_()
        
        
if __name__ == "__main__":
    
    from config import *
    from compiler import *
    
    QtVideoPlayer.test(CONFIG)
