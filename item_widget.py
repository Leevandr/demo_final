from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from gen.ItemWidget import Ui_ItemWidget


class ItemWidget(QWidget):
    def __init__(self, product):
        super().__init__()
        self.ui = Ui_ItemWidget()
        self.ui.setupUi(self)
        self.product = product
        self.fill_items()

    def fill_items(self):
        self.ui.label_title.setText(str(f"<font size=10>{self.product["product_name"]}</font>"))
        self.ui.label_category.setText(str(f"<font size=10>{self.product["category_name"]} |</font>"))

        self.ui.label_unit.setText(str(f"Единица измерения: {self.product["unit_name"]}"))
        self.ui.label_quantity.setText(str(f"Количество: {self.product["quantity"]}"))
        self.ui.label_manufacture.setText(str(f"Производитель: {self.product["manufacture_name"]}"))
        self.ui.label_description.setText(str(f"Описание: {self.product["descrip"]}"))
        self.ui.label_supplier.setText(str(f"Поставщик: {self.product["supplier_name"]}"))
        self.ui.label_discount.setText(str(f"Скидка: {self.product["discount"]}"))

        if self.product["discount"] > 15:
            price_do = ((((100 - self.product["discount"])/100) * self.product["price"]) / self.product["discount"]) + self.product["price"]
            self.ui.label_price.setText(str(f"Цена до скидки: <s> {round(price_do, 2)} </s> <br>"
                                            f"<font color='red'>Цена после скидки: {self.product["price"]} </font>"))
        else:
            self.ui.label_price.setText(str(f"Цена до скидки: {self.product["price"]}"))

        if self.product["image_path"]:
            path = "image\\" + self.product["image_path"]
            pix = QPixmap(path).scaled(150, 150)
        else:
            path = "image\\default.png"
            pix = QPixmap(path).scaled(150, 150)
        self.ui.label_image.setPixmap(pix)

    def mousePressEvent(self, a0):
        main = self.window()
        main.select_widget(self)
