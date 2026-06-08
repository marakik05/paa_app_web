# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_page_1.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_page_1(object):
    def setupUi(self, page_1):
        if not page_1.objectName():
            page_1.setObjectName(u"page_1")
        page_1.resize(1009, 680)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(page_1.sizePolicy().hasHeightForWidth())
        page_1.setSizePolicy(sizePolicy)
        page_1.setMinimumSize(QSize(781, 483))
        page_1.setMaximumSize(QSize(1009, 680))
        self.verticalLayout = QVBoxLayout(page_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.scrollArea = QScrollArea(page_1)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMinimumSize(QSize(0, 200))
        self.scrollArea.setMaximumSize(QSize(16777215, 662))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1064, 639))
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy2)
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox_5 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox_5.sizePolicy().hasHeightForWidth())
        self.comboBox_5.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox_5, 5, 1, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_5 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_5, 5, 2, 1, 1)

        self.lineEdit_4 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy4.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_4, 4, 2, 1, 1)

        self.comboBox_7 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.setObjectName(u"comboBox_7")
        sizePolicy3.setHeightForWidth(self.comboBox_7.sizePolicy().hasHeightForWidth())
        self.comboBox_7.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox_7, 8, 1, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy4.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit, 1, 2, 1, 1)

        self.comboBox = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy3.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox, 7, 1, 1, 1)

        self.comboBox_3 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        sizePolicy3.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox_3, 3, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy4.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_3, 3, 2, 1, 1)

        self.lineEdit_11 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        sizePolicy3.setHeightForWidth(self.lineEdit_11.sizePolicy().hasHeightForWidth())
        self.lineEdit_11.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.lineEdit_11, 8, 2, 1, 1)

        self.lineEdit_6 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        sizePolicy3.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.lineEdit_6, 6, 2, 1, 1)

        self.lineEdit_12 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        sizePolicy3.setHeightForWidth(self.lineEdit_12.sizePolicy().hasHeightForWidth())
        self.lineEdit_12.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.lineEdit_12, 9, 2, 1, 1)

        self.lineEdit_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy4.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.lineEdit_2, 2, 2, 1, 1)

        self.comboBox_2 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy3.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox_2, 2, 1, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_9 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        sizePolicy3.setHeightForWidth(self.lineEdit_9.sizePolicy().hasHeightForWidth())
        self.lineEdit_9.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.lineEdit_9, 1, 1, 1, 1)

        self.lineEdit_7 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy5)

        self.gridLayout.addWidget(self.lineEdit_7, 10, 1, 1, 1)

        self.comboBox_6 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        sizePolicy3.setHeightForWidth(self.comboBox_6.sizePolicy().hasHeightForWidth())
        self.comboBox_6.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox_6, 6, 1, 1, 1)

        self.lineEdit_8 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        sizePolicy5.setHeightForWidth(self.lineEdit_8.sizePolicy().hasHeightForWidth())
        self.lineEdit_8.setSizePolicy(sizePolicy5)

        self.gridLayout.addWidget(self.lineEdit_8, 10, 2, 1, 1)

        self.comboBox_8 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.setObjectName(u"comboBox_8")
        sizePolicy3.setHeightForWidth(self.comboBox_8.sizePolicy().hasHeightForWidth())
        self.comboBox_8.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox_8, 9, 1, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.lineEdit_10 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        sizePolicy3.setHeightForWidth(self.lineEdit_10.sizePolicy().hasHeightForWidth())
        self.lineEdit_10.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.lineEdit_10, 7, 2, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 10, 0, 1, 1)

        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 9, 0, 1, 1)

        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 8, 0, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.comboBox_4 = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        sizePolicy3.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox_4, 4, 1, 1, 1)

        self.lineEdit_13 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        sizePolicy3.setHeightForWidth(self.lineEdit_13.sizePolicy().hasHeightForWidth())
        self.lineEdit_13.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.lineEdit_13, 11, 2, 1, 1)

        self.label_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 11, 0, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(page_1)

        QMetaObject.connectSlotsByName(page_1)
    # setupUi

    def retranslateUi(self, page_1):
        page_1.setWindowTitle(QCoreApplication.translate("page_1", u"Form", None))
        self.comboBox_5.setItemText(0, QCoreApplication.translate("page_1", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_5.setItemText(1, QCoreApplication.translate("page_1", u"\u039d\u03b1\u03b9", None))
        self.comboBox_5.setItemText(2, QCoreApplication.translate("page_1", u"\u038c\u03c7\u03b9", None))

        self.label_7.setText(QCoreApplication.translate("page_1", u"6.  \u0394\u03b5\u03bd \u03b5\u03af\u03bd\u03b1\u03b9 \u03ac\u03bc\u03b5\u03c3\u03b1 \u03c3\u03c5\u03bd\u03c4\u03b1\u03be\u03b9\u03bf\u03b4\u03bf\u03c4\u03bf\u03cd\u03bc\u03b5\u03bd\u03bf\u03c2 \u03b1\u03c0\u03cc \u03bf\u03c0\u03bf\u03b9\u03bf\u03b4\u03ae\u03c0\u03bf\u03c4\u03b5 \u03c4\u03b1\u03bc\u03b5\u03af\u03bf \u03c4\u03bf\u03c5 \u03b5\u03c3\u03c9\u03c4\u03b5\u03c1\u03b9\u03ba\u03bf\u03cd \u03ae \u03b5\u03be\u03c9\u03c4\u03b5\u03c1\u03b9\u03ba\u03bf\u03cd, \u03b5\u03be\u03b1\u03b9\u03c1\u03bf\u03c5\u03bc\u03ad\u03bd\u03c9\u03bd \u03c4\u03c9\u03bd \u03c0\u03b5\u03c1\u03b9\u03c0\u03c4\u03ce\u03c3\u03b5\u03c9\u03bd \u03c3\u03c5\u03bd\u03c4\u03b1\u03be\u03b9\u03bf\u03b4\u03cc\u03c4\u03b7\u03c3\u03b7\u03c2 \u03bb\u03cc\u03b3\u03c9 \u03b1\u03bd\u03b1\u03c0\u03b7\u03c1\u03af\u03b1\u03c2 \u03c4\u03bf\u03c5 \u03ac\u03c1\u03b8\u03c1\u03bf\u03c5 37 \u03c4\u03bf\u03c5 \u039d. 3996/2011\n"
" \u03ba\u03b1\u03b9 \u03c4\u03bf\u03c5 \u03ac\u03c1\u03b8\u03c1\u03bf\u03c5 5, \u03c0\u03b1\u03c1. \u03b3, \u03c4\u03bf\u03c5 \u039d"
                        ".1287/1982", None))
        self.label_6.setText(QCoreApplication.translate("page_1", u"5. \u0395\u03af\u03bd\u03b1\u03b9 \u03b1\u03c3\u03c6\u03b1\u03bb\u03b9\u03c3\u03c4\u03b9\u03ba\u03ac \u03ba\u03b1\u03b9 \u03c6\u03bf\u03c1\u03bf\u03bb\u03bf\u03b3\u03b9\u03ba\u03ac \u03b5\u03bd\u03ae\u03bc\u03b5\u03c1\u03bf\u03c2;", None))
        self.label_2.setText(QCoreApplication.translate("page_1", u"1. \u03a3\u03c5\u03bc\u03c0\u03bb\u03b7\u03c1\u03ce\u03c3\u03c4\u03b5 \u03c4\u03b7\u03bd \u03b7\u03bb\u03b9\u03ba\u03af\u03b1 \u03c4\u03bf\u03c5 \u03c5\u03c0\u03bf\u03c8\u03b7\u03c6\u03af\u03bf\u03c5. \u039f \u03c5\u03c0\u03bf\u03c8\u03ae\u03c6\u03b9\u03bf\u03c2 \u03c0\u03c1\u03ad\u03c0\u03b5\u03b9 \u03bd\u03b1 \u03ad\u03c7\u03b5\u03b9 \u03b5\u03bd\u03b7\u03bb\u03b9\u03ba\u03b9\u03c9\u03b8\u03b5\u03af \u03ba\u03b1\u03b9 \u03bd\u03b1 \u03bc\u03b7\u03bd \u03ad\u03c7\u03b5\u03b9 \u03c5\u03c0\u03b5\u03c1\u03b2\u03b5\u03af \u03c4\u03bf 63\u03bf \u03ad\u03c4\u03bf\u03c2 \u03c4\u03b7\u03c2 \u03b7\u03bb\u03b9\u03ba\u03af\u03b1\u03c2 \u03ba\u03b1\u03c4\u03ac \u03c4\u03b7\u03bd \u03c5\u03c0\u03bf\u03b2\u03bf\u03bb\u03ae \u03c4\u03b7\u03c2 \u03b1\u03af\u03c4\u03b7\u03c3\u03b7\u03c2 \u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7\u03c2.", None))
        self.comboBox_7.setItemText(0, QCoreApplication.translate("page_1", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_7.setItemText(1, QCoreApplication.translate("page_1", u"\u039d\u03b1\u03b9", None))
        self.comboBox_7.setItemText(2, QCoreApplication.translate("page_1", u"\u038c\u03c7\u03b9", None))

        self.label_3.setText(QCoreApplication.translate("page_1", u"2. \u0395\u03af\u03bd\u03b1\u03b9 \u03b5\u03c0\u03b1\u03b3\u03b3\u03b5\u03bb\u03bc\u03b1\u03c4\u03af\u03b1\u03c2 \u03b1\u03b3\u03c1\u03cc\u03c4\u03b7\u03c2 \u03ae \u039d\u03ad\u03bf\u03c2 \u0391\u03b3\u03c1\u03cc\u03c4\u03b7\u03c2 \u03c4\u03b7\u03c2 \u03a0\u03b1\u03c1\u03ad\u03bc\u03b2\u03b1\u03c3\u03b7\u03c2  \u03a03-75.1 ;", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("page_1", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("page_1", u"\u039d\u03b1\u03b9", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("page_1", u"\u038c\u03c7\u03b9", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("page_1", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("page_1", u"\u039d\u03b1\u03b9", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("page_1", u"\u038c\u03c7\u03b9", None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("page_1", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("page_1", u"\u039d\u03b1\u03b9", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("page_1", u"\u038c\u03c7\u03b9", None))

        self.label.setText(QCoreApplication.translate("page_1", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">\u039a\u03a1\u0399\u03a4\u0397\u03a1\u0399\u0391 \u0395\u03a0\u0399\u039b\u0395\u039e\u0399\u039c\u039f\u03a4\u0397\u03a4\u0391\u03a3 \u03a5\u03a0\u039f\u03a8\u0397\u03a6\u0399\u039f\u03a5</span></p></body></html>", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("page_1", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("page_1", u"\u039d\u03b1\u03b9", None))
        self.comboBox_6.setItemText(2, QCoreApplication.translate("page_1", u"\u038c\u03c7\u03b9", None))

        self.comboBox_8.setItemText(0, QCoreApplication.translate("page_1", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_8.setItemText(1, QCoreApplication.translate("page_1", u"\u039d\u03b1\u03b9", None))
        self.comboBox_8.setItemText(2, QCoreApplication.translate("page_1", u"\u038c\u03c7\u03b9", None))

        self.label_9.setText(QCoreApplication.translate("page_1", u"7. \u039f \u03c5\u03c0\u03bf\u03c8\u03ae\u03c6\u03b9\u03bf\u03c2 \u03c3\u03c4\u03bf \u03c0\u03bb\u03b1\u03af\u03c3\u03b9\u03bf \u03c4\u03b7\u03c2 534/13.3.2023 \u03a0\u03c1\u03cc\u03c3\u03ba\u03bb\u03b7\u03c3\u03b7\u03c2 (\u0394\u03c1\u03ac\u03c3\u03b7 4.1.5) \u03bf\u03c1\u03b9\u03c3\u03c4\u03b9\u03ba\u03bf\u03c0\u03bf\u03af\u03b7\u03c3\u03b5 \u03c3\u03c4\u03bf \u03a0\u03a3\u039a\u0395 \u03c4\u03bf\u03c5\u03bb\u03ac\u03c7\u03b9\u03c3\u03c4\u03bf\u03bd \u03ad\u03bd\u03b1 \u03b1\u03af\u03c4\u03b7\u03bc\u03b1 \u03c0\u03c1\u03bf\u03ba\u03b1\u03c4\u03b1\u03b2\u03bf\u03bb\u03ae\u03c2 \u03ae \u03c0\u03bb\u03b7\u03c1\u03c9\u03bc\u03ae\u03c2 \u03b1\u03c0\u03cc \u03c4\u03bf \u03bf\u03c0\u03bf\u03af\u03bf \u03c0\u03c1\u03bf\u03ad\u03ba\u03c5\u03c8\u03b5 \u03ba\u03b1\u03c4\u03b1\u03b2\u03bf\u03bb\u03ae \n"
"\u03bf\u03b9\u03ba\u03bf\u03bd\u03bf\u03bc\u03b9\u03ba\u03ae\u03c2 \u03b5\u03bd\u03af\u03c3\u03c7\u03c5\u03c3\u03b7\u03c2;", None))
        self.label_5.setText(QCoreApplication.translate("page_1", u"4. \u0388\u03c7\u03b5\u03b9 \u03c5\u03c0\u03bf\u03b2\u03ac\u03bb\u03b5\u03b9 \u03c0\u03b1\u03c1\u03b1\u03b4\u03b5\u03ba\u03c4\u03ae \u0395\u0391\u0395 \u03b3\u03b9\u03b1 \u03c4\u03bf \u03ad\u03c4\u03bf\u03c2 2025;", None))
        self.label_8.setText(QCoreApplication.translate("page_1", u"10.  \u0397 \u03b3\u03b5\u03c9\u03c1\u03b3\u03b9\u03ba\u03ae \u03b5\u03ba\u03bc\u03b5\u03c4\u03ac\u03bb\u03bb\u03b5\u03c5\u03c3\u03b7 \u03c0\u03c1\u03ad\u03c0\u03b5\u03b9 \u03bd\u03b1 \u03ad\u03c7\u03b5\u03b9 \u03b5\u03bb\u03ac\u03c7\u03b9\u03c3\u03c4\u03bf \u03bc\u03ad\u03b3\u03b5\u03b8\u03bf\u03c2 \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03b9\u03ba\u03ae\u03c2 \u03b4\u03c5\u03bd\u03b1\u03bc\u03b9\u03ba\u03cc\u03c4\u03b7\u03c4\u03b1\u03c2 (\u03b5\u03ba\u03c6\u03c1\u03b1\u03c3\u03bc\u03ad\u03bd\u03b7 \u03c9\u03c2 \u03c4\u03c5\u03c0\u03b9\u03ba\u03ae \u03b1\u03c0\u03cc\u03b4\u03bf\u03c3\u03b7) \u03c3\u03cd\u03bc\u03c6\u03c9\u03bd\u03b1 \u03bc\u03b5 \u03c4\u03b7\u03bd \u0395\u03bd\u03b9\u03b1\u03af\u03b1 \u0394\u03ae\u03bb\u03c9\u03c3\u03b7 \u0395\u03ba\u03bc\u03b5\u03c4\u03ac\u03bb\u03bb\u03b5\u03c5\u03c3\u03b7\u03c2 \u03c4\u03bf\u03c5 \u03ad\u03c4\u03bf\u03c5\u03c2 2025\n"
" \u03c4\u03b1 12.000 \u20ac, \u03b5\u03c6\u03cc\u03c3\u03bf\u03bd \u03b1\u03c5\u03c4\u03ae \u03b2\u03c1\u03af\u03c3\u03ba\u03b5\u03c4\u03b1"
                        "\u03b9 \u03c3\u03c4\u03b7\u03bd \u03b7\u03c0\u03b5\u03b9\u03c1\u03c9\u03c4\u03b9\u03ba\u03ae \u03c7\u03ce\u03c1\u03b1, \u03c4\u03b7\u03bd \u039a\u03c1\u03ae\u03c4\u03b7 \u03ae \u03c4\u03b7\u03bd \u0395\u03cd\u03b2\u03bf\u03b9\u03b1 \u03ae \u03c4\u03b1 8.000 \u20ac \u03b5\u03c6\u03cc\u03c3\u03bf\u03bd \u03b1\u03c5\u03c4\u03ae \u03b2\u03c1\u03af\u03c3\u03ba\u03b5\u03c4\u03b1\u03b9 \u03c3\u03b5 \u03ba\u03ac\u03c0\u03bf\u03b9\u03bf \u03b1\u03c0\u03cc \u03c4\u03b1 \u03bd\u03b7\u03c3\u03b9\u03ac \u03c4\u03b7\u03c2 \u03a7\u03ce\u03c1\u03b1\u03c2 \u03c0\u03bb\u03b7\u03bd \u039a\u03c1\u03ae\u03c4\u03b7\u03c2 \u03ba\u03b1\u03b9 \u0395\u03cd\u03b2\u03bf\u03b9\u03b1\u03c2.", None))
        self.label_11.setText(QCoreApplication.translate("page_1", u"9. \u039f \u03c5\u03c0\u03bf\u03c8\u03ae\u03c6\u03b9\u03bf\u03c2 \u03b5\u03b3\u03ba\u03c1\u03af\u03b8\u03b7\u03ba\u03b5 \u03c3\u03c4\u03b9\u03c2 \u0394\u03c1\u03ac\u03c3\u03b5\u03b9\u03c2 4.1.1, 4.1.2 \u03ba\u03b1\u03b9 4.1.3 \u03c4\u03c9\u03bd \u03c5\u03c0\u2019 \u03b1\u03c1\u03b9\u03b8. 13849/14.12.2017 \u03ba\u03b1\u03b9 1710/7.5.2021 \u03a0\u03c1\u03bf\u03c3\u03ba\u03bb\u03ae\u03c3\u03b5\u03c9\u03bd \u03ba\u03b1\u03b9 \u03b4\u03b5\u03bd \u03ad\u03c7\u03b5\u03b9 \u03bf\u03bb\u03bf\u03ba\u03bb\u03b7\u03c1\u03ce\u03c3\u03b5\u03b9 \u03c4\u03bf \u03b5\u03c0\u03b5\u03bd\u03b4\u03c5\u03c4\u03b9\u03ba\u03cc \u03c4\u03bf\u03c5 \u03c3\u03c7\u03ad\u03b4\u03b9\u03bf;", None))
        self.label_10.setText(QCoreApplication.translate("page_1", u"8.  \u039f \u03c5\u03c0\u03bf\u03c8\u03ae\u03c6\u03b9\u03bf\u03c2 \u03ad\u03c7\u03b5\u03b9 \u03c5\u03c0\u03bf\u03b2\u03ac\u03bb\u03b5\u03b9 \u03b1\u03af\u03c4\u03b7\u03c3\u03b7 \u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7\u03c2 \u03c3\u03c4\u03b7\u03bd \u03a0\u03b1\u03c1\u03ad\u03bc\u03b2\u03b1\u03c3\u03b7 \u03a03-73-2.9 (\u0398\u03b5\u03c1\u03bc\u03bf\u03ba\u03ae\u03c0\u03b9\u03b1) \u03ba\u03b1\u03b9 \u03b1\u03c5\u03c4\u03ae \u03b5\u03b3\u03ba\u03c1\u03b9\u03b8\u03b5\u03af;", None))
        self.label_4.setText(QCoreApplication.translate("page_1", u"3.  \u0397 \u03b5\u03c0\u03ad\u03bd\u03b4\u03c5\u03c3\u03b7 \u03c4\u03bf\u03c5 \u03b8\u03b1 \u03c5\u03bb\u03bf\u03c0\u03bf\u03b9\u03b7\u03b8\u03b5\u03af \u03b5\u03bd\u03c4\u03cc\u03c2 \u03c4\u03b7\u03c2 \u03a0\u03b5\u03c1\u03b9\u03c6\u03ad\u03c1\u03b5\u03b9\u03b1\u03c2 \u03c0\u03bf\u03c5 \u03b2\u03c1\u03af\u03c3\u03ba\u03b5\u03c4\u03b1\u03b9 \u03b7 \u03ad\u03b4\u03c1\u03b1 \u03c4\u03b7\u03c2 \u03b5\u03ba\u03bc\u03b5\u03c4\u03ac\u03bb\u03bb\u03b5\u03c5\u03c3\u03ae\u03c2 \u03c4\u03bf\u03c5;", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("page_1", u"--\u0395\u03c0\u03b9\u03bb\u03ad\u03be\u03c4\u03b5", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("page_1", u"\u039d\u03b1\u03b9", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("page_1", u"\u038c\u03c7\u03b9", None))

        self.label_12.setText(QCoreApplication.translate("page_1", u"<html><head/><body><p><span style=\" font-weight:600;\">\u0391\u03c0\u03bf\u03c4\u03ad\u03bb\u03b5\u03c3\u03bc\u03b1 \u03b5\u03c0\u03b9\u03bb\u03b5\u03be\u03b9\u03bc\u03cc\u03c4\u03b7\u03c4\u03b1\u03c2 \u03c5\u03c0\u03bf\u03c8\u03b7\u03c6\u03af\u03bf\u03c5 \u03ba\u03b1\u03c4\u03cc\u03c0\u03b9\u03bd \u03c3\u03c5\u03bc\u03c0\u03bb\u03ae\u03c1\u03c9\u03c3\u03b7\u03c2 \u03c4\u03c9\u03bd \u03ba\u03c1\u03b9\u03c4\u03b7\u03c1\u03af\u03c9\u03bd \u03b5\u03c0\u03b9\u03bb\u03b5\u03be\u03b9\u03bc\u03cc\u03c4\u03b7\u03c4\u03b1\u03c2</span></p></body></html>", None))
    # retranslateUi

