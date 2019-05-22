# box section of image

from PIL import Image, ImageFilter, ImageOps, ImageDraw
import os
import sys

directory = sys.argv[1]

for filename in os.listdir(directory):
    if os.path.splitext(filename)[1] == ".jpg":
        rawname = os.path.splitext(filename)[0]
        im = Image.open(os.path.join(directory, filename)).convert("RGBA")
    else:
        continue

    width, height = im.size

    with open("%s.txt" % (os.path.join(directory, rawname))) as textFile:
        lines = [line.split() for line in textFile]


    def labels2box(width, height, line):
        b1 = width * (float(line[1]) - 0.5 * float(line[3]))
        b2 = height * (float(line[2]) - 0.5 * float(line[4]))
        b3 = width * (float(line[1]) + 0.5 * float(line[3]))
        b4 = height * (float(line[2]) + 0.5 * float(line[4]))
        #print(int(b1), int(b2), int(b3), int(b4))
        return (int(b1), int(b2), int(b3), int(b4))


    boxes = []

    for line in lines:
        boxes.append(labels2box(width, height, line))

    trigger = [2, 7]

    for i in range(len(boxes)):
        if (int(lines[i][0]) in trigger):
            box = boxes[i]
            box_width = box[2] - box[0]
            box_height = box[3] - box[1]
            print(box_width)
            print(box_height)
            draw = ImageDraw.Draw(im)
            draw.rectangle(box)
#            im.paste(ic, Image.open("sponge.png"))
#            ic = ic.filter(ImageFilter.GaussianBlur(10))
#            ic = ic.filter(ImageFilter.BLUR)
#            ic = ic.filter(ImageFilter.BLUR)
#            im.paste(ic, box)

    im.save("%s_boxed.png" % (os.path.join(directory, rawname)))
