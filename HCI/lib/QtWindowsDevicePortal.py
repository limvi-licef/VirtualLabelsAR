# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from ui.Ui_WindowsDevicePortal import Ui_WindowsDevicePortal
from lib.WindowsDevicePortal import WindowsDevicePortal
from lib.Matrix import Matrix
from numpy import array


###########################################################################
class QtWindowsDevicePortal(QtWidgets.QWidget):
    
    
    #######################################################################
    def __init__(self, parent=None):
        
        QtWidgets.QWidget.__init__(self, parent)
        
        WindowsDevicePortal().interface(self)
        
        self.ui = Ui_WindowsDevicePortal()
        self.ui.setupUi(self)
    
        self.batteryTimer = QtCore.QTimer()
        self.batteryTimer.timeout.connect(self.updateBattery)
        self.batteryTimer.start(2000)
    
        self.previewTimer = QtCore.QTimer()
        self.previewTimer.timeout.connect(self.updatePreview)
        
        self.previewOn = False


    #######################################################################
    def _disable(self, b):
        
        self.ui.connectButton.setDisabled(b)
        self.ui.hostInput.setDisabled(b)
        self.ui.loginInput.setDisabled(b)
        self.ui.passwordInput.setDisabled(b)
        self.ui.previewButton.setDisabled(not b)


    #######################################################################
    def updateBattery(self):
        
        b = self.getBattery()
        self.ui.batteryLevel.setText(b)
        
        if not self.isConnected():
            self._disable(False)


    #######################################################################
    def setupConnection(self):
        
        host = self.ui.hostInput.text()
        login = self.ui.loginInput.text()
        password = self.ui.passwordInput.text()
        
        self.connect(host, auth=(login, password), certfile="resources/holocert")
        
        if self.isConnected():
            self._disable(True)


    #######################################################################
    def togglePreview(self):
        
        self.previewOn = not self.previewOn
        
        if self.previewOn:
            self.ui.previewButton.setText("Off")
            self.previewTimer.start(1)
            self.sendData("activeclient")
            self.sendData("resumetracking")
        else:
            self.ui.previewButton.setText("On")
            self.previewTimer.stop()
            self.ui.previewInfo.setText("")


    #######################################################################
    def updatePreview(self):
        
        data = self.getData()
        
        if self.isConnected() and "TrackingState" in data:
            
            origin = Matrix.fromList(data["OriginToAttachedFor"])
            translation = map(lambda x: round(x, 2), Matrix.getTranslation(origin))
            
            head = Matrix.fromList(data["HeadToAttachedFor"], toTranspose=True)
            rotation = Matrix.getRotation(head)
            gaze = map(lambda x: round(x, 2), Matrix.getGaze(rotation))
            
            preview = f"""
Position: {list(translation)}
Gaze: {list(gaze)}
            """
            
            self.ui.previewInfo.setText(preview)
            
            
    #######################################################################
    @staticmethod
    def test(config):
        
        import sys
        
        app = QtWidgets.QApplication(sys.argv)
        wdp = QtWindowsDevicePortal()
        
        wdp.ui.hostInput.setText(config["host"])
        wdp.ui.loginInput.setText(config["auth"][0])
        wdp.ui.passwordInput.setText(config["auth"][1])
        
        wdp.show()
        app.exec_()
        
        
if __name__ == "__main__":
    
    from config import *
    from compiler import *
    
    QtWindowsDevicePortal.test(CONFIG)
