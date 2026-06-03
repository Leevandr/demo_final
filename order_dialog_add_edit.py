from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QDialog, QFormLayout,
    QComboBox, QSpinBox, QDialogButtonBox, QLabel,
    QTableWidgetItem
)

from db import dao
from gen.order_dialog import Ui_OrderDialog


class AddEditOrderDialog(QWidget):
    def __init__(self, order=None, on_save=None):
        super().__init__()
        self.ui = Ui_OrderDialog()
        self.ui.setupUi(self)
        self.order = order
        self.on_save = on_save

        # список товаров в памяти: [{product_id, article, name, quantity, price, item_id}]
        self._items = []

        self._load_combos()
        self.ui.orderdateDateEdit.setDate(QDate.currentDate())
        self.ui.deliverydateDateEdit.setDate(QDate.currentDate())

        if order:
            self.setWindowTitle("Редактирование заказа")
            self._fill_order_fields()
            self._load_existing_items()

        self.ui.pushButton_save.setStyleSheet("background-color: #00FA9A; color: black;")
        self.ui.pushButton_save.clicked.connect(self._save)
        self.ui.pushButton_cancel.clicked.connect(self.close)
        self.ui.pushButton_add_item.clicked.connect(self._add_item)
        self.ui.pushButton_edit_qty.clicked.connect(self._edit_qty)
        self.ui.pushButton_del_item.clicked.connect(self._del_item)

    def _load_combos(self):
        for s in dao.get_all_statuses():
            self.ui.statusComboBox.addItem(s["status_name"], s["status_id"])
        for pp in dao.get_all_pickup_points():
            self.ui.pickup_pointComboBox.addItem(pp["address"], pp["pickup_point_id"])
        for u in dao.get_all_users():
            self.ui.usersComboBox.addItem(u["full_name"], u["user_id"])

    def _fill_order_fields(self):
        for combo, key in [
            (self.ui.statusComboBox,       "status_id"),
            (self.ui.pickup_pointComboBox, "pickup_point_id"),
            (self.ui.usersComboBox,        "user_id"),
        ]:
            idx = combo.findData(self.order.get(key))
            if idx >= 0:
                combo.setCurrentIndex(idx)
        for date_edit, key in [
            (self.ui.orderdateDateEdit,    "order_date"),
            (self.ui.deliverydateDateEdit, "delivery_date"),
        ]:
            d = self.order.get(key)
            if d:
                date_edit.setDate(QDate(d.year, d.month, d.day))

    def _load_existing_items(self):
        rows = dao.get_order_items(self.order["order_id"])
        for r in rows:
            self._items.append({
                "item_id":    r["item_id"],
                "product_id": r["product_id"],
                "article":    r["article"],
                "name":       r["product_name"],
                "quantity":   r["quantity"],
                "price":      float(r["price"]),
            })
        self._refresh_table()

    def _refresh_table(self):
        self.ui.tableWidget.setRowCount(0)
        total = 0.0
        for i, item in enumerate(self._items):
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            subtotal = item["quantity"] * item["price"]
            total += subtotal
            for col, val in enumerate([
                str(i + 1),
                item["article"],
                item["name"],
                str(item["quantity"]),
                f"{item['price']:.2f}",
                f"{subtotal:.2f}",
            ]):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(val))

        # строка итого
        row = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setItem(row, 4, QTableWidgetItem("ИТОГО:"))
        self.ui.tableWidget.setItem(row, 5, QTableWidgetItem(f"{total:.2f} руб."))

    def _add_item(self):
        products = dao.get_all_products()
        if not products:
            QMessageBox.warning(self, "Предупреждение", "Нет доступных товаров.")
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("Добавить товар")
        layout = QFormLayout(dlg)

        combo = QComboBox()
        for p in products:
            combo.addItem(f"{p['article']} — {p['product_name']}", p)
        layout.addRow(QLabel("Товар:"), combo)

        spin = QSpinBox()
        spin.setMinimum(1)
        spin.setMaximum(9999)
        spin.setValue(1)
        layout.addRow(QLabel("Количество:"), spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addRow(buttons)

        if dlg.exec() == QDialog.DialogCode.Accepted:
            product = combo.currentData()
            self._items.append({
                "item_id":    None,
                "product_id": product["product_id"],
                "article":    product["article"],
                "name":       product["product_name"],
                "quantity":   spin.value(),
                "price":      float(product["price"] or 0),
            })
            self._refresh_table()

    def _edit_qty(self):
        row = self.ui.tableWidget.currentRow()
        # последняя строка — итого, её не редактируем
        if row < 0 or row >= len(self._items):
            QMessageBox.warning(self, "Предупреждение", "Выберите товар для изменения количества.")
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("Изменить количество")
        layout = QFormLayout(dlg)

        spin = QSpinBox()
        spin.setMinimum(1)
        spin.setMaximum(9999)
        spin.setValue(self._items[row]["quantity"])
        layout.addRow(QLabel("Количество:"), spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addRow(buttons)

        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._items[row]["quantity"] = spin.value()
            self._refresh_table()

    def _del_item(self):
        row = self.ui.tableWidget.currentRow()
        if row < 0 or row >= len(self._items):
            QMessageBox.warning(self, "Предупреждение", "Выберите товар для удаления.")
            return
        self._items.pop(row)
        self._refresh_table()

    def _save(self):
        if not self._items:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один товар в заказ.")
            return

        status_id       = self.ui.statusComboBox.currentData()
        pickup_point_id = self.ui.pickup_pointComboBox.currentData()
        user_id         = self.ui.usersComboBox.currentData()
        order_date      = self.ui.orderdateDateEdit.date().toPyDate()
        delivery_date   = self.ui.deliverydateDateEdit.date().toPyDate()

        try:
            if self.order:
                dao.update_order(self.order["order_id"], status_id,
                                 pickup_point_id, order_date, delivery_date, user_id)
                # удаляем старые позиции и сохраняем новые
                dao.delete_order_items(self.order["order_id"])
                for item in self._items:
                    dao.add_order_item(
                        self.order["order_id"],
                        item["product_id"],
                        item["quantity"],
                        item["price"],
                    )
            else:
                order_id = dao.add_order(status_id, pickup_point_id,
                                         order_date, delivery_date, user_id)
                for item in self._items:
                    dao.add_order_item(
                        order_id,
                        item["product_id"],
                        item["quantity"],
                        item["price"],
                    )

            if self.on_save:
                self.on_save()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные.\n{e}")
