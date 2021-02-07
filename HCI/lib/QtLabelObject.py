# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from lib.LabelObject import LabelObject
from ui.Ui_LabelObject import Ui_LabelObject
from numpy import ndarray
from lib.Matrix import Matrix

        
class QtLabelObject(QtWidgets.QWidget):
    
    def __init__(self, label, parent=None):
        
        QtWidgets.QWidget.__init__(self, parent)
        
        self.ui = Ui_LabelObject()
        self.ui.setupUi(self)
        
        
        self.allow_update = False
        
        self.label = label
        self.ui.textInput.setText(label.text)
        self.ui.sizeInput.setValue(label.size)
        self.ui.thickInput.setValue(label.thick)
        
        pos = Matrix.getTranslation(label.position)
        orient = Matrix.getAngles(Matrix.getRotation(label.position))
        self.ui.xposInput.setValue(pos.x)
        self.ui.yposInput.setValue(pos.y)
        self.ui.zposInput.setValue(pos.z)
        
        self.ui.xorientInput.setValue(orient.x)
        self.ui.yorientInput.setValue(orient.y)
        
        self.allow_update = True
        
        
    def update(self):
        
        QtWidgets.QWidget.update(self)
        
        if self.allow_update:
            text = self.ui.textInput.text()
            size = self.ui.sizeInput.value()
            thick = self.ui.thickInput.value()
            self.label.setText(text, size, thick)
            
            pos = (self.ui.xposInput.value(), self.ui.yposInput.value(), self.ui.zposInput.value())
            orient = (self.ui.xorientInput.value(), self.ui.yorientInput.value())
            self.label.setPos(pos, orient)
        
        
    @staticmethod
    def test(config):
            
        import sys
        import time
        import glfw
        import glm
        
        LabelObject.SHADERS = config["shaders"]
        
        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Label Object", None, None)
        glfw.make_context_current(win)

        labelShader = LabelObject.getShader()
        label = LabelObject()
        label.setText("Label", 3, 2)
        label.setPos((0.05,0.05,-0.05), (5,5,5))
        
        glUseProgram(labelShader)
        
        projection = glm.perspective(glm.radians(28), W/H, 0.25, 5.0)
        glUniformMatrix4fv(labelShader.uProjection, 1, False, glm.value_ptr(projection))
        
        modelview = glm.translate(glm.mat4(), (0,0,-0.35))
        glUniformMatrix4fv(labelShader.uModelview, 1, False, glm.value_ptr(modelview))
        
        glClearColor(0.1, 0.3, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        
        def draw():
            
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glUseProgram(labelShader)
            
            label.draw(labelShader)
            
            glfw.swap_buffers(win)
            glfw.poll_events()
        
        
        app = QtWidgets.QApplication(sys.argv)
        root = QtWidgets.QWidget()
        
        label_widget = QtLabelObject(label, root)
        
        label_widget.timer = QtCore.QTimer()
        label_widget.timer.timeout.connect(draw)
        label_widget.timer.start(int(1000/30))
        
        
        root.setWindowTitle("QtLabelObject")
        root.show()
        app.exec_()
        
        glfw.terminate()
        
        
if __name__ == "__main__":
    
    from config import *
    from compiler import *
    from OpenGL.GL import *
    
    QtLabelObject.test(CONFIG)
