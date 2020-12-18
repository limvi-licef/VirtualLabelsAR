# -*- coding: utf-8 -*-


import cv2

from set_env import *
from lib.Video import Video


video = Video("C:\\Users\\Anthony\\Videos\\Base Profile\\Syphon Filter - First Level.mp4")
assert video.isOpened(), "Video could not be read"

print(video.WIDTH, video.HEIGHT)
print("%.3f" % video.getTime(), "=>", video.getTime(mode=Video.MIN_S_MS), "=>", video.getTime(mode=Video.MIN_SEC))

cv2.namedWindow('Trackbar')
cv2.createTrackbar("Time", "Trackbar", 0, int(video.TIME), lambda x: video.setCurrentTime(x))


video.setCurrentTime(0.1, mode=Video.RATIO)
while video.isOpened():
    
    _, frame = video.read()

    cv2.imshow("", cv2.resize(frame, (640,480)))
    key = cv2.waitKey(1)

    if key == ord('q'):
        video.release()
    else:
        print("%.3f" % video.getCurrentTime(),
              "=>", video.getCurrentTime(mode=Video.MIN_S_MS),
              "=>", video.getCurrentTime(mode=Video.MIN_SEC),
              end='\r')

    #cv2.setTrackbarPos("Time", "Trackbar", int(video.getCurrentTime()))

    #video.setCurrentTime(0.5, mode=Video.RATIO)