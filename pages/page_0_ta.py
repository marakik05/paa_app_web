from pages.base_table import baseTable
from ui.ui_page import Ui_page


class taPage(baseTable):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Φόρτωμα UI από Designer
        self.ui=Ui_page()
       
        self.ui.setupUi(self)

        self.setup_ui()
        
       
         # Σύνδεση κουμπιών με συνάρτηση προσθήκης σειράς
        self.ui.addbtn.clicked.connect(self.add_row)
 
        #Combobox Περιφέρειας
        self.selected_periferia = None
    
    
        
   

   
   
                    
               
                



                
        
        
        

        

           

   
        
        
        
       


        

        
       

