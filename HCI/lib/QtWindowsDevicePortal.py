# -*- coding: utf-8 -*-


############################################################################################
# Packages
from PyQt5 import QtCore, QtGui, QtWidgets
from numpy import array

# Ui
#from compiler import *
from ui.Ui_WindowsDevicePortal import Ui_WindowsDevicePortal

# Lib
from lib.WindowsDevicePortal import WindowsDevicePortal
from lib.Matrix import Matrix

from config import *

###########################################################################
class QtWindowsDevicePortal(WindowsDevicePortal, QtWidgets.QWidget):
    
    
    """
        Widget wrapper of WindowsDevicePortal.
    """
    
    
    #######################################################################
    def __init__(self, parent=None):
        
        """
            Constructor.
        """
        
        # initialize with father constructor
        QtWidgets.QWidget.__init__(self, parent)
        WindowsDevicePortal.__init__(self)
        
        # setup ui
        self.ui = Ui_WindowsDevicePortal()
        self.ui.setupUi(self)
        self.ui.hostInput.setText(CONFIG["host"])
        self.ui.loginInput.setText(CONFIG["auth"][0])
        self.ui.passwordInput.setText(CONFIG["auth"][1])

        # Preview is currently not used, so hidden for the user. Code remains here as it might be useful later
        self.ui.previewButton.setVisible(False)
        self.ui.previewLabel.setVisible(False)
        
        # prepare timers and set preview state
        self._initTimers()
        self.previewOn = False


    #######################################################################
    def _initTimers(self):
        
        """
            Initialize a timer for battery charging level display and preview.
        """
    
        self.batteryTimer = QtCore.QTimer()
        self.batteryTimer.timeout.connect(self._updateBattery)
        self.batteryTimer.start(2000)
    
        self.previewTimer = QtCore.QTimer()
        self.previewTimer.timeout.connect(self._updatePreview)
        

    #######################################################################
    def _disable(self, b):
        
        """
            Enable control of inputs.
            
            @param b: bool, indicates if line edit must be enabled
        """
        
        self.ui.connectButton.setDisabled(b)
        self.ui.hostInput.setDisabled(b)
        self.ui.loginInput.setDisabled(b)
        self.ui.passwordInput.setDisabled(b)
        self.ui.previewButton.setDisabled(not b)


    #######################################################################
    def _updateBattery(self):
        
        """
            Display update of battery charging level.
        """
        
        b = self.getBattery()
        self.ui.batteryLevel.setText(b)
        
        # check if still connected
        if not self.isConnected():
            self._disable(False)


    #######################################################################
    def _updatePreview(self):
        
        """
            Display update of Hololens tracking information.
        """
        
        # get data from websocket
        data = self.getData()
        
        # if still connected and received data are tracking information
        if self.isConnected() and "TrackingState" in data:
            
            # build translation matrix
            origin = Matrix.fromList(data["OriginToAttachedFor"])
            translation = map(lambda x: round(x, 2), Matrix.getTranslation(origin))
            
            # build rotation matrix and computer gaze
            head = Matrix.fromList(data["HeadToAttachedFor"], toTranspose=True)
            rotation = Matrix.getRotation(head)
            gaze = map(lambda x: round(x, 2), Matrix.getGaze(rotation))
            
            # display info
            preview = f"Position: {list(translation)}\n"
            preview += f"Gaze: {list(gaze)}"
            self.ui.previewInfo.setText(preview)


    #######################################################################
    def connection(self):
        
        """
            Button event.
        """
        
        # pick up lineEdit text inputs
        host = self.ui.hostInput.text()
        login = self.ui.loginInput.text()
        password = self.ui.passwordInput.text()
        
        # try connect
        self.connect(host, auth=(login, password), certfile=CONFIG["certfile"] )
        if self.isConnected():
            self._disable(True)


    #######################################################################
    def togglePreview(self):
        
        # swap preview state
        self.previewOn = not self.previewOn
        
        if self.previewOn:
            self.ui.previewButton.setText("Off") # change text of preview button
            self.previewTimer.start(1) # start preview display
            # ask new data to hololens
            self.sendData("activeclient")
            self.sendData("resumetracking")
            
        else:
            self.ui.previewButton.setText("On") # change text of preview button
             # stop preview display and clear info
            self.previewTimer.stop()
            self.ui.previewInfo.setText("")

    # This function does not seem to be used in the project
    # #######################################################################
    # def activatePreview(self):
    #
    #     """
    #         Activate the preview.
    #     """
    #
    #     if not self.previewOn:
    #         self.togglePreview()


    #######################################################################
    def stopPreview(self):
        
        """
            Stop the preview.
        """
        
        if self.previewOn:
            self.togglePreview()
            
            
    #######################################################################
    @staticmethod
    def test(config):
        
        import sys
        
        app = QtWidgets.QApplication(sys.argv)
        wdp = QtWindowsDevicePortal()
        
        wdp.ui.hostInput.setText(config["host"])
        wdp.ui.loginInput.setText(config["auth"][0])
        wdp.ui.passwordInput.setText(config["auth"][1])
        
        wdp.setWindowTitle("QtVideoPlayer")
        wdp.show()
        sys.exit(app.exec_())
        
        
###########################################################################
if __name__ == "__main__":
    
    from config import *
    
    QtWindowsDevicePortal.test(CONFIG)
