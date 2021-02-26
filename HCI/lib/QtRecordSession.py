# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from lib.RecordSession import RecordSession
from ui.Ui_RecordSession import Ui_RecordSession


class QtRecordSession(QtWidgets.QWidget):
    
    
    VIDEOPATH = ""
    
    
    def __init__(self, parent=None):
        
        QtWidgets.QWidget.__init__(self, parent)        
        self.ui = Ui_RecordSession()
        self.ui.setupUi(self)
        
        self.rs = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.ping)
        
        
    def setWdp(self, wdp):
        
        self.wdp = wdp
        self.rs = RecordSession(wdp.wdp)
        
        
    def start(self):
        
        if self.rs and self.rs.start():
            self.wdp.stopPreview()
            self.ui.recordButton.setDisabled(True)
            self.ui.stopButton.setDisabled(False)
            self.ui.saveButton.setDisabled(True)
            self.ui.time.setDisabled(False)
            self.timer.start(1)
            self.ui.progressBar.setValue(0)
        
        
    def stop(self):
        
        if self.rs and self.rs.stop():
            self.ui.recordButton.setDisabled(True)
            self.ui.stopButton.setDisabled(True)
            self.ui.saveButton.setDisabled(False)
            self.ui.time.setDisabled(True)
            self.timer.stop()
            
            
    def save(self):
        
        if self.rs:
            
            file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
            self.rs.wdp.download_callback = lambda x: self.ui.progressBar.setValue(int(x*100)) and self.update()
            self.rs.save(file, QtRecordSession.VIDEOPATH)
            
            self.ui.recordButton.setDisabled(False)
            self.ui.stopButton.setDisabled(True)
            self.ui.saveButton.setDisabled(True)
            self.ui.time.setDisabled(True)
        
        
    def ping(self):
        
        if self.rs:
            typ, data = self.rs.ping()
            
            t = data["time"]
            s = str(int(t % 60)).zfill(2)
            m = int(t/60)
            self.ui.time.setText(f"{m}:{s}")
        
        
    @staticmethod
    def test(config):
        
        import sys
        from lib.QtWindowsDevicePortal import QtWindowsDevicePortal
        
        QtRecordSession.VIDEOPATH = config["rec_video"]
        
        app = QtWidgets.QApplication(sys.argv)
        root = QtWidgets.QWidget()
        root.layout = QtWidgets.QVBoxLayout()
        
        wdp = QtWindowsDevicePortal()
        wdp.ui.hostInput.setText(config["host"])
        wdp.ui.loginInput.setText(config["auth"][0])
        wdp.ui.passwordInput.setText(config["auth"][1])
        
        recordSession = QtRecordSession()
        recordSession.setWdp(wdp)
        
        root.layout.addWidget(wdp)
        root.layout.addWidget(recordSession)
        
        root.setLayout(root.layout)
        root.setWindowTitle("QtRecordSession")
        root.show()
        app.exec_()
        
        
if __name__ == "__main__":
    
    from config import *
    from compiler import *
    
    QtRecordSession.test(CONFIG)