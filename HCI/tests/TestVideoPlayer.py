# -*- coding: utf-8 -*-


import cv2
import tkinter as tk

from set_env import *
from lib.Video import Video
from lib.VideoPlayer import VideoPlayer


videoPlayer = VideoPlayer("C:\\Users\\Anthony\\Videos\\Base Profile\\Syphon Filter - First Level.mp4")

root = tk.Tk()

tk.Button(root, text="Play", command=videoPlayer.play).pack()
tk.Button(root, text="Pause", command=videoPlayer.pause).pack()
tk.Button(root, text="Stop", command=videoPlayer.stop).pack()
tk.Button(root, text="Release", command=videoPlayer.release).pack()

def scaleCallback(value):
    videoPlayer.setCurrentTime(var.get(), mode=Video.SECONDS)

var = tk.DoubleVar()
scale = tk.Scale(root, orient=tk.HORIZONTAL, variable=var, command=scaleCallback, to=videoPlayer.TIME)
scale.pack(fill=tk.X, expand=tk.TRUE)

label = tk.Label(root, text="0:00")
label.pack()

while videoPlayer.isOpened():
    
    _, frame = videoPlayer.read()

    if _: cv2.imshow("", cv2.resize(frame, (640,480)))
    key = cv2.waitKey(1)

    if key == ord('q'):
        videoPlayer.release()
    else:
        print("%.3f" % videoPlayer.getCurrentTime(),
              "=>", videoPlayer.getCurrentTime(mode=VideoPlayer.MIN_S_MS),
              "=>", videoPlayer.getCurrentTime(mode=VideoPlayer.MIN_SEC),
              end='\r')

        var.set(videoPlayer.getCurrentTime(mode=Video.SECONDS))
        label["text"] = "{}:{}".format(*videoPlayer.getCurrentTime(mode=Video.MIN_SEC))

    root.update()