
from PyQt6.QtWidgets import QWidget, QLayout
from db import dao
from gen.main_window import Ui_MainForm
from item_widget import ItemWidget

def clear_layout(layout: QLayout):
    while layout.count():
        w = layout.takeAt(0).widget()
        if w:
            w.deleteLater()

class MainWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.user = user
        print(user)
        self.postav = None
        self.selected_widget = None
        self.product_item_window = None
        self.__conn()

    def __conn(self):
        self.fill_name()
        self.fill_sort_combo_box()
        self.fill_postav_combo_box()
        self.add_widgets_product()

        self.ui.comboBox_sort.currentIndexChanged.connect(self.add_widgets_product)
        self.ui.lineEdit_search.textChanged.connect(self.add_widgets_product)
        self.ui.comboBox_postav.currentIndexChanged.connect(self.add_widgets_product)

    def fill_name(self):
        self.ui.label_fio.setText(self.user["full_name"])

    def fill_sort_combo_box(self):
        self.ui.comboBox_sort.addItem("Без сортировки")
        self.ui.comboBox_sort.addItem("По возрастанию кол-ва на складе")
        self.ui.comboBox_sort.addItem("По убыванию кол-ва на складе")

    def fill_postav_combo_box(self):
        self.postav = dao.get_all_postav()
        self.ui.comboBox_postav.addItem("Все")
        self.ui.comboBox_postav.addItems(post["supplier_name"] for post in self.postav)

    def add_widgets_product(self):
        clear_layout(self.ui.verticalLayout_4)

        search = self.ui.lineEdit_search.text()
        sort = self.ui.comboBox_sort.currentText()
        postav = self.ui.comboBox_postav.currentText()

        products = dao.get_all_products(search, sort, postav)
        for product in products:
            self.ui.verticalLayout_4.addWidget(ItemWidget(product))
            print("Item ======== ", product, "\n")
        self.selected_widget = None

    def select_widget(self, widget):
        if self.selected_widget:
            self.selected_widget.setStyleSheet("")

        self.selected_widget = widget
        self.selected_widget.setStyleSheet("border: 2px solid #8bbfff; border-radius: 6px")