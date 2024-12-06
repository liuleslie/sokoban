# sokoban_player.py
#   main sokoban game.
# Leslie Liu / leslieli / Section Q

'''
THE LATEST:
around line 210, need to fix image display issue. something with the if statements in drawCell.

'''

from cmu_graphics import *
from sokoban_loader import *

'''
resetLevel: doesnt reload entire app --> no need to re-read pickle file
redoMove: use reset() to re-draw moves
where does useHardcodedLevel go?
'''

# for grading: just before winning step of level 1
LEVEL1_ALMOST_MOVES =  [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (0, 1), (1, 0), (0, 1), (-1, 0), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (1, 0), (0, 1), (0, 1), (1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, -1), (1, 0), (0, 1), (0, 1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, 1), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (0, 1), (0, 1), (1, 0), (0, 1), (-1, 0), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (0, 1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (0, 1), (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, 1), (0, 1), (1, 0), (0, 1), (-1, 0), (-1, 0), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, -1), (1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (-1, 0)]

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

################################################
###               GAME SETUP
################################################
def onAppStart(app,useHardcodedLevel=False):
    # canvas
    app.isHardcodedLevel = useHardcodedLevel
    app.width, app.height = 600,600
    app.pdg = app.width * 0.02 # padding
    app.gameInfoHeight = app.height * 0.13
    app.availGameWidth, app.availGameHeight = app.width - (2 * app.pdg), app.height - (app.pdg * 2) - app.gameInfoHeight

    # game
    loadLevelMode = None if useHardcodedLevel else getLevel(app) # 0 should be path.
    app.level, app.images = loadLevel(loadLevelMode) # initial board, images to draw
    app.pMoves = []
    app.undoneMove = (None, None)
    app.undoMove = False
    app.redoMove = False
    resetLevel(app)

def getLevel(app,levelNum=1):
    if 1 <= levelNum <= 4:
        files = ['level1-10x10.png','level2-7x9.png','level3-8x6.png','level4-8x6.png']
        app.level, app.images = loadLevel(files[levelNum-1]) # initial board, images to draw
        resetLevel(app)
        app.pMoves = []
        app.levelNum = levelNum
    return files[levelNum-1]

def resetLevel(app):
    app.counter = 0
    app.gameOver = False

    app.levelNum = 1
    app.numRows, app.numCols = len(app.level), len(app.level[0])
    app.gameBoard, app.gameTargets, app.pRow, app.pCol = setupLevel(app)

    # canvas, meso structure: drawing the board (game)
    app.bTopLeftX, app.bTopLeftY = app.pdg, app.gameInfoHeight + (app.pdg)
    app.cellSize = app.availGameHeight // max(app.numRows,app.numCols)
    app.bWidth, app.bHeight = app.cellSize * app.numCols, app.cellSize * app.numRows
    app.bTopLeftX = (app.width // 2) - (app.bWidth // 2)

    # player
    app.pSize = app.cellSize * 0.5
    app.pWon = False


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
    app.counter += 1

def onKeyPress(app,key):
    if not app.gameOver:
        if key == 'h': app.isHardcodedLevel = not app.isHardcodedLevel
        if key == 'u' and len(app.pMoves) > 0: undoMove(app)
        if key == 'i' and app.undoneMove != (None, None): pass # SOMETHING
        if key == 'a' and app.levelNum == 1: # hardcoded jump to almost solution for grading
            resetLevel(app)
            app.pMoves = LEVEL1_ALMOST_MOVES
            for move in app.pMoves:
                makeMove(app,*move)
        
        else:
            if key in 'up down left right'.split():
                dRow,dCol = 0,0
                if key == 'up': dRow -= 1
                if key == 'down': dRow += 1 # elif?
                if key == 'left': dCol -= 1
                if key == 'right': dCol += 1
                if canMove(app,dRow,dCol) and (dRow,dCol) != (0,0):
                    makeMove(app,dRow,dCol)
                    app.pMoves.append((dRow,dCol)) # update player moves
    
    if key == 'r': resetLevel(app)
    if key in '1234':
        getLevel(app,int(key))
        print(f'curr level is {app.levelNum}')
    
    if checkForWin(app):
        app.gameOver = True
        app.pWon = True

def onKeyRelease(app,key):
    if key == 'r': app.pMoves = [] # is this hacky?

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
    # move boxes, if any are there. should only work if boxes are movable; boxes shouldnt go out of bounds
    if app.gameBoard[app.pRow][app.pCol] in 'rgbvc': # there was a box where player now is
        app.gameBoard[app.pRow+dRow][app.pCol+dCol] = app.gameBoard[app.pRow][app.pCol]
        app.gameBoard[app.pRow][app.pCol] = '-'        

def undoMove(app):
    app.undoneMove = app.pMoves.pop()
    resetLevel(app)
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
###                 DRAWING
################################################

def redrawAll(app):
    # if not app.gameOver:
    drawGameInfo(app) # draw header/game info text
    drawGame(app) # draw game: board, pieces
    if app.pWon: 
        drawRect(0,0,app.width,app.height,fill='black',opacity=75)
        drawLabel('player won! restart or something',app.width//2,app.height//2,fill='white')

def drawGame(app):
    drawRect(app.pdg, app.gameInfoHeight, app.availGameWidth, app.availGameHeight, fill='whitesmoke')

    category, key = '', ''
    for row in range(app.numRows):
        for col in range(app.numCols):
            if app.gameTargets[row][col] != '-' and app.gameBoard[row][col] == '-':
                    category = 'target'
                    key = app.gameTargets[row][col]
            elif app.gameBoard[row][col] != '-':
                key = app.gameBoard[row][col]
                # if app.gameBoard[row][col] == 'w':
                #     category = 'wall'
                # else:
                category = 'board'
            else:
                category = 'nothing'
            

            drawCell(app,app.bTopLeftX + (col * app.cellSize), app.bTopLeftY + (row * app.cellSize), app.cellSize, category, key)
    drawCell(app,app.bTopLeftX + (app.pCol * app.cellSize), app.bTopLeftY + (app.pRow * app.cellSize), app.cellSize, category='player', key='p')

def drawCell(app,topLeftX, topLeftY, size, category, key):
    if category == 'board':
        if app.isHardcodedLevel: drawRect(topLeftX, topLeftY, size, size, fill=COLORS_MAPPED[key])
    elif category == 'player':
        if app.isHardcodedLevel: drawCircle(topLeftX + (size//2), topLeftY + (size//2), app.pSize * 0.75, fill=COLORS_MAPPED[key], align='center')
    elif category == 'target':
        tgtSz = size * 0.5
        if app.isHardcodedLevel: drawCircle(topLeftX + (size//2), topLeftY + (size//2), tgtSz * 0.5, fill=None, border=COLORS_MAPPED[f'd{key}'], borderWidth=8, align='center')   
    if not app.isHardcodedLevel:
        if category == 'nothing':
            drawRect(topLeftX,topLeftY,size,size,fill='white')
        else: # if key != '' and key != '-':
            if category == 'target': key = key.upper()
            drawImage(app.images[key],topLeftX, topLeftY,width=size,height=size)

def drawGameInfo(app):
    drawRect(0,0,app.width,app.height,fill='white') # background
    header = f'Sokoban! [Level {app.levelNum}]'
    steps = f'[{len(app.pMoves)} steps]'
    timer = getTimerInfo(app)
    instruc = '''\
        Use arrow keys to solve the puzzle.
        Press u to undo moves, r to reset level.
        Press 1,2,3,4 to play different levels.
        '''
    baseline = app.pdg * 1.2
    drawLabel(header, app.width//2, baseline, size=18, align='center')
    drawLabel(steps, app.pdg, baseline, size=18, align='left')
    drawLabel(timer, app.width - app.pdg, baseline, size=18, align='right')
    baseline += app.pdg * 1.5
    for line in instruc.splitlines():
        drawLabel(line, app.width//2, baseline, size=15, align='center')
        baseline += app.pdg * 1.33
    drawLine(app.pdg, app.gameInfoHeight, app.pdg + app.availGameWidth, app.gameInfoHeight)

def getTimerInfo(app):
    sec = app.counter // app.stepsPerSecond
    if sec == 60: sec = 0
    secFiller = '0' if sec < 10 else ''
    minFiller = '0' if sec // 60 < 10 else ''
    res = f'[{minFiller}{sec//60}:{secFiller}{(app.counter//app.stepsPerSecond)%60}]'
    return res

def main(app,useHardcodedLevel=False):
    runApp(useHardcodedLevel)

main(app)
