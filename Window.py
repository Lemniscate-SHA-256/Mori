import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Biomimetic Design Tool")
    self.setGeometry(100, 100, 800, 600)

#initialization of the application
app = QApplication(sys.argv)

#creating instance of the main window
window = MainWindow()

window.show()

sys.exit(app.exec_())