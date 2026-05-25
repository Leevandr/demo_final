from PyQt6.QtWidgets import QWidget, QLayout

from src.db import dao
from src.widgets.ItemDialog import ItemDialog
from src.widgets.ItemWidget import ItemWidget
from ui.gen.MainWidget import Ui_MainWidget


def clear_layout(layout: QLayout):
    while layout.count():
        w = layout.takeAt(0).widget()
        if w:
            w.deleteLater()


class MainWindow(QWidget):
    def __init__(self, user=None):
        super().__init__()
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        self.user = user
        self.fill_fio()
        self.access_setting()
        self.add_widgets_items()
        self.conn()

    def conn(self):
        self.ui.pushButton_add_product.clicked.connect(self.add_product)

    def add_product(self):
        ItemDialog().exec()
        self.add_widgets_items()

    def add_widgets_items(self):
        clear_layout(self.ui.verticalLayout_products)
        items = dao.get_all_products()
        print(items)
        for item in items:
            print(item)
            self.ui.verticalLayout_products.addWidget(ItemWidget(item))


    def access_setting(self):
        if self.user:
            if self.user["role_id"] == 4:
                self.ui.pushButton_add_product.setVisible(False)
                self.ui.pushButton_edit_product.setVisible(False)
                self.ui.pushButton_delete_product.setVisible(False)

            if self.user["role_id"] == 2:
                self.ui.pushButton_add_product.setVisible(False)
                self.ui.pushButton_edit_product.setVisible(False)
                self.ui.pushButton_delete_product.setVisible(False)
                self.ui.tabWidget.setTabVisible(1, False)

        else:
            self.ui.pushButton_add_product.setVisible(False)
            self.ui.pushButton_edit_product.setVisible(False)
            self.ui.pushButton_delete_product.setVisible(False)

            self.ui.tabWidget.setTabVisible(1, False)

            self.ui.lineEdit_search.setVisible(False)
            self.ui.comboBox_count.setVisible(False)
            self.ui.comboBox_suppilers.setVisible(False)

    def fill_fio(self):
        if self.user:
            self.ui.fio.setText(str(self.user["full_name"]))
        else:
            self.ui.fio.setText("Гостевой режим")
