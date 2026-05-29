from PyQt6.QtWidgets import QWidget

from gen.order_item_window import Ui_OrderItemWidget

_STYLE_NORMAL = """
    #OrderItemWidget {
        border: 1px solid #b0b0b0;
        border-radius: 6px;
        background-color: #ffffff;
    }
    #OrderItemWidget QLabel {
        border: none;
        background: transparent;
    }
"""

_STYLE_SELECTED = """
    #OrderItemWidget {
        border: 2px solid #8bbfff;
        border-radius: 6px;
        background-color: #ffffff;
    }
    #OrderItemWidget QLabel {
        border: none;
        background: transparent;
    }
"""


class OrderItemWidget(QWidget):
    def __init__(self, order):
        super().__init__()
        self.ui = Ui_OrderItemWidget()
        self.ui.setupUi(self)
        self.setObjectName("OrderItemWidget")
        self.setAutoFillBackground(True)
        self.order = order
        self._fill()
        self.setStyleSheet(_STYLE_NORMAL)

    def _fill(self):
        article = self.order.get("article", "")
        self.ui.label_articul.setText(f"<b>Артикул: {article}</b>")
        self.ui.label_status.setText(f"Статус: {self.order.get('status_name', '')}")
        self.ui.label_pick_point.setText(f"Пункт выдачи: {self.order.get('address', '')}")
        self.ui.label_order_date.setText(f"Дата заказа: {self.order.get('order_date', '')}")
        delivery = self.order.get("delivery_date")
        self.ui.label_delivery_date.setText(
            f"Дата доставки:\n{delivery}" if delivery else "Дата доставки:\n—"
        )

    def set_selected(self, selected: bool):
        self.setStyleSheet(_STYLE_SELECTED if selected else _STYLE_NORMAL)

    def mousePressEvent(self, a0):
        main = self.window()
        if hasattr(main, "select_order_widget"):
            main.select_order_widget(self)
