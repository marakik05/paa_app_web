
from PySide2.QtWidgets import (QLabel, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QTableWidget, QTableWidgetItem,  QCheckBox,
                               QHeaderView, QTextEdit)
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QColor

def show_temp_message(parent, text, duration=3000, bg_color="#F44336"):
    """Εμφανίζει προσωρινό μήνυμα σε οποιοδήποτε widget για τους πίνακες"""
    msg_label = QLabel(text, parent)
    msg_label.setStyleSheet(f"""
        background-color: {bg_color};
        color: white;
        padding: 6px 12px;
        border-radius: 3px;
        font-weight: bold;
    """)
    msg_label.adjustSize()
    msg_label.move(110, 35)
    msg_label.show()
    QTimer.singleShot(duration, msg_label.hide)

def show_temp_message_main(parent, text, duration=3000, bg_color="#F44336"):
    """Εμφανίζει προσωρινό μήνυμα σε οποιοδήποτε widget για το main window"""
    msg_label = QLabel(text, parent)
    msg_label.setStyleSheet(f"""
        background-color: {bg_color};
        color: white;
        padding: 6px 12px;
        border-radius: 3px;
        font-weight: bold;
    """)
    msg_label.adjustSize()
    msg_label.move(120, 170)
    msg_label.show()
    QTimer.singleShot(duration, msg_label.hide)


class ImportConflictDialog(QDialog):
    """Dialog για επιλογή AFM που υπάρχουν ήδη στη βάση"""
    
    def __init__(self, conflicting_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Αντικατάσταση Υπαρχόντων AΦΜ")
        self.setMinimumSize(700, 500)
        self.setStyleSheet("""
                           QDialog{
                           background-color:#F2F7FA}
                           """)
        self.conflicting_data = conflicting_data  # Μόνο AΦM που υπάρχουν
        self.selected_afms = set()
        
        self.setup_ui()
        self.populate_table()
    
    def setup_ui(self):
        """Δημιουργία UI"""
        layout = QVBoxLayout(self)
        
        # Label με προειδοποίηση
        info_label = QLabel(
            " Τα παρακάτω ΑΦΜ υπάρχουν ήδη στη βάση.\n"
            "Επιλέξτε ποια θέλετε να ΑΝΤΙΚΑΤΑΣΤΑΘΟΥΝ με τα νέα δεδομένα."
            
        )
        info_label.setStyleSheet("color: #000000; font-weight: bold;")
        layout.addWidget(info_label)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Επιλογή", "ΑΦΜ", "Όνομα", "Επώνυμο"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.select_all_btn = QPushButton("Επιλογή Όλων")
        self.select_all_btn.clicked.connect(self.select_all)
        self.select_all_btn.setStyleSheet("""QPushButton{
                                        
                                        padding:8px 15px;
                                          }
                                  """)
        
        self.deselect_all_btn = QPushButton("Αποεπιλογή Όλων")
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        self.deselect_all_btn.setStyleSheet("""QPushButton{
                                        
                                        padding:8px 15px;
                                            }
                                  """)
        
        self.ok_btn = QPushButton("Αντικατάσταση Επιλεγμένων")
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setStyleSheet("""QPushButton{
                                        
                                        padding:8px 15px;
                                  }
                                  """)
        
        self.cancel_btn = QPushButton("Ακύρωση")
        self.cancel_btn.setStyleSheet("""QPushButton{
                                        
                                        padding:8px 15px;
                                       }
                                  """)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.select_all_btn)
        btn_layout.addWidget(self.deselect_all_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def populate_table(self):
        """Γέμισμα πίνακα"""
        self.table.setRowCount(len(self.conflicting_data))
        
        yellow = QColor("#F2F7FA")
        
        for row, data in enumerate(self.conflicting_data):
            afm = data['afm']
            
            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(False)  # Default: ΟΧΙ αντικατάσταση
            checkbox.stateChanged.connect(
                lambda state, a=afm: self.on_checkbox_changed(state, a)
            )
            
            checkbox_widget = QTableWidgetItem()
            self.table.setItem(row, 0, checkbox_widget)
            self.table.setCellWidget(row, 0, checkbox)
            
            # ΑΦΜ
            afm_item = QTableWidgetItem(afm)
            afm_item.setFlags(afm_item.flags() & ~Qt.ItemIsEditable)
            afm_item.setBackground(yellow)
            
            # Όνομα
            name_item = QTableWidgetItem(data.get('name', ''))
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            name_item.setBackground(yellow)
            
            # Επώνυμο
            surname_item = QTableWidgetItem(data.get('surname', ''))
            surname_item.setFlags(surname_item.flags() & ~Qt.ItemIsEditable)
            surname_item.setBackground(yellow)
            
            self.table.setItem(row, 1, afm_item)
            self.table.setItem(row, 2, name_item)
            self.table.setItem(row, 3, surname_item)
    
    def on_checkbox_changed(self, state, afm):
        """Όταν αλλάζει checkbox"""
        if state == Qt.Checked:
            self.selected_afms.add(afm)
        else:
            self.selected_afms.discard(afm)
        count = len(self.selected_afms)
        total = len(self.conflicting_data)
        self.ok_btn.setText(f"Αντικατάσταση Επιλεγμένων \n({count}/{total})")
        
    
    def select_all(self):
        """Επιλογή όλων"""
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            checkbox.setChecked(True)
    
    def deselect_all(self):
        """Αποεπιλογή όλων"""
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            checkbox.setChecked(False)
    
    def get_selected_afms(self):
        """Επιστρέφει τα επιλεγμένα AFM"""
        return self.selected_afms



class MissingCategoriesDialog(QDialog):
    def __init__(self, message, details, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Προειδοποίηση")
        self.resize(700, 500)
        self.setStyleSheet("""
                           QDialog{
                           background-color:#F2F7FA}
                           """)

        layout = QVBoxLayout(self)

        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)

        text_box = QTextEdit()
        text_box.setReadOnly(True)
        text_box.setPlainText(details)
        layout.addWidget(text_box)

        ok_btn = QPushButton("Εντάξει")
        ok_btn.clicked.connect(self.accept)
        
        ok_btn.setFixedWidth(120)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        
        
        layout.addLayout(btn_layout)