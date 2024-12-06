# sokoban_player.py
#   main sokoban game.
# Leslie Liu / leslieli / Section Q

from cmu_graphics import *
from sokoban_loader import *
import os, pathlib, random, time

''' thanks to Juhani Junkala (SubspaceAudio on OpenGameArt.org) 
for the public domain 8-bit game sounds:
https://opengameart.org/content/512-sound-effects-8-bit-style '''

# for grading: just before winning step of level 1
LEVEL1_ALMOST_MOVES =  [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (0, 1), (1, 0), (0, 1), (-1, 0), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (1, 0), (0, 1), (0, 1), (1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, -1), (1, 0), (0, 1), (0, 1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, 1), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (0, 1), (0, 1), (1, 0), (0, 1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (0, 1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, 1), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (0, 1), (1, 0), (0, 1), (-1, 0), (-1, 0), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, -1), (1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (-1, 0)]

# colors for graphics when using hardcoded levels
COLORS_MAPPED = {
    'r': 'firebrick',
    'g': 'forestgreen',
    'b': 'royalblue',
    'v': 'mediumpurple',
    'c': 'mediumturquoise',
    'w': 'burlywood',
    'p': 'black',
    '-': None,
    'dr': 'darkred',
    'dg': 'darkgreen',
    'db': 'navy',
    'dv': 'purple',
    'dc': 'teal'
} 

SFX_URL = {
    'cantMove' : {'sfx/cantMove1.wav','sfx/cantMove2.wav'},
    'moveIntoEmptyCell' : {'sfx/move1.wav', 'sfx/move2.wav'},
    'moveBox' : {'sfx/moveBox1.wav', 'sfx/moveBox2.wav'},
    'overTarget' : {'sfx/overTarget1.wav', 'sfx/overTarget2.wav'},
    'playerWins' : {'sfx/pWins.wav'}
}

################################################
###               GAME SETUP
################################################
def onAppStart(app,useHardcodedLevel=False):

    # canvas
    app.paused = True
    app.isMutedCounter = 0
    app.isMuted = False
    app.isHardcodedLevel = useHardcodedLevel
    app.width, app.height = 600,600
    app.pdg = app.width * 0.02 # padding
    app.gameInfoHeight = app.height * 0.13
    app.availGameWidth, app.availGameHeight = app.width - (2 * app.pdg), app.height - (app.pdg * 2) - app.gameInfoHeight
    app.isDrawingControlsInfo = False

    # game
    loadLevelMode = None if useHardcodedLevel else getLevel(app) # 0 should be path.
    app.level, app.images = loadLevel(loadLevelMode) # initial board, images to draw
    app.pMoves = []
    app.undoneMove = (None, None)
    app.undoneMoves = []
    app.undoMove = False
    app.redoMove = False
    resetLevel(app,'full')
    app.sisyphus = False
    app.unpushBox = False

    # sound effects
    loadSoundEffects(app)

def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

def loadSoundEffects(app):
    app.sfx = dict()
    for sfxCategory in SFX_URL:
        app.sfx[sfxCategory] = []
        for oneSfx in SFX_URL[sfxCategory]:
            app.sfx[sfxCategory].append(loadSound(oneSfx))

def getLevel(app,levelNum=1):
    if 1 <= levelNum <= 4:
        files = ['level1-10x10.png','level2-7x9.png','level3-8x6.png','level4-8x6.png']
        app.level, app.images = loadLevel(files[levelNum-1]) # initial board, images to draw
        resetLevel(app,mode='full')
        app.pMoves = []
        app.levelNum = levelNum
    return files[levelNum-1]

def resetLevel(app,mode='full'):
    if mode == 'full': app.counter = 0
    app.gameOver = False
    app.isMuted = app.isMutedCounter % 2 == 1

    app.numRows, app.numCols = len(app.level), len(app.level[0])
    app.gameBoard, app.gameTargets, app.pRow, app.pCol = setupLevel(app)
    app.origPRow, app.origPCol = app.pRow, app.pCol

    # canvas: drawing the board (game)
    app.bTopLeftX, app.bTopLeftY = app.pdg, app.gameInfoHeight + (app.pdg)
    app.cellSize = app.availGameHeight // max(app.numRows,app.numCols)
    app.bWidth, app.bHeight = app.cellSize * app.numCols, app.cellSize * app.numRows
    app.bTopLeftX = (app.width // 2) - (app.bWidth // 2)

    # player
    app.pSize = app.cellSize * 0.5
    app.pWon = False
    app.pWonTime = ''


def setupLevel(app):
    gameBoard, gameTargets = [(['-'] * app.numCols) for row in range(app.numRows)], [(['-'] * app.numCols) for row in range(app.numRows)]
    pRow, pCol = None, None

    # separate out level info
    for row in range(app.numRows):
        for col in range(app.numCols):
            currCell = app.level[row][col]
            if currCell != '-':
                if currCell.isupper(): # target
                    gameTargets[row][col] = currCell.lower()
                else: # walls, boxes, or player
                    if currCell == 'p':
                        pRow, pCol = row, col
                        currCell = '-'
                    gameBoard[row][col] = currCell

    return gameBoard, gameTargets, pRow, pCol



################################################
###             GAME CONTROLS
################################################

def onStep(app):
    if not app.gameOver and not app.paused: app.counter += 1

def onKeyPress(app,key):
    if not app.gameOver: # player can still move around when game is not over
        if key == 'v': app.isHardcodedLevel = not app.isHardcodedLevel
        # if key == 's': app.sisyphus = not app.sisyphus
        if key == 'u' and len(app.pMoves) > 0: undoMove(app)
        if key == 'y' and app.undoneMoves != []: redoMove(app) # SOMETHING
        if key == 'a' and app.levelNum == 1: # hardcoded jump to almost solution for grading
            makeAlmostMoves(app) # this only works on the first try
        else:
            if key in 'up down left right'.split():
                dRow,dCol = 0,0
                if key == 'up': dRow -= 1
                if key == 'down': dRow += 1 # elif?
                if key == 'left': dCol -= 1
                if key == 'right': dCol += 1

                if canMove(app,dRow,dCol) and (dRow,dCol) != (0,0):
                    makeMove(app,dRow,dCol)
                    # if app.sisyphus and pushedBox(app,dRow,dCol):
                    #     print('should return')
                    #     app.pRow, app.pCol = app.origPRow, app.origPCol
                    app.pMoves.append((dRow,dCol)) # update player moves
                
                else:
                    playSfx(app,'cantMove')
            # if app.sisyphus: app.pMoves = []
    
    # these game controls are accessible regardless of game over state
    if key == 'space': app.paused = not app.paused
    if key == 'r': resetLevel(app,mode='full')
    if key == 'm': 
        app.isMutedCounter += 1
        app.isMuted = app.isMutedCounter % 2 == 1

    if key == 'c': app.isDrawingControlsInfo = not app.isDrawingControlsInfo
    if key in '1234':
        getLevel(app,int(key))
    
    # check for a potential win every time player presses a key
    if not app.gameOver and checkForWin(app):
        app.gameOver = True
        app.pWon = True
        app.pWonTime = getTimerInfo(app)
        time.sleep(0.2) # slight delay applied
        playSfx(app,'playerWins')

def pushedBox(app,dRow,dCol):
    tentativeRow, tentativeCol = app.pRow + dRow, app.pCol + dCol
    tentativeNextRow, tentativeNextCol = tentativeRow + dRow, tentativeCol + dCol
    return isBox(app, tentativeRow, tentativeCol) and isBox(app, tentativeNextRow, tentativeNextCol)

def onKeyRelease(app,key):
    if key == 'r': app.pMoves = [] # clearing moves here to allow for access to moves if undoing
    if key == 'u': app.undoMove = False # setting to false to accommodate sound effects.
    if key == 'y': app.redoMove = False

def canMove(app,dRow,dCol):
    tentativeRow, tentativeCol = app.pRow + dRow, app.pCol + dCol
    tentativeNextRow, tentativeNextCol = tentativeRow + dRow, tentativeCol + dCol
    if isWall(app, tentativeRow, tentativeCol): return False # moving into wall
    if (isBox(app, tentativeRow, tentativeCol) and 
       (isBox(app, tentativeNextRow, tentativeNextCol) or isWall(app, tentativeNextRow, tentativeNextCol))
       ): return False # pushing 2 boxes, or pushing box into wall
    return True

def isWall(app,row,col): return app.gameBoard[row][col] == 'w'
def isEmpty(app,row,col): return app.gameBoard[row][col] == '-'
def isBox(app,row,col): return app.gameBoard[row][col] in 'rgbvc'

def makeMove(app,dRow,dCol):
    app.pRow += dRow
    app.pCol += dCol
    # move boxes, if any are there and are movable
    if app.gameBoard[app.pRow][app.pCol] in 'rgbvc': # there was a box where player now is
        app.gameBoard[app.pRow+dRow][app.pCol+dCol] = app.gameBoard[app.pRow][app.pCol]
        app.gameBoard[app.pRow][app.pCol] = '-'   
        if app.gameTargets[app.pRow+dRow][app.pCol+dCol] == app.gameBoard[app.pRow+dRow][app.pCol+dCol]: 
            playSfx(app,'overTarget') # box on top of corresponding target
        else: playSfx(app,'moveBox')
    else: playSfx(app,'moveIntoEmptyCell')

def makeAlmostMoves(app): # for grading
    resetLevel(app,'notFull')
    app.pWon = False
    app.pMoves = LEVEL1_ALMOST_MOVES
    redrawMoves(app)

def undoMove(app):
    app.undoMove = True
    app.undoneMoves.append(app.pMoves.pop())
    resetLevel(app,'notFull')
    redrawMoves(app)

def redoMove(app): # this is buggy — something to do with the list setup, I think.
    app.redoMove = True
    if canMove(app,*app.undoneMoves[0]): 
        makeMove(app,*app.undoneMoves[0])
        app.pMoves.append(app.undoneMoves.pop(0))
    
def redrawMoves(app):
    for move in app.pMoves:
        makeMove(app,*move)

def checkForWin(app):
    # iterate over targets and board. check if each target location is same as on board
    for row in range(app.numRows):
        for col in range(app.numCols):
            if app.gameTargets[row][col] != '-':
                if app.gameTargets[row][col] != app.gameBoard[row][col]:
                    return False
    return True

################################################
###              SOUND EFFECTS
################################################
def playSfx(app,occasion):
    if (not app.isMuted) and (not (app.undoMove or app.redoMove)): # checking if redoing/undoing moves to minimize abrasive sfx.
        random.choice(app.sfx[occasion]).play(restart=True)

################################################
###                 DRAWING
################################################

def redrawAll(app):
    if not app.paused:
        drawGameInfo(app) # draw header/game info text
        drawGame(app) # draw game: board, pieces
        if app.isDrawingControlsInfo: drawControlsInfo(app)
        if app.pWon: drawPlayerWin(app)
    else:
        drawHomescreen(app)

def drawGame(app):
    drawRect(app.pdg, app.gameInfoHeight, app.availGameWidth, app.availGameHeight, fill='white')
    category, key, onTarget = '', '', False

    for row in range(app.numRows):
        for col in range(app.numCols):
            if app.gameTargets[row][col] != '-' and app.gameBoard[row][col] == '-':
                    category = 'target'
                    key = app.gameTargets[row][col]
            elif app.gameBoard[row][col] != '-':
                key = app.gameBoard[row][col]
                category = 'board'
            else: category = 'nothing'
            drawCell(app,app.bTopLeftX + (col * app.cellSize), app.bTopLeftY + (row * app.cellSize), app.cellSize, category, key) # draw everything else
            if app.gameBoard[row][col] == app.gameTargets[row][col] and app.gameBoard[row][col] != '-':
                drawCell(app,app.bTopLeftX + (col * app.cellSize), app.bTopLeftY + (row * app.cellSize), app.cellSize, category='overTarget', key='NA')
    drawCell(app,app.bTopLeftX + (app.pCol * app.cellSize), app.bTopLeftY + (app.pRow * app.cellSize), app.cellSize, category='player', key='p') # draw player

def drawCell(app,topLeftX, topLeftY, size, category, key):
    if category == 'overTarget':
        drawRect(topLeftX,topLeftY,size,size,fill='black',opacity=60)
    elif category == 'board':
        if app.isHardcodedLevel: drawRect(topLeftX, topLeftY, size, size, fill=COLORS_MAPPED[key])
    elif category == 'player':
        if app.isHardcodedLevel: drawCircle(topLeftX + (size//2), topLeftY + (size//2), app.pSize * 0.75, fill=COLORS_MAPPED[key], align='center')
    elif category == 'target':
        tgtSize = size * 0.5
        if app.isHardcodedLevel: drawCircle(topLeftX + (size//2), topLeftY + (size//2), tgtSize * 0.5, fill=None, border=COLORS_MAPPED[f'd{key}'], borderWidth=8, align='center')   
    if not app.isHardcodedLevel:
        if category == 'nothing':
            drawRect(topLeftX,topLeftY,size,size,fill='white')
        elif category != 'overTarget': 
            if category == 'target': key = key.upper()
            drawImage(app.images[key],topLeftX, topLeftY,width=size,height=size)            

def drawGameInfo(app):
    drawRect(0,0,app.width,app.height,fill='white') # background
    header = f'Sokoban! [Level {app.levelNum}]'
    steps = f'[{len(app.pMoves)} steps]'
    timer = getTimerInfo(app)
    instruc = '''\
        Use arrow keys to solve the puzzle.
        Press [u] to undo moves, [y] to redo moves, and [r] to reset level. 
        Press [1],[2],[3],[4] to play different levels, and [c] to toggle controls on/off.
        '''
    baseline = app.pdg * 1.2
    drawLabel(header, app.width//2, baseline, size=18, align='center')
    if not app.pWon: 
        drawLabel(steps, app.pdg, baseline, size=18, align='left')
        drawLabel(timer, app.width - app.pdg, baseline, size=18, align='right')
    baseline += app.pdg * 1.5
    for line in instruc.splitlines():
        drawLabel(line, app.width//2, baseline, size=15, align='center')
        baseline += app.pdg * 1.33
    drawLine(app.pdg, app.gameInfoHeight, app.pdg + app.availGameWidth, app.gameInfoHeight)

def getTimerInfo(app):
    secondsPassed = app.counter // app.stepsPerSecond
    minuteNum = secondsPassed // 60
    secondNum = secondsPassed - (minuteNum * 60)
    minFiller = '0' if minuteNum < 10 else ''
    secFiller = '0' if secondNum < 10 else ''
    return f'[{minFiller}{minuteNum}:{secFiller}{secondNum}]'

def drawHomescreen(app):
    baseline = app.gameInfoHeight + (app.bHeight * 0.33)
    intro = f'''\
    Sokoban!
    Press [space] to play.
    '''
    drawBigText(app,intro,mode='home')

def drawPlayerWin(app):
    drawRect(0,0,app.width,app.height,fill='black',opacity=85)
    celebration = f'''\
    Hooray! You solved LEVEL {app.levelNum}.
    YOUR STEPS: {len(app.pMoves)} 
    YOUR TIME: {app.pWonTime[1:-1]}

    Press [r] to replay the level, 
    or [1], [2], [3], or [4] to select a level.
    '''
    drawBigText(app,celebration,mode='win')

def drawBigText(app,message,mode=''):
    textCol = 'white' if mode == 'win' else 'black'
    textSize = 18 if mode == 'win' else 24
    baseline = app.gameInfoHeight + (app.bHeight * 0.33)
    for line in message.splitlines():
        drawLabel(line, app.width//2, baseline, size=textSize, align='center', fill=textCol)
        baseline += app.pdg * 2.5

def drawControlsInfo(app):
    refUnit = 50
    audioButtonW = refUnit * 2
    buttonH = refUnit // 2 
    buttonX = app.pdg
    buttonY = app.bTopLeftY + app.pdg  if app.levelNum != 2 else app.availGameHeight * 0.8
    soundOn = 'OFF' if app.isMuted else 'ON'
    soundInfo = f'[m] SOUND {soundOn}'
    drawButton(buttonX,buttonY,audioButtonW,buttonH,soundInfo)
    buttonY += buttonH * 1.2
    viewButtonW = refUnit * 3
    viewMode = 'SHAPES' if app.isHardcodedLevel else 'DUDE'
    viewInfo = f'[v] GRAPHICS: {viewMode}'
    drawButton(buttonX,buttonY,viewButtonW,buttonH,viewInfo)
    # toil = 'NEVERENDING' if app.sisyphus else 'STANDARD'
    # buttonY += buttonH * 1.2
    # toilButtonW = audioButtonW
    # drawButton(buttonX,buttonY,toilButtonW,buttonH,toil)
    ''' scrapping the sisyphean mod for now... '''

def drawButton(x,y,w,h,buttonLabel):
    pdg = w * 0.05
    drawRect(x,y,w,h,fill='whitesmoke',border='black',borderWidth=1)
    drawLabel(buttonLabel,x+pdg,y+pdg,align='left-top')

def main(app,useHardcodedLevel=False):
    runApp(useHardcodedLevel)

main(app)