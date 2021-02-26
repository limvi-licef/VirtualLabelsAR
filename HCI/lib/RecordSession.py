# -*- coding: utf-8 -*-


#############################################################################
# Packages
import time
from base64 import b64encode, b64decode
from json import dumps
from os.path import join

# Lib
from lib.MeshObject import MeshObject
from lib.Video import Video


#############################################################################
class RecordSession:
    
    
    """
        Automation of data recovering by using a WindowsDevicePortal object.
    """
    
   
    #########################################################################
    def __init__(self, wdp):
        
        """
            Constructor.
            
            @param wdp: WindowsDevicePortal object
        """
        
        self.wdp = wdp
        self.isRecording = False
    
   
    #########################################################################
    def _sessionClear(self):
        
        self.session = {}
        self.session["id"] = time.time()
        self.session["camera"] = []
        self.session["meshes"] = {}
        self.session["video"] = None
        self.session["sync"] = []
    
   
    #########################################################################
    def start(self):
        
        """
            Start a record.
            
            @return bool, indicates if record is starting
        """
        
        if self.wdp.isConnected() and not self.isRecording:
            
            # start video and ask new data
            self.wdp.startVideo()
            self.wdp.sendData("resumetracking")
            self.wdp.sendData("getsrdata")
            
            # clear session and update status
            self.isRecording = True
            self._sessionClear()
            
            return True
        
        return False
    
   
    #########################################################################
    def stop(self):
        
        """
            Stop a record.
        """
        
        if self.isRecording:
            
            self.stopReq = self.wdp.stopVideo()
            self.isRecording = False
            
            return True
        
        return False

            
    #########################################################################
    def _sync(self, filename):
        
        """
            Post record parsing. Synchronize each frame to a spatial set of info.
            
            @param filename: str, path to video file
        """
            
        # get info from video
        video = Video(filename)
        total_fc = video.FRAME_COUNT
        total_time = video.TIME
        video.release()
        
        
        # loop on each frame
        n = 0 # index
        for fc in range(total_fc):
            
            t = fc/total_fc * total_time # get frame timestamp
            
            # incement index for matching camera data
            while n+1 < len(self.session["camera"]) and t > self.session["camera"][n]["time"]:
                n += 1
                
            self.session["sync"].append(n) # append index
                
            
    #########################################################################
    def save(self, filename, videopath):
        
        """
            Save the current session.
            
            @param filename: str, name of record file
            @param videopath: str, path to the video directory
        """
        
        # build fullname for video and add to session
        videoname = self.stopReq.json["VideoFileName"]
        videofullname = join(videopath, videoname)
        self.session["video"] = videofullname

        # download and save video
        download = self.wdp.download(videoname, videofullname)
        del download # DELETE FOR AVOID MEMORY ERROR

        # sync video with camera and save session        
        self._sync(videofullname)
        with open(filename, mode="w") as file:
            data = dumps(self.session)
            file.write(data)


    #########################################################################
    def getTime(self):
        
        """
            Get the time from record start
            
            @return int, time in seconds
        """
        
        if self.isRecording:
            return time.time() - self.session["id"]
        
        return 0

            
    #########################################################################
    def ping(self):
        
        """
            Get and parse data from the websocket.
            
            @return tuple(str, dict),
                str: type of data
                dict: info from received data
        """
        
        if self.isRecording:
    
            self.lastData = self.wdp.getData() # store data as attributes for easy access
            
            # parse camera info
            if "OriginToAttachedFor" in self.lastData and "HeadToAttachedFor" in self.lastData:
                data = {
                    "time": self.getTime(),
                    "position": self.lastData["OriginToAttachedFor"],
                    "rotation": self.lastData["HeadToAttachedFor"],
                    }
                self.session["camera"].append(data)
                
                return "camera", data
            
            # parse mesh info
            if "SurfaceObserverStatus" in self.lastData and self.lastData["SurfaceObserverStatus"] == "OK":
                meshId = self.lastData["Surface"]["SurfaceId"]
                self.session["meshes"][meshId] = MeshObject(self.lastData, context=False).save()
                
                return "mesh", {
                    "time": self.getTime(),
                    "meshId": meshId
                    }
        
        return None, { "time": self.getTime() }
        
        
    #########################################################################
    @staticmethod
    def test(config):
        
        import time
        from lib.WindowsDevicePortal import WindowsDevicePortal
        
        host = config["host"]
        auth = config["auth"]
        certfile = config["certfile"]
        
        wdp = WindowsDevicePortal(logs=True)
        wdp.connect(host, auth=auth, certfile=certfile)
        
        if wdp.isConnected():
            print("connected")
            
            rs = RecordSession(wdp)
            
            rs.start()
            print("start record")
            
            for n in range(50):
                typ, data = rs.ping()
                print("ping at:", data["time"])
                print("type :", typ)
                time.sleep(0.1)
                
            rs.stop()
            print("stop record")
            
            record = config["record"] + "/record_test.rs"
            rs.wdp.download_callback = lambda x: print("download: ", int(x*100), "%", sep="")
            rs.save(record, config["video"])
            rs.wdp.download_callback = None
            print("record saved")
            
            
            
            
if __name__ == "__main__":
    
    from config import *
    
    RecordSession.test(CONFIG)
        
        