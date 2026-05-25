from PyQt6.QtWidgets import QWidget, QMessageBox

from src.db import dao
from src.widgets.MainWindow import MainWindow
from ui.gen.Auth import Ui_Auth


class Auth(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Auth()
        self.ui.setupUi(self)

        self.main_window = None
        self.ui.pushButton_2.clicked.connect(self.login)
        self.ui.pushButton.clicked.connect(self.login_as_guest)

    def login_as_guest(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def login(self):

        login = self.ui.lineEdit_login.text()
        password = self.ui.lineEdit_password.text()
        if not login or not password:
            QMessageBox.warning(self,"Проверьте логин или пароль", "Введите логин и пароль")

        user = dao.login(login,password)

        if user:
            self.main_window = MainWindow(user)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Пользователь не существует", "Пользователь не существует")

