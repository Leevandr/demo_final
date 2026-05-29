import os
import shutil

from PyQt6.QtWidgets import QWidget, QMessageBox, QFileDialog

from db import dao
from gen.add_product_window import Ui_ProductDialog


class ProductDialog(QWidget):
    def __init__(self, product=None, on_save=None):
        super().__init__()
        self.ui = Ui_ProductDialog()
        self.ui.setupUi(self)
        self.product = product
        self.on_save = on_save
        self._chosen_image_path = None

        self._fill_combos()
        if product:
            self.setWindowTitle("Редактирование товара")
            self._fill_fields()

        self.ui.pushButton_image.clicked.connect(self._choose_image)
        self.ui.pushButton_save.clicked.connect(self._save)

    def _fill_combos(self):
        for cat in dao.get_all_categories():
            self.ui.categoryComboBox.addItem(cat["category_name"], cat["category_id"])
        for m in dao.get_all_manufactures():
            self.ui.manufacturerComboBox.addItem(m["manufacture_name"], m["manufacture_id"])
        for s in dao.get_all_suppliers():
            self.ui.supplierComboBox.addItem(s["supplier_name"], s["supplier_id"])
        for u in dao.get_all_units():
            self.ui.unitComboBox.addItem(u["unit_name"], u["unit_id"])

    def _fill_fields(self):
        p = self.product
        self.ui.articleLineEdit.setText(str(p.get("article") or ""))
        self.ui.product_nameLineEdit.setText(str(p.get("product_name") or ""))
        self.ui.descriptionLineEdit.setText(str(p.get("descrip") or ""))
        self.ui.priceDoubleSpinBox.setValue(float(p.get("price") or 0))
        self.ui.quantityDoubleSpinBox.setValue(float(p.get("quantity") or 0))
        self.ui.discountDoubleSpinBox.setValue(float(p.get("discount") or 0))

        idx = self.ui.categoryComboBox.findData(p.get("category_id"))
        if idx >= 0:
            self.ui.categoryComboBox.setCurrentIndex(idx)
        idx = self.ui.manufacturerComboBox.findData(p.get("manufacture_id"))
        if idx >= 0:
            self.ui.manufacturerComboBox.setCurrentIndex(idx)
        idx = self.ui.supplierComboBox.findData(p.get("supplier_id"))
        if idx >= 0:
            self.ui.supplierComboBox.setCurrentIndex(idx)
        idx = self.ui.unitComboBox.findData(p.get("unit_id"))
        if idx >= 0:
            self.ui.unitComboBox.setCurrentIndex(idx)

        if p.get("image_path"):
            self.ui.image_pathLineEdit.setText(p["image_path"])

    def _choose_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            self._chosen_image_path = path
            self.ui.image_pathLineEdit.setText(os.path.basename(path))

    def _save(self):
        name = self.ui.product_nameLineEdit.text().strip()
        article = self.ui.articleLineEdit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Не удалось сохранить данные. Проверьте заполнение полей.")
            return

        category_id = self.ui.categoryComboBox.currentData()
        manufacture_id = self.ui.manufacturerComboBox.currentData()
        supplier_id = self.ui.supplierComboBox.currentData()
        unit_id = self.ui.unitComboBox.currentData()
        descrip = self.ui.descriptionLineEdit.text().strip()
        price = self.ui.priceDoubleSpinBox.value()
        quantity = int(self.ui.quantityDoubleSpinBox.value())
        discount = self.ui.discountDoubleSpinBox.value()

        image_path = self.ui.image_pathLineEdit.text().strip() or None
        if self._chosen_image_path:
            from PyQt6.QtGui import QPixmap
            filename = os.path.basename(self._chosen_image_path)
            dest = os.path.join("image", filename)
            if not os.path.exists("image"):
                os.makedirs("image")
            pix = QPixmap(self._chosen_image_path).scaled(300, 200)
            pix.save(dest)
            if self.product and self.product.get("image_path"):
                old = os.path.join("image", self.product["image_path"])
                if os.path.exists(old) and os.path.abspath(old) != os.path.abspath(dest):
                    os.remove(old)
            image_path = filename

        try:
            if self.product:
                dao.update_product(
                    self.product["product_id"], article, name, category_id, descrip,
                    manufacture_id, supplier_id, price, unit_id, quantity, discount, image_path
                )
            else:
                dao.add_product(
                    article, name, category_id, descrip, manufacture_id,
                    supplier_id, price, unit_id, quantity, discount, image_path
                )
            if self.on_save:
                self.on_save()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные. Проверьте заполнение полей.\n{e}")
