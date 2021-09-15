import glfw
import glm
from lib.Matrix import Matrix
from lib.MeshObject import MeshObject
from OpenGL.GL import *

##########################################################################
class DataManager:

    m_currentTimestamp = 0 #updated by GlRecordViewer to keep track of the camera frame being viewed
    m_cameraInfos = {} #dictionary<timestamp,cameraInfo>

    m_labelTranslationOffset = glm.mat4([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1, 0.0, 0.0],
                [0.0, 0.0, 1, 0.0],
                [0.02, -0.1,-0.5, 1.0]]) #correspond to [x,y,z,1.0]

    m_mesh = []
    m_sync = []
    m_camera = []

    #@staticmethod
    def getCameraInfoFromTimestamp(self,timestamp):
        """
        @return return the camera information with the corresponding timestamp
        """
        return self.m_cameraInfos[timestamp]

    def getCameraInfo(self):
        return self.m_camera

    def __init__(self, data=None):
        #print("[DataManager::__init__] Called")

        for cameraInfo in data["camera"]:
            self.m_cameraInfos[cameraInfo["time"]] = cameraInfo

        for meshId, meshData in data["meshes"].items():
            mesh = MeshObject(meshData)
            self.m_mesh.append(mesh)

        self.m_sync = data["sync"]
        self.m_camera = data["camera"]

    def getMesh(self):
        return self.m_mesh

    def getSync(self):
        return self.m_sync

    def getCurrentTimestamp(self):
        return self.m_currentTimestamp

    def setTimeStamp(self, timestamp):
        #print ("[DataManager::setTimeStamp] timestamp to set: " + str(timestamp))
        self.m_currentTimestamp = timestamp

    ######################################################################
    def init(self, timestamp=0):
        print("[CameraManager::init] Called")
        self.m_currentTimestamp = timestamp
        return self

    #@staticmethod
    def convertCameraToWorld(self,position, timestamp):
        """
        Calculate the position in world coordinate from position in camera referential (camera pose + translation offset)
        @return position in world coordinate
        """
        cameraInfo = self.getCameraInfoFromTimestamp(timestamp)
        cameraTranslation = glm.mat4(Matrix.fromList(cameraInfo["position"]))
        cameraRotation = glm.mat4(Matrix.fromList(cameraInfo["rotation"]))

        return cameraTranslation * cameraRotation * DataManager.m_labelTranslationOffset * position

    #@staticmethod
    def convertWorldToCamera(self,position, timestamp):
        """
        Calculate the position in camera referential (camera pose + translation offset) from world coordinate position
        @return position in world coordinate
        """
        #cameraInfo = DataManager.getCameraInfoFromTimestamp(timestamp)
        cameraInfo = self.getCameraInfoFromTimestamp(timestamp)
        cameraTranslation = glm.mat4(Matrix.fromList(cameraInfo["position"]))
        cameraRotation = glm.mat4(Matrix.fromList(cameraInfo["rotation"]))

        return glm.inverse(cameraTranslation * cameraRotation * DataManager.m_labelTranslationOffset) * position

    #@staticmethod
    def calculateRealPosition(self,positionSetting, timestamp):
        """
        @positionSetting: position set by user in camera referential
        @timestamp: timestamp of the camera to get the camera transform
        @return position in world coordinate
        """
        return self.convertCameraToWorld(positionSetting, timestamp)

    #@staticmethod
    def getPositionSetting(self,position, timestamp):
        """
        @position: position in world coordinate
        @timestamp: timestamp of the camera to get the camera transform
        @return position set by the user in camera referential
        """
        return self.convertWorldToCamera(position, timestamp)

