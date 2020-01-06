# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 16:40:53 2018

@author: jtreguer
"""

import cv2
import sys
 
minor_ver = 4    
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[5]
    # 0,1,2,3,4,6,7 tested OK
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            print("Creating GOTURN tracker")
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
 
    # Read video
    video = cv2.VideoCapture("chaplin.mp4")
    #video = cv2.VideoCapture("reduced_flame.avi")
 
    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
     
    # Define an initial bounding box
    #bbox = (276, 23, 86, 320)
    bbox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
    #bbox = cv2.selectROI(frame, False)
 
    # Initialize tracker with first frame and bounding box
    # Result of a detection
    ok = tracker.init(frame, bbox)
    print("First frame initialization completed")
 
    cv2.waitKey(0)
    
    while True:
        # Read a new frame
        ok, frame = video.read()
         
        if not ok:
            print("EOF reached")
            break
         
        
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    print("Loop left")        
    video.release()
    # Closes all the frames
    cv2.destroyAllWindows()

#while True:
#    k = cv2.waitKey(1) & 0xFF
#    print(k)
#    if k==ord('q'): break
    
            