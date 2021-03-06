# Turns an image into ASCII art.
# requires python3 and PIL, and UbuntuMono-R.ttf 
#  (you will have to change the font for different operating systems.)

#  usage: python3 imageToAscii.py [-h] [-i] [--fontsize FONTSIZE] filename
#  
#  Convert an image to ASCII
#  
#  positional arguments:
#    filename              image filename to convert
#  
#  optional arguments:
#    -h, --help            show this help message and exit
#    -i, --invert          create text for white text on a black background
#    --fontsize FONTSIZE, -f FONTSIZE
#                          Point Size of Font - the larger the fontsize, the
#                          smaller the ASCII output
#  

import argparse

parser = argparse.ArgumentParser(description='Convert an image to ASCII')
parser.add_argument('filename', help='image filename to convert')
parser.add_argument('-i', "--invert", dest='invert',
                   help='create text for white text on a black background', action="store_true")
parser.add_argument("--fontsize", "-f", dest='fontsize', action="store",
                   help='Point Size of Font - the larger the fontsize, the smaller the ASCII output', default=24, type=int)

args = parser.parse_args()

# Save the relevant command line arguments
imageFileName = args.filename
if args.fontsize:
   fontSize = args.fontsize
else: 
   fontSize = 24

if args.invert:
   textBackgroundColor = "black"
   textColor = (255,255,255,255)
else:
   textBackgroundColor = "white"
   textColor = (0,0,0,255)

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
# ASCII 0-256 that printed on my terminal
printables = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀ'

image = Image.open(imageFileName)
width, height = image.size

pixelsImage = image.load()


for y in range(height//fontSize):
   asciiLine = ''
   for x in range(width//(fontSize//2)):
      deviationMin=1e308
      newChar= ''
      for char in printables:
         # Use a small image the size of a character.  Draw the character to the image and compare 
         # that to the associated part of the main image.  Compute the sum of the square deviation
         # and find the character for which that sum is minimum.
         txtBlockImage = Image.new( 'RGB', (fontSize//2,fontSize), textBackgroundColor)
         draw = ImageDraw.Draw(txtBlockImage)
         font = ImageFont.truetype("UbuntuMono-R.ttf", fontSize)
         draw.text((0, 0), char,textColor,font=font)
         pixelsTxt = txtBlockImage.load()
         deviationSum=0
         for blockx in range(fontSize//2):
            for blocky in range(fontSize):
               deviationSum += ( (pixelsTxt[blockx, blocky][0] +
                                                pixelsTxt[blockx, blocky][1] +
                                                pixelsTxt[blockx, blocky][2]) -          
                                               (pixelsImage[x*(fontSize//2) + blockx,y * fontSize + blocky][0] +
                                                pixelsImage[x*(fontSize//2) + blockx,y * fontSize + blocky][1] + 
                                                pixelsImage[x*(fontSize//2) + blockx,y * fontSize + blocky][2])                                                
                                                   ) ** 2
         if deviationSum < deviationMin:
            newChar=char
            deviationMin = deviationSum;
      asciiLine = asciiLine + newChar
   print(asciiLine);
