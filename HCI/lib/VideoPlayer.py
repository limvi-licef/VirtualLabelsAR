# -*- coding: utf-8 -*-


import cv2


############################################################################################
class VideoPlayer(cv2.VideoCapture):

    MIN_S_MS = 0
    SECONDS = 1
    MIN_SEC = 2

    ########################################################################################
    def __init__(self, filename):

        cv2.VideoCapture.__init__(self, filename)


        self.WIDTH = int(self.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.HEIGHT = int(self.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.FPS = self.get(cv2.CAP_PROP_FPS)
        self.FRAME_COUNT = int(self.get(cv2.CAP_PROP_FRAME_COUNT))
        self.TIME = self.FRAME_COUNT / self.FPS

        self.current_frame = 0.0


    ########################################################################################
    def read(self):
        
        self.current_frame += 1.0

        return cv2.VideoCapture.read(self)


    ########################################################################################
    def getTime(self, mode='s'):
        
        if mode == VideoPlayer.MIN_S_MS:
            return int(self.TIME/60), round(self.TIME%60), round(self.TIME%1*1000)
        elif mode == VideoPlayer.MIN_SEC:
            return int(self.TIME/60), round(self.TIME%60)
        else:
            return self.TIME


    ########################################################################################
    def getCurrentTime(self, mode='s'):

        time = self.current_frame / self.FPS
        
        if mode == VideoPlayer.MIN_S_MS:
            return int(time/60), round(time%60), round(time%1*1000)
        elif mode == VideoPlayer.MIN_SEC:
            return int(time/60), round(time%60)
        else:
            return time


    ########################################################################################
    def setCurrentTime(self, s, m=0, ms=0):

        time_sec = m * 60
        time_sec += s
        time_sec += ms // 1000

        current_frame = self.FRAME_COUNT * int(time_sec) // self.TIME
        self.set(cv2.CAP_PROP_POS_FRAMES, current_frame)