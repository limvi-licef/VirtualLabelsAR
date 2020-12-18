# -*- coding: utf-8 -*-


import cv2
import time
from numpy import zeros, uint8

from set_env import *
from lib.Video import Video

############################################################################################
class VideoPlayer(Video):

    STOP = 0
    PLAY = 1
    PAUSE = 2

    ########################################################################################
    def __init__(self, filename):

        Video.__init__(self, filename)
        self.status = VideoPlayer.STOP


    ########################################################################################
    def play(self):

        if self.status == VideoPlayer.STOP:
            self.setCurrentTime(0.0)

        self.status = VideoPlayer.PLAY


    ########################################################################################
    def pause(self):

        if self.status == VideoPlayer.PLAY:
            self.status = VideoPlayer.PAUSE


    ########################################################################################
    def stop(self):

        self.status = VideoPlayer.STOP
        self.setCurrentTime(1.0, mode=Video.RATIO)


    ########################################################################################
    def read(self):

        if self.status != VideoPlayer.PLAY:
            return False, False
        elif self.status == VideoPlayer.PLAY and self.getCurrentTime() >= self.TIME:
            self.stop()
            return False, False
        else:
            return Video.read(self)