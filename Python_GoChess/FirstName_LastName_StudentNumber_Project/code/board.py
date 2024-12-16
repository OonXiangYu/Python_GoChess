from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QRectF
from PyQt6.QtGui import QPainter, QColor, QBrush

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(QPoint)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from
    margin = 40

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.boardArray = [[0 for _ in range(8)] for _ in range(8)]    # TODO - create a 2d int/Piece array to store the state of the game
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def squareWidth(self):
        '''Returns the width of one square in the game board considering the margins'''
        return (self.contentsRect().width() - 2 * self.margin) / self.boardWidth

    def squareHeight(self):
        '''Returns the height of one square in the game board considering the margins'''
        return (self.contentsRect().height() - 2 * self.margin) / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if self.counter == 0:
            print("Game over")
        self.counter -= 1
        #print('timerEvent()', self.counter)
        self.updateTimerSignal.emit(self.counter)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)

        self.drawPieces(painter)

    def mousePosToColRow(self, click_point: QPoint):
        '''convert the mouse click event to a row and column'''
        cell_width = self.width() / 8
        cell_height = self.height() / 8

        col = int(click_point.x() / cell_width)
        row = int(click_point.y() / cell_height)

        return row,col

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = event.position().toPoint()  # get the click position
        #print(f"Mouse click at: {clickLoc}")  # Convert QPoint for debugging
        row, col = self.mousePosToColRow(clickLoc)
        #self.clickLocationSignal.emit(clickLoc)  # Emit signal

        # Save the clicked point and trigger a repaint
        self.boardArray[row][col] = 1
        self.printBoardArray()
        self.update()

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game
        self.boardArray = [[0 for _ in range(Board.boardWidth)] for _ in range(Board.boardHeight)]
        self.counter = 10  # Reset counter
        print("resetGame() - board and counter reset")
        self.update()  # Redraw the board

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        pass  # Implement this method according to your logic

    def drawBoardSquares(self, painter):
        '''Draw all the squares on the game board with a fixed margin on all four sides'''
        print("start paint")

        # Calculate the square size
        square_width = self.squareWidth()
        square_height = self.squareHeight()

        # Loop over rows and columns to draw squares with a fixed margin
        for row in range(self.boardHeight):
            for col in range(self.boardWidth):
                rect = QRectF(
                    self.margin + col * square_width,  # Offset by margin on the x-axis
                    self.margin + row * square_height,  # Offset by margin on the y-axis
                    square_width,
                    square_height
                )
                painter.setBrush(QBrush(QColor(255, 255, 255)))
                painter.drawRect(rect)

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        '''
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(col * self.squareWidth(), row * self.squareHeight())
                # TODO draw some pieces as ellipses
                # TODO choose your color and set the painter brush to the correct color
                painter.setBrush(QBrush(QColor(0, 0, 255)))  # Set the circle's color to blue

                radius = (self.squareWidth() - 2) / 2
                center = QPoint(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
        '''
        cell_width = self.width() / 8
        cell_height = self.height() / 8
        painter.setBrush(QBrush(QColor(255, 0, 0)))  # Red color
        try:
            for row_idx, row in enumerate(self.boardArray): # based on board array i will know which position i need to place a piece
                for col_idx, point in enumerate(row):
                    if point != 0:
                        center_x = int((col_idx + 0.55) * cell_width)
                        center_y = int((row_idx + 0.45) * cell_height)
                        radius = int(min(cell_width, cell_height) / 4)
                        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
        except Exception as e:
            print(e)

