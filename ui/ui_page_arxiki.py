# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_page_arxiki.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_page(object):
    def setupUi(self, page):
        if not page.objectName():
            page.setObjectName(u"page")
        page.resize(1460, 1024)
        page.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableView = QTableView(page)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setMaximumSize(QSize(1500, 16777215))

        self.gridLayout.addWidget(self.tableView, 9, 0, 1, 6)

        self.label_2 = QLabel(page)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 3, 1, 1)

        self.label = QLabel(page)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(130, 16777215))

        self.gridLayout.addWidget(self.label, 8, 0, 1, 1)

        self.pushButton = QPushButton(page)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QSize(170, 16777215))

        self.gridLayout.addWidget(self.pushButton, 8, 2, 1, 1)

        self.lineEdit_search = QLineEdit(page)
        self.lineEdit_search.setObjectName(u"lineEdit_search")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_search.sizePolicy().hasHeightForWidth())
        self.lineEdit_search.setSizePolicy(sizePolicy1)
        self.lineEdit_search.setMaximumSize(QSize(120, 16777215))

        self.gridLayout.addWidget(self.lineEdit_search, 8, 1, 1, 1)


        self.retranslateUi(page)

        QMetaObject.connectSlotsByName(page)
    # setupUi

    def retranslateUi(self, page):
        page.setWindowTitle(QCoreApplication.translate("page", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("page", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">\u03a3\u03a5\u0393\u039a\u0395\u039d\u03a4\u03a1\u03a9\u03a4\u0399\u039a\u039f\u03a3 \u03a0\u0399\u039d\u0391\u039a\u0391\u03a3 \u0395\u0393\u0393\u03a1\u0391\u03a6\u03a9\u039d</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("page", u"<html><head/><body><p align=\"center\">\u0391\u03bd\u03b1\u03b6\u03ae\u03c4\u03b7\u03c3\u03b7 \u0391\u03a6\u039c</p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("page", u"\u0395\u03be\u03b1\u03b3\u03c9\u03b3\u03ae \u0395\u03b3\u03b3\u03c1\u03b1\u03c6\u03ce\u03bd", None))
    # retranslateUi

