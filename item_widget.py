from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from gen.ItemWidget import Ui_ItemWidget

CARD_BASE = """
    QWidget#ItemWidget {{
        border: 1px solid #b0b0b0;
        border-radius: 6px;
        {bg}
    }}
"""


class ItemWidget(QWidget):
    def __init__(self, product):
        super().__init__()
        self.ui = Ui_ItemWidget()
        self.ui.setupUi(self)
        self.setObjectName("ItemWidget")
        self.product = product
        self.base_style = ""
        self.fill_items()

    def fill_items(self):
        article = self.product.get("article", "")
        self.ui.label_category.setText(f"Артикул: {article}")
        self.ui.label_title.setText(f"<b>Название: {self.product['product_name']}</b>")
        self.ui.label_manufacture.setText(f"Производитель: {self.product['manufacture_name']}")
        self.ui.label_description.setText(f"Описание: {self.product['descrip']}")
        self.ui.label_supplier.setText(f"Поставщик: {self.product['supplier_name']}")
        self.ui.label_unit.setText(f"Ед. изм.: {self.product['unit_name']}")
        self.ui.label_quantity.setText(f"Остаток: {self.product['quantity']} Шт.")

        discount = self.product["discount"] or 0
        price = self.product["price"] or 0
        self.ui.label_discount.setText(f"<b>Скидка: {discount} %</b>")

        if discount > 0:
            final_price = round(price * (1 - discount / 100), 2)
            self.ui.label_price.setText(
                f"<font color='red'><s>Цена: {price:.2f} Руб.</s></font><br>"
                f"Итоговая цена: {final_price:.2f} Руб."
            )
        else:
            self.ui.label_price.setText(f"Цена: {price:.2f} Руб.")

        if discount > 15:
            bg = "background-color: #2E8B57;"
        elif self.product["quantity"] == 0:
            bg = "background-color: #ADD8E6;"
        else:
            bg = "background-color: #ffffff;"

        self.base_style = CARD_BASE.format(bg=bg)
        self.setStyleSheet(self.base_style)

        if self.product["image_path"]:
            path = "image\\" + self.product["image_path"]
            pix = QPixmap(path)
        else:
            pix = QPixmap("image\\default.png")
        self.ui.label_image.setPixmap(pix.scaled(150, 150))

    def mousePressEvent(self, a0):
        main = self.window()
        main.select_widget(self)
