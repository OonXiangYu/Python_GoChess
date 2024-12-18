from PyQt6.QtWidgets import QFrame, QApplication, QMessageBox, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QRectF, pyqtSlot
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont

from Python_GoChess.FirstName_LastName_StudentNumber_Project.code.game_logic import GameLogic


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal1 = pyqtSignal(int)  # signal sent when the timer is updated for player 1
    updateTimerSignal2 = pyqtSignal(int) # signal sent when the timer is updated for player 2
    clickLocationSignal = pyqtSignal(QPoint)  # signal sent when there is a new click location
    playerTurnSignal = pyqtSignal(int) # signal sent when player turn changed

    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #
    timerSpeed = 1000  # the timer updates every 1 second
    counter1 = 600  # the number the counter will count down from
    counter2 = 600 # for diff players
    margin = 40
    colMargin = 9
    rowMargin = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.start()

        self.boardArray = [[0 for _ in range(8)] for _ in range(8)]    # TODO - create a 2d int/Piece array to store the state of the game
        self.game = GameLogic(self.boardArray)
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

    def makeConnection(self, score_board):
        score_board.resetSignal.connect(self.resetGame)

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

    def squareSize(self):
        '''Returns the size (width and height) of one square in the game board as a square'''
        available_width = self.contentsRect().width() - 2 * self.margin
        available_height = self.contentsRect().height() - 2 * self.margin

        # Determine the maximum square size that fits within the available space
        square_size = min(available_width / self.boardWidth, available_height / self.boardHeight)
        return square_size

    def start(self):
        '''starts game'''
        #self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if self.game.getGameTurn() % 2 == 0: # if player turn is player2 turn then decrease player1 time is becuz te turn will only increase when the player clicked
            if self.counter1 == 0:
                print("Player 1 Game over")
                self.timer.stop()
            else:
                self.counter1 -= 1
                self.updateTimerSignal1.emit(self.counter1) # for player 1
        else:
            if self.counter2 == 0:
                print("Player 2 Game over")
                self.timer.stop()
            else:
                self.counter2 -= 1
                self.updateTimerSignal2.emit(self.counter2) # for player 2

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        try:
            painter.setBrush(QBrush(QColor(246, 178, 107)))
            painter.drawRect(self.rect())

            self.drawColumnHeaders(painter)
            self.drawRowHeaders(painter)

            self.drawBoardSquares(painter)

            self.drawPieces(painter)
        except Exception as e:
            print(e)

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
        try:
            if self.game.gameTurn() == 1:
                self.start()  # start the game which will start the timer
                if self.boardArray[row][col] == 0 or self.boardArray[row][col] == 4: # 4 is mean the place u place will make you suicide
                    self.boardArray[row][col] = 1 # Black pieces / Player 1
                    self.playerTurnSignal.emit(self.game.getGameTurn())
                else:
                    try:
                        self.game.regretGameTurn()
                        show_error()
                    except Exception as e:
                        print(e)

            else:
                if self.boardArray[row][col] == 0 or self.boardArray[row][col] == 3:
                    self.boardArray[row][col] = 2 # White pieces/ Player 2
                    self.playerTurnSignal.emit(self.game.getGameTurn())
                else:
                    try:
                        self.game.regretGameTurn()
                        show_error()
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)

        self.game.eatPieces()

        self.printBoardArray()
        self.update()

    @pyqtSlot()
    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game
        print("reset")
        self.boardArray = [[0 for _ in range(self.boardWidth + 1)] for _ in range(self.boardHeight + 1)]
        self.counter1 = 600  # Reset counter
        self.counter2 = 600
        self.updateTimerSignal1.emit(self.counter1)  # for player 1
        self.updateTimerSignal2.emit(self.counter2)  # for player 2
        self.game.resetGameTurn()
        print("resetGame() - board and counter reset")
        self.update()  # Redraw the board

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        pass  # Implement this method according to your logic

    def drawColumnHeaders(self, painter):
        '''Draw the column headers A, B, C, D, ... above the game board'''
        try:
            painter.setBrush(QBrush(QColor(0, 0, 0)))  # Use black text for column headers
            font = QFont()
            font.setPointSize(12)  # Adjust size as needed
            painter.setFont(font)

            for col in range(self.boardWidth + 1):
                # Calculate the position for each column header
                rect = QRectF(
                    self.colMargin + col * self.squareWidth() + self.squareWidth() / 2 - 8,
                    self.margin / 2 - 20,
                    20,
                    20
                )
                # Draw the text label (A, B, C, ...)
                painter.drawText(rect, Qt.AlignmentFlag.AlignLeft, chr(65 + col))
        except Exception as e:
            print(e)

    def drawRowHeaders(self, painter):
        '''Draw the row numbers 1, 2, 3, ... along the left side of the game board'''
        try:
            painter.setBrush(QBrush(QColor(0, 0, 0)))  # Use black text for row headers
            font = QFont()
            font.setPointSize(12)  # Adjust size as needed
            painter.setFont(font)

            for row in range(self.boardHeight + 1):
                # Calculate the position for each row number
                rect = QRectF(
                    self.margin / 2 - 18,
                    self.rowMargin + row * self.squareHeight() + self.squareHeight() / 2 - 20,
                    20,
                    20
                )
                # Draw the text label (1, 2, 3, ... )
                painter.drawText(rect, Qt.AlignmentFlag.AlignLeft, str(row + 1))
        except Exception as e:
            print(e)

    def drawBoardSquares(self, painter):
        '''Draw all the squares on the game board with a fixed margin on all four sides'''
        try:
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
                    painter.setBrush(QBrush(QColor(246, 178, 107)))
                    painter.drawRect(rect)
        except Exception as e:
            print(e)

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        cell_width = self.width() / 8
        cell_height = self.height() / 8

        try:
            for row_idx, row in enumerate(self.boardArray): # based on board array i will know which position i need to place a piece
                for col_idx, point in enumerate(row):
                    if 0 < point <= 2:# only 1 and 2 is represent color
                        center_x = int((col_idx + 0.5) * cell_width)
                        center_y = int((row_idx + 0.5) * cell_height)
                        radius = int(min(cell_width, cell_height) / 4)

                        if point == 1:
                            painter.setBrush(QBrush(QColor(0, 0, 0)))  # Black color
                        elif point == 2:
                            painter.setBrush(QBrush(QColor(255, 255, 255)))  # White colour

                        painter.drawEllipse(center_x - radius, center_y - radius, int(radius * 2), int(radius * 2))
        except Exception as e:
            print(e)

def show_error():
    # Create and display an error message box
    error_msg = QMessageBox()
    error_msg.setIcon(QMessageBox.Icon.Critical)
    error_msg.setWindowTitle("Error")
    error_msg.setText("You are not allow to place here")
    error_msg.setInformativeText("Please do another move")
    error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    error_msg.exec()

