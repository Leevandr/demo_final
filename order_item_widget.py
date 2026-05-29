from PyQt6.QtWidgets import QWidget

from gen.order_item_window import Ui_OrderItemWidget


class OrderItemWidget(QWidget):
    def __init__(self, order):
        super().__init__()
        self.ui = Ui_OrderItemWidget()
        self.ui.setupUi(self)
        self.setObjectName("OrderItemWidget")
        self.setAutoFillBackground(True)
        self.order = order
        self._fill()
        self._apply_style(selected=False)

    def _fill(self):
        self.ui.label_articul.setText(f"Артикул: {self.order.get('article', '')}")
        self.ui.label_status.setText(f"Статус: {self.order.get('status_name', '')}")
        self.ui.label_pick_point.setText(f"Пункт выдачи: {self.order.get('address', '')}")
        self.ui.label_order_date.setText(f"Дата заказа: {self.order.get('order_date', '')}")
        delivery = self.order.get("delivery_date")
        self.ui.label_delivery_date.setText(
            f"Дата доставки:\n{delivery}" if delivery else "Дата доставки:\n—"
        )

    def _apply_style(self, selected: bool):
        border = "2px solid #8bbfff" if selected else "1px solid #b0b0b0"
        self.setStyleSheet(f"""
            #OrderItemWidget {{
                border: {border};
                border-radius: 6px;
                background-color: white;
            }}
            #OrderItemWidget QLabel {{
                border: none;
                background: transparent;
            }}
            QLabel#label_delivery_date {{
                border: 1px solid #b0b0b0;
                border-radius: 4px;
                background-color: white;
                padding: 6px;
            }}
        """)

    def set_selected(self, selected: bool):
        self._apply_style(selected)

    def mousePressEvent(self, a0):
        main = self.window()
        if hasattr(main, "select_order_widget"):
            main.select_order_widget(self)
