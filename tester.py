# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:28:33 2019

@author: mfz.intern
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:28:33 2019

@author: mfz.intern
"""
import numpy as np
import pylab as pl
from scipy.io import wavfile
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from pydub import AudioSegment,silence
from pydub.silence import split_on_silence, detect_nonsilent
import speech_recognition as sr

#read in wave file
sample, data = wavfile.read('longtest.wav')

print("Samples: %d" % sample) #sampling rate
print("Number of items in data array: %d" % len(data)) #how many items in data array
print "Audio length: ", round(data.size/sample/2, 2) #length of audio

t = np.arange(len(data))*1.0/sample #making equal intervals for x axis
pl.plot(t, data)
pl.xlabel("Time")
pl.ylabel("Amplitude")
pl.show() #plot the amplitude -> orange chart

try:
    p = 20*np.log10(np.abs(np.fft.rfft(data))) #fft is the frequencies and power of decibels in data
except ZeroDivisionError:
    p = 0
f = np.linspace(0, sample/2.0, len(p))
pl.plot(f, p)
pl.xlabel("Frequency(Hz)")
pl.ylabel("Power(dB)")
pl.show() #plot fft -> blue chart

def convert(seconds): #converting seconds to minutes, hours etc
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds) 

myaudio = AudioSegment.from_wav('longtest.wav') #check where silence is with pydub

silence = silence.detect_silence(myaudio, min_silence_len=3000, silence_thresh=-50) #detecting where silence is 

nonsilence = detect_nonsilent(myaudio, min_silence_len=3000, silence_thresh=-50) #detecting where sound is

silence = [((start/1000),(stop/1000)) for start,stop in silence] #convert to sec
nonsilence = [((start/1000),(stop/1000)) for start,stop in nonsilence] #convert to sec
print "Silence chunks: ", silence #print where silence is but i keep getting [(0,30)]
print "NONSilent chunks: ", nonsilence #print where silence is but i keep getting [(0,30)]

sT = open("silenceTimes.txt","w+") #open file to write times in

for t in silence:
    t0con = convert(t[0]) #converting the seconds
    t1con = convert(t[1]) #converting the seconds    
    sT.write("Start silence: %s seconds       End silence: %s seconds \n" % (t0con, t1con)) #writing to file

sT.close()

nsT = open("nonsilenceTimes.txt","w+") #open file to write times in

for nt in nonsilence:
    nt0con = convert(nt[0]) #converting the seconds
    nt1con = convert(nt[1]) #converting the seconds    
    nsT.write("Start nonsilence: %s seconds       End nonsilence: %s seconds \n" % (nt0con, nt1con)) #writing to file

nsT.close()

r = sr.Recognizer() #convert audio to audio source
tClips = open("transcribeCips.txt","w+") #open file to write the transcription
countAud = 1 

for x in nonsilence:
    first = x[0] * 1000 #taking times from tuple to extract new audio file
    last = x[1] * 1000
   # print(first)
   # print(last)
    newaudio = myaudio[first:last] #saving new audio snippit
    newaudio.export("audio" + str(countAud) + ".wav", format="wav") #exporting, saving and naming
    if (x[0] != x[1]): #transcribing
        aud = sr.AudioFile("audio" + str(countAud) + ".wav")
        with aud as source:
            audio = r.record(source)
        transcribe = r.recognize_google(audio)
        tClips.write("Clip #" + str(countAud) + ": " + transcribe + "\n")
        print("Clip #" + str(countAud) + ": " + transcribe + "\n")    
    countAud = countAud + 1

tClips.close()




