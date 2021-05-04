import pandas as pd
import argparse
from cv2 import cv2

ap = argparse.ArgumentParser()

ap.add_argument('-i', '--image', required=True, help="Image path")
args = vars(ap.parse_args())
img_path = args['image']


img = cv2.imread(img_path)


dimensions = img.shape
height = img.shape[0]
width = img.shape[1]
area = height*width


clicked = False
r = g = b = xpos = ypos = 0

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=True)

def getColorName(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(csv)):
        d = abs(R-int(csv.loc[i, "R"])) + abs(G-int(csv.loc[i, "G"])) + abs(B-int(csv.loc[i, "B"]))
        if d<=minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]

    return cname


def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        gloabal b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y

        b, g, r = img[y, x]

        b = int(b)
        g = int(g)
        r = int(r)


if area <= 662000:
    cv2.nameWindow('image')
else:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)

cv2.setMouseCallback('image', draw_function)

while(1):
    cv2.imshow("image", img)
    if clicked:
        recEnd = (round(width * .735), round(height * .1))
        textStart = (round(width * .05), round(height * .08))

        cv2.rectangle(img, (20, 20), recEnd, (b, g, r), -1)
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        if r+g+b>600:
            cv2.putText(img, text, textStart, cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(img, text, textStart, cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

        clicked = False

    if cv2.waitKey(28) & 0xFF == 27:
        break

cv2.destroyWindow()
