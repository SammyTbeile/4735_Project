import io
import argparse
import cv2
import os
from PIL import Image
import wand.image
import pyocr
import numpy as np
import re

# Helper function to convert number to word
def getWord(i):
    names = ["", "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten", "eleven", "twelve"]
    return names[i]


def main():
    # Set up arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", action="store", default="")
    ap.add_argument("-t", "--tools", action="store", default="")
    ap.add_argument("-l", "--lang", action="store", default="")
    args = ap.parse_args()

    # Get desired OCR tool:
    tool_choice = args.tools
    if(tool_choice == ""):
        tool_list = "Please select the number of your desired OCR tool:\n"
        i = 0
        for tool in pyocr.get_available_tools():
            tool_list += str(i+1) + ". " + str(tool) + "\n"
            i+=1
        tool_choice = input(tool_list)
    tool = pyocr.get_available_tools()[int(tool_choice)-1]

    # Get desired language
    lang_choice = args.lang
    if(lang_choice == ""):
        lang_list = "Please select the number of your desired language:\n"
        i = 0
        for lang in tool.get_available_languages():
            lang_list += str(i+1) + "." + str(lang) +"\n"
            i+=1
        lang_choice = input(lang_list)
    lang = tool.get_available_languages()[int(lang_choice)-1]

    # get pdf
    filename = args.image
    if (filename == ""):
        filename = input("Please enter a pdf file: ")

    # Split pdf by pages
    image_pdf = wand.image.Image(filename=filename, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')
    images = []
    for img in image_jpeg.sequence:
        image_page = wand.image.Image(image=img)
        images.append(image_page.make_blob('jpeg'))

    # Go page by page and do OCR
    print("got " + str(len(images)) + " images")
    # Page counter
    i =0
    # Character counter
    current_char = 1
    # List to hold assigned lines
    sentences = []
    # Dictionary to hold conversion between characters and nubmers (for tts)
    characters = dict()
    # List of pronouns
    pronouns = ["he", "she", "they"]
    # Loop to do the heavy lifting
    for image in images:
        i +=1
        # Read in file for preprocessing
        image = Image.open(io.BytesIO(image)).convert('RGB')
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.medianBlur(image, 3)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0 ,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        new_name = "page" + str(i) + ".jpg"
        cv2.imwrite(new_name,gray)

        #run OCR and print results
        # text = pytesseract.image_to_string(gray)
        text = tool.image_to_string(
            Image.open(new_name),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        #Print OCR of the page
        print("Page: " + str(i))
        print(text)
        print("\n")

        # Parse the text to determine speaker
        # text = "Page " + str(i) +"\n" + str(text)
        sentences.append("Page  " + str(i) + ":\n")

        # for sentence in text.split("\n"):
        sentence = text
        # Standardizez quotation marks
        sentence = sentence.replace("“","\"")
        sentence = sentence.replace("”", "\"")
        # Don't record empty lines
        if (sentence == ""):
            continue
        #If there is no quotes then it must be narrator
        if("\"" not in sentence and "“" not in sentence and "”" not in sentence):
            # get rid of newlines in the sentence (for tts)
            sentences.append("nar: " + str(sentence.replace("\n"," ")) + "\n")

        #Otherwise we will need to parse it
        else:
            # remove the quoted (spoken) portion from the line
            res = re.findall(r'"([^"]*)"', sentence)
            print("res: " +str(res))
            sentence_portion = sentence.replace("\"","")
            # keep track of speakers for pronoun references
            speakers = []
            if(res != None):
                # for each quote attribute preamble to narrator and process quote
                previous_char = ""
                for quote in res:
                    print("quote is: "  + quote)
                    print("quote to process is: " + sentence_portion)

                    # Split the sentence into the part before the quote and after
                    without_quote = sentence_portion.split(quote)
                    print("w/o quote: " + str(without_quote))
                    # if there is stuff before the quote, attribute to narrator and then continue to process the quote
                    if (without_quote[0] != ""):
                        print("In nar block")
                        print("w/o quote:" + str(without_quote))
                        sentences.append("nar: " + str(without_quote[0].replace("\n"," ")) + "\n")

                    # Process the current quote
                    quote_to_process = quote.replace("\"", "")
                    # if there is more than one quote, we need to isolate what comes after
                    if (len(res) >1):

                        print("processing")
                        print("w/o quote processing: " + str(without_quote))
                        if(len(without_quote) <2):
                            print("In here")
                            print(without_quote)
                            if(without_quote  == ""):
                                continue
                            if (previous_char not in characters):
                                characters[previous_char] = getWord(current_char)
                                current_char +=1
                            sentences.append(characters[previous_char] + ": " + str(without_quote.replace("\n"," ")) + "\n")
                            continue
                        # if the quote occurs at the end check for a previous character
                        if(without_quote[1] == ""):
                            print("In this one")
                            # print(quote_to_process)
                            if (previous_char not in characters):
                                characters[previous_char] = getWord(current_char)
                                current_char +=1
                            sentences.append(characters[previous_char] + ": " + str(quote_to_process.replace("\n"," ")) + "\n")
                            continue
                        # otherwise get the text between the two quotes
                        if (res.index(quote) != len(res) -1):
                            print("in between")
                            # print(without_quote)
                            # print("creating between from: " + str(quote) + " and:  " + str(res[res.index(quote) + 1]))
                            # print("between list" + str(without_quote[1].split(res[res.index(quote) + 1])))
                            between = without_quote[1].split(res[res.index(quote) + 1])[0]
                            if (between.strip() == ""):
                                # print("Found character: "  + char_name)
                                # print(quote)
                                if(char_name not in speakers):
                                    speakers.append(char_name)
                                if(char_name not in characters):
                                    characters[char_name] = getWord(current_char)
                                    current_char += 1
                                previous_char = char_name
                                sentences.append(characters[char_name] + ": " + str(quote.replace("\n"," "))  + "\n")
                                sentence_portion = sentence_portion.split(quote)[1]
                                continue
                                # between = without_quote[1].split(res[res.index(quote) + 1])[1]
                            # print("between: " + str(between))
                            #If there is no between, use the previous character
                            if(between.strip() == ""):
                                if (previous_char not in characters):
                                    characters[previous_char] = getWord(current_char)
                                    current_char +=1
                                sentences.append(characters[previous_char] + ": " + str(quote.replace("\n", " ")) + "\n")
                                sentence_portion = sentence_portion.split(quote)[1]
                                continue
                            char_name = ""
                            # Look for the first capitalized word or pronoun
                            for word in between.split():
                                if(word.capitalize() == word and word != "It" and word not in pronouns):
                                    char_name = word.strip().strip(".").strip("'s")
                                    break
                                if(word.strip() in pronouns):
                                    # print("speakers: " + str(speakers))
                                    if(previous_char in speakers and len(speakers) >1):
                                        speakers2 = speakers.copy()
                                        speakers2.remove(previous_char)
                                        speakers2.reverse()
                                        char_name = speakers2[0].strip(".")
                                    else:
                                        char_name = previous_char
                                    break
                            if(char_name != ""):
                                # print("Found character: "  + char_name)
                                # print(quote)
                                if(char_name not in speakers):
                                    speakers.append(char_name)
                                if (char_name not in characters):
                                    characters[char_name] = getWord(current_char)
                                    current_char +=1
                                previous_char = char_name
                                sentences.append(characters[char_name] + ": " + str(quote.replace("\n"," "))  + "\n")
                            else:
                                sentences.append("unknown" + ": " + str(quote.replace("\n"," "))  + "\n")
                                # sentences.append("nar: " + str(without_quotes))
                        # Another possiblity is that the part of the previous narrator is between them
                        else:
                            print("in else")
                            if(("nar: " + str(without_quote[0].replace("\n","")) +"\n") not in sentences):
                                sentences.append("nar: " + str(without_quote[0].replace("\n"," ")) + "\n")
                            if(previous_char != ""):
                                sentences.append(characters[previous_char] + ": " + str(quote.replace("\n"," ")) + "\n")
                            else:
                                sentences.append("unknown: " + str(quote.replace("\n"," ")) + "\n")
                            sentences.append("nar: " + str(without_quote[1].replace("\n"," ")) + "\n")
                            # sentence_portion = sentence_portion.split(quote)[1]
                            continue
                    #If there is only one quote (we also know quote is at beginning)
                    elif (len(res) == 1):
                        char_name = ""
                        # Look for the first capitalized word or pronoun
                        for word in without_quote[1].split():
                            if(word.capitalize() == word and word != "It" and word not in pronouns):
                                char_name = word.strip().strip(".").strip("'s")
                                break
                            if(word.strip() in pronouns):
                                # print("speakers: " + str(speakers))
                                if(previous_char in speakers and len(speakers) >1):
                                    speakers2 = speakers.copy()
                                    speakers2.remove(previous_char)
                                    speakers2.reverse()
                                    char_name = speakers2[0].strip(".")
                                else:
                                    char_name = previous_char
                                break
                        if(char_name != ""):
                            # print("Found character: "  + char_name)
                            # print(quote)
                            if(char_name not in speakers):
                                speakers.append(char_name)
                            if (char_name not in characters):
                                characters[char_name] = getWord(current_char)
                                current_char +=1
                            previous_char = char_name
                            sentences.append(characters[char_name] + ": " + str(quote.replace("\n"," "))  + "\n")
                            sentences.append("nar: " + str(without_quote[1].replace("\n","")) + "\n")
                        else:
                            sentences.append("unknown" + ": " + str(quote.replace("\n"," "))  + "\n")
                            sentences.append("nar: " + str(without_quote[1].replace("\n","")) + "\n")
                    sentence_portion = sentence_portion.split(quote)[1]
                    print(sentence_portion)

        #dispaly image
        os.remove(new_name)
        # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)

    # remove duplicates
    sentences = sorted(set(sentences), key=sentences.index)
    with open("output.txt", "w") as outfile:
        for sentence in sentences:
            outfile.write(sentence)

if __name__ == "__main__":
    main()
