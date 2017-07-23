# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\script\dlg.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 120)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(80, 80, 239, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fast_update_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.fast_update_button.setObjectName("fast_update_button")
        self.horizontalLayout.addWidget(self.fast_update_button)
        self.full_update_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.full_update_button.setObjectName("full_update_button")
        self.horizontalLayout.addWidget(self.full_update_button)
        self.cancel_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 338, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        self.retranslateUi(Dialog)
        self.cancel_button.clicked.connect(Dialog.close)
        self.full_update_button.clicked.connect(Dialog.full_update)
        self.fast_update_button.clicked.connect(Dialog.fast_update)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "选择测试模式"))
        self.fast_update_button.setText(_translate("Dialog", "快速更新"))
        self.full_update_button.setText(_translate("Dialog", "完整更新"))
        self.cancel_button.setText(_translate("Dialog", "取消"))
        self.label.setText(_translate("Dialog", "请选择快速更新或完整更新"))
        self.label_2.setText(_translate("Dialog", "快速更新只测试当前使用的名单中的账号，适合平时使用"))
        self.label_3.setText(_translate("Dialog", "完整更新测试所有用户，耗时较长，一般只在没有可用账号时用"))

