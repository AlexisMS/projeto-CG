import sys, logging
from object import WireFrame
from PySide6.QtCore import Qt, QSize, QPoint, QLine, Slot, QRect
from PySide6.QtGui import QColor, QPolygon
from PySide6.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QListWidget, QListWidgetItem, QLabel, QGroupBox, QGraphicsScene, QGraphicsView, QPlainTextEdit, QLayout, QMainWindow, QGraphicsLineItem, QLineEdit, QSpinBox

class QTextEditLogger(logging.Handler):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

class NewObjectDialog(QWidget):
    def __init__(self, point_amount):
        super().__init__()

        self.points = []

        self.x_label = []
        self.x_coord = []
        self.y_label = []
        self.y_coord = []

        for n in range(point_amount): 
            self.x_label.append(QLabel("X"+str(n)))
            self.x_coord.append(QLineEdit())
            self.y_label.append(QLabel("Y"+str(n)))
            self.y_coord.append(QLineEdit())

        #self.buttonAddPoint= QPushButton("Adicionar ponto")
        #self.buttonAddPoint.clicked.connect(self.new_Point)
        self.buttonCreateObject = QPushButton("Criar objeto")
        self.buttonCreateObject.clicked.connect(self.new_Object)
        
        point_layout = []
        point_widget = []
        for n in range(point_amount):
            point_layout.append(QHBoxLayout())
            point_layout[n].addWidget(self.x_label[n])
            point_layout[n].addWidget(self.x_coord[n])
            point_layout[n].addWidget(self.y_label[n])
            point_layout[n].addWidget(self.y_coord[n])
            point_widget.append(QWidget())
            point_widget[n].setLayout(point_layout[n])

        layout = QVBoxLayout()
        for n in range(point_amount):
            layout.addWidget(point_widget[n])
        #layout.addWidget(self.buttonAddPoint)
        layout.addWidget(self.buttonCreateObject)
        self.setLayout(layout)
        self.setWindowTitle("Novo Objeto")
    
    @Slot()
    def new_Point(self, n):
        self.points.append(QPoint(int(self.x_coord[n].text()), int(self.y_coord[n].text())))
        #self.xx.clear()
        #self.yy.clear()
    
    @Slot()
    def new_Object(self, point_ammount):
        for n in range(point_ammount):
            self.new_Point(n)
        self.x_coord.clear()
        self.y_coord.clear()
        #polygon = QPolygon(self.points)        
        #scene.addPolygon(polygon)
 
        message = ("poligono criado em")
        for p in self.points:
            message += " (" +self.x_coord[n].text()+ "," +self.y_coord[n].text()+ ")"

        logging.info(message)

        self.close()
    
