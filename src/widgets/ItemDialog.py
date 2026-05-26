import shutil
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QFileDialog

from src.db import dao
from src.widgets.ItemWidget import image_path
from ui.gen.ItemDialog import Ui_ItemDialog


class ItemDialog(QDialog):
    def __init__(self, item=None):
        super().__init__()
        self.ui = Ui_ItemDialog()
        self.ui.setupUi(self)
        self.item = None
        self.fill()
        if item:
            self.item = item
            self.fill_exist()

        self.ui.pushButton_save.clicked.connect(self.save)
        self.image_name = None
        self.ui.pushButton_image.clicked.connect(self.choose_image)

    def choose_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать изображение",
            "",
            "Картинки (*.png *.jpg *.jpeg)"
        )
        if not file_path:
            return
        src = Path(file_path)

        project_dir = Path(__file__).resolve().parents[2]
        images_dir = project_dir / "resources" / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        dst = images_dir / src.name
        if src.resolve() != dst.resolve():
            shutil.copy(src, dst)

        self.image_name = src.name

        pixmap = QPixmap(str(dst)).scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.label.setPixmap(pixmap)

    def fill_exist(self):
        item = self.item
        self.ui.categoryComboBox.setCurrentText(item["category"])
        self.ui.manufactureComboBox.setCurrentText(item["manufacture"])
        self.ui.suppilerComboBox.setCurrentText(item["suppiler"])
        self.ui.unitComboBox.setCurrentText(item["unit"])

        self.ui.spinBox.setValue(int(item["article"]))
        self.ui.titleLineEdit.setText(item["title"])
        self.ui.descriptionLineEdit.setText(item["description"])
        self.ui.priceSpinBox.setValue(int(item["price"]))
        self.ui.spinBox_quantity.setValue(int(item["quantity"]))
        self.ui.discountDoubleSpinBox.setValue(float(item["discount"]))

        image_name = item["image"] or "img.png"
        pixmap = QPixmap(image_path(image_name))
        if pixmap.isNull():
            pixmap = QPixmap(image_path("img.png"))

        pixmap = pixmap.scaled(150,150, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.label.setPixmap(pixmap)


    def fill(self):
        categories = dao.get_all_categories()
        for category in categories:
            self.ui.categoryComboBox.addItem(category["title"])
        suppilers = dao.get_all_suppilers()
        for suppiler in suppilers:
            self.ui.suppilerComboBox.addItem(suppiler["title"])
        manufactures = dao.get_all_manufactures()
        for manufacture in manufactures:
            self.ui.manufactureComboBox.addItem(manufacture["title"])
        units = dao.get_all_units()
        for unit in units:
            self.ui.unitComboBox.addItem(unit["title"])

    def save(self):

        article = self.ui.spinBox.value()
        title = self.ui.titleLineEdit.text()
        description = self.ui.descriptionLineEdit.text()

        category = self.ui.categoryComboBox.currentText()
        category_id = dao.get_category_id(category)["id"]

        manufacture = self.ui.manufactureComboBox.currentText()
        manufacture_id = dao.get_manufacture_id(manufacture)["id"]

        suppiler = self.ui.suppilerComboBox.currentText()
        suppiler_id = dao.get_suppiler_id(suppiler)["id"]

        unit = self.ui.unitComboBox.currentText()
        unit_id = dao.get_unit_id(unit)["id"]

        discount = self.ui.discountDoubleSpinBox.value()
        quantity = self.ui.spinBox_quantity.value()
        image = self.image_name
        price = str(self.ui.priceSpinBox.text())

        if self.item:
            product_id = self.item["id"]
            dao.edit_product(product_id,
                             str(article),
                             str(title),
                             str(category_id),
                             str(description),
                             str(manufacture_id),
                             str(suppiler_id),
                             str(price),
                             str(unit_id),
                             str(quantity),
                             str(discount),
                             str(image))
        else:
            dao.add_new_product(str(article),
                                str(title),
                                str(category_id),
                                str(description),
                                str(manufacture_id),
                                str(suppiler_id),
                                str(price),
                                str(unit_id),
                                str(quantity),
                                str(discount),
                                str(image))

        self.accept()
