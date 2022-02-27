#1. Extract audio from video in wav format
#2. Split big audio to smaller audio chunks
#3. Convert smaller audio chunks to text with timestamp

import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
import os

def extract_audio_from_video(userVideoPath):
    clip = mp.VideoFileClip(userVideoPath)
    clip.audio.write_audiofile(r"converted-moviepy.wav")


def split_audio_to_chunks(inputAudioPath, outputFolder):
    t = [0,20,60,119] #Seconds 
    fullAudio = AudioSegment.from_wav(inputAudioPath)
    for i in range (0,len(t)-1):
        t1 = t[i] * 1000
        t2 = t[i+1] * 1000
        newAudio = fullAudio[t1:t2]
        newAudio.export('AudioChunks/chunk'+str(i)+'.wav', format="wav") #Exports to a wav file in the current path.

def convert_chunks_to_text(folder):
    fh = open("audio-recognized.txt", "w+")
    fh.close()
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.wav'): 
            speech_to_text_audio(folder + "/" + filename)

def speech_to_text_audio(audioPath):
    fh = open("audio-recognized.txt", "a")
    r = sr.Recognizer()
    audio = sr.AudioFile(audioPath)
    with audio as source:
        audio_file = r.record(source)
    result = r.recognize_google(audio_file)
    fh.write("\nTimestamp:\n")
    fh.write(result+". ")
    fh.close()


video_path = "C:/Users/Harsh/Desktop/TE/SEM7/Major Project/videos/v2.mp4"
audio_name = "converted-moviepy.wav"
chunksFolder = "AudioChunks"
extract_audio_from_video(video_path)
split_audio_to_chunks(audio_name,chunksFolder)
convert_chunks_to_text(chunksFolder)