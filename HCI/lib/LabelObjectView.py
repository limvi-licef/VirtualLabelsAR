# -*- coding: UTF-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
#from lib.LabelObject import LabelObject
from ui.Ui_LabelObject import Ui_LabelObject
from numpy import ndarray
from lib.Matrix import Matrix
#from lib.LabelManager import LabelManager
from PyQt5.QtCore import (Qt, pyqtSignal)

        
class LabelObjectView(QtWidgets.QWidget):

    #s_dataUpdated = pyqtSignal()
    # textClose, textFar, size, thick, position(x,y,z), orientation(x,y)
    s_guiUpdated = pyqtSignal(str, str, float, int, tuple, tuple)

    def __init__(self, parent=None):
        #print ("[QtLabelObject::__init__] Called")

        QtWidgets.QWidget.__init__(self, parent)
        
        self.ui = Ui_LabelObject()
        self.ui.setupUi(self)
        
        
        self.allow_update = False
        
        #self.label = label
        #self.ui.textInput.setText(label.text)
        # self.ui.textCloseInput.setText(label.m_textClose)
        # self.ui.textFarInput.setText(label.m_textFar)
        # self.ui.sizeInput.setValue(label.size)
        # self.ui.thickInput.setValue(label.thick)
        #
        # pos = Matrix.getTranslation(label.position)
        # orient = Matrix.getAngles(Matrix.getRotation(label.position))
        # self.ui.xposInput.setValue(pos.x)
        # self.ui.yposInput.setValue(pos.y)
        # self.ui.zposInput.setValue(pos.z)
        #
        # self.ui.xorientInput.setValue(orient.x)
        # self.ui.yorientInput.setValue(orient.y)
        
        self.allow_update = True


        #print("[QtLabelObject::__init__] End")
        
        
    def update(self):
        #print("[QtLabelObject:update] Called")
        QtWidgets.QWidget.update(self)
        
        if self.allow_update:
            #print("[QtLabelObject:update] allow update")
            #text = self.ui.textInput.text()
            text = self.ui.textDisplayed.text()
            name = self.ui.textLabelName.text()
            size = self.ui.sizeInput.value()
            thick = self.ui.thickInput.value()
            #self.label.setText(textClose, textFar, size, thick)
            
            #pos = (self.ui.xposInput.value(), self.ui.yposInput.value(), self.ui.zposInput.value())
            #orient = (self.ui.xorientInput.value(), self.ui.yorientInput.value())
            #self.label.setPos(pos, orient)

            position = (self.ui.xposInput.value(),
                        self.ui.yposInput.value(),
                        self.ui.zposInput.value())
            orientation = (self.ui.xorientInput.value(),
                           self.ui.yorientInput.value())

            self.s_guiUpdated.emit(name, text, size, thick, position, orientation)

        #self.s_dataUpdated.emit()
        #LabelManager.getInstance().saveToTXT()
        
    @staticmethod
    def test(config):
         print ("[QtLabelObject:test] Called - but empty so nothing will happen")
        # import sys
        # import time
        # import glfw
        # import glm
        #
        # LabelObject.SHADERS = config["shaders"]
        #
        # W, H = 640, 360
        # glfw.init()
        # win = glfw.create_window(W, H, "Label Object", None, None)
        # glfw.make_context_current(win)
        #
        # labelShader = LabelObject.getShader()
        # label = LabelObject()
        # label.setText("Label", 3, 2)
        # label.setPos((0.05,0.05,-0.05), (5,5,5))
        #
        # glUseProgram(labelShader)
        #
        # projection = glm.perspective(glm.radians(28), W/H, 0.25, 5.0)
        # glUniformMatrix4fv(labelShader.uProjection, 1, False, glm.value_ptr(projection))
        #
        # modelview = glm.translate(glm.mat4(), (0,0,-0.35))
        # glUniformMatrix4fv(labelShader.uModelview, 1, False, glm.value_ptr(modelview))
        #
        # glClearColor(0.1, 0.3, 0.4, 1.0)
        # glEnable(GL_DEPTH_TEST)
        #
        # def draw():
        #
        #     glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #     glUseProgram(labelShader)
        #
        #     label.draw(labelShader)
        #
        #     glfw.swap_buffers(win)
        #     glfw.poll_events()
        #
        #
        # app = QtWidgets.QApplication(sys.argv)
        # root = QtWidgets.QWidget()
        #
        # label_widget = QtLabelObject(label, root)
        #
        # label_widget.timer = QtCore.QTimer()
        # label_widget.timer.timeout.connect(draw)
        # label_widget.timer.start(int(1000/30))
        #
        #
        # root.setWindowTitle("QtLabelObject")
        # root.show()
        # app.exec_()
        #
        # glfw.terminate()
        
        
if __name__ == "__main__":
    
    from config import *
    #from compiler import *
    from OpenGL.GL import *
    
    LabelObjectView.test(CONFIG)
