from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QMenuBar, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon

from board import Board
from score_board import ScoreBoard
from game_logic import GameLogic


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''Initiates application UI'''
        self.board = Board(self)
        self.setCentralWidget(self.board)

        menuBar = self.menuBar()
        rules = menuBar.addMenu("Rules")
        ruleAction = QAction("Rules",self)
        ruleAction = QAction(QIcon("./image/rule.png"), "Rules", self)
        ruleAction.triggered.connect(self.showRule)
        rules.addAction(ruleAction)

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)
        self.board.makeConnection(self.scoreBoard)

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Go')
        self.show()


    def center(self):
        '''Centers the window on the screen'''
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def showRule(self): # window to show rules
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Rule")
        msg_box.setWindowIcon(QIcon("./image/rule.png"))
        msg_box.setText("1. Every Players have only 2 mins for play \n"
                        "2. Players can't redo continuously \n"
                        "3. Player who reach above 32 territory first victory \n"
                        "4. Players have unlimited pass chances")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()





