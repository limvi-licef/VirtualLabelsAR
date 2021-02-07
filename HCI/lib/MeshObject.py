# -*- coding: utf-8 -*-


import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import OpenGL.arrays.vbo as vbo
import glfw
import glm
import ctypes as ct
from os.path import join


##########################################################################
class MeshObject:
    
    
    SHADERS = ""
    
    
    ######################################################################
    def __init__(self, data, context=True):
        
        if type(data)==list:
            self.buildFromList(data)
        else:
            self.buildFromDict(data)
            
        if context: self.prepare()
        
        
    ######################################################################
    def buildFromList(self, data):
        
        self.id = data[0]
        self.vt = data[1]
        self.nt = data[2]
        self.vertices = data[3]
        self.normals = data[4]
        self.indices = data[5]
            

    ######################################################################
    def buildFromDict(self, data):
        
            self.id = data["Surface"]["SurfaceId"]
            self.vt = np.array(data["Surface"]["VertexTransform"]).reshape((4,4))
            self.nt = np.array(data["Surface"]["NormalTransform"]).reshape((4,4))
            self.vertices = np.array([
                data["Surface"]["Vertices"]["x"],
                data["Surface"]["Vertices"]["y"],
                data["Surface"]["Vertices"]["z"],
                data["Surface"]["Vertices"]["w"]
            ], dtype=np.float32).transpose()
            self.normals = np.array([
                data["Surface"]["Normals"]["x"],
                data["Surface"]["Normals"]["y"],
                data["Surface"]["Normals"]["z"]
            ], dtype=np.float32).transpose()
            self.indices = np.array(data["Surface"]["Indices"], dtype=np.uint32)
            
        
    ######################################################################
    def prepare(self):
        
        self.vertexTransform = glm.mat4(self.vt)
        self.normalTransform = glm.mat4(self.nt)
        self.vert_vbo = vbo.VBO(self.vertices)
        self.norm_vbo = vbo.VBO(self.normals)
        self.ind_vbo = vbo.VBO(self.indices, target=GL_ELEMENT_ARRAY_BUFFER)
        
        
    ######################################################################
    def draw(self, shader, mode="triangle"):
        
        glUseProgram(shader)
        glUniformMatrix4fv(shader.uVertexTransform, 1, False, glm.value_ptr(self.vertexTransform))
        glUniformMatrix4fv(shader.uNormalTransform, 1, False, glm.value_ptr(self.normalTransform))
        
        self.ind_vbo.bind()
        
        self.vert_vbo.bind()
        glEnableVertexAttribArray(shader.aPos)
        glVertexAttribPointer(shader.aPos, 4, GL_FLOAT, False, 0, ct.c_void_p(0))
        self.vert_vbo.unbind()

        self.norm_vbo.bind()
        glEnableVertexAttribArray(shader.aNorm)
        glVertexAttribPointer(shader.aNorm, 3, GL_FLOAT, False, 0, ct.c_void_p(0))
        self.norm_vbo.unbind()

        if mode =="point":
            glDrawElements(GL_POINTS, self.indices.shape[0], GL_UNSIGNED_INT, ct.c_void_p(0));
        else:
            glDrawElements(GL_TRIANGLES, self.indices.shape[0], GL_UNSIGNED_INT, ct.c_void_p(0))

        self.ind_vbo.unbind()
        glUseProgram(0)
        
        
    ######################################################################
    def save(self):
        
        return [
            self.id,
            self.vt,
            self.nt,
            self.vertices,
            self.normals,
            self.indices
        ]
        
        
    ######################################################################
    @staticmethod
    def getShader():
        
        assert MeshObject.SHADERS != "", "MeshObject.SHADERS not set"
        VERTEX = join(MeshObject.SHADERS, "mesh.vs")
        FRAGMENT = join(MeshObject.SHADERS, "mesh.fs")
        
        meshShader = shaders.compileProgram(
            shaders.compileShader(open(VERTEX).read(), GL_VERTEX_SHADER),
            shaders.compileShader(open(FRAGMENT).read(), GL_FRAGMENT_SHADER)
            )
        glUseProgram(meshShader)
        meshShader.uModelview = glGetUniformLocation(meshShader, "uModelview")
        meshShader.uProjection = glGetUniformLocation(meshShader, "uProjection")
        meshShader.uNormalTransform = glGetUniformLocation(meshShader, "uNormalTransform")
        meshShader.uVertexTransform = glGetUniformLocation(meshShader, "uVertexTransform")
        meshShader.aPos = glGetAttribLocation(meshShader, "aPos")
        meshShader.aNorm = glGetAttribLocation(meshShader, "aNorm")
        
        return meshShader
        
        
    ######################################################################
    @staticmethod
    def test(config):
        
        import time
        MeshObject.SHADERS = config["shaders"]
        
        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Mesh Object", None, None)
        glfw.make_context_current(win)

        meshShader = MeshObject.getShader()
        
        vertexMat4 = np.array([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
            ], dtype=np.float32).reshape((4,4))
        normalMat4 = np.array([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
            ], dtype=np.float32).reshape((4,4))
        vertices = np.array([
            -0.5, -0.5,  0.5, 1.0,
             0.5,  0.5,  0.5, 1.0,
             0.5, -0.5,  0.5, 1.0,
             0.5, -0.5, -0.5, 1.0,
            ], dtype=np.float32)
        normals = np.array([
            0.0,  0.0,  1.0,
            1.0,  0.0,  1.0,
            1.0,  0.0,  1.0,
            1.0,  0.0,  0.0,
            ], dtype=np.float32)
        indices = np.array([
            0, 1, 2,
            1, 2, 3
            ], dtype=np.uint32)
        
        meshObject = MeshObject([123456789, vertexMat4, normalMat4, vertices, normals, indices])
        
        glUseProgram(meshShader)
        projection = glm.perspective(glm.radians(75), W/H, 0.25, 5.0)
        glUniformMatrix4fv(meshShader.uProjection, 1, False, glm.value_ptr(projection))
        
        rotation = glm.mat4()
        
        glClearColor(0.1, 0.3, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        while not glfw.window_should_close(win):
            
            start = time.time()
            rotation = glm.rotate(rotation, glm.radians(45/30), (0,1,0))
            
            modelview = glm.mat4()
            modelview = glm.translate(modelview, (0,0,-1.5))
            modelview = modelview * rotation
            
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glUseProgram(meshShader)
            glUniformMatrix4fv(meshShader.uModelview, 1, False, glm.value_ptr(modelview))
            meshObject.draw(meshShader)
            
            glfw.swap_buffers(win)
            glfw.poll_events()
            
            tic = time.time() - start
            delay = 1/30 - tic
            if delay > 0:
                time.sleep(delay)
    
        glfw.terminate()
        
        
if __name__ == "__main__":
    
    from config import *
    
    MeshObject.test(CONFIG)        
        