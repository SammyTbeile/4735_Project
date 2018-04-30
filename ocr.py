import io
import argparse
import cv2
import os
from PIL import Image
import wand.image
import pyocr
import numpy as np

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
        filename = input("Please enter an image file: ")

    # Split pdf by pages
    image_pdf = wand.image.Image(filename=filename, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')
    images = []
    for img in image_jpeg.sequence:
        image_page = wand.image.Image(image=img)
        images.append(image_page.make_blob('jpeg'))

    print("got " + str(len(images)) + " images")
    i =1
    for image in images:
        # Read in file for preprocessing
        image = Image.open(io.BytesIO(image)).convert('RGB')
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.medianBlur(image, 3)
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.threshold(gray, 0 ,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        new_name = "page" + str(i) + ".jpg"
        cv2.imwrite(new_name,gray)

        #run OCR and print results
        # text = pytesseract.image_to_string(gray)
        text = tool.image_to_string(
            Image.open(new_name),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        print(text)

        #dispaly image
        # os.remove(new_name)
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        i +=1

if __name__ == "__main__":
    main()
