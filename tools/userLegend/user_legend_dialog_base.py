# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_legend_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(342, 498)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.composerList = QtWidgets.QListWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.composerList.sizePolicy().hasHeightForWidth())
        self.composerList.setSizePolicy(sizePolicy)
        self.composerList.setMinimumSize(QtCore.QSize(0, 0))
        self.composerList.setMaximumSize(QtCore.QSize(16777215, 100))
        self.composerList.setObjectName("composerList")
        self.verticalLayout.addWidget(self.composerList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_scale = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_scale.setObjectName("lineEdit_scale")
        self.horizontalLayout.addWidget(self.lineEdit_scale)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(23, 23))
        self.pushButton.setMaximumSize(QtCore.QSize(23, 23))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.layerList = QtWidgets.QListWidget(Dialog)
        self.layerList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.layerList.setObjectName("layerList")
        self.verticalLayout.addWidget(self.layerList)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(7)
        font.setItalic(True)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Слои легенды"))
        self.label_2.setText(_translate("Dialog", "Макеты:"))
        self.composerList.setToolTip(_translate("Dialog", "Список доступных макетов."))
        self.label.setText(_translate("Dialog", "Масштаб: "))
        self.lineEdit_scale.setToolTip(_translate("Dialog", "Масштаб, при котором будут сформированы символы."))
        self.pushButton.setToolTip(_translate("Dialog", "Применить масштаб."))
        self.pushButton.setText(_translate("Dialog", ">"))
        self.label_3.setText(_translate("Dialog", "Слои для легенды:"))
        self.layerList.setToolTip(_translate("Dialog", "Список слоев, доступных при выбранном масштабе."))

