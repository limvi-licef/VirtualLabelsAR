# -*- coding: utf-8 -*-


import cv2

from set_env import *
from lib.VideoPlayer import VideoPlayer


videoPlayer = VideoPlayer("C:\\Users\\Anthony\\Videos\\Base Profile\\Syphon Filter - First Level.mp4")
assert videoPlayer.isOpened(), "Video could not be read"

print(videoPlayer.WIDTH, videoPlayer.HEIGHT)
print("%.3f" % videoPlayer.getTime(), "=>", videoPlayer.getTime(mode=VideoPlayer.MIN_S_MS), "=>", videoPlayer.getTime(mode=VideoPlayer.MIN_SEC))

cv2.namedWindow('Trackbar')
cv2.createTrackbar("Time", "Trackbar", 0, int(videoPlayer.TIME), lambda x: videoPlayer.setCurrentTime(x))


while videoPlayer.isOpened():
    
    _, frame = videoPlayer.read()

    cv2.imshow("", cv2.resize(frame, (640,480)))
    key = cv2.waitKey(1)

    if key == ord('q'):
        videoPlayer.release()

    #cv2.setTrackbarPos("Time", "Trackbar", int(videoPlayer.getCurrentTime()))

    print("%.3f" % videoPlayer.getCurrentTime(),
          "=>", videoPlayer.getCurrentTime(mode=VideoPlayer.MIN_S_MS),
          "=>", videoPlayer.getCurrentTime(mode=VideoPlayer.MIN_SEC),
          end='\r')