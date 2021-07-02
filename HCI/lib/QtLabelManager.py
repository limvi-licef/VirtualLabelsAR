# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from lib.QtLabelObject import QtLabelObject
#from lib.LabelManager import LabelManager
from lib.LabelObject import LabelObject
from ui.Ui_LabelManager import Ui_LabelManager
#from lib.QtRecordViewer import QtRecordViewer
from numpy import ndarray
from lib.Matrix import Matrix
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import OpenGL.arrays.vbo as vbo
from PyQt5.QtCore import (Qt, pyqtSignal)
        
class QtLabelManager(QtWidgets.QWidget):
    s_remove = pyqtSignal()
    s_select = pyqtSignal(str)
    s_create = pyqtSignal()
    def __init__(self, parent=None):
        print ("[QtLabelManager::__init__] Called")

        QtWidgets.QWidget.__init__(self, parent)        
        self.ui = Ui_LabelManager()
        self.ui.setupUi(self)
        
        #self.manager = LabelManager.getInstance()
        self.panel = None


        print("[QtLabelManager::__init__] End")
        
        
    def create(self):
        ##add canvas
        print ("[QtLabelManager::create] Called")
        self.s_create.emit()

        # self.canvas.makeCurrent()
        # label = self.manager.create()
        # self.ui.list.addItem(label.id)
        
        
    def remove(self):
        print("[QtLabelManager::remove] Called")
        self.s_remove.emit()

        # if self.manager.selected:
        #     for item in self.ui.list.selectedItems():
        #         row = self.ui.list.row(item)
        #         self.ui.list.takeItem(row)
        #
        #     label = self.manager.removeSelected()
        #     self.ui.list.clearSelection()
        #     self.panel.deleteLater()
        #     self.ui.removeButton.setDisabled(True)
        #     self.panel.deleteLater()
        #     self.panel = None
        
        
    def displayLabelPanel(self, item):
        print("[QtLabelManager::displayLabelPanel] Called")
        #self.manager.select(item.text())
        self.s_select.emit(item.text())

        # if self.panel: self.panel.deleteLater()
        #
        # if self.manager.selected:
        #     self.panel = QtLabelObject(self.manager.selected)
        #     self.ui.verticalLayout.addWidget(self.panel)
        #     self.ui.removeButton.setDisabled(False)
            
        
    def addLabelToGui (self, label):
        print("[QtLabelManager::addLabelToGui] Called")
        print (label.id)
        self.canvas.makeCurrent()
        self.ui.list.addItem(label.id)
        
    @staticmethod
    def test(config):
            
        import time
        import sys
        import glfw
        import glm

        LabelObject.SHADERS = config["shaders"]
        
        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Label Object", None, None)
        glfw.make_context_current(win)

        app = QtWidgets.QApplication(sys.argv)
        root = QtWidgets.QWidget()
        root.layout = QtWidgets.QVBoxLayout()
        
        labelManager = QtLabelManager()
        root.layout.addWidget(labelManager)
        root.setLayout(root.layout)
        
        glUseProgram(labelManager.manager.shader)
        projection = glm.perspective(glm.radians(28), W/H, 0.25, 5.0)
        glUniformMatrix4fv(labelManager.manager.shader.uProjection, 1, False, glm.value_ptr(projection))        
        modelview = glm.translate(glm.mat4(), (0,0,-0.5))
        glUniformMatrix4fv(labelManager.manager.shader.uModelview, 1, False, glm.value_ptr(modelview))
        
        glClearColor(0.1, 0.3, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        def draw():
            
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            labelManager.manager.draw()
            
            glfw.swap_buffers(win)
            glfw.poll_events()
            
        
        
        labelManager.timer = QtCore.QTimer()
        labelManager.timer.timeout.connect(draw)
        labelManager.timer.start(int(1000/30))
        
        root.setWindowTitle("QtLabelManager")
        root.show()
        
        
        e = app.exec_()
        glfw.terminate()
        sys.exit(e)
    
        
        
if __name__ == "__main__":
    
    from config import *
    from compiler import *
    from OpenGL.GL import *
    
    QtLabelManager.test(CONFIG)
