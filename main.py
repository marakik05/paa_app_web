import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QIcon
from main_window import MainWindow
from utils.excel_loader import resource_path

def main():
    # High DPI Support για Windows 7+
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    # Windows DPI Awareness + AppUserModelID για σωστό taskbar icon/grouping
    try:
        from ctypes import windll
        # Windows 8.1+: shcore.SetProcessDpiAwareness
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except (OSError, AttributeError):
            # Windows 7/Vista fallback: user32.SetProcessDPIAware (Vista+)
            try:
                windll.user32.SetProcessDPIAware()
            except Exception:
                pass # nosec B110 - DPI fallback, μη κρίσιμο
        # Windows 7+: AppUserModelID (διαθέσιμο από Win7)
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("paa.app.moria.1")
    except Exception:
        pass  # nosec B110 - non-Windows OS, σκόπιμα ignore
    app = QApplication(sys.argv)
    # Εφαρμογή icon σε όλα τα παράθυρα (main window, QMessageBox, dialogs)
    app.setWindowIcon(QIcon(resource_path("logo/pic.ico")))
    # Default font (Verdana fallback)
    font = QFont("Verdana", 9)
    app.setFont(font)
    window = MainWindow()
    window.setAttribute(Qt.WA_StyledBackground, True)
    window.show()
    # Force event loop να επεξεργαστεί το show() — κάνει το main window
    # πραγματικά visible πριν κλείσουμε το splash, αποφεύγοντας flicker
    # ("κενή" στιγμή χωρίς ορατό παράθυρο μεταξύ splash close & main show).
    QApplication.processEvents()
    # Κλείσιμο PyInstaller splash screen όταν εμφανιστεί το main window
    try:
        import pyi_splash  # type: ignore
        pyi_splash.close()
    except (ImportError, RuntimeError):
        pass  # nosec B110 - δεν τρέχει σε dev mode (χωρίς --splash) ή ήδη closed

    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
