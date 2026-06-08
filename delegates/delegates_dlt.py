from PySide2.QtWidgets import QStyledItemDelegate, QPushButton, QComboBox, QCompleter, QLineEdit, QTableView, QApplication, QStyle
from PySide2.QtGui import QRegExpValidator, QValidator, QPainter, QPen, QBrush, QColor, QFont
from PySide2.QtCore import QEvent, QTimer, Signal, Qt, QModelIndex, QPersistentModelIndex, QRegExp, QSize
from utils.excel_loader import norm



class DeleteButtonDelegate(QStyledItemDelegate):
    """Κουμπί διαγραφής σειρών πίνακα — paint-based (χωρίς widget per cell)."""
    deleteClicked = Signal(QModelIndex)

    _PAD = 2
    _BORDER = QColor("#BBDEFB")
    _HOVER_BG = QColor("#BBDEFB")
    _BG = QColor("white")
    _FG = QColor("red")
    # Greyed-out version όταν ο view / viewport είναι disabled
    _DISABLED_BORDER = QColor("#BBDEFB")
    _DISABLED_BG = QColor("#E3F2FD")
    _DISABLED_FG = QColor("#A0A0A0")

    def _button_rect(self, cell_rect):
        return cell_rect.adjusted(self._PAD, self._PAD, -self._PAD, -self._PAD)

    def paint(self, painter, option, index):
        rect = self._button_rect(option.rect)
        enabled = bool(option.state & QStyle.State_Enabled)
        is_hover = enabled and bool(option.state & QStyle.State_MouseOver)

        if enabled:
            border, bg, fg = self._BORDER, (self._HOVER_BG if is_hover else self._BG), self._FG
        else:
            border, bg, fg = self._DISABLED_BORDER, self._DISABLED_BG, self._DISABLED_FG

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(QPen(border, 1))
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(rect, 3, 3)

        font = QFont("Segoe UI Symbol", 16)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(fg)
        painter.drawText(rect, Qt.AlignCenter, "×")
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if not (option.state & QStyle.State_Enabled):
            return False
        if event.type() == QEvent.MouseButtonRelease:
            if self._button_rect(option.rect).contains(event.pos()):
                self.deleteClicked.emit(index)
                return True
        return False

    def sizeHint(self, option, index):
        return QSize(40, 35)


class EditButtonDelegate(QStyledItemDelegate):
    """Κουμπί επεξεργασίας πίνακα αρχικής σελίδας — paint-based."""
    editClicked = Signal(QModelIndex)

    _PAD = 2
    _BORDER = QColor("#BBDEFB")
    _HOVER_BG = QColor("#BBDEFB")
    _BG = QColor("white")
    _FG = QColor("green")
    _DISABLED_BORDER = QColor("#BBDEFB")
    _DISABLED_BG = QColor("#E3F2FD")
    _DISABLED_FG = QColor("#A0A0A0")

    def _button_rect(self, cell_rect):
        return cell_rect.adjusted(self._PAD, self._PAD, -self._PAD, -self._PAD)

    def paint(self, painter, option, index):
        rect = self._button_rect(option.rect)
        enabled = bool(option.state & QStyle.State_Enabled)
        is_hover = enabled and bool(option.state & QStyle.State_MouseOver)

        if enabled:
            border, bg, fg = self._BORDER, (self._HOVER_BG if is_hover else self._BG), self._FG
        else:
            border, bg, fg = self._DISABLED_BORDER, self._DISABLED_BG, self._DISABLED_FG

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(QPen(border, 1))
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(rect, 3, 3)

        font = QFont("Segoe UI Symbol", 12)
        painter.setFont(font)
        painter.setPen(fg)
        painter.drawText(rect, Qt.AlignCenter, "✎")
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if not (option.state & QStyle.State_Enabled):
            return False
        if event.type() == QEvent.MouseButtonRelease:
            if self._button_rect(option.rect).contains(event.pos()):
                self.editClicked.emit(index)
                return True
        return False

    def sizeHint(self, option, index):
        return QSize(40, 35)


