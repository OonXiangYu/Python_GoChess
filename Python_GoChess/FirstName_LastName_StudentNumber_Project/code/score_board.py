from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import pyqtSlot, pyqtSignal

from Python_GoChess.FirstName_LastName_StudentNumber_Project.code.game_logic import GameLogic


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''
    resetSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        self.game = GameLogic(1)

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        self.label_playerTurn = QLabel("Current Player : Player 1")
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining1 = QLabel("Player 1 Time remaining: 10 : 00")
        self.label_timeRemaining2 = QLabel("Player 2 Time remaining: 10 : 00")
        self.resetButton = QPushButton(" Reset Game")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_playerTurn)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.label_timeRemaining1)
        self.mainLayout.addSpacing(1)
        self.mainLayout.addWidget(self.label_timeRemaining2)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.resetButton)
        self.setWidget(self.mainWidget)

        self.resetButton.clicked.connect(self.resetGame)

        self.rst = 0

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        #board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal1.connect(self.setTimeRemaining1)
        board.updateTimerSignal2.connect(self.setTimeRemaining2)
        board.playerTurnSignal.connect(self.updateCurrentPlayer)

    def resetGame(self):
        self.resetSignal.emit()

    @pyqtSlot(int)
    def updateCurrentPlayer(self,turn):
        if turn % 2 == 1: # is not = 0 becuz before this method i ady add 1 to the game turn
            self.label_playerTurn.setText("Current Player : Player 2")
        else:
            self.label_playerTurn.setText("Current Player : Player 1")

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location: " + clickLoc)
        #print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining1(self, timeRemaining):
        '''updates the time remaining label to show the time remaining for player 1'''
        min = timeRemaining // 60  # Get the whole minutes
        secs = timeRemaining % 60  # Get the remaining seconds
        if secs == 0:
            update = f"Player 1 Time Remaining: {min} : 00 "
        else:
            update = f"Player 1 Time Remaining: {min} : {secs} "
        self.label_timeRemaining1.setText(update)

    @pyqtSlot(int)
    def setTimeRemaining2(self, timeRemaining):
        '''updates the time remaining label to show the time remaining for player 2'''
        min = timeRemaining // 60  # Get the whole minutes
        secs = timeRemaining % 60  # Get the remaining seconds
        if secs == 0:
            update = f"Player 2 Time Remaining: {min} : 00 "
        else:
            update = f"Player 2 Time Remaining: {min} : {secs} "
        self.label_timeRemaining2.setText(update)


