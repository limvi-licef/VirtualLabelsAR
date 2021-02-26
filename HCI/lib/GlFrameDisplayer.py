# -*- coding: utf-8 -*-


import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import OpenGL.arrays.vbo as vbo
import glfw
import ctypes as ct
from os.path import join


##########################################################################
class GlFrameDisplayer:
    
    
    SHADERS = ""
        
        
    ######################################################################
    def __init__(self):
        
        self.setShader()
        self.setBuffer()
        self.texture = None
        
        
    ######################################################################
    def setBuffer(self):
        
        data = np.array([
            -0.5,  0.5,     0.0, 0.0,
             0.5,  0.5,     1.0, 0.0,
             0.5, -0.5,     1.0, 1.0,
            -0.5, -0.5,     0.0, 1.0,
            ], dtype=np.float32)
        
        self.vbo = vbo.VBO(data)
        
        
    ######################################################################
    def setShader(self):
        
        assert GlFrameDisplayer.SHADERS != "", "MeshObject.SHADERS not set"
        VERTEX = join(GlFrameDisplayer.SHADERS, "frame.vs")
        FRAGMENT = join(GlFrameDisplayer.SHADERS, "frame.fs")
        
        self.shader = shaders.compileProgram(
            shaders.compileShader(open(VERTEX).read(), GL_VERTEX_SHADER),
            shaders.compileShader(open(FRAGMENT).read(), GL_FRAGMENT_SHADER)
            )
        glUseProgram(self.shader)
        self.shader.aCoords = glGetAttribLocation(self.shader, "aCoords")
        self.shader.uTexture = glGetUniformLocation(self.shader, "uTexture")
        
        
    ######################################################################
    def setTexture(self, width, height):
    
        self.texture = glGenTextures(1);
        glActiveTexture(GL_TEXTURE0+self.texture)
        glBindTexture(GL_TEXTURE_2D, self.texture);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None);
        glGenerateMipmap(GL_TEXTURE_2D);
        glBindTexture(GL_TEXTURE_2D, 0);
        
        self.width = width
        self.height = height
        
        return self
        
        
    ######################################################################
    def receive(self, frame):
        
        if self.texture:
            w = self.width
            h = self.height
            
            glBindTexture(GL_TEXTURE_2D, self.texture);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, frame)
            glBindTexture(GL_TEXTURE_2D, 0);
        
        
    ######################################################################
    def draw(self):
        
        if self.texture:
            glUseProgram(self.shader)
            glActiveTexture(GL_TEXTURE0+self.texture)
            glBindTexture(GL_TEXTURE_2D, self.texture);
            glUniform1i(self.shader.uTexture, self.texture)
            self.vbo.bind()
            
            glEnableVertexAttribArray(self.shader.aCoords)
            glVertexAttribPointer(self.shader.aCoords, 4, GL_FLOAT, False, 0, ct.c_void_p(0))
            glDrawArrays(GL_QUADS, 0, 4)
            
            self.vbo.unbind()
            glBindTexture(GL_TEXTURE_2D, 0);
            glUseProgram(0)
        
        
    ######################################################################
    @staticmethod
    def test(config):
        
        import time
        from cv2 import imread
        from lib.VideoPlayer import VideoPlayer

        GlFrameDisplayer.SHADERS = config["shaders"]
        videoPlayer = VideoPlayer(config["video"])
        
        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Frame Displayer", None, None)
        glfw.make_context_current(win)
        
        frameDisplayer = GlFrameDisplayer().setTexture(videoPlayer.WIDTH, videoPlayer.HEIGHT)
        
        videoPlayer.play()
        glClearColor(0.1, 0.3, 0.4, 1.0)
        while not glfw.window_should_close(win):
            
            start = time.time()
            
            _, frame = videoPlayer.read()
            if _:
                frameDisplayer.receive(frame)
                frameDisplayer.draw()
            
            glfw.swap_buffers(win)
            glfw.poll_events()
            
            tic = time.time() - start
            delay = 1/videoPlayer.FPS - tic
            if delay > 0:
                time.sleep(delay)
    
        glfw.terminate()
        
        
if __name__ == "__main__":
    
    from config import *
    
    GlFrameDisplayer.test(CONFIG)        