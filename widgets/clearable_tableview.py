from PySide2.QtWidgets import QTableView, QApplication, QAbstractItemView, QLineEdit, QAbstractItemDelegate
from PySide2.QtCore import Qt, QEvent


class ClearableTableView(QTableView):
    """Νέο tableview για τους πίνακες της ΤΑ"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)

        self.setEditTriggers(
            QAbstractItemView.DoubleClicked |
            QAbstractItemView.EditKeyPressed |
            QAbstractItemView.AnyKeyPressed
        )

        self.setTabKeyNavigation(False)
        self.setFocusPolicy(Qt.StrongFocus)

    def edit(self, index, trigger, event):
        result = super().edit(index, trigger, event)
        if result:
            editor = self.indexWidget(index)
            if editor and isinstance(editor, QLineEdit):
                editor.installEventFilter(self)
        return result

    # Block hover events στις combo στήλες (0, 1, 4, 7) — αλλιώς χάνεται focus.
    def viewportEvent(self, event):
        if event.type() == QEvent.MouseMove and event.buttons() == Qt.NoButton:
            idx = self.indexAt(event.pos())
            if idx.isValid() and idx.column() in (0, 1, 4, 7):
                return True
        return super().viewportEvent(event)

    # Πιάνει τα arrow keys ΣΤΟ EDITOR
    def eventFilter(self, obj, event):
        if isinstance(obj, QLineEdit) and event.type() == QEvent.KeyPress:
            key = event.key()
            if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                self.commitData(obj)
                self.closeEditor(obj, QAbstractItemDelegate.SubmitModelCache)

                if key == Qt.Key_Left:
                    self.move_horizontal(-1)
                elif key == Qt.Key_Right:
                    self.move_horizontal(1)
                elif key == Qt.Key_Up:
                    self.move_vertical(-1)
                elif key == Qt.Key_Down:
                    self.move_vertical(1)

                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):

        key = event.key()
        mod = event.modifiers()
        model = self.model()

        if not model:
            super().keyPressEvent(event)
            return

        # COPY
        if key == Qt.Key_C and mod == Qt.ControlModifier:
            self.copy_selection()
            return

        # DELETE
        if key in (Qt.Key_Delete, Qt.Key_Backspace):
            self.clear_selected_cells()
            return

        # PASTE
        if key == Qt.Key_V and mod == Qt.ControlModifier:
            self.paste_selection()
            return

        # ENTER NAV
        if key in (Qt.Key_Return, Qt.Key_Enter):
            self.move_vertical(-1 if mod == Qt.ShiftModifier else 1)
            return

        super().keyPressEvent(event)

    # NAVIGATION

    def move_vertical(self, step):
        idx = self.currentIndex()
        row = max(0, min(self.model().rowCount() - 1, idx.row() + step))
        self.setCurrentIndex(self.model().index(row, idx.column()))

    def move_horizontal(self, step):
        idx = self.currentIndex()
        col = max(0, min(self.model().columnCount() - 1, idx.column() + step))
        self.setCurrentIndex(self.model().index(idx.row(), col))

    # COPY MULTI CELLS

    def copy_selection(self):

        indexes = self.selectedIndexes()
        if not indexes:
            return

        indexes = sorted(indexes, key=lambda i: (i.row(), i.column()))

        min_row = indexes[0].row()
        max_row = indexes[-1].row()
        min_col = min(i.column() for i in indexes)
        max_col = max(i.column() for i in indexes)

        rows = []

        for r in range(min_row, max_row + 1):
            row_data = []
            for c in range(min_col, max_col + 1):
                idx = self.model().index(r, c)
                val = self.model().data(idx) or ""
                row_data.append(str(val))
            rows.append("\t".join(row_data))

        QApplication.clipboard().setText("\n".join(rows))

    # CLEAR CELLS

    def clear_selected_cells(self):

        model = self.model()

        for index in self.selectedIndexes():
            item = model.itemFromIndex(index)
            if not item:
                continue
            if not (item.flags() & Qt.ItemIsEditable):
                continue
            if model.data(index) == "":
                continue
            model.setData(index, "")

    # PASTE

    def paste_selection(self):
        """Επικόλληση από clipboard με validation"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()

        if not text:
            return

        selection = self.selectionModel().selectedIndexes()
        if not selection:
            return

        rows = text.split('\n')
        data = [row.split('\t') for row in rows if row]

        start_row = min(i.row() for i in selection)
        start_col = min(i.column() for i in selection)

        for i, row_data in enumerate(data):
            for j, value in enumerate(row_data):
                target_row = start_row + i
                target_col = start_col + j

                if target_row >= self.model().rowCount():
                    break
                if target_col >= self.model().columnCount():
                    break

                index = self.model().index(target_row, target_col)

                item = self.model().itemFromIndex(index)
                if not item or not (item.flags() & Qt.ItemIsEditable):
                    continue

                if target_col == 3:  # Έκταση (float, 2 δεκαδικά)
                    try:
                        normalized = f"{float(value.replace(',', '.')):.2f}"
                        self.model().setData(index, normalized)
                    except ValueError:
                        self.model().setData(index, "")
                elif target_col in (5, 6):  # Δένδρα (int)
                    try:
                        normalized = str(int(value))
                        self.model().setData(index, normalized)
                    except ValueError:
                        self.model().setData(index, "")
                else:
                    self.model().setData(index, value)



