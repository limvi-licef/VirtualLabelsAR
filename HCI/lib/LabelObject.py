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
        

##########################################################################
class LabelObject:
    
    
    # default label sizes
    WIDTH = 320
    HEIGHT = 180
       
    
    ######################################################################
    def __init__(self, data=None, ID=None):
        
        self.initialized = False
        #########TEST########
        self._setVertices()
        self.initTexture()
        #########TEST########
        if data:
            
            self.id = data["id"]
            
            text, size, thick = data["info"]["text"], data["info"]["size"], data["info"]["thick"]
            self.setText(text, size, thick)
            self.position = glm.mat4(data["position"])
            
        else:
            self.id = ID if ID else int(time()*1000)
            self.position = glm.mat4()            
            self.setText(str(self.id))
        
       
    ######################################################################
    def _setVertices(self):
        
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
        '''save self data in JSON object format'''
        dataJSON = {
            "id": self.id,
            "info": {
                "textClose": self.text+"close",
                "textFar": self.text + "far",
                "size": self.size,
                "thick": self.thick,
                },
            "position": self.position.to_list()
        }
        return dataJSON
        
        
    ######################################################################
    def initTexture(self):
        
        w, h = LabelObject.WIDTH, LabelObject.HEIGHT
        
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
        
        position = glm.mat4()
        
        position = glm.translate(position, pos)
        
        position = glm.rotate(position, glm.radians(orient[1]), (0,1,0))
        position = glm.rotate(position, glm.radians(orient[0]), (1,0,0))            
            
        self.position = position
        
        
    ######################################################################
    def setText(self, text, size=0.75, thick=2):
        
        w, h = LabelObject.WIDTH, LabelObject.HEIGHT
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        textsize = cv2.getTextSize(text, font, size, thick)[0]
        x = (w - textsize[0]) // 2
        y = (h + textsize[1]) // 2
        img = np.zeros((h, w, 3), dtype=np.uint8)
        
        self.text = text
        self.size = size
        self.thick = thick
        self.render = cv2.putText(img, text, (x,y), font, size, (255,255,255), thick)
        
           
    ######################################################################
    def draw(self, shader):

        if not self.initialized:
            self.initialized = True
            glUseProgram(shader)
            self._setVertices()
            self.initTexture()

        else:
            w, h = LabelObject.WIDTH, LabelObject.HEIGHT
            
            glUseProgram(shader)
            self.vbo.bind()
            
            glActiveTexture(GL_TEXTURE0+self.texture)
            glBindTexture(GL_TEXTURE_2D, self.texture);
            glUniform1i(shader.uTexture, self.texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, self.render)
            
            glUniformMatrix4fv(shader.uPosition, 1, False, glm.value_ptr(self.position))
            
            glEnableVertexAttribArray(shader.aCoords)
            glVertexAttribPointer(shader.aCoords, 4, GL_FLOAT, False, 0, ct.c_void_p(0))
            glDrawArrays(GL_QUADS, 0, 4)

            glBindTexture(GL_TEXTURE_2D, 0);
            self.vbo.unbind()
            glUseProgram(0)
        
        
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