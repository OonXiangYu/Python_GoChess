class GameLogic:
    # TODO add code here to manage the logic of your game
    def __init__(self, boardArr):
        super().__init__()
        self.playerTurn = 0
        self.boardArr = boardArr

    def gameTurn(self):
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

    def eatPieces(self):
        try:
            for row in range(8):
                for col in range(8):
                    if self.boardArr[row][col] == 1:
                        if self.checkArr(row, col,2) == False:
                            self.boardArr[row][col] = 3 # ate by white chess, use a number to mark
                        else:
                            group = self.checkMultipleArr([row[:] for row in self.boardArr], 1)
                            if self.eatMultiplePieces(group, 2):
                                for x, y in group:
                                    self.boardArr[x][y] = 0
                    elif self.boardArr[row][col] == 2:
                        if self.checkArr(row, col,1) == False:
                            self.boardArr[row][col] = 4 # ate by black chess, use a number to mark
                        else:
                            group = self.checkMultipleArr([row[:] for row in self.boardArr], 2)
                            if self.eatMultiplePieces(group, 1):
                                for x, y in group:
                                    self.boardArr[x][y] = 0

        except Exception as e:
            print(e)

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

        for x in range(len(boardArray)):
            for y in range(len(boardArray[0])):
                if boardArray[x][y] == index:  # Start DFS at the first index found
                    group = []
                    dfs(x, y, group)
                    if len(group) > 1: # where there is multiple pieces form a group
                        return group  # Return the first group found

        return []  # Return an empty list if no group is found

    def eatMultiplePieces(self, group, index):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        groupSet = {tuple(point) for point in group}

        for x, y in group:  # Iterate through all points in the group
            for dx, dy in directions:  # Check four directions
                row = x + dx
                col = y + dy

                # Check if the neighbor is within bounds and not part of the group
                if (0 <= row < 8 and 0 <= col < 8 and (row, col) not in groupSet):
                    if self.boardArr[row][col] != index:
                        return False

        return True
