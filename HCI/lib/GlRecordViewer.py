# -*- coding: utf-8 -*-


import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import OpenGL.arrays.vbo as vbo
import glfw
import glm
import ctypes as ct
from os.path import join
from lib.LabelManager import LabelManager
from lib.DataManager import DataManager
from lib.GlFrameDisplayer import GlFrameDisplayer
from lib.Matrix import Matrix
from lib.MeshObject import MeshObject
from PyQt5 import QtCore, QtGui, QtWidgets


##########################################################################
class GlRecordViewer:

    ######################################################################
    def __init__(self, videoSize, labelManager, dataManager):

        self.m_glInitialized = False
        self.nframe = 0
        #self.labelqt = 0
        self.m_videoSize = videoSize
        self.m_labelManager = labelManager
        self.m_dataManager = dataManager

    def initializeGl(self):
        self.frameDisplayer = GlFrameDisplayer()
        # print("IIIINNNNNIIIITTTT")
        # self.data = data
        #self.m_labelManager = labelManager.init()
        #self.m_dataManager = dataManager.init()
        self.m_labelManager.initializeGl()
        self.m_dataManager.init()

        projection = glm.perspective(glm.radians(28), 16 / 9, 0.25, 5.0)

        glClearColor(0.1, 0.3, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)

        # w, h = videoSize
        # self.frameDisplayer.setTexture(w, h)
        self.frameDisplayer.setTexture(self.m_videoSize[0], self.m_videoSize[1])

        self.meshShader = MeshObject.getShader()
        glUseProgram(self.meshShader)
        glUniformMatrix4fv(self.meshShader.uProjection, 1, False, glm.value_ptr(projection))

        glUseProgram(self.m_labelManager.shader)
        glUniformMatrix4fv(self.m_labelManager.shader.uProjection, 1, False, glm.value_ptr(projection))

        # Moved to DataManager
        # self.meshes = []
        # for idMesh, meshData in data["meshes"].items():
        #    mesh = MeshObject(meshData)
        #    self.meshes.append(mesh)

        self.m_glInitialized = True

    ######################################################################
    #def init(self):

        # self.frameDisplayer = GlFrameDisplayer()
        # # print("IIIINNNNNIIIITTTT")
        # #self.data = data
        # self.m_labelManager = labelManager.init()
        # self.m_dataManager = dataManager.init()
        #
        # self.projection = glm.perspective(glm.radians(28), 16 / 9, 0.25, 5.0)
        #
        # glClearColor(0.1, 0.3, 0.4, 1.0)
        # glEnable(GL_DEPTH_TEST)
        #
        # w, h = videoSize
        # self.frameDisplayer.setTexture(w, h)
        #
        # self.meshShader = MeshObject.getShader()
        # glUseProgram(self.meshShader)
        # glUniformMatrix4fv(self.meshShader.uProjection, 1, False, glm.value_ptr(self.projection))
        #
        # glUseProgram(self.m_labelManager.shader)
        # glUniformMatrix4fv(self.m_labelManager.shader.uProjection, 1, False, glm.value_ptr(self.projection))
        #
        # # Moved to DataManager
        # #self.meshes = []
        # #for idMesh, meshData in data["meshes"].items():
        # #    mesh = MeshObject(meshData)
        # #    self.meshes.append(mesh)
        #
        # self.initialized = True

    ######################################################################
    def receive(self, nframe, frame):

        if self.m_glInitialized and self.frameDisplayer:
            #self.nframe = nframe if nframe < len(self.data["sync"]) else len(self.data["sync"]) - 1
            self.nframe = nframe if nframe < len(self.m_dataManager.getSync()) else len(self.m_dataManager.getSync()) - 1
            self.frameDisplayer.receive(frame)

    ######################################################################
    def draw(self):

        if self.m_glInitialized:
            # print("DDDDDRRRRRRRAAAAWWWWW")
            #idCam = self.data["sync"][self.nframe]
            idCam = self.m_dataManager.getSync()[self.nframe]
            #infoCam = self.data["camera"][idCam]
            infoCam = self.m_dataManager.getCameraInfo()[idCam]

            glClear(GL_COLOR_BUFFER_BIT)

            self.frameDisplayer.draw()

            glClear(GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.meshShader)
            # glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            position = Matrix.fromList(infoCam["position"])
            rotation = Matrix.fromList(infoCam["rotation"], toTranspose=True)
            modelview = rotation * position
            glUniformMatrix4fv(self.meshShader.uModelview, 1, False, glm.value_ptr(modelview))
            for mesh in self.m_dataManager.getMesh():
                mesh.draw(self.meshShader)
            #for mesh in self.meshes:
            #    mesh.draw(self.meshShader)

            #DataManager.m_currentTimestamp = infoCam["time"]
            self.m_dataManager.setTimeStamp(infoCam["time"])

            #LabelObject.cameraTranslation = glm.mat4(Matrix.fromList(infoCam["position"]))
            #LabelObject.cameraRotation = glm.mat4(Matrix.fromList(infoCam["rotation"]))

            glUseProgram(self.m_labelManager.shader)
            glUniformMatrix4fv(self.m_labelManager.shader.uModelview, 1, False, glm.value_ptr(modelview))

            self.m_labelManager.draw()

    ######################################################################
    @staticmethod
    def test(config):

        import time
        import glm
        import sys
        from lib.VideoPlayer import VideoPlayer
        from json import loads
        from lib.LabelManagerView import LabelManagerView
        from lib.LabelObject import LabelObject

        with open(config["rec_test"], mode="r") as datafile:
            data = loads(datafile.read())
        LabelObject.SHADERS = config["shaders"]
        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Mesh Object", None, None)
        glfw.make_context_current(win)

        app = QtWidgets.QApplication(sys.argv)
        root = QtWidgets.QWidget()
        root.layout = QtWidgets.QVBoxLayout()
        labelManager = LabelManagerView()
        root.layout.addWidget(labelManager)
        root.setLayout(root.layout)

        videoPlayer = VideoPlayer(data["video"])
        videoPlayer.play()
        Manage = LabelManager()

        glUseProgram(labelManager.manager.shader)
        projection = glm.perspective(glm.radians(28), W / H, 0.25, 5.0)
        glUniformMatrix4fv(labelManager.manager.shader.uProjection, 1, False, glm.value_ptr(projection))
        modelview = glm.translate(glm.mat4(), (0, 0, -0.5))
        glUniformMatrix4fv(labelManager.manager.shader.uModelview, 1, False, glm.value_ptr(modelview))

        def draw():

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            labelManager.manager.draw()

            glfw.swap_buffers(win)
            glfw.poll_events()

        rv = GlRecordViewer()
        rv.init((videoPlayer.WIDTH, videoPlayer.HEIGHT), data, Manage)

        while not glfw.window_should_close(win):

            start = time.time()

            _, frame = videoPlayer.read()
            if _: rv.receive(videoPlayer.getFrameNumber(), frame)

            rv.draw()
            labelManager.manager.draw()
            glfw.swap_buffers(win)
            glfw.poll_events()

            tic = time.time() - start
            delay = 1 / videoPlayer.FPS - tic
            if delay > 0:
                time.sleep(delay)
            ###TESTLUCAS1
            labelManager.timer = QtCore.QTimer()
            # labelManager.timer.timeout.connect(draw)
            labelManager.timer.start(int(1000 / 30))
            root.setWindowTitle("QtLabelManager")
            root.show()
        # e = app.exec_()
        glfw.terminate()
        # sys.exit(e)

        ###TESTLUCAS2

        # glfw.terminate()


if __name__ == "__main__":
    from config import *

    GlFrameDisplayer.SHADERS = CONFIG["shaders"]
    MeshObject.SHADERS = CONFIG["shaders"]
    LabelObject.SHADERS = CONFIG["shaders"]

    GlRecordViewer.test(CONFIG)
