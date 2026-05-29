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
        self.ui.pushButton.clicked.connect(self.auth)
        self.ui.pushButton_2.clicked.connect(self.guest)

    def auth(self):
        login = self.ui.lineEdit_login.text()
        passwd = self.ui.lineEdit_password.text()

        if not login or not passwd:
            QMessageBox.warning(self, "Предупреждение заполните оба поля")
        else:
            user = dao.login(login, passwd)
            if user:
                self.main_window = MainWindow(user)
                self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь с таким логинов и паролем не найден")

    def guest(self):
        self.main_window = MainWindow(user={"role_id": 4, "full_name": "Выполнен вход в качестве гостя"})
        self.main_window.show()
        self.close()