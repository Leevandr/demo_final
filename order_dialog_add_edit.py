from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QMessageBox

from db import dao
from gen.order_dialog import Ui_OrderDialog


class AddEditOrderDialog(QWidget):
    def __init__(self, order=None, on_save=None):
        super().__init__()
        self.ui = Ui_OrderDialog()
        self.ui.setupUi(self)
        self.order = order
        self.on_save = on_save

        for p in dao.get_all_products():
            self.ui.productComboBox.addItem(f"{p['article']} — {p['product_name']}", p["product_id"])
        for s in dao.get_all_statuses():
            self.ui.statusComboBox.addItem(s["status_name"], s["status_id"])
        for pp in dao.get_all_pickup_points():
            self.ui.pickup_pointComboBox.addItem(pp["address"], pp["pickup_point_id"])
        for u in dao.get_all_users():
            self.ui.usersComboBox.addItem(u["full_name"], u["user_id"])

        self.ui.orderdateDateEdit.setDate(QDate.currentDate())
        self.ui.deliverydateDateEdit.setDate(QDate.currentDate())

        if order:
            self.setWindowTitle("Редактирование заказа")
            for combo, key in [
                (self.ui.productComboBox,      "product_id"),
                (self.ui.statusComboBox,       "status_id"),
                (self.ui.pickup_pointComboBox, "pickup_point_id"),
                (self.ui.usersComboBox,        "user_id"),
            ]:
                idx = combo.findData(order.get(key))
                if idx >= 0:
                    combo.setCurrentIndex(idx)
            for date_edit, key in [
                (self.ui.orderdateDateEdit,    "order_date"),
                (self.ui.deliverydateDateEdit, "delivery_date"),
            ]:
                d = order.get(key)
                if d:
                    date_edit.setDate(QDate(d.year, d.month, d.day))

        self.ui.pushButton_save.setStyleSheet("background-color: #00FA9A; color: black;")

        from PyQt6.QtWidgets import QPushButton
        self._btn_back = QPushButton("Назад")
        self._btn_back.clicked.connect(self.close)
        self.ui.formLayout.addRow("", self._btn_back)

        self.ui.pushButton_save.clicked.connect(self._save)

    def _save(self):
        product_id      = self.ui.productComboBox.currentData()
        status_id       = self.ui.statusComboBox.currentData()
        pickup_point_id = self.ui.pickup_pointComboBox.currentData()
        user_id         = self.ui.usersComboBox.currentData()
        order_date      = self.ui.orderdateDateEdit.date().toPyDate()
        delivery_date   = self.ui.deliverydateDateEdit.date().toPyDate()
        try:
            if self.order:
                dao.update_order(self.order["order_id"], product_id, status_id,
                                 pickup_point_id, order_date, delivery_date, user_id)
            else:
                dao.add_order(product_id, status_id, pickup_point_id, order_date, delivery_date, user_id)
            if self.on_save:
                self.on_save()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные. Проверьте заполнение полей.\n{e}")
