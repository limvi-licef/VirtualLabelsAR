# -*- coding: utf-8 -*-


from glm import (
    mat4, mat3, vec3, vec2,
    translate, rotate, transpose, normalize,
    dot, radians, degrees, asin, acos, value_ptr)

from numpy import array, float32, sign


################################################################
class Matrix:
    
    ############################################################
    @staticmethod
    def fromList(lst, toTranspose=False):
        temp = array(lst, dtype=float32).reshape((4, 4))

        mat = mat4(temp.tolist())
        
        if toTranspose: mat = transpose(mat)
        
        return mat
    
    
    ############################################################
    @staticmethod
    def getTranslation(matrix4):
        
        return vec3(list(matrix4[3])[0:4])
    
    
    ############################################################
    @staticmethod
    def getRotation(matrix4):
        
        return mat3([
            list(matrix4[0])[0:3],
            list(matrix4[1])[0:3],
            list(matrix4[2])[0:3]
            ])
    
    
    ############################################################
    @staticmethod
    def getGaze(matrix3):
        
        return matrix3 * vec3(0,0,-1)
    
    
    ############################################################
    @staticmethod
    def getAngles(matrix3):
        
        dot_y = dot(vec2(0,-1), normalize((matrix3 * vec3(0,0,-1)).xz))
        sign_y = -sign(dot(vec3(1,0,0), (matrix3 * vec3(0,0,-1))))
        ry = acos(dot_y) * sign_y
        
        m3 = mat3(rotate(mat4(matrix3), -ry, (0,1,0)))
        
        dot_x = dot(vec3(0,1,0), matrix3 * vec3(0,1,0))
        sign_x = -sign(dot(vec3(0,0,-1), (m3 * vec3(0,1,0))))
        rx = acos(dot_x) * sign_x
        
        return vec2(degrees(rx), degrees(ry))
    
    
    ############################################################
    @staticmethod
    def test(config):
        
        mat = Matrix.fromList([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
            ])
        mat = translate(mat, (1,2,3))
        mat = rotate(mat, radians(-40), (0,1,0))
        mat = rotate(mat, radians(89), (1,0,0))
        
        translation = Matrix.getTranslation(mat)
        rotation = Matrix.getRotation(mat)
        gaze = Matrix.getGaze(rotation)
        angles = Matrix.getAngles(rotation)
        
        print("translation", translation)
        print("gaze", gaze)
        print("angles", angles)
        
        
        
if __name__ == "__main__":
    
    from config import *
    
    Matrix.test(CONFIG)      
    