from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from ui.gen.ItemOrderWidget import Ui_ItemOrderWidget


class ItemOrderWidget(QWidget):
    def __init__(self, item):
        super().__init__()
        self.ui = Ui_ItemOrderWidget()
        self.ui.setupUi(self)
        self.ui.frame_card.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.item = item
        self.is_selected = False
        self.fill()

    def apply_style(self):
        border = "4px solid #1f6feb" if self.is_selected else "1px solid #263238"
        self.ui.frame_card.setStyleSheet(
            "QFrame#frame_card { background-color: #ffffff; border: %s; border-radius: 0px; }" % border
        )

    def set_selected(self, value: bool):
        self.is_selected = value
        self.apply_style()

    def fill(self):
        self.apply_style()
        self.ui.label_status_name.setText(f'Статус: {self.item["status"]}')
        self.ui.label_product_name.setText(f'Артикул: {self.item["article"]}')
        self.ui.label_pickup_point.setText(f'Пункт выдачи: {self.item["pickup"]}')
        self.ui.label_order_date.setText(f'Дата заказа: {self.item["order_date"]}')
        self.ui.label_delivery_date.setText(f'Дата доставки: {self.item["delivery_date"]}')

    def mousePressEvent(self, a0):
        main = self.window()
        main.select_widget(self)
