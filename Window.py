import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QPushButton, QVBoxLayout, QWidget, QColorDialog, QSlider, QLabel
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import  Qt, QPoint

class Canvas(QWidget):
  def __init__(self):
    super().__init__()
    self.start_point = None #Start point of the line
    self.end_point = None #End point of the line
    self.current_points = [] #For freeform drawing
    self.lines = [] #To store drawn lines (each as a tuple of start and end points)
    self.pen_color = Qt.black #Default color
    self.pen_thickness = 3 #Default pen thickness
    self.drawing_mode = 'line' #Defaukt drawing mode (line, freeform, rectangle, circle)
  def paintEvent(self, event):
    #Method called whenever the widget needs to be updated
    painter = QPainter(self)
    
    #Draw all stored shapes/lines
    for shape in self.lines:
      if shape['type'] == 'line':
        self.draw_line(painter, shape)
      elif shape['type'] == 'freeform':
        self.draw_freeform(painter, shape)
      elif shape['type'] == 'rectangle':
        self.draw_rectangle(painter, shape)
      elif shape['type'] == 'circle':
              self.draw_circle(painter, shape)

    #Draw the shape being actively drawn
    if self.start_point and self.end_point:
      if self.drawing_mode == 'line':
        self.draw_line(painter, {'start': self.start_point, 'end': self.end_point, 'color': self.pen_color, 'thickness': self.pen_thickness })
      elif self.drawing_mode == 'rectangle':
        self.draw_rectangle(painter, {'start': self.start_point, 'end': self.end_point, 'color': self.pen_color, 'thickness': self.pen_thickness })
      elif self.drawing_mode == 'circle':
        self.draw_circle(painter, {'start': self.start_point, 'end': self.end_point, 'color': self.pen_color, 'thickness': self.pen_thickness })
    
    #If the user is currently drawing a shape, we draw it as well
    if self.start_point and self.end_point:
      painter.drawLine(self.start_point, self.end_point)
      pen = QPen(self.pen_color, self.pen_thickness, Qt.SolidLine)
      painter.setPen(pen)
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
      self.lines.append((self.start_point, self.end_point, self.pen_color, self.pen_thickness)) #Store the line
      self.start_point = None
      self.end_point = None
      self.update() #Updating the canvas
  #Function to set the pen color
  def set_pen_color(self, color):
    self.pen_color = color
  def set_pen_thickness(self, thickness):
    print(f"Pen thickness set to : {thickness}")  #Debugging : Print to check
    self.pen_thickness = thickness
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
    #Creatin a button for the color picker
    color_button = QPushButton("Pick Color", self)
    color_button.clicked.connect(self.pick_color)
    #Creating a slider for adjusting the line thickness
    thickness_slider = QSlider(Qt.Horizontal, self)
    thickness_slider.setRange(1, 10) #Line thickness between 1 and 10
    thickness_slider.setValue(3) #Default value
    thickness_slider.valueChanged.connect(self.change_thickness)
    #Creating a label for the slider
    slider_label = QLabel("Line thickness", self)
    #Create a layout and add the button, the canvas
    layout = QVBoxLayout()
    layout.addWidget(new_design_button)
    layout.addWidget(self.canvas)
    layout.addWidget(clear_button)
    layout.addWidget(color_button)
    layout.addWidget(thickness_slider)
    layout.addWidget(slider_label)
    #create a central widget, set the layout, and assign it to the main window
    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)
  def start_new_design(self):
      # function that get called when the button is clicked
      print("Starting a new Design")
  def pick_color(self):
    #Open a color dialog and let the user select the color
    color = QColorDialog.getColor()
    if color.isValid():
      self.canvas.set_pen_color(color)  #Set the chosen color to the canvas
  def change_thickness(self, value):
    #Change the pen thickness when the slider is adjusted
    print(f"Changing line thickness to {value}")
    self.canvas.set_pen_thickness(value)
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