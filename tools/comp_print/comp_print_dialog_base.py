# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'comp_print_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CompPrintDialogBase(object):
    def setupUi(self, CompPrintDialogBase):
        CompPrintDialogBase.setObjectName("CompPrintDialogBase")
        CompPrintDialogBase.setWindowModality(QtCore.Qt.NonModal)
        CompPrintDialogBase.resize(304, 531)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CompPrintDialogBase.sizePolicy().hasHeightForWidth())
        CompPrintDialogBase.setSizePolicy(sizePolicy)
        CompPrintDialogBase.setMinimumSize(QtCore.QSize(0, 0))
        CompPrintDialogBase.setMaximumSize(QtCore.QSize(10000, 10000))
        CompPrintDialogBase.setSizeGripEnabled(False)
        CompPrintDialogBase.setModal(False)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(CompPrintDialogBase)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(CompPrintDialogBase)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(CompPrintDialogBase)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox = QtWidgets.QGroupBox(CompPrintDialogBase)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setContentsMargins(-1, 1, -1, 4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/orient_gor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.radioButton.setIcon(icon)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/orient_vert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.radioButton_2.setIcon(icon1)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_6.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(CompPrintDialogBase)
        self.groupBox_4.setEnabled(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setContentsMargins(-1, 1, -1, 4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_5.setChecked(True)
        self.radioButton_5.setObjectName("radioButton_5")
        self.verticalLayout_2.addWidget(self.radioButton_5)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_3.setEnabled(True)
        self.radioButton_3.setChecked(False)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_2.addWidget(self.radioButton_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_6.addWidget(self.groupBox_4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.groupBox_2 = QtWidgets.QGroupBox(CompPrintDialogBase)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.horizontalSlider.setMouseTracking(False)
        self.horizontalSlider.setAcceptDrops(False)
        self.horizontalSlider.setToolTip("")
        self.horizontalSlider.setAutoFillBackground(False)
        self.horizontalSlider.setMaximum(4)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setProperty("value", 0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_5.addWidget(self.horizontalSlider)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_8.addWidget(self.groupBox_2)
        self.groupBox_6 = QtWidgets.QGroupBox(CompPrintDialogBase)
        self.groupBox_6.setFlat(False)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_3.setContentsMargins(9, 4, -1, 4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_9 = QtWidgets.QLabel(self.groupBox_6)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.spinBox_Top = QtWidgets.QSpinBox(self.groupBox_6)
        self.spinBox_Top.setMaximum(500)
        self.spinBox_Top.setProperty("value", 10)
        self.spinBox_Top.setObjectName("spinBox_Top")
        self.gridLayout.addWidget(self.spinBox_Top, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_6)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 2, 1, 1)
        self.spinBox_Right = QtWidgets.QSpinBox(self.groupBox_6)
        self.spinBox_Right.setMaximum(500)
        self.spinBox_Right.setProperty("value", 10)
        self.spinBox_Right.setObjectName("spinBox_Right")
        self.gridLayout.addWidget(self.spinBox_Right, 0, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_6)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.spinBox_Left = QtWidgets.QSpinBox(self.groupBox_6)
        self.spinBox_Left.setMaximum(500)
        self.spinBox_Left.setProperty("value", 10)
        self.spinBox_Left.setObjectName("spinBox_Left")
        self.gridLayout.addWidget(self.spinBox_Left, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_6)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1)
        self.spinBox_Bottom = QtWidgets.QSpinBox(self.groupBox_6)
        self.spinBox_Bottom.setMaximum(500)
        self.spinBox_Bottom.setProperty("value", 10)
        self.spinBox_Bottom.setObjectName("spinBox_Bottom")
        self.gridLayout.addWidget(self.spinBox_Bottom, 1, 3, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        self.checkBox_Frame = QtWidgets.QCheckBox(self.groupBox_6)
        self.checkBox_Frame.setChecked(True)
        self.checkBox_Frame.setObjectName("checkBox_Frame")
        self.horizontalLayout_3.addWidget(self.checkBox_Frame)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout_8.addWidget(self.groupBox_6)
        self.groupBox_Stamps = QtWidgets.QGroupBox(CompPrintDialogBase)
        self.groupBox_Stamps.setCheckable(True)
        self.groupBox_Stamps.setChecked(False)
        self.groupBox_Stamps.setObjectName("groupBox_Stamps")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_Stamps)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.comboBox_Stamps = QtWidgets.QComboBox(self.groupBox_Stamps)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_Stamps.sizePolicy().hasHeightForWidth())
        self.comboBox_Stamps.setSizePolicy(sizePolicy)
        self.comboBox_Stamps.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_Stamps.setObjectName("comboBox_Stamps")
        self.horizontalLayout_7.addWidget(self.comboBox_Stamps)
        self.pushButton_edit = QtWidgets.QPushButton(self.groupBox_Stamps)
        self.pushButton_edit.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_edit.setIcon(icon2)
        self.pushButton_edit.setObjectName("pushButton_edit")
        self.horizontalLayout_7.addWidget(self.pushButton_edit)
        self.check_onlyFirstPage = QtWidgets.QCheckBox(self.groupBox_Stamps)
        self.check_onlyFirstPage.setObjectName("check_onlyFirstPage")
        self.horizontalLayout_7.addWidget(self.check_onlyFirstPage)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.verticalLayout_9.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_13 = QtWidgets.QLabel(self.groupBox_Stamps)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_8.addWidget(self.label_13)
        self.comboBox_layoutStamp = QtWidgets.QComboBox(self.groupBox_Stamps)
        self.comboBox_layoutStamp.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_layoutStamp.setObjectName("comboBox_layoutStamp")
        self.horizontalLayout_8.addWidget(self.comboBox_layoutStamp)
        self.verticalLayout_9.addLayout(self.horizontalLayout_8)
        self.verticalLayout_8.addWidget(self.groupBox_Stamps)
        self.groupBox_3 = QtWidgets.QGroupBox(CompPrintDialogBase)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.spinBox_nalog = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.spinBox_nalog.setDecimals(1)
        self.spinBox_nalog.setProperty("value", 8.0)
        self.spinBox_nalog.setObjectName("spinBox_nalog")
        self.horizontalLayout_4.addWidget(self.spinBox_nalog)
        self.line = QtWidgets.QFrame(self.groupBox_3)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_4.addWidget(self.line)
        self.checkBox_textLines = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_textLines.setChecked(True)
        self.checkBox_textLines.setObjectName("checkBox_textLines")
        self.horizontalLayout_4.addWidget(self.checkBox_textLines)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.line_2 = QtWidgets.QFrame(self.groupBox_3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_7.addWidget(self.line_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_8.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/lines.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon3)
        self.pushButton_8.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_8.setCheckable(False)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_6.addWidget(self.pushButton_8)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/frames.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_6.addWidget(self.pushButton_5)
        self.pushButton_9 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_9.setMinimumSize(QtCore.QSize(21, 21))
        self.pushButton_9.setMaximumSize(QtCore.QSize(21, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setStyleSheet("color: rgb(255, 0, 0);")
        self.pushButton_9.setCheckable(False)
        self.pushButton_9.setObjectName("pushButton_9")
        self.verticalLayout_6.addWidget(self.pushButton_9)
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        spacerItem6 = QtWidgets.QSpacerItem(13, 66, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.frame = QtWidgets.QFrame(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(111, 61))
        self.frame.setMaximumSize(QtCore.QSize(111, 61))
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 40, 31, 21))
        self.pushButton_3.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/arrow_bottom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon5)
        self.pushButton_3.setIconSize(QtCore.QSize(12, 12))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(70, 20, 31, 21))
        self.pushButton_4.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/arrow_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon6)
        self.pushButton_4.setIconSize(QtCore.QSize(12, 12))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(40, 0, 31, 21))
        self.pushButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/arrow_up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon7)
        self.pushButton.setIconSize(QtCore.QSize(12, 12))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.pushButton_2.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/arrow_left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon8)
        self.pushButton_2.setIconSize(QtCore.QSize(12, 12))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(40, 20, 31, 21))
        self.pushButton_6.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon9)
        self.pushButton_6.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_5.addWidget(self.frame)
        spacerItem7 = QtWidgets.QSpacerItem(13, 66, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_7.setStyleSheet("/*background-color: rgb(222, 255, 212);*/")
        self.pushButton_7.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/create.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon10)
        self.pushButton_7.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_5.addWidget(self.pushButton_7)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.verticalLayout_8.addWidget(self.groupBox_3)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem8)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        font = QtGui.QFont()
        font.setItalic(True)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.retranslateUi(CompPrintDialogBase)
        QtCore.QMetaObject.connectSlotsByName(CompPrintDialogBase)
        CompPrintDialogBase.setTabOrder(self.pushButton_6, self.radioButton)
        CompPrintDialogBase.setTabOrder(self.radioButton, self.horizontalSlider)
        CompPrintDialogBase.setTabOrder(self.horizontalSlider, self.radioButton_3)
        CompPrintDialogBase.setTabOrder(self.radioButton_3, self.pushButton)
        CompPrintDialogBase.setTabOrder(self.pushButton, self.pushButton_4)
        CompPrintDialogBase.setTabOrder(self.pushButton_4, self.pushButton_3)
        CompPrintDialogBase.setTabOrder(self.pushButton_3, self.pushButton_2)
        CompPrintDialogBase.setTabOrder(self.pushButton_2, self.groupBox_Stamps)
        CompPrintDialogBase.setTabOrder(self.groupBox_Stamps, self.radioButton_2)
        CompPrintDialogBase.setTabOrder(self.radioButton_2, self.spinBox_Top)
        CompPrintDialogBase.setTabOrder(self.spinBox_Top, self.spinBox_Right)
        CompPrintDialogBase.setTabOrder(self.spinBox_Right, self.spinBox_Left)
        CompPrintDialogBase.setTabOrder(self.spinBox_Left, self.spinBox_Bottom)
        CompPrintDialogBase.setTabOrder(self.spinBox_Bottom, self.lineEdit)
        CompPrintDialogBase.setTabOrder(self.lineEdit, self.checkBox_Frame)
        CompPrintDialogBase.setTabOrder(self.checkBox_Frame, self.comboBox_Stamps)
        CompPrintDialogBase.setTabOrder(self.comboBox_Stamps, self.check_onlyFirstPage)
        CompPrintDialogBase.setTabOrder(self.check_onlyFirstPage, self.radioButton_5)
        CompPrintDialogBase.setTabOrder(self.radioButton_5, self.spinBox_nalog)
        CompPrintDialogBase.setTabOrder(self.spinBox_nalog, self.checkBox_textLines)
        CompPrintDialogBase.setTabOrder(self.checkBox_textLines, self.pushButton_8)
        CompPrintDialogBase.setTabOrder(self.pushButton_8, self.pushButton_5)
        CompPrintDialogBase.setTabOrder(self.pushButton_5, self.pushButton_9)
        CompPrintDialogBase.setTabOrder(self.pushButton_9, self.pushButton_7)

    def retranslateUi(self, CompPrintDialogBase):
        _translate = QtCore.QCoreApplication.translate
        CompPrintDialogBase.setWindowTitle(_translate("CompPrintDialogBase", "Компоновщик"))
        self.label.setText(_translate("CompPrintDialogBase", "Масштаб   1: "))
        self.lineEdit.setText(_translate("CompPrintDialogBase", "500"))
        self.groupBox.setTitle(_translate("CompPrintDialogBase", "Ориентация"))
        self.radioButton.setText(_translate("CompPrintDialogBase", "Альбомная"))
        self.radioButton_2.setText(_translate("CompPrintDialogBase", "Книжная"))
        self.groupBox_4.setTitle(_translate("CompPrintDialogBase", "Способ компоновки"))
        self.radioButton_5.setToolTip(_translate("CompPrintDialogBase", "Все рамки в отдном многостраничном макете"))
        self.radioButton_5.setText(_translate("CompPrintDialogBase", "Многостранично"))
        self.radioButton_3.setToolTip(_translate("CompPrintDialogBase", "Каждая выбранная или последняя рамка в отдельном макете"))
        self.radioButton_3.setText(_translate("CompPrintDialogBase", "Постранично"))
        self.groupBox_2.setTitle(_translate("CompPrintDialogBase", "Размер листа"))
        self.label_2.setText(_translate("CompPrintDialogBase", "А4"))
        self.label_3.setText(_translate("CompPrintDialogBase", "А3"))
        self.label_4.setText(_translate("CompPrintDialogBase", "А2"))
        self.label_5.setText(_translate("CompPrintDialogBase", "А1"))
        self.label_6.setText(_translate("CompPrintDialogBase", "А0"))
        self.groupBox_6.setTitle(_translate("CompPrintDialogBase", "Поля"))
        self.label_9.setText(_translate("CompPrintDialogBase", "Верхнее"))
        self.label_11.setText(_translate("CompPrintDialogBase", "Правое"))
        self.label_10.setText(_translate("CompPrintDialogBase", "Левое"))
        self.label_12.setText(_translate("CompPrintDialogBase", "Нижнее"))
        self.checkBox_Frame.setToolTip(_translate("CompPrintDialogBase", "Отдельная рамка в виде прозрачного прямоугольника вместо встроенной рамки карты. Позволяет в макете наносить маску под рамкой."))
        self.checkBox_Frame.setText(_translate("CompPrintDialogBase", "Внешняя\n"
"рамка"))
        self.groupBox_Stamps.setTitle(_translate("CompPrintDialogBase", "Штамп"))
        self.pushButton_edit.setToolTip(_translate("CompPrintDialogBase", "Отредактировать текущий штамп"))
        self.check_onlyFirstPage.setToolTip(_translate("CompPrintDialogBase", "Вставить штамп только на первом листе"))
        self.check_onlyFirstPage.setText(_translate("CompPrintDialogBase", "На 1 листе"))
        self.label_13.setText(_translate("CompPrintDialogBase", "Пользовательский штамп:"))
        self.groupBox_3.setTitle(_translate("CompPrintDialogBase", "Навигация"))
        self.label_7.setText(_translate("CompPrintDialogBase", "Наложение:"))
        self.checkBox_textLines.setToolTip(_translate("CompPrintDialogBase", "Отображение номера стыковочного листа над линией"))
        self.checkBox_textLines.setText(_translate("CompPrintDialogBase", "Подпись стыковок"))
        self.pushButton_8.setToolTip(_translate("CompPrintDialogBase", "Создать линии стыковки"))
        self.pushButton_5.setToolTip(_translate("CompPrintDialogBase", "Показать/скрыть рамки"))
        self.pushButton_9.setToolTip(_translate("CompPrintDialogBase", "Сбросить все"))
        self.pushButton_9.setText(_translate("CompPrintDialogBase", "X"))
        self.pushButton_3.setToolTip(_translate("CompPrintDialogBase", "Создать рамку снизу"))
        self.pushButton_4.setToolTip(_translate("CompPrintDialogBase", "Создать рамку справа"))
        self.pushButton.setToolTip(_translate("CompPrintDialogBase", "Создать рамку сверху"))
        self.pushButton_2.setToolTip(_translate("CompPrintDialogBase", "Создать рамку слева"))
        self.pushButton_6.setToolTip(_translate("CompPrintDialogBase", "Создать новую начальную рамку"))
        self.pushButton_7.setToolTip(_translate("CompPrintDialogBase", "Создать макет для области карты в рамке"))

