# from __future__ import unicode_literals
# import youtube_dl
import os
from flask import Flask, flash, request, redirect, url_for, session,jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
# import logging
from  extract_frame  import  *
from  genetic  import  *
from  ocr  import  *
from audio import *
from merge import *
from summ import *
from mcq import  *


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = './videos'

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER)
    if not os.path.isdir(target):
        os.mkdir(target)
    print("welcome to upload`")
    file = request.files['file'] 
    print(file.filename)
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    print("File Upload Success")

    time_stamps=extract(destination)
    print("TimeStamps Extracted")
    
    update_time=genDE(time_stamps)
    print("Updated TimeStamps Extracted")

    ocr_extract=ocr_extraction(update_time,destination)
    print("OCR Extracted")

    audio_ext=audio_extract(destination,update_time)
    print("Audio Extracted")

    transcript=final_merge(ocr_extract,audio_ext)
    print("Transcript Extracted", transcript)
    summary=t5(transcript)
    print("Summary Generated",summary)
    
    # transcript={"hi":"hello"}
    # summary=['A database view is a subset of a database and is based on a query that runs on one or more database tables. Database views are saved in the database as named queries and can be used to save frequently used, complex queries. There are two types of database views: dynamic views and static views.']
    
    question=gen_mcq(summary)
    print("Question Generated")

    return jsonify({"data":"File Upload Success","transcript":transcript,"summary":summary,"question":question})
    


if __name__ == "__main__":
    #code  to get video from youtube


    # DOWNLOAD_PATH = "./videos/"   
    # # link of the video to be downloaded  
    # link="https://www.youtube.com/watch?v=Xi8Fabcb_MA" 
    # ydl_opts = {
    #     'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
    #     }
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([link])

    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=True)
