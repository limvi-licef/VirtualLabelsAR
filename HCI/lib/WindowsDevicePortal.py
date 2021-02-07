# -*- coding: utf-8 -*-


import requests as req
import json
from base64 import b64encode
import ssl
import websocket as websock


#############################################################################
class WindowsDevicePortal:
    
    
    #########################################################################
    def __init__(self, logs=False):
        
        self.conn = False
        self._logs = logs
    
    
    #########################################################################
    def log(self, *args, **kwargs):
        
        if self._logs: print(*args, **kwargs)


    #########################################################################
    def isConnected(self):
        
        return self.conn and self.conn.status_code == 200 and self.conn.ws and self.conn.ws.connected
        
        
    #########################################################################
    def connect(self, host, auth, certfile=False):
        
        self.log(f"connection to WDP at {host}")
        self._restConnection(host, auth, certfile)
        
        if not (self.conn and self.conn.status_code == 200):
            if type(self.conn) != bool:
                self.log("connection failed:", self.conn.status_code, '-', self.conn.reason)
                self.conn.ws = False
        else:
            self.log(f"connection to websocket")
            self._websocketConnection()
            
        
    #########################################################################
    def _restConnection(self, host, auth, certfile=False):
        
        try:
            self.conn = req.get(host, auth=auth, verify=certfile)
            
        except req.ConnectionError:
            self.conn = False
        
        else:
            self.conn.auth = auth
            self.conn.auth64 = b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
            self.conn.cert = certfile


    #########################################################################
    def _websocketConnection(self, timeout=1):
            
        url = self.conn.url.replace('http','ws') + "ext/perception/client?clientmode=active"
        h = {
            "X-CSRF-Token": self.conn.cookies["CSRF-Token"],
            "Authorization": "Basic "+ self.conn.auth64
        }
        ssl_options = {"cert_reqs": ssl.CERT_NONE}

        self.conn.ws = websock.create_connection(url, header=h, sslopt=ssl_options)
        self.conn.ws.settimeout(timeout)


    #########################################################################
    @staticmethod
    def saveContent(filename, content, mode='w'):
        
        with open(filename, mode=mode) as file:
            file.write(content)


    #########################################################################
    def _defaultRequest(self, method, url_api="", p={}):
        
        url = self.conn.url + url_api
        h = { "X-CSRF-Token": self.conn.cookies["CSRF-Token"] }
        
        return method(url, headers=h, params=p, auth=self.conn.auth, verify=self.conn.cert)


    #########################################################################
    def takePicture(self, preview=False, holo=False):
        
        if self.isConnected():
            
            url = "api/holographic/mrc/photo"
            p = {
                'holo': 'true' if holo else 'false',
                'pv': 'true' if preview else 'false'
            }
            
            res = self._defaultRequest(req.post, url, p)
            res.json = json.loads(res.text)
            
            return res
        
        return None


    #########################################################################
    def getFiles(self):
        
        if self.isConnected():
            
            return self._defaultRequest(req.get, "api/holographic/mrc/files")
        
        return None


    #########################################################################
    def download(self, filename):
        
        if self.isConnected():
            
            url = "api/holographic/mrc/file"
            p = {
                "filename": b64encode(filename.encode()),
                "op": "stream"
            }
            
            res = self._defaultRequest(req.get, url, p)
            res.save = lambda: WindowsDevicePortal.saveContent(filename, res.content, 'wb')
            
            return res
        
        return None


    #########################################################################
    def startVideo(self, preview=True, holo=False):
        
        if self.isConnected():
            
            url = "api/holographic/mrc/video/control/start"
            p = {
                'holo': 'true' if holo else 'false',
                'pv': 'true' if preview else 'false'
            }
            
            res = self._defaultRequest(req.post, url, p)
            
            return res
        
        return None
    
    
    #########################################################################
    def stopVideo(self):
        
        if self.isConnected():
            
            res = self._defaultRequest(req.post, "api/holographic/mrc/video/control/stop")
            res.json = json.loads(res.text)
            
            return res
        
        return None
    
    
    #########################################################################
    def getVideoStatus(self):
        
        if self.isConnected():
            
            res = self._defaultRequest(req.get, "api/holographic/mrc/status")
            res.json = json.loads(res.text)
        
            return res
        
        return None
        
        
    #########################################################################
    def getData(self):
        
        if self.isConnected():
            message = self.conn.ws.recv()
            return json.loads(message)
        else:
            return {}
        
        
    #########################################################################
    def sendData(self, message):
        
        if self.isConnected():
            self.conn.ws.send(message)
        else:
            return {}
        
        
    #########################################################################
    def getBattery(self):
        
        if self.isConnected():
            
            res = self._defaultRequest(req.get, "/api/power/battery")
            res.json = json.loads(res.text)
        
            level = res.json["RemainingCapacity"]/res.json["MaximumCapacity"] * 100
            return str(round(level)) + "%"
        
        return "/"
        
        
    #########################################################################
    def interface(self, obj):
        
        obj.wdp = self
        obj.isConnected = self.isConnected
        obj.connect = self.connect
        obj.takePicture = self.takePicture
        obj.getFiles = self.getFiles
        obj.download = self.download
        obj.startVideo = self.startVideo
        obj.stopVideo = self.stopVideo
        obj.getVideoStatus = self.getVideoStatus
        obj.getData = self.getData
        obj.sendData = self.sendData
        obj.getBattery = self.getBattery
        
        
    #########################################################################
    @staticmethod
    def test(config):
        
        import time
        
        host = config["host"]
        auth = config["auth"]
        certfile = config["certfile"]
        
        wdp = WindowsDevicePortal(logs=True)
        wdp.connect(host, auth=auth, certfile=certfile)
        
        if not wdp.isConnected():
            print("unable to connect")
        else:
            print("Connected")
            
            print(wdp.startVideo().status_code)
            print(wdp.getVideoStatus().json)
            
            for n in range(20):
                data = wdp.getData()
                if "TrackingState" in data:
                    print("TrackingState", data["TrackingState"])
                time.sleep(1)
                    
            stop = wdp.stopVideo()
            print(stop.json)
            
            # uncomment to download
            # download = wdp.download(stop.json["VideoFileName"])
            # download.save()
            


if __name__ == "__main__":
    
    from config import *
    
    WindowsDevicePortal.test(CONFIG)
            
    