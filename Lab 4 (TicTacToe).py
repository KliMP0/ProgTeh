import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout,
                             QPushButton, QMessageBox, QVBoxLayout,
                             QLabel, QHBoxLayout, QRadioButton)
from PyQt5.QtCore import Qt


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Крестики-нолики 10x10")
        self.initUI()

    def initUI(self):
        self.player = 'X'
        self.game_over = False

        self.reset_button = QPushButton("Перезапуск игры", self)
        self.reset_button.clicked.connect(self.reset_game)

        self.buttonX = QRadioButton("X")
        self.buttonX.clicked.connect(self.chose_X)
        self.buttonX.setChecked(True)
        self.button0 = QRadioButton("O")
        self.button0.clicked.connect(self.chose_0)

        self.label_status = QLabel("Выберите игрока и ходите")
        self.label_status.setStyleSheet("font-family: 'Times New Roman'; font-size: 20px;")

        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.buttons = [[None for _ in range(10)] for _ in range(10)]
        self.create_grid()

        # Компоновка
        layout = QVBoxLayout()
        layout.setSpacing(15)

        layout.addWidget(self.reset_button)

        layout_chose = QHBoxLayout()
        layout_chose.setSpacing(30)
        layout_chose.addWidget(self.buttonX, alignment=Qt.AlignRight)
        layout_chose.addWidget(self.button0, alignment=Qt.AlignLeft)
        layout.addLayout(layout_chose)

        layout.addWidget(self.label_status, alignment=Qt.AlignCenter)

        layout.addLayout(self.grid)

        self.setLayout(layout)

    def create_grid(self):
        for i in range(10):
            for j in range(10):
                button = QPushButton("")
                button.setFixedSize(40, 40)
                button.clicked.connect(lambda checked, row=i, col=j: self.button_clicked(row, col))
                self.buttons[i][j] = button
                self.grid.addWidget(button, i, j)

    def button_clicked(self, row, col):

        self.buttonX.setEnabled(False)
        self.button0.setEnabled(False)

        if self.game_over or self.buttons[row][col].text():
            return


        self.buttons[row][col].setText(self.player)
        if self.player == 'X':
            self.buttons[row][col].setStyleSheet(f"background-color: lightblue; color: black; font-size: 20px;")
        else:
            self.buttons[row][col].setStyleSheet(f"background-color: lightcoral; color: black; font-size: 20px;")

        if self.check_win(row, col):
            self.game_over = True
            self.label_status.setText("Игра окончена")
            QMessageBox.information(self, "Игра окончена!", f"Победил игрок {self.player}!")
        else:
            self.switch_player()

    def check_win(self, row, col):
        # по горизонтали
        count = 1
        for j in range(col + 1, 10):
            if self.buttons[row][j].text() == self.player:
                count += 1
            else:
                break
        for j in range(col - 1, -1, -1):
            if self.buttons[row][j].text() == self.player:
                count += 1
            else:
                break
        if count >= 4:
            return True

        # по вертикали
        count = 1
        for i in range(row + 1, 10):
            if self.buttons[i][col].text() == self.player:
                count += 1
            else:
                break
        for i in range(row - 1, -1, -1):
            if self.buttons[i][col].text() == self.player:
                count += 1
            else:
                break
        if count >= 4:
            return True

        # по диагонали (слева-вправо)
        count = 1
        i = row + 1
        j = col + 1
        while i < 10 and j < 10:
            if self.buttons[i][j].text() == self.player:
                count += 1
                i += 1
                j += 1
            else:
                break
        i = row - 1
        j = col - 1
        while i >= 0 and j >= 0:
            if self.buttons[i][j].text() == self.player:
                count += 1
                i -= 1
                j -= 1
            else:
                break
        if count >= 4:
            return True

        # (справа-влево)
        count = 1
        i = row + 1
        j = col - 1
        while i < 10 and j >= 0:
            if self.buttons[i][j].text() == self.player:
                count += 1
                i += 1
                j -= 1
            else:
                break
        i = row - 1
        j = col + 1
        while i >= 0 and j < 10:
            if self.buttons[i][j].text() == self.player:
                count += 1
                i -= 1
                j += 1
            else:
                break
        if count >= 4:
            return True

        return False

    def chose_X(self):
        self.player = 'X'

    def chose_0(self):
        self.player = 'O'

    def switch_player(self):
        if self.player == 'X':
            self.label_status.setText("Ход игрока O")
            self.player = 'O'
        else:
            self.label_status.setText("Ход игрока X")
            self.player = 'X'

    def reset_game(self):
        self.buttonX.setEnabled(True)
        self.button0.setEnabled(True)

        self.game_over = False
        self.label_status.setText("выберите игрока и ходите")

        if self.buttonX.isChecked():
            self.player = 'X'
        else:
            self.player = 'O'

        for i in range(10):
            for j in range(10):
                self.buttons[i][j].setText("")
                self.buttons[i][j].setStyleSheet("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = TicTacToe()
    game.setFixedSize(430, 540)
    game.show()
    sys.exit(app.exec_())