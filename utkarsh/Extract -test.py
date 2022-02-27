#1. Extract audio from video in wav format
#2. Split big audio to smaller audio chunks
#3. Convert smaller audio chunks to text with timestamp

import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
import os
import pickle
import glob

def extract_audio_from_video(userVideoPath):
    clip = mp.VideoFileClip(userVideoPath)
    clip.audio.write_audiofile(r"converted-moviepy.wav")


def split_audio_to_chunks(inputAudioPath, outputFolder,t):
    fullAudio = AudioSegment.from_wav(inputAudioPath)
    for i in range (0,len(t)-1):
        t1 = t[i] * 1000
        t2 = t[i+1] * 1000
        newAudio = fullAudio[t1:t2]
        newAudio.export(outputFolder+"chunk"+str(i)+'.wav', format="wav") #Exports to a wav file in the current path.

def convert_chunks_to_text(folder,t):
    fh = open("audio-recognized.txt", "w+")
    fh.close()
    i=0
    files = list(filter(os.path.isfile, glob.glob(folder + "*")))
    files.sort(key=lambda x: os.path.getmtime(x))
    for file in files:
        if file.endswith('.wav'): 
            speech_to_text_audio(file,t[i],t[i+1])
            i+=1

def speech_to_text_audio(audioPath,startTime,endTime):
    try:
        fh = open("audio-recognized.txt", "a")
        r = sr.Recognizer()
        audio = sr.AudioFile(audioPath)
        with audio as source:
            audio_file = r.record(source)
        result = r.recognize_google(audio_file)
        fh.write("\n" + str(startTime) + " to " + str(endTime) + "\n")
        fh.write(result+". ")
        fh.close()
    except:
        fh.write("\n" + str(startTime) + " to " + str(endTime) + "\n")
        fh.write("No text found")
        fh.close()



video_path = "C:/Users/Harsh/Desktop/TE/SEM7/Major Project/videos/v1.mp4"
audio_name = "converted-moviepy.wav"
chunksFolder = "AudioChunks/"
with open("../harsh/test2.txt", "rb") as fp:   # Unpickling
        t = pickle.load(fp)
        print(t,len(t))
new_b=[0]
for i in range(1,len(t)):
    if t[i]-t[i-1]>5:
        new_b.append(t[i-1])
t=new_b
extract_audio_from_video(video_path)
split_audio_to_chunks(audio_name,chunksFolder,t)
convert_chunks_to_text(chunksFolder,t)