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

from gtts import gTTS
dict = {
  'nar' : 'en-au',
  'one' : 'en-ca',
  'two' : 'en-in',
  'three' : 'en-nz',
  'four' : 'en-ie',
  'five' : 'en-gb',
  'six' : 'en-ng',
  'seven' : 'en-gh',
  'eight' : 'en-ph',
  'nine' : 'en-tz',
  'ten' : 'en-uk',
  'eleven' : 'en-us',
  'twelve' : 'en-za'
}

file = open('sample.txt', 'r')
lines = file.readlines()
file.close()
list = []
for i, line in enumerate(lines):
    print(i, line)
    sound = line.split(":")
    if "Page " in sound[0]:
        language = dict['nar']
        mytext = sound[0] + "                                         "
        # can have multiple langauges
        myobj = gTTS(text=mytext, lang=language, slow=True)
        list.append(myobj)
    else:
        lang = dict[sound[0]]
        text = sound[1]
        # can have multiple langauges
        obj = gTTS(text=text, lang=lang, slow=False)
        list.append(obj)

print(list)
with open('TyroneTheTerrible.mp3', 'wb') as f:
    for v in list:
        v.write_to_fp(f)
