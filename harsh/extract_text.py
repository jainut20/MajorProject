import random
import cv2
import math
import imageio
from skimage.metrics import structural_similarity as ssim
import pickle
import numpy as np
import os
import shutil
import time
from matplotlib import pyplot as plot
import pytesseract
import re 
from difflib import SequenceMatcher as SM
import nltk

def extract_main():
    with open("test2.txt", "rb") as fp:   # Unpickling
        b = pickle.load(fp)
    new_b=[0]
    for i in range(1,len(b)):
        if b[i]-b[i-1]>5:
            new_b.append(b[i-1])
    for filename in os.listdir('final/'):
        filepath = os.path.join('final/', filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)
    b=new_b
    video_path = "../videos/v1.mp4" # Video path
    cap = cv2.VideoCapture(video_path)
    print(len(b))
    count=0
    for i in range(1,len(b)):
        start=b[i-1]
        end=b[i]
        avg=(start+end)*500
        cap.set(0, avg)
        ret,curr_frame=cap.read()
        if ret:
            cv2.imwrite('final/'+str(i)+'.jpg',curr_frame)
            count+=1
    return b,count

def ocr(b,count):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    config = ('-l eng --oem 1 --psm 3')
    out_text=[]
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()
    for i in range(1,count+1):
        img = cv2.imread('final/'+str(i)+'.jpg')
        # Preprocessing the image starts
    
        # Convert the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        
        # Specify structure shape and kernel size.
        # Kernel size increases or decreases the area
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
        
        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
        
        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                        cv2.CHAIN_APPROX_NONE)
        im2 = img.copy()
        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            
            
        
        # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            # text_encode = text.encode(encoding="ascii", errors="ignore")
            # text_decode = text_encode.decode()
            #text = " ".join([word for word in text_decode.split()])
            text=re.sub(r'\n+', '\n', text).strip()
            text = re.sub("@\S+", "", text)
            text = re.sub("\$", "", text)
            text = re.sub("\¥", "", text)
            text = re.sub("https?:\/\/.*[\r\n]*", "", text)
            text = re.sub("#", "", text)
            text = re.sub(r'"', '', text)
            #text = " ".join(w for w in nltk.wordpunct_tokenize(text) if w.lower() in words or not w.isalpha())
            # if len(out_text)>0:
            #     s1=out_text[-1]
            #     s2=text
            #     if s1 in s2:
            #         text.replace(s1,"")
            # Appending the text into file
            text="["+str(b[i-1])+","+str(b[i])+"]\n"+text
            out_text.append(text)
        # Apply OCR on the cropped image
    file = open("recognized.txt", "a")
    for i in range(len(out_text)):
        file.write(out_text[i])

        file.write("\n\n")
    return out_text

def main():
    start_time = time.time()
    b,count=extract_main()
    out_text=ocr(b,count)
    print("Total time take by OCR extraction is : %s seconds" % (time.time() - start_time))

main()