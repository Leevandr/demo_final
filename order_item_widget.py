from PyQt6.QtWidgets import QWidget, QFrame

from gen.order_item_window import Ui_OrderItemWidget


class OrderItemWidget(QWidget):
    def __init__(self, order, role_id=1):
        super().__init__()
        self.ui = Ui_OrderItemWidget()
        self.ui.setupUi(self)
        self.order = order
        self._fill()
        # кнопка удаления видна только администратору
        self.ui.pushButton_del.setVisible(role_id == 1)
        self.ui.pushButton_del.clicked.connect(self._on_delete)

    def _fill(self):
        from PyQt6.QtGui import QFont
        font = QFont("Times New Roman", 11)

        count = self.order.get("items_count", 0)
        total = self.order.get("total_amount", 0)
        self.ui.label_articul.setText(
            f"Заказ №{self.order.get('order_id')} | Товаров: {count} | Сумма: {float(total):.2f} руб."
        )
        self.ui.label_status.setText(f"Статус: {self.order.get('status_name', '')}")
        self.ui.label_pick_point.setText(f"Пункт выдачи: {self.order.get('address', '')}")
        self.ui.label_order_date.setText(f"Дата заказа: {self.order.get('order_date', '')}")
        delivery = self.order.get("delivery_date")
        self.ui.label_delivery_date.setText(
            f"Дата доставки:\n{delivery}" if delivery else "Дата доставки:\n—"
        )
        for lbl in [self.ui.label_articul, self.ui.label_status,
                    self.ui.label_pick_point, self.ui.label_order_date,
                    self.ui.label_delivery_date]:
            lbl.setFont(font)

    def set_selected(self, selected: bool):
        if selected:
            self.ui.frame_left.setStyleSheet("QFrame#frame_left { border: 2px solid #8bbfff; }")
            self.ui.frame_right.setStyleSheet("QFrame#frame_right { border: 2px solid #8bbfff; }")
        else:
            self.ui.frame_left.setStyleSheet("")
            self.ui.frame_right.setStyleSheet("")

    def _on_delete(self):
        main = self.window()
        if hasattr(main, "select_order_widget"):
            main.select_order_widget(self)
        if hasattr(main, "delete_order"):
            main.delete_order()

    def mouseDoubleClickEvent(self, event):
        # двойной клик открывает диалог редактирования заказа
        main = self.window()
        if hasattr(main, "select_order_widget"):
            main.select_order_widget(self)
        if hasattr(main, "edit_order"):
            main.edit_order()
