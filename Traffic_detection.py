import datetime
from imutils.video import VideoStream
#from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import cv2
import os
import numpy
import json
#import argparse
print "[Tool Status] - STARTED"
# todo-michael: force learn after a certain time, even if active
# todo-michael: "night mode"
# todo-michael: web server incl. statistics
# todo-michael: rework recording 

# construct the argument parse and parse the arguments
# USAGE
# python videostream_demo.py
# python videostream_demo.py --picamera 1
# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--picamera", type=int, default=-1,
#	help="whether or not the Raspberry Pi camera should be used")
#args = vars(ap.parse_args())
conf = json.load(open("Bahnhofstr14.json"))




def DetectionResultOutput(LiveFeed,c, direction, TrafficCounter, InactiveCounter,x,y,w,h,cx,cy, StatisticFileName):
    if time.daylight == 0:
        Daylight = "NIGHT"
    elif time.daylight == 1:
        Daylight = "DAYLIGHT"

    DetectionDetails = format(time.strftime("%Y-%m-%d %H:%M:%S")) + ";" + \
                    format(TrafficCounter) + ";" + \
                    Daylight + ";" + \
                    direction + ";" + \
                    format(InactiveCounter) + ";" + \
                    format(x) + ";" + \
                    format(y) + ";" + \
                    format(w) + ";" + \
                    format(h) + ";" + \
                    format(cx) + ";" + \
                    format(cy) + ";" + \
                    format(cv2.contourArea(c))
    # print some info in the console
    print DetectionDetails
    if conf["ShowPictures"] == True or conf["StoreDetection"] == True:
    	# in case tone of the two options is activated, put some information to the picture:
        cv2.putText(LiveFeed, "Vehicles counted by algo: {}".format(TrafficCounter), (10, 35),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1)

    if conf["ShowPictures"] == True:
        # show frame where the vehicle went over the line, only in case the option is activated:
        cv2.imshow("Detection view", LiveFeed)
    #cv2.imshow("Detection view", LiveFeed)                                                                              # show frame where the vehicle went over the line
    if conf["StoreDetection"] == True:
        cv2.imwrite("Screenshots\_" + format(TrafficCounter) + ".jpg", LiveFeed)
        StatisticFileName.write(DetectionDetails + "\n")
        cv2.imwrite("Screenshots\_" + format(TrafficCounter) + "_"+ format(SimpleCounter)+".jpg", LiveFeed)
        StatisticFileName.write(DetectionDetails + "\n")

    
def ShowVideoOutput(LiveFeed, frameDelta, thresh, firstFrame):
    if conf["ShowPictures"] == True:
        cv2.imshow("Live View", LiveFeed)
        cv2.imshow("Frame Delta", frameDelta)
        cv2.imshow("Thresholded View", thresh)
        cv2.imshow("Background substraction base", firstFrame)

    
def DrawDetectionFrames(LiveFeed):
    # function which draws the detection thresholds
    cv2.rectangle(LiveFeed, (conf["mindetectionwindowX"], conf["mindetectionwindowY"]),
                  (conf["maxdetectionwindowX"], conf["maxdetectionwindowY"]), (127, 255,0), 2)
    cv2.line(LiveFeed, (DetectionLineUpperPoint), (DetectionLineLowerPoint), (255, 0, 0),2)

