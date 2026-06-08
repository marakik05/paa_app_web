from pages.base_table import baseTable
from utils.message import show_temp_message
from ui.ui_page_mellontiki import Ui_page_mellontiki
class mellontikiPage(baseTable):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # Φόρτωμα UI από Designer
        self.ui=Ui_page_mellontiki()
       
        self.ui.setupUi(self)

        self.setup_ui()
        
       
         # Σύνδεση κουμπιών με συνάρτηση προσθήκης σειράς
        self.ui.addbtn_mel.clicked.connect(self.add_row)
        self.selected_periferia = None
   
        self.ui.copybtn.clicked.connect(self.import_from_table1)
    
    def set_source_table(self, source_table):
        
        self.source_table = source_table
    
    def import_from_table1(self):
        """Αντιγραφή εγγραφών του πίνακα 1-Αρχική ΤΑ"""       
       
        #  Έλεγχος: Έχει εγγραφές ο table1;
        if self.source_table.model.rowCount() == 0:
            show_temp_message(self,"Ο πίνακας της αρχικής ΤΑ δεν έχει εγγραφές!")
            return
        
        #  Πάρε όλα τα δεδομένα από τον 1ο πίνακα
        data = self.source_table.get_all_rows_data()
        
        #  Φόρτωσέ τα στον 2ο πίνακα (διαγράφει αυτόματα τα υπάρχοντα)
        self.load_rows_from_data(data)
        
       
