# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\script\update_pro.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 136)
        self.btn = QtWidgets.QPushButton(Dialog)
        self.btn.setGeometry(QtCore.QRect(120, 100, 80, 23))
        self.btn.setObjectName("btn")
        self.pro_bar = QtWidgets.QProgressBar(Dialog)
        self.pro_bar.setGeometry(QtCore.QRect(60, 20, 221, 23))
        self.pro_bar.setProperty("value", 0)
        self.pro_bar.setObjectName("pro_bar")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(128, 50, 71, 41))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.now = QtWidgets.QLabel(self.gridLayoutWidget)
        self.now.setText("")
        self.now.setObjectName("now")
        self.gridLayout.addWidget(self.now, 0, 1, 1, 1)
        self.all = QtWidgets.QLabel(self.gridLayoutWidget)
        self.all.setText("")
        self.all.setObjectName("all")
        self.gridLayout.addWidget(self.all, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.btn.clicked.connect(Dialog.cancel_update)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "更新进度"))
        self.btn.setText(_translate("Dialog", "取消"))
        self.label.setText(_translate("Dialog", "第"))
        self.label_2.setText(_translate("Dialog", "共"))
        self.label_3.setText(_translate("Dialog", "个"))
        self.label_4.setText(_translate("Dialog", "个"))

