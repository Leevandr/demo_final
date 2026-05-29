from PyQt6.QtWidgets import QWidget

from gen.order_item_window import Ui_OrderItemWidget


class OrderItemWidget(QWidget):
    def __init__(self, order):
        super().__init__()
        self.ui = Ui_OrderItemWidget()
        self.ui.setupUi(self)
        self.order = order
        self._fill()

    def _fill(self):
        self.ui.label_articul.setText(f"Артикул: {self.order.get('article', '')}")
        self.ui.label_status.setText(f"Статус: {self.order.get('status_name', '')}")
        self.ui.label_pick_point.setText(f"Пункт выдачи: {self.order.get('address', '')}")
        self.ui.label_order_date.setText(f"Дата заказа: {self.order.get('order_date', '')}")
        delivery = self.order.get("delivery_date")
        self.ui.label_delivery_date.setText(f"Дата выдачи: {delivery if delivery else '—'}")

    def mousePressEvent(self, a0):
        main = self.window()
        if hasattr(main, "select_order_widget"):
            main.select_order_widget(self)
