from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QMessageBox

from db import dao
from gen.order_dialog import Ui_OrderDialog


class OrderDialogCtrl(QWidget):
    def __init__(self, order=None, on_save=None):
        super().__init__()
        self.ui = Ui_OrderDialog()
        self.ui.setupUi(self)
        self.order = order
        self.on_save = on_save

        self._fill_combos()
        if order:
            self.setWindowTitle("Редактирование заказа")
            self._fill_fields()

        self.ui.pushButton_save.clicked.connect(self._save)

    def _fill_combos(self):
        for p in dao.get_all_products():
            self.ui.productComboBox.addItem(
                f"{p['article']} — {p['product_name']}", p["product_id"]
            )
        for s in dao.get_all_statuses():
            self.ui.statusComboBox.addItem(s["status_name"], s["status_id"])
        for pp in dao.get_all_pickup_points():
            self.ui.pickup_pointComboBox.addItem(pp["address"], pp["pickup_point_id"])
        for u in dao.get_all_users():
            self.ui.usersComboBox.addItem(u["full_name"], u["user_id"])

        self.ui.orderdateDateEdit.setDate(QDate.currentDate())
        self.ui.deliverydateDateEdit.setDate(QDate.currentDate())

    def _fill_fields(self):
        o = self.order
        idx = self.ui.productComboBox.findData(o.get("product_id"))
        if idx >= 0:
            self.ui.productComboBox.setCurrentIndex(idx)
        idx = self.ui.statusComboBox.findData(o.get("status_id"))
        if idx >= 0:
            self.ui.statusComboBox.setCurrentIndex(idx)
        idx = self.ui.pickup_pointComboBox.findData(o.get("pickup_point_id"))
        if idx >= 0:
            self.ui.pickup_pointComboBox.setCurrentIndex(idx)
        idx = self.ui.usersComboBox.findData(o.get("user_id"))
        if idx >= 0:
            self.ui.usersComboBox.setCurrentIndex(idx)

        if o.get("order_date"):
            d = o["order_date"]
            self.ui.orderdateDateEdit.setDate(QDate(d.year, d.month, d.day))
        if o.get("delivery_date"):
            d = o["delivery_date"]
            self.ui.deliverydateDateEdit.setDate(QDate(d.year, d.month, d.day))

    def _save(self):
        product_id = self.ui.productComboBox.currentData()
        status_id = self.ui.statusComboBox.currentData()
        pickup_point_id = self.ui.pickup_pointComboBox.currentData()
        user_id = self.ui.usersComboBox.currentData()
        order_date = self.ui.orderdateDateEdit.date().toPyDate()
        delivery_date = self.ui.deliverydateDateEdit.date().toPyDate()

        try:
            if self.order:
                dao.update_order(
                    self.order["order_id"], product_id, status_id,
                    pickup_point_id, order_date, delivery_date, user_id
                )
            else:
                dao.add_order(product_id, status_id, pickup_point_id, order_date, delivery_date, user_id)
            if self.on_save:
                self.on_save()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные. Проверьте заполнение полей.\n{e}")
