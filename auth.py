from PyQt6.QtWidgets import QWidget, QMessageBox

from db import dao
from gen.auth_window import Ui_AuthForm
from main_window import MainWindow


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AuthForm()
        self.ui.setupUi(self)
        self.conn()
        self.main_window = None

    def conn(self):
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QPixmap
        self.ui.label_for_logo.setPixmap(QPixmap("image/logo/logo.png").scaled(
            80, 60, Qt.AspectRatioMode.KeepAspectRatio
        ))
        self.ui.pushButton.setStyleSheet("background-color: #00FA9A; color: black;")
        self.ui.pushButton.clicked.connect(self.auth)
        self.ui.pushButton_2.clicked.connect(self.guest)

    def auth(self):
        login = self.ui.lineEdit_login.text()
        passwd = self.ui.lineEdit_password.text()

        if not login or not passwd:
            QMessageBox.warning(self, "Предупреждение", "Введите логин и пароль.")
        else:
            user = dao.login(login, passwd)
            if user:
                self.main_window = MainWindow(user)
                self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь с указанными данными не найден.")

    def guest(self):
        # вход без авторизации с минимальными правами
        self.main_window = MainWindow(user={"role_id": 4, "full_name": "Гость"})
        self.main_window.show()
        self.close()