class NoWheelComboBox(QComboBox):
    """Κλάση για αγνόηση του scroll από το combobox """
    def wheelEvent(self, event):
        
        event.ignore()

      #  Επιτρέπει navigation με βελάκια όταν το dropdown είναι κλειστό
    def keyPressEvent(self, event):
        key = event.key()
        
        # Αν το dropdown είναι κλειστό και πατάς Left/Right → πέρνα το event στον πίνακα
        if not self.view().isVisible():
            if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                # Βρες το QTableView
                parent = self.parent()
                while parent and not isinstance(parent, QTableView):
                    parent = parent.parent()
                
                if parent:
                    # Πέρασε το event στον πίνακα
                    QApplication.sendEvent(parent, event)
                    return
        
        # Αλλιώς, φυσιολογική συμπεριφορά
        super().keyPressEvent(event)

class ListValidator(QValidator):
    """Validator για την 1η και 2η στήλη του πίνακα"""
    def __init__(self, valid_items, parent=None):
        super().__init__(parent)
        if "--Επιλέξτε" not in valid_items:
            valid_items = ["--Επιλέξτε"] + valid_items
        self.valid_items = [norm(item) for item in valid_items]

        
       
    
    def validate(self, input_text, pos):
        """
        Επιστρέφει:
        - Acceptable: Η τιμή υπάρχει ακριβώς στη λίστα
        - Intermediate: Η τιμή είναι μερικό match (επιτρέπει πληκτρολόγηση)
        - Invalid: Η τιμή ΔΕΝ μπορεί να γίνει ποτέ valid
        """
        if not input_text or input_text.strip() == "":
            
            
            return QValidator.Acceptable, input_text, pos
        
        input_norm = norm(input_text)
        
        # Exact match
        if input_norm in self.valid_items:
            if input_text.endswith(" "):
                #self.set_editor_style(self.parent(), "invalid")
                return QValidator.Invalid, input_text, pos
           
            else:
                return QValidator.Acceptable, input_text, pos
        
        # Partial match
        for item in self.valid_items:
            if item.startswith(input_norm): 
                
                
                return QValidator.Intermediate, input_text, pos
            
         # Contains match - έλεγχος αν το input ΠΕΡΙΕΧΕΤΑΙ σε κάποιο item
        # (για reverse search - αν σβήνεις από τη μέση)
        for item in self.valid_items:
            if input_norm in item:
                
                return QValidator.Intermediate, input_text, pos
        
        # Invalid
        #  Invalid - Κόκκινο background
        #self.set_editor_style(self.parent(), "invalid")
        return QValidator.Invalid, input_text, pos

    
    # def set_editor_style(self, editor, state):
    #     """Visual feedback"""
        
    #     if state == "invalid":
    #         editor.setStyleSheet("background-color: #FFEBEE;")  # Ανοιχτό κόκκινο
    #     else:
    #         editor.setStyleSheet("background-color: white;") 


