import pytesseract
import argparse
import cv2
import os
from PIL import Image
from autocorrect import spell

def main():
    # Set up arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", action="store", default="")
    args = ap.parse_args()
    filename = args.image
    if (filename == ""):
        filename = input("Please enter an image file: ")
    # Read in file for preprocessing
    image = cv2.imread(filename)
    gray = cv2.medianBlur(image, 3)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0 ,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    new_name = filename.split(".")[0] + "_processed." + filename.split(".")[1]
    # cv2.imwrite(new_name,gray)

    #run OCR and print results
    text = pytesseract.image_to_string(gray)
    print(text)

    #dispaly image
    # os.remove(new_name)
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", image)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
