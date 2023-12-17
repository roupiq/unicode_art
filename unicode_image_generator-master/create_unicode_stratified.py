# -*- coding: utf-8 -*-

"""UNICODE CHARACTER GENERATOR

A script to generate image files for each character in the
first plane of Unicode

"""

import sys
import os
import unicodedata as ucd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import filecmp
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
import time


def showImage(image):
    plt.imshow(image)
    plt.show()


xsize = 128  # size of images
ysize = 295
xoffset = 0  # offset to centralize characters in image
yoffset = 0
shades_of_grey = 256

# font = "consola.ttf"  # font file to use
font = "UbuntuMono-Regular.ttf"  # font file to use
fontsize = 256
FONT = ImageFont.truetype(font, fontsize)
bg = (256, 256, 256)

directory = "unicode_jpgs"
if not os.path.exists(directory):
    os.makedirs(directory)
directory += "/"

letter = chr(10)
empty = (
    directory + "empty.jpg"
)  # get empty to use a reference for when the script didn't render a character
image = Image.new("RGB", (xsize, ysize), (0, 0, 0))
draw = ImageDraw.Draw(image)
draw.text((xoffset, yoffset), letter, font=ImageFont.truetype(font, fontsize), fill=bg)
image.save(empty, "JPEG")

letter = chr(1)
unsupported = (
    directory + "unsupported.jpg"
)  # get unsupported to use a reference for when the script didn't render a character
image = Image.new("RGB", (xsize, ysize), (0, 0, 0))
draw = ImageDraw.Draw(image)
draw.text((xoffset, yoffset), letter, font=ImageFont.truetype(font, fontsize), fill=bg)
image.save(unsupported, "JPEG")
unicodeIndex = {}
indexUnicode = {}

# letter = ''
# unsupported = directory+"unsupported.jpg" # get unsupported to use a reference for when the script didn't render a character
# image = Image.new('RGB', (xsize, ysize), (0,0,0))
# draw = ImageDraw.Draw(image)
# draw.text((xoffset, yoffset), letter, font=ImageFont.truetype(font, fontsize), fill=bg)
# image.save(unsupported, "JPEG")
# unicodeIndex = {}
# indexUnicode = {}

GREYS = []
for i in range(0, shades_of_grey):
    GREYS += [[-1] * shades_of_grey]
# print(GREYS)

letters = []

# for i in range(0x0000, 1 + 0xffff, 1):
for i in range(0x0000, 1 + 0xffff, 1):
    if str.isprintable(chr(i)):
        letters += chr(i)
        # print(chr(i))


# print(letters)


def get_text_dimensions(text_string):
    ascent, descent = FONT.getmetrics()
    if FONT.getmask(text_string).getbbox() == None:
        return (0x213769420, 0x213769420)
    text_width = FONT.getmask(text_string).getbbox()[2]
    text_height = FONT.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)


# print("default:", get_text_dimensions('▒'))
normal_width, amongus = get_text_dimensions("___")


def joinImagesHorizontal(image1, image2):
    image1_size = image1.size
    image2_size = image2.size
    new_image = Image.new(
        "RGB", (image2_size[0] + image1_size[0], image1_size[1]), (256, 256, 256)
    )
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    return new_image


def joinImagesVertical(image1, image2):
    image1_size = image1.size
    image2_size = image2.size
    new_image = Image.new("RGB", (image1_size[0], image1_size[1] + image2_size[1]), bg)
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (0, image1_size[1]))
    return new_image


i = 0
for j in range(len(letters)):
    letter = letters[j]

    name = directory + str(i) + ".jpg"
    # name = directory + letter + ".jpg"

    image = Image.new("RGB", (xsize, ysize), bg)
    draw = ImageDraw.Draw(image)
    draw.text(
        (xoffset, yoffset), letter, font=ImageFont.truetype(font, fontsize), fill=bg
    )

    image.save(name, "JPEG")

    if (
        filecmp.cmp(name, empty)
        or filecmp.cmp(name, unsupported)
        or get_text_dimensions("_" + letter + "_")[0] != normal_width
    ):
        os.remove(name)
    else:
        image = Image.new("RGB", (xsize, ysize), bg)
        draw = ImageDraw.Draw(image)

        color = [0, 0, 0]
        draw.text(
            (xoffset, yoffset),
            letter,
            font=ImageFont.truetype(font, fontsize),
            fill=(color[0], color[1], color[2]),
        )
        # image = image.resize((2, 4), Image.LANCZOS)
        image = image.resize((32, 64), Image.LANCZOS)

        image.save(name, "JPEG")
        unicodeIndex[letter] = i
        indexUnicode[i] = letter
        i += 1


rows = (i) // 1
cols = 1

col = []

kłełe = []

for i in range(0, rows * cols):
    imgN = Image.open(f"{directory}{i}.jpg")
    img = imgN.resize((1, 2), Image.LANCZOS)
    # img2 = img.resize((32, 64), Image.BOX)
    # showImage(joinImagesHorizontal(imgN,img2))
    # showImage(img)

    matrix = np.array(img)

    greys = []
    for x in matrix:
        for pixel in x:
            greys.append((int(pixel[0]) + int(pixel[1]) + int(pixel[2])) // 3)

    # greyscale = sum(greys)//len(greys)
    greys[0] = (greys[0] * shades_of_grey)//256
    greys[1] = (greys[1] * shades_of_grey)//256

    # print(greys)
    # if GREYS[int(greys[0])][int(greys[1])] == -1:
    kłełe.append((int(greys[0]), int(greys[1]), i))
    GREYS[int(greys[0])][int(greys[1])] = i

    col.append((greys, i))

def getchar(x, y):
    if GREYS[x][y] < 0:
        return ' '
    return indexUnicode[GREYS[x][y]]

while len(kłełe) > 0:
    # print(kłełe)
    x, y, v = kłełe[0]
    kłełe = kłełe[1:]

    if x + 1 < shades_of_grey and GREYS[x + 1][y] == -1:
        GREYS[x + 1][y] = v
        kłełe.append((x + 1, y, v))
    if y + 1 < shades_of_grey and GREYS[x][y + 1] == -1:
        GREYS[x][y + 1] = v
        kłełe.append((x, y + 1, v))
    if y > 0 and GREYS[x][y - 1] == -1:
        GREYS[x][y - 1] = v
        kłełe.append((x, y - 1, v))
    if x > 0 and GREYS[x - 1][y] == -1:
        GREYS[x - 1][y] = v
        kłełe.append((x - 1, y, v))


print('"""', end="")
for x in range(0, shades_of_grey):
    for y in range(0, shades_of_grey):
        print(getchar(x, y), end="")
    print("")
print('"""')

os.remove(empty)
os.remove(unsupported)
