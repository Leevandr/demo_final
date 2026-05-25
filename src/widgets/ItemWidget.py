from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from ui.gen.ItemWidget import Ui_ItemWidget
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
IMAGES_DIR = ROOT_DIR / "resources" / "images"

def image_path(filename: str) -> str:
    return str(IMAGES_DIR / filename)

class ItemWidget(QWidget):
    def __init__(self, item):
        super().__init__()
        self.ui = Ui_ItemWidget()
        self.ui.setupUi(self)

        self.item = item
        self.fill()

    def fill(self):
        item = self.item
        self.ui.label_article.setText(item["article"])
        self.ui.label_title.setText(item["title"])
        self.ui.label_category.setText(item["category"])
        self.ui.label_description.setText(item["description"])
        self.ui.label_manufacrure.setText(item["manufacture"])
        self.ui.label_suppiler.setText(item["suppiler"])
        self.ui.label_quantity.setText(f'{item["quantity"]} {item["unit"]}')
        self.ui.label_discount.setText(f'{item["discount"]} %')


        self.ui.label_price.setText(str(item["price"]))

        if item["image"]:
            pixmap = QPixmap(image_path(item["image"])).scaled(150,150)
            self.ui.label_image.setPixmap(pixmap)
        else:
            pixmap = QPixmap(path).scaled(150,150)
            self.ui.label_image.setPixmap(pixmap)