#προηγούμενος πίνακας με undo

# from PySide2.QtWidgets import QMessageBox, QTableView, QApplication, QAbstractItemView, QLineEdit, QAbstractItemDelegate
# from PySide2.QtCore import Qt, QModelIndex, QEvent
# from PySide2.QtWidgets import QUndoStack, QUndoCommand



# class CellEditCommand(QUndoCommand):
#     """Undo command για αλλαγες κελιών των πινάκων ΤΑ"""

#     def __init__(self, model, changes, description="Edit cells"):
#         super().__init__(description)
#         self.model = model
#         self.changes = changes

#     def undo(self):
#         for index, old, new in self.changes:
#             self.model.setData(index, old)

#     def redo(self):
#         for index, old, new in self.changes:
#             self.model.setData(index, new)


# class ClearableTableView(QTableView):
#     """Νέο tableview για τους πίνακες της ΤΑ"""

#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.undo_stack = QUndoStack(self)

#         self.setSelectionMode(QAbstractItemView.ExtendedSelection)
#         self.setSelectionBehavior(QAbstractItemView.SelectItems)

#         self.setEditTriggers(
#             QAbstractItemView.DoubleClicked |
#             QAbstractItemView.EditKeyPressed |
#             QAbstractItemView.AnyKeyPressed
# )

#         self.setTabKeyNavigation(False)
#         self.setFocusPolicy(Qt.StrongFocus)

#     def edit(self, index, trigger, event):
#         result = super().edit(index, trigger, event)
#         if result:
#             editor = self.indexWidget(index)
#             if editor and isinstance(editor, QLineEdit):
#                 editor.installEventFilter(self)
#         return result

#     #  Αυτό πιάνει τα arrow keys ΣΤΟ EDITOR
#     def eventFilter(self, obj, event):
#         if isinstance(obj, QLineEdit) and event.type() == QEvent.KeyPress:
#             key = event.key()
#             if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
#                 self.commitData(obj)
#                 self.closeEditor(obj, QAbstractItemDelegate.SubmitModelCache)
                
#                 if key == Qt.Key_Left:
#                     self.move_horizontal(-1)
#                 elif key == Qt.Key_Right:
#                     self.move_horizontal(1)
#                 elif key == Qt.Key_Up:
#                     self.move_vertical(-1)
#                 elif key == Qt.Key_Down:
#                     self.move_vertical(1)
                
#                 return True
#         return super().eventFilter(obj, event)

#     # def move_vertical(self, step):
#     #     idx = self.currentIndex()
#     #     row = max(0, min(self.model().rowCount() - 1, idx.row() + step))
#     #     self.setCurrentIndex(self.model().index(row, idx.column()))

#     # def move_horizontal(self, step):
#     #     idx = self.currentIndex()
#     #     col = max(0, min(self.model().columnCount() - 1, idx.column() + step))
#     #     self.setCurrentIndex(self.model().index(idx.row(), col))

#         #Keyboard
#     def keyPressEvent(self, event):

#         key = event.key()
#         mod = event.modifiers()
#         model = self.model()

#         if not model:
#             super().keyPressEvent(event)
#             return
  
#         # COPY

#         if key == Qt.Key_C and mod == Qt.ControlModifier:
#             self.copy_selection()
#             return

        
#         # DELETE
#         # ---------------------------------
#         if key in (Qt.Key_Delete, Qt.Key_Backspace):
#             self.clear_selected_cells()
#             return

