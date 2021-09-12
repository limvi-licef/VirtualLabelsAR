# -*- coding: utf-8 -*-

############################################################################################
# Packages
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import OpenGL.arrays.vbo as vbo
import glfw
import glm
import ctypes as ct
from os.path import join
import cv2
from time import time
import json

from lib.DataManager import DataManager
from lib.QtLabelObject import QtLabelObject
from PyQt5.QtCore import (Qt, pyqtSignal, QObject)
from lib.Matrix import Matrix

from config import *

##########################################################################
class LabelObject (QObject):
    s_dataUpdated = pyqtSignal()
    
    # default label sizes
    m_width = 320
    m_height = 180
    SHADERS = CONFIG["shaders"]

    m_textClose = ""
    m_textFar = ""
    m_ui = None
    m_size=-1.0
    m_thickness = -1
    m_render = None
    m_dataManager = None

    # cameraTranslation = glm.mat4()
    #cameraRotation = glm.mat4()
    
    ######################################################################
    #def __init__(self, ID=None, timestamp=0):
    def __init__(self, ID=None, labelData = None, dataManager = None, timestamp=0 ):
        #print ("[LabelObject::__init__] Called")

        QObject.__init__(self)

        self.m_dataManager = dataManager

        self.initialized = False
        #########TEST########
        #self._setVertices()
        #self.initTexture()
        #########TEST########
        # New version were data is migrated to DataManager
        # self.id = ID if ID is not None else int(time() * 1000)
        # #self.timestamp = timestamp
        # self.timestamp = dataManager.getCurrentTimestamp()
        # self.positionSetting = glm.mat4() #Position set by the users (in cameraRef)
        # #self.position = DataManager.calculateRealPosition(self.positionSetting, self.timestamp) #Position in world coordinate
        # self.position = dataManager.calculateRealPosition(self.positionSetting, self.timestamp)  # Position in world coordinate
        # self.setText(str(self.id))

        # Version before migrating DataManager to data
        if labelData:
            #print("[LabelObject::__init__] Data")
            self.id = labelData["id"]
            self.timestamp = labelData["timestamp"]

            textClose, textFar, size, thick = labelData["info"]["textClose"], labelData["info"]["textFar"], labelData["info"]["size"], labelData["info"]["thick"]
            self.setText(textClose, textFar, size, thick)
            #self.positionSetting = DataManager.getPositionSetting(glm.mat4(labelData["position"]), labelData["timestamp"]) #Position set by the users (in cameraRef)
            self.positionSetting = dataManager.getPositionSetting(glm.mat4(labelData["position"]), labelData[
                "timestamp"])  # Position set by the users (in cameraRef)
            self.position = glm.mat4(labelData["position"]) #Position in world coordinate

        else:
            #print("[LabelObject::__init__] No data")
            self.id = ID if ID is not None else int(time()*1000)
            self.timestamp = timestamp
            #self.id = ID
            self.positionSetting = glm.mat4() #Position set by the users (in cameraRef)
            self.position = dataManager.calculateRealPosition(self.positionSetting, self.timestamp) #Position in world coordinate
            self.setText(str(self.id))

        # Version before migrating DataManager to data
        # if data:
        #     #print("[LabelObject::__init__] Data")
        #     self.id = data["id"]
        #     self.timestamp = data["timestamp"]
        #
        #     textClose, textFar, size, thick = data["info"]["textClose"], data["info"]["textFar"], data["info"]["size"], data["info"]["thick"]
        #     self.setText(textClose, textFar, size, thick)
        #     self.positionSetting = DataManager.getPositionSetting(glm.mat4(data["position"]), data["timestamp"]) #Position set by the users (in cameraRef)
        #     self.position = glm.mat4(data["position"]) #Position in world coordinate
        #
        # else:
        #     #print("[LabelObject::__init__] No data")
        #     self.id = ID if ID is not None else int(time()*1000)
        #     self.timestamp = timestamp
        #     #self.id = ID
        #     self.positionSetting = glm.mat4() #Position set by the users (in cameraRef)
        #     self.position = DataManager.calculateRealPosition(self.positionSetting, self.timestamp) #Position in world coordinate
        #     self.setText(str(self.id))

        #print("[LabelObject::__init__] End")

        self.cameraTranslation = glm.mat4()
        self.cameraRotation = glm.mat4()
        
       
    ######################################################################
    def _setVertices(self):
        #print("[LabelObject::_setVertices] Called")
        w = 0.16 / 2
        h = 0.09 / 2
        self.vertices = np.array([
            -w,  h,     0.0, 0.0,
             w,  h,     1.0, 0.0,
             w, -h,     1.0, 1.0,
            -w, -h,     0.0, 1.0,
            ], dtype=np.float32)
        
        self.vbo = vbo.VBO(self.vertices)
        
        
    ######################################################################
    @staticmethod
    def getShader():
        #print("[LabelObject::getShader] Called")

        assert LabelObject.SHADERS != "", "LabelObject.SHADERS not set"
        VERTEX = join(LabelObject.SHADERS, "label.vs")
        FRAGMENT = join(LabelObject.SHADERS, "label.fs")
        
        labelShader = shaders.compileProgram(
            shaders.compileShader(open(VERTEX).read(), GL_VERTEX_SHADER),
            shaders.compileShader(open(FRAGMENT).read(), GL_FRAGMENT_SHADER)
            )
        glUseProgram(labelShader)
        labelShader.uModelview = glGetUniformLocation(labelShader, "uModelview")
        labelShader.uProjection = glGetUniformLocation(labelShader, "uProjection")
        labelShader.uPosition = glGetUniformLocation(labelShader, "uPosition")
        labelShader.uTexture = glGetUniformLocation(labelShader, "uTexture")
        labelShader.aCoords = glGetAttribLocation(labelShader, "aCoords")
        
        return labelShader
        
        
    ######################################################################
    def save(self):
        #print("[LabelObject::save] Called")
        '''save self data in JSON object format'''
        dataJSON = {
            "id": self.id,
            "timestamp": self.timestamp,
            "info": {
                "textClose": self.m_textClose,
                "textFar": self.m_textFar,
                "size": self.m_size,
                "thick": self.m_thickness,
                },
            "position": self.position.to_list()
        }
        return dataJSON
        
        
    ######################################################################
    def initTexture(self):
        #print("[LabelObject::initTexture] Called")
        w, h = LabelObject.m_width, LabelObject.m_height
        
        self.texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0+self.texture)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        
    ######################################################################
    def setPos(self, pos, orient=(0,0)):
        #print("[LabelObject::setPos] Called")

        position = glm.mat4();
        
        position = glm.translate(position, pos)
        
        position = glm.rotate(position, glm.radians(orient[1]), (0,1,0))
        position = glm.rotate(position, glm.radians(orient[0]), (1,0,0))            
            
        self.positionSetting = position
        #self.position = DataManager.calculateRealPosition(self.positionSetting, self.timestamp)
        self.position = self.m_dataManager.calculateRealPosition(self.positionSetting, self.timestamp)
        
        
    ######################################################################
    def setText(self, textClose="", textFar="", size=0.75, thick=2):
        print("[LabelObject::setText] Called - textFar: " + textFar)
        w, h = LabelObject.m_width, LabelObject.m_height
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        textsize = cv2.getTextSize(textFar, font, size, thick)[0]
        x = (w - textsize[0]) // 2
        y = (h + textsize[1]) // 2
        img = np.zeros((h, w, 3), dtype=np.uint8)
        
        self.m_textFar = textFar
        self.m_textClose = textClose
        self.m_size = size
        self.m_thickness = thick
        self.m_render = cv2.putText(img, textFar, (x,y), font, size, (255,255,255), thick)
        
           
    ######################################################################
    def draw(self, shader):
        if not self.initialized:
            self.initialized = True
            glUseProgram(shader)
            self._setVertices()
            self.initTexture()

        else:
            w, h = LabelObject.m_width, LabelObject.m_height
            
            glUseProgram(shader)
            self.vbo.bind()
            
            glActiveTexture(GL_TEXTURE0+self.texture)
            glBindTexture(GL_TEXTURE_2D, self.texture);
            glUniform1i(shader.uTexture, self.texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, self.m_render)
            
            glUniformMatrix4fv(shader.uPosition, 1, False, glm.value_ptr(self.position))
            
            glEnableVertexAttribArray(shader.aCoords)
            glVertexAttribPointer(shader.aCoords, 4, GL_FLOAT, False, 0, ct.c_void_p(0))
            glDrawArrays(GL_QUADS, 0, 4)

            glBindTexture(GL_TEXTURE_2D, 0);
            self.vbo.unbind()
            glUseProgram(0)

    def setUi (self, parent=None):
        #print ("[LabelObject::setUi] Called")
        # print("\t ID: " + self.id)
        # print("\t Text close: " + self.m_textClose)
        # print("\t Text far: " + self.m_textFar)
        # print("\t Size: " + str(self.m_size))
        # print("\t Thickness: " + str(self.m_thickness))
        # print("\t Position: " + str(self.position))
        # print("\t Orientation: " + str(Matrix.getRotation(self.position)))
        self.m_ui = QtLabelObject(parent)
        self.m_ui.ui.textCloseInput.setText(self.m_textClose)
        self.m_ui.ui.textFarInput.setText(self.m_textFar)
        self.m_ui.ui.sizeInput.setValue(self.m_size)
        self.m_ui.ui.thickInput.setValue(self.m_thickness)

        pos = Matrix.getTranslation(self.positionSetting)
        orient = Matrix.getAngles(Matrix.getRotation(self.positionSetting))
        self.m_ui.ui.xposInput.setValue(pos.x)
        self.m_ui.ui.yposInput.setValue(pos.y)
        self.m_ui.ui.zposInput.setValue(pos.z)

        self.m_ui.ui.xorientInput.setValue(orient.x)
        self.m_ui.ui.yorientInput.setValue(orient.y)

        self.m_ui.s_guiUpdated.connect(self.updateData)

    def updateData(self, textClose, textFar, size, thick, position, orientation):
        print ("[LabelObject:updateData] Called")
        # print("\t ID: " + self.id)
        # print("\t Text close: " + textClose)
        # print("\t Text far: " + textFar)
        # print("\t Size: " + str(size))
        # print("\t Thickness: " + str(thick))
        # print("\t Position: " + str(position))
        # print("\t Orientation: " + str(orientation))
        self.setText(textClose, textFar, size, thick)
        self.setPos(position, orientation)
        self.s_dataUpdated.emit()


    ######################################################################
    @staticmethod
    def test(config):
        
        import time
        
        # set shader location
        LabelObject.SHADERS = config["shaders"]
        
        # start OpenGL
        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Label Object", None, None)
        glfw.make_context_current(win)

        # get the shader program
        labelShader = LabelObject.getShader()
        
        # first label, created with dict, in front of user
        label0 = LabelObject({
            'id': 1612520470451.0574,
            'info': {
                'text': 'Custom text',
                'size': 0.75,
                'thick': 2
                },
            'position': [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]]
            })
        
        
        label1 = LabelObject()
        label1.setPos((0.2, 0.0, 0.0), (0, 30))
        label1.setText("Label 1")
        
        label2 = LabelObject()
        label2.setPos((-0.2, 0.0, 0.0), (30, 0))
        
        label3 = LabelObject()
        label3.setPos((0.0, 0.1, 0.0), (30, 30))
        
        
        glUseProgram(labelShader)
        
        projection = glm.perspective(glm.radians(28), W/H, 0.25, 5.0)
        glUniformMatrix4fv(labelShader.uProjection, 1, False, glm.value_ptr(projection))
        
        modelview = glm.translate(glm.mat4(), (0,0,-0.75))
        glUniformMatrix4fv(labelShader.uModelview, 1, False, glm.value_ptr(modelview))
        
        glClearColor(0.1, 0.3, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        while not glfw.window_should_close(win):
            
            start = time.time()
            
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glUseProgram(labelShader)
            
            label0.draw(labelShader)
            label1.draw(labelShader)
            label2.draw(labelShader)
            label3.draw(labelShader)
            
            glfw.swap_buffers(win)
            glfw.poll_events()
            
            tic = time.time() - start
            delay = 1/30 - tic
            if delay > 0:
                time.sleep(delay)
    
        glfw.terminate()
        
        print(label1.save())
        

if __name__ == "__main__":
    
    from config import *
    
    LabelObject.test(CONFIG)