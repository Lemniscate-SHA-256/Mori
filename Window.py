import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Biomimetic Design Tool")
    self.setGeometry(100, 100, 800, 600)

    self.create_menu_bar()
  def create_menu_bar(self):

    menu_bar = self.menuBar()
    file_menu = menu_bar.addMenu("File")

    open_action = QAction("Open", self)
    open_action.triggered.connect(self.open_file_dialog)

    save_action = QAction("Save", self)
    save_action.triggered.connect(self.save_file_dialog)

    exit_action = QAction("Exit", self)
    exit_action.triggered.connect(self.close)

    #Add Actions To Menu
    file_menu.addAction(open_action)
    file_menu.addAction(save_action)
    file_menu.addAction(exit_action)

  def open_file_dialog(self):
    options = QFileDialog.Options()
    file_name , _ = QFileDialog.getOpenFileName(self, "Open Design File", "", "All Files (*);;Design Files (*.des)", options=options)
    if file_name:
      print(f"Opening file: {file_name}")

  def save_file_dialog(self):
    options = QFileDialog.Options()
    file_name , _ = QFileDialog.getSaveFileName(self, "Save Design File", "", "All Files (*);;Design Files (* .des)", options=options)
    if file_name:
      print(f"Saving file: {file_name}")


#initialization of the application
app = QApplication(sys.argv)

#creating instance of the main window
window = MainWindow()

window.show()

sys.exit(app.exec_())