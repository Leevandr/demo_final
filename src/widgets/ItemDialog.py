import shutil
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QFileDialog, QLabel, QLineEdit, QMessageBox

from src.db import dao
from src.widgets.ItemWidget import image_path
from ui.gen.ItemDialog import Ui_ItemDialog

IMAGE_WIDTH = 300
IMAGE_HEIGHT = 200
PROTECTED_IMAGES = {"img.png", "logo.png", "app_icon.png"}


def images_dir():
    project_dir = Path(__file__).resolve().parents[2]
    path = project_dir / "resources" / "images"
    path.mkdir(parents=True, exist_ok=True)
    return path


def normalized_image_name(value):
    if not value or value == "None":
        return "img.png"
    return str(value)


class ItemDialog(QDialog):
    def __init__(self, item=None):
        super().__init__()
        self.ui = Ui_ItemDialog()
        self.ui.setupUi(self)
        self.item = item
        self.image_name = "img.png"
        self.setup_id_field()
        self.setup_limits()
        self.fill()
        if self.item and self.item["image"] and self.item["image"] != "None":
            self.image_name = self.item["image"]
        if self.item:
            self.fill_exist()
            self.setWindowTitle("Редактирование товара")
        else:
            self.id_label.hide()
            self.id_line_edit.hide()
            self.show_image("img.png")
            self.setWindowTitle("Добавление товара")

        self.ui.pushButton_save.clicked.connect(self.save)
        self.ui.pushButton_image.clicked.connect(self.choose_image)

    def setup_id_field(self):
        self.id_label = QLabel("ID")
        self.id_line_edit = QLineEdit()
        self.id_line_edit.setReadOnly(True)
        self.ui.formLayout.insertRow(0, self.id_label, self.id_line_edit)

    def setup_limits(self):
        self.ui.priceSpinBox.setDecimals(2)
        self.ui.priceSpinBox.setMinimum(0)
        self.ui.priceSpinBox.setMaximum(990000)
        self.ui.discountDoubleSpinBox.setDecimals(2)
        self.ui.discountDoubleSpinBox.setMinimum(0)
        self.ui.discountDoubleSpinBox.setMaximum(100)
        self.ui.spinBox_quantity.setMinimum(0)

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

        dst = self.unique_destination(src)
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

        self.image_name = dst.name
        self.show_image(self.image_name)

    def unique_destination(self, src):
        dst = images_dir() / src.name
        try:
            if dst.exists() and src.resolve() == dst.resolve():
                return dst
        except OSError:
            pass

        if not dst.exists():
            return dst

        index = 1
        while True:
            candidate = dst.with_name(f"{src.stem}_{index}{src.suffix}")
            if not candidate.exists():
                return candidate
            index += 1

    def show_image(self, image_name):
        pixmap = QPixmap(image_path(normalized_image_name(image_name)))
        if pixmap.isNull():
            pixmap = QPixmap(image_path("img.png"))

        pixmap = pixmap.scaled(
            IMAGE_WIDTH,
            IMAGE_HEIGHT,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.ui.label.setPixmap(pixmap)

    def fill_exist(self):
        item = self.item
        self.id_line_edit.setText(str(item["id"]))
        self.ui.categoryComboBox.setCurrentText(item["category"])
        self.ui.manufactureComboBox.setCurrentText(item["manufacture"])
        self.ui.suppilerComboBox.setCurrentText(item["suppiler"])
        self.ui.unitComboBox.setCurrentText(item["unit"])

        self.ui.articleLineEdit.setText(str(item["article"]))
        self.ui.titleLineEdit.setText(item["title"])
        self.ui.descriptionLineEdit.setText(item["description"])
        self.ui.priceSpinBox.setValue(float(item["price"]))
        self.ui.spinBox_quantity.setValue(int(item["quantity"]))
        self.ui.discountDoubleSpinBox.setValue(float(item["discount"]))
        self.show_image(self.image_name)

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
        article = self.ui.articleLineEdit.text().strip()
        title = self.ui.titleLineEdit.text().strip()
        description = self.ui.descriptionLineEdit.text().strip()

        if not article:
            QMessageBox.warning(self, "Ошибка", "Введите артикул товара")
            return
        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название товара")
            return
        if not description:
            QMessageBox.warning(self, "Ошибка", "Введите описание товара")
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
            old_image = normalized_image_name(self.item["image"])
            saved = dao.edit_product(product_id,
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
            if saved:
                self.remove_old_image(old_image, normalized_image_name(image))
        else:
            saved = dao.add_new_product(article,
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

        if not saved:
            QMessageBox.warning(
                self,
                "Ошибка сохранения",
                "Проверьте артикул и заполненные данные. Возможно, товар с таким артикулом уже существует."
            )
            return

        self.accept()

    def remove_old_image(self, old_image, new_image):
        if old_image == new_image or old_image in PROTECTED_IMAGES:
            return
        if dao.get_image_usage_count(old_image) > 0:
            return

        path = images_dir() / old_image
        if path.exists():
            path.unlink()
