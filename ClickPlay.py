#this program will play the audio for each charachter based on pressing on them
#read in text file
# for each click recognize the page numbers
#find the color for that charachter
#if the click contains that color then play the audio
#when click up then stop playing the audio

#go through images and decide if the charachter is present
#if the charachter is present on that page and there is audio for that charachter on that page
    #then play the audio

from gtts import gTTS
from playsound import playsound
import cv2 as cv
import os
from mutagen.mp3 import MP3
import numpy as np
from matplotlib import pyplot as plt

diction = {
  'nar': 'en-au',
  'one': 'en-ca',
  'two': 'en-in',
  'three': 'en-nz',
  'four': 'en-ie',
  'five': 'en-gb',
  'six': 'en-ng',
  'seven': 'en-gh',
  'eight': 'en-ph',
  'nine': 'en-tz',
  'ten': 'en-uk',
  'eleven': 'en-us',
  'unknown': 'en-za'
}
dictionTwo = {
  '1': 'en-au',
  '2': 'en-ca',
  '3': 'en-in',
  '4': 'en-nz',
  '5': 'en-ie',
  '6': 'en-gb',
  '7': 'en-ng',
  '8': 'en-gh',
  '9': 'en-ph',
  '10': 'en-tz',
  '11': 'en-uk',
  '12': 'en-us',
  '13': 'en-za'
}
color = {}

fileTest = open('bear.txt', 'r')
lines = fileTest.readlines()
fileTest.close()
obj_list = []
time_tracker = []

img = cv.imread('bear/bear-12.jpg', 1)
r = 1000.0 / img.shape[1]
dim = (1000, int(img.shape[0] * r))

# perform the actual resizing of the image and show it
resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
# cv.Not(im,im)
# f=cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX,1.0,1.0,1.0,1,8)
cv.namedWindow("Display", cv.WINDOW_NORMAL)


#	this is the method to define a mouse callback function. Several events are given in OpenCV documentation
counter = 0
def my_mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:  # here event is left mouse button double-clicked
        print x, y
        print(resized[x,y])
        if resized[x,y] in color.keys:
             voice = color[resized[x,y]]
             audio = dictionTwo[voice]

        else:
            counter =+ 1
            voice = counter
            audio = dictionTwo[voice]
            color[resized[x, y]] = counter

        for i, line in enumerate(lines):
            sound = line.split(":")
            speaker = sound[0]
            if audio == diction[speaker]:
                txt = sound[1]
                tts = gTTS(text=txt, lang=audio)
                filename = '/tmp/temp.mp3'
                tts.save(filename)
                playsound('/tmp/temp.mp3')

        # text="{0},{1}".format(x,y)
        # cv.PutText(im,text,(x+5,y+5),f,cv.RGB(0,255,255))
print(color)
cv.setMouseCallback("Display", my_mouse_callback)  # binds the screen,function and image


while (1):
    cv.imshow("Display", resized)
    if cv.waitKey(15) % 0x100 == 27: break  # waiting for clicking escape key
cv.destroyAllWindows()