class SearchableComboDelegate(QStyledItemDelegate): 
    """searchable combobox στην στήλη 1 του πίνακα"""
    def __init__(self, items, parent=None): 
        super().__init__(parent) 
        self.items = items 
    
    def createEditor(self, parent, option, index):
        combo = NoWheelComboBox(parent)
        combo.setEditable(True)
        combo.addItems(self.items)

        validator = ListValidator(self.items, combo)
        combo.setValidator(validator)

        completer = QCompleter(self.items, combo)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        combo.setCompleter(completer)
        # ClickFocus αντί StrongFocus: το combo αποκτά focus μόνο σε mouse click,
        # όχι σε hover. Αποτρέπει Ι-beam cursor / visual focus σε mouse-over του cell.
        combo.setFocusPolicy(Qt.ClickFocus)

        # Αποθήκευση αρχικής τιμής
        combo.setProperty("cell_index", index)
        combo.setProperty("initial_value", index.data())

        combo.activated.connect(lambda: self.on_selection_changed(combo))  # activated = μόνο όταν επιλέγεις

        combo.installEventFilter(self)

        return combo

    def eventFilter(self, editor, event):
        """Έλεγχος όταν χάνει το focus"""
        if event.type() == QEvent.FocusOut:
            #  Όταν χάνει focus, κάνε manual commit
            self.validate_and_commit(editor)

        return super().eventFilter(editor, event)

    def validate_and_commit(self, editor):
        """Validate και commit με έλεγχο"""
        text = editor.currentText().strip()

        # Έλεγχος αν η τιμή είναι valid
        if text not in self.items:
            # Invalid - force set to --Επιλέξτε
            editor.setCurrentText("--Επιλέξτε")

        # Commit
        self.commitData.emit(editor)

    def on_selection_changed(self, combo):

        initial = combo.property("initial_value")
        current = combo.currentText()

        # Κλείσε μόνο αν άλλαξε πραγματικά
        if initial != current:
            index = combo.property("cell_index")
            view = combo.parent().parent()

            self.commitData.emit(combo)
            self.closeEditor.emit(combo, QStyledItemDelegate.NoHint)

            # Επαναφορά current index στο cell που μόλις επεξεργάστηκε —
            # τα itemChanged signals από on_item_changed (π.χ. recalculate/total
            # updates στη γραμμή 0) μπορεί να έχουν μετακινήσει το currentIndex.
            if index.isValid():
                view.setCurrentIndex(index)

    def setEditorData(self, editor, index):
        value = index.data()
        if value:
            editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        text = editor.currentText().strip()
        if text in self.items or text == "--Επιλέξτε":
             model.setData(index, text)
        else:
            # Άκυρη τιμή - μην την αποθηκεύσεις
            # Επαναφορά στην αρχική ή κενό
            model.setData(index, "--Επιλέξτε")



    def commit_and_close(self, editor):
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)


class DynamicComboDelegate(QStyledItemDelegate):
    """Κλάση για το combobox της 2ης στήλης-ποικιλία """
    def __init__(self, get_items_func, parent=None): 
        super().__init__(parent) 
        self.get_items = get_items_func 

    def createEditor(self, parent, option, index): 
        combo = QComboBox(parent) 
        combo.addItems(self.get_items(index))
        combo.currentIndexChanged.connect(
        lambda: self.commit_and_close(combo)
    )
        
        return combo 
    
    def setEditorData(self, editor, index): 
        value = index.data() 
        if value: editor.setCurrentText(value) 
        
    def setModelData(self, editor, model, index): 
        model.setData(index, editor.currentText()) 
    
    def commit_and_close(self, editor):
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)
    
  

