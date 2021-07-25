#Carlos Gonzalez
#cggonzal
#Section C


from tkinter import *
import random
import copy

def init(data):

    #Seven "standard" pieces (tetrominoes)
    iPiece = [
        [ True,  True,  True,  True]
      ]

    jPiece = [
        [ True, False, False ],
        [ True, True,  True]
      ]

    lPiece = [
        [ False, False, True],
        [ True,  True,  True]
      ]

    oPiece = [
        [ True, True],
        [ True, True]
      ]

    sPiece = [
        [ False, True, True],
        [ True,  True, False ]
      ]

    tPiece = [
        [ False, True, False ],
        [ True,  True, True]
      ]

    zPiece = [
        [ True,  True, False ],
        [ False, True, True]
      ]
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    data.tetrisPieces = tetrisPieces
    data.tetrisPieceColors = tetrisPieceColors

    data.gameOver = False
    data.score = 0
    # set board dimensions and margin
    data.rows = 15
    data.cols = 10
    data.margin = 20

    data.fallingPiece = newFallingPiece(data)

    # make board
    data.emptyColor = "blue"
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]


def newFallingPiece(data):
    index = random.randint(0,6)
    data.fallingPiece = data.tetrisPieces[index]
    data.fallingPieceColor = data.tetrisPieceColors[index]
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2 - 1
    return data.fallingPiece


# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if event.keysym == "Left":
        moveFallingPiece(data,0,-1)
    elif event.keysym == "Right":
        moveFallingPiece(data,0,1)
    elif event.keysym == "Up":
        rotateFallingPiece(data)
    elif event.keysym == "Down":
        moveFallingPiece(data,1,0)
    elif event.char == "r":
        init(data)


def timerFired(data):
    removeFullRows(data)
    if data.gameOver:
        return
    if moveFallingPiece(data,1,0):
        pass
    else:
        placeFallingPiece(data)
        newFallingPiece(data)
        if fallingPieceIsLegal(data) == False:
            data.gameOver = True

def drawGame(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas,data)
    canvas.create_text(data.width/2,31*data.height/32,text = "Press \"r\" to restart:")
    if data.gameOver:
        canvas.create_text(data.width/2,data.height/2,font = ("Helvetica",32),text = "GAME OVER!",fill = "red")

def drawBoard(canvas, data):
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] != "blue":
                drawCell(canvas, data, row, col,data.board[row][col])
            else:
                drawCell(canvas, data, row, col,data.board[row][col])


def removeFullRows(data):
    newRow = len(data.board) - 1
    topRow = 0
    for oldRow in range(len(data.board)-1,-1,-1):
        full = True
        for oldCol in range(len(data.board[oldRow])):
            if data.board[oldRow][oldCol] == "blue":
                full = False

        if full == False:
            data.board[newRow] = copy.deepcopy(data.board[oldRow])
            newRow -= 1

        elif full == True:
             data.score += 1



def drawFallingPiece(canvas, data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col] == True:
                drawCell(canvas,data,row+data.fallingPieceRow,col+data.fallingPieceCol,data.fallingPieceColor)

def placeFallingPiece(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.board[row+data.fallingPieceRow][col+data.fallingPieceCol] == data.emptyColor and data.fallingPiece[row][col] == True:
                data.board[row + data.fallingPieceRow][col+data.fallingPieceCol] = data.fallingPieceColor


    return

def moveFallingPiece(data,drow,dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if fallingPieceIsLegal(data) == False:
        data.fallingPieceCol -= dcol
        data.fallingPieceRow -= drow
        return False

    return True

def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPieceRow + len(data.fallingPiece) > data.rows or data.fallingPieceRow < 0 or\
            data.fallingPieceCol + len(data.fallingPiece[row]) > data.cols \
             or data.fallingPieceCol < 0:
                return False

    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col] == True:
                if data.board[data.fallingPieceRow + row][data.fallingPieceCol + col] != data.emptyColor:
                    return False

    return True




def drawCell(canvas, data, row, col,color):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color)

def redrawAll(canvas, data):
    drawGame(canvas, data)

def rotateFallingPiece(data):
    oldCols = len(data.fallingPiece[0])
    oldRows = len(data.fallingPiece)
    newRows = oldCols
    newCols = oldRows

    pieceRow = data.fallingPieceRow
    pieceCol = data.fallingPieceCol
    oldPiece = copy.deepcopy(data.fallingPiece)

    newPieceRow = oldCols - 1 - pieceCol

    centerRow = data.fallingPieceRow +len(data.fallingPiece)//2
    newCenter = newPieceRow + newRows//2

    newPiece =[[None]*newCols for row in range(newRows)]

    for row in range(oldRows):
        for col in range(oldCols):
            if row == centerRow and col == newCols//2:
                newPiece[centerRow][newCols//2] = newCenter
            else:
                newPiece[oldCols-1-col][row] = (oldPiece[row][col])


    data.fallingPiece = newPiece

    if fallingPieceIsLegal(data) == False:
        data.fallingPiece = oldPiece

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(300, 300)

####################################
# playTetris() [calls run()]
####################################

def playTetris():
    rows = 15
    cols = 10
    margin = 20 # margin around grid
    cellSize = 20 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    run(width, height)

playTetris()
