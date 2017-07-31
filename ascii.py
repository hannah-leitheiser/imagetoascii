# Turns an image into ASCII art.
# requires python3 and PIL, and UbuntuMono-R.ttf 
#  (you will have to change the font for different operating systems.)

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
# ASCII 0-256 that printed on my terminal
printables = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀ'

print("Prints ASCII representation of an image.")
imageFileName = str( input("Filename (default: image.png):") or 'image.png')
fontSize = int ( input("Font Size (default: 24):") or 24 )
invert = input("Invert(Y/N) (default: N):");
if invert == 'y' or invert == 'Y':
   textBackgroundColor = "black"
   textColor = (255,255,255,255)
else:
   textBackgroundColor = "white"
   textColor = (0,0,0,255)

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