class SearchableDynamicComboDelegate(QStyledItemDelegate): 
    """Κλάση για το search combobox της 2ης στήλης"""
    def __init__(self, get_items_func, parent=None): 
        super().__init__(parent) 
        self.get_items = get_items_func 
        
    def createEditor(self, parent, option, index):
        combo = NoWheelComboBox(parent)
        combo.setEditable(True)
        items = self.get_items(index)
        combo.addItems(items)

        validator = ListValidator(items, combo)
        combo.setValidator(validator)

        completer = QCompleter(items, combo)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        combo.setCompleter(completer)
        combo.setFocusPolicy(Qt.ClickFocus)

        #  Αποθήκευση αρχικής τιμής
        combo.setProperty("cell_index", index)
        combo.setProperty("initial_value", index.data())
        combo.setProperty("valid_items", items)
     
        combo.activated.connect(lambda: self.on_selection_changed(combo))  # activated = μόνο όταν επιλέγεις
        combo.installEventFilter(self)

        return combo 
    
    def eventFilter(self, editor, event):
        """Έλεγχος όταν χάνει το focus"""
        if event.type() == QEvent.FocusOut:
            # 🔥 Όταν χάνει focus, validate και commit
            self.validate_and_commit(editor)

        return super().eventFilter(editor, event)

    def validate_and_commit(self, editor):
        """Validate και commit με έλεγχο"""
        text = editor.currentText().strip()
        valid_items = editor.property("valid_items")
        
        # Έλεγχος αν η τιμή είναι valid
        if text not in valid_items:
            # Invalid - force set to --Επιλέξτε
            editor.setCurrentText("--Επιλέξτε")
        
        # Commit
        self.commitData.emit(editor)
    
    def on_selection_changed(self, combo):
        """Κλείσε ΜΟΝΟ αν άλλαξε η τιμή"""
        initial = combo.property("initial_value")
        current = combo.currentText()
        
        #  Κλείσε μόνο αν άλλαξε πραγματικά
        if initial != current:
            self.commitData.emit(combo)
            
            index = combo.property("cell_index")
            view = combo.parent().parent()
            
            view.closePersistentEditor(index)
            QTimer.singleShot(10, lambda: view.openPersistentEditor(index))
    
    def setEditorData(self, editor, index): 
        value = index.data() 
        if value: 
            editor.setCurrentText(value) 

    def setModelData(self, editor, model, index): 
        text = editor.currentText().strip()
        valid_items = editor.property("valid_items")
        
        #  Έλεγχος αν η τιμή υπάρχει στη λίστα
        if text in valid_items or text == "--Επιλέξτε":
            model.setData(index, text)
        else:
            # Άκυρη τιμή - επαναφορά
            model.setData(index, "--Επιλέξτε")
        
    def commit_and_close(self, editor):
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)
            

class NoWheelComboDelegate(QStyledItemDelegate): 
    """Κλάση για combobox μη searchable που αγνοεί το scroll"""
    def __init__(self, items, parent=None): 
        super().__init__(parent) 
        self.items = items 
    
    def createEditor(self, parent, option, index): 
       
        combo = NoWheelComboBox(parent) 
        combo.addItems(self.items) 
        combo.currentIndexChanged.connect(
        lambda: self.commit_and_close(combo)
    )
        combo.setFocusPolicy(Qt.ClickFocus)
        return combo 
    
    def setEditorData(self, editor, index): 
        value = index.data() 
        if value: 
            editor.setCurrentText(value) 
            
    def setModelData(self, editor, model, index): 
        model.setData(index, editor.currentText())

    def commit_and_close(self, editor):
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)


class Double2DecimalDelegate(QStyledItemDelegate):
    """Κλάση με 2 δεκαδικά και max 7 ακέραιους"""

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setAlignment(Qt.AlignCenter)

        # ✔ δέχεται αριθμούς με , ή .
        regex = QRegExp(r"^\d{0,7}(?:[.,]\d{0,2})?$")
        validator = QRegExpValidator(regex, editor)
        editor.setValidator(validator)

        return editor

    def setEditorData(self, editor, index):
        value = index.data()
        if value is not None:
            editor.setText(str(value))

    def setModelData(self, editor, model, index):
        text = editor.text().strip()

        if not text:
            model.setData(index, "")
            return

        # ✔ αποθήκευση πάντα με τελεία
        text = text.replace(",", ".")

        try:
            value = float(text)
            model.setData(index, f"{value:.2f}")
        except ValueError:
            model.setData(index, "")


class IntOnlyDelegate(QStyledItemDelegate):
    """Κλάση για ακέραιους (max 7 ακέραιοι)"""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        
        #  Μόνο ακέραιοι 0-9999999, ΟΧΙ κόμμα
        regex = QRegExp(r"^\d{0,7}$")  # μόνο ψηφία, max 7
        validator = QRegExpValidator(regex, editor)
        editor.setValidator(validator)
        editor.setAlignment(Qt.AlignCenter)

        return editor

    def setEditorData(self, editor, index):
        value = index.data()
        if value:
            editor.setText(str(value))

    def setModelData(self, editor, model, index):
        text = editor.text().strip()
        if not text:
            model.setData(index, "")
        else:
            try:
                # "007" → 7 → "7"
                clean_value = str(int(text))
                model.setData(index, clean_value)
            except ValueError:
                model.setData(index, text)












