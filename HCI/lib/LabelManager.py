# -*- coding: utf-8 -*-


import json

import glfw
import glm
from OpenGL.GL import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (Qt, pyqtSignal)

from lib.LabelObject import LabelObject
from lib.QtLabelManager import QtLabelManager
from lib.QtLabelObject import QtLabelObject


##########################################################################
class LabelManager:

    #__instance = None

    #@staticmethod
    #def getInstance():
    #    '''Static access to labelManager'''
    #    if LabelManager.__instance == None:
    #        LabelManager()
    #    return LabelManager.__instance

    ######################################################################
    def __init__(self):
        print("[LabelManager::__init__] Called")
        #initialize singleton
        # if LabelManager.__instance != None:
        #     raise Exception("This class is a singleton.")
        # else:
        #     LabelManager.__instance = self

        self.labels = {}
        self.selected = None
        self.counter = 0
        self.m_ui = None
        self.m_directoryFilePath = ""

        #self.shader= Lab   elObject.getShader()


    ######################################################################
    def init(self):
        print("[LabelManager::init] Called")
        self.shader = LabelObject.getShader()

        return self

    ######################################################################
    def save(self):
        print("[LabelManager::save] Called")
        '''Save labels in JSON object format'''
        dataJSON = []

        for label in self.labels.values():
            dataJSON.append(label.save())

        return dataJSON


    ######################################################################
    #return LabelObject
    def create(self, data=None):
        print("[LabelManager::create] Called")
        if data is None:
            ID = f"Label_{self.counter}"
            while ID in self.labels:
                self.counter += 1
                ID = f"Label_{self.counter}"
        else:
            ID = data["id"]

        print ("ID=" + ID + " data=" + str(data))

        label = LabelObject(ID=ID, data=data)
        label.setUi()

        label.s_dataUpdated.connect(self.saveToTXT)

        self.labels[ID] = label

        self.saveToTXT()

        return label

    def saveToTXT(self, path="labels.txt"):
        print("[LabelManager::saveToTXT] Called")
        """ Save labels from self in JSON string format at the path"""

        file = open(self.m_directoryFilePath + "/labels.txt", "w+") #open file on override writting mode
        dataJSON = json.dumps(self.save())
        file.write(dataJSON)
        file.close()


    ######################################################################
    def select(self, ID):
        print("[LabelManager::select] Called")
        if ID in self.labels:
            self.selected = self.labels[ID]
        else:
            self.selected = None


    ######################################################################
    def remove(self, ID):
        print("[LabelManager::remove] Called")
        if ID in self.labels:
            label = self.labels[ID]
            del self.labels[ID]
            self.saveToTXT()
            return label
        else:
            return None


    ######################################################################
    def removeSelected(self):
        print("[LabelManager::removeSelected] Called")
        if self.selected:
            ID = self.selected.id
            label = self.labels[ID]
            del self.labels[ID]
            self.saveToTXT()
            return label
        else:
            return None


    ######################################################################
    def draw(self):
        #print("[LabelManager::draw] Called")
        for ID, label in self.labels.items():
            label.draw(self.shader)

    def initFromFile(self, pathToFile):
        print ("[LabelManager::initFromFile] Called")
        print (pathToFile)

        try:
            f = open(pathToFile, "r")
            test = f.read()
            labelsRaw = json.loads(test)
            print(labelsRaw)
            for l in labelsRaw:
                print(l)
                label = self.create(data=l)
                self.m_ui.addLabelToGui(label)
        except FileNotFoundError as e:
            print ("[LabelManager::initFromFile] No labels files")
        except ValueError as e:
            print("[LabelManager::initFromFile] Nothing to read: continue")


    #@pyqtSlot()
    def removeLabel(self):
        print("[LabelManager::removeLabel] Called")
        if self.selected:
            for item in self.m_ui.ui.list.selectedItems():
                row = self.m_ui.ui.list.row(item)
                self.m_ui.ui.list.takeItem(row)

            self.removeSelected()
            self.m_ui.ui.list.clearSelection()
            self.m_ui.panel.deleteLater()
            self.m_ui.ui.removeButton.setDisabled(True)
            self.m_ui.panel.deleteLater()
            self.m_ui.panel = None

    def selectLabel(self, labelId):
        print("[LabelManager::selectLabel] Called")

        self.select(labelId)

        if self.m_ui.panel: self.m_ui.panel.deleteLater()

        if self.selected:
            print("[LabelManager::selectLabel] Selected")
            self.selected.setUi()
            self.m_ui.panel = self.selected.m_ui #QtLabelObject(self.selected)
            #self.m_ui.panel.s_dataUpdated.connect(self.saveToTXT)
            self.m_ui.ui.verticalLayout.addWidget(self.m_ui.panel)
            self.m_ui.ui.removeButton.setDisabled(False)

    def createLabel(self):
        print("[LabelManager::createLabel] Called")
        label = self.create()
        self.m_ui.addLabelToGui(label)



    def setUI (self, parent):
        print ("[LabelManager::setUI] Called")
        self.m_ui = QtLabelManager(parent)
        #QObject.connect(self.m_ui, SIGNAL("s_remove()"), self.removeLabel())
        self.m_ui.s_remove.connect(self.removeLabel)
        self.m_ui.s_select.connect(self.selectLabel)
        self.m_ui.s_create.connect(self.createLabel)
        print("[LabelManager::setUI] End")
        return self.m_ui

    def setDirectoryFilePath(self, filePath):
        self.m_directoryFilePath = filePath

    ######################################################################
    @staticmethod
    def test(config):

        import time
        LabelObject.SHADERS = config["shaders"]

        W, H = 640, 360
        glfw.init()
        win = glfw.create_window(W, H, "Label Object", None, None)
        glfw.make_context_current(win)

        labelManager = LabelManager.GetInstance()

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