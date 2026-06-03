from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_OrderDialog(object):
    def setupUi(self, OrderDialog):
        OrderDialog.setObjectName("OrderDialog")
        OrderDialog.resize(720, 580)

        self.verticalLayout_main = QtWidgets.QVBoxLayout(OrderDialog)
        self.verticalLayout_main.setObjectName("verticalLayout_main")

        # --- GroupBox: информация о заказе ---
        self.groupBox_info = QtWidgets.QGroupBox(parent=OrderDialog)
        self.groupBox_info.setObjectName("groupBox_info")
        self.formLayout_info = QtWidgets.QFormLayout(self.groupBox_info)
        self.formLayout_info.setObjectName("formLayout_info")

        self.statusLabel = QtWidgets.QLabel(parent=self.groupBox_info)
        self.statusLabel.setObjectName("statusLabel")
        self.formLayout_info.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.statusLabel)
        self.statusComboBox = QtWidgets.QComboBox(parent=self.groupBox_info)
        self.statusComboBox.setObjectName("statusComboBox")
        self.formLayout_info.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.statusComboBox)

        self.pickup_pointLabel = QtWidgets.QLabel(parent=self.groupBox_info)
        self.pickup_pointLabel.setObjectName("pickup_pointLabel")
        self.formLayout_info.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.pickup_pointLabel)
        self.pickup_pointComboBox = QtWidgets.QComboBox(parent=self.groupBox_info)
        self.pickup_pointComboBox.setObjectName("pickup_pointComboBox")
        self.formLayout_info.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.pickup_pointComboBox)

        self.orderdateLabel = QtWidgets.QLabel(parent=self.groupBox_info)
        self.orderdateLabel.setObjectName("orderdateLabel")
        self.formLayout_info.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.orderdateLabel)
        self.orderdateDateEdit = QtWidgets.QDateEdit(parent=self.groupBox_info)
        self.orderdateDateEdit.setCalendarPopup(True)
        self.orderdateDateEdit.setObjectName("orderdateDateEdit")
        self.formLayout_info.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.orderdateDateEdit)

        self.deliverydateLabel = QtWidgets.QLabel(parent=self.groupBox_info)
        self.deliverydateLabel.setObjectName("deliverydateLabel")
        self.formLayout_info.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.deliverydateLabel)
        self.deliverydateDateEdit = QtWidgets.QDateEdit(parent=self.groupBox_info)
        self.deliverydateDateEdit.setCalendarPopup(True)
        self.deliverydateDateEdit.setObjectName("deliverydateDateEdit")
        self.formLayout_info.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.deliverydateDateEdit)

        self.userLabel = QtWidgets.QLabel(parent=self.groupBox_info)
        self.userLabel.setObjectName("userLabel")
        self.formLayout_info.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.userLabel)
        self.usersComboBox = QtWidgets.QComboBox(parent=self.groupBox_info)
        self.usersComboBox.setObjectName("usersComboBox")
        self.formLayout_info.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.usersComboBox)

        self.verticalLayout_main.addWidget(self.groupBox_info)

        # --- GroupBox: товары в заказе ---
        self.groupBox_items = QtWidgets.QGroupBox(parent=OrderDialog)
        self.groupBox_items.setObjectName("groupBox_items")
        self.verticalLayout_items = QtWidgets.QVBoxLayout(self.groupBox_items)
        self.verticalLayout_items.setObjectName("verticalLayout_items")

        self.tableWidget = QtWidgets.QTableWidget(parent=self.groupBox_items)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        for i, title in enumerate(["#", "Артикул", "Наименование", "Кол-во", "Цена, руб.", "Сумма, руб."]):
            self.tableWidget.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(title))
        self.verticalLayout_items.addWidget(self.tableWidget)

        self.horizontalLayout_item_btns = QtWidgets.QHBoxLayout()
        self.horizontalLayout_item_btns.setObjectName("horizontalLayout_item_btns")
        self.pushButton_add_item = QtWidgets.QPushButton(parent=self.groupBox_items)
        self.pushButton_add_item.setObjectName("pushButton_add_item")
        self.horizontalLayout_item_btns.addWidget(self.pushButton_add_item)
        self.pushButton_edit_qty = QtWidgets.QPushButton(parent=self.groupBox_items)
        self.pushButton_edit_qty.setObjectName("pushButton_edit_qty")
        self.horizontalLayout_item_btns.addWidget(self.pushButton_edit_qty)
        self.pushButton_del_item = QtWidgets.QPushButton(parent=self.groupBox_items)
        self.pushButton_del_item.setObjectName("pushButton_del_item")
        self.horizontalLayout_item_btns.addWidget(self.pushButton_del_item)
        self.verticalLayout_items.addLayout(self.horizontalLayout_item_btns)

        self.verticalLayout_main.addWidget(self.groupBox_items)

        # --- нижние кнопки ---
        self.horizontalLayout_main_btns = QtWidgets.QHBoxLayout()
        self.horizontalLayout_main_btns.setObjectName("horizontalLayout_main_btns")
        self.pushButton_save = QtWidgets.QPushButton(parent=OrderDialog)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_main_btns.addWidget(self.pushButton_save)
        self.pushButton_cancel = QtWidgets.QPushButton(parent=OrderDialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_main_btns.addWidget(self.pushButton_cancel)
        self.verticalLayout_main.addLayout(self.horizontalLayout_main_btns)

        self.retranslateUi(OrderDialog)
        QtCore.QMetaObject.connectSlotsByName(OrderDialog)

    def retranslateUi(self, OrderDialog):
        _translate = QtCore.QCoreApplication.translate
        OrderDialog.setWindowTitle(_translate("OrderDialog", "Добавление заказа"))
        self.groupBox_info.setTitle(_translate("OrderDialog", "Информация о заказе"))
        self.statusLabel.setText(_translate("OrderDialog", "Статус:"))
        self.pickup_pointLabel.setText(_translate("OrderDialog", "Пункт выдачи:"))
        self.orderdateLabel.setText(_translate("OrderDialog", "Дата заказа:"))
        self.deliverydateLabel.setText(_translate("OrderDialog", "Дата доставки:"))
        self.userLabel.setText(_translate("OrderDialog", "Пользователь:"))
        self.groupBox_items.setTitle(_translate("OrderDialog", "Товары в заказе"))
        self.pushButton_add_item.setText(_translate("OrderDialog", "Добавить товар"))
        self.pushButton_edit_qty.setText(_translate("OrderDialog", "Изменить количество"))
        self.pushButton_del_item.setText(_translate("OrderDialog", "Удалить товар"))
        self.pushButton_save.setText(_translate("OrderDialog", "Сохранить"))
        self.pushButton_cancel.setText(_translate("OrderDialog", "Назад"))
