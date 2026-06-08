# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_page_moria.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_page_moria(object):
    def setupUi(self, page_moria):
        if not page_moria.objectName():
            page_moria.setObjectName(u"page_moria")
        page_moria.resize(1009, 680)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(page_moria.sizePolicy().hasHeightForWidth())
        page_moria.setSizePolicy(sizePolicy)
        page_moria.setMinimumSize(QSize(781, 483))
        page_moria.setMaximumSize(QSize(1009, 16777215))
        self.verticalLayout = QVBoxLayout(page_moria)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.scrollArea = QScrollArea(page_moria)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMinimumSize(QSize(0, 200))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(-254, 0, 1226, 768))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox_3_1_4 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_3_1_4.addItem("")
        self.comboBox_3_1_4.addItem("")
        self.comboBox_3_1_4.addItem("")
        self.comboBox_3_1_4.setObjectName(u"comboBox_3_1_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBox_3_1_4.sizePolicy().hasHeightForWidth())
        self.comboBox_3_1_4.setSizePolicy(sizePolicy2)
        self.comboBox_3_1_4.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_3_1_4, 9, 1, 1, 1)

        self.lineEdit_epileximos = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_epileximos.setObjectName(u"lineEdit_epileximos")
        sizePolicy2.setHeightForWidth(self.lineEdit_epileximos.sizePolicy().hasHeightForWidth())
        self.lineEdit_epileximos.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_epileximos, 19, 2, 1, 1)

        self.label_16 = QLabel(self.scrollAreaWidgetContents)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 14, 0, 1, 1)

        self.label_17 = QLabel(self.scrollAreaWidgetContents)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 15, 0, 1, 1)

        self.label_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 11, 0, 1, 1)

        self.comboBox_3_1_2 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_3_1_2.addItem("")
        self.comboBox_3_1_2.addItem("")
        self.comboBox_3_1_2.addItem("")
        self.comboBox_3_1_2.setObjectName(u"comboBox_3_1_2")
        sizePolicy2.setHeightForWidth(self.comboBox_3_1_2.sizePolicy().hasHeightForWidth())
        self.comboBox_3_1_2.setSizePolicy(sizePolicy2)
        self.comboBox_3_1_2.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_3_1_2, 7, 1, 1, 1)

        self.lineEdit_2_1 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_2_1.setObjectName(u"lineEdit_2_1")
        sizePolicy2.setHeightForWidth(self.lineEdit_2_1.sizePolicy().hasHeightForWidth())
        self.lineEdit_2_1.setSizePolicy(sizePolicy2)
        self.lineEdit_2_1.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_2_1, 4, 1, 1, 1)

        self.lineEdit_5_1_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_5_1_moria.setObjectName(u"lineEdit_5_1_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_5_1_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_5_1_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_5_1_moria, 15, 2, 1, 1)

        self.lineEdit_6_1_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_6_1_moria.setObjectName(u"lineEdit_6_1_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_6_1_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_6_1_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_6_1_moria, 16, 2, 1, 1)

        self.lineEdit_2_2_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_2_2_moria.setObjectName(u"lineEdit_2_2_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_2_2_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_2_2_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_2_2_moria, 5, 2, 1, 1)

        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 9, 0, 1, 1)

        self.lineEdit_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_moria.setObjectName(u"lineEdit_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_moria, 18, 2, 1, 1)

        self.lineEdit_3_1_4_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3_1_4_moria.setObjectName(u"lineEdit_3_1_4_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_3_1_4_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_3_1_4_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_3_1_4_moria, 9, 2, 1, 1)

        self.label_14 = QLabel(self.scrollAreaWidgetContents)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 12, 0, 1, 1)

        self.comboBox_1_1 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_1_1.addItem("")
        self.comboBox_1_1.addItem("")
        self.comboBox_1_1.addItem("")
        self.comboBox_1_1.setObjectName(u"comboBox_1_1")
        sizePolicy2.setHeightForWidth(self.comboBox_1_1.sizePolicy().hasHeightForWidth())
        self.comboBox_1_1.setSizePolicy(sizePolicy2)
        self.comboBox_1_1.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_1_1, 2, 1, 1, 1)

        self.comboBox_7_1 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_7_1.addItem("")
        self.comboBox_7_1.addItem("")
        self.comboBox_7_1.addItem("")
        self.comboBox_7_1.setObjectName(u"comboBox_7_1")
        sizePolicy2.setHeightForWidth(self.comboBox_7_1.sizePolicy().hasHeightForWidth())
        self.comboBox_7_1.setSizePolicy(sizePolicy2)
        self.comboBox_7_1.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_7_1, 17, 1, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_20 = QLabel(self.scrollAreaWidgetContents)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 18, 1, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)

        self.lineEdit_5_1 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_5_1.setObjectName(u"lineEdit_5_1")
        sizePolicy2.setHeightForWidth(self.lineEdit_5_1.sizePolicy().hasHeightForWidth())
        self.lineEdit_5_1.setSizePolicy(sizePolicy2)
        self.lineEdit_5_1.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_5_1, 15, 1, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.lineEdit_3_5_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3_5_moria.setObjectName(u"lineEdit_3_5_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_3_5_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_3_5_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_3_5_moria, 13, 2, 1, 1)

        self.lineEdit_3_1_1 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3_1_1.setObjectName(u"lineEdit_3_1_1")
        sizePolicy2.setHeightForWidth(self.lineEdit_3_1_1.sizePolicy().hasHeightForWidth())
        self.lineEdit_3_1_1.setSizePolicy(sizePolicy2)
        self.lineEdit_3_1_1.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_3_1_1, 6, 1, 1, 1)

        self.lineEdit_3_1_2_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3_1_2_moria.setObjectName(u"lineEdit_3_1_2_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_3_1_2_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_3_1_2_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_3_1_2_moria, 7, 2, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.lineEdit_budget = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_budget.setObjectName(u"lineEdit_budget")
        self.lineEdit_budget.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lineEdit_budget.sizePolicy().hasHeightForWidth())
        self.lineEdit_budget.setSizePolicy(sizePolicy3)
        self.lineEdit_budget.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.lineEdit_budget, 1, 2, 1, 1)

        self.lineEdit_3_1_1_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3_1_1_moria.setObjectName(u"lineEdit_3_1_1_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_3_1_1_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_3_1_1_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_3_1_1_moria, 6, 2, 1, 1)

        self.lineEdit_7_1_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_7_1_moria.setObjectName(u"lineEdit_7_1_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_7_1_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_7_1_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_7_1_moria, 17, 2, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.lineEdit_1_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_1_2.setObjectName(u"lineEdit_1_2")
        sizePolicy2.setHeightForWidth(self.lineEdit_1_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_1_2.setSizePolicy(sizePolicy2)
        self.lineEdit_1_2.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_1_2, 3, 1, 1, 1)

        self.label_19 = QLabel(self.scrollAreaWidgetContents)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout.addWidget(self.label_19, 17, 0, 1, 1)

        self.label_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 10, 0, 1, 1)

        self.lineEdit_2_1_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_2_1_moria.setObjectName(u"lineEdit_2_1_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_2_1_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_2_1_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_2_1_moria, 4, 2, 1, 1)

        self.comboBox_3_5 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_3_5.addItem("")
        self.comboBox_3_5.addItem("")
        self.comboBox_3_5.addItem("")
        self.comboBox_3_5.setObjectName(u"comboBox_3_5")
        sizePolicy2.setHeightForWidth(self.comboBox_3_5.sizePolicy().hasHeightForWidth())
        self.comboBox_3_5.setSizePolicy(sizePolicy2)
        self.comboBox_3_5.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_3_5, 13, 1, 1, 1)

        self.lineEdit_2_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_2_2.setObjectName(u"lineEdit_2_2")
        sizePolicy2.setHeightForWidth(self.lineEdit_2_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2_2.setSizePolicy(sizePolicy2)
        self.lineEdit_2_2.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_2_2, 5, 1, 1, 1)

        self.lineEdit_3_1_3_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3_1_3_moria.setObjectName(u"lineEdit_3_1_3_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_3_1_3_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_3_1_3_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_3_1_3_moria, 8, 2, 1, 1)

        self.lineEdit_3_2_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3_2_moria.setObjectName(u"lineEdit_3_2_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_3_2_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_3_2_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_3_2_moria, 10, 2, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 19, 1, 1, 1)

        self.comboBox_3_1_3 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_3_1_3.addItem("")
        self.comboBox_3_1_3.addItem("")
        self.comboBox_3_1_3.addItem("")
        self.comboBox_3_1_3.setObjectName(u"comboBox_3_1_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBox_3_1_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3_1_3.setSizePolicy(sizePolicy4)
        self.comboBox_3_1_3.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_3_1_3, 8, 1, 1, 1)

        self.lineEdit_1_2_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_1_2_moria.setObjectName(u"lineEdit_1_2_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_1_2_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_1_2_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_1_2_moria, 3, 2, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)

        self.comboBox_6_1 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_6_1.addItem("")
        self.comboBox_6_1.addItem("")
        self.comboBox_6_1.addItem("")
        self.comboBox_6_1.setObjectName(u"comboBox_6_1")
        sizePolicy2.setHeightForWidth(self.comboBox_6_1.sizePolicy().hasHeightForWidth())
        self.comboBox_6_1.setSizePolicy(sizePolicy2)
        self.comboBox_6_1.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_6_1, 16, 1, 1, 1)

        self.lineEdit_1_1_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_1_1_moria.setObjectName(u"lineEdit_1_1_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_1_1_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_1_1_moria.setSizePolicy(sizePolicy2)
        self.lineEdit_1_1_moria.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.lineEdit_1_1_moria, 2, 2, 1, 1)

        self.label_15 = QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 13, 0, 1, 1)

        self.comboBox_3_3 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_3_3.addItem("")
        self.comboBox_3_3.addItem("")
        self.comboBox_3_3.addItem("")
        self.comboBox_3_3.addItem("")
        self.comboBox_3_3.addItem("")
        self.comboBox_3_3.setObjectName(u"comboBox_3_3")
        sizePolicy2.setHeightForWidth(self.comboBox_3_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3_3.setSizePolicy(sizePolicy2)
        self.comboBox_3_3.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_3_3, 11, 1, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_4_1_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_4_1_moria.setObjectName(u"lineEdit_4_1_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_4_1_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_4_1_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_4_1_moria, 14, 2, 1, 1)

        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout.addWidget(self.label_18, 16, 0, 1, 1)

        self.lineEdit_4_1 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_4_1.setObjectName(u"lineEdit_4_1")
        sizePolicy2.setHeightForWidth(self.lineEdit_4_1.sizePolicy().hasHeightForWidth())
        self.lineEdit_4_1.setSizePolicy(sizePolicy2)
        self.lineEdit_4_1.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_4_1, 14, 1, 1, 1)

        self.lineEdit_3_3_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3_3_moria.setObjectName(u"lineEdit_3_3_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_3_3_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_3_3_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_3_3_moria, 11, 2, 1, 1)

        self.lineEdit_3_4_moria = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3_4_moria.setObjectName(u"lineEdit_3_4_moria")
        sizePolicy2.setHeightForWidth(self.lineEdit_3_4_moria.sizePolicy().hasHeightForWidth())
        self.lineEdit_3_4_moria.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_3_4_moria, 12, 2, 1, 1)

        self.comboBox_3_4 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_3_4.addItem("")
        self.comboBox_3_4.addItem("")
        self.comboBox_3_4.addItem("")
        self.comboBox_3_4.addItem("")
        self.comboBox_3_4.addItem("")
        self.comboBox_3_4.addItem("")
        self.comboBox_3_4.setObjectName(u"comboBox_3_4")
        sizePolicy2.setHeightForWidth(self.comboBox_3_4.sizePolicy().hasHeightForWidth())
        self.comboBox_3_4.setSizePolicy(sizePolicy2)
        self.comboBox_3_4.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_3_4, 12, 1, 1, 1)

        self.comboBox_3_2 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_3_2.addItem("")
        self.comboBox_3_2.addItem("")
        self.comboBox_3_2.addItem("")
        self.comboBox_3_2.addItem("")
        self.comboBox_3_2.addItem("")
        self.comboBox_3_2.setObjectName(u"comboBox_3_2")
        sizePolicy2.setHeightForWidth(self.comboBox_3_2.sizePolicy().hasHeightForWidth())
        self.comboBox_3_2.setSizePolicy(sizePolicy2)
        self.comboBox_3_2.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.comboBox_3_2, 10, 1, 1, 1)

        self.label_21 = QLabel(self.scrollAreaWidgetContents)
        self.label_21.setObjectName(u"label_21")
        sizePolicy2.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_21, 1, 1, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(page_moria)

        QMetaObject.connectSlotsByName(page_moria)
    # setupUi

    def retranslateUi(self, page_moria):
        page_moria.setWindowTitle(QCoreApplication.translate("page_moria", u"Form", None))
        self.comboBox_3_1_4.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_3_1_4.setItemText(1, QCoreApplication.translate("page_moria", u"\u039d\u03b1\u03b9", None))
        self.comboBox_3_1_4.setItemText(2, QCoreApplication.translate("page_moria", u"\u038c\u03c7\u03b9", None))

        self.label_16.setText(QCoreApplication.translate("page_moria", u"4.1 \u0391\u03be\u03b9\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03ba\u03b1\u03b9 \u03b2\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03b7 \u03ba\u03b1\u03c4\u03b7\u03b3\u03bf\u03c1\u03af\u03b1 \u03b5\u03c0\u03b5\u03bd\u03b4\u03c5\u03c4\u03b9\u03ba\u03ce\u03bd \u03b4\u03b1\u03c0\u03b1\u03bd\u03ce\u03bd. 1. \u0395\u03c0\u03b5\u03bd\u03b4\u03cd\u03c3\u03b5\u03b9\u03c2 \u03c3\u03b5 \u0391\u03a0\u0395, 2. \u03a3\u03c4\u03b1\u03b2\u03bb\u03b9\u03ba\u03ad\u03c2 \u03b5\u03b3\u03ba\u03b1\u03c4\u03b1\u03c3\u03c4\u03ac\u03c3\u03b5\u03b9\u03c2 \u03ba\u03b1\u03b9 \u03b5\u03be\u03bf\u03c0\u03bb\u03b9\u03c3\u03bc\u03cc\u03c2 \u03b6\u03c9\u03b9\u03ba\u03ae\u03c2 \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03ae\u03c2, \u03c3\u03b9\u03bb\u03cc \u03b1\u03c0\u03bf\u03b8\u03ae\u03ba\u03b5\u03c5\u03c3\u03b7\u03c2 \u03b6\u03c9\u03bf\u03c4\u03c1\u03bf\u03c6\u03ce\u03bd\n"
" \u03ba\u03b1\u03b9 \u03b1\u03bc\u03b5\u03bb\u03ba\u03c4\u03b9\u03ba\u03ad\u03c2 \u03bc\u03b7\u03c7\u03b1\u03bd\u03ad\u03c2"
                        ", 3. \u0398\u03b5\u03c1\u03bc\u03bf\u03ba\u03ae\u03c0\u03b9\u03b1, \u03b4\u03b9\u03ba\u03c4\u03c5\u03bf\u03ba\u03ae\u03c0\u03b9\u03b1, \u03b5\u03b3\u03ba\u03b1\u03c4\u03b1\u03c3\u03c4\u03ac\u03c3\u03b5\u03b9\u03c2 \u03c6\u03c5\u03c4\u03b9\u03ba\u03ae\u03c2 \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03ae\u03c2 \u03c4\u03cd\u03c0\u03bf\u03c5 \u03c4\u03bf\u03bb (\u03c0\u03af\u03bd\u03b1\u03ba\u03b1 9.2\u03b1  \u03c4\u03bf\u03c5 \u03c0\u03b1\u03c1. 9 \u03c4\u03b7\u03c2 \u03a5\u0391) \u03ba\u03b1\u03b9 \u03b5\u03be\u03bf\u03c0\u03bb\u03b9\u03c3\u03bc\u03cc\u03c2 \u03c4\u03bf\u03c5\u03c2,  4. \u0395\u03c0\u03b5\u03bd\u03b4\u03cd\u03c3\u03b5\u03b9\u03c2 \u03c0\u03bf\u03c5 \u03b1\u03c6\u03bf\u03c1\u03bf\u03cd\u03bd \n"
"\u03c3\u03c4\u03b7\u03bd \u03c0\u03c1\u03bf\u03b5\u03c4\u03bf\u03b9\u03bc\u03b1\u03c3\u03af\u03b1 \u03b3\u03b9\u03b1 \u03c0\u03c1\u03ce\u03c4\u03b7 \u03c0\u03ce\u03bb\u03b7\u03c3\u03b7 (\u03ba\u03c4\u03af\u03c1\u03b9\u03b1 \u03ba\u03b1\u03b9 \u03b5\u03be\u03bf\u03c0\u03bb\u03b9\u03c3\u03bc\u03cc\u03c2"
                        "), 5. \u0395\u03b3\u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7 \u03bd\u03ad\u03c9\u03bd \u03c6\u03c5\u03c4\u03b5\u03b9\u03ce\u03bd, 6. \u0395\u03c0\u03b5\u03bd\u03b4\u03cd\u03c3\u03b5\u03b9\u03c2 \u03c0\u03bf\u03c5 \u03b1\u03c6\u03bf\u03c1\u03bf\u03cd\u03bd \u03c3\u03b5 \u03b1\u03c0\u03bf\u03b8\u03b7\u03ba\u03b5\u03c5\u03c4\u03b9\u03ba\u03bf\u03cd\u03c2 \u03c7\u03ce\u03c1\u03bf\u03c5\u03c2 (\u03ba\u03c4\u03af\u03c1\u03b9\u03b1 \u03ba\u03b1\u03b9 \u03bc\u03b7\u03c7\u03b1\u03bd\u03bf\u03bb\u03bf\u03b3\u03b9\u03ba\u03cc\u03c2 \u03b5\u03be\u03bf\u03c0\u03bb\u03b9\u03c3\u03bc\u03cc\u03c2 \n"
"\u03bb\u03b5\u03b9\u03c4\u03bf\u03c5\u03c1\u03b3\u03af\u03b1\u03c2 \u03c4\u03bf\u03c5\u03c2) \u03c0\u03c1\u03bf\u03ca\u03cc\u03bd\u03c4\u03c9\u03bd \u03c4\u03b7\u03c2 \u03b5\u03ba\u03bc\u03b5\u03c4\u03ac\u03bb\u03bb\u03b5\u03c5\u03c3\u03b7\u03c2, 7. \u0391\u03b3\u03bf\u03c1\u03ac \u03b1\u03b3\u03c1\u03bf\u03c4\u03b5\u03bc\u03b1\u03c7\u03af\u03bf\u03c5 \u03cc\u03bc\u03bf\u03c1\u03bf\u03c5 \u03c0\u03c1\u03bf\u03c2 \u03b9"
                        "\u03b4\u03b9\u03cc\u03ba\u03c4\u03b7\u03c4\u03bf \u03b1\u03b3\u03c1\u03bf\u03c4\u03b5\u03bc\u03ac\u03c7\u03b9\u03bf\n"
"", None))
        self.label_17.setText(QCoreApplication.translate("page_moria", u"5.1 \u0391\u03be\u03b9\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03ba\u03b1\u03b9 \u03b2\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03b7 \u03ba\u03b1\u03b9\u03bd\u03bf\u03c4\u03bf\u03bc\u03af\u03b1 \u03c4\u03c9\u03bd \u03b5\u03c0\u03b5\u03bd\u03b4\u03c5\u03c4\u03b9\u03ba\u03ce\u03bd \u03b4\u03b1\u03c0\u03b1\u03bd\u03ce\u03bd \u03bc\u03b5 \u03c0\u03c1\u03bf\u03c4\u03b5\u03c1\u03b1\u03b9\u03cc\u03c4\u03b7\u03c4\u03b1 \u03c3\u03b5 \u03b1\u03c5\u03c4\u03ad\u03c2 \u03c0\u03bf\u03c5 \u03b1\u03c6\u03bf\u03c1\u03bf\u03cd\u03bd \u03c3\u03b5 \u03b3\u03b5\u03c9\u03c1\u03b3\u03af\u03b1 \u03b1\u03ba\u03c1\u03b9\u03b2\u03b5\u03af\u03b1\u03c2 \u03ba\u03b1\u03b9 \u03c4\u03b7\u03bd \u03ad\u03be\u03c5\u03c0\u03bd\u03b7 \u03b3\u03b5\u03c9\u03c1\u03b3\u03af\u03b1. ", None))
        self.label_13.setText(QCoreApplication.translate("page_moria", u"3.3 \u0391\u03be\u03b9\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03ba\u03b1\u03b9 \u03b2\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03c4\u03bf \u03b5\u03c0\u03af\u03c0\u03b5\u03b4\u03bf \u03b5\u03ba\u03c0\u03b1\u03af\u03b4\u03b5\u03c5\u03c3\u03b7\u03c2 \u03c4\u03bf\u03c5 \u03c5\u03c0\u03bf\u03c8\u03b7\u03c6\u03af\u03bf\u03c5\n"
"", None))
        self.comboBox_3_1_2.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_3_1_2.setItemText(1, QCoreApplication.translate("page_moria", u"\u039d\u03b1\u03b9", None))
        self.comboBox_3_1_2.setItemText(2, QCoreApplication.translate("page_moria", u"\u038c\u03c7\u03b9", None))

        self.label_10.setText(QCoreApplication.translate("page_moria", u"3.1.4 \u038e\u03c0\u03b1\u03c1\u03be\u03b7 \u03ba\u03b5\u03c1\u03b4\u03bf\u03c6\u03bf\u03c1\u03af\u03b1\u03c2 \u03ba\u03b1\u03c4\u03ac \u03c4\u03b9\u03c2 3 \u03c4\u03b5\u03bb\u03b5\u03c5\u03c4\u03b1\u03af\u03b5\u03c2 \u03b4\u03b9\u03b1\u03c7\u03b5\u03b9\u03c1\u03b9\u03c3\u03c4\u03b9\u03ba\u03ad\u03c2 \u03c7\u03c1\u03ae\u03c3\u03b5\u03b9\u03c2 (\u03bc\u03ad\u03c3\u03bf\u03c2 \u03cc\u03c1\u03bf\u03c2 3\u03b5\u03c4\u03af\u03b1\u03c2) \u03c0\u03c1\u03bf \u03c6\u03cc\u03c1\u03c9\u03bd \u03ba\u03b1\u03b9 \u03b1\u03c0\u03bf\u03c3\u03b2\u03ad\u03c3\u03b5\u03c9\u03bd\n"
"", None))
        self.label_14.setText(QCoreApplication.translate("page_moria", u"3.4 \u0391\u03be\u03b9\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03ba\u03b1\u03b9 \u03b2\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03bf \u03b2\u03b1\u03b8\u03bc\u03cc\u03c2 \u03c3\u03c5\u03bc\u03bc\u03b5\u03c4\u03bf\u03c7\u03ae\u03c2 \u03c4\u03bf\u03c5 \u03c5\u03c0\u03bf\u03c8\u03b7\u03c6\u03af\u03bf\u03c5 \u03c3\u03b5 \u03c3\u03c5\u03bb\u03bb\u03bf\u03b3\u03b9\u03ba\u03ac \u03c3\u03c7\u03ae\u03bc\u03b1\u03c4\u03b1 \u03ba\u03b1\u03b9 \u03c3\u03c5\u03bd\u03b5\u03c4\u03b1\u03b9\u03c1\u03b9\u03c3\u03bc\u03bf\u03cd\u03c2. \u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5 \u03b1\u03bd \u03bf \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03cc\u03c2 \u03b5\u03af\u03bd\u03b1\u03b9 \u03bc\u03ad\u03bb\u03bf\u03c2 \u03c3\u03b5 \u03ba\u03ac\u03c0\u03bf\u03b9\u03bf \u03c3\u03c5\u03bb\u03bb\u03bf\u03b3\u03b9\u03ba\u03cc \u03c3\u03c7\u03ae\u03bc\u03b1\n"
"", None))
        self.comboBox_1_1.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_1_1.setItemText(1, QCoreApplication.translate("page_moria", u"\u039d\u03b1\u03b9", None))
        self.comboBox_1_1.setItemText(2, QCoreApplication.translate("page_moria", u"\u038c\u03c7\u03b9", None))

        self.comboBox_7_1.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_7_1.setItemText(1, QCoreApplication.translate("page_moria", u"\u039d\u03b1\u03b9", None))
        self.comboBox_7_1.setItemText(2, QCoreApplication.translate("page_moria", u"\u038c\u03c7\u03b9", None))

        self.label_3.setText(QCoreApplication.translate("page_moria", u"1.1 \u0392\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03cc\u03c4\u03b1\u03bd \u03c4\u03bf \u03c0\u03bf\u03c3\u03bf\u03c3\u03c4\u03cc \u03c4\u03b7\u03c2 \u03c4\u03c5\u03c0\u03b9\u03ba\u03ae\u03c2 \u03b1\u03c0\u03cc\u03b4\u03bf\u03c3\u03b7\u03c2 \u03c4\u03b7\u03c2 \u03b5\u03ba\u03bc\u03b5\u03c4\u03ac\u03bb\u03bb\u03b5\u03c5\u03c3\u03b7\u03c2 \u03c3\u03c4\u03b7\u03bd \u03c5\u03c6\u03b9\u03c3\u03c4\u03ac\u03bc\u03b5\u03bd\u03b7 \u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7 (\u0395\u0391\u0395 2022) \u03c0\u03bf\u03c5 \u03c0\u03c1\u03bf\u03ad\u03c1\u03c7\u03b5\u03c4\u03b1\u03b9 \u03b1\u03c0\u03cc \u03c4\u03b7\u03bd \u03b1\u03b9\u03b3\u03bf-\u03c0\u03c1\u03bf\u03b2\u03b1\u03c4\u03bf\u03c4\u03c1\u03bf\u03c6\u03af\u03b1 \u03ae/\u03ba\u03b1\u03b9 \u03c4\u03b7\u03bd \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03ae \n"
"\u03bf\u03c0\u03c9\u03c1\u03bf\u03ba\u03b7\u03c0\u03b5\u03c5\u03c4\u03b9\u03ba\u03ce\u03bd \u03ae/\u03ba\u03b1\u03b9 \u03c4\u03b9\u03c2 \u03ba\u03b1\u03bb\u03bb\u03b9"
                        "\u03ad\u03c1\u03b3\u03b5\u03b9\u03b5\u03c2 \u03ba\u03b1\u03b9 \u03c4\u03b9\u03c2 \u03b5\u03ba\u03c4\u03c1\u03bf\u03c6\u03ad\u03c2 \u03c0\u03bf\u03c5 \u03c3\u03c5\u03bc\u03b2\u03ac\u03bb\u03bb\u03bf\u03c5\u03bd \u03c3\u03c4\u03b7\u03bd \u03b5\u03c0\u03b9\u03c3\u03b9\u03c4\u03b9\u03c3\u03c4\u03b9\u03ba\u03ae \u03b5\u03c0\u03ac\u03c1\u03ba\u03b5\u03b9\u03b1 \u03ba\u03b1\u03b9 \u03b1\u03c3\u03c6\u03ac\u03bb\u03b5\u03b9\u03b1 \u03ae/\u03ba\u03b1\u03b9 \u03c4\u03b7\u03bd \u03b5\u03bb\u03b1\u03b9\u03bf\u03ba\u03b1\u03bb\u03bb\u03b9\u03ad\u03c1\u03b3\u03b5\u03b9\u03b1 \u03ae/\u03ba\u03b1\u03b9 \u03c4\u03b7\u03bd \u03bc\u03b5\u03bb\u03b9\u03c3\u03c3\u03bf\u03ba\u03bf\u03bc\u03af\u03b1 \u03ae/\u03ba\u03b1\u03b9 \u03c4\u03bf \u03b2\u03b1\u03bc\u03b2\u03ac\u03ba\u03b9 \n"
"\u03ae/\u03ba\u03b1\u03b9 \u03c4\u03b7\u03bd \u03b1\u03bc\u03c0\u03b5\u03bb\u03bf\u03ba\u03b1\u03bb\u03bb\u03b9\u03ad\u03c1\u03b3\u03b5\u03b9\u03b1 \u03ae/\u03ba\u03b1\u03b9 \u03c4\u03b9\u03c2 \u03b1\u03bd\u03b8\u03b5\u03ba\u03c4\u03b9\u03ba\u03ad\u03c2"
                        " \u03c3\u03c4\u03b7\u03bd \u03ba\u03bb\u03b9\u03bc\u03b1\u03c4\u03b9\u03ba\u03ae \u03b1\u03bb\u03bb\u03b1\u03b3\u03ae \u03ba\u03b1\u03bb\u03bb\u03b9\u03ad\u03c1\u03b3\u03b5\u03b9\u03b5\u03c2 \u03ae \u03c3\u03c5\u03bc\u03b2\u03ac\u03bb\u03b5\u03b9 \u03c3\u03c4\u03b7\u03bd \u03ac\u03bc\u03b2\u03bb\u03c5\u03bd\u03c3\u03b7 \u03c4\u03c9\u03bd \u03b5\u03c0\u03b9\u03c0\u03c4\u03ce\u03c3\u03b5\u03c9\u03bd \u03c4\u03b7\u03c2 \u03ba\u03bb\u03b9\u03bc\u03b1\u03c4\u03b9\u03ba\u03ae\u03c2 \u03b1\u03bb\u03bb\u03b1\u03b3\u03ae\u03c2 \u03c5\u03c0\u03b5\u03c1\u03b2\u03b1\u03af\u03bd\u03b5\u03b9 \u03c4\u03bf 80% \u03c4\u03b7\u03c2 \u03c3\u03c5\u03bd\u03bf\u03bb\u03b9\u03ba\u03ae\u03c2 \n"
"\u03c4\u03c5\u03c0\u03b9\u03ba\u03ae\u03c2 \u03b1\u03c0\u03cc\u03b4\u03bf\u03c3\u03b7\u03c2 \u03c4\u03b7\u03c2 \u03b5\u03ba\u03bc\u03b5\u03c4\u03ac\u03bb\u03bb\u03b5\u03c5\u03c3\u03b7\u03c2\n"
"", None))
        self.label_20.setText(QCoreApplication.translate("page_moria", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">\u03a3\u03c5\u03bd\u03bf\u03bb\u03b9\u03ba\u03ae \u03b2\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03af\u03b1</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("page_moria", u"3.1.1 \u03a4\u03b5\u03ba\u03bc\u03b7\u03c1\u03b9\u03c9\u03bc\u03ad\u03bd\u03b7 \u03b9\u03ba\u03b1\u03bd\u03cc\u03c4\u03b7\u03c4\u03b1 \u03ba\u03ac\u03bb\u03c5\u03c8\u03b7\u03c2 \u03c4\u03bf\u03c5 \u03b1\u03b9\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd\u03bf\u03c5 \u03c0\u03c1\u03bf\u03cb\u03c0\u03bf\u03bb\u03bf\u03b3\u03b9\u03c3\u03bc\u03bf\u03cd \u03ba\u03b1\u03c4\u03ac \u03c4\u03b7\u03bd \u03c5\u03c0\u03bf\u03b2\u03bf\u03bb\u03ae \u03c4\u03b7\u03c2 \u03b1\u03af\u03c4\u03b7\u03c3\u03b7\u03c2 \u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7\u03c2. \u0391\u03c0\u03bf\u03b4\u03af\u03b4\u03bf\u03bd\u03c4\u03b1\u03b9 20 \u03bc\u03cc\u03c1\u03b9\u03b1 \u03b5\u03c6\u03cc\u03c3\u03bf\u03bd \u03b7 \u03b9\u03ba\u03b1\u03bd\u03cc\u03c4\u03b7\u03c4\u03b1 \u03ba\u03ac\u03bb\u03c5\u03c8\u03b7\u03c2 \u03c4\u03bf\u03c5 \u03b1\u03b9\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd\u03bf\u03c5 \n"
"\u03c0/\u03c5 \u03bc\u03b5 \u03af\u03b4\u03b9\u03b1 \u03ba\u03b5\u03c6\u03ac\u03bb\u03b1\u03b9\u03b1 \u03c5\u03c0\u03b5\u03c1\u03b2\u03b1\u03af\u03bd\u03b5\u03b9"
                        " \u03c4\u03bf 20% \u03ba\u03b1\u03b9 \u03ad\u03c9\u03c2 50 \u03bc\u03cc\u03c1\u03b9\u03b1 (\u03b1\u03bd\u03b1\u03bb\u03bf\u03b3\u03b9\u03ba\u03ac) \u03b5\u03c6\u03cc\u03c3\u03bf\u03bd \u03c5\u03c0\u03b5\u03c1\u03b2\u03b1\u03af\u03bd\u03b5\u03b9 50% \u03c4\u03bf\u03c5 \u03b1\u03b9\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd\u03bf\u03c5 \u03c0/\u03c5\n"
" ", None))
        self.label_4.setText(QCoreApplication.translate("page_moria", u"1.2 E\u03ba\u03bc\u03b5\u03c4\u03b1\u03bb\u03bb\u03b5\u03cd\u03c3\u03b5\u03b9\u03c2 \u03bf\u03b9 \u03bf\u03c0\u03bf\u03af\u03b5\u03c2 \u03b4\u03b9\u03b1\u03b8\u03ad\u03c4\u03bf\u03c5\u03bd \u03c0\u03b9\u03c3\u03c4\u03bf\u03c0\u03bf\u03af\u03b7\u03c3\u03b7 \u03b2\u03b9\u03bf\u03bb\u03bf\u03b3\u03b9\u03ba\u03ce\u03bd \u03ae/\u03ba\u03b1\u03b9 \u03b5\u03bd\u03c9\u03c3\u03b9\u03b1\u03ba\u03ce\u03bd/\u03b5\u03b8\u03bd\u03b9\u03ba\u03ce\u03bd/\u03bb\u03bf\u03b9\u03c0\u03ce\u03bd \u03c3\u03c5\u03c3\u03c4\u03b7\u03bc\u03ac\u03c4\u03c9\u03bd \u03c0\u03bf\u03b9\u03cc\u03c4\u03b7\u03c4\u03b1\u03c2 \u03b7 \u03bf\u03c0\u03bf\u03af\u03b1 \u03ba\u03ac\u03bb\u03c5\u03c0\u03c4\u03b5 \u03c4\u03b9\u03c2 \u03ba\u03b1\u03bb\u03bb\u03b9\u03ad\u03c1\u03b3\u03b5\u03b9\u03b5\u03c2 / \u03b5\u03ba\u03c4\u03c1\u03bf\u03c6\u03ad\u03c2 \u03c0\u03bf\u03c5 \u03b4\u03b7\u03bb\u03ce\u03b8\u03b7\u03ba\u03b1\u03bd \n"
"\u03c3\u03c4\u03b7\u03bd \u0395\u0391\u0395 \u03c4\u03bf\u03c5 \u03ad\u03c4\u03bf\u03c5\u03c2 2022. \u0392\u03b1\u03b8\u03bc\u03bf"
                        "\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03b5\u03c6\u03cc\u03c3\u03bf\u03bd \u03b7 \u03c4\u03c5\u03c0\u03b9\u03ba\u03ae \u03b1\u03c0\u03cc\u03b4\u03bf\u03c3\u03b7 \u03c4\u03c9\u03bd \u03c0\u03b9\u03c3\u03c4\u03bf\u03c0\u03bf\u03b9\u03b7\u03bc\u03ad\u03bd\u03c9\u03bd \u03ba\u03b1\u03bb\u03bb\u03b9\u03b5\u03c1\u03b3\u03b5\u03b9\u03ce\u03bd / \u03b5\u03ba\u03c4\u03c1\u03bf\u03c6\u03ce\u03bd \u03c5\u03c0\u03b5\u03c1\u03b2\u03b1\u03af\u03bd\u03b5\u03b9, \u03b1\u03b8\u03c1\u03bf\u03b9\u03c3\u03c4\u03b9\u03ba\u03ac, \u03c4\u03bf 50% \u03c4\u03b7\u03c2 \u03c3\u03c5\u03bd\u03bf\u03bb\u03b9\u03ba\u03ae\u03c2 \u03c4\u03c5\u03c0\u03b9\u03ba\u03ae\u03c2 \u03b1\u03c0\u03cc\u03b4\u03bf\u03c3\u03b7\u03c2 \u03c4\u03b7\u03c2 \n"
"\u03c5\u03c6\u03b9\u03c3\u03c4\u03ac\u03bc\u03b5\u03bd\u03b7\u03c2 \u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7\u03c2 (\u0395\u0391\u0395 2022). (\u03c3\u03c5\u03bc\u03c0\u03b5\u03c1\u03b9\u03bb\u03b1\u03bc\u03b2\u03ac\u03bd\u03bf\u03bd\u03c4\u03b1\u03b9 \u03a0\u039f\u03a0/\u03a0\u0393"
                        "\u0395)\n"
"", None))
        self.label_6.setText(QCoreApplication.translate("page_moria", u"2.2 \u0392\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03bf\u03cd\u03bd\u03c4\u03b1\u03b9 \u03b5\u03ba\u03bc\u03b5\u03c4\u03b1\u03bb\u03bb\u03b5\u03cd\u03c3\u03b5\u03b9\u03c2 \u03bc\u03b5 \u03c4\u03c5\u03c0\u03b9\u03ba\u03ae \u03b1\u03c0\u03cc\u03b4\u03bf\u03c3\u03b7 : \u03b1)\u03ad\u03c9\u03c2 \u03ba\u03b1\u03b9 15.000 \u20ac \u03c0\u03bf\u03c5 \u03c4\u03bf \u03cd\u03c8\u03bf\u03c2 \u03c4\u03c9\u03bd \u03b1\u03b9\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd\u03c9\u03bd \u03b5\u03c0\u03b5\u03bd\u03b4\u03cd\u03c3\u03b5\u03c9\u03bd \u03b4\u03b5\u03bd \u03be\u03b5\u03c0\u03b5\u03c1\u03bd\u03ac \u03c4\u03b1 75.000 \u20ac, \u03b2) \u03c0\u03ac\u03bd\u03c9 \u03b1\u03c0\u03cc 15.000 \u20ac \u03c0\u03bf\u03c5 \u03c4\u03bf \u03c3\u03cd\u03bd\u03bf\u03bb\u03bf\n"
" \u03c4\u03c9\u03bd \u03b1\u03b9\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd\u03c9\u03bd \u03b5\u03c0\u03b5\u03bd\u03b4\u03cd\u03c3\u03b5\u03c9\u03bd \u03b4\u03b5\u03bd \u03be\u03b5\u03c0\u03b5\u03c1\u03bd\u03bf\u03cd\u03bd \u03c0\u03b5\u03bd\u03c4\u03b1\u03c0\u03bb\u03ac\u03c3"
                        "\u03b9\u03bf \u03c4\u03b7\u03c2 \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03b9\u03ba\u03ae\u03c2 \u03b4\u03c5\u03bd\u03b1\u03bc\u03b9\u03ba\u03cc\u03c4\u03b7\u03c4\u03b1\u03c2, \u03b3)\u03c0\u03ac\u03bd\u03c9 \u03b1\u03c0\u03cc 12.500 \u20ac \u03c0\u03bf\u03c5 \u03c4\u03bf \u03c3\u03cd\u03bd\u03bf\u03bb\u03bf \u03c4\u03c9\u03bd \u03b1\u03b9\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd\u03c9\u03bd \u03b5\u03c0\u03b5\u03bd\u03b4\u03cd\u03c3\u03b5\u03c9\u03bd \u03b4\u03b5\u03bd \u03be\u03b5\u03c0\u03b5\u03c1\u03bd\u03bf\u03cd\u03bd \u03c4\u03bf \u03b5\u03be\u03b1\u03c0\u03bb\u03ac\u03c3\u03b9\u03bf \n"
"\u03c4\u03b7\u03c2 \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03b9\u03ba\u03ae\u03c2 \u03b4\u03c5\u03bd\u03b1\u03bc\u03b9\u03ba\u03cc\u03c4\u03b7\u03c4\u03b1\u03c2\n"
"", None))
        self.label_5.setText(QCoreApplication.translate("page_moria", u"2.1 \u0391\u03be\u03b9\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03c4\u03bf \u03bf\u03b9\u03ba\u03bf\u03bd\u03bf\u03bc\u03b9\u03ba\u03cc \u03bc\u03ad\u03b3\u03b5\u03b8\u03bf\u03c2 \u03c4\u03b7\u03c2 \u03b5\u03ba\u03bc\u03b5\u03c4\u03ac\u03bb\u03bb\u03b5\u03c5\u03c3\u03b7\u03c2 \u03c3\u03c4\u03b7\u03bd \u03c5\u03c6\u03b9\u03c3\u03c4\u03ac\u03bc\u03b5\u03bd\u03b7 \u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7 \u03c3\u03b5 \u03cc\u03c1\u03bf\u03c5\u03c2 \u03c4\u03c5\u03c0\u03b9\u03ba\u03ae\u03c2 \u03b1\u03c0\u03cc\u03b4\u03bf\u03c3\u03b7\u03c2. \u0395\u03ba\u03bc\u03b5\u03c4\u03ac\u03bb\u03bb\u03b5\u03c5\u03c3\u03b7 \u03bc\u03b5 \u03c4\u03c5\u03c0\u03b9\u03ba\u03ae \u03b1\u03c0\u03cc\u03b4\u03bf\u03c3\u03b7, \u03b2\u03ac\u03c3\u03b5\u03b9 \u03c4\u03b7\u03c2 \u0395\u0391\u0395 \u03c4\u03bf\u03c5 \u03ad\u03c4\u03bf\u03c5\u03c2 2025:\n"
" \u03b1) \u03ad\u03c9\u03c2 16.000\u20ac, \u03b2) \u03b1\u03c0\u03cc 16.000 \u03ad\u03c9\u03c2 25.000 \u20ac, \u03b3)  \u03ac\u03bd\u03c9 \u03c4\u03c9\u03bd 25"
                        ".000 \u20ac\n"
"", None))
        self.label_19.setText(QCoreApplication.translate("page_moria", u"7.1 \u0391\u03be\u03b9\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03ba\u03b1\u03b9 \u03b2\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03b7 \u03c0\u03c1\u03b1\u03b3\u03bc\u03b1\u03c4\u03bf\u03c0\u03bf\u03af\u03b7\u03c3\u03b7 \u03b5\u03c0\u03b5\u03bd\u03b4\u03cd\u03c3\u03b5\u03c9\u03bd \u03c3\u03b5 \u03b5\u03ba\u03bc\u03b5\u03c4\u03b1\u03bb\u03bb\u03b5\u03cd\u03c3\u03b5\u03b9\u03c2 \u03c0\u03b5\u03c1\u03b9\u03bf\u03c7\u03ce\u03bd \u03c0\u03bf\u03c5 \u03ad\u03c7\u03bf\u03c5\u03bd \u03ba\u03b7\u03c1\u03c5\u03c7\u03b8\u03b5\u03af \u03c0\u03c5\u03c1\u03cc\u03c0\u03bb\u03b7\u03ba\u03c4\u03b5\u03c2 ", None))
        self.label_12.setText(QCoreApplication.translate("page_moria", u"3.2 \u0391\u03be\u03b9\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03ba\u03b1\u03b9 \u03b2\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03b7 \u03b4\u03c5\u03bd\u03b1\u03bc\u03b9\u03ba\u03ae \u03c4\u03bf\u03c5 \u03c5\u03c0\u03bf\u03c8\u03b7\u03c6\u03af\u03bf\u03c5\n"
"", None))
        self.comboBox_3_5.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_3_5.setItemText(1, QCoreApplication.translate("page_moria", u"\u039d\u03b1\u03b9", None))
        self.comboBox_3_5.setItemText(2, QCoreApplication.translate("page_moria", u"\u038c\u03c7\u03b9", None))

        self.label_2.setText(QCoreApplication.translate("page_moria", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">\u0395\u03c0\u03b9\u03bb\u03b5\u03be\u03b9\u03bc\u03cc\u03c4\u03b7\u03c4\u03b1</span></p></body></html>", None))
        self.comboBox_3_1_3.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_3_1_3.setItemText(1, QCoreApplication.translate("page_moria", u"\u039d\u03b1\u03b9", None))
        self.comboBox_3_1_3.setItemText(2, QCoreApplication.translate("page_moria", u"\u038c\u03c7\u03b9", None))

        self.label_8.setText(QCoreApplication.translate("page_moria", u"3.1.2 \u038e\u03c0\u03b1\u03c1\u03be\u03b7 \u03c6\u03bf\u03c1\u03bf\u03bb\u03bf\u03b3\u03b9\u03ba\u03ae \u03ba\u03b1\u03b9 \u03b1\u03c3\u03c6\u03b1\u03bb\u03b9\u03c3\u03c4\u03b9\u03ba\u03ad\u03c2 \u03b5\u03bd\u03b7\u03bc\u03b5\u03c1\u03cc\u03c4\u03b7\u03c4\u03b5\u03c2 (\u03b3\u03b9\u03b1 \u03b5\u03af\u03c3\u03c0\u03c1\u03b1\u03be\u03b7 \u03c7\u03c1\u03b7\u03bc\u03ac\u03c4\u03c9\u03bd \u2013 \u03cc\u03c7\u03b9 \u03b3\u03b9\u03b1 \u03ba\u03ac\u03b8\u03b5 \u03bd\u03cc\u03bc\u03b9\u03bc\u03b7 \u03c7\u03c1\u03ae\u03c3\u03b7) \u03c7\u03c9\u03c1\u03af\u03c2 \u03c0\u03b1\u03c1\u03b1\u03ba\u03c1\u03b1\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd\u03b5\u03c2 \u03bf\u03c6\u03b5\u03b9\u03bb\u03ad\u03c2\n"
"", None))
        self.comboBox_6_1.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_6_1.setItemText(1, QCoreApplication.translate("page_moria", u"\u039d\u03b1\u03b9", None))
        self.comboBox_6_1.setItemText(2, QCoreApplication.translate("page_moria", u"\u038c\u03c7\u03b9", None))

        self.label_15.setText(QCoreApplication.translate("page_moria", u"3.5 \u0392\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03b7 \u03c3\u03c5\u03bc\u03bc\u03b5\u03c4\u03bf\u03c7\u03ae \u03c4\u03bf\u03c5 \u03c5\u03c0\u03bf\u03c8\u03ae\u03c6\u03b9\u03bf\u03c5 \u03c3\u03b5 \u03c3\u03c7\u03ae\u03bc\u03b1\u03c4\u03b1 \u03c3\u03c5\u03bc\u03b2\u03bf\u03bb\u03b1\u03b9\u03b1\u03ba\u03ae\u03c2 \u03b3\u03b5\u03c9\u03c1\u03b3\u03af\u03b1\u03c2 \u03c3\u03c4\u03b7\u03bd \u03c5\u03c6\u03b9\u03c3\u03c4\u03ac\u03bc\u03b5\u03bd\u03b7 \u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7\n"
"", None))
        self.comboBox_3_3.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_3_3.setItemText(1, QCoreApplication.translate("page_moria", u"\u039a\u03b1\u03c4\u03bf\u03c7\u03ae \u03c0\u03c4\u03c5\u03c7\u03af\u03bf\u03c5 >= 6, 7, 8", None))
        self.comboBox_3_3.setItemText(2, QCoreApplication.translate("page_moria", u"\u039a\u03b1\u03c4\u03bf\u03c7\u03ae \u03b3\u03b5\u03c9\u03c4\u03b5\u03c7\u03bd\u03b9\u03ba\u03bf\u03cd \u03c0\u03c4\u03c5\u03c7\u03af\u03bf\u03c5 =< 3, 4, 5", None))
        self.comboBox_3_3.setItemText(3, QCoreApplication.translate("page_moria", u"\u039a\u03b1\u03c4\u03bf\u03c7\u03ae \u03b3\u03b5\u03c9\u03c4\u03b5\u03c7\u03bd\u03b9\u03ba\u03bf\u03cd \u03c0\u03c4\u03c5\u03c7\u03af\u03bf\u03c5 >= 6, 7, 8", None))
        self.comboBox_3_3.setItemText(4, QCoreApplication.translate("page_moria", u"\u039a\u03b1\u03bd\u03ad\u03bd\u03b1 \u03b1\u03c0\u03cc \u03c4\u03b1 \u03c0\u03b1\u03c1\u03b1\u03c0\u03ac\u03bd\u03c9", None))

        self.label_9.setText(QCoreApplication.translate("page_moria", u"3.1.3 \u038e\u03c0\u03b1\u03c1\u03be\u03b7 \u03b1\u03b4\u03b5\u03b9\u03ce\u03bd \u03b1\u03c0\u03b1\u03c1\u03b1\u03af\u03c4\u03b7\u03c4\u03c9\u03bd \u03b3\u03b9\u03b1 \u03c4\u03b7\u03bd \u03c5\u03bb\u03bf\u03c0\u03bf\u03af\u03b7\u03c3\u03b7 \u03ba\u03b1\u03c4\u03ac \u03c4\u03b7\u03bd \u03c5\u03c0\u03bf\u03b2\u03bf\u03bb\u03ae \u03c4\u03b7\u03c2 \u03b1\u03af\u03c4\u03b7\u03c3\u03b7\u03c2 \u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7\u03c2\n"
"", None))
        self.label.setText(QCoreApplication.translate("page_moria", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">\u039a\u03a1\u0399\u03a4\u0397\u03a1\u0399\u0391 \u039c\u039f\u03a1\u0399\u039f\u0394\u039f\u03a4\u0397\u03a3\u0397\u03a3 \u03a5\u03a0\u039f\u03a8\u0397\u03a6\u0399\u039f\u03a5</span></p></body></html>", None))
        self.label_18.setText(QCoreApplication.translate("page_moria", u"6.1 \u0391\u03be\u03b9\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03ba\u03b1\u03b9 \u03b2\u03b1\u03b8\u03bc\u03bf\u03bb\u03bf\u03b3\u03b5\u03af\u03c4\u03b1\u03b9 \u03b7 \u03c3\u03c5\u03bc\u03bc\u03b5\u03c4\u03bf\u03c7\u03ae \u03c3\u03b5 \u03ba\u03bb\u03ac\u03b4\u03bf\u03c5\u03c2 (\u03c3\u03c4\u03b7\u03bd \u03c5\u03c6\u03b9\u03c3\u03c4\u03ac\u03bc\u03b5\u03bd\u03b7 \u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7) \u03c0\u03bf\u03c5 \u03b1\u03bd\u03b1\u03b4\u03b5\u03b9\u03ba\u03bd\u03cd\u03bf\u03bd\u03c4\u03b1\u03b9 \u03c3\u03c4\u03bf \u03c0\u03bb\u03b1\u03af\u03c3\u03b9\u03bf \u03c4\u03c9\u03bd \u03b9\u03b4\u03b9\u03b1\u03b9\u03c4\u03b5\u03c1\u03bf\u03c4\u03ae\u03c4\u03c9\u03bd \u03ba\u03b1\u03b9 \u03b1\u03bd\u03b1\u03b3\u03ba\u03ce\u03bd \u03c4\u03b7\u03c2 \u03ba\u03ac\u03b8\u03b5 \u03a0\u03b5\u03c1\u03b9\u03c6\u03ad\u03c1\u03b5\u03b9\u03b1\u03c2 \u03b1\u03bb\u03bb\u03ac \u03ba\u03b1\u03b9 \u03c4\u03b9\u03c2 \n"
"\u03c3\u03c4\u03c1\u03b1\u03c4\u03b7\u03b3\u03b9\u03ba\u03ad\u03c2 RIS3. ", None))
        self.comboBox_3_4.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_3_4.setItemText(1, QCoreApplication.translate("page_moria", u"\u039f\u03a0/\u039f\u03bc.\u03a0 \u03bc\u03b5 \u03bc\u03ad\u03bb\u03b7>10", None))
        self.comboBox_3_4.setItemText(2, QCoreApplication.translate("page_moria", u"\u0391\u03a3", None))
        self.comboBox_3_4.setItemText(3, QCoreApplication.translate("page_moria", u"\u0391\u03a3 \u03ba\u03b1\u03b9 \u039f\u03a0/\u039f\u03bc.\u03a0 \u03bc\u03b5 \u03bc\u03ad\u03bb\u03b7>10", None))
        self.comboBox_3_4.setItemText(4, QCoreApplication.translate("page_moria", u"\u0391\u03bd\u03b1\u03b3\u03ba\u03b1\u03c3\u03c4\u03b9\u03ba\u03cc\u03c2 \u03a3\u03c5\u03bd\u03b5\u03c4\u03b1\u03b9\u03c1\u03b9\u03c3\u03bc\u03cc\u03c2", None))
        self.comboBox_3_4.setItemText(5, QCoreApplication.translate("page_moria", u"\u039a\u03b1\u03bd\u03ad\u03bd\u03b1 \u03b1\u03c0\u03cc \u03c4\u03b1 \u03c0\u03b1\u03c1\u03b1\u03c0\u03ac\u03bd\u03c9", None))

        self.comboBox_3_2.setItemText(0, QCoreApplication.translate("page_moria", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_3_2.setItemText(1, QCoreApplication.translate("page_moria", u"\u039d\u03ad\u03bf\u03c2 \u0391\u03b3\u03c1\u03cc\u03c4\u03b7\u03c2 2018 \u03ae 2021", None))
        self.comboBox_3_2.setItemText(2, QCoreApplication.translate("page_moria", u"\u0395\u03c0\u03b9\u03bb\u03b1\u03c7\u03cc\u03bd\u03c4\u03b1\u03c2 \u03c4\u03bf\u03c5 \u039c6.1", None))
        self.comboBox_3_2.setItemText(3, QCoreApplication.translate("page_moria", u"\u0395\u03bc\u03c0\u03b5\u03b9\u03c1\u03af\u03b1 >5 \u03b5\u03c4\u03ce\u03bd \u03ba\u03b1\u03b9 \u03ad\u03c9\u03c2 50 \u03b5\u03c4\u03ce\u03bd", None))
        self.comboBox_3_2.setItemText(4, QCoreApplication.translate("page_moria", u"\u039a\u03b1\u03bd\u03ad\u03bd\u03b1 \u03b1\u03c0\u03cc \u03c4\u03b1 \u03c0\u03b1\u03c1\u03b1\u03c0\u03ac\u03bd\u03c9", None))

        self.label_21.setText(QCoreApplication.translate("page_moria", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">\u03a0\u03c1\u03bf\u03cb\u03c0\u03bf\u03bb\u03bf\u03b3\u03b9\u03c3\u03bc\u03cc\u03c2 \u03ad\u03c1\u03b3\u03bf\u03c5</span></p></body></html>", None))
    # retranslateUi

