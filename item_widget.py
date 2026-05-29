from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QWidget

from gen.ItemWidget import Ui_ItemWidget


class ItemWidget(QWidget):
    def __init__(self, product):
        super().__init__()
        self.ui = Ui_ItemWidget()
        self.ui.setupUi(self)
        self.product = product
        self._selected = False
        self.fill_items()

    def fill_items(self):
        discount = self.product["discount"] or 0
        price = self.product["price"] or 0

        self.ui.label_category.setText(f"{self.product['category_name']} |")
        self.ui.label_title.setText(f"<b>Название: {self.product['product_name']}</b>")
        self.ui.label_manufacture.setText(f"Производитель: {self.product['manufacture_name']}")
        self.ui.label_supplier.setText(f"Поставщик: {self.product['supplier_name']}")
        self.ui.label_description.setText(f"Описание: {self.product['descrip']}")
        self.ui.label_unit.setText(f"Ед. изм.: {self.product['unit_name']}")
        self.ui.label_quantity.setText(f"Остаток: {self.product['quantity']} шт.")
        self.ui.label_discount.setText(f"<b>Скидка: {discount}%</b>")

        if discount > 0:
            final = round(price * (1 - discount / 100), 2)
            self.ui.label_price.setText(
                f"<font color='red'><s>{price:.2f}</s></font><br>{final:.2f} руб."
            )
        else:
            self.ui.label_price.setText(f"{price:.2f} руб.")

        self.ui.frame_discount.setStyleSheet(self._bg())

        pix = QPixmap("image\\" + self.product["image_path"]) if self.product["image_path"] else QPixmap("image\\default.png")
        self.ui.label_image.setPixmap(pix.scaled(150, 150))

        # шрифт наследуется от приложения, установлен в main.py
        font = QFont("Times New Roman", 11)
        for lbl in [self.ui.label_category, self.ui.label_title, self.ui.label_manufacture,
                    self.ui.label_supplier, self.ui.label_description, self.ui.label_unit,
                    self.ui.label_quantity, self.ui.label_discount, self.ui.label_price]:
            lbl.setFont(font)

    def _bg(self):
        # цвет фона карточки зависит от скидки и наличия товара
        discount = self.product["discount"] or 0
        if discount > 15:
            return "background-color: #2E8B57;"
        elif self.product["quantity"] == 0:
            return "background-color: #ADD8E6;"
        return ""

    def set_selected(self, selected: bool):
        if selected:
            self.ui.frame_info.setStyleSheet("QFrame#frame_info { border: 2px solid #8bbfff; }")
            self.ui.frame_discount.setStyleSheet(f"QFrame#frame_discount {{ border: 2px solid #8bbfff; {self._bg()} }}")
        else:
            self.ui.frame_info.setStyleSheet("")
            self.ui.frame_discount.setStyleSheet(self._bg())

    def mousePressEvent(self, a0):
        self.window().select_widget(self)

    def mouseDoubleClickEvent(self, event):
        # двойной клик на карточке товара открывает диалог редактирования
        self.window().select_widget(self)
        self.window().edit_product()
