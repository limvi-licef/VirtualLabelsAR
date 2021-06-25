# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from lib.RecordSession import RecordSession
from lib.GlRecordViewer import GlRecordViewer
from ui.Ui_RecordViewer import Ui_RecordViewer

from lib.LabelObject import LabelObject
from lib.LabelManager import LabelManager

from lib.GlFrameDisplayer import GlFrameDisplayer
from lib.Matrix import Matrix
from lib.MeshObject import MeshObject
from OpenGL.GL import *


class QtRecordViewer(QtWidgets.QOpenGLWidget):
    
    
    def __init__(self, a, parent=None):
        
        QtWidgets.QOpenGLWidget.__init__(self, parent)
        
        self.rv = GlRecordViewer()
        self.a = a
        self.ui = Ui_RecordViewer()
        #self.ui.setupUi(self)
        

        #self.ui.canvas.initializeGL = self.init
        #self.paintGL = self.rv.draw

        self.receive = self.rv.receive
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        
        
    def resizeGL(self, width, height):
        
        glViewport(0, 0, width, height)
        
    
    def initializeGL(self):
        
       self.rv.init(self.a[0],self.a[1],self.a[2])
       glClearColor(0.1, 0.3, 0.4, 1.0)
        
    
    def paintGL(self):
       self.rv.draw()
       glFlush()
        
    
    @staticmethod
    def test(config):
        import sys
        from json import loads
        from lib.QtVideoPlayer import QtVideoPlayer
        
        with open(config["rec_test"], mode="r") as datafile:
            data = loads(datafile.read())
        
        app = QtWidgets.QApplication(sys.argv)
        
        root = QtWidgets.QWidget()
        
        root.layout = QtWidgets.QVBoxLayout()
        
        
        qtVideoPlayer = QtVideoPlayer(data["video"])
        
        w, h = qtVideoPlayer.core.WIDTH, qtVideoPlayer.core.HEIGHT
        args = ((w,h), data, LabelManager.getInstance())
        rv = QtRecordViewer(args)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        rv.setSizePolicy(sizePolicy)
        
        
        qtVideoPlayer.frameUpdate.connect(rv.receive)
        root.layout.addWidget(rv)
        root.layout.addWidget(qtVideoPlayer)
        
        root.setLayout(root.layout)
        root.setWindowTitle("QtRecordViewer")
        root.show()
        app.exec_()
        
        
if __name__ == "__main__":
    
    from config import *
    from compiler import *
    
    GlFrameDisplayer.SHADERS = CONFIG["shaders"]
    MeshObject.SHADERS = CONFIG["shaders"]
    LabelObject.SHADERS = CONFIG["shaders"]
    
    QtRecordViewer.test(CONFIG)