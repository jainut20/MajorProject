import numpy as np
import os
import shutil
import cv2
import time
import pickle


def extract(video_path):
    for filename in os.listdir('./temp/'):
        filepath = os.path.join('./temp/', filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)
    p_frame_thresh = 400000 # You may need to adjust this threshold
    start_time = time.time()
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(5))
    if(fps==0):
        print("Not available")
    # Read the first frame.
    ret, prev_frame = cap.read()
    i = 1
    count = 1
    try:
        cv2.imwrite('./temp/_'+str(i)+'.jpg',prev_frame)
    except:
        print("No frame to save")
    temp=[]
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    while ret:
        ret, curr_frame = cap.read()
        frame_count+=1
        if ret:
            diff = cv2.absdiff(curr_frame, prev_frame)
            non_zero_count = np.count_nonzero(diff)
            if non_zero_count > p_frame_thresh:
                temp.append(float(frame_count)/fps)
                print("Saving Frame number: {}".format(i), end='\r')
                count += 1
                cv2.imwrite('./temp/_'+str(count)+'.jpg',curr_frame)
            prev_frame = curr_frame
            i += 1
    print("Total Number of frames saved: {}".format(count))
    print(temp)
    print("Total time take by thresholding is : %s seconds" % (time.time() - start_time))
    return temp
