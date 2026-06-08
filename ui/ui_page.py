# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_page.ui'
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
        page.resize(1566, 497)
        self.gridLayout = QGridLayout(page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(page)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.addbtn = QPushButton(page)
        self.addbtn.setObjectName(u"addbtn")
        self.addbtn.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout.addWidget(self.addbtn)

        self.tableView = QTableView(page)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.label_2 = QLabel(page)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)


        self.retranslateUi(page)

        QMetaObject.connectSlotsByName(page)
    # setupUi

    def retranslateUi(self, page):
        page.setWindowTitle(QCoreApplication.translate("page", u"Form", None))
        self.label.setText(QCoreApplication.translate("page", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">\u03a4\u03a5\u03a0\u0399\u039a\u0397 \u0391\u03a0\u039f\u0394\u039f\u03a3\u0397 \u0391\u03a1\u03a7\u0399\u039a\u0397\u03a3 \u039a\u0391\u03a4\u0391\u03a3\u03a4\u0391\u03a3\u0397\u03a3</span></p></body></html>", None))
        self.addbtn.setText(QCoreApplication.translate("page", u"\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7", None))
        self.label_2.setText(QCoreApplication.translate("page", u"<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">\u03a3\u03b7\u03bc\u03b5\u03af\u03c9\u03c3\u03b7</span><span style=\" font-style:italic;\">: \u039f\u03b9 \u03c4\u03b9\u03bc\u03ad\u03c2 \u03a4\u03c5\u03c0\u03b9\u03ba\u03ae\u03c2 \u0391\u03c0\u03cc\u03b4\u03bf\u03c3\u03b7\u03c2 \u03c0\u03bf\u03c5 \u03ad\u03c1\u03c7\u03bf\u03bd\u03c4\u03b1\u03b9 \u03c0\u03c1\u03bf\u03c3\u03c5\u03bc\u03c0\u03bb\u03b7\u03c1\u03c9\u03bc\u03ad\u03bd\u03b5\u03c2 \u03b1\u03c6\u03bf\u03c1\u03bf\u03cd\u03bd \u03b4\u03b7\u03bb\u03c9\u03b8\u03ad\u03bd\u03c4\u03b1 \u03c3\u03c4\u03bf\u03b9\u03c7\u03b5\u03af\u03b1. \u0395\u03bd\u03b4\u03ad\u03c7\u03b5\u03c4\u03b1\u03b9 \u03bd\u03b1 \u03c5\u03c0\u03ac\u03c1\u03be\u03bf\u03c5\u03bd \u03b1\u03c0\u03bf\u03ba\u03bb\u03af\u03c3\u03b5\u03b9\u03c2 \u03ae \u03bc\u03b5\u03b9\u03c9\u03bc\u03ad\u03bd\u03b5\u03c2 \u03c4\u03b9\u03bc\u03ad\u03c2 \u03ba\u03b1\u03c4\u03ac \u03c4\u03b7\u03bd \u03b5\u03be\u03b1\u03c4\u03bf\u03bc\u03af\u03ba\u03b5\u03c5\u03c3\u03b7.</span></p></body></"
                        "html>", None))
    # retranslateUi

