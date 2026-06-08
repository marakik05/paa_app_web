# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from delegates.delegates_dlt import NoWheelComboBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1046, 802)
        MainWindow.setStyleSheet(u"*{\n"
"font-size:9pt;\n"
"font-family:\"Verdana\",\"Arial\", \"Helvetica\",  sans-serif;\n"
"}\n"
"QMainWindow {\n"
"    background-color: #F2F7FA;\n"
"}\n"
"QScrollArea{\n"
"background-color: #F2F7FA;\n"
"border:none\n"
"}\n"
"\n"
"QScrollArea QWidget#scrollAreaWidgetContents {\n"
"    background-color: #F2F7FA;\n"
"}\n"
"\n"
"QToolBar{\n"
"background-color:#2E91DB;\n"
"}\n"
"QToolBar QToolButton {\n"
"font-weight:bold;\n"
"\n"
"color:white;\n"
"}\n"
"\n"
"\n"
"QToolBar :hover {\n"
"background-color:#0D80D6\n"
"}\n"
"\n"
"QToolBar QToolButton:disabled {\n"
"    color: #A0C8E8;      \n"
"    font-weight: normal;  \n"
"    background-color: transparent;\n"
"}\n"
"QPushButton{\n"
"font-weight:bold;\n"
"background-color:#2E91DB;\n"
"color:white;\n"
"border:1px solid #BBDEFB;\n"
"border-radius:3px;\n"
"padding: 6px 0px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #0D80D6;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #0A77C9;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-col"
                        "or: #E3F2FD;\n"
"    color: #9E9E9E;\n"
"    border: 1px solid #BBDEFB;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: white;\n"
"    border:1px solid #BBDEFB;\n"
"    border-radius: 3px;\n"
"    padding: 3px 8px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid #2E91DB;\n"
"}\n"
"\n"
"QLineEdit:read-only {\n"
"    background-color: #E3F2FD;\n"
"    color: #9E9E9E;\n"
"	border: 1px solid #BBDEFB;\n"
" 	font-weight:bold;\n"
"}\n"
"\n"
"QComboBox {\n"
"    background-color: white;\n"
"    border:1px solid #BBDEFB;\n"
"    border-radius: 3px;\n"
"    padding: 4px 8px;\n"
"}\n"
"QComboBox:focus {\n"
"    border: 2px solid #2E91DB;\n"
"}\n"
"\n"
"QTableView {\n"
"    background-color: white;           \n"
"    selection-background-color: #2E91DB;      \n"
"    selection-color: white;                  \n"
"    gridline-color: #BBDEFB; \n"
"	               \n"
"    border: 1px solid #BBDEFB;                \n"
"}\n"
"\n"
"QTableView::viewport {\n"
"    background-color: white;\n"
"}\n"
"\n"
"\n"
"QHea"
                        "derView::section {\n"
"    background-color: #E3F2FD;              \n"
"    color: #1976D2;                           \n"
"    padding: 4px 3px;\n"
"    border: 1px solid #BBDEFB;  \n"
"    font-weight: bold;\n"
"   \n"
"}\n"
"\n"
"\n"
"\n"
"QHeaderView::section:hover {\n"
"    background-color: #BBDEFB;\n"
"}\n"
"\n"
"QHeaderView::section:disabled {\n"
"    background-color: #E3F2FD;\n"
"    color: #A0A0A0;\n"
" \n"
"}\n"
"\n"
"\n"
"\n"
"QStackedWidget > QWidget {\n"
"    background-color: white;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background-color: #F5F5F5;\n"
"    width: 12px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background-color: #BBDEFB;\n"
"    border-radius: 6px;\n"
"    min-height: 30px;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background-color: #90CAF9;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:pressed {\n"
"    background-color: #2E91DB;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    background-color: #F5F5F5;\n"
" "
                        "   height: 12px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background-color: #BBDEFB;\n"
"    border-radius: 6px;\n"
"    min-width: 30px;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal:hover {\n"
"    background-color: #90CAF9;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal:pressed {\n"
"    background-color: #2E91DB;\n"
"}\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-line:horizontal,\n"
"QScrollBar::sub-line:horizontal {\n"
"    height: 0px;\n"
"    width: 0px;\n"
"}\n"
"\n"
"QScrollBar::corner {\n"
"    background-color: #F5F5F5;\n"
"}\n"
"\n"
"QMessageBox {\n"
"    background-color:  #F2F7FA;\n"
"    color: #333333;\n"
"}\n"
"\n"
"\n"
"\n"
"QMessageBox QPushButton {\n"
"    background-color: #2E91DB;\n"
"    color: white;\n"
"    border:1px solid #BBDEFB;\n"
"    border-radius: 3px;\n"
"    padding: 6px 10px;\n"
"    font-weight: bold;\n"
"   min-width:60px;\n"
"   \n"
"}\n"
"\n"
"QMessageBox QPushButton:hover {"
                        "\n"
"    background-color: #2579B8;  \n"
"}\n"
"\n"
"QMessageBox QPushButton:pressed {\n"
"    background-color: #1F6594;\n"
"}")
        self.ta = QAction(MainWindow)
        self.ta.setObjectName(u"ta")
        self.epileximotita = QAction(MainWindow)
        self.epileximotita.setObjectName(u"epileximotita")
        self.mellontiki = QAction(MainWindow)
        self.mellontiki.setObjectName(u"mellontiki")
        self.arxiki = QAction(MainWindow)
        self.arxiki.setObjectName(u"arxiki")
        self.moria = QAction(MainWindow)
        self.moria.setObjectName(u"moria")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_4.sizePolicy().hasHeightForWidth())
        self.page_4.setSizePolicy(sizePolicy)
        self.stackedWidget.addWidget(self.page_4)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.page)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        sizePolicy1.setHeightForWidth(self.page_2.sizePolicy().hasHeightForWidth())
        self.page_2.setSizePolicy(sizePolicy1)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        sizePolicy1.setHeightForWidth(self.page_3.sizePolicy().hasHeightForWidth())
        self.page_3.setSizePolicy(sizePolicy1)
        self.stackedWidget.addWidget(self.page_3)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        sizePolicy.setHeightForWidth(self.page_5.sizePolicy().hasHeightForWidth())
        self.page_5.setSizePolicy(sizePolicy)
        self.stackedWidget.addWidget(self.page_5)

        self.gridLayout.addWidget(self.stackedWidget, 10, 0, 1, 5)

        self.lineEdit_afm = QLineEdit(self.centralwidget)
        self.lineEdit_afm.setObjectName(u"lineEdit_afm")
        self.lineEdit_afm.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_afm, 0, 1, 1, 1)

        self.combo_periferia = NoWheelComboBox(self.centralwidget)
        self.combo_periferia.setObjectName(u"combo_periferia")
        self.combo_periferia.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.combo_periferia, 9, 1, 1, 1)

        self.label_surname = QLabel(self.centralwidget)
        self.label_surname.setObjectName(u"label_surname")
        self.label_surname.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.label_surname, 7, 0, 1, 1)

        self.label_name = QLabel(self.centralwidget)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.label_name, 5, 0, 1, 1)

        self.lineEdit_surname = QLineEdit(self.centralwidget)
        self.lineEdit_surname.setObjectName(u"lineEdit_surname")
        self.lineEdit_surname.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_surname, 7, 1, 1, 1)

        self.importbtn = QPushButton(self.centralwidget)
        self.importbtn.setObjectName(u"importbtn")

        self.gridLayout.addWidget(self.importbtn, 0, 3, 1, 1)

        self.label_afm = QLabel(self.centralwidget)
        self.label_afm.setObjectName(u"label_afm")
        self.label_afm.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.label_afm, 0, 0, 1, 1)

        self.exportbtn = QPushButton(self.centralwidget)
        self.exportbtn.setObjectName(u"exportbtn")
        self.exportbtn.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.exportbtn, 9, 3, 1, 1)

        self.savebtn = QPushButton(self.centralwidget)
        self.savebtn.setObjectName(u"savebtn")
        self.savebtn.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.savebtn, 9, 2, 1, 1)

        self.label_periferia = QLabel(self.centralwidget)
        self.label_periferia.setObjectName(u"label_periferia")
        self.label_periferia.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.label_periferia, 9, 0, 1, 1)

        self.lineEdit_name = QLineEdit(self.centralwidget)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        self.lineEdit_name.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.lineEdit_name, 5, 1, 1, 1)

        self.searchbtn = QPushButton(self.centralwidget)
        self.searchbtn.setObjectName(u"searchbtn")
        self.searchbtn.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.searchbtn, 0, 2, 1, 1)

        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setMargin(0)

        self.gridLayout.addWidget(self.label_logo, 0, 4, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1046, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.arxiki)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.ta)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.mellontiki)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.epileximotita)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.moria)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ta.setText(QCoreApplication.translate("MainWindow", u"\u03a4\u0391 \u0391\u03c1\u03c7\u03b9\u03ba\u03ae\u03c2", None))
        self.epileximotita.setText(QCoreApplication.translate("MainWindow", u"\u0395\u03c0\u03b9\u03bb\u03b5\u03be\u03b9\u03bc\u03cc\u03c4\u03b7\u03c4\u03b1", None))
        self.mellontiki.setText(QCoreApplication.translate("MainWindow", u"\u03a4\u0391 \u039c\u03b5\u03bb\u03bb\u03bf\u03bd\u03c4\u03b9\u03ba\u03ae\u03c2", None))
        self.arxiki.setText(QCoreApplication.translate("MainWindow", u"\u0391\u03c1\u03c7\u03b9\u03ba\u03ae", None))
        self.moria.setText(QCoreApplication.translate("MainWindow", u"\u039c\u03bf\u03c1\u03b9\u03bf\u03b4\u03cc\u03c4\u03b7\u03c3\u03b7", None))
        self.label_surname.setText(QCoreApplication.translate("MainWindow", u"\u0395\u03a0\u03a9\u039d\u03a5\u039c\u039f", None))
        self.label_name.setText(QCoreApplication.translate("MainWindow", u"\u039f\u039d\u039f\u039c\u0391", None))
        self.importbtn.setText(QCoreApplication.translate("MainWindow", u"\u0395\u03b9\u03c3\u03b1\u03b3\u03c9\u03b3\u03ae", None))
        self.label_afm.setText(QCoreApplication.translate("MainWindow", u"\u0391\u03a6\u039c", None))
        self.exportbtn.setText(QCoreApplication.translate("MainWindow", u"\u0395\u03be\u03b1\u03b3\u03c9\u03b3\u03ae Excel", None))
        self.savebtn.setText(QCoreApplication.translate("MainWindow", u"\u0391\u03c0\u03bf\u03b8\u03ae\u03ba\u03b5\u03c5\u03c3\u03b7", None))
        self.label_periferia.setText(QCoreApplication.translate("MainWindow", u"\u03a0\u0395\u03a1\u0399\u03a6\u0395\u03a1\u0395\u0399\u0391", None))
        self.searchbtn.setText(QCoreApplication.translate("MainWindow", u"\u03a6\u03cc\u03c1\u03c4\u03c9\u03c3\u03b7", None))
        self.label_logo.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

