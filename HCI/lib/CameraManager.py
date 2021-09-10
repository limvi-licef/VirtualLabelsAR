import glfw
import glm
from lib.Matrix import Matrix
from OpenGL.GL import *

##########################################################################
class CameraManager:

    m_currentTimestamp = 0 #updated by GlRecordViewer to keep track of the camera frame being viewed
    __cameraInfos = {} #dictionary<timestamp,cameraInfo>

    __labelTranslationOffset = glm.mat4([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1, 0.0, 0.0],
                [0.0, 0.0, 1, 0.0],
                [0.02, -0.1,-0.5, 1.0]]) #correspond to [x,y,z,1.0]

    @staticmethod
    def getCameraInfo(timestamp):
        """
        @return return the camera information with the corresponding timestamp
        """
        return CameraManager.__cameraInfos[timestamp]

    def __init__(self, data=None):
        print("[CameraManager::__init__] Called")

        for cameraInfo in data["camera"]:
            self.__cameraInfos[cameraInfo["time"]] = cameraInfo

    ######################################################################
    def init(self, timestamp=0):
        print("[CameraManager::init] Called")
        CameraManager.m_currentTimestamp = timestamp
        return self

    @staticmethod
    def convertCameraToWorld(position, timestamp):
        """
        Calculate the position in world coordinate from position in camera referential (camera pose + translation offset)
        @return position in world coordinate
        """
        cameraInfo = CameraManager.getCameraInfo(timestamp)
        cameraTranslation = glm.mat4(Matrix.fromList(cameraInfo["position"]))
        cameraRotation = glm.mat4(Matrix.fromList(cameraInfo["rotation"]))

        return cameraTranslation * cameraRotation * CameraManager.__labelTranslationOffset * position

    @staticmethod
    def convertWorldToCamera(position, timestamp):
        """
        Calculate the position in camera referential (camera pose + translation offset) from world coordinate position
        @return position in world coordinate
        """
        cameraInfo = CameraManager.getCameraInfo(timestamp)
        cameraTranslation = glm.mat4(Matrix.fromList(cameraInfo["position"]))
        cameraRotation = glm.mat4(Matrix.fromList(cameraInfo["rotation"]))

        return glm.inverse(cameraTranslation * cameraRotation * CameraManager.__labelTranslationOffset) * position

    @staticmethod
    def calculateRealPosition(positionSetting, timestamp):
        """
        @positionSetting: position set by user in camera referential
        @timestamp: timestamp of the camera to get the camera transform
        @return position in world coordinate
        """
        return CameraManager.convertCameraToWorld(positionSetting, timestamp)

    @staticmethod
    def getPositionSetting(position, timestamp):
        """
        @position: position in world coordinate
        @timestamp: timestamp of the camera to get the camera transform
        @return position set by the user in camera referential
        """
        return CameraManager.convertWorldToCamera(position, timestamp)