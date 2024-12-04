# color_viewer.py
#   custom eyedropper tool for sokoban images.
# Leslie Liu / leslieli / Section Q

from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image

def loadPILImage(url):
    return Image.open(url).convert('RGB')

def onAppStart(app, path):
    app.path = path
    app.PILImg = loadPILImage(path)
    app.CMUImg = CMUImage(app.PILImg)
    app.padding = 20
    app.CMUImgLeft = 20
    app.CMUImgTop = 100
    app.CMUImgWidth, app.CMUImgHeight = getImageSize(path)
    app.width = app.CMUImgWidth + (2 * app.padding)
    app.height = app.CMUImgTop + app.CMUImgHeight + (2 * app.padding)
    app.userMX, app.userMY = 0,0
    app.rVal, app.gVal, app.bVal = None, None, None

def analyzeColors(app):
    if (app.userMX in range(app.PILImg.width)) and (app.userMY in range(app.PILImg.height)):
        app.rVal,app.gVal,app.bVal = app.PILImg.getpixel((app.userMX,app.userMY))

def onMouseMove(app,mx,my):
    app.userMX = mx - app.CMUImgLeft
    app.userMY = my - app.CMUImgTop
    analyzeColors(app)

def redrawAll(app):
    drawLabel('Color Viewer', app.width/2, 20, size=16, bold=True)
    drawLabel(f'file = {app.path}', app.width/2, 35, size=14)
    if (app.userMX in range(app.PILImg.width)) and (app.userMY in range(app.PILImg.height)):
        colorInfo = f'mouse @ ({app.userMX},{app.userMY}): rgb({app.rVal},{app.gVal},{app.bVal})'
    else:
        colorInfo = f'mouse out of bounds of image'

    drawLabel(colorInfo,app.width/2, 50, size=14)
    drawLine(app.CMUImgLeft,app.CMUImgTop-app.padding,app.width-app.padding,app.CMUImgTop-app.padding)
    drawImage(app.CMUImg,app.CMUImgLeft,app.CMUImgTop,align='top-left')

def main():
    runApp(path='level1-10x10.png')
    # runApp(path='level2-7x9.png')
    # runApp(path='level3-8x6.png')
    # runApp(path='level4-8x6.png')

main()
