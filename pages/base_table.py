from PySide2.QtWidgets import QWidget, QHeaderView, QMessageBox, QAbstractItemView
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QStandardItemModel, QStandardItem, QColor, QFontMetrics, QFont
from delegates.delegates_dlt import DeleteButtonDelegate, SearchableComboDelegate, SearchableDynamicComboDelegate, NoWheelComboDelegate, Double2DecimalDelegate, IntOnlyDelegate 
from utils.excel_loader import load_excel_data, contains_norm_keyword, resource_path, in_norm_set, LOCK_AMPELI_NORM, LOCK_TREES_NORM,FMZ_ZWIKI_NORM, FMZ_MELISSES_NORM, PARAGWGIKA_NORM, PARAGWGIKA_CAT_NORM, AEGEAN_PERIFERIES, DEFAULT
from widgets.clearable_tableview import  ClearableTableView
from utils.message import show_temp_message



class baseTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setup_ui(self):

        self.model = QStandardItemModel(self)
        old_view = self.ui.tableView
        parent = old_view.parent()

        self.ui.tableView = ClearableTableView(parent)
        self.ui.tableView.setModel(self.model)

        layout = parent.layout()
        layout.replaceWidget(old_view, self.ui.tableView)
        old_view.deleteLater()

        # Ορισμός τίτλων στηλών
        
        self.model.setHorizontalHeaderLabels([
                                              "Κατηγορία ΟΣΔΕ", 
                                              "Περιγραφή \nΕίδους/Ποικιλίας/Ζώων", 
                                              "Τυπική \nΑπόδοση", 
                                              "Έκταση/\nΑριθμός ζώων",
                                              "Βιολογικά \nΟλοκλ/μένη \nΠΟΠ/ΠΓΕ", 
                                              "Δένδρα\n>=4 ετών", 
                                              "Δένδρα\n<4 ετών",
                                              "Αμπέλι\n>3 ετών", 
                                              "ΤΑ ανά \nεπιλογή", 
                                              "Διαγραφή",
                                              "Σύνολο ΤΑ",                                              
                                              "ΤΑ \nΠαραγωγικών",
                                              "ΤΑ Φυτικής",
                                              "ΤΑ Ζωικής",
                                              "ΤΑ Μελίσσια \nMεταξοσκώληκες",                                              
                                                ])
       
        

        # Interactive mode (επιτρέπει χειροκίνητο resize)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)

       

        # Ορισμός αρχικού πλάτους στηλών 
        self.ui.tableView.setColumnWidth(0, 250)  
        self.ui.tableView.setColumnWidth(1, 250) 
        self.ui.tableView.setColumnWidth(3, 125) 
        self.ui.tableView.setColumnWidth(4, 110) 
        self.ui.tableView.setColumnWidth(5, 125)
        self.ui.tableView.setColumnWidth(6, 115)
        self.ui.tableView.setColumnWidth(7, 110)
        self.ui.tableView.setColumnWidth(8, 120)
        self.ui.tableView.setColumnWidth(10, 110)
        self.ui.tableView.setColumnWidth(14, 155)    

        
        
        #Σύδεση με delegates για την αφαίρεση κουμπιού
        self.delete_delegate = DeleteButtonDelegate(self.ui.tableView)
        self.delete_delegate.deleteClicked.connect(self.delete_row)
        self.ui.tableView.setItemDelegateForColumn(9, self.delete_delegate)
    

        #load αρχείου excel ta.xlsx
        
        excel_path = resource_path("data/ta.xlsx")
        self.mapping, self.value_mapping = load_excel_data(excel_path)

        #1η στήλη "Καλλιέργειες" combobox
        self.crop_delegate = SearchableComboDelegate(list(self.mapping.keys()), self.ui.tableView)
        self.ui.tableView.setItemDelegateForColumn(0, self.crop_delegate)

        #2η στήλη "Ποικιλία" combobox
        def second_column_choices(index):
                
                row = index.row()
                item = self.model.item(row, 0)

                if not item:
                    return []
                return self.mapping.get(item.text(), [])
                               
        
        self.season_delegate = SearchableDynamicComboDelegate(second_column_choices, self.ui.tableView)
        self.ui.tableView.setItemDelegateForColumn(1, self.season_delegate)
        
        #signals
        self.model.itemChanged.connect(self.on_item_changed)
        self._updating = False

        #Δημιουργία combobox στήλης συστημάτων Ποιότητας
        self.organic = NoWheelComboDelegate(["--Επιλέξτε", "Συμβατικά", "Βιολογικά", "Ολοκληρωμένη", "ΠΟΠ/ΠΓΕ"], self.ui.tableView)
        
        self.ui.tableView.setItemDelegateForColumn(4, self.organic)

        #Δημιουργία combobox στήλης Αμπελιού
        self.ampeli = NoWheelComboDelegate(["--Επιλέξτε", "Ναι", "Όχι"], self.ui.tableView)
        
        self.ui.tableView.setItemDelegateForColumn(7, self.ampeli)


        #Περιορισμός έκτασης ώστε να επιτρέπονται μόνο αριθμοί με 2 δεκαδικά
        self.hectars = Double2DecimalDelegate(self.ui.tableView)
        self.ui.tableView.setItemDelegateForColumn(3, self.hectars)
        

        #Περιορισμός δένδρων ώστε να επιτρέπονται μόνο ακέραιοι αριθμοί
        self.trees_older = IntOnlyDelegate(self.ui.tableView)
        self.ui.tableView.setItemDelegateForColumn(5, self.trees_older)
        

        self.trees = IntOnlyDelegate(self.ui.tableView)
        self.ui.tableView.setItemDelegateForColumn(6, self.trees)

        #ρυθμίσεις windows
        self._setup_table_windows_compatibility()

    #signals για τη συνολική τυπική απόδοση και τα βιολογικά
    totalChanged = Signal(str)

    biologicChanged = Signal(str)

   
    #def επανυπολογισμού 3ης στήλης
    def recalculate(self, row):
            """Επανυπολογισμός με την αλλαγή της Περιφέρειας"""
        
            crop_item = self.model.item(row, 0)
            season_item = self.model.item(row, 1)
            if row >= self.model.rowCount():
                return
            # αν λείπουν επιλογές → καθάρισε 3η στήλη
            if (
                not crop_item or not crop_item.text().strip()
                or not season_item or not season_item.text().strip()
                or not getattr(self, "selected_periferia", None)
                or self.selected_periferia == "--Επιλέξτε"
            ):
                item = QStandardItem("")
                item.setEditable(False)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QColor("#E3F2FD"))
                self.model.setItem(row, 2, item)
                return

            crop = crop_item.text().strip()
            season = season_item.text().strip()
            values = self.value_mapping.get((crop, season))
            if not values:
                item = QStandardItem("")
                item.setEditable(False)
                item.setBackground(QColor("#E3F2FD"))
                item.setTextAlignment(Qt.AlignCenter)
                self.model.setItem(row, 2, item)
                return
            

            if self.selected_periferia in AEGEAN_PERIFERIES:
                value = values.get("aegean")
               
            else:
                value = values.get("default")
               

            item = QStandardItem("" if value is None else str(value))
            item.setEditable(False)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("#E3F2FD"))
            self.model.setItem(row, 2, item)
        
    
     
    def delete_row(self, p_index):
        """Διαγραφή σειράς πίνακα"""
        if not p_index.isValid():
            return
        self.model.removeRow(p_index.row())
        self.total_col_ta_10()
        self.total_fzm()
        
        self.paragwgikwn()
        self.biologicChanged.emit(self.biologic())


    def on_item_changed(self, item):
       
        """def για τις αλλαγές στις στήλες 1-3"""
        if not item:
            return
        
        if self._updating:
            return
        
        self._updating = True
        try:
        
            row = item.row()
            col = item.column()
                
            crop_item = self.model.item(row, 0)
            season_item=self.model.item(row, 1)
           
            # Αν λείπει επιλογή → καθάρισε 2η & 3η στήλη
    
            if not crop_item or not crop_item.text().strip():
             
                
                self.model.blockSignals(True)
           
                self.model.setItem(row, 1, QStandardItem(""))
                item = QStandardItem("")
                item.setEditable(False)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QColor("#E3F2FD"))
                self.model.setItem(row, 2, item)
              
                self.model.blockSignals(False)
                return
            

            if col == 0:
                crop = crop_item.text().strip()
                choices = self.mapping.get(crop, [])
                index = self.model.index(row, 1)

                self.model.blockSignals(True)
                # ΚΛΕΙΣΕ τον editor (κρατάει παλιές επιλογές)
                self.ui.tableView.closePersistentEditor(index)

                # καθάρισε 2η & 3η στήλη
                self.model.setItem(row, 1, QStandardItem(""))
                self.model.setItem(row, 2, QStandardItem(""))
                
                self.model.blockSignals(False)

                self.lock_ampeli()
                self.lock_trees(5)
                self.lock_trees(6)
        

        # 🔹 αν υπάρχει τουλάχιστον μία επιλογή στη 2η στήλη
                if choices:
                    first_choice = "--Επιλέξτε"

                    self.model.blockSignals(True)
                    self.model.setItem(row, 1, QStandardItem(first_choice))
                    self.model.blockSignals(False)

               
                # αν άλλαξε η 1η ή 2η στήλη → επανυπολογισμός
                if col in (0, 1):
                    first_choice = "--Επιλέξτε"
                    self.model.blockSignals(True)
                    self.model.setItem(row, 1, QStandardItem(first_choice))
                    self.model.blockSignals(False)
                    self.ui.tableView.openPersistentEditor(index)
                    self.recalculate(row)
         
            
            if col == 1:
                #  αν η ποικιλία ΔΕΝ είναι έγκυρη επιλογή
                if not self.is_valid_season(row):
                    self.model.blockSignals(True)
                    self.model.setItem(row, 2, QStandardItem(""))
                    self.model.blockSignals(False)
           
                #  μόνο αν είναι έγκυρη → υπολογισμοί
                self.recalculate(row)
         
            if col in (0,1,2,3,4,5,6,7):
                self.recalculate(row)
                self.update_col_ta_8(row)
                self.total_col_ta_10()
                self.total_fzm()
                self.paragwgikwn()
                self.biologicChanged.emit(self.biologic())
                if col in (0, 1):
                    self._smart_resize_column_for_row(col, row)
        
        finally:
            self._updating=False
    

    def add_row(self):
        """Προσθήκη σειράς στον πίνακα"""
        row_items = []

        first_crop = next(iter(self.mapping)) 

        for col in range(15):

            # 1η στήλη → default επιλογή
            if col == 0:
                item = QStandardItem(first_crop)
 
            else:
                item = QStandardItem("")

        
            if col in (2, 8):
                item.setEditable(False)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QColor("#E3F2FD"))

            if col in (10, 11, 12, 13, 14):
                item.setEditable(False)
                item.setTextAlignment(Qt.AlignCenter)

          
            if col in (3,5,6):
                item.setTextAlignment(Qt.AlignCenter)

            row_items.append(item)

        self.model.appendRow(row_items)
        self.lock_ampeli()
        self.lock_trees(5)
        self.lock_trees(6)

        row = self.model.rowCount() - 1
    
         # 🔹 default επιλογή 2ης στήλης
        choices = self.mapping.get(first_crop, [])
        if choices:
            self.model.setItem(row, 1, QStandardItem(choices[0]))

        # editors (col 9 = paint-based delete button, no persistent editor needed)
        self.ui.tableView.openPersistentEditor(self.model.index(row, 0))
        self.ui.tableView.openPersistentEditor(self.model.index(row, 1))
        self.ui.tableView.openPersistentEditor(self.model.index(row, 4))
    
        if not self.selected_periferia or self.selected_periferia == DEFAULT:
            show_temp_message(self,"Για τον υπολογισμό της τυπικής απόδοσης επιλέξτε Περιφέρεια.")
        else:
            self.recalculate(row)


    
    def _smart_resize_column_for_row(self, col, row):
        """def για autorisize στηλων 0 και 1"""
    
        # Πάρε το τρέχον πλάτος της στήλης
        current_width = self.ui.tableView.columnWidth(col)
        
        # Πάρε το επιλεγμένο κείμενο
        item = self.model.item(row, col)  # τελευταία γραμμή που άλλαξε
        if not item:
            return
        
        text = item.text()
        if not text:
            return
        
        # Υπολογισμός απαιτούμενου πλάτους για το συγκεκριμένο κείμενο
       
        font = self.ui.tableView.font()
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(text) + 60  # +60 για padding + dropdown arrow
        
        #  Μεγάλωσε ΜΟΝΟ αν το κείμενο δεν χωράει
        if text_width > current_width:
            self.ui.tableView.setColumnWidth(col, text_width)

    def get_cell_strip(self, row, col):
        """βοηθητική def για text.strip"""
        item = self.model.item(row, col)
        if not item:
            return ""
        return item.text().strip()
    

 
    def get_cell_float(self, row, col):
        """βοηθητική def για float"""
        try:
            text = self.get_cell_strip(row, col)

            if not text:
                return None

            return float(text.replace(",", "."))
        except ValueError:
                QMessageBox.warning(
                self,
                "Μη έγκυρη τιμή",
                f"Η τιμή στη γραμμή {row + 1}, στήλη {col + 1} δεν είναι έγκυρος αριθμός.\n\n"
                f"Παρακαλώ εισάγετε μόνο αριθμούς."
        )
                return None
            
        
    
    def get_cell_int(self, row, col):
        """βοηθητική def για int"""
        try:
            text = self.get_cell_strip(row, col)

            if not text:
                return None

            
            return int(text)
        except ValueError:
            QMessageBox.warning(
            self,
            "Μη έγκυρη τιμή",
            f"Η τιμή στη γραμμή {row + 1} πρέπει να είναι ακέραιος αριθμός."
        )
            return None
         
       
   
    def typiki_apodosi(self,row):
        """Υπολογισμός ΤΑ ανά αγροτεμάχιο"""  
        try:      
            col_2=self.get_cell_float(row,2)
            col_3=self.get_cell_float(row,3)
            col_5=self.get_cell_int(row,5)
            col_6=self.get_cell_int(row,6)
            col_7=self.get_cell_strip(row,7)
            col_0=self.get_cell_strip(row,0)
        
            if col_2 is None or col_3 is None  :
                return None
        
            if  in_norm_set(col_0, LOCK_AMPELI_NORM):
                if col_7 =="Ναι":
                    return col_2*col_3
            
                if col_7 == "Όχι":
                    return (col_2 / 2) * col_3
                
                if col_7 in ("", "--Επιλέξτε"):
                    
                        return None 
            else:
            
                if (col_5 is None or  col_5==0) and (col_6 is None or col_6==0):
                    return col_2*col_3
                if col_5 is None or col_5==0:
                    return (col_2/2)*col_3
                if col_6 is None or col_6==0 :
                    return col_2*col_3
                
                total=col_5+col_6
                result=(col_2*(col_3*(col_5/total))+(col_2/2)*(col_3*(col_6/total)))
                return result
            
    
        except Exception as e:
            QMessageBox.critical(
                self,
                "Σφάλμα Υπολογισμού",
                f"Σφάλμα κατά τον υπολογισμό της Τυπικής Απόδοσης:\n{str(e)}"
            )
            return None
        
    
    def ta_paragwgikwn(self,row):
        """Υπολογισμός ΤΑ παραγωγικών δένδρων"""
        try:
        
            col_2=self.get_cell_float(row,2)
            col_3=self.get_cell_float(row,3)
            col_5=self.get_cell_int(row,5)
            col_6=self.get_cell_int(row,6)
            col_7=self.get_cell_strip(row,7)
            col_0=self.get_cell_strip(row,0)
        
            # Αν λείπουν βασικές τιμές → δεν υπολογίζουμε
        
            if col_2 is None or col_3 is None:
                return None
            
            if  in_norm_set(col_0, LOCK_AMPELI_NORM):
                if col_7 == "Ναι":
                    return col_2 * col_3
                if col_7 == "Όχι":
                    return None
                
                if col_7 in ("", "--Επιλέξτε"):
                    
                        return None 
            else:        
                
                if (col_5 is None or  col_5==0) and (col_6 is None or col_6==0):
                    return col_2*col_3
                if col_5 is None or col_5==0:
                    return None
                if col_6 is None or col_6==0 :
                    return col_2*col_3
                    
                total=col_5+col_6
                result=(col_2*(col_3*(col_5/total)))
                return result
        except Exception as e:
            QMessageBox.critical(
                self,
                "Σφάλμα Υπολογισμού",
                f"Σφάλμα κατά τον υπολογισμό της Τυπικής Απόδοσης Παραγωγικών:\n{str(e)}"
            )
            return None
        
            
    
    def update_col_ta_8(self, row):
            """def ενημέρωσης στήλης 8"""
        
            result= self.typiki_apodosi(row)
               
            self.model.blockSignals(True)

            item = QStandardItem("" if result is None else f"{result:.2f}")
            item.setEditable(False)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("#E3F2FD"))

            self.model.setItem(row, 8, item)  

            self.model.blockSignals(False)

   
    def total_col_ta_10(self):
            """def υπολογισμού και ενημέρωσης στήλης 10"""
        
            col_8_index = 8
            col_10_index = 10

            if self.model.rowCount() == 0:
                self.totalChanged.emit("")
                return

            total = 0.0
            has_value = False  #  για να ξέρουμε αν υπάρχει έστω 1 αριθμός

            for row in range(self.model.rowCount()):
                item = self.model.item(row, col_8_index)
                if item is not None:
                    try:
                        value = float(item.text())
                        total += value
                        has_value = True
                    except ValueError:
                        pass

            # δημιούργησε κελί στη στήλη 10 αν δεν υπάρχει
            target_item = self.model.item(0, col_10_index)
            if target_item is None:
                return
                
            #  αν δεν υπάρχει καμία τιμή → άδειο κελί
            if not has_value:
                target_item.setText("")
                target_item.setBackground(QColor("#E3F2FD"))
                self.totalChanged.emit("")
                
            else:
                text = f"{total:.2f}"
                target_item.setText(text)
                target_item.setBackground(QColor("#E3F2FD"))
                bold_font = QFont()
                bold_font.setBold(True)
                target_item.setFont(bold_font)
                self.totalChanged.emit(text)
                self.biologicChanged.emit(self.biologic())

    
    def _set_total_cell(self, row, col, total, has_value):
        """βοηθητική def για τον υπολογισμό της ΤΑ φυτικής, ζωικής, μεικτής"""
        item = self.model.item(row, col)
        if item is None:
            item = QStandardItem()
            item.setEditable(False)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("#E3F2FD"))
            self.model.setItem(row, col, item)

        item.setText(f"{total:.2f}" if has_value else "")
        item.setBackground(QColor("#E3F2FD"))

    
    def total_fzm(self):
        """def για τον υπολογισμό της ΤΑ φυτικής, ζωικής, μεικτής"""
        col_8_index = 8
        col_12_index = 12
        col_13_index = 13
        col_14_index = 14

        if self.model.rowCount() == 0:
            return

        total_12 =0.0
        total_13 = 0.0
        total_14 = 0.0
  
        has_value_12 = False
        has_value_13 = False
        has_value_14 = False

        for row in range(self.model.rowCount()):
            crop_item = self.model.item(row, 0)
            value_item = self.model.item(row, col_8_index)

            if not crop_item or not value_item:
                continue

            try:
                value = float(value_item.text())
            except ValueError:
                continue

            crop = crop_item.text().strip()
            
 
            if in_norm_set(crop, FMZ_ZWIKI_NORM):
                              
                    total_13 += value
                    has_value_13 = True
               
   
            elif in_norm_set(crop, FMZ_MELISSES_NORM):
                
                    total_14 += value
                    has_value_14 = True
                         
            else:
                
                    total_12 += value
                    has_value_12 = True

        self._set_total_cell(0, col_14_index, total_14, has_value_14)
        self._set_total_cell(0, col_12_index, total_12, has_value_12)
        self._set_total_cell(0, col_13_index, total_13, has_value_13)

    
                    
    def biologic(self):
        """def για τον υπολογισμό ποσοστού συνολικής ΤΑ βιολογικών/συστημάτων ποιότητας"""
        col_8_index=8
        col_4_index=4
        #EXCLUDED = {"", "--Επιλέξτε", "Συμβατικά"}
        INCLUDED= {"Βιολογικά", "Ολοκληρωμένη", "ΠΟΠ/ΠΓΕ"}
                
        
        if self.model.rowCount() == 0:
                
                return ""

        total_bio = 0.0
        has_value = False 

        for row in range(self.model.rowCount()):
            choice_item = self.model.item(row, col_4_index)
            choice = choice_item.text().strip() if choice_item else ""
            if choice not in INCLUDED:
                continue
            item = self.model.item(row, col_8_index)
            
            if item is None :
                continue

            try:
                total_bio += float(item.text())
                
                has_value = True
            except ValueError:
                pass

        if not has_value:
            # αν υπάρχουν γραμμές αλλά όλες είναι Συμβατικά/--Επιλέξτε → 0%
            total_item = self.model.item(0, 10)
            if total_item is None:
                return ""
            try:
                float(total_item.text())  # έλεγχος ότι υπάρχει συνολική ΤΑ
                return "0.00%"
            except ValueError:
                return ""
        
        
        # Συνολική ΤΑ από στήλη 10
        total_item = self.model.item(0, 10)
        if total_item is None:
            return ""
        try:
            total_ta = float(total_item.text())
        except ValueError:
            return ""

        if total_ta == 0:
            return ""

        pct = (total_bio / total_ta) * 100
        return f'{pct:.2f}%'
            

      
    def lock_ampeli(self):
        """def για κλείδωμα αμπελιού>3 ετών"""
        
        for row in range(self.model.rowCount()):
            crop_item = self.model.item(row, 0)
            
            
            ampeli = self.model.item(row, 7)

            if not crop_item or not ampeli:
                continue
            crop = crop_item.text().strip()
           
            
            index = self.model.index(row, 7)   
            if not in_norm_set(crop, LOCK_AMPELI_NORM):    
                ampeli.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                ampeli.setText("")
                ampeli.setBackground(QColor("#E3F2FD")) 
                self.ui.tableView.closePersistentEditor(index)           
            else:

                ampeli.setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
            )
                ampeli.setBackground(QColor("#E3F2FD"))
                self.ui.tableView.openPersistentEditor(index)

       
    def lock_trees(self,col):
        """def για κλείδωμα δένδρων>4 ετών και <4ετών"""
        
        for row in range(self.model.rowCount()):
            crop_item = self.model.item(row, 0)
            
            trees = self.model.item(row, col)

            if not crop_item or not trees:
                continue
            crop = crop_item.text().strip()
          
            if  in_norm_set(crop, LOCK_TREES_NORM):    
                trees.setEditable(False)
                trees.setText("")
                trees.setBackground(QColor("#E3F2FD"))
                  
            else:

                trees.setEditable(True)
                trees.setBackground(QColor("white"))


    def paragwgikwn(self):
        """def για τον υπολογισμό ΤΑ παραγωγικών"""
        
        col_11_index = 11

        if self.model.rowCount() == 0:
            return

        total = 0.0
        has_value = False

        for row in range(self.model.rowCount()):
            crop_item = self.model.item(row, 0)
            season_item = self.model.item(row, 1)

            if not crop_item or not season_item:
                continue

            crop = crop_item.text().strip()
            season = season_item.text().strip()
   
            if in_norm_set(crop, PARAGWGIKA_CAT_NORM):
                if not contains_norm_keyword(season, PARAGWGIKA_NORM):
                    continue

                value_item = self.model.item(row, 8)
                if not value_item:
                    continue

                try:
                    value = float(value_item.text())
                except ValueError:
                    continue

                total += value
                has_value = True
                continue

            
            value = self.ta_paragwgikwn(row)
            if value is None:
                continue

            total += round(value,2)
            has_value = True

        self._set_total_cell(0, col_11_index, total, has_value)


    def is_valid_season(self, row):
        """βοηθητική συνάρτηση για την def on_item_changed"""
        season_item = self.model.item(row, 1)
        crop_item = self.model.item(row, 0)

        if not season_item or not crop_item:
            return False

        season = season_item.text().strip()
        crop = crop_item.text().strip()

        if not season or not crop:
            return False

        valid_choices = self.mapping.get(crop, [])
        return season in valid_choices
    
 
    def get_all_rows_data(self):
        """Συλλογή των δεδομένων των πινάκων"""
    
        all_data = []
      
        for row in range(self.model.rowCount()):
            row_data = []
            for col in range(15):  # 15 στήλες (0-14)
                item = self.model.item(row, col)
                row_data.append(item.text() if item else "")
            all_data.append(row_data)
        
        return all_data


    def load_rows_from_data(self, data):        
        """Φόρτωση δεδομένων στους πίνακες"""
         # Block signals κατά τη φόρτωση
        self.model.blockSignals(True)      
        
        self.model.removeRows(0, self.model.rowCount())
       
        # Αν δεν υπάρχουν δεδομένα → ΤΕΛΟΣ
        if not data:
            self.model.blockSignals(False)
            #reset του view του πίνακα
            self.ui.tableView.setModel(None)
            self.ui.tableView.setModel(self.model)
            #επαναφορά ρυθμίσεων πίνακα
            self._restore_table_settings()
            
            # Καθαρισμός συνόλων
            self.total_col_ta_10()
            self.total_fzm()
            self.paragwgikwn()
            
            return  
            
        # Προσθήκη νέων γραμμών
        for row_data in data:
            row_items = []

            for col, value in enumerate(row_data):
                if value is None:

                    value = ""
                else:
                    if col == 3:  # Έκταση (2 δεκαδικά)
                        try:
                            value = f"{float(value):.2f}"
                        except (ValueError, TypeError):
                            value = ""

                    elif col in (5, 6):  # Δένδρα (ακέραιοι)
                        try:
                            value = str(int(float(value)))
                        except (ValueError, TypeError):
                            value = ""

                    else:
                        # Υπόλοιπες στήλες
                        value = str(value)

                # Κενή Περιγραφή με συμπληρωμένη Κατηγορία ΟΣΔΕ → "--Επιλέξτε"
                # ώστε το persistent combobox να μην επιλέγει σιωπηλά την 1η ποικιλία.
                if col == 1 and not value:
                    cat = row_data[0]
                    if cat is not None and str(cat).strip():
                        value = "--Επιλέξτε"

                item = QStandardItem(value)
                
                
                if col in (2, 8):
                    item.setEditable(False)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor("#E3F2FD"))
                
                if col in (10, 11, 12, 13, 14):
                    item.setEditable(False)
                    item.setTextAlignment(Qt.AlignCenter)
                
                if col in (3, 5, 6):
                    item.setTextAlignment(Qt.AlignCenter)
                
                row_items.append(item)
            
            self.model.appendRow(row_items)
        #  Unblock signals ΠΡΙΝ τα persistent editors
        self.model.blockSignals(False)
     
        #  Ενεργοποίηση persistent editors (col 9 = paint-based delete button)
        for row in range(self.model.rowCount()):
            self.ui.tableView.openPersistentEditor(self.model.index(row, 0))
            self.ui.tableView.openPersistentEditor(self.model.index(row, 1))
            self.ui.tableView.openPersistentEditor(self.model.index(row, 4))
        
            #  : Επανυπολογισμός ΟΛΩΝ των γραμμών
        if self.selected_periferia and self.selected_periferia != "--Επιλέξτε":
            for row in range(self.model.rowCount()):
                self.recalculate(row)
                self.update_col_ta_8(row)

        # refresh resize
        self._resize_columns_after_load()
        

        #  Refresh locks και calculations
        self.lock_ampeli()
        self.lock_trees(5)
        self.lock_trees(6)
        
        self.total_col_ta_10()
        self.total_fzm()
        self.paragwgikwn()
        
        

    
    def _restore_table_settings(self):
        """Επαναφορά ΟΛΩΝ των ρυθμίσεων του πίνακα μετά το reset"""
        
        #  1. Header resize modes
        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)

        #self.ui.tableView.setShowGrid(True) 
        
        #  2. Πλάτη στηλών
        self.ui.tableView.setColumnWidth(0, 250)  
        self.ui.tableView.setColumnWidth(1, 250) 
        self.ui.tableView.setColumnWidth(3, 125) 
        self.ui.tableView.setColumnWidth(4, 110) 
        self.ui.tableView.setColumnWidth(5, 125)
        self.ui.tableView.setColumnWidth(6, 115)
        self.ui.tableView.setColumnWidth(7, 110)
        self.ui.tableView.setColumnWidth(8, 120)
        self.ui.tableView.setColumnWidth(10, 110)
        self.ui.tableView.setColumnWidth(14, 155) 
        
        #  3. Delete button delegate
        self.ui.tableView.setItemDelegateForColumn(9, self.delete_delegate)
        
        #  4. Crop combobox (στήλη 0)
        self.ui.tableView.setItemDelegateForColumn(0, self.crop_delegate)
        
        #  5. Variety combobox (στήλη 1)
        self.ui.tableView.setItemDelegateForColumn(1, self.season_delegate)
        
        #  6. Quality systems combobox (στήλη 4)
        self.ui.tableView.setItemDelegateForColumn(4, self.organic)
        
        #  7. Vineyard combobox (στήλη 7)
        self.ui.tableView.setItemDelegateForColumn(7, self.ampeli)
        
        #  8. Area numeric delegate (στήλη 3)
        self.ui.tableView.setItemDelegateForColumn(3, self.hectars)
        
        #  9. Trees delegates (στήλες 5, 6)
        self.ui.tableView.setItemDelegateForColumn(5, self.trees_older)
        self.ui.tableView.setItemDelegateForColumn(6, self.trees)

    
    def _resize_columns_after_load(self):
        """Auto-resize στηλών 0 και 1 μετά τη φόρτωση δεδομένων"""
       
        for row in range(self.model.rowCount()):
           self._smart_resize_column_for_row(0,row)
           self._smart_resize_column_for_row(1,row)

    
    def _setup_table_windows_compatibility(self):
        """Ρυθμίσεις για Windows 7+ compatibility"""

        #  Ενεργοποίηση gridlines (για να φαίνονται)
        self.ui.tableView.setShowGrid(True)

        # Mouse tracking για hover στο painted delete button (col 9). Το
        # ClearableTableView.viewportEvent φιλτράρει τα hover events ώστε να
        # μην φτάνουν στις στήλες 0/1/4 (persistent combos) που θα έχαναν focus.
        self.ui.tableView.setMouseTracking(True)

        
        # Vertical header setup
        v_header = self.ui.tableView.verticalHeader()
        v_header.setVisible(True)  # Αν θες να φαίνονται οι αριθμοί
        v_header.setStretchLastSection(False)
        v_header.setDefaultSectionSize(35)
        
        # Smooth scrolling
        self.ui.tableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.ui.tableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

   



                  
               
                



                
        
        
        

        

           

   
        
        
        
       


        

        
       

