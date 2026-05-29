from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QMessageBox

from db import dao
from gen.main_window import Ui_MainForm
from item_widget import ItemWidget
from order_item_widget import OrderItemWidget


def clear_layout(layout: QLayout):
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w:
            w.deleteLater()


class MainWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.user = user

        self.postav = None
        self.selected_widget = None
        self.selected_order_widget = None
        self.product_dialog = None
        self.order_dialog = None
        self.auth_window = None
        self.__conn()

    def __conn(self):
        self.visibles()
        self.fill_name()
        self.fill_sort_combo_box()
        self.fill_postav_combo_box()
        self.add_widgets_product()
        self.load_orders()
        self._apply_styles()

        self.ui.comboBox_sort.currentIndexChanged.connect(self.add_widgets_product)
        self.ui.lineEdit_search.textChanged.connect(self.add_widgets_product)
        self.ui.comboBox_postav.currentIndexChanged.connect(self.add_widgets_product)
        self.ui.pushButton_logout.clicked.connect(self.logout)

        self.ui.pushButton_add.clicked.connect(self.add_product)
        self.ui.pushButton_edit.clicked.connect(self.edit_product)
        self.ui.pushButton_del.clicked.connect(self.delete_product)

        self.ui.pushButton_add_order.clicked.connect(self.add_order)
        self.ui.pushButton_edit_order.clicked.connect(self.edit_order)
        self.ui.pushButton_delete_order.clicked.connect(self.delete_order)

    def _apply_styles(self):
        # открывать каталог первым при входе
        self.ui.tabWidget.setCurrentIndex(0)

        # дополнительный фон верхней панели
        # создаём контейнер с цветом фона и переносим в него все виджеты шапки
        from PyQt6.QtWidgets import QWidget, QHBoxLayout
        header = QWidget()
        header.setStyleSheet("background-color: #7FFF00;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(4, 4, 4, 4)
        hl.setSpacing(self.ui.horizontalLayout.spacing())

        items = []
        while self.ui.horizontalLayout.count():
            items.append(self.ui.horizontalLayout.takeAt(0))
        for item in items:
            w = item.widget()
            if w is self.ui.label_fio:
                hl.addWidget(w, 0, Qt.AlignmentFlag.AlignVCenter)
            elif w is not None:
                hl.addWidget(w)

        for i in range(self.ui.verticalLayout.count()):
            if self.ui.verticalLayout.itemAt(i).layout() is self.ui.horizontalLayout:
                self.ui.verticalLayout.takeAt(i)
                self.ui.verticalLayout.insertWidget(i, header)
                break

        # лейблы прозрачные — фон контейнера просвечивает сквозь них
        self.ui.label_for_logo.setStyleSheet("background: transparent;")
        self.ui.label_fio.setStyleSheet("background: transparent; color: black;")
        self.ui.pushButton_logout.setStyleSheet(
            "background-color: #00FA9A; color: black; border: 1px solid #333; border-radius: 3px; padding: 4px 12px;"
        )

        # акцент на кнопках целевого действия
        self.ui.pushButton_add.setStyleSheet("background-color: #00FA9A; color: black;")
        self.ui.pushButton_add_order.setStyleSheet("background-color: #00FA9A; color: black;")


    def fill_name(self):
        self.ui.label_fio.setText(self.user.get("full_name", ""))
        from PyQt6.QtGui import QPixmap
        self.ui.label_for_logo.setPixmap(QPixmap("image/logo/logo.png").scaled(
            self.ui.label_for_logo.width() or 80,
            self.ui.label_for_logo.height() or 60,
            Qt.AspectRatioMode.KeepAspectRatio
        ))

    def fill_sort_combo_box(self):
        self.ui.comboBox_sort.addItem("Без сортировки")
        self.ui.comboBox_sort.addItem("По возрастанию кол-ва на складе")
        self.ui.comboBox_sort.addItem("По убыванию кол-ва на складе")

    def fill_postav_combo_box(self):
        self.postav = dao.get_all_suppliers()
        self.ui.comboBox_postav.addItem("Все")
        self.ui.comboBox_postav.addItems(p["supplier_name"] for p in self.postav)

    def add_widgets_product(self):
        clear_layout(self.ui.verticalLayout_4)

        search = self.ui.lineEdit_search.text()
        sort = self.ui.comboBox_sort.currentText()
        postav = self.ui.comboBox_postav.currentText()

        products = dao.get_all_products(search, sort, postav)
        for product in products:
            self.ui.verticalLayout_4.addWidget(ItemWidget(product))
        self.ui.verticalLayout_4.addStretch()
        self.selected_widget = None

    def select_widget(self, widget):
        if self.selected_widget:
            self.selected_widget.set_selected(False)
        self.selected_widget = widget
        self.selected_widget.set_selected(True)

    def load_orders(self):
        clear_layout(self.ui.verticalLayout_9)
        orders = dao.get_all_orders()
        for order in orders:
            self.ui.verticalLayout_9.addWidget(OrderItemWidget(order))
        self.ui.verticalLayout_9.addStretch()
        self.selected_order_widget = None

    def select_order_widget(self, widget):
        if self.selected_order_widget:
            self.selected_order_widget.set_selected(False)
        self.selected_order_widget = widget
        self.selected_order_widget.set_selected(True)

    def _dialog_open(self):
        return self.product_dialog is not None and self.product_dialog.isVisible()

    def add_product(self):
        if self._dialog_open():
            self.product_dialog.activateWindow()
            return
        from product_dialog import ProductDialog
        self.product_dialog = ProductDialog(on_save=self.add_widgets_product)
        self.product_dialog.show()

    def edit_product(self):
        if not self.selected_widget:
            QMessageBox.warning(self, "Предупреждение", "Выберите товар для редактирования.")
            return
        if self._dialog_open():
            self.product_dialog.activateWindow()
            return
        from product_dialog import ProductDialog
        self.product_dialog = ProductDialog(
            product=self.selected_widget.product,
            on_save=self.add_widgets_product
        )
        self.product_dialog.show()

    def delete_product(self):
        if not self.selected_widget:
            QMessageBox.warning(self, "Предупреждение", "Выберите товар для удаления.")
            return
        product_id = self.selected_widget.product["product_id"]
        # нельзя удалить товар если он привязан к заказу
        if dao.product_in_orders(product_id):
            QMessageBox.warning(self, "Ошибка", "Товар присутствует в заказе, удаление невозможно.")
            return
        reply = QMessageBox.question(
            self, "Подтверждение", "Вы действительно хотите удалить запись?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            dao.delete_product(product_id)
            self.add_widgets_product()

    def add_order(self):
        from order_dialog_add_edit import AddEditOrderDialog
        self.order_dialog = AddEditOrderDialog(on_save=self.load_orders)
        self.order_dialog.show()

    def edit_order(self):
        if not self.selected_order_widget:
            QMessageBox.warning(self, "Предупреждение", "Выберите заказ.")
            return
        from order_dialog_add_edit import AddEditOrderDialog
        self.order_dialog = AddEditOrderDialog(
            order=self.selected_order_widget.order,
            on_save=self.load_orders
        )
        self.order_dialog.show()

    def delete_order(self):
        if not self.selected_order_widget:
            QMessageBox.warning(self, "Предупреждение", "Выберите заказ.")
            return
        reply = QMessageBox.question(
            self, "Подтверждение", "Вы действительно хотите удалить запись?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            dao.delete_order(self.selected_order_widget.order["order_id"])
            self.load_orders()

    def logout(self):
        from auth import AuthWindow
        self.auth_window = AuthWindow()
        self.auth_window.show()
        self.close()

    def visibles(self):
        # скрываем кнопки и вкладки в зависимости от роли пользователя
        user_role = self.user.get("role_id")
        if user_role in (2, 3, 4):
            self.ui.pushButton_del.setVisible(False)
            self.ui.pushButton_add.setVisible(False)
            self.ui.pushButton_edit.setVisible(False)

        if user_role in (2, 3, 4):
            self.ui.pushButton_delete_order.setVisible(False)
            self.ui.pushButton_edit_order.setVisible(False)
            self.ui.pushButton_add_order.setVisible(False)

        if user_role in (3, 4):
            self.ui.tabWidget.setTabVisible(1, False)
            self.ui.lineEdit_search.setVisible(False)
            self.ui.comboBox_postav.setVisible(False)
            self.ui.comboBox_sort.setVisible(False)
