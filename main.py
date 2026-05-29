from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QIcon

from auth import AuthWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # шрифт и иконка применяются ко всем окнам приложения
    app.setFont(QFont("Times New Roman", 11))
    app.setWindowIcon(QIcon("image/logo/logo.png"))

    window = AuthWindow()
    window.show()
    sys.exit(app.exec())
