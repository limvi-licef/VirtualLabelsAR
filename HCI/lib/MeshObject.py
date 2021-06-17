# -*- coding: utf-8 -*-


##########################################################################
# Packages
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
    
    
    SHADERS = "" # shader file location
    
    
    ######################################################################
    def __init__(self, data, context=True):
        
        """
            Constructor. Takes data and prepares buffer if an OpenGL context exists.
            
            @arg data: list or dict, data of mesh
            @arg context: bool that indicates if OpenGL buffers should be prepared
        """

        if type(data)==list:
            self._buildFromList(data)
        else:
            self._buildFromDict(data)
            
        if context: self.prepare()
        
        
    ######################################################################
    def _buildFromList(self, data):
        
        """
            Called in constructor. Build arrays of data from a list of saved data.
            
            @arg data: list of arrays.
        """

        self.id = data[0]
        print ("_buildFromList called")
        print (data[1])
        #self.vt = np.array(data[1], dtype=np.float32)
        self.vt = data[1]
        #self.nt = np.array(data[2], dtype=np.float32)
        self.nt = data[2]
        self.vertices = np.array(data[3], dtype=np.float32)
        self.normals = np.array(data[4], dtype=np.float32)
        self.indices = np.array(data[5], dtype=np.uint32)
            

    ######################################################################
    def _buildFromDict(self, data):
        
        """
            Called in constructor. Build arrays of data from a dict provided by WDP (via websocket).
            
            @arg data: dict of data.
        """

        print ("_buildFromDict called")

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
        
        """
            Creates buffers from arrays of data.
        """

        print ("prepare called")
        self.vertexTransform = glm.mat4(self.vt)
        self.normalTransform = glm.mat4(self.nt)
        self.vert_vbo = vbo.VBO(self.vertices)
        self.norm_vbo = vbo.VBO(self.normals)
        self.ind_vbo = vbo.VBO(self.indices, target=GL_ELEMENT_ARRAY_BUFFER)
        
        
    ######################################################################
    def draw(self, shader, mode="triangle"):
        
        """
            Draw mesh by using a shader program.
            
            @arg shader: shader program object to use
            @arg mode: str, draw mode ('point', 'lines', 'triangles')
        """
        
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
        if mode =="lines":
            glDrawElements(GL_LINE_LOOP, self.indices.shape[0], GL_UNSIGNED_INT, ct.c_void_p(0));
        else:
            glDrawElements(GL_TRIANGLES, self.indices.shape[0], GL_UNSIGNED_INT, ct.c_void_p(0))

        self.ind_vbo.unbind()
        glUseProgram(0)
        
        
    ######################################################################
    def save(self):
        
        """
            Return an array which contains all mesh information.
            
            @return array of arrays
        """
        
        return [
            self.id,
            self.vt.tolist(),
            self.nt.tolist(),
            self.vertices.tolist(),
            self.normals.tolist(),
            self.indices.tolist()
        ]
        
        
    ######################################################################
    @staticmethod
    def getShader():
        
        """
            Static method for getting the shader program
        """
        
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
        
        # set the shader location
        MeshObject.SHADERS = config["shaders"]
        
        # start OpenGL
        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Mesh Object", None, None)
        glfw.make_context_current(win)
        meshShader = MeshObject.getShader() # get the shader program
        
        # create some data for creating a mesh object
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
        
        # set projection matrix
        glUseProgram(meshShader)
        projection = glm.perspective(glm.radians(75), W/H, 0.25, 5.0)
        glUniformMatrix4fv(meshShader.uProjection, 1, False, glm.value_ptr(projection))
        
        # scene rotation matrix
        rotation = glm.mat4()
        
        glClearColor(0.1, 0.3, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        while not glfw.window_should_close(win):
            
            start = time.time()
            
            # scene rotation
            rotation = glm.rotate(rotation, glm.radians(45/30), (0,1,0))
            
            # compute new modelview matrix
            modelview = glm.mat4()
            modelview = glm.translate(modelview, (0,0,-1.5))
            modelview = modelview * rotation
            
            # rendering
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glUseProgram(meshShader)
            glUniformMatrix4fv(meshShader.uModelview, 1, False, glm.value_ptr(modelview))
            meshObject.draw(meshShader)
            
            # frame update
            glfw.swap_buffers(win)
            glfw.poll_events()
            
            # time control
            tic = time.time() - start
            delay = 1/30 - tic
            if delay > 0:
                time.sleep(delay)
    
        glfw.terminate()
        
        
if __name__ == "__main__":
    
    from config import *
    
    MeshObject.test(CONFIG)        
        