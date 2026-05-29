from PyQt6.QtWidgets import QApplication

from auth import AuthWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())
