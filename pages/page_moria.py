from PySide2.QtWidgets import QWidget, QComboBox, QListView
from PySide2.QtCore import QEvent, QRegExp, Qt
from PySide2.QtGui import QRegExpValidator, QFontMetrics
from ui.ui_page_moria import Ui_page_moria
from utils.decimal_utils import to_decimal, q2, fmt2
from decimal import Decimal



class moriaPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_page_moria()
        self.ui.setupUi(self)

        for combo in (
              self.ui.comboBox_1_1,
              self.ui.comboBox_3_1_2,
              self.ui.comboBox_3_1_3,
              self.ui.comboBox_3_1_4,
              self.ui.comboBox_3_2,
              self.ui.comboBox_3_3,
              self.ui.comboBox_3_4,
              self.ui.comboBox_3_5,
              self.ui.comboBox_6_1,
              self.ui.comboBox_7_1):
            combo.installEventFilter(self)
            
            fm = QFontMetrics(combo.font())
            max_width = max(fm.horizontalAdvance(combo.itemText(i)) 
                        for i in range(combo.count())) + 40  # +40 για padding
            view = QListView()
            view.setMinimumWidth(max_width)
            combo.setView(view)
            

        self.selected_periferia = None

         #βάζουμε read only τα lineEdit
        self.ui.lineEdit_1_1_moria.setReadOnly(True)
        self.ui.lineEdit_1_2.setReadOnly(True)
        self.ui.lineEdit_1_2_moria.setReadOnly(True)
        self.ui.lineEdit_2_1.setReadOnly(True)
        self.ui.lineEdit_2_1_moria.setReadOnly(True)
        self.ui.lineEdit_2_2.setReadOnly(True)
        self.ui.lineEdit_2_2_moria.setReadOnly(True)
        self.ui.lineEdit_3_1_1_moria.setReadOnly(True)
        self.ui.lineEdit_3_1_2_moria.setReadOnly(True)
        self.ui.lineEdit_3_1_3_moria.setReadOnly(True)
        self.ui.lineEdit_3_1_4_moria.setReadOnly(True)
        self.ui.lineEdit_3_2_moria.setReadOnly(True)
        self.ui.lineEdit_3_3_moria.setReadOnly(True)
        self.ui.lineEdit_3_4_moria.setReadOnly(True)
        self.ui.lineEdit_3_5_moria.setReadOnly(True)
        self.ui.lineEdit_4_1_moria.setReadOnly(True)
        self.ui.lineEdit_5_1_moria.setReadOnly(True)
        self.ui.lineEdit_6_1_moria.setReadOnly(True)
        self.ui.lineEdit_7_1_moria.setReadOnly(True)
        self.ui.lineEdit_moria.setReadOnly(True)
        self.ui.lineEdit_epileximos.setReadOnly(True)

        #βάζουμε align center τα lineEdit

        self.ui.lineEdit_1_1_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_1_2.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_1_2_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_2_1.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_2_1_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_2_2.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_2_2_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_3_1_1.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_3_1_1_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_3_1_2_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_3_1_3_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_3_1_4_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_3_2_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_3_3_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_3_4_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_3_5_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_4_1.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_4_1_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_5_1.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_5_1_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_6_1_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_7_1_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_moria.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_epileximos.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_budget.setAlignment(Qt.AlignCenter)

        #περιορισμός έως 9 ψηφίων στο lineEdit του ΑΦΜ
        
        regex = QRegExp(r"^\d{0,7}(?:[.]\d{0,2})?$") # έως 7 ψηφία στο ακέραιο μέρος και έως 2 στα δεκαδικά
        validator = QRegExpValidator(regex)
        self.ui.lineEdit_3_1_1.setValidator(validator)
        self.ui.lineEdit_4_1.setValidator(validator)
        self.ui.lineEdit_5_1.setValidator(validator)
        self.ui.lineEdit_budget.setValidator(validator)

        for le in (self.ui.lineEdit_3_1_1,
           self.ui.lineEdit_4_1,
           self.ui.lineEdit_5_1,
           self.ui.lineEdit_budget):
            le.editingFinished.connect(lambda le=le: self._format_lineEdit(le))

        #σύνδεση για τον υπολογισμό των μορίων ανάλογα με τις απαντήσεις των combobox
        self.ui.comboBox_1_1.currentTextChanged.connect(lambda: self.moria_1_1())
        self.ui.comboBox_3_1_2.currentTextChanged.connect(lambda: self.moria_3_1_2())
        self.ui.comboBox_3_1_3.currentTextChanged.connect(lambda: self.moria_3_1_3())
        self.ui.comboBox_3_1_4.currentTextChanged.connect(lambda: self.moria_3_1_4())
        self.ui.comboBox_3_2.currentTextChanged.connect(lambda: self.moria_3_2())
        self.ui.comboBox_3_3.currentTextChanged.connect(lambda: self.moria_3_3())
        self.ui.comboBox_3_4.currentTextChanged.connect(lambda: self.moria_3_4())
        self.ui.comboBox_3_5.currentTextChanged.connect(lambda: self.moria_3_5())
        self.ui.comboBox_6_1.currentTextChanged.connect(lambda: self.moria_6_1())
        self.ui.comboBox_7_1.currentTextChanged.connect(lambda: self.moria_7_1())

        #σύνδεση lineEdits για τον υπολογισμό της συνολικής μοριοδότησης 
        self.ui.lineEdit_1_1_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_1_2_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_2_1_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_2_2_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_3_1_1_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_3_1_2_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_3_1_3_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_3_1_4_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_3_2_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_3_3_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_3_4_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_3_5_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_4_1_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_5_1_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_6_1_moria.textChanged.connect(self.sum_total_moria)
        self.ui.lineEdit_7_1_moria.textChanged.connect(self.sum_total_moria)

        #Σύνδεση budget για άμεση ενημέρωση της επιλεξιμότητας (το budget είναι μέρος των 17 πεδίων)
        self.ui.lineEdit_budget.textChanged.connect(self.epilex_moria)
        #Σύνδεση για τον υπολογισμό μορίων του κριτηρίου 1.2
        self.ui.lineEdit_1_2.textChanged.connect(self.moria_1_2)
        #Σύνδεση για τον υπολογισμό μορίων του κριτηρίου 2.1
        self.ui.lineEdit_2_1.textChanged.connect(self.moria_2_1)
        #Σύνδεση για τον υπολογισμό μορίων του κριτηρίου 2.2
        self.ui.lineEdit_2_2.textChanged.connect(self.moria_2_2)
        self.ui.lineEdit_budget.textChanged.connect(self.moria_2_2)
        #Σύνδεση για τον υπολογισμό μορίων του κριτηρίου 3.1.1
        self.ui.lineEdit_3_1_1.textChanged.connect(self.moria_3_1_1)
        self.ui.lineEdit_budget.textChanged.connect(self.moria_3_1_1)
        #Σύνδεση για τον υπολογισμό μορίων του κριτηρίου 4.1
        self.ui.lineEdit_4_1.textChanged.connect(self.moria_4_1)
        self.ui.lineEdit_budget.textChanged.connect(self.moria_4_1)
        #Σύνδεση για τον υπολογισμό μορίων του κριτηρίου 5.1
        self.ui.lineEdit_5_1.textChanged.connect(self.moria_5_1)
        self.ui.lineEdit_budget.textChanged.connect(self.moria_5_1)

        

    def _format_lineEdit(self, line_edit):
        """Μορφοποίηση lineEdit σε 2 δεκαδικά"""
        text = line_edit.text().strip()
        if not text or text == ".":
            line_edit.setText("")
            return
        formatted = fmt2(text)
        line_edit.setText(formatted)

    def moria_1_1(self):
        """Yπολογισμός κριτηρίου επιλογής 1.1"""
        if self.ui.comboBox_1_1.currentText() == "Ναι":
            self.ui.lineEdit_1_1_moria.setText("5.00")
            
            
        elif self.ui.comboBox_1_1.currentText() == "Όχι":
            self.ui.lineEdit_1_1_moria.setText("0.00")
        else:
            self.ui.lineEdit_1_1_moria.clear()

    def moria_1_2(self):
        """Υπολογισμός μορίων κριτηρίου 1.2"""
        try:
            biologic_text=self.ui.lineEdit_1_2.text().strip()
            if not biologic_text:
                self.ui.lineEdit_1_2_moria.setText("")
                return
            biologic_float=float(biologic_text.replace("%",""))
            if biologic_float>50:
                self.ui.lineEdit_1_2_moria.setText("6.00")
            else:
                self.ui.lineEdit_1_2_moria.setText("0.00")
        except (ValueError, TypeError):
            self.ui.lineEdit_1_2_moria.setText("")



    def moria_2_1(self):
        """Υπολογισμός μορίων κριτηρίου 2.1"""
        try:
            ta = to_decimal(self.ui.lineEdit_2_1.text())
            if ta is None:
                self.ui.lineEdit_2_1_moria.setText("")
                return
            if ta < 16000:
                self.ui.lineEdit_2_1_moria.setText("2.50")
            elif ta <= 25000:
                moria = 50 + 50 * (ta - 16000) / 9000
                self.ui.lineEdit_2_1_moria.setText(fmt2(moria * Decimal("0.05")))
            elif ta > 25000:
                self.ui.lineEdit_2_1_moria.setText("5.00")
            else:
                self.ui.lineEdit_2_1_moria.setText("")

        except Exception:
            self.ui.lineEdit_2_1_moria.setText("")
    
    def moria_2_2(self):
        """Υπολογισμός μορίων κριτηρίου 2.2"""
        try:
            ta = to_decimal(self.ui.lineEdit_2_2.text())
            budget = to_decimal(self.ui.lineEdit_budget.text())
            if ta is None or budget is None:
                self.ui.lineEdit_2_2_moria.setText("")
                return
            ta_5x = ta * 5
            ta_6x = ta * 6
            if ta <= 15000 and budget <= 75000:
                self.ui.lineEdit_2_2_moria.setText("16.00")
            elif ta > 15000 and budget <= ta_5x:
                self.ui.lineEdit_2_2_moria.setText("16.00")
            elif ta > 12500 and budget <= ta_6x:
                self.ui.lineEdit_2_2_moria.setText("9.60")
            else:
                self.ui.lineEdit_2_2_moria.setText("0.00")

        except Exception:
            self.ui.lineEdit_2_2_moria.setText("")
    
    def moria_3_1_1(self):
        """Yπολογισμός κριτηρίου επιλογής 3.1.1"""
        try:
            idia = to_decimal(self.ui.lineEdit_3_1_1.text())
            budget = to_decimal(self.ui.lineEdit_budget.text())

            if idia is None or budget is None:
                self.ui.lineEdit_3_1_1_moria.setText("")
                return

            if budget == 0:
                self.ui.lineEdit_3_1_1_moria.setText("0.00")
                return

            ratio = idia / budget

            if ratio <= Decimal("0.2"):
                self.ui.lineEdit_3_1_1_moria.setText("0.00")

            elif ratio > Decimal("0.5"):
                self.ui.lineEdit_3_1_1_moria.setText("7.00")

            else:
                # γραμμική παρεμβολή μεταξύ [0.2, 0.5] → [20, 50]
                moria = 20 + 30 * (ratio - Decimal("0.2")) / Decimal("0.3")
                self.ui.lineEdit_3_1_1_moria.setText(fmt2(moria * Decimal("0.14")))

        except Exception:
            self.ui.lineEdit_3_1_1_moria.setText("")

    def moria_3_1_2(self):
        """Yπολογισμός κριτηρίου επιλογής 3.1.2"""
        if self.ui.comboBox_3_1_2.currentText() == "Ναι":
            self.ui.lineEdit_3_1_2_moria.setText("4.20")
            
            
        elif self.ui.comboBox_3_1_2.currentText() == "Όχι":
            self.ui.lineEdit_3_1_2_moria.setText("0.00")
        else:
            self.ui.lineEdit_3_1_2_moria.clear()

    def moria_3_1_3(self):
        """Yπολογισμός κριτηρίου επιλογής 3.1.3"""
        if self.ui.comboBox_3_1_3.currentText() == "Ναι":
            self.ui.lineEdit_3_1_3_moria.setText("1.40")
            
            
        elif self.ui.comboBox_3_1_3.currentText() == "Όχι":
            self.ui.lineEdit_3_1_3_moria.setText("0.00")
        else:
            self.ui.lineEdit_3_1_3_moria.clear()

    def moria_3_1_4(self):
        """Yπολογισμός κριτηρίου επιλογής 3.1.4"""
        if self.ui.comboBox_3_1_4.currentText() == "Ναι":
            self.ui.lineEdit_3_1_4_moria.setText("1.40")
            
            
        elif self.ui.comboBox_3_1_4.currentText() == "Όχι":
            self.ui.lineEdit_3_1_4_moria.setText("0.00")
        else:
            self.ui.lineEdit_3_1_4_moria.clear()

   

    def moria_3_2(self):
        """Yπολογισμός κριτηρίου επιλογής 3.2"""
        if self.ui.comboBox_3_2.currentText()=="Νέος Αγρότης 2018 ή 2021" or self.ui.comboBox_3_2.currentText()=="Επιλαχόντας του Μ6.1" or self.ui.comboBox_3_2.currentText()=="Εμπειρία >5 ετών και έως 50 ετών":
            self.ui.lineEdit_3_2_moria.setText("8.00")
        elif self.ui.comboBox_3_2.currentText()=="Κανένα από τα παραπάνω":
            self.ui.lineEdit_3_2_moria.setText("0.00")
        
        else:
            self.ui.lineEdit_3_2_moria.setText("")  

    def moria_3_3(self):
        """Yπολογισμός κριτηρίου επιλογής 3.3"""
        if self.ui.comboBox_3_3.currentText()=="Κατοχή πτυχίου >= 6, 7, 8" or self.ui.comboBox_3_3.currentText()=="Κατοχή γεωτεχνικού πτυχίου =< 3, 4, 5" :
            self.ui.lineEdit_3_3_moria.setText("3.50")
        elif self.ui.comboBox_3_3.currentText()=="Κατοχή γεωτεχνικού πτυχίου >= 6, 7, 8":
            self.ui.lineEdit_3_3_moria.setText("5.00")
        elif self.ui.comboBox_3_3.currentText()=="Κανένα από τα παραπάνω":
            self.ui.lineEdit_3_3_moria.setText("0.00")
        
        else:
            self.ui.lineEdit_3_3_moria.setText("") 

    def moria_3_4(self):
        """Yπολογισμός κριτηρίου επιλογής 3.4"""
        if self.ui.comboBox_3_4.currentText()=="ΟΠ/Ομ.Π με μέλη>10" :
            self.ui.lineEdit_3_4_moria.setText("2.40")
        elif self.ui.comboBox_3_4.currentText()=="ΑΣ" :
            self.ui.lineEdit_3_4_moria.setText("3.60")
        elif self.ui.comboBox_3_4.currentText()=="ΑΣ και ΟΠ/Ομ.Π με μέλη>10"  or self.ui.comboBox_3_4.currentText()=="Αναγκαστικός Συνεταιρισμός" :
            self.ui.lineEdit_3_4_moria.setText("6.00")
        elif self.ui.comboBox_3_4.currentText()=="Κανένα από τα παραπάνω":
            self.ui.lineEdit_3_4_moria.setText("0.00")
        
        else:
            self.ui.lineEdit_3_4_moria.setText("") 

    def moria_3_5(self):
        """Yπολογισμός κριτηρίου επιλογής 3.5"""
        if self.ui.comboBox_3_5.currentText() == "Ναι":
            self.ui.lineEdit_3_5_moria.setText("2.00")
            
            
        elif self.ui.comboBox_3_5.currentText() == "Όχι":
            self.ui.lineEdit_3_5_moria.setText("0.00")
        else:
            self.ui.lineEdit_3_5_moria.clear()

    def moria_4_1(self):
        """Yπολογισμός κριτηρίου επιλογής 4.1"""
        try:
            poso_4_1_text = self.ui.lineEdit_4_1.text().strip()
            budget_text = self.ui.lineEdit_budget.text().strip()

            if not poso_4_1_text or not budget_text:
                self.ui.lineEdit_4_1_moria.setText("")
                return

            poso = to_decimal(poso_4_1_text)
            budget = to_decimal(budget_text)

            if poso is None or budget is None:
                self.ui.lineEdit_4_1_moria.setText("")
                return

            if budget == 0:
                self.ui.lineEdit_4_1_moria.setText("0.00")
                return

            ratio = poso / budget

            if ratio <= Decimal("0.1"):
                self.ui.lineEdit_4_1_moria.setText("0.00")

            elif ratio > Decimal("0.6"):
                self.ui.lineEdit_4_1_moria.setText("12.00")

            else:
                # γραμμική παρεμβολή μεταξύ [0.1, 0.6] → [10, 100]
                moria = 10 + 90 * (ratio - Decimal("0.1")) / Decimal("0.5")
                self.ui.lineEdit_4_1_moria.setText(fmt2(moria * Decimal("0.12")))

        except Exception:
            self.ui.lineEdit_4_1_moria.setText("")

    def moria_5_1(self):
        """Yπολογισμός κριτηρίου επιλογής 5.1"""
        try:
            poso_5_1_text = self.ui.lineEdit_5_1.text().strip()
            budget_text = self.ui.lineEdit_budget.text().strip()

            if not poso_5_1_text or not budget_text:
                self.ui.lineEdit_5_1_moria.setText("")
                return

            poso = to_decimal(poso_5_1_text)
            budget = to_decimal(budget_text)

            if poso is None or budget is None:
                self.ui.lineEdit_5_1_moria.setText("")
                return

            if budget == 0:
                self.ui.lineEdit_5_1_moria.setText("0.00")
                return

            ratio = poso / budget

            if ratio <= Decimal("0.05"):
                self.ui.lineEdit_5_1_moria.setText("0.00")

            elif ratio > Decimal("0.2"):
                self.ui.lineEdit_5_1_moria.setText("12.00")

            else:
                # γραμμική παρεμβολή μεταξύ [0.05, 0.2] → [10, 100]
                moria = 10 + 90 * (ratio - Decimal("0.05")) / Decimal("0.15")
                self.ui.lineEdit_5_1_moria.setText(fmt2(moria * Decimal("0.08")))

        except Exception:
            self.ui.lineEdit_5_1_moria.setText("")

    

    def moria_6_1(self):
        """Yπολογισμός κριτηρίου επιλογής 6.1"""
        if self.ui.comboBox_6_1.currentText() == "Ναι":
            self.ui.lineEdit_6_1_moria.setText("13.00")
            
            
        elif self.ui.comboBox_6_1.currentText() == "Όχι":
            self.ui.lineEdit_6_1_moria.setText("0.00")
        else:
            self.ui.lineEdit_6_1_moria.clear()

    def moria_7_1(self):
        """Yπολογισμός κριτηρίου επιλογής 7.1"""
        if self.ui.comboBox_7_1.currentText() == "Ναι":
            self.ui.lineEdit_7_1_moria.setText("3.00")
            
            
        elif self.ui.comboBox_7_1.currentText() == "Όχι":
            self.ui.lineEdit_7_1_moria.setText("0.00")
        else:
            self.ui.lineEdit_7_1_moria.clear()

    
    def sum_total_moria(self):
        """Αθροίζει τα μόρια του υποψήφιου"""
        fields = [
            self.ui.lineEdit_1_1_moria,
            self.ui.lineEdit_1_2_moria,
            self.ui.lineEdit_2_1_moria,
            self.ui.lineEdit_2_2_moria,
            self.ui.lineEdit_3_1_1_moria,
            self.ui.lineEdit_3_1_2_moria,
            self.ui.lineEdit_3_1_3_moria,
            self.ui.lineEdit_3_1_4_moria,
            self.ui.lineEdit_3_2_moria,
            self.ui.lineEdit_3_3_moria,
            self.ui.lineEdit_3_4_moria,
            self.ui.lineEdit_3_5_moria,
            self.ui.lineEdit_4_1_moria,
            self.ui.lineEdit_5_1_moria,
            self.ui.lineEdit_6_1_moria,
            self.ui.lineEdit_7_1_moria,
        ]

       
        if all(f.text().strip() == "" for f in fields):
            self.ui.lineEdit_moria.setText("")
            self.epilex_moria()
            return

        total = Decimal(0)
        for f in fields:
            v = to_decimal(f.text())
            if v is not None:
                total += v
        self.ui.lineEdit_moria.setText(fmt2(total))
        self.epilex_moria()

    def epilex_moria(self):
        """Τιμή LineEdit Επιλεξιμότητας Μοριοδότησης"""
        try:
            fields=[
                self.ui.lineEdit_1_1_moria,
            self.ui.lineEdit_1_2_moria,
            self.ui.lineEdit_2_1_moria,
            self.ui.lineEdit_2_2_moria,
            self.ui.lineEdit_3_1_1_moria,
            self.ui.lineEdit_3_1_2_moria,
            self.ui.lineEdit_3_1_3_moria,
            self.ui.lineEdit_3_1_4_moria,
            self.ui.lineEdit_3_2_moria,
            self.ui.lineEdit_3_3_moria,
            self.ui.lineEdit_3_4_moria,
            self.ui.lineEdit_3_5_moria,
            self.ui.lineEdit_4_1_moria,
            self.ui.lineEdit_5_1_moria,
            self.ui.lineEdit_6_1_moria,
            self.ui.lineEdit_7_1_moria,
            self.ui.lineEdit_budget

            ]
            if any(f.text().strip()=="" for f in fields):
                self.ui.lineEdit_epileximos.setText("")
                self.ui.lineEdit_epileximos.setStyleSheet('QLineEdit[readOnly=true]{background-color: #E3F2FD;}')
                return 
            moria_text=self.ui.lineEdit_moria.text().strip()
            if  moria_text:
                moria_float=float(moria_text)
                if moria_float<40 :
                    self.ui.lineEdit_epileximos.setText("ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
                    self.ui.lineEdit_epileximos.setStyleSheet("""QLineEdit[readOnly=true]{
                                        background-color: #F44336;
                                        color: white;
                                        font-weight: bold;
                                        border: 2px solid #D32F2F;}""")
                else :
                    self.ui.lineEdit_epileximos.setText("ΕΠΙΛΕΞΙΜΟΣ")
                    self.ui.lineEdit_epileximos.setStyleSheet("""QLineEdit[readOnly=true]{
                                                background-color: #4CAF50;
                                                color: white;
                                                font-weight: bold;
                                                border: 2px solid #45a049;}""")
            else :
                self.ui.lineEdit_epileximos.setText("")
                self.ui.lineEdit_epileximos.setStyleSheet('QLineEdit[readOnly=true]{background-color: #E3F2FD;}')
                
                
        except(ValueError,TypeError):
            self.ui.lineEdit_epileximos.setText("")
            self.ui.lineEdit_epileximos.setStyleSheet('QLineEdit[readOnly=true]{background-color: #E3F2FD;}')
            
            

    def eventFilter(self, obj, event):
        if isinstance(obj, QComboBox) and event.type() == QEvent.Wheel:
            return True  
        return super().eventFilter(obj, event)
    
    def update_lineEdit_1_2(self, value):  
            self.ui.lineEdit_1_2.setText(value)
    
    def update_lineEdit_2_1(self, value):  
            self.ui.lineEdit_2_1.setText(value)
            # self.ui.lineEdit_2_1.setAlignment(Qt.AlignCenter)
    def update_lineEdit_2_2(self, value):  
            self.ui.lineEdit_2_2.setText(value)
    
    def recalculate_all_results_moria(self):
            """Eπανυπολογισμός combobox και lineEdits"""
            self.moria_1_1()
            self.moria_1_2()
            self.moria_2_1()
            self.moria_2_2()
            self.moria_3_1_1()
            self.moria_3_1_2()
            self.moria_3_1_3()
            self.moria_3_1_4()
            self.moria_3_2()
            self.moria_3_3()
            self.moria_3_4()
            self.moria_3_5()
            self.moria_4_1()
            self.moria_5_1()
            self.moria_6_1()
            self.moria_7_1()
            self.sum_total_moria()
           
    
    def get_moria_data(self):
        """Μαζεύει τις απαντήσεις από τα Comboboxes και τα lineEdits."""
        # Επιστρέφει ένα tuple με τις  τιμές που περιμένει η save_moria_data
        return (
            self.ui.comboBox_1_1.currentText(),  
            self.ui.lineEdit_1_2.text().strip(),
            self.ui.lineEdit_2_1.text().strip(),  
            self.ui.lineEdit_2_2.text().strip(),
            self.ui.lineEdit_3_1_1.text().strip(),
            self.ui.comboBox_3_1_2.currentText(), 
            self.ui.comboBox_3_1_3.currentText(), 
            self.ui.comboBox_3_1_4.currentText(), 
            self.ui.comboBox_3_2.currentText(),
            self.ui.comboBox_3_3.currentText(), 
            self.ui.comboBox_3_4.currentText(),
            self.ui.comboBox_3_5.currentText(), 
            self.ui.lineEdit_4_1.text().strip(), 
            self.ui.lineEdit_5_1.text().strip(), 
            self.ui.comboBox_6_1.currentText(), 
            self.ui.comboBox_7_1.currentText(),
            self.ui.lineEdit_budget.text().strip(),
            self.ui.lineEdit_moria.text().strip(),
            self.ui.lineEdit_epileximos.text().strip()   # moria_epileximos
        )

    def set_moria_data(self, data):
        """Τοποθετεί τα δεδομένα από τη βάση στα widgets της σελίδας."""
        if not data:
            return

        def s(v):
            return "" if v is None else str(v)

        # def num(v):
        #     return fmt2(v)
        def num(v):
            if v is None or v == "":
                return ""
            try:
                return "{:.2f}".format(float(v))
            except (TypeError, ValueError):
                return str(v)

        # Το data έρχεται από τη fetch_moria: (q1, q2, q3, q4, q5, q6, val)
        self.ui.comboBox_1_1.setCurrentText(s(data[0]))
        self.ui.lineEdit_1_2.setText(s(data[1]))
        self.ui.lineEdit_2_1.setText(num(data[2]))
        self.ui.lineEdit_2_2.setText(num(data[3]))
        self.ui.lineEdit_3_1_1.setText(num(data[4]))
        self.ui.comboBox_3_1_2.setCurrentText(s(data[5]))
        self.ui.comboBox_3_1_3.setCurrentText(s(data[6]))
        self.ui.comboBox_3_1_4.setCurrentText(s(data[7]))
        self.ui.comboBox_3_2.setCurrentText(s(data[8]))
        self.ui.comboBox_3_3.setCurrentText(s(data[9]))
        self.ui.comboBox_3_4.setCurrentText(s(data[10]))
        self.ui.comboBox_3_5.setCurrentText(s(data[11]))
        self.ui.lineEdit_4_1.setText(num(data[12]))
        self.ui.lineEdit_5_1.setText(num(data[13]))
        self.ui.comboBox_6_1.setCurrentText(s(data[14]))
        self.ui.comboBox_7_1.setCurrentText(s(data[15]))
        self.ui.lineEdit_budget.setText(num(data[16]))
        self.ui.lineEdit_moria.setText(num(data[17]))
        self.ui.lineEdit_epileximos.setText(s(data[18]))


    def clear_page_moria(self):
        """Καθαρισμός lineEdit και combobox"""
        #lineEdits
        self.ui.lineEdit_1_1_moria.clear()
        self.ui.lineEdit_1_2.clear()
        self.ui.lineEdit_1_2_moria.clear()
        self.ui.lineEdit_2_1.clear()
        self.ui.lineEdit_2_1_moria.clear()
        self.ui.lineEdit_2_2.clear()
        self.ui.lineEdit_2_2_moria.clear()
        self.ui.lineEdit_3_1_1.clear()
        self.ui.lineEdit_3_1_1_moria.clear()
        self.ui.lineEdit_3_1_2_moria.clear()
        self.ui.lineEdit_3_1_3_moria.clear()
        self.ui.lineEdit_3_1_4_moria.clear()
        self.ui.lineEdit_3_2_moria.clear()
        self.ui.lineEdit_3_3_moria.clear()
        self.ui.lineEdit_3_4_moria.clear()
        self.ui.lineEdit_3_5_moria.clear()
        self.ui.lineEdit_4_1.clear()
        self.ui.lineEdit_4_1_moria.clear()
        self.ui.lineEdit_5_1.clear()
        self.ui.lineEdit_5_1_moria.clear()
        self.ui.lineEdit_6_1_moria.clear()
        self.ui.lineEdit_7_1_moria.clear()
        self.ui.lineEdit_budget.clear()
        self.ui.lineEdit_epileximos.clear()
        self.ui.lineEdit_moria.clear()

        #lineEdits setStyleSheet
        
        self.ui.lineEdit_1_1_moria.setStyleSheet("")
        self.ui.lineEdit_2_1_moria.setStyleSheet("")
        self.ui.lineEdit_2_2_moria.setStyleSheet("")
        self.ui.lineEdit_3_1_1.setStyleSheet("")
        self.ui.lineEdit_3_1_1_moria.setStyleSheet("")
        self.ui.lineEdit_3_1_2_moria.setStyleSheet("")
        self.ui.lineEdit_3_1_3_moria.setStyleSheet("")
        self.ui.lineEdit_3_1_4_moria.setStyleSheet("")
        self.ui.lineEdit_3_2_moria.setStyleSheet("")
        self.ui.lineEdit_3_3_moria.setStyleSheet("")
        self.ui.lineEdit_3_4_moria.setStyleSheet("")
        self.ui.lineEdit_3_5_moria.setStyleSheet("")
        self.ui.lineEdit_4_1.setStyleSheet("")
        self.ui.lineEdit_4_1_moria.setStyleSheet("")
        self.ui.lineEdit_5_1.setStyleSheet("")
        self.ui.lineEdit_5_1_moria.setStyleSheet("")
        self.ui.lineEdit_6_1_moria.setStyleSheet("")
        self.ui.lineEdit_7_1_moria.setStyleSheet("")
        self.ui.lineEdit_budget.setStyleSheet("")
        self.ui.lineEdit_epileximos.setStyleSheet("")
        self.ui.lineEdit_moria.setStyleSheet("")

        #combobox
        
        self.ui.comboBox_1_1.setCurrentIndex(0)
        self.ui.comboBox_3_1_2.setCurrentIndex(0)
        self.ui.comboBox_3_1_3.setCurrentIndex(0)
        self.ui.comboBox_3_1_4.setCurrentIndex(0)
        self.ui.comboBox_3_2.setCurrentIndex(0)
        self.ui.comboBox_3_3.setCurrentIndex(0)
        self.ui.comboBox_3_4.setCurrentIndex(0)
        self.ui.comboBox_3_5.setCurrentIndex(0)
        self.ui.comboBox_6_1.setCurrentIndex(0)
        self.ui.comboBox_7_1.setCurrentIndex(0)