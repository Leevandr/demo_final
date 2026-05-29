from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from gen.ItemWidget import Ui_ItemWidget


class ItemWidget(QWidget):
    def __init__(self, product):
        super().__init__()
        self.ui = Ui_ItemWidget()
        self.ui.setupUi(self)
        self.product = product
        self.base_style = ""
        self.fill_items()

    def fill_items(self):
        self.ui.label_title.setText(f"<b>{self.product['product_name']}</b>")
        self.ui.label_category.setText(f"{self.product['category_name']} |")
        self.ui.label_unit.setText(f"Единица измерения: {self.product['unit_name']}")
        self.ui.label_quantity.setText(f"Количество: {self.product['quantity']}")
        self.ui.label_manufacture.setText(f"Производитель: {self.product['manufacture_name']}")
        self.ui.label_description.setText(f"Описание: {self.product['descrip']}")
        self.ui.label_supplier.setText(f"Поставщик: {self.product['supplier_name']}")

        discount = self.product["discount"] or 0
        price = self.product["price"] or 0
        self.ui.label_discount.setText(f"Скидка: {discount}%")

        if discount > 0:
            final_price = round(price * (1 - discount / 100), 2)
            self.ui.label_price.setText(
                f"<s><font color='red'>{price}</font></s> {final_price} руб."
            )
        else:
            self.ui.label_price.setText(f"{price} руб.")

        if discount > 15:
            self.base_style = "background-color: #2E8B57;"
        elif self.product["quantity"] == 0:
            self.base_style = "background-color: #ADD8E6;"
        else:
            self.base_style = ""

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
