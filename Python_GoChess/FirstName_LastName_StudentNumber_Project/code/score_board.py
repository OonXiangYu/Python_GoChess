from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSlot, pyqtSignal

class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''
    resetSignal = pyqtSignal()
    passSignal = pyqtSignal()
    redoSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')
        self.blackPiece = "./image/black.png"
        self.whitePiece = "./image/white.png"

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        self.label_playerTurn = QLabel()
        self.label_playerTurn.setText(
            f'<span>Current Player: Player 1 </span>'
            f'<img src="{self.blackPiece}" width="16" height="16">'
        )

        self.label_clickLocation = QLabel("Click Location: ")

        self.label_timeRemaining1 = QLabel()
        self.label_timeRemaining1.setText(
            f'<div>Player 1 '
            f'<img src="{self.blackPiece}" width="16" height="16">'
            f' Time remaining: 2 : 00</div>'
        )
        self.label_timeRemaining2 = QLabel()
        self.label_timeRemaining2.setText(
            f'<div>Player 2 '
            f'<img src="{self.whitePiece}" width="16" height="16">'
            f' Time remaining: 2 : 00</div>'
        )
        self.label_territory1 = QLabel("Player 1 Territory : 0")
        self.label_territory1.setText(
            f'<div>Player 1 '
            f'<img src="{self.blackPiece}" width="16" height="16">'
            f' Territory : 0</div>'
        )

        self.label_territory2 = QLabel("Player 2 Territory : 0")
        self.label_territory2.setText(
            f'<div>Player 2 '
            f'<img src="{self.whitePiece}" width="16" height="16">'
            f' Territory : 0</div>'
        )
        self.label_captured1 = QLabel("Player 1 Captured : 0")
        self.label_captured1.setText(
            f'<div>Player 1 '
            f'<img src="{self.blackPiece}" width="16" height="16">'
            f' Captured : 0</div>'
        )

        self.label_captured2 = QLabel("Player 2 Captured : 0")
        self.label_captured2.setText(
            f'<div>Player 2 '
            f'<img src="{self.whitePiece}" width="16" height="16">'
            f' Captured : 0</div>'
        )

        self.passButton = QPushButton("Pass")
        self.regretButton = QPushButton("Undo")
        self.resetButton = QPushButton("Reset Game")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_playerTurn)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.label_territory1)
        self.mainLayout.addSpacing(1)
        self.mainLayout.addWidget(self.label_territory2)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.label_captured1)
        self.mainLayout.addSpacing(1)
        self.mainLayout.addWidget(self.label_captured2)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.label_timeRemaining1)
        self.mainLayout.addSpacing(1)
        self.mainLayout.addWidget(self.label_timeRemaining2)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.passButton)
        self.mainLayout.addWidget(self.regretButton)
        self.mainLayout.addWidget(self.resetButton)
        self.setWidget(self.mainWidget)

        self.resetButton.clicked.connect(self.resetGame)
        self.passButton.clicked.connect(self.passGame)
        self.regretButton.clicked.connect(self.redoBoard)

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal1.connect(self.setTimeRemaining1)
        board.updateTimerSignal2.connect(self.setTimeRemaining2)
        board.playerTurnSignal.connect(self.updateCurrentPlayer)
        board.player1TerritorySignal.connect(self.updatePlayer1Territory)
        board.player2TerritorySignal.connect(self.updatePlayer2Territory)
        board.player1CapturedSignal.connect(self.updatePlayer1Captured)
        board.player2CapturedSignal.connect(self.updatePlayer2Captured)

    def resetGame(self):
        self.resetSignal.emit()
        self.label_playerTurn.setText(
            f'<span>Current Player: Player 1 </span>'
            f'<img src="{self.blackPiece}" width="16" height="16">'
        )

    def passGame(self):
        self.passSignal.emit()

    def redoBoard(self):
        self.redoSignal.emit()

    @pyqtSlot(int)
    def updateCurrentPlayer(self,turn):
        if turn % 2 == 1: # is not = 0 becuz before this method i ady add 1 to the game turn
            self.label_playerTurn.setText(
                f'<span>Current Player: Player 2 </span>'
                f'<img src="{self.whitePiece}" width="16" height="16">'
            )
        else:
            self.label_playerTurn.setText(
                f'<span>Current Player: Player 1 </span>'
                f'<img src="{self.blackPiece}" width="16" height="16">'
            )

    @pyqtSlot(list)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        if clickLoc[0] > -1:
            update = f"{chr(65 + clickLoc[1])} , {clickLoc[0] + 1}" # using acsii table to get alphabet
        else:
            update = ""

        self.label_clickLocation.setText("Click Location: " + update)
        #print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining1(self, timeRemaining):
        '''updates the time remaining label to show the time remaining for player 1'''
        min = timeRemaining // 60  # Get the whole minutes
        secs = timeRemaining % 60  # Get the remaining seconds
        if secs == 0:
            update = f"{min} : 00 "
        else:
            update = f"{min} : {secs} "

        self.label_timeRemaining1.setText(
            f'<div>Player 1 '
            f'<img src="{self.blackPiece}" width="16" height="16">'
            f' Time remaining: {update}</div>'
        )

    @pyqtSlot(int)
    def setTimeRemaining2(self, timeRemaining):
        '''updates the time remaining label to show the time remaining for player 2'''
        min = timeRemaining // 60  # Get the whole minutes
        secs = timeRemaining % 60  # Get the remaining seconds
        if secs == 0:
            update = f"{min} : 00 "
        else:
            update = f"{min} : {secs} "

        self.label_timeRemaining2.setText(
            f'<div>Player 2 '
            f'<img src="{self.whitePiece}" width="16" height="16">'
            f' Time remaining: {update}</div>'
        )

    @pyqtSlot(int)
    def updatePlayer1Territory(self, territory):

        self.label_territory1.setText(
            f'<div>Player 1 '
            f'<img src="{self.blackPiece}" width="16" height="16">'
            f' Territory : {territory}</div>'
        )

    @pyqtSlot(int)
    def updatePlayer2Territory(self, territory):

        self.label_territory2.setText(
            f'<div>Player 2 '
            f'<img src="{self.whitePiece}" width="16" height="16">'
            f' Territory : {territory}</div>'
        )

    @pyqtSlot(int)
    def updatePlayer1Captured(self, piece):

        self.label_captured1.setText(
            f'<div>Player 1 '
            f'<img src="{self.blackPiece}" width="16" height="16">'
            f' Captured : {piece}</div>'
        )

    @pyqtSlot(int)
    def updatePlayer2Captured(self, piece):

        self.label_captured2.setText(
            f'<div>Player 2 '
            f'<img src="{self.whitePiece}" width="16" height="16">'
            f' Captured : {piece}</div>'
        )

