import shutil
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox

from src.db import dao
from src.widgets.ItemWidget import image_path
from ui.gen.ItemDialog import Ui_ItemDialog

IMAGE_WIDTH = 300
IMAGE_HEIGHT = 200


class ItemDialog(QDialog):
    def __init__(self, item=None):
        super().__init__()
        self.ui = Ui_ItemDialog()
        self.ui.setupUi(self)
        self.item = item
        self.image_name = "img.png"
        self.fill()
        if self.item and self.item["image"] and self.item["image"] != "None":
            self.image_name = self.item["image"]
        if self.item:
            self.fill_exist()

        self.ui.pushButton_save.clicked.connect(self.save)
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
        pixmap = QPixmap(str(src))
        if pixmap.isNull():
            if src.resolve() != dst.resolve():
                shutil.copy(src, dst)
        else:
            pixmap = pixmap.scaled(
                IMAGE_WIDTH,
                IMAGE_HEIGHT,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            pixmap.save(str(dst))

        self.image_name = src.name

        pixmap = QPixmap(str(dst)).scaled(
            IMAGE_WIDTH,
            IMAGE_HEIGHT,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.ui.label.setPixmap(pixmap)

    def fill_exist(self):
        item = self.item
        self.ui.categoryComboBox.setCurrentText(item["category"])
        self.ui.manufactureComboBox.setCurrentText(item["manufacture"])
        self.ui.suppilerComboBox.setCurrentText(item["suppiler"])
        self.ui.unitComboBox.setCurrentText(item["unit"])

        self.ui.spinBox.setValue(int(item["article"]) if str(item["article"]).isdigit() else 0)
        self.ui.titleLineEdit.setText(item["title"])
        self.ui.descriptionLineEdit.setText(item["description"])
        self.ui.priceSpinBox.setValue(int(item["price"]))
        self.ui.spinBox_quantity.setValue(int(item["quantity"]))
        self.ui.discountDoubleSpinBox.setValue(float(item["discount"]))

        image_name = self.image_name or "img.png"
        pixmap = QPixmap(image_path(image_name))
        if pixmap.isNull():
            pixmap = QPixmap(image_path("img.png"))

        pixmap = pixmap.scaled(IMAGE_WIDTH, IMAGE_HEIGHT, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.label.setPixmap(pixmap)

    def fill(self):
        categories = dao.get_all_categories()
        for category in categories:
            self.ui.categoryComboBox.addItem(category["title"], category["id"])
        suppilers = dao.get_all_suppilers()
        for suppiler in suppilers:
            self.ui.suppilerComboBox.addItem(suppiler["title"], suppiler["id"])
        manufactures = dao.get_all_manufactures()
        for manufacture in manufactures:
            self.ui.manufactureComboBox.addItem(manufacture["title"], manufacture["id"])
        units = dao.get_all_units()
        for unit in units:
            self.ui.unitComboBox.addItem(unit["title"], unit["id"])

    def save(self):
        article = self.ui.spinBox.value()
        title = self.ui.titleLineEdit.text()
        description = self.ui.descriptionLineEdit.text()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название товара")
            return

        category_id = self.ui.categoryComboBox.currentData()
        manufacture_id = self.ui.manufactureComboBox.currentData()
        suppiler_id = self.ui.suppilerComboBox.currentData()
        unit_id = self.ui.unitComboBox.currentData()
        discount = self.ui.discountDoubleSpinBox.value()
        quantity = self.ui.spinBox_quantity.value()
        image = self.image_name or "img.png"
        price = self.ui.priceSpinBox.value()

        if self.item:
            product_id = self.item["id"]
            dao.edit_product(product_id,
                             article,
                             title,
                             category_id,
                             description,
                             manufacture_id,
                             suppiler_id,
                             price,
                             unit_id,
                             quantity,
                             discount,
                             image)
        else:
            dao.add_new_product(article,
                                title,
                                category_id,
                                description,
                                manufacture_id,
                                suppiler_id,
                                price,
                                unit_id,
                                quantity,
                                discount,
                                image)

        self.accept()
