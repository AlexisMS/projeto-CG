import sys, logging
from PySide6.QtCore import Qt, QSize, QPoint, QLine, Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QListWidget, QListWidgetItem, QLabel, QGroupBox, QGraphicsScene, QGraphicsView, QPlainTextEdit, QLayout, QMainWindow, QGraphicsLineItem, QLineEdit

class QTextEditLogger(logging.Handler):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

class NewObjectDialog(QWidget):
    def __init__(self):
        super().__init__()

        x1_label = QLabel("X1")
        self.x1 = QLineEdit()
        x2_label = QLabel("X2")
        self.x2 = QLineEdit()
        y1_label = QLabel("Y1")
        self.y1 = QLineEdit()
        y2_label = QLabel("Y2")
        self.y2 = QLineEdit()
        self.confirm = QPushButton("Criar")
        self.confirm.clicked.connect(self.new_Object)
        
        line1_layout = QHBoxLayout()
        line1_layout.addWidget(x1_label)
        line1_layout.addWidget(self.x1)
        line1_layout.addWidget(y1_label)
        line1_layout.addWidget(self.y1)
        line1 = QWidget()
        line1.setLayout(line1_layout)

        line2_layout = QHBoxLayout()
        line2_layout.addWidget(x2_label)
        line2_layout.addWidget(self.x2)
        line2_layout.addWidget(y2_label)
        line2_layout.addWidget(self.y2)
        line2 = QWidget()
        line2.setLayout(line2_layout)

        layout = QVBoxLayout()
        layout.addWidget(line1)
        layout.addWidget(line2)
        layout.addWidget(self.confirm)
        self.setLayout(layout)
        self.setWindowTitle("Novo Objeto")
    
    @Slot()
    def new_Object(self):        
        scene.addLine(QLine(int(self.x1.text()), int(self.y1.text()), int(self.x2.text()), int(self.y2.text())))
        #scene.update()
        logging.info("reta criada em ("+self.x1.text()+","+self.y1.text()+"), ("+self.x2.text()+","+self.y2.text()+")")

class SubWindows():
    def open_NewObjectDialog(self, checked):
        self.new_window = NewObjectDialog()
        self.new_window.show()

class Functions():
    def zoom_In():
        pass

    def zoom_Out():
        pass

    def nav_left():
        pass

    def nav_right():
        pass

    def nav_up():
        pass

    def nav_down():
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.setBackgroundBrush(QColor('grey'))

    subWindows = SubWindows()
    functions = Functions()

    #features
    viewport = QGraphicsView(scene)
    viewport.setFixedSize(QSize(800,600))
    viewport.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
    viewport.setSceneRect(0,0, 780,580)

    object_list = QListWidget()
    for i in range(6):
        item = QListWidgetItem(f"Objeto {i}")
        item.setTextAlignment(Qt.AlignCenter)
        object_list.addItem(item)

    create_object_button = QPushButton("Novo Objeto")
    create_object_button.clicked.connect(subWindows.open_NewObjectDialog)

    logTextBox = QTextEditLogger()
    logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(logTextBox)
    logging.getLogger().setLevel(logging.DEBUG)

    # Inicio dos layouts
    # Layout do menu dos objetos
    create_object_button = QPushButton("Novo Objeto")
    create_object_button.clicked.connect(subWindows.open_NewObjectDialog)

    left_objects_layout = QVBoxLayout()    
    left_objects_layout.addWidget(create_object_button)
    left_objects_layout.addWidget(object_list)
    left_objects_menu = QGroupBox("Objetos")
    left_objects_menu.setLayout(left_objects_layout)

    # Layout do menu de zooms
    zoom_in_button = QPushButton("+")
    zoom_out_button = QPushButton("-")
    zoom_in_button.clicked.connect(functions.zoom_In)
    zoom_out_button.clicked.connect(functions.zoom_Out)

    left_zoom_layout = QHBoxLayout()
    left_zoom_layout.addWidget(zoom_in_button)
    left_zoom_layout.addWidget(zoom_out_button)
    left_zoom_menu = QGroupBox("Zoom")
    left_zoom_menu.setLayout(left_zoom_layout)

    # Layout do menu de navegação
    nav_left_button = QPushButton("left")
    nav_right_button = QPushButton("right")
    nav_up_button = QPushButton("up")
    nav_down_button = QPushButton("down")
    nav_left_button.clicked.connect(functions.nav_left)
    nav_right_button.clicked.connect(functions.nav_right)
    nav_up_button.clicked.connect(functions.nav_up)
    nav_down_button.clicked.connect(functions.nav_down)

    left_nav_layout = QGridLayout()
    left_nav_layout.addWidget(nav_up_button, 1, 2)
    left_nav_layout.addWidget(nav_left_button, 2, 1)
    left_nav_layout.addWidget(nav_right_button, 2, 3)
    left_nav_layout.addWidget(nav_down_button, 3, 2)
    left_nav_menu = QGroupBox("Navegação")
    left_nav_menu.setLayout(left_nav_layout)

    # Layout do menu a esquerda
    left_menu_layout = QVBoxLayout()
    left_menu_layout.addWidget(left_objects_menu)
    left_menu_layout.addWidget(left_zoom_menu)
    left_menu_layout.addWidget(left_nav_menu)
    left_menu = QGroupBox()
    left_menu.setLayout(left_menu_layout)

    # Layout do viewport
    viewport_layout = QVBoxLayout()
    viewport_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    viewport_layout.addWidget(viewport)
    main_widget = QGroupBox("Viewport")
    main_widget.setLayout(viewport_layout)

    log_layout = QVBoxLayout()
    log_layout.addWidget(logTextBox.widget)
    log_widget = QGroupBox("Logs")
    log_widget.setLayout(log_layout)

    main_ui_layout = QHBoxLayout()
    main_ui_layout.addWidget(left_menu, 1)
    main_ui_layout.addWidget(main_widget, 3)
    main_ui = QWidget()    
    main_ui.setLayout(main_ui_layout)

    window_layout = QVBoxLayout()
    window_layout.addWidget(main_ui, 10)
    window_layout.addWidget(log_widget, 1)
    window_ui = QWidget()
    window_ui.setLayout(window_layout)
    window_ui.setWindowTitle("Computação Gráfica")
    window_ui.show()

    logging.info('programa iniciado')
    sys.exit(app.exec())