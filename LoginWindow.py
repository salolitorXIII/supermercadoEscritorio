import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QDesktopWidget
from Database import Database
from MainWindow import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Correo electrónico")
        layout.addWidget(self.username_field)

        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Contraseña")
        self.password_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_field)

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.center_window()

    def center_window(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def login(self):
        login = Database().login(self.username_field.text(), self.password_field.text())
        if login:
            self.open_main_window()
        else:
            self.status_label.setText("Error de inicio de sesión")

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
