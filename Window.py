import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import  Qt, QPoint

class Canvas(QWidget):
  def __init__(self):
    super().__init__()
    self.start_point = None #Start point of the line
    self.end_point = None #End point of the line
    self.lines = [] #To store drawn lines (each as a tuple of start and end points)
  def paintEvent(self, event):
    #Method called whenever the widget needs to be updated
    painter = QPainter(self)
    pen = QPen(Qt.black, 3, Qt.SolidLine)
    painter.setPen(pen)
    #Draw all the previously stored lines
    for lines in self.lines:
      painter.drawLine(lines[0], lines[1])
    #If the user is currently drawing a line, we draw it as well
    if self.start_point and self.end_point:
      painter.drawLine(self.start_point, self.end_point)
  def mousePressEvent(self, event):
    #When the mouse button is pressed, whe start drawing a new line
    if event.button() == Qt.LeftButton:
      self.start_point = event.pos()
      self.end_point = self.start_point
  def mouseMoveEvent(self, event):
    #When the mouse is moved while pressed, update the end point of the current line
    if self.start_point:
      self.end_point = event.pos()
      self.update() #Update the canvas to reflect the changes
  def mouseReleaseEvent(self, event):
    #When the mouse button is released, finalize the line and store it
    if event.button() == Qt.LeftButton:
      self.end_point = event.pos()
      self.lines.append((self.start_point, self.end_point)) #Store the line
      self.start_point = None
      self.end_point = None
      self.update() #Updating the canvas
class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Biomimetic Design Tool")
    self.setGeometry(100, 100, 800, 600)
    self.create_menu_bar()
    # creating the main layout and adding a button
    self.init_ui()
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
  def init_ui(self):
    #Creating the canvas widget
    self.canvas = Canvas()
    #Create a button for starting new design
    new_design_button = QPushButton("Start New Design", self)
    new_design_button.clicked.connect(self.start_new_design)
    #Creating a button for clearing the canvas
    clear_button = QPushButton("Clear Canvas", self)
    clear_button.clicked.connect(self.clear_canvas)
    #Create a layout and add the button, the canvas
    layout = QVBoxLayout()
    layout.addWidget(new_design_button)
    layout.addWidget(self.canvas)
    layout.addWidget(clear_button)
    #create a central widget, set the layout, and assign it to the main window
    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)
  def start_new_design(self):
      # function that get called when the button is clicked
      print("Starting a new Design")
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
  def clear_canvas(self):
    #Function to clear canvas
    self.canvas.lines = []
    self.canvas.update()
    print("Clearing Canvas")

#Initialization of the application
app = QApplication(sys.argv)
#Creating instance of the main window
window = MainWindow()
#Show the window
window.show()
#Execute the application loop
sys.exit(app.exec_())