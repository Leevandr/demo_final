from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from pathlib import Path
from decimal import Decimal

from ui.gen.ItemWidget import Ui_ItemWidget

ROOT_DIR = Path(__file__).resolve().parents[2]
IMAGES_DIR = ROOT_DIR / "resources" / "images"


def image_path(filename: str) -> str:
    return str(IMAGES_DIR / filename)


class ItemWidget(QWidget):
    def __init__(self, item):
        super().__init__()
        self.ui = Ui_ItemWidget()
        self.ui.setupUi(self)
        self.ui.frame_card.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.item = item
        self.is_selected = False
        self.fill()

    def price_color(self):
        if int(self.item["quantity"]) <= 0:
            return "#1f6feb"
        return "black"

    def price_text(self, value):
        price = Decimal(str(value)).quantize(Decimal("0.01"))
        return str(price)

    def apply_style(self):
        border = "4px solid #1f6feb" if self.is_selected else "1px solid #263238"
        self.ui.frame_card.setStyleSheet(
            "QFrame#frame_card { background-color: #ffffff; border: %s; border-radius: 0px; }" % border
        )
        self.ui.frame_price.setStyleSheet(
            "QFrame#frame_price { background-color: #ffffff; border: 1px solid #263238; border-radius: 0px; }"
        )

    def set_selected(self, value: bool):
        self.is_selected = value
        self.apply_style()

    def fill(self):
        item = self.item
        self.apply_style()
        self.ui.label_article.setText(f'Артикул: {item["article"]}')
        self.ui.label_title.setText(f'Название: {item["title"]}')
        self.ui.label_category.setText(f'Категория: {item["category"]}')
        self.ui.label_description.setText(f'Описание: {item["description"]}')
        self.ui.label_manufacrure.setText(f'Производитель: {item["manufacture"]}')
        self.ui.label_suppiler.setText(f'Поставщик: {item["suppiler"]}')
        self.ui.label_quantity.setText(f'Остаток: {item["quantity"]} {item["unit"]}')
        self.ui.label_discount.setText(f'Скидка: {item["discount"]} %')

        price = Decimal(str(item["price"]))
        discount = Decimal(str(item["discount"]))

        if discount > 0:
            new_price = price
            if discount >= 100:
                old_price = new_price
            else:
                old_price = new_price / (1 - discount / Decimal("100"))

            self.ui.label_price.setText(
                f'<span style="color:red;">Старая цена: <s>{self.price_text(old_price)}</s> Руб</span><br>'
                f'<span style="color:{self.price_color()};">Новая цена: {self.price_text(new_price)} Руб</span>'
            )
        else:
            self.ui.label_price.setText(
                f'<span style="color:{self.price_color()};">{self.price_text(price)} Руб</span>'
            )

        image_name = item["image"] or "img.png"
        if image_name == "None":
            image_name = "img.png"
        pixmap = QPixmap(image_path(image_name))
        if pixmap.isNull():
            pixmap = QPixmap(image_path("img.png"))

        pixmap = pixmap.scaled(
            150,
            150,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.ui.label_image.setPixmap(pixmap)

    def mousePressEvent(self, a0):
        main = self.window()
        main.select_widget(self)
