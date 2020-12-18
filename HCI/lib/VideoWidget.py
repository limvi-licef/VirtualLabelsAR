# -*- coding: utf-8 -*-


import tkinter as tk
from PIL import Image, ImageTk

from set_env import *
from lib.VideoPlayer import VideoPlayer


############################################################################################
class VideoWidget(tk.Canvas):


    ########################################################################################
    def setVideoPlayer(self, videoPlayer):

        self.videoPlayer = videoPlayer
        self.after(1, self.tick)


    ########################################################################################
    def updateImage(self):

        _, frame = self.videoPlayer.read()
        width, height = int(self["width"]), int(self["height"])
        image = Image.fromarray(frame).resize((width, height))
        self.photoImage = ImageTk.PhotoImage(image)
        self.create_image(0, 0, image=self.photoImage, anchor="nw")


    ########################################################################################
    def tick(self):
        
        self.updateImage()
        self.after(1000//30, self.tick)

