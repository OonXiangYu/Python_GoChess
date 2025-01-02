from PyQt6.QtWidgets import QFrame, QApplication, QMessageBox, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QRectF, pyqtSlot
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont
import copy

class GameLogic(QFrame):
    # TODO add code here to manage the logic of your game
    def __init__(self, boardArr):
        super().__init__()
        self.playerTurn = 0
        self.boardArr = boardArr
        self.tempBoard = copy.deepcopy(self.boardArr)

    def getBlackPiece(self): # get the total black pieces on the board
        blackPiece = 0

        for row in range(7):
            for col in range(7):
                if self.boardArr[row][col] == 1:
                    blackPiece += 1

        return blackPiece

    def getWhitePiece(self): # get the total white pieces on the board
        whitePiece = 0

        for row in range(7):
            for col in range(7):
                if self.boardArr[row][col] == 2:
                    whitePiece += 1

        return whitePiece

    def resetGameTurn(self):
        self.playerTurn = 0

    def getGameTurn(self): # for getting player turn
        return self.playerTurn

    def setGameTurn(self, gameTurn): # reset the game turn
        self.playerTurn = gameTurn

    def gameTurn(self): # for switching turn when press
        try:
            self.playerTurn += 1
            if self.playerTurn % 2 == 0:
                return 2
            else:
                return 1
        except Exception as e:
            print(e)

    def regretGameTurn(self): # make the game turn to previous
        try:
            self.playerTurn -= 1
        except Exception as e:
            print(e)

    def passGameTurn(self):
        self.playerTurn += 1

    def suicideRule(self, row, col, amount, idx): # to count the pieces on the board after placed, if the amount is decrease then is suicide
        self.tempBoard = copy.deepcopy(self.boardArr)
        num = 0
        self.tempBoard[row][col] = idx
        self.eatPiecesTesting()

        for x in range(7):
            for y in range(7):
                if self.tempBoard[x][y] == idx:
                    num += 1

        if num < amount:
            print(num, "," , amount)
            return False
        else:
            return True

    def eatPieces(self):
        try:
            for row in range(7):
                for col in range(7):
                    if self.boardArr[row][col] == 1:
                        if self.checkArr(row, col,2) == False:
                            self.boardArr[row][col] = 0
                        else:
                            group = self.checkMultipleArr([row[:] for row in self.boardArr], 1)
                            for grp in group:
                                if self.eatMultiplePieces(grp, 2):
                                    for x, y in grp:
                                        self.boardArr[x][y] = 0

                    elif self.boardArr[row][col] == 2:
                        if self.checkArr(row, col,1) == False:
                            self.boardArr[row][col] = 0

                        else:
                            group = self.checkMultipleArr([row[:] for row in self.boardArr], 2)
                            for grp in group:
                                if self.eatMultiplePieces(grp, 1):
                                    for x, y in grp:
                                        self.boardArr[x][y] = 0

        except Exception as e:
            print("eatPieces : ",e)

    def checkArr(self, x, y, idx): # just for 1 piece checking
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        for dx, dy in directions:  # Check four directions
            row, col = x + dx, y + dy

            if (0 <= row < len(self.boardArr) and 0 <= col < len(self.boardArr[0])):
                if self.boardArr[row][col] != idx:
                    return True

        return False

    def checkMultipleArr(self, boardArray, index):
        def dfs(x, y, group):
            if x < 0 or y < 0 or x >= len(boardArray) or y >= len(boardArray[0]) or boardArray[x][y] != index:
                return
            boardArray[x][y] = -1  # Mark as visited
            group.append([x, y])

            # Explore all 4 directions
            dfs(x + 1, y, group)
            dfs(x - 1, y, group)
            dfs(x, y + 1, group)
            dfs(x, y - 1, group)

        groups = [] # a big arr to store all the group
        for x in range(len(boardArray)):
            for y in range(len(boardArray[0])):
                if boardArray[x][y] == index:  # Start DFS at the first index found
                    group = []
                    dfs(x, y, group)
                    if len(group) > 1: # where there is multiple pieces form a group
                        groups.append(group)

        return groups

    def eatMultiplePieces(self, group, index):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        groupSet = {tuple(point) for point in group}

        for x, y in group:  # Iterate through all points in the group
            for dx, dy in directions:  # Check four directions
                row = x + dx
                col = y + dy

                # Check if the neighbor is within bounds and not part of the group
                if (0 <= row < 7 and 0 <= col < 7 and (row, col) not in groupSet):
                    if self.boardArr[row][col] != index:
                        return False

        return True

    def eatPiecesTesting(self): # testing for suicide Rule same logic as above
        try:
            for row in range(7):
                for col in range(7):
                    if self.tempBoard[row][col] == 1:
                        if self.checkArrTesting(row, col, 2) == False:
                            self.tempBoard[row][col] = 0
                        else:
                            group = self.checkMultipleArrTesting([row[:] for row in self.tempBoard], 1)
                            for grp in group:
                                if self.eatMultiplePiecesTesting(grp, 2):
                                    for x, y in grp:
                                        self.tempBoard[x][y] = 0
                    elif self.tempBoard[row][col] == 2:
                        if self.checkArrTesting(row, col, 1) == False:
                            self.tempBoard[row][col] = 0
                        else:
                            group = self.checkMultipleArrTesting([row[:] for row in self.tempBoard], 2)
                            for grp in group:
                                if self.eatMultiplePiecesTesting(grp, 1):
                                    for x, y in grp:
                                        self.tempBoard[x][y] = 0
        except Exception as e:
            print("eatPieces : ", e)

    def checkArrTesting(self, x, y, idx):  # just for 1 piece checking
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        for dx, dy in directions:  # Check four directions
            row, col = x + dx, y + dy

            if (0 <= row < len(self.tempBoard) and 0 <= col < len(self.tempBoard[0])):
                if self.tempBoard[row][col] != idx:
                    return True

        return False

    def checkMultipleArrTesting(self, boardArray, index):
        def dfs(x, y, group):
            if x < 0 or y < 0 or x >= len(boardArray) or y >= len(boardArray[0]) or boardArray[x][y] != index:
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
                if boardArray[x][y] == index:  # Start DFS at the first index found
                    group = []
                    dfs(x, y, group)
                    if len(group) > 1:  # where there is multiple pieces form a group
                        groups.append(group)

        return groups

    def eatMultiplePiecesTesting(self, group, index):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        groupSet = {tuple(point) for point in group}

        for x, y in group:  # Iterate through all points in the group
            for dx, dy in directions:  # Check four directions
                row = x + dx
                col = y + dy

                # Check if the neighbor is within bounds and not part of the group
                if (0 <= row < 7 and 0 <= col < 7 and (row, col) not in groupSet):
                    if self.tempBoard[row][col] != index:
                        return False

        return True

def show_error():
    # Create and display an error message box
    error_msg = QMessageBox()
    error_msg.setIcon(QMessageBox.Icon.Critical)
    error_msg.setWindowTitle("Error")
    error_msg.setText("You are not allow to redo")
    error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    error_msg.exec()