import sys, logging
from object import WireFrame
from PySide6.QtCore import Qt, QSize, QPoint, QLine, Slot
from PySide6.QtGui import QColor, QPolygon
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

        self.points = []

        xx_label = QLabel("X1")
        self.xx = QLineEdit()
        yy_label = QLabel("Y1")
        self.yy = QLineEdit()

        self.buttonAddPoint= QPushButton("Adicionar ponto")
        self.buttonAddPoint.clicked.connect(self.new_Point)
        self.buttonCreateObject = QPushButton("Criar objeto")
        self.buttonCreateObject.clicked.connect(self.new_Object)
        
        line_layout = QHBoxLayout()
        line_layout.addWidget(xx_label)
        line_layout.addWidget(self.xx)
        line_layout.addWidget(yy_label)
        line_layout.addWidget(self.yy)
        line = QWidget()
        line.setLayout(line_layout)

        layout = QVBoxLayout()
        layout.addWidget(line)
        layout.addWidget(self.buttonAddPoint)
        layout.addWidget(self.buttonCreateObject)
        self.setLayout(layout)
        self.setWindowTitle("Novo Objeto")
    
    @Slot()
    def new_Point(self):
        self.points.append(QPoint(int(self.xx.text()), int(self.yy.text())))
        self.xx.clear()
        self.yy.clear()
    
    @Slot()
    def new_Object(self):
        polygon = QPolygon(self.points)        
        scene.addPolygon(polygon)
 
        message = ("poligono criado em")
        for p in self.points:
            message += " (" +str(p.x())+ "," +str(p.y())+ ")"

        logging.info(message)

        self.close()
    
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

    # Viewport
    viewport = QGraphicsView(scene)
    viewport.setFixedSize(QSize(800,600))
    viewport.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
    viewport.setSceneRect(0,0, 780,580)


    object_list = QListWidget()
    for i in range(6):
        item = QListWidgetItem(f"Objeto {i}")
        item.setTextAlignment(Qt.AlignCenter)
        object_list.addItem(item)

    logTextBox = QTextEditLogger()
    logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(logTextBox)
    logging.getLogger().setLevel(logging.DEBUG)

    # Botão de criação de objetos
    create_object_button = QPushButton("Novo Objeto")
    create_object_button.clicked.connect(subWindows.open_NewObjectDialog)

    # Botões reerentes a função de zoom
    zoom_in_button = QPushButton("+")
    zoom_out_button = QPushButton("-")
    zoom_in_button.clicked.connect(functions.zoom_In)
    zoom_out_button.clicked.connect(functions.zoom_Out)

    # Botões referentes a função de navegação
    nav_left_button = QPushButton("left")
    nav_right_button = QPushButton("right")
    nav_up_button = QPushButton("up")
    nav_down_button = QPushButton("down")
    nav_left_button.clicked.connect(functions.nav_left)
    nav_right_button.clicked.connect(functions.nav_right)
    nav_up_button.clicked.connect(functions.nav_up)
    nav_down_button.clicked.connect(functions.nav_down)

    # Inicio dos layouts
    # Layout do menu dos objetos
    # Contém a lista de objetos e botão de criar objetos
    left_objects_layout = QVBoxLayout()    
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