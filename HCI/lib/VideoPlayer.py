# -*- coding: utf-8 -*-


import cv2
import time
from numpy import zeros, uint8

from lib.Video import Video

############################################################################################
class VideoPlayer(Video):

    """
        An extends class for making use of Video class easier.
    """

    # reading status modes
    STOP = 0
    PLAY = 1
    PAUSE = 2

    ########################################################################################
    def __init__(self, filename):

        """
            Constructor. Instanciate the mother class and set the read status to STOP.

            @arg filename: string, path to video file.
        """

        Video.__init__(self, filename)
        self.status = VideoPlayer.STOP
        self.pause_update = False


    ########################################################################################
    def play(self):

        """
            Start playing the video.
        """

        # skip to the begin of video
        if self.status == VideoPlayer.STOP:
            self.setCurrentTime(0.0)

        if self.status == VideoPlayer.PAUSE:
            self.start += time.time() - self.start_pause
            
        # update reading status
        self.status = VideoPlayer.PLAY


    ########################################################################################
    def pause(self):

        """
            Pause the video
        """

        # update reading status
        if self.status == VideoPlayer.PLAY:
            self.status = VideoPlayer.PAUSE
            self.start_pause = time.time()
            self.pause_update = False


    ########################################################################################
    def stop(self):

        """
            Stop the video
        """

        # skip to the end of video
        self.setCurrentTime(1.0, mode=Video.RATIO)

        # update reading status
        self.status = VideoPlayer.STOP
        
        
    ########################################################################################
    def setCurrentTime(self, *args, **kwargs):
        
        Video.setCurrentTime(self, *args, **kwargs)
        
        # in case of time setting when on pause
        if self.status == VideoPlayer.PAUSE:
            self.start_pause = time.time()
            self.pause_update = True


    ########################################################################################
    def read(self):

        """
            Read the current frame

            @return: tuple(bool, frame),
                -bool: boolean wich indicates that a frame was extracted
                -frame: False or numpy array depending on bool value
        """

        if self.status == VideoPlayer.STOP:
            return True, zeros((self.HEIGHT, self.WIDTH, 3), dtype=uint8)
        
        elif self.status == VideoPlayer.PAUSE:
            if self.pause_update:
                self.pause_update = False
                return Video.read(self)
            else:
                return False, None

        # if current time exceeds video time, stop video
        if self.getRecordTime() >= self.TIME:
            self.stop()
            return False, None

        # if the video is too slow
        elif self.getRealTime() < self.getRecordTime():
            return False, None
            
        else:
            delay = self.getRealTime() - self.getRecordTime()
            for n in range(int(delay / self.FPS)): Video.read(self)
            return Video.read(self)
        
        
    ########################################################################################
    def wait(self):
        
        """
            Method to call for controlling frame rate.
        """
        
        while self.getRealTime() < self.getRecordTime():
            pass


    ########################################################################################
    def interface(self, obj):

        obj.videoPlayer = self
        obj.read = self.read
        obj.play = self.play
        obj.pause = self.pause
        obj.stop = self.stop
        obj.setCurrentTime = self.setCurrentTime


    ########################################################################################
    @staticmethod
    def test(config):

        """
            Test of class.
        """
        
        import tkinter as tk
            
        # instanciates new Video object
        videoPlayer = VideoPlayer(config["video"])
        assert videoPlayer.isOpened(), "Video could not be read"

        # control panel
        root = tk.Tk()
        tk.Button(root, text="Play", command=videoPlayer.play).pack()
        tk.Button(root, text="Pause", command=videoPlayer.pause).pack()
        tk.Button(root, text="Stop", command=videoPlayer.stop).pack()
        tk.Button(root, text="Release", command=videoPlayer.release).pack()
        
        # scale bar and its variable
        scale_var = tk.DoubleVar()
        scale = tk.Scale(root, orient=tk.HORIZONTAL, variable=scale_var, command=videoPlayer.setCurrentTime, to=int(videoPlayer.TIME))
        scale.pack(fill=tk.X, expand=tk.TRUE)

        # label of time
        label = tk.Label(root, text="0:00")
        label.pack()

        # loop until user closes the tk window or the video is released
        while videoPlayer.isOpened():
            
            # update and display a frame
            _, frame = videoPlayer.read()
            if _:
                display = cv2.resize(frame, (640,480)) # resize
                cv2.imshow("Display", display)
            
            # check events
            if cv2.waitKey(1) == ord('q'):
                videoPlayer.release()
            else:
                print("%.3f" % videoPlayer.getRecordTime(),
                      "=>", videoPlayer.getRecordTime(mode=VideoPlayer.MIN_S_MS),
                      "=>", videoPlayer.getRecordTime(mode=VideoPlayer.MIN_SEC),
                      end='\r')

                # update scale bar value and label of time
                # root could be destroyed so operations are included in try/except bloc
                try:
                    scale_var.set(int(videoPlayer.getRecordTime(mode=Video.SECONDS)))
                    label["text"] = "{}:{}".format(*videoPlayer.getRecordTime(mode=Video.MIN_SEC))
                except:
                    break

            # update the tk window
            root.update()
            videoPlayer.wait()
            
        cv2.destroyAllWindows()
        root.destroy()
            
            
if __name__ == "__main__":
    
    from config import *
    
    VideoPlayer.test(CONFIG)
                