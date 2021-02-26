# -*- coding: utf-8 -*-


import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import OpenGL.arrays.vbo as vbo
import glfw
import glm
import ctypes as ct
from os.path import join
from lib.LabelObject import LabelObject
from lib.LabelManager import LabelManager
from lib.GlFrameDisplayer import GlFrameDisplayer
from lib.Matrix import Matrix
from lib.MeshObject import MeshObject


##########################################################################
class GlRecordViewer:
    
    
    ######################################################################
    def __init__(self):
        
        self.initialized = False
        self.nframe = 0

    
    ######################################################################
    def init(self, video_dims, data, labelManager):
    
        self.frameDisplayer = GlFrameDisplayer()
        
        self.data = data
        self.labelManager = labelManager.init()
        self.projection = glm.perspective(glm.radians(28), 16/9, 0.25, 5.0)
        
        glClearColor(0.1, 0.3, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
    
        w, h = video_dims
        self.frameDisplayer.setTexture(w, h)
        
        self.meshShader = MeshObject.getShader()
        glUseProgram(self.meshShader)
        glUniformMatrix4fv(self.meshShader.uProjection, 1, False, glm.value_ptr(self.projection))
        
        self.meshes = []
        for idMesh, meshData in data["meshes"].items():
            mesh = MeshObject(meshData)
            self.meshes.append(mesh)
            
        glUseProgram(self.labelManager.shader)
        glUniformMatrix4fv(self.labelManager.shader.uProjection, 1, False, glm.value_ptr(self.projection))
        
        self.initialized = True
        
        
    ######################################################################
    def receive(self, nframe, frame):
        
        if self.initialized and self.frameDisplayer:
            
            self.nframe = nframe if nframe < len(self.data["sync"]) else len(self.data["sync"]) - 1
            self.frameDisplayer.receive(frame)
        
    
    ######################################################################
    def draw(self):
        
        if self.initialized:
            
            idCam = self.data["sync"][self.nframe]
            infoCam = self.data["camera"][idCam]
            
            glClear(GL_COLOR_BUFFER_BIT)
            
            self.frameDisplayer.draw()
            
            glClear(GL_DEPTH_BUFFER_BIT)
            
            glUseProgram(self.meshShader)

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            position = Matrix.fromList(infoCam["position"])
            rotation = Matrix.fromList(infoCam["rotation"], toTranspose=True)
            modelview = rotation * position
            glUniformMatrix4fv(self.meshShader.uModelview, 1, False, glm.value_ptr(modelview))
            for mesh in self.meshes:
                mesh.draw(self.meshShader)
                
            glUseProgram(self.labelManager.shader)
            glUniformMatrix4fv(self.labelManager.shader.uModelview, 1, False, glm.value_ptr(modelview))
            self.labelManager.draw()
        
        
    ######################################################################
    @staticmethod
    def test(config):
        
        import time
        from lib.VideoPlayer import VideoPlayer
        from json import loads
        
        with open(config["rec_test"], mode="r") as datafile:
            data = loads(datafile.read())
        
        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Mesh Object", None, None)
        glfw.make_context_current(win)
        
        videoPlayer = VideoPlayer(data["video"])
        videoPlayer.play()
        
        labelManager = LabelManager().init()
        
        label0 = labelManager.create()
        label0.setPos((-0.1, 0.0, -1.0))
        
        label1 = labelManager.create()
        label1.setPos((0.1, 0.0, -4.0))
        
        rv = GlRecordViewer()
        rv.init((videoPlayer.WIDTH, videoPlayer.HEIGHT), data, labelManager)
        
        while not glfw.window_should_close(win):
            
            start = time.time()
            
            _, frame = videoPlayer.read()
            if _: rv.receive(videoPlayer.getFrameNumber(), frame)
            
            rv.draw()
            
            glfw.swap_buffers(win)
            glfw.poll_events()
            
            tic = time.time() - start
            delay = 1/videoPlayer.FPS - tic
            if delay > 0:
                time.sleep(delay)
    
        glfw.terminate()
        
        
if __name__ == "__main__":
    
    from config import *
    
    GlFrameDisplayer.SHADERS = CONFIG["shaders"]
    MeshObject.SHADERS = CONFIG["shaders"]
    LabelObject.SHADERS = CONFIG["shaders"]
    
    GlRecordViewer.test(CONFIG)
        