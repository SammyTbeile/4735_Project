# replace all occurences of "Mac" to "PC" and "Firefox" to "Chrome"
# sub_pairs = [('Mac', 'PC'), ('Firefox', 'Chrome')]
# pp = PreProcessorSub(sub_pairs)
#       - pp = re.compile('Mac', re.IGNORECASE), repl = 'PC'),
#               re.compile('Firefox', re.IGNORECASE), repl = 'Chrome')
#pp.run("I use firefox on my mac")
# new page marker
# different charachter reader
"""
  en-au: English (Australia)
  en-ca: English (Canada)
  en-gb: English (UK)
  en-gh: English (Ghana)
  en-ie: English (Ireland)
  en-in: English (India)
  en-ng: English (Nigeria)
  en-nz: English (New Zealand)
  en-ph: English (Philippines)
  en-tz: English (Tanzania)
  en-uk: English (UK)
  en-us: English (US)
  en-za: English (South Africa)

fullTextPg1 = 'Boland was a little dinasaur. He lived with his mother and father in a great swamp forest. There were a lot of dinasaur children in Bolands neighborhood.'
#...

fullTextPg3 = 'Bolands playmates tried to help.'
mytext = 'You have to get Tyrone to be your friend,'

language = 'en'
mytextTwo = 'Hello Jill. I am doing well'
languageTwo = 'en-uk'
# can have multiple langauges
myobj = gTTS(text=mytext, lang=language, slow = False)
myobjTwo = gTTS(text=mytextTwo, lang=languageTwo, slow = False)
#myobj.save("John.mp3")
#myobjTwo.save("Jill.mp3")

with open('hello_both.mp3', 'wb') as f:
    myobj.write_to_fp(f)
    myobjTwo.write_to_fp(f)
"""
#-*- coding: utf-8 -*-
import os
from mutagen.mp3 import MP3
from gtts import gTTS
import sys
from gtts import tokenizer
from gtts.tokenizer import pre_processors, Tokenizer
import gtts.tokenizer.symbols

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

#fileTest = open('sample.txt', 'r')
fileTest = open(sys.argv[1], 'r')
lines = fileTest.readlines()
fileTest.close()
obj_list = []
time_tracker = []
#gTTS.tokenizer.symbols.SUB_PAIRS.append(('-', '  '))
#gTTS.tokenizer.symbols.SUB_PAIRS.append(('ght', 'fight'))
#gTTS.tokenizer.symbols.SUB_PAIRS.append(('ight', 'fight'))
for i, line in enumerate(lines):
    sound = line.split(":")
    if "Page " in sound[0]:
        language = diction['nar']
        mytext = sound[0] + "                                         "
        # can have multiple langauges
        myobj = gTTS(text=mytext, lang=language, slow=True)
        time_tracker.append(sound[0])
        myobj.save('example.mp3')
        audio = MP3('example.mp3')
        time_tracker.append(audio.info.length)
        obj_list.append(myobj)
    else:
        lang = diction[sound[0]]
        if sound[1] != '\n':
            text = sound[1]
            #pre_processors.word_sub(text)
            text.replace('-', ' ')
            text = ''.join([i if ord(i) < 128 else ' ' for i in text])
        else:
            print('HELLO')
            text = 'space'

        # can have multiple langauges
        obj = gTTS(text=text, lang=lang, slow=False)
        obj.save('example.mp3')
        audio = MP3('example.mp3')
        time_tracker.append(audio.info.length)
        obj_list.append(obj)
timeSum = 0
final_list = []
for time in time_tracker:
    if type(time) == str:
        final_list.append(timeSum)
        timeSum = 0
    else:
        timeSum = timeSum + time
#for the last page
final_list.append(timeSum)
audiofile = open('timeing.txt', 'w+')

for i, a in enumerate(final_list):
    if i != 0:
        audiofile.write('file')
        audiofile.write(' book/page')
        audiofile.write(str(i))
        audiofile.write('.jpg\n')
        audiofile.write('duration ')
        audiofile.write(str(a))
        audiofile.write('\n')
audiofile.close()

with open('CatAudio.mp3', 'wb') as f:
    for v in obj_list:
        v.write_to_fp(f)
f.close()
os.system("ffmpeg -i CatAudio.mp3 -f concat -i timeing.txt -vcodec mpeg4 -y cubeCat.mp4")