from PyQt6.QtWidgets import QFrame, QApplication, QMessageBox, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QRectF, pyqtSlot, pyqtBoundSignal
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont, QRadialGradient
import copy

from Python_GoChess.FirstName_LastName_StudentNumber_Project.code.game_logic import GameLogic


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal1 = pyqtSignal(int)  # signal sent when the timer is updated for player 1
    updateTimerSignal2 = pyqtSignal(int) # signal sent when the timer is updated for player 2
    clickLocationSignal = pyqtSignal(QPoint)  # signal sent when there is a new click location
    playerTurnSignal = pyqtSignal(int) # signal sent when player turn changed\
    player1TerritorySignal = pyqtSignal(int)  # signal for record territory
    player2TerritorySignal = pyqtSignal(int)  # signal for record territory

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
        self.tempBoard = [[0 for _ in range(8)] for _ in range(8)]
        self.game = GameLogic(self.boardArray)
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

        self.player1Territory = 0
        self.player2Territory = 0

    def makeConnection(self, score_board):
        score_board.resetSignal.connect(self.resetGame)
        score_board.passSignal.connect(self.passGame)
        score_board.redoSignal.connect(self.redoGame)

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

        print("TempBoard:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.tempBoard]))

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
                print("Player 2 Victory")
                self.timer.stop()
                show_Victory("Player 2")
            else:
                self.counter1 -= 1
                self.updateTimerSignal1.emit(self.counter1) # for player 1
        else:
            if self.counter2 == 0:
                print("Player 1 Victory")
                self.timer.stop()
                show_Victory("Player 1")
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
                if self.boardArray[row][col] == 0:
                    tempBlack = self.game.getBlackPiece() # total black piece before place / purpose for suicide

                    # if suicide rule for multiple pieces or single piece suicide rule trigger
                    if self.game.suicideRule(row, col, tempBlack, 1) == False or self.game.checkArr(row, col, 2) == False:
                        self.game.regretGameTurn()
                        show_error()
                    else:
                        self.tempBoard = copy.deepcopy(self.boardArray) # save the current board before modified for redo purpose
                        self.boardArray[row][col] = 1 # Black pieces / Player 1
                        self.playerTurnSignal.emit(self.game.getGameTurn())

                else:
                    try:
                        self.game.regretGameTurn()
                        show_error()
                    except Exception as e:
                        print(e)

            else:
                if self.boardArray[row][col] == 0:
                    tempWhite = self.game.getWhitePiece() # total white piece before place / purpose for suicide

                    #if suicide rule for multiple pieces or single piece suicide rule trigger
                    if self.game.suicideRule(row, col, tempWhite, 2) == False or self.game.checkArr(row, col, 1) == False:
                        self.game.regretGameTurn()
                        show_error()
                    else:
                        self.tempBoard = copy.deepcopy(self.boardArray)  # save the current board before modified for redo purpose
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

        tempWhite = self.game.getWhitePiece()  # total white piece before place / purpose for effect
        tempBlack = self.game.getBlackPiece()  # total black piece before place / purpose for effect
        num1 = 0
        num2 = 0

        self.game.eatPieces()
        self.determineWinner()

        for x in range(8):
            for y in range(8):
                if self.boardArray[x][y] == 1:
                    num1 += 1
                elif self.boardArray[x][y] == 2:
                    num2 += 1

        if num1 < tempBlack or num2 < tempWhite:
            self.highlightEffect = True

        self.latestPiece = (row, col)
        self.printBoardArray()
        self.update()

    @pyqtSlot()
    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game
        print("reset")
        self.player1Territory = 0
        self.player2Territory = 0
        self.player1TerritorySignal.emit(self.player1Territory)
        self.player2TerritorySignal.emit(self.player2Territory)
        self.boardArray = [[0 for _ in range(8)] for _ in range(8)]
        self.tempBoard = [[0 for _ in range(8)] for _ in range(8)]
        self.counter1 = 600  # Reset counter
        self.counter2 = 600
        self.updateTimerSignal1.emit(self.counter1)  # for player 1
        self.updateTimerSignal2.emit(self.counter2)  # for player 2
        self.game.resetGameTurn()
        self.game = GameLogic(self.boardArray)
        print("resetGame() - board and counter reset")
        self.update()  # Redraw the board

    @pyqtSlot()
    def passGame(self):
        self.game.passGameTurn()
        self.tempBoard = copy.deepcopy(self.boardArray)
        self.playerTurnSignal.emit(self.game.getGameTurn())

    @pyqtSlot()
    def redoGame(self):
        if self.game.getGameTurn() != 0:
            self.game.regretGameTurn()
            self.boardArray = copy.deepcopy(self.tempBoard)
            self.game = GameLogic(self.boardArray)
            self.playerTurnSignal.emit(self.game.getGameTurn())
            self.update()
        else:
            show_error_redo()

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
        """Draw all the squares on the game board with a fixed margin on all four sides."""
        try:
            # Ensure 'highlightEffect' is properly initialized
            if not hasattr(self, "highlightEffect"):
                self.highlightEffect = False

            # Calculate the square size
            square_width = self.squareWidth()
            square_height = self.squareHeight()

            # Determine square color based on the highlightEffect variable
            square_color = QColor(242, 86, 65) if self.highlightEffect else QColor(246, 178, 107)

            # Loop over rows and columns to draw squares with a fixed margin
            for row in range(self.boardHeight):
                for col in range(self.boardWidth):
                    rect = QRectF(
                        self.margin + col * square_width,  # Offset by margin on the x-axis
                        self.margin + row * square_height,  # Offset by margin on the y-axis
                        square_width,
                        square_height
                    )
                    painter.setBrush(QBrush(square_color))
                    painter.drawRect(rect)

            # If highlightEffect is active, reset it after 2 seconds
            if self.highlightEffect:
                QTimer.singleShot(1000, lambda: self.resetHighlightEffect())

        except Exception as e:
            print(e)

    def resetHighlightEffect(self):
        """Reset the highlight effect after 2 seconds."""
        self.highlightEffect = False
        self.update()  # Trigger a repaint to remove the effect

    def drawPieces(self, painter):
        """Draw the pieces on the board."""
        cell_width = self.width() / 8
        cell_height = self.height() / 8

        if not hasattr(self, "latestPiece"):
            self.latestPiece = None
        if not hasattr(self, "isFlashing"):
            self.isFlashing = False

        try:
            for row_idx, row in enumerate(self.boardArray):  # Based on board array, determine piece positions
                for col_idx, point in enumerate(row):
                    if 0 < point <= 2:  # Only 1 and 2 represent colors
                        center_x = int((col_idx + 0.5) * cell_width)
                        center_y = int((row_idx + 0.5) * cell_height)
                        radius = int(min(cell_width, cell_height) / 4)

                        # Check if this is the latest piece (flashing effect)
                        if (row_idx, col_idx) == getattr(self, "latestPiece", (-1, -1)):
                            if getattr(self, "isFlashing", False):  # Flash is active
                                painter.setBrush(QBrush(QColor(255, 0, 0)))  # Red for flash
                            else:
                                # After the flash ends, draw the piece with its normal color
                                painter.setBrush(QBrush(QColor(0, 0, 0) if point == 1 else QColor(255, 255, 255)))
                        else:
                            # Normal piece colors
                            if point == 1:
                                painter.setBrush(QBrush(QColor(0, 0, 0)))  # Black color
                            elif point == 2:
                                painter.setBrush(QBrush(QColor(255, 255, 255)))  # White color

                        # Draw the piece
                        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

            # Reset the flash effect after drawing the latest piece
            if hasattr(self, "latestPiece") and not getattr(self, "isFlashing", False):
                self.isFlashing = True
                QTimer.singleShot(500, lambda: self.stopFlashEffect())

        except Exception as e:
            print(e)

    def stopFlashEffect(self):
        """Stop the flashing effect."""
        self.isFlashing = False
        self.latestPiece = None
        self.update()  # Trigger a repaint to remove the flash

    def determineWinner(self): # calculate by sum the pieces and the territory suround by the pieces
        self.player1Territory = 0
        self.player2Territory = 0

        group = self.checkMultipleArrWinning([row[:] for row in self.boardArray])

        for grp in group: # calculate territory
            if self.eatMultiplePiecesWinning(grp, 1):
                self.player1Territory += len(grp)

            if self.eatMultiplePiecesWinning(grp, 2):
                self.player2Territory += len(grp)

        self.player1Territory += self.game.getBlackPiece()
        self.player2Territory += self.game.getWhitePiece()

        self.player1TerritorySignal.emit(self.player1Territory)
        self.player2TerritorySignal.emit(self.player2Territory)

        if self.player1Territory > 32: # if anyone of them have above half territory means they win
            show_Victory("Player 1")
        elif self.player2Territory > 32:
            show_Victory("Player 2")

    def checkMultipleArrWinning(self, boardArray):
        def dfs(x, y, group):
            if x < 0 or y < 0 or x >= len(boardArray) or y >= len(boardArray[0]) or boardArray[x][y] != 0:
                return
            boardArray[x][y] = -1  # Mark as visited
            group.append([x, y])

            # Explore all 4 directions
            dfs(x + 1, y, group)
            dfs(x - 1, y, group)
            dfs(x, y + 1, group)
            dfs(x, y - 1, group)

        groups = []  # a big arr to store all the group
        for x in range(len(boardArray)):
            for y in range(len(boardArray[0])):
                if boardArray[x][y] == 0:  # Start DFS at the first index found
                    group = []
                    dfs(x, y, group)
                    groups.append(group)

        return groups

    def eatMultiplePiecesWinning(self, group, index):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        groupSet = {tuple(point) for point in group}

        num = 0

        for x, y in group:  # Iterate through all points in the group
            for dx, dy in directions:  # Check four directions
                row = x + dx
                col = y + dy

                # Check if the neighbor is within bounds and not part of the group
                if (0 <= row < 8 and 0 <= col < 8 and (row, col) not in groupSet):
                    num += 1
                    if self.boardArray[row][col] != index:
                        return False

        if num < len(group):
            return False

        return True

def show_error():
    # Create and display an error message box
    error_msg = QMessageBox()
    error_msg.setIcon(QMessageBox.Icon.Critical)
    error_msg.setWindowTitle("Error")
    error_msg.setText("You are not allow to place here")
    error_msg.setInformativeText("Please do another move")
    error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    error_msg.exec()

def show_error_redo():
    # Create and display an error message box
    error_msg = QMessageBox()
    error_msg.setIcon(QMessageBox.Icon.Critical)
    error_msg.setWindowTitle("Error")
    error_msg.setText("You are not allow to redo")
    error_msg.setInformativeText("")
    error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    error_msg.exec()

def show_Victory(player):
    info_box = QMessageBox()
    info_box.setIcon(QMessageBox.Icon.Information)
    info_box.setWindowTitle(f"{player} Victory")
    info_box.setText(f"Congrat {player}")
    info_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    info_box.exec()
