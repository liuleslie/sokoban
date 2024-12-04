# sokoban_loader.py
#   loads levels based on image data. 
# Leslie Liu / leslieli / Section Q


# level files are lightly-edited screenshots from here:
# https://www.sokobanonline.com/play/community/bjertrup/sokomind-plus

from PIL import Image
from cmu_graphics import CMUImage
import pickle, os
import pprint

COLORS = {
    'red':      (175, 71, 68),
    'green':    (114, 187, 82),
    'blue':     (66, 82, 183),
    'violet':   (149, 69, 182),
    'cyan':     (101, 186, 188),
    'brown':    (148, 110, 47),
    'tan':      (245, 218, 131)
}

PIECE_COLORS = [ 'red', 'green', 'blue', 'violet', 'cyan' ]

def readPickleFile(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def writePickleFile(path, contents):
    with open(path, 'wb') as f:
        pickle.dump(contents, f)

def loadPILImage(url):
    return Image.open(url).convert('RGB')

def loadLevel(path):
    # first return a hardcoded level for testing purposes
    if path == None:
        return loadHardcodedLevel()

    fileBaseName = os.path.basename(path)
    fileName = fileBaseName[:-4]

    # if path exists, read pickled file. otherwise, write pickle file
    pickledFileName = f'pickled-{fileName}.pickle'
    
    if os.path.exists(pickledFileName):
        return readPickleFile(pickledFileName)
    
    gameSize = fileName.split('-')[1]
    chunks = gameSize.split('x')
    numRows = int(chunks[0])
    numCols = int(chunks[1])
    PILImg = loadPILImage(path) # read file in as PIL
    rowSize = int(PILImg.height/numRows)
    colSize = int(PILImg.width/numCols)

    level = []
    images = dict()

    m = 3 # margin
    for r in range(0,numRows):
        rowKeys = []
        for c in range(0,numCols):          
            cellKey = getAverageColor(PILImg,c*colSize,r*rowSize,colSize,rowSize)
            rowKeys.append(cellKey)
            if cellKey not in images:
                PILImgCrop = PILImg.crop((c*colSize,r*rowSize,(c*colSize)+colSize,(r*rowSize)+rowSize))
                if cellKey != '-':
                    images[cellKey] = CMUImage(PILImgCrop)
        level.append(rowKeys)
    writePickleFile(pickledFileName, (level,images))
    return level,images

def getAverageColor(img,topLeftX,topLeftY,width,height):
    colorDistThreshold = 50
    tally = dict() # tally of color frequencies.
    for color in COLORS: tally[color] = 0
    m = 3 # margin
    
    for y in range(topLeftY+m,topLeftY+height-m):
        for x in range(topLeftX+m,topLeftX+width-m):
            r,g,b = img.getpixel((x,y))
            for color in COLORS:
                if colorDist(*COLORS[color],r,g,b) <= colorDistThreshold:
                    tally[color] += 1 
    
    # color analysis.
    if tally['brown'] > 2000: return 'w'
    elif tally['tan'] > 800: return 'p'
    else:
        for color,colorFreq in tally.items():
            if colorFreq > 4000: return color[0]
            elif colorFreq > 700: return color[0].upper()
    return '-'

def colorDist(r1,g1,b1,r2,g2,b2):
    return (((r2-r1)**2)+((g2-g1)**2)+((b2-b1)**2))**0.5

def loadHardcodedLevel():
    level = [   [ '-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w' ],
                [ '-', '-', '-', '-', 'w', 'w', 'w', 'R', 'R', 'w' ],
                [ '-', '-', '-', '-', 'w', '-', '-', 'G', 'B', 'w' ],
                [ '-', '-', '-', '-', 'w', '-', 'r', 'R', 'R', 'w' ],
                [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w' ],
                [ 'w', 'p', '-', '-', '-', '-', '-', 'w', 'w', 'w' ],
                [ 'w', 'w', '-', 'g', '-', 'r', '-', 'r', '-', 'w' ],
                [ '-', 'w', '-', 'b', 'r', 'w', '-', 'w', '-', 'w' ],
                [ '-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
                [ '-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w' ] ]
    images = dict()
    return level, images

def testSokobanLoader():
    print('Testing sokoban_loader...')
    files = ['level1-10x10.png',
             'level2-7x9.png',
             'level3-8x6.png',
             'level4-8x6.png']
    
    correctLevels = [
        # level1-10x10.png
        [ [ '-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'R', 'R', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', 'G', 'B', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', 'r', 'R', 'R', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w' ],
          [ 'w', 'p', '-', '-', '-', '-', '-', 'w', 'w', 'w' ],
          [ 'w', 'w', '-', 'g', '-', 'r', '-', 'r', '-', 'w' ],
          [ '-', 'w', '-', 'b', 'r', 'w', '-', 'w', '-', 'w' ],
          [ '-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w' ] ],

        # level2-7x9.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', '-' ],
          [ 'w', 'R', 'G', 'B', 'V', 'w', 'w', 'w', 'w' ],
          [ 'w', 'p', '-', 'r', 'g', 'b', '-', '-', 'w' ],
          [ 'w', 'w', '-', '-', 'v', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', '-', 'w', '-', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'w', 'w' ] ],
        
        # level3-8x6.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w' ],
          [ 'w', '-', '-', 'p', '-', 'w' ],
          [ 'w', '-', 'r', '-', '-', 'w' ],
          [ 'w', 'w', '-', 'w', 'g', 'w' ],
          [ 'w', '-', 'b', 'v', '-', 'w' ],
          [ 'w', '-', '-', 'c', 'B', 'w' ],
          [ 'w', 'C', 'R', 'V', 'G', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w' ] ],
        
        # level4-8x6.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w' ],
          [ 'w', 'B', 'G', 'p', 'R', 'w' ],
          [ 'w', '-', '-', 'r', '-', 'w' ],
          [ 'w', 'w', 'g', 'w', 'w', 'w' ],
          [ 'w', '-', '-', 'b', '-', 'w' ],
          [ 'w', '-', '-', '-', '-', 'w' ],
          [ 'w', '-', '-', '-', '-', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w' ] ]

    ]

    for i in range(len(files)):
        file = files[i]
        correctLevel = correctLevels[i]
        level, images = loadLevel(file)
        print(images)
        if level != correctLevel:
            print(f'{file} is incorrect!')
            print('Correct result:')
            print(correctLevel)
            print('Your result:')
            print(level)
            assert(False)
        print(f'  {file} is correct')
    print('Passed!')

if __name__ == '__main__':
    testSokobanLoader()