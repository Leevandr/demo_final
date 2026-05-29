import os


from PyQt6.QtGui import QPixmap
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

        for cat in dao.get_all_categories():
            self.ui.categoryComboBox.addItem(cat["category_name"], cat["category_id"])
        for m in dao.get_all_manufactures():
            self.ui.manufacturerComboBox.addItem(m["manufacture_name"], m["manufacture_id"])
        for s in dao.get_all_suppliers():
            self.ui.supplierComboBox.addItem(s["supplier_name"], s["supplier_id"])
        for u in dao.get_all_units():
            self.ui.unitComboBox.addItem(u["unit_name"], u["unit_id"])

        if product:
            # режим редактирования — заполняем поля текущими значениями
            self.setWindowTitle("Редактирование товара")
            self.ui.articleLineEdit.setText(str(product.get("article") or ""))
            self.ui.product_nameLineEdit.setText(str(product.get("product_name") or ""))
            self.ui.descriptionLineEdit.setText(str(product.get("descrip") or ""))
            self.ui.priceDoubleSpinBox.setValue(float(product.get("price") or 0))
            self.ui.quantityDoubleSpinBox.setValue(float(product.get("quantity") or 0))
            self.ui.discountDoubleSpinBox.setValue(float(product.get("discount") or 0))
            for combo, key in [
                (self.ui.categoryComboBox,    "category_id"),
                (self.ui.manufacturerComboBox,"manufacture_id"),
                (self.ui.supplierComboBox,    "supplier_id"),
                (self.ui.unitComboBox,        "unit_id"),
            ]:
                idx = combo.findData(product.get(key))
                if idx >= 0:
                    combo.setCurrentIndex(idx)
            if product.get("image_path"):
                self.ui.image_pathLineEdit.setText(product["image_path"])

        self.ui.pushButton_save.setStyleSheet("background-color: #00FA9A; color: black;")

        from PyQt6.QtWidgets import QPushButton
        self._btn_back = QPushButton("Назад")
        self._btn_back.clicked.connect(self.close)
        self.ui.formLayout.addRow("", self._btn_back)

        self.ui.pushButton_image.clicked.connect(self._choose_image)
        self.ui.pushButton_save.clicked.connect(self._save)

    def _choose_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            self._chosen_image_path = path
            self.ui.image_pathLineEdit.setText(os.path.basename(path))

    def _save(self):
        name = self.ui.product_nameLineEdit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Не удалось сохранить данные. Проверьте заполнение полей.")
            return

        article      = self.ui.articleLineEdit.text().strip()
        category_id  = self.ui.categoryComboBox.currentData()
        manufacture_id = self.ui.manufacturerComboBox.currentData()
        supplier_id  = self.ui.supplierComboBox.currentData()
        unit_id      = self.ui.unitComboBox.currentData()
        descrip      = self.ui.descriptionLineEdit.text().strip()
        price        = self.ui.priceDoubleSpinBox.value()
        quantity     = int(self.ui.quantityDoubleSpinBox.value())
        discount     = self.ui.discountDoubleSpinBox.value()
        image_path   = self.ui.image_pathLineEdit.text().strip() or None

        if self._chosen_image_path:
            # копируем изображение в папку приложения и сохраняем только имя файла
            filename = os.path.basename(self._chosen_image_path)
            dest = os.path.join("image", filename)
            os.makedirs("image", exist_ok=True)
            QPixmap(self._chosen_image_path).scaled(300, 200).save(dest)
            if self.product and self.product.get("image_path"):
                old = os.path.join("image", self.product["image_path"])
                if os.path.exists(old) and os.path.abspath(old) != os.path.abspath(dest):
                    os.remove(old)
            image_path = filename

        try:
            if self.product:
                dao.update_product(self.product["product_id"], article, name, category_id,
                                   descrip, manufacture_id, supplier_id, price,
                                   unit_id, quantity, discount, image_path)
            else:
                dao.add_product(article, name, category_id, descrip, manufacture_id,
                                supplier_id, price, unit_id, quantity, discount, image_path)
            if self.on_save:
                self.on_save()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные. Проверьте заполнение полей.\n{e}")