#         #PASTE
#         #---------------------------------
#         if key == Qt.Key_V and mod == Qt.ControlModifier:
#             self.paste_selection()
#             return

    
#         # ENTER NAV
#         # ---------------------------------
#         if key in (Qt.Key_Return, Qt.Key_Enter):
#             self.move_vertical(-1 if mod == Qt.ShiftModifier else 1)
#             return


#         super().keyPressEvent(event)

    
#     # NAVIGATION
    
#     def move_vertical(self, step):
#         idx = self.currentIndex()
#         row = max(0, min(self.model().rowCount() - 1, idx.row() + step))
#         self.setCurrentIndex(self.model().index(row, idx.column()))

#     def move_horizontal(self, step):
#         idx = self.currentIndex()
#         col = max(0, min(self.model().columnCount() - 1, idx.column() + step))
#         self.setCurrentIndex(self.model().index(idx.row(), col))

#     # COPY MULTI CELLS
   
#     def copy_selection(self):

#         indexes = self.selectedIndexes()
#         if not indexes:
#             return

#         indexes = sorted(indexes, key=lambda i: (i.row(), i.column()))

#         min_row = indexes[0].row()
#         max_row = indexes[-1].row()
#         min_col = min(i.column() for i in indexes)
#         max_col = max(i.column() for i in indexes)

#         rows = []

#         for r in range(min_row, max_row + 1):
#             row_data = []
#             for c in range(min_col, max_col + 1):
#                 idx = self.model().index(r, c)
#                 val = self.model().data(idx) or ""
#                 row_data.append(str(val))
#             rows.append("\t".join(row_data))

#         QApplication.clipboard().setText("\n".join(rows))

    
#     # CLEAR CELLS (WITH UNDO)
    
#     def clear_selected_cells(self):

#         model = self.model()
#         changes = []

#         for index in self.selectedIndexes():

#             item = model.itemFromIndex(index)
#             if not item:
#                 continue

#             if not (item.flags() & Qt.ItemIsEditable):
#                 continue

#             old = model.data(index)
#             if old == "":
#                 continue

#             changes.append((QModelIndex(index), old, ""))

#         if not changes:
#             return

#         cmd = CellEditCommand(model, changes, "Clear cells")
#         self.undo_stack.push(cmd)

#     def paste_selection(self):
#         """Επικόλληση από clipboard με validation"""
#         clipboard = QApplication.clipboard()
#         text = clipboard.text()
        
#         if not text:
#             return
        
#         selection = self.selectionModel().selectedIndexes()
#         if not selection:
#             return
        
#         # Parse clipboard data
#         rows = text.split('\n')
#         data = [row.split('\t') for row in rows if row]
        
#         start_row = selection[0].row()
#         start_col = selection[0].column()
        
#         for i, row_data in enumerate(data):
#             for j, value in enumerate(row_data):
#                 target_row = start_row + i
#                 target_col = start_col + j
                
#                 if target_row >= self.model().rowCount():
#                     break
#                 if target_col >= self.model().columnCount():
#                     break
                
#                 # Validation ανά στήλη
#                 index = self.model().index(target_row, target_col)

#                 # ← Έλεγχος read-only
#                 item = self.model().itemFromIndex(index)
#                 if not item or not (item.flags() & Qt.ItemIsEditable):
#                     continue
#                 # Έλεγχος αν η στήλη πρέπει να περιέχει αριθμούς
#                 if target_col in (3, 5, 6):  # Έκταση, Δένδρα
#                     # Προσπάθησε να το μετατρέψεις σε αριθμό
#                     try:
#                         if target_col == 3:  # Float
#                             float(value.replace(",", "."))
#                         else:  # Int
#                             int(value)
                        
#                         # Αν επιτυχία, κάνε paste
#                         self.model().setData(index, value, Qt.EditRole)
                    
#                     except ValueError:
#                         # Αν αποτυχία, ΜΗΝ κάνεις paste
                        
#                         # Βάλε κενό αντί για την invalid τιμή
#                         self.model().setData(index, "", Qt.EditRole)
#                 else:
#                     # Για τις άλλες στήλες (text), κάνε paste κανονικά
#                     self.model().setData(index, value, Qt.EditRole)
