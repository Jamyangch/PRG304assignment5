import sys
from PyQt6.QtWidgets import QApplication
from ui import LibraryWindow

app = QApplication(sys.argv)

window = LibraryWindow()
window.show()

sys.exit(app.exec())