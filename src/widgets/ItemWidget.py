from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

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
        self.ui.label_article.setText(f' Артикль: {item["article"]}')
        self.ui.label_title.setText(f'Название: {item["title"]}')
        self.ui.label_category.setText(f'Категория: {item["category"]}')
        self.ui.label_description.setText(f'Описание: {item["description"]}')
        self.ui.label_manufacrure.setText(f'Производитель: {item["manufacture"]}')
        self.ui.label_suppiler.setText(f'Поставщик: {item["suppiler"]}')
        self.ui.label_quantity.setText(f'Количество на складе: {item["quantity"]} {item["unit"]}')
        self.ui.label_discount.setText(f'Скидка: {item["discount"]} %')



        if item["discount"] >= 15:
            old_price = item["price"]
            discount = item["discount"]
            new_price = old_price * (1 - discount / 100)

            self.ui.label_price.setText(
                f'<span style="color:red;"> Старая цена: <s>{old_price}</s> Руб</span><br>'
                f'<span style="color:black;">Новая цена: {round(new_price, 2)} Руб</span>'
            )
        else:
            self.ui.label_price.setText(f'{item["price"]} Руб')

        image_name = item["image"] or "img.png"
        pixmap = QPixmap(image_path(image_name))
        if pixmap.isNull():
            pixmap=QPixmap(image_path("img.png"))

        pixmap = pixmap.scaled(150,150, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.label_image.setPixmap(pixmap)

    def mousePressEvent(self, a0):
        main = self.window()
        main.select_widget(self)
