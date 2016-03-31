
from PIL import Image
import os
import random
from math import floor
import math

animate = True

tries = 500
points = []

frames = []
framecount = 8

files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) and f.split(".")[-1] in ["jpg","jpeg","png"] ] 

background = "none"
bg_w = 300
bg_h = 300

for f in files:
    name = f.split(".")

    if "bg" in name:
        background = Image.open(f)  
        bg_w, bg_h = background.size
        for seg in name:
            if seg[0] == "s" and len(seg)>1:
                ratio = int(seg[1:])
                background.thumbnail((floor(bg_w*ratio/100), floor(bg_h*ratio/100)))
                bg_w, bg_h = background.size

            if seg[0] == "x" and "y" in seg and "p" in seg:
                x = int( seg.split("x")[1].split("y")[0])
                y = int( seg.split("y")[1].split("p")[0])
                p = int( seg.split("p")[1])
                points.append((x,y,p))

if background == "none":
    background = Image.new('RGBA', (bg_w, bg_h), (200, 200, 200, 255))

print(bg_w,bg_h)

for i in range(framecount):
    frames.append(background.copy())

for f in files:    
    name = f.split(".")
    print(name)
    ignore = False

    if "bg" not in name:
        image = Image.open(f)
        im_w, im_h = image.size
        ratio = 35
        gyrate = 10
        alpha = 255
        for seg in name:
            if seg[0] == "s" and len(seg)>1 and seg[1:].isdigit():
                ratio = int(seg[1:])
                print("ratio",ratio)
            if seg[0] == "g" and len(seg)>1 and seg[1:].isdigit():
                gyrate = int(seg[1:])
                print("gyrate",gyrate)
            if seg == "tmp":
                print("ignore")
                ignore = True
            if seg[0] == "a" and len(seg)>1 and seg[1:].isdigit():
                alpha = int(seg[1:])
                print("alpha",alpha)
       
        if ignore: continue

        image.thumbnail((int(bg_w*ratio / 100), int(bg_h*ratio / 100)))
        image.putalpha(alpha)
        im_w, im_h = image.size

#        best = (random.randrange(0,bg_w - im_w),random.randrange(0,bg_h - im_h))
#        bestd = (best[0]-pointx)**2 + (best[1]-pointy**2)
#        for i in range(tries):
#            offset = (random.randrange(0,bg_w - im_w),random.randrange(0,bg_h - im_h)) 
#           distance = (offset[0]-pointx)**2 + (offset[1]-pointy**2)
#            if distance > bestd:
#                best = offset
#                bestd = distance
#
#        pointx = (best[0]*ratio + pointx*strength)/(ratio+strength)
#        pointy = (best[1]*ratio + pointy*strength)/(ratio+strength)
#        strength += ratio

        best = (random.randrange(0,bg_w - im_w),random.randrange(0,bg_h - im_h))
        bestscore = "none"
        for i in range(tries):
            if len(points)==0: break
            offset = (random.randrange(0,bg_w - im_w),random.randrange(0,bg_h - im_h)) 
            score = 0
            for p in points:
                distance = (offset[0]+int(im_w/2)-p[0])**2 + (offset[1]+int(im_w/2)-p[1])**2 + .000001
                score += p[2]**3/(distance**2)
            if bestscore == "none" or score < bestscore:
                best = offset
                bestscore = score

        points.append((best[0]+floor(im_w/2),best[1]+floor(im_h/2),ratio))
        direction = random.choice([-1,1])
        if animate:
            for i in range(len(frames)):
                angle = (i/framecount)*2*math.pi * direction
                offset = (int(best[0]+math.cos(angle)*im_w*gyrate/100),int(best[1]+math.sin(angle)*im_h*gyrate/100))
                frames[i].paste(image,offset,image)
        else:
           background.paste(image,best,image)

if animate:

    

    if not os.path.exists("out.tmp.frames"):
        os.makedirs("out.tmp.frames")
    else:
        os.system("rm out.tmp.frames/*")
        
    for i in range(len(frames)):
        frames[i].save("out.tmp.frames/" + str(i) + ".jpg")

    os.system("ffmpeg -y -r 10 -i out.tmp.frames/%d.jpg -threads 0 out.tmp.frames/out.tmp.webm")

else:
    background.save('out.tmp.png')

