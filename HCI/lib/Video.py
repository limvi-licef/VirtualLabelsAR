# -*- coding: utf-8 -*-


import cv2
import time


############################################################################################
class Video(cv2.VideoCapture):

    """
        Base class for working with OpenCV video.
    """

    # Time modes
    MIN_S_MS = 0
    SECONDS = 1
    MIN_SEC = 2
    RATIO = 3

    ########################################################################################
    def __init__(self, filename):

        """
            Constructor. Loads a video file and sets some constants.

            @arg filename: string, path to video file.
        """

        cv2.VideoCapture.__init__(self, filename)

        self.WIDTH = int(self.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.HEIGHT = int(self.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.FPS = self.get(cv2.CAP_PROP_FPS)
        self.FRAME_COUNT = int(self.get(cv2.CAP_PROP_FRAME_COUNT))
        self.TIME = self.FRAME_COUNT / self.FPS
        
        self.start = time.time()


    ########################################################################################
    def getTime(self, mode=1):

        """
            Indicates the whole time of the video.

            @arg optional mode: integer, class time mode defined above
            @return: float (SECONDS mode), tuple of 2 int (MIN_SEC mode) or tuple of 3 int (MIN_S_MS mode)
        """
        
        if mode == Video.MIN_S_MS:
            return int(self.TIME/60), int(self.TIME%60), int(self.TIME%1*1000)
        elif mode == Video.MIN_SEC:
            return int(self.TIME/60), int(self.TIME%60)
        else:
            return self.TIME


    ########################################################################################
    def getRealTime(self):
        
        return time.time() - self.start


    ########################################################################################
    def getRecordTime(self, mode=1):

        """
            Indicates the current time of the video.

            @arg optional mode: integer, class time mode defined above
            @return: float (SECONDS mode), tuple of 2 int (MIN_SEC mode) or tuple of 3 int (MIN_S_MS mode)
        """

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

        """
            Skip to specific time in video. The default time unit is the second. Minute and
            millisecond or ratio could also be used depending on the time mode.

            @arg t: int or float, seconds or ratio
            @arg m: int, number of minute for MIN_SEC mode
            @arg ms: int, number of millisecond for MIN_S_MS
            @arg optional mode: integer, class time mode defined above
        """

        # calculates the frame number at requested time
        if mode == Video.RATIO:
            time_sec = self.TIME * float(t)
            current_frame = (self.FRAME_COUNT-1) * t
        else:
            time_sec = (int(m) * 60) + float(t) + (int(ms) // 1000)
            current_frame = (self.FRAME_COUNT-1) * time_sec // self.TIME

        # skip to the frame
        self.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        self.start = time.time() - time_sec


    ########################################################################################
    @staticmethod
    def test(config):

        """
            Test of class.
        """

        # instanciates new Video object
        video = Video(config["video"])
        assert video.isOpened(), "Video could not be read"

        # print infos
        print("Video size (width, height):", video.WIDTH, video.HEIGHT)
        print("Video whole time: %.3f" % video.getTime(),
              "=>", video.getTime(mode=Video.MIN_S_MS),
              "=>", video.getTime(mode=Video.MIN_SEC))

        # create window wich contains a slider for setting time
        cv2.namedWindow('Trackbar')
        cv2.createTrackbar("Time", "Trackbar", 0, int(video.TIME), lambda t: video.setCurrentTime(t))
            
        # loop until user closes a window or the video has ended
        video.setCurrentTime(0)
        while video.isOpened():
            
            # update and display a frame
            _, frame = video.read()
            if _:
                display = cv2.resize(frame, (640,480)) # resize
                cv2.imshow("Display", display)

            # events
            key = cv2.waitKey(1)
            display_open = cv2.getWindowProperty("Display", cv2.WND_PROP_VISIBLE)
            trackbar_open = cv2.getWindowProperty("Trackbar", cv2.WND_PROP_VISIBLE)

            # check events
            if key == ord('q') or not display_open or not trackbar_open:
                # release video => breaks the loop
                video.release()
                
            print("Video current time: %.3f" % video.getRecordTime(),
                  "=>", video.getRecordTime(mode=Video.MIN_S_MS),
                  "=>", video.getRecordTime(mode=Video.MIN_SEC),
                  end='\r')
            
            # time control
            n_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
            while video.getRealTime() < video.getRecordTime():
                pass
                
                
        # close all windows
        cv2.destroyAllWindows()
        
        
if __name__ == "__main__":
    
    from config import *
    
    Video.test(CONFIG)