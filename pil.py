from PIL import Image, ImageDraw, ImageFont, ImageEnhance

import Image
import ImageDraw
import ImageFont
import sys
import os
import os.path

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

def get_pic(name, value):
    filename = "%s.png" % (name)
    if os.path.exists(filename):
        return filename
#TODO:
# 1. existance
# 2. datestamp check
    #os.mkdir(os.path.dirname(filename))
    #fontname = "Arial.ttf"
    fontname = 'wqy-zenhei.ttc'
    fontsize = 14
    text = ("%.2f" % value)

    colorText = "#FEFEFE"
    colorOutline = "red"
    colorBackground = "#0088BB"


    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+4, height+4), colorBackground)
    d = ImageDraw.Draw(img)
    d.text((2, 2), text, fill=colorText, font=font)
    #d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
    img.save(filename)
    return filename
    #return img

#get_pic("BSP", 5555)
