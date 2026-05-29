from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication

from auth import AuthWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    p = QPalette()
    p.setColor(QPalette.ColorRole.Window,          QColor("#f0f0f0"))
    p.setColor(QPalette.ColorRole.WindowText,      QColor("#000000"))
    p.setColor(QPalette.ColorRole.Base,            QColor("#ffffff"))
    p.setColor(QPalette.ColorRole.AlternateBase,   QColor("#e8e8e8"))
    p.setColor(QPalette.ColorRole.Text,            QColor("#000000"))
    p.setColor(QPalette.ColorRole.Button,          QColor("#e0e0e0"))
    p.setColor(QPalette.ColorRole.ButtonText,      QColor("#000000"))
    p.setColor(QPalette.ColorRole.BrightText,      QColor("#ffffff"))
    p.setColor(QPalette.ColorRole.Highlight,       QColor("#0078d4"))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(p)

    window = AuthWindow()
    window.show()
    sys.exit(app.exec())
