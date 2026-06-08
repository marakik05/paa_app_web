# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_page_mellontiki.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_page_mellontiki(object):
    def setupUi(self, page_mellontiki):
        if not page_mellontiki.objectName():
            page_mellontiki.setObjectName(u"page_mellontiki")
        page_mellontiki.resize(1566, 495)
        self.gridLayout = QGridLayout(page_mellontiki)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(page_mellontiki)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.addbtn_mel = QPushButton(page_mellontiki)
        self.addbtn_mel.setObjectName(u"addbtn_mel")
        self.addbtn_mel.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout.addWidget(self.addbtn_mel)

        self.copybtn = QPushButton(page_mellontiki)
        self.copybtn.setObjectName(u"copybtn")
        self.copybtn.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout.addWidget(self.copybtn)

        self.tableView = QTableView(page_mellontiki)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.label_2 = QLabel(page_mellontiki)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)


        self.retranslateUi(page_mellontiki)

        QMetaObject.connectSlotsByName(page_mellontiki)
    # setupUi

    def retranslateUi(self, page_mellontiki):
        page_mellontiki.setWindowTitle(QCoreApplication.translate("page_mellontiki", u"Form", None))
        self.label.setText(QCoreApplication.translate("page_mellontiki", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">\u03a4\u03a5\u03a0\u0399\u039a\u0397 \u0391\u03a0\u039f\u0394\u039f\u03a3\u0397 \u039c\u0395\u039b\u039b\u039f\u039d\u03a4\u0399\u039a\u0397\u03a3 \u039a\u0391\u03a4\u0391\u03a3\u03a4\u0391\u03a3\u0397\u03a3</span></p></body></html>", None))
        self.addbtn_mel.setText(QCoreApplication.translate("page_mellontiki", u"\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7", None))
        self.copybtn.setText(QCoreApplication.translate("page_mellontiki", u"\u0391\u03bd\u03c4\u03b9\u03b3\u03c1\u03b1\u03c6\u03ae \u0391\u03c1\u03c7\u03b9\u03ba\u03ae\u03c2", None))
        self.label_2.setText(QCoreApplication.translate("page_mellontiki", u"<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">\u03a3\u03b7\u03bc\u03b5\u03af\u03c9\u03c3\u03b7</span><span style=\" font-style:italic;\"> : \u039c\u03b5 \u03c4\u03bf \u03ba\u03bf\u03c5\u03bc\u03c0\u03af \u0391\u03bd\u03c4\u03b9\u03b3\u03c1\u03b1\u03c6\u03ae \u0391\u03c1\u03c7\u03b9\u03ba\u03ae\u03c2 \u03bc\u03c0\u03bf\u03c1\u03b5\u03af\u03c4\u03b5 \u03bd\u03b1 \u03c6\u03ad\u03c1\u03b5\u03c4\u03b5 \u03cc\u03bb\u03b5\u03c2 \u03c4\u03b9\u03c2 \u03b5\u03b3\u03b3\u03c1\u03b1\u03c6\u03ad\u03c2 \u03c4\u03bf\u03c5 \u03c0\u03af\u03bd\u03b1\u03ba\u03b1 \u03c4\u03b7\u03c2 \u0391\u03c1\u03c7\u03b9\u03ba\u03ae\u03c2 \u03a4\u0391 \u03c3\u03c4\u03bf\u03bd \u03c0\u03af\u03bd\u03b1\u03ba\u03b1 \u03c4\u03b7\u03c2 \u039c\u03b5\u03bb\u03bb\u03bf\u03bd\u03c4\u03b9\u03ba\u03ae\u03c2 \u03a4\u0391. \u039f\u03c0\u03bf\u03b9\u03b1\u03b4\u03ae\u03c0\u03bf\u03c4\u03b5 \u03bc\u03b5\u03c4\u03b1\u03b2\u03bf\u03bb\u03ae \u03c0\u03bf\u03c5 \u03b1\u03c6\u03bf\u03c1\u03ac \u03c4\u03b7\u03bd \u03b1\u03bb\u03bb\u03b1\u03b3"
                        "\u03ae \u03bd\u03b5\u03b1\u03c1\u03ce\u03bd \u03b4\u03ad\u03bd\u03b4\u03c1\u03c9\u03bd/\u03b1\u03bc\u03c0\u03b5\u03bb\u03ce\u03bd\u03c9\u03bd \u03c3\u03b5 \u03b5\u03bd\u03ae\u03bb\u03b9\u03ba\u03b1 \u03b8\u03b1 \u03c0\u03c1\u03ad\u03c0\u03b5\u03b9 \u03bd\u03b1 \u03c4\u03b7\u03bd \u03c0\u03c1\u03b1\u03b3\u03bc\u03b1\u03c4\u03bf\u03c0\u03bf\u03b9\u03ae\u03c3\u03b5\u03c4\u03b5 \u03c7\u03b5\u03b9\u03c1\u03bf\u03ba\u03af\u03bd\u03b7\u03c4\u03b1.</span></p></body></html>", None))
    # retranslateUi

