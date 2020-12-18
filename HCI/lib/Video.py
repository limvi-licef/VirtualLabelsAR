# -*- coding: utf-8 -*-


import cv2


############################################################################################
class Video(cv2.VideoCapture):

    MIN_S_MS = 0
    SECONDS = 1
    MIN_SEC = 2
    RATIO = 3

    ########################################################################################
    def __init__(self, filename):

        cv2.VideoCapture.__init__(self, filename)


        self.WIDTH = int(self.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.HEIGHT = int(self.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.FPS = self.get(cv2.CAP_PROP_FPS)
        self.FRAME_COUNT = int(self.get(cv2.CAP_PROP_FRAME_COUNT))
        self.TIME = self.FRAME_COUNT / self.FPS


    ########################################################################################
    def getTime(self, mode=1):
        
        if mode == Video.MIN_S_MS:
            return int(self.TIME/60), int(self.TIME%60), int(self.TIME%1*1000)
        elif mode == Video.MIN_SEC:
            return int(self.TIME/60), int(self.TIME%60)
        else:
            return self.TIME


    ########################################################################################
    def getCurrentTime(self, mode=1):
        if mode == Video.RATIO:
            return self.get(cv2.CAP_PROP_POS_FRAMES) / self.FRAME_COUNT

        else:
            time = self.get(cv2.CAP_PROP_POS_FRAMES) / self.FPS
        
            if mode == Video.MIN_S_MS:
                return int(time/60), int(time%60), int(time%1*1000)
            elif mode == Video.MIN_SEC:
                return int(time/60), int(time%60)
            else:
                return time


    ########################################################################################
    def setCurrentTime(self, t, m=0, ms=0, mode=1):

        if mode == Video.RATIO:
            current_frame = (self.FRAME_COUNT-1) * t
        else:
            time_sec = (m * 60) + t + (ms // 1000)
            current_frame = (self.FRAME_COUNT-1) * time_sec // self.TIME

        self.set(cv2.CAP_PROP_POS_FRAMES, current_frame)