class SubWindows():
    def open_NewObjectDialog(self, checked):
        self.new_window = NewObjectDialog(create_object_point_amount.value())
        self.new_window.show()

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
    
    # Viewport
    viewport = QGraphicsView(scene)
    viewport.setFixedSize(QSize(800,600))
    viewport.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)        
    viewport.setSceneRect(QRect(0,0, 780,580))
    
    object_list = QListWidget()
    for i in range(6):
        item = QListWidgetItem(f"Objeto {i}")
        item.setTextAlignment(Qt.AlignCenter)
        object_list.addItem(item)

    logTextBox = QTextEditLogger()
    logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(logTextBox)
    logging.getLogger().setLevel(logging.DEBUG)

    # Interface para iniciar criação de objetos
    create_object_point_amount_label = QLabel("Número de pontos:")
    create_object_point_amount = QSpinBox()
    create_object_point_amount.setMinimum(1)
    create_object_point_amount_layout = QHBoxLayout()
    create_object_point_amount_layout.addWidget(create_object_point_amount_label)
    create_object_point_amount_layout.addWidget(create_object_point_amount)
    create_object_point_amount_widget = QWidget()
    create_object_point_amount_widget.setLayout(create_object_point_amount_layout)
    create_object_button = QPushButton("Novo Objeto")
    create_object_button.clicked.connect(subWindows.open_NewObjectDialog)

    scene.addLine(QLine(100, 200, 300, 200))

    # Botões referentes a função de zoom
    zoom_in_button = QPushButton("+")
    zoom_out_button = QPushButton("-")
    zoom_in_button.clicked.connect(lambda: viewport.scale(1.2, 1.2))
    zoom_out_button.clicked.connect(lambda: viewport.scale(1/1.2, 1/1.2))

    # Botões referentes a função de navegação
    nav_left_button = QPushButton("left")
    nav_right_button = QPushButton("right")
    nav_up_button = QPushButton("up")
    nav_down_button = QPushButton("down")
    nav_left_button.clicked.connect(nav_left)
    nav_right_button.clicked.connect(nav_right)
    nav_up_button.clicked.connect(nav_up)
    nav_down_button.clicked.connect(nav_down)

    # Inicio dos layouts
    # Layout do menu dos objetos
    # Contém a lista de objetos e botão de criar objetos
    left_objects_layout = QVBoxLayout()  
    left_objects_layout.addWidget(create_object_point_amount_widget)  
    left_objects_layout.addWidget(create_object_button)
    left_objects_layout.addWidget(object_list)
    left_objects_menu = QGroupBox("Objetos")
    left_objects_menu.setLayout(left_objects_layout)

    # Layout do menu de zooms
    # Contém todos os botões de zoom
    left_zoom_layout = QHBoxLayout()
    left_zoom_layout.addWidget(zoom_in_button)
    left_zoom_layout.addWidget(zoom_out_button)
    left_zoom_menu = QGroupBox("Zoom")
    left_zoom_menu.setLayout(left_zoom_layout)

    # Layout do menu de navegação
    # Contém todos os botões de navegação
    left_nav_layout = QGridLayout()
    left_nav_layout.addWidget(nav_up_button, 1, 2)
    left_nav_layout.addWidget(nav_left_button, 2, 1)
    left_nav_layout.addWidget(nav_right_button, 2, 3)
    left_nav_layout.addWidget(nav_down_button, 3, 2)
    left_nav_menu = QGroupBox("Navegação")
    left_nav_menu.setLayout(left_nav_layout)

    # Layout do menu
    # Contém lista de objetos e funções de zoom e navegação
    left_menu_layout = QVBoxLayout()
    left_menu_layout.addWidget(left_objects_menu)
    left_menu_layout.addWidget(left_zoom_menu)
    left_menu_layout.addWidget(left_nav_menu)
    left_menu = QGroupBox()
    left_menu.setLayout(left_menu_layout)

    # Layout do viewport
    # Contém a parte gráfica do viewport
    viewport_layout = QVBoxLayout()
    viewport_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    viewport_layout.addWidget(viewport)
    main_widget = QGroupBox("Viewport")
    main_widget.setLayout(viewport_layout)

    # Layout do log
    # Contém a paret textual do log
    log_layout = QVBoxLayout()
    log_layout.addWidget(logTextBox.widget)
    log_widget = QGroupBox("Logs")
    log_widget.setLayout(log_layout)

    # Layout da interface de usuario
    # Contém o menu de funções e objetos 
    main_ui_layout = QHBoxLayout()
    main_ui_layout.addWidget(left_menu, 1)
    main_ui_layout.addWidget(main_widget, 3)
    main_ui = QWidget()    
    main_ui.setLayout(main_ui_layout)

    # Janela principal
    # Contém interface de usuario e parte de log
    window_layout = QVBoxLayout()
    window_layout.addWidget(main_ui, 10)
    window_layout.addWidget(log_widget, 1)
    window_ui = QWidget()
    window_ui.setLayout(window_layout)
    window_ui.setWindowTitle("Computação Gráfica")
    window_ui.show()

    logging.info('programa iniciado')
    sys.exit(app.exec())