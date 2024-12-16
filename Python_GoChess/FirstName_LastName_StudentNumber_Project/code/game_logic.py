class GameLogic:
    # TODO add code here to manage the logic of your game
    def __init__(self, boardArr):
        super().__init__()
        self.playerTurn = 0
        self.boardArr = boardArr

    def gameTurn(self):
        self.playerTurn += 1
        if self.playerTurn % 2 == 0:
            return 2
        else:
            return 1

    def eatPieces(self):

        for row in range(8):
            for col in range(8):
                if self.boardArr[row][col] == 1:
                    if self.checkArr(row, col,2) == False:
                        self.boardArr[row][col] = 0

                elif self.boardArr[row][col] == 2:
                    if self.checkArr(row, col,1) == False:
                        self.boardArr[row][col] = 0

    def checkArr(self, x,y,idx): # just for 1 piece checking

        if x == 0:
            if y ==0:
                if self.boardArr[x+1][y] == idx and self.boardArr[x][y+1] == idx:
                    return False
                else:
                    return True
            elif y ==7:
                if self.boardArr[x+1][y] == idx and self.boardArr[x][y-1] == idx:
                    return False
                else:
                    return True
            else:
                if self.boardArr[x+1][y] == idx and self.boardArr[x][y-1] == idx and self.boardArr[x][y+1] == idx:
                    return False
                else:
                    return True

        elif x == 7:
            if y == 0:
                if self.boardArr[x - 1][y] == idx and self.boardArr[x][y + 1] == idx:
                    return False
                else:
                    return True
            elif y == 7:
                if self.boardArr[x - 1][y] == idx and self.boardArr[x][y - 1] == idx:
                    return False
                else:
                    return True
            else:
                if self.boardArr[x - 1][y] == idx and self.boardArr[x][y - 1] == idx and self.boardArr[x][y + 1] == idx:
                    return False
                else:
                    return True

        else:
            if y == 0:
                if self.boardArr[x + 1][y] == idx and self.boardArr[x - 1][y] == idx and self.boardArr[x][y + 1] == idx:
                    return False
                else:
                    return True
            elif y == 7:
                if self.boardArr[x + 1][y] == idx and self.boardArr[x - 1][y] == idx and self.boardArr[x][y - 1] == idx:
                    return False
                else:
                    return True
            else:
                if self.boardArr[x + 1][y] == idx and self.boardArr[x - 1][y] == idx and self.boardArr[x][y - 1] == idx and self.boardArr[x][y + 1] == idx:
                    return False
                else:
                    return True