def DrawVideoInformation(LiveFeed, DetectionStatus, TrafficCounter, ManualCounter, elapsedtime):
    if conf["ShowPictures"] == True or conf["StoreDetection"] == True:
    # function which draws the detection results and some timestamps
        cv2.putText(LiveFeed, format(elapsedtime),
                    (10, LiveFeed.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)                           # Draw the elapsed time in the lower left corner
        cv2.putText(LiveFeed, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (300, LiveFeed.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)                          # Draw the current time in the lower right corner
        cv2.putText(LiveFeed, "Traffic detection: {}".format(DetectionStatus), (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5,
                    (0, 0, 0), 1)                                                                                           # Draw the Detection status on the frame
        cv2.putText(LiveFeed, "Vehicles counted by algo: {}".format(TrafficCounter), (10, 35),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1)                                                      # Draw the Traffic counter from Algo
        if ManualCounter > 0:
            cv2.putText(LiveFeed, "Vehicles counted by user: {}".format(ManualCounter), (10, 50),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1)                                                      # Draw the Traffic conunter from user (if exists)

def CloseCamera(camera):
    # a function to ensure camera is properly closed and all display windows are removed
    cv2.destroyAllWindows()
    vs.stop()
    print "[Camera Status] - deactivated"

def RecordVideo(camera):
    # a function to record a vide for later off-line analysis
    VideoName = raw_input("VideoName (without extension) : ")                                                           # ask for filename
    if os.path.isfile("videos"+chr(92)+ format(VideoName)+'.avi'):                                                      # check if file exists
        Selection = raw_input("File exists! Overwrite? (y/n) :")                                                        # ask to overwrite in case the file is already existing
        if Selection.lower() == "y":                                                                                    # if overwrite was chosen,
            os.remove("videos"+chr(92)+ format(VideoName)+'.avi')                                                       # delete the file
        else:                                                                                                           # if overwrite was not chosen,
            RecordVideo(camera)                                                                                         # restart function and re-ask for the name

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')                                                                 # Define the codec and create VideoWriter object
    RecordedVideo = cv2.VideoWriter("videos"+chr(92)+ format(VideoName) + '.avi', fourcc, 25, (640, 480), True)         # Define the Video parameters (name, resolution, framerate)
    #camera = vs.read()

    #while (camera.isOpened()):                                                                                          # loop over frames from camera
    while True:
        LiveFeed = vs.read()                                                                                   # read single frame from camera
        LiveFeed = imutils.resize(LiveFeed, width=500)
        if True:                                                                                                 # as long as there is a frame,
            RecordedVideo.write(LiveFeed)                                                                               # add this frame to the defined video stream
            cv2.putText(LiveFeed, "Recording file .."+chr(92)+"videos"+chr(92)+ format(VideoName)+'.avi',               # for the live view, add an identifier that the video is recorded
                        (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 2)
            cv2.imshow('Recorder', LiveFeed)                                                                            # and show the frame as live view
            if cv2.waitKey(1) & 0xFF == 27:                                                                             # when ESC button was pressed,
                CloseCamera(camera)                                                                                     # call the camera close function
                RecordedVideo.release()                                                                                 # and release the recorded video file to ensure this is properly stored
                break                                                                                                   # go back to main menu
        else:                                                                                                           # if camera hardware is closed externally(for any reason, e.g. USB unplugged)
            CloseCamera(camera)                                                                                         # call the camera close function
            RecordedVideo.release()                                                                                     # and release the recorded video file to ensure this is properly stored
            break                                                                                                       # go back to main menu
    return camera
def CameraCalibration(camera):
    # a function which allows to calibrate the camera orientation before recording or live tracking is started
    #while(camera.isOpened()):                                                                                           # loop over frames from camera
    while True:
        LiveFeed = vs.read()
        LiveFeed = imutils.resize(LiveFeed, width=500)
        # read single frame from camera
        #if grabbed==True:                                                                                                   # as long as there is a frame,
        if True:
            cv2.putText(LiveFeed, "Calibration - ", (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 2)               # for the live view, add an identifier that the video is only for calibration
            DrawDetectionFrames(LiveFeed)                                                                               # call the function which writes the detection frame and crossing lines
            cv2.putText(LiveFeed, "MinX:   " + str(conf["mindetectionwindowX"]) + "---- MinY:    "+ str(conf["mindetectionwindowY"])+"---- MaxX:   "+
             str(conf["maxdetectionwindowX"])+ "---- MaxY:    " + str(conf["maxdetectionwindowY"]),
                        (10, LiveFeed.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.imshow('Calibration Window - press ESC to finalize',LiveFeed)                                                                   # and show the frame as live view

            if cv2.waitKey(1) & 0xFF == 27:                                                                             # when ESC button was pressed,
                print "calibration finished"
                cv2.imwrite('static\images\Calibration.jpg', LiveFeed)
                CloseCamera(camera)  # call the camera close function
                break

def OfflineVideo():
    # a function to initialize an pre-recorded video for offfline analysis
    print "All *.avi files in .."+chr(92)+"videos"+chr(92)+":"
    for file in os.listdir("videos"):                                                                           # show the content of the videos folder
        if "avi" in file:                                                                                               # only print avi files
            print file
    Selection = raw_input("select file to play (without extension): ")                                                  # ask user to type in the file to play
    if Selection=="":                                                                                                   # if nothing is entered
        camera = cv2.VideoCapture("videos" + chr(92) + "LongVideo1_quer" + ".avi")                                      # take the default video
    else:
        if os.path.isfile("videos"+chr(92)+Selection+".avi"):                                                           # check if the file is existing
            camera = cv2.VideoCapture("videos"+chr(92)+Selection+".avi")                                                # take the file defined by the user if it is existing in the video folder
            print "Selected file: " + camera
        else:
            print "file not found!"                                                                                     # if file was not found,
            OfflineVideo()                                                                                              # restart function and re-ask for name
    return camera
def OnlineVideo():
    # a function to define the standard camera hardware as video source
    #camera = cv2.VideoCapture(0)
    global vs
    vs = VideoStream(usePiCamera=conf["PiCamera"]).start()
    print "[Camera Status] - warming up"
    time.sleep(0.5)
    camera = vs.read()
    print "[Camera Status] - ready"
    return camera

def TrafficDetection(camera):
    # This is the main Traffic Detection function (side detection view)
    global SimpleCounter
    # Default Settings--------------------------------------------------------------------------------------------------
    firstFrame = None
    TrafficCounter = 0
    xold = 0
    yold = 0
    x = 0
    y = 0
    w = 0
    h = 0
    cx = 0
    cy = 0
    ManualCounter = 0
    DetectionStatus = "Inactive"
    ActiveCounter = 0
    InactiveCounter = 0
    Starttime = time.time()
    UpdateTime = 0
    TimeSinceLastUpdate = 0
    SimpleCounter = 0
    # ------------------------------------------------------------------------------------------------------------------
    StatisticFileName = open(StatisticFile, 'w')
    while True:                                                                                                         # loop over the frames of the video
        elapsedtime = time.time() - Starttime                                                                           # calculate the time since the video has started
        UpdateTime = time.time() - Starttime - TimeSinceLastUpdate                                                      # calculate the time since the last background substraction reference picture was taken
        #(grabbed, LiveFeed) = camera.read()                                                                             # grab the current frame
        LiveFeed = vs.read()
        LiveFeed = imutils.resize(LiveFeed, width=500)

        DetectionStatus = "Inactive"                                                                                    # initialize the status text displayed in the video
        InactiveCounter = InactiveCounter +1                                                                            # increse the Inactivty counter every loop
        ActiveCounter = 0
#        if not grabbed:                                                                                                 # if the frame could not be grabbed, then we have reached the end of the video
#            CloseCamera(camera)                                                                                         # call the camera close function
#            break                                                                                                       # go back to main menu

        LiveFeed = imutils.resize(LiveFeed, width=500)                                                                 # resize the LiveFeed
        Grayscaled_Picture = cv2.cvtColor(LiveFeed, cv2.COLOR_BGR2GRAY)                                                 # convert the LiveFeed to grayscale
        Grayscaled_Picture = cv2.GaussianBlur(Grayscaled_Picture, (21, 21), 0)                                          # blur the LiveFeed

        if firstFrame is None:                                                                                          # if the first frame is None, initialize it
            firstFrame = Grayscaled_Picture
            continue


        frameDelta = cv2.absdiff(firstFrame, Grayscaled_Picture)                                                        # compute the absolute difference between the current frame and first frame
        thresh = cv2.threshold(frameDelta, conf["ThresholdCalibration"], 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=conf["DilateIterations"])                                                  # dilate the thresholded image to fill in holes, then find contours on thresholded image
        #(_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)                      # opencv 2.4 requires three arguments to find the contours
        (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)                          # opencv 2.4 requires three arguments to find the contours

        for c in cnts:                                                                                                  # loop over the contours
           # print "frame c- ", cv2.contourArea(c), " --- ", cx, " , ", cy, cv2.boundingRect(c)
            if cv2.contourArea(c) > int(conf["MinObjectSize"]):                                                                 # if the contour is too small, ignore it
                SimpleCounter = SimpleCounter + 1
                (xold, yold, wold, hold) = (cx, cy, w, h)                                                               # store the former bounding box data to calculate the direction of movement
                (x, y, w, h) = cv2.boundingRect(c)                                                                      # compute the bounding box for the contour
                if conf["maxdetectionwindowY"] > y > conf["mindetectionwindowY"]:                                                       # only do an analyis in a specific height of the video
                    DetectionStatus = "Active"                                                                          # Set Detection Status to Active, if there is a larger movement in the detection window
                    centroid = cv2.moments(c)                                                                           # find the mass center of the blob
                    cx = int(centroid['m10'] / centroid['m00'])                                                         # for x direction
                    cy = int(centroid['m01'] / centroid['m00'])                                                         # for y direction
                    cv2.rectangle(LiveFeed, (x, y), (x + w, y + h), (0, 255, 0),
                                  2)  # draw the bounding box on the frame
                    cv2.putText(LiveFeed, \
                                "frame  : " " -x- -y- -w- -h- Size",
                                (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                    cv2.putText(LiveFeed, \
                                "current: " + str(cv2.boundingRect(c)) + " Size-" + str(cv2.contourArea(c)), \
                                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                    cv2.putText(LiveFeed, \
                                "former: " + str((xold, yold, wold, hold)) + " Size-" + str(cv2.contourArea(c-1)), \
                                (x, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                    direction = "None"
                    DetectionResultOutput(LiveFeed, c, direction, TrafficCounter, InactiveCounter,
                                          x, y, w, h, cx, cy, StatisticFileName)
                    if cx >= conf["DetectionLine"] and xold < conf["DetectionLine"] and xold < cx and (cx-xold)<=conf["MaximumMovementDelta"]:  # detect movement accross the line (only small movements are allowed) from left to right
                        TrafficCounter = TrafficCounter + 1                                                             # increase the counter
                        direction = "North"
                        time.sleep(0.1)
                        DetectionResultOutput(LiveFeed,c, direction, TrafficCounter,InactiveCounter,
                                              x,y,w,h,cx,cy, StatisticFileName)                                         # call the function which prints some console stuff, shows the dected picture and write the statistic file
                    if cx <= conf["DetectionLine"] and xold > conf["DetectionLine"] and xold > cx and (xold-cx)<=conf["MaximumMovementDelta"]:  # detect movement accross the line (only small movements are allowed) from right to left
                        TrafficCounter = TrafficCounter + 1                                                             # increase the counter
                        direction = "South"
                        time.sleep(0.1)
                        DetectionResultOutput(LiveFeed,c, direction, TrafficCounter, InactiveCounter,
                                              x, y, w, h, cx, cy, StatisticFileName)                                    # call the function which prints some console stuff, shows the dected picture and write the statistic file
                DetectionStatus = "Active"
                ActiveCounter = ActiveCounter + 1
                # Set Detection Status to Active, if there is a larger movement in the detection window
                InactiveCounter = 0                                                                                     # Reset the Inactive Counter, because there is some activity detected
                #print cv2.contourArea(c)
                #time.sleep(0.1)                                                                                        # optional: slowmotion when movement detected (only offline modus)

        if UpdateTime > conf["MinTimeToWaitForUpdateBackground"] and \
                        InactiveCounter >= conf["MinNoMovementFramesToWaitForUpdateBackground"]:                                # update background image
            firstFrame = Grayscaled_Picture
            print "updated first frame @ ",elapsedtime
            TimeSinceLastUpdate = time.time() - Starttime

        DrawDetectionFrames(LiveFeed)
        DrawVideoInformation(LiveFeed, DetectionStatus, TrafficCounter, ManualCounter, elapsedtime)
        
        ShowVideoOutput(LiveFeed, frameDelta, thresh, firstFrame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:                                                                                                   # if the ESC key is pressed, break from the loop
            cv2.imwrite("Screenshots\Final.jpg", LiveFeed)                                                              # write the last frame to a file for storage
            break
        if key == ord("c"):                                                                                             # "c" increases the counts of manual counted vehicles
            ManualCounter=ManualCounter+1
        if key == ord("x"):                                                                                             # "x" will store the current frame as picture with prefix "missed detection"
            print "missed detection @ ", elapsedtime
            cv2.imwrite("Screenshots\missed_dectection @ "+format(elapsedtime)+ ".jpg", LiveFeed)
        if key == ord("l"):                                                                                             # "l" manually triggers the background substraction relearn
            print "manually learn new first frame"
            firstFrame = Grayscaled_Picture

    StatisticFileName.close()
    CloseCamera(camera)


# Calibration Definitions-----------------------------------------------------------------------------------------------
#global mindetectionwindowY
#global maxdetectionwindowY
#global mindetectionwindowX
#global maxdetectionwindowX
#global DetectionLine
global DetectionLineUpperPoint
global DetectionLineLowerPoint
#global MinObjectSize
#global DilateIterations
#global ThresholdCalibration
#global MaximumMovementDelta
#global MinTimeToWaitForUpdateBackground
#global MinNoMovementFramesToWaitForUpdateBackground
global StatisticFile



DetectionLineUpperPoint= conf["DetectionLine"], conf["mindetectionwindowY"]
DetectionLineLowerPoint= conf["DetectionLine"], conf["maxdetectionwindowY"]
StatisticFile = r'C:\Data\Git\Tools\TrafficDetection\Statistic_'+format(datetime.datetime.now().strftime("%Y%m%d_%H%Mq%S"))+'.csv'

print "Main Menu:"                                                                                                      # Main Menu
print "C - Calibrate Camera"
print "R - Record Video"
print "O - Offline Video Analysis"
print "L - Live Traffic Detection"
print "Q - Quit"

camera = ""
while True:                                                                                                             # endless loop
    Selection=raw_input("Your Choice : ")
    if Selection.lower() == "c":
        camera = OnlineVideo()
        CameraCalibration(camera)
    if Selection.lower() == "r":
        camera = OnlineVideo()
        RecordVideo(camera)
    if Selection.lower() == "o":
        camera = OfflineVideo()
        TrafficDetection(camera)
    if Selection.lower() == "l":
        camera = OnlineVideo()
        TrafficDetection(camera)
    if Selection.lower() == "q" or Selection == chr(27):
        print str(camera)
        if camera != "":
            CloseCamera(camera)
        print "[Tool Status] - ENDED"
        break
