# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from lib.QtLabelObject import QtLabelObject
from lib.LabelManager import LabelManager
from lib.LabelObject import LabelObject
from ui.Ui_LabelManager import Ui_LabelManager
from numpy import ndarray
from lib.Matrix import Matrix
        
class QtLabelManager(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        
        QtWidgets.QWidget.__init__(self, parent)        
        self.ui = Ui_LabelManager()
        self.ui.setupUi(self)
        
        self.manager = LabelManager()
        self.panel = None
        
        
    def create(self):
        
        label = self.manager.create()
        self.ui.list.addItem(label.id)
        
        
        
    def displayLabelPanel(self, item):
        
        self.manager.select(item.text())
        if self.manager.selected:
            if self.panel: self.panel.deleteLater()
            self.panel = QtLabelObject(self.manager.selected)
            self.ui.verticalLayout.addWidget(self.panel)
            
        
        
        
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
        # labelManager = LabelManager()
        
        # label1 = labelManager.create()
        # label1.setPos((-0.1, 0.0, 0.0))
        
        # label2 = labelManager.create()
        # label2.setPos((0.1, 0.0, 0.0))
        
        glUseProgram(labelManager.manager.shader)
        projection = glm.perspective(glm.radians(28), W/H, 0.25, 5.0)
        glUniformMatrix4fv(labelManager.manager.shader.uProjection, 1, False, glm.value_ptr(projection))        
        modelview = glm.translate(glm.mat4(), (0,0,-0.5))
        glUniformMatrix4fv(labelManager.manager.shader.uModelview, 1, False, glm.value_ptr(modelview))
        
        glClearColor(0.1, 0.3, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        def draw():
            
            # if glfw.get_key(win, glfw.KEY_1):
            #     labelManager.select(0)
            # elif glfw.get_key(win, glfw.KEY_2):
            #     labelManager.select(1)
            # elif glfw.get_key(win, glfw.KEY_3):
            #     labelManager.select(3)
                
            # label1.setText("1")
            # label2.setText("2")
            # if labelManager.selected:
            #     labelManager.selected.setText("Selected")
            
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
