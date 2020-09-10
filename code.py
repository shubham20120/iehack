import moviepy.editor as mp
import speech_recognition as sr
import requests
import sys

#path="/home/hackathon/shubham/iehack/"+str(sys.argv)

clip = mp.VideoFileClip(r"/home/hackathon/shubham/iehack/xyz.mp4")


clip.audio.write_audiofile(r"/home/hackathon/shubham/iehack/xyz.wav")


r = sr.Recognizer()


with sr.AudioFile('/home/hackathon/shubham/iehack/xyz.wav') as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    print(text)

