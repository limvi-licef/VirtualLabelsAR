# -*- coding: utf-8 -*-


# Packages
import requests as req
import json
from base64 import b64encode
import ssl
import websocket as websock


#############################################################################
class WindowsDevicePortal:
    
    
    """
        Class for use the windows device portal API of Hololens.
        
        Contains method for:
            - being connected
            - taking a picture
            - starting and stopping a video record
            - enumerating et downloading files
            - sending or receiving data using websocket
    """
    
    
    #########################################################################
    def __init__(self, logs=False):
        
        """
            Constructor.
            
            @param logs: bool that indicates if log must be printed
        """
        
        self.conn = False # connection to WDP
        self.downloadCallback = lambda x: None # a callback for monitoring download progress
        
        if logs: self.log = print
        else: self.log = lambda *args, **kwargs: None



    #########################################################################
    def isConnected(self):
        
        """
            Indicates if the object is connected to both rest API and websocket.
            
            @return bool
        """
        
        return self.conn and self.conn.status_code == 200 and self.conn.ws and self.conn.ws.connected
        
        
    #########################################################################
    def connect(self, host, auth, certfile=False):
        
        """
            Connection to WDP.
            
            @param host: str, host adress to Hololens on the network => <http(s)://ip:port>
            @param auth: tuple of str, login and password to connect WDP
            @param certfile: str, path to the certificate of Hololens
        """
        
        self.log(f"connection to WDP at {host}")
        
        # try to connect the rest API
        self._restConnection(host, auth, certfile)
        
        # if connection failed (no response or bad http status)
        if not (self.conn and self.conn.status_code == 200):
            # in case of bad status
            if type(self.conn) != bool:
                # log the http status code
                self.log("connection failed:", self.conn.status_code, '-', self.conn.reason)
                self.conn.ws = False
        
        # else try to connect the websocket
        else:
            self.log(f"connection to websocket")
            self._websocketConnection()
            
        
    #########################################################################
    def _restConnection(self, host, auth, certfile=False):
        
        """
            Connection to rest API. See 'connect' method for parameters details.
        """
        
        try:
            self.conn = req.get(host, auth=auth, verify=certfile)
            
        except req.ConnectionError:
            self.conn = False
        
        else:
            # add some properties for make use of connection easier
            self.conn.auth = auth
            self.conn.auth64 = b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
            self.conn.cert = certfile


    #########################################################################
    def _websocketConnection(self, timeout=1):
        
        """
            Connection to WDP websocket.
            
            @param timeout: int, millisecond timeout duration for websocket
        """
            
        # same host url as rest API connection but replace http protocol with ws protocol
        url = self.conn.url.replace('http','ws') + "ext/perception/client?clientmode=active"
        
        # header wich include authentication informations
        h = {
            "X-CSRF-Token": self.conn.cookies["CSRF-Token"],
            "Authorization": "Basic "+ self.conn.auth64
        }
        
        # explicit none use of certificate
        ssl_options = {"cert_reqs": ssl.CERT_NONE}

        # create connection and set timeout
        self.conn.ws = websock.create_connection(url, header=h, sslopt=ssl_options)
        self.conn.ws.settimeout(timeout)


    #########################################################################
    def _defaultRequest(self, method, urlApi="", p={}, *args, **kwargs):
        
        """
            Default rest API request.
            
            @param method: request function, method to use
            @param urlApi: str, url to handle
            @param p: optional dict, argument(s) of the request
            
            @ return the result of request
        """
        
        url = self.conn.url + urlApi # build full url
        h = { "X-CSRF-Token": self.conn.cookies["CSRF-Token"] } # set header for authentication
        
        return method(url, headers=h, params=p, auth=self.conn.auth, verify=self.conn.cert, *args, **kwargs)


    #########################################################################
    def takePicture(self, preview=False, holo=False):
        
        """
            Take picture on Hololens. Request response contains picture filename.
            
            @param preview: bool, indicate if camera view must be included
            @param holo: bool, indicate if holograms must be included
            
            @return request reponse object with json parsing
        """
        
        if self.isConnected():
            
            url = "api/holographic/mrc/photo"
            p = {
                'holo': 'true' if holo else 'false',
                'pv': 'true' if preview else 'false'
            }
            
            # make and return request
            res = self._defaultRequest(req.post, url, p)
            res.json = json.loads(res.text) # parse response as JSON
            return res
        
        return None


    #########################################################################
    def getFiles(self):
        
        """
            Enumerate files on Hololens.
            
            @return request response object
        """
        
        if self.isConnected():
            
            return self._defaultRequest(req.get, "api/holographic/mrc/files")
        
        return None


    #########################################################################
    def download(self, filename, filepath=None):
        
        """
            Download a file from the Hololens.
            
            @param filename: str, name on the Hololens
            @param optional filepath: str, path on the computer
        """
        
        if self.isConnected():
            
            # default name on computer is the same as the one on Hololens
            if not filepath: filepath = filename
            
            url = "api/holographic/mrc/file"
            p = {"filename": b64encode(filename.encode())} # filename is base64 encoded
            
            res = self._defaultRequest(req.get, url, p, stream=True)
            
            # open file
            with open(filepath, "wb") as file:
                
                # read chunk by chunk for avoiding memory problems
                step = 0 # progress counter
                for chunk in res.iter_content(chunk_size=8192):
                    step += len(chunk)
                    
                    # write in file and callback                    
                    file.write(chunk)
                    self.downloadCallback(step/int(res.headers["Content-Length"]))
            
            return res
        
        return None


    #########################################################################
    def startVideo(self, preview=True, holo=False):
        
        """
            Start a video record.
            
            @param preview: bool, indicate if camera view must be included
            @param holo: bool, indicate if holograms must be included
            
            @return request reponse object
        """
        
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
        
        """
            Stop video record.
            
            @return request reponse object with json parsing that contains video filename
        """
        
        if self.isConnected():
            
            res = self._defaultRequest(req.post, "api/holographic/mrc/video/control/stop")
            res.json = json.loads(res.text)
            
            return res
        
        return None
    
    
    #########################################################################
    def getVideoStatus(self):
        
        """
            Indicates the record status.
            
            @return request reponse object with json parsing
        """
        
        if self.isConnected():
            
            res = self._defaultRequest(req.get, "api/holographic/mrc/status")
            res.json = json.loads(res.text)
        
            return res
        
        return None
        
        
    #########################################################################
    def getData(self):
        
        """
            Get data from websocket.
            
            @return json dict
        """
        
        if self.isConnected():
            message = self.conn.ws.recv()
            return json.loads(message)
        else:
            return {}
        
        
    #########################################################################
    def sendData(self, message):
        
        """
            Send a message to the websocket.
            
            @param message: str
        """
        
        if self.isConnected():
            self.conn.ws.send(message)
        else:
            return {}
        
        
    #########################################################################
    def getBattery(self):
        
        """
            Request battery charging level of the Hololens.
            
            @return str, battery charging level, '/' if not connected
        """
        
        if self.isConnected():
            
            res = self._defaultRequest(req.get, "/api/power/battery")
            res.json = json.loads(res.text)
        
            level = res.json["RemainingCapacity"]/res.json["MaximumCapacity"] * 100
            return str(round(level)) + "%"
        
        return "/"
        
        
    #########################################################################
    # def interface(self, obj):
        
    #     obj.wdp = self
    #     obj.isConnected = self.isConnected
    #     obj.connect = self.connect
    #     obj.takePicture = self.takePicture
    #     obj.getFiles = self.getFiles
    #     obj.download = self.download
    #     obj.startVideo = self.startVideo
    #     obj.stopVideo = self.stopVideo
    #     obj.getVideoStatus = self.getVideoStatus
    #     obj.getData = self.getData
    #     obj.sendData = self.sendData
    #     obj.getBattery = self.getBattery
        
        
    #########################################################################
    @staticmethod
    def test(config):
        
        import time
        
        host = config["host"]
        auth = config["auth"]
        certfile = config["certfile"]
        savepath = config["resources"]
        
        wdp = WindowsDevicePortal(logs=True)
        wdp.connect(host, auth=auth, certfile=certfile)
        
        if not wdp.isConnected():
            print("unable to connect")
        else:
            print("Connected")
            
            print(wdp.startVideo().status_code)
            print(wdp.getVideoStatus().json)
            
            for n in range(5):
                data = wdp.getData()
                if "TrackingState" in data:
                    print("TrackingState", data["TrackingState"])
                time.sleep(1)
                    
            stop = wdp.stopVideo()
            print(stop.json)
            
            # uncomment to download
            wdp.downloadCallback = lambda x: print("download: ", int(x*100), "%", sep="", end="\r")
            download = wdp.download(stop.json["VideoFileName"], "WindowsDevicePortal.mp4")
            wdp.downloadCallback = None
            


if __name__ == "__main__":
    
    from config import *
    
    WindowsDevicePortal.test(CONFIG)
            
    