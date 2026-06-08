from PySide2.QtWidgets import QWidget, QComboBox
from PySide2.QtCore import QEvent, Qt, QRegExp
from PySide2.QtGui import QRegExpValidator
from ui.ui_page_1 import Ui_page_1
from utils.excel_loader import ISLANDS


class epileximotitaPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_page_1()
        self.ui.setupUi(self)
        
        for combo in (
              self.ui.comboBox_2,
              self.ui.comboBox_3,
              self.ui.comboBox_4,
              self.ui.comboBox_5,
              self.ui.comboBox_6,
              self.ui.comboBox,
              self.ui.comboBox_7,
              self.ui.comboBox_8):
            combo.installEventFilter(self)
        
        #align lineEdit_9
        self.ui.lineEdit_9.setAlignment(Qt.AlignCenter)

        #περιορισμός έως 9 ψηφίων στο lineEdit του ΑΦΜ
        
        regex = QRegExp(r"^(?:0|[1-9]\d{0,2})$") # έως 3 ακεραια ψηφία 
        validator = QRegExpValidator(regex)
        self.ui.lineEdit_9.setValidator(validator)
        #βάζουμε read only τα lineEdit
        self.ui.lineEdit.setReadOnly(True)
        self.ui.lineEdit_2.setReadOnly(True)
        self.ui.lineEdit_3.setReadOnly(True)
        self.ui.lineEdit_4.setReadOnly(True)
        self.ui.lineEdit_5.setReadOnly(True)
        self.ui.lineEdit_6.setReadOnly(True)
        self.ui.lineEdit_7.setReadOnly(True)
        self.ui.lineEdit_8.setReadOnly(True)
        self.ui.lineEdit_10.setReadOnly(True)
        self.ui.lineEdit_11.setReadOnly(True)
        self.ui.lineEdit_12.setReadOnly(True)
        self.ui.lineEdit_13.setReadOnly(True)

        #συνδέουμε τα combobox με τη def positive
        
        self.ui.comboBox_2.currentTextChanged.connect(lambda: self.positive(self.ui.comboBox_2, self.ui.lineEdit_2))
        self.ui.comboBox_3.currentTextChanged.connect(lambda: self.positive(self.ui.comboBox_3, self.ui.lineEdit_3))
        self.ui.comboBox_4.currentTextChanged.connect(lambda: self.positive(self.ui.comboBox_4, self.ui.lineEdit_4))
        self.ui.comboBox_5.currentTextChanged.connect(lambda: self.positive(self.ui.comboBox_5, self.ui.lineEdit_5))
        self.ui.comboBox_6.currentTextChanged.connect(lambda: self.positive(self.ui.comboBox_6, self.ui.lineEdit_6))
        self.ui.comboBox.currentTextChanged.connect(lambda: self.negative(self.ui.comboBox, self.ui.lineEdit_10))
        self.ui.comboBox_7.currentTextChanged.connect(lambda: self.negative(self.ui.comboBox_7, self.ui.lineEdit_11))
        self.ui.comboBox_8.currentTextChanged.connect(lambda: self.negative(self.ui.comboBox_8, self.ui.lineEdit_12))

        #σύνδεση του lineEdit_7 με την def update_lineEdit_8
        self.ui.lineEdit_7.textChanged.connect(self.update_lineEdit_8)

        self.ui.lineEdit_9.textChanged.connect(self.age_lineEdit_9)

        self.ui.lineEdit.textChanged.connect(self.result_lineEdit_13)
        self.ui.lineEdit_2.textChanged.connect(self.result_lineEdit_13)
        self.ui.lineEdit_3.textChanged.connect(self.result_lineEdit_13)
        self.ui.lineEdit_4.textChanged.connect(self.result_lineEdit_13)
        self.ui.lineEdit_5.textChanged.connect(self.result_lineEdit_13)
        self.ui.lineEdit_6.textChanged.connect(self.result_lineEdit_13)
        self.ui.lineEdit_8.textChanged.connect(self.result_lineEdit_13)
        self.ui.lineEdit_10.textChanged.connect(self.result_lineEdit_13)
        self.ui.lineEdit_11.textChanged.connect(self.result_lineEdit_13)
        self.ui.lineEdit_12.textChanged.connect(self.result_lineEdit_13)
      
        self.selected_periferia = None

    def positive(self, combo, line_edit):
        """Εμφάνιση αποτελέσματος ΕΠΙΛΕΞΙΜΟΣ/ΜΗ ΕΠΙΛΕΞΙΜΟΣ"""
        if combo.currentText() == "Ναι":
            line_edit.setText("ΕΠΙΛΕΞΙΜΟΣ")
            line_edit.setAlignment(Qt.AlignCenter)
            line_edit.setStyleSheet("""QLineEdit[readOnly=true]{
                                            background-color: #4CAF50;
                                            color: white;
                                            font-weight: bold;
                                            border: 2px solid #45a049;}""")
            
        elif combo.currentText() == "Όχι":
            line_edit.setText("ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
            line_edit.setAlignment(Qt.AlignCenter)
            line_edit.setStyleSheet("""QLineEdit[readOnly=true]{
                                    background-color: #F44336;
                                    color: white;
                                    font-weight: bold;
                                    border: 2px solid #D32F2F;}""")
        else:
            line_edit.clear()
            line_edit.setStyleSheet('QLineEdit[readOnly=true]{background-color: #E3F2FD;}')

    def negative(self, combo, line_edit):
        """Εμφάνιση αποτελέσματος ΕΠΙΛΕΞΙΜΟΣ/ΜΗ ΕΠΙΛΕΞΙΜΟΣ"""
        if combo.currentText() == "Ναι":
            line_edit.setText("ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
            line_edit.setAlignment(Qt.AlignCenter)
            line_edit.setStyleSheet("""QLineEdit[readOnly=true]{
                                    background-color: #F44336;
                                    color: white;
                                    font-weight: bold;
                                    border: 2px solid #D32F2F;}""")
            
        elif combo.currentText() == "Όχι":
            line_edit.setText("ΕΠΙΛΕΞΙΜΟΣ")
            line_edit.setAlignment(Qt.AlignCenter)
            line_edit.setStyleSheet("""QLineEdit[readOnly=true]{
                                            background-color: #4CAF50;
                                            color: white;
                                            font-weight: bold;
                                            border: 2px solid #45a049;}""")
        else:
            line_edit.clear()
            line_edit.setStyleSheet('QLineEdit[readOnly=true]{background-color: #E3F2FD;}')
    
    def age_lineEdit_9(self):
        if not self.ui.lineEdit_9.text():
            self.ui.lineEdit.clear()
            self.ui.lineEdit.setStyleSheet('QLineEdit[readOnly=true]{background-color: #E3F2FD;}')
            return
        try:
            lineEdit_int=int(self.ui.lineEdit_9.text())
        except ValueError:
            self.ui.lineEdit.clear()
            self.ui.lineEdit.setStyleSheet('QLineEdit[readOnly=true]{background-color: #E3F2FD;}')
            return
        if lineEdit_int>=18 and lineEdit_int<=62:
            self.ui.lineEdit.setText("ΕΠΙΛΕΞΙΜΟΣ")
            self.ui.lineEdit.setAlignment(Qt.AlignCenter)
            self.ui.lineEdit.setStyleSheet("""QLineEdit[readOnly=true]{
                                            background-color: #4CAF50;
                                            color: white;
                                            font-weight: bold;
                                            border: 2px solid #45a049;}""")
        elif lineEdit_int>=0 and lineEdit_int<18 or lineEdit_int>62:
            self.ui.lineEdit.setText("ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
            self.ui.lineEdit.setAlignment(Qt.AlignCenter)
            self.ui.lineEdit.setStyleSheet("""QLineEdit[readOnly=true]{
                                    background-color: #F44336;
                                    color: white;
                                    font-weight: bold;
                                    border: 2px solid #D32F2F;}""")
        else:
            self.ui.lineEdit.clear()
            self.ui.lineEdit.setStyleSheet('QLineEdit[readOnly=true]{background-color: #E3F2FD;}')

    
    def result_lineEdit_13(self):
        """"Συγκεντρωτικό Αποτέλεσμα ΕΠΙΛΕΞΙΜΟΣ/ΜΗ ΕΠΙΛΕΞΙΜΟΣ"""
        fields = [
            self.ui.lineEdit,
            self.ui.lineEdit_2,
            self.ui.lineEdit_3,
            self.ui.lineEdit_4,
            self.ui.lineEdit_5,
            self.ui.lineEdit_6,
            self.ui.lineEdit_8,
            self.ui.lineEdit_10,
            self.ui.lineEdit_11,
            self.ui.lineEdit_12
        
        ]

        
        if any(f.text().strip() == "ΜΗ ΕΠΙΛΕΞΙΜΟΣ" for f in fields):
            self.ui.lineEdit_13.setText("ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
            self.ui.lineEdit_13.setAlignment(Qt.AlignCenter)
            self.ui.lineEdit_13.setStyleSheet("""QLineEdit[readOnly=true]{
                                    background-color: #F44336;
                                    color: white;
                                    font-weight: bold;
                                    border: 2px solid #D32F2F;}""")
        elif all(f.text().strip() == "ΕΠΙΛΕΞΙΜΟΣ" for f in fields):
            self.ui.lineEdit_13.setText("ΕΠΙΛΕΞΙΜΟΣ")
            self.ui.lineEdit_13.setAlignment(Qt.AlignCenter)
            self.ui.lineEdit_13.setStyleSheet("""QLineEdit[readOnly=true]{
                                            background-color: #4CAF50;
                                            color: white;
                                            font-weight: bold;
                                            border: 2px solid #45a049;}""")
        else:
            self.ui.lineEdit_13.clear()
            self.ui.lineEdit_13.setStyleSheet('QLineEdit[readOnly=true]{background-color: #E3F2FD;}')
            






    def recalculate_all_results(self):
            """Eπανυπολογισμός combobox και lineEdit8"""

            
            self.positive(self.ui.comboBox_2, self.ui.lineEdit_2)
            self.positive(self.ui.comboBox_3, self.ui.lineEdit_3)
            self.positive(self.ui.comboBox_4, self.ui.lineEdit_4)
            self.positive(self.ui.comboBox_5, self.ui.lineEdit_5)
            self.positive(self.ui.comboBox_6, self.ui.lineEdit_6)
            self.negative(self.ui.comboBox, self.ui.lineEdit_10)
            self.negative(self.ui.comboBox_7, self.ui.lineEdit_11)
            self.negative(self.ui.comboBox_8, self.ui.lineEdit_12)
            
            self.update_lineEdit_8() 
            self.age_lineEdit_9() 
            self.result_lineEdit_13()

    def eventFilter(self, obj, event):
        if isinstance(obj, QComboBox) and event.type() == QEvent.Wheel:
            return True  
        return super().eventFilter(obj, event)
    
    def update_lineEdit_7(self, value):  
            self.ui.lineEdit_7.setText(value)
            self.ui.lineEdit_7.setAlignment(Qt.AlignCenter)

    def update_lineEdit_8(self):
        """ΕΠΙΛΕΞΙΜΟΣ/ΜΗ ΕΠΙΛΕΞΙΜΟΣ στο lineEdit_8"""
        text=self.ui.lineEdit_7.text().strip()
        if not text:
            self.ui.lineEdit_8.clear()
            self.ui.lineEdit_8.setStyleSheet(
            'QLineEdit[readOnly=true]{background-color: #E3F2FD;}'
        )
            return

        try:
            float_text=float(text)
        except ValueError:
            self.ui.lineEdit_8.clear()
            self.ui.lineEdit_8.setStyleSheet(
                'QLineEdit[readOnly=true]{background-color: #E3F2FD;}'
            )
            return
        if self.selected_periferia in ISLANDS:
            if float_text>=8000:
                self.ui.lineEdit_8.setText("ΕΠΙΛΕΞΙΜΟΣ")
                self.ui.lineEdit_8.setAlignment(Qt.AlignCenter)
                self.ui.lineEdit_8.setStyleSheet("""QLineEdit[readOnly=true]{
                                                background-color: #4CAF50;
                                                color: white;
                                                font-weight: bold;
                                                border: 2px solid #45a049;}""")
            else:
                self.ui.lineEdit_8.setText("ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
                self.ui.lineEdit_8.setAlignment(Qt.AlignCenter)
                self.ui.lineEdit_8.setStyleSheet("""QLineEdit[readOnly=true]{
                                        background-color: #F44336;
                                        color: white;
                                        font-weight: bold;
                                        border: 2px solid #D32F2F;}""")
        else:
            if float_text>=12000:
                self.ui.lineEdit_8.setText("ΕΠΙΛΕΞΙΜΟΣ")
                self.ui.lineEdit_8.setAlignment(Qt.AlignCenter)
                self.ui.lineEdit_8.setStyleSheet("""QLineEdit[readOnly=true]{
                                                background-color: #4CAF50;
                                                color: white;
                                                font-weight: bold;
                                                border: 2px solid #45a049;}""")
            else:
                self.ui.lineEdit_8.setText("ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
                self.ui.lineEdit_8.setAlignment(Qt.AlignCenter)
                self.ui.lineEdit_8.setStyleSheet("""QLineEdit[readOnly=true]{
                                        background-color: #F44336;
                                        color: white;
                                        font-weight: bold;
                                        border: 2px solid #D32F2F;}""")

    def get_eligibility_data(self):
        """Μαζεύει τις απαντήσεις από τα Comboboxes και την ΤΑ για αποθήκευση."""
        # Επιστρέφει ένα tuple με τις τιμές που περιμένει η save_eligibility_data
        return (
            self.ui.lineEdit_9.text().strip(),# q1
            self.ui.comboBox_2.currentText(), # q2
            self.ui.comboBox_3.currentText(), # q3
            self.ui.comboBox_4.currentText(), # q4
            self.ui.comboBox_5.currentText(), # q5
            self.ui.comboBox_6.currentText(), # q6
            self.ui.comboBox.currentText(), # q7
            self.ui.comboBox_7.currentText(), # q8
            self.ui.comboBox_8.currentText(), # q9
            self.ui.lineEdit_7.text().strip(),        # typical_output_val
            self.ui.lineEdit_13.text().strip()  # eligibility_result
        )

    def set_eligibility_data(self, data):
        """Τοποθετεί τα δεδομένα από τη βάση στα widgets της σελίδας."""
        if not data:
            return

        def s(v):
            return "" if v is None else str(v)

        def num(v):
            if v is None or v == "":
                return ""
            try:
                return "{:.2f}".format(float(v))
            except (TypeError, ValueError):
                return str(v)

        # Το data έρχεται από τη fetch_eligibility: (q1, q2, q3, q4, q5, q6, val)
        self.ui.lineEdit_9.setText(s(data[0]))
        self.ui.comboBox_2.setCurrentText(s(data[1]))
        self.ui.comboBox_3.setCurrentText(s(data[2]))
        self.ui.comboBox_4.setCurrentText(s(data[3]))
        self.ui.comboBox_5.setCurrentText(s(data[4]))
        self.ui.comboBox_6.setCurrentText(s(data[5]))
        self.ui.comboBox.setCurrentText(s(data[6]))
        self.ui.comboBox_7.setCurrentText(s(data[7]))
        self.ui.comboBox_8.setCurrentText(s(data[8]))
        self.ui.lineEdit_7.setText(num(data[9]))
        self.ui.lineEdit_13.setText(s(data[10]))


    def clear_page_epi(self):
        """Καθαρισμός lineEdit και combobox"""
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_7.clear()
        self.ui.lineEdit_8.clear()
        self.ui.lineEdit_9.clear()
        self.ui.lineEdit_10.clear()
        self.ui.lineEdit_11.clear()
        self.ui.lineEdit_12.clear()
        self.ui.lineEdit_13.clear()
        self.ui.lineEdit.setStyleSheet("")
        self.ui.lineEdit_2.setStyleSheet("")
        self.ui.lineEdit_3.setStyleSheet("")
        self.ui.lineEdit_4.setStyleSheet("")
        self.ui.lineEdit_5.setStyleSheet("")
        self.ui.lineEdit_6.setStyleSheet("")
        self.ui.lineEdit_8.setStyleSheet("")
        self.ui.lineEdit_10.setStyleSheet("")
        self.ui.lineEdit_11.setStyleSheet("")
        self.ui.lineEdit_12.setStyleSheet("")
        self.ui.lineEdit_13.setStyleSheet("")
        
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.comboBox_3.setCurrentIndex(0)
        self.ui.comboBox_4.setCurrentIndex(0)
        self.ui.comboBox_5.setCurrentIndex(0)
        self.ui.comboBox_6.setCurrentIndex(0)
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_7.setCurrentIndex(0)
        self.ui.comboBox_8.setCurrentIndex(0)

       

        
