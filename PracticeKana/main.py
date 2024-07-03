import sys
import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QStackedWidget, QStyleFactory, QMessageBox, QShortcut
)
from kana_data import (
    hiragana_basic, katakana_basic, hiragana_dakuten, katakana_dakuten,
    hiragana_to_romaji, katakana_to_romaji
)


class MainMenu(QWidget):
    def __init__(self, switch_to_practice):
        super().__init__()
        self.switch_to_practice = switch_to_practice
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('PracitceKana.ico'))
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        buttons = [
            ("Practice Hiragana Basic", 'hiragana_basic'),
            ("Practice Katakana Basic", 'katakana_basic'),
            ("Practice Hiragana Dakuten", 'hiragana_dakuten'),
            ("Practice Katakana Dakuten", 'katakana_dakuten'),
            ("Practice Hiragana All", 'hiragana_all'),
            ("Practice Katakana All", 'katakana_all'),
        ]

        for text, mode in buttons:
            button = QPushButton(text)
            button.setFont(QFont('Arial', 16))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-radius: 10px;
                    padding: 15px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            button.clicked.connect(self.create_switch_to_practice_lambda(mode))
            layout.addWidget(button)

        self.setLayout(layout)

    def create_switch_to_practice_lambda(self, mode):
        return lambda: self.switch_to_practice(mode)


class KanaPracticeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_kana = ""
        self.kana_to_romaji = {}
        self.used_kanas = set()
        self.correct_answers = 0
        self.total_answers = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kana Practice')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('PracitceKana.ico'))

        self.setStyleSheet("background-color: #ecf0f1;")

        self.stacked_widget = QStackedWidget()

        self.main_menu = MainMenu(self.switch_to_practice)
        self.practice_widget = QWidget()
        self.practice_layout = QVBoxLayout()

        self.kana_label = QLabel("", self.practice_widget)
        self.kana_label.setFont(QFont('Arial', 100))
        self.kana_label.setAlignment(Qt.AlignCenter)
        self.practice_layout.addWidget(self.kana_label)

        self.input_line = QLineEdit(self.practice_widget)
        self.input_line.setFont(QFont('Arial', 24))
        self.input_line.setAlignment(Qt.AlignCenter)
        self.input_line.returnPressed.connect(self.handle_enter_key)
        self.practice_layout.addWidget(self.input_line)

        self.check_button = QPushButton("Check", self.practice_widget)
        self.check_button.setFont(QFont('Arial', 16))
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.check_button.clicked.connect(self.check_answer)
        self.practice_layout.addWidget(self.check_button)

        self.result_label = QLabel("", self.practice_widget)
        self.result_label.setFont(QFont('Arial', 18))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.practice_layout.addWidget(self.result_label)

        self.next_button = QPushButton("Next", self.practice_widget)
        self.next_button.setFont(QFont('Arial', 16))
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        self.next_button.clicked.connect(self.update_kana)
        self.practice_layout.addWidget(self.next_button)

        self.back_button = QPushButton("Back to Main Menu", self.practice_widget)
        self.back_button.setFont(QFont('Arial', 16))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.back_button.clicked.connect(self.back_to_main_menu)
        self.practice_layout.addWidget(self.back_button)

        self.practice_layout.setSpacing(20)
        self.practice_layout.setContentsMargins(50, 50, 50, 50)

        self.practice_widget.setLayout(self.practice_layout)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.practice_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def switch_to_practice(self, mode):
        if mode == 'hiragana_basic':
            self.kana_list = hiragana_basic[:]
            self.kana_to_romaji = hiragana_to_romaji
        elif mode == 'katakana_basic':
            self.kana_list = katakana_basic[:]
            self.kana_to_romaji = katakana_to_romaji
        elif mode == 'hiragana_dakuten':
            self.kana_list = hiragana_dakuten[:]
            self.kana_to_romaji = hiragana_to_romaji
        elif mode == 'katakana_dakuten':
            self.kana_list = katakana_dakuten[:]
            self.kana_to_romaji = katakana_to_romaji
        elif mode == 'hiragana_all':
            self.kana_list = hiragana_basic + hiragana_dakuten
            self.kana_to_romaji = hiragana_to_romaji
        elif mode == 'katakana_all':
            self.kana_list = katakana_basic + katakana_dakuten
            self.kana_to_romaji = katakana_to_romaji

        self.used_kanas.clear()
        self.correct_answers = 0
        self.total_answers = 0
        self.stacked_widget.setCurrentWidget(self.practice_widget)
        self.update_kana()
        self.input_line.setFocus()

    def back_to_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def update_kana(self):
        if len(self.kana_list) == 0:
            self.display_results()
        else:
            self.current_kana = random.choice(self.kana_list)
            self.kana_list.remove(self.current_kana)
            self.kana_label.setText(self.current_kana)
            self.input_line.clear()
            self.result_label.setText("")
            self.input_line.setFocus()

    def check_answer(self):
        user_input = self.input_line.text().strip().lower()
        correct_answer = self.kana_to_romaji.get(self.current_kana, "")

        if user_input == correct_answer:
            self.correct_answers += 1
            self.result_label.setText("Correct!")
            self.result_label.setStyleSheet("color: green;")
        else:
            self.result_label.setText(f"Wrong! Correct answer: {correct_answer}")
            self.result_label.setStyleSheet("color: red;")

        self.total_answers += 1

    def handle_enter_key(self):
        if self.result_label.text() == "":
            self.check_answer()
        else:
            self.update_kana()
            self.input_line.setFocus()

    def display_results(self):
        percentage = (self.correct_answers / self.total_answers) * 100 if self.total_answers > 0 else 0
        result_message = f"You have practiced all kana!\nCorrect answers: {self.correct_answers}/{self.total_answers}\nAccuracy: {percentage:.2f}%"
        self.result_label.setText(result_message)
        self.kana_label.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = KanaPracticeApp()
    ex.show()
    sys.exit(app.exec_())