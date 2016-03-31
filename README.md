# mememaker3000
####To run:
1. load images you want into a directory (must be jpg or png)
2. run mememaker.py from that directory, wait for script to complete 
3. congratulations, your meme has been saved to out.tmp.frames/out.tmp.webm

####Depends On:
+ pillow (python image library)
+ ffmpeg (command line video tool)

####Advanced Options:
+ you can specify one of your images as the background by puting ".bg" into the filename
   - ex) "kitten.bg.jpg"

+ you can specify relative sizes of images too using ".s#" where # is the percent of total height
   - ex) "mainimage.s75.png" #this image will be 75% of the height
   - ex) "extraimage.s10.jpg" #this image will be 10% of the height

+ you can also specify the amount of gyration on each image using ".g#" where # is the radius as a percent of image size
   - ex) "littlespin.g10.png" "lottaspin.g100.png"

+ the transparency can likewise be set using ".a#" where # is between 0 and 255 (corresponmding to alpha)
   - ex) "ghost_spooky.a100.jpg" #the background will show through this ghost 

+ all advanced options (except background) can be combined
   - ex) "transparent_spinning_tiny_thing.a50.s5.g200.png"

+ and as a final note, adding ".tmp" to a images name will tell the script to ignore it
   - ex) "image.tmp.png" #this will not show up in your generated meme
