# 1. Extract audio from video in wav format
# 2. Split big audio to smaller audio chunks
# 3. Convert smaller audio chunks to text with timestamp

import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
import os
import pickle
import glob
import time
import shutil 

def extract_audio_from_video(userVideoPath):
    clip = mp.VideoFileClip(userVideoPath)
    clip.audio.write_audiofile(r"converted-moviepy.wav")


def split_audio_to_chunks(inputAudioPath, outputFolder, t):
    for filename in os.listdir(outputFolder):
        filepath = os.path.join(outputFolder, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)
    fullAudio = AudioSegment.from_wav(inputAudioPath)
    for i in range(0, len(t)-1):
        t1 = t[i] * 1000
        t2 = t[i+1] * 1000
        newAudio = fullAudio[t1:t2]
        # Exports to a wav file in the current path.
        newAudio.export(outputFolder+"chunk"+str(i)+'.wav', format="wav")


def convert_chunks_to_text(folder, t,d):
    fh = open("audio-recognized.txt", "w+")
    fh.close()
    i = 0
    files = list(filter(os.path.isfile, glob.glob(folder + "*")))
    files.sort(key=lambda x: os.path.getmtime(x))
    for file in files:
        if file.endswith('.wav'):
            speech_to_text_audio(file, t[i], t[i+1],d)
            i += 1


def speech_to_text_audio(audioPath, startTime, endTime,d):
    try:
        fh = open("audio-recognized.txt", "a")
        r = sr.Recognizer()
        audio = sr.AudioFile(audioPath)
        with audio as source:
            audio_file = r.record(source)
        result = r.recognize_google(audio_file)
        d[str(startTime)+", "+ str(endTime)] = result
        fh.write("\n" + str(startTime) + " to " + str(endTime) + "\n")
        fh.write(result+". ")
        fh.close()
    except:
        d[str(startTime)+", "+ str(endTime)] = ""
        fh.write("\n" + str(startTime) + " to " + str(endTime) + "\n")
        fh.write("No text found")
        fh.close()

def audio_extract(video_path,t):
    start_time = time.time()
    audio_name = "converted-moviepy.wav"
    chunksFolder = "AudioChunks/"
    new_b = [0]
    for i in range(1, len(t)):
        if t[i]-t[i-1] > 5:
            new_b.append(t[i-1])
    t = new_b
    d = {}
    extract_audio_from_video(video_path)
    split_audio_to_chunks(audio_name, chunksFolder, t)
    convert_chunks_to_text(chunksFolder, t,d)
    print("Total time take by Audio Algorithm extraction is : %s seconds" % (time.time() - start_time))
    return d
