# -*- coding: utf-8 -*-


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

from lib.LabelObject import LabelObject
        

##########################################################################
class LabelManager:
       
    
    ######################################################################
    def __init__(self):
        
        self.labels = {}
        self.selected = None
        self.counter = 0
        
        
    ######################################################################
    def init(self):
        
        self.shader = LabelObject.getShader()
        
        return self
        
        
    ######################################################################
    def save(self):
        
        data = []
        
        for label in self.labels:
            data.append(label.save())
        
        return data
        
        
    ######################################################################
    def create(self):
        
        ID = f"Label_{self.counter}"
        while ID in self.labels:
            self.counter += 1
            ID = f"Label_{self.counter}"
        
        self.labels[ID] = label = LabelObject(ID=ID)
        
        return label
        
        
    ######################################################################
    def select(self, ID):
        
        if ID in self.labels:
            self.selected = self.labels[ID]
        else:
            self.selected = None
        
        
    ######################################################################
    def remove(self, ID):
        
        if ID in self.labels:
            label = self.labels[ID]
            del self.labels[ID]
            return label
        else:
            return None
        
        
    ######################################################################
    def removeSelected(self):
        
        if self.selected:
            ID = self.selected.id
            label = self.labels[ID]
            del self.labels[ID]
            return label
        else:
            return None
        
           
    ######################################################################
    def draw(self):

        for ID, label in self.labels.items():
            label.draw(self.shader)
        
        
    ######################################################################
    @staticmethod
    def test(config):
        
        import time
        LabelObject.SHADERS = config["shaders"]
        
        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Label Object", None, None)
        glfw.make_context_current(win)

        labelManager = LabelManager().init()
        
        label0 = labelManager.create()
        label0.setPos((-0.1, 0.0, 0.0))
        
        label1 = labelManager.create()
        label1.setPos((0.1, 0.0, 0.0))
        
        glUseProgram(labelManager.shader)
        projection = glm.perspective(glm.radians(28), W/H, 0.25, 5.0)
        glUniformMatrix4fv(labelManager.shader.uProjection, 1, False, glm.value_ptr(projection))        
        modelview = glm.translate(glm.mat4(), (0,0,-0.5))
        glUniformMatrix4fv(labelManager.shader.uModelview, 1, False, glm.value_ptr(modelview))
        
        glClearColor(0.1, 0.3, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        while not glfw.window_should_close(win):
            
            start = time.time()
            
            if glfw.get_key(win, glfw.KEY_1):
                labelManager.select("Label_0")
            elif glfw.get_key(win, glfw.KEY_2):
                labelManager.select("Label_1")
            elif glfw.get_key(win, glfw.KEY_3):
                labelManager.select("Label_2")
                
            label0.setText("1")
            label1.setText("2")
            if labelManager.selected:
                labelManager.selected.setText("Selected")
            
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            labelManager.draw()
            
            glfw.swap_buffers(win)
            glfw.poll_events()
            
            tic = time.time() - start
            delay = 1/30 - tic
            if delay > 0:
                time.sleep(delay)
    
        glfw.terminate()
        

if __name__ == "__main__":
    
    from config import *
    
    LabelManager.test(CONFIG)