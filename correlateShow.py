from rain import *
img = None
files =  sorted(glob.glob("img/*.png"))


for f in files:
    im = imread(f)
    if img is None:
        img = imshow(im)
    else:
        img.set_data(im)
    pause(.5)
    draw()

