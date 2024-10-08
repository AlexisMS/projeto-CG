import sys, logging
from object import WireFrame
from PySide6.QtCore import Qt, QSize, QPoint, QLine, Slot, QRect, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QListWidget, QListWidgetItem, QLabel, QGroupBox, QGraphicsScene, QGraphicsView, QPlainTextEdit, QMainWindow, QLineEdit, QSpinBox


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

        self.buttonCreateObject = QPushButton("Criar objeto")
        self.buttonCreateObject.clicked.connect(lambda : self.new_Object(point_amount))
        
        self.point_layout = []
        self.point_widget = []
        for n in range(point_amount):
            self.point_layout.append(QHBoxLayout())
            self.point_layout[n].addWidget(self.x_label[n])
            self.point_layout[n].addWidget(self.x_coord[n])
            self.point_layout[n].addWidget(self.y_label[n])
            self.point_layout[n].addWidget(self.y_coord[n])
            self.point_widget.append(QWidget())
            self.point_widget[n].setLayout(self.point_layout[n])

        self.name_label = QLabel("Nome do Objeto")
        self.name_entry = QLineEdit()
        self.name_layout = QHBoxLayout()
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_entry)
        self.name_widget = QWidget()
        self.name_widget.setLayout(self.name_layout)

        # Configura o layout
        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.name_widget)

        for n in range(point_amount):
            self.layout.addWidget(self.point_widget[n])

        self.layout.addWidget(self.buttonCreateObject)
        self.setLayout(self.layout)
        self.setWindowTitle("Novo Objeto")
    
    @Slot()
    def new_Point(self, n):
        self.points.append(QPoint(int(self.x_coord[n].text()), int(self.y_coord[n].text())))
    
    @Slot()
    def new_Object(self, point_ammount):
        # Checa se há valor vazio em alguma coordenada submetida
        empty_coord = False
        for i in range(len(self.x_coord)):
            if self.x_coord[i].text() == "" or self.y_coord[i].text() == "":
                empty_coord = True
                break

        # Cancela criação de objetos se não cumprir algum requisito
        if self.name_entry.text() == "" or empty_coord:
            logging.info("wireframe não criado: campos precisam ser preenchidos")
            self.close()
        else:
            for n in range(point_ammount):
                self.new_Point(n)

            wireframe_object = WireFrame(self.name_entry.text().upper(), self.points)
            display_file.append(wireframe_object)
            
            item = QListWidgetItem(wireframe_object.get_name())
            object_list.addItem(item)

            window.update_plot()

            message = ("wireframe "+wireframe_object.get_name()+"<"
                       +wireframe_object.get_type()+"> criado em "
                       +wireframe_object.get_str_points())
            
            logging.info(message)
            self.close()
    
class SubWindows():
    def open_NewObjectDialog(self, point_amount):
        self.new_window = NewObjectDialog(point_amount)
        self.new_window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor('grey'))

        self.subWindows = SubWindows()
        
        # Viewport
        self.viewport = QGraphicsView(self.scene)
        self.viewport.setFixedSize(QSize(800,600))
        self.viewport.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)        
        self.scene.setSceneRect(0,0,780,580)

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_plot)
        # self.timer.start(2000)

        self.logTextBox = QTextEditLogger()
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

        # Interface para iniciar criação de objetos
        self.create_object_point_amount_label = QLabel("Número de pontos:")
        self.create_object_point_amount = QSpinBox()
        self.create_object_point_amount.setMinimum(1)
        self.create_object_point_amount_layout = QHBoxLayout()
        self.create_object_point_amount_layout.addWidget(self.create_object_point_amount_label)
        self.create_object_point_amount_layout.addWidget(self.create_object_point_amount)
        self.create_object_point_amount_widget = QWidget()
        self.create_object_point_amount_widget.setLayout(self.create_object_point_amount_layout)
        self.create_object_button = QPushButton("Novo Objeto")
        self.create_object_button.clicked.connect(lambda : self.subWindows.open_NewObjectDialog(self.create_object_point_amount.value()))

        # SOMENTE PARA TESTES
        #self.scene.addLine(QLine(100, 200, 300, 200))

        # Botões referentes a função de zoom
        self.zoom_in_button = QPushButton("+")
        self.zoom_out_button = QPushButton("-")
        self.zoom_in_button.clicked.connect(self.zoom_In)
        self.zoom_out_button.clicked.connect(self.zoom_Out)

        # Botões referentes a função de navegação
        self.nav_left_button = QPushButton("left")
        self.nav_right_button = QPushButton("right")
        self.nav_up_button = QPushButton("up")
        self.nav_down_button = QPushButton("down")
        self.nav_left_button.clicked.connect(self.nav_left)
        self.nav_right_button.clicked.connect(self.nav_right)
        self.nav_up_button.clicked.connect(self.nav_up)
        self.nav_down_button.clicked.connect(self.nav_down)

        # Inicio dos layouts
        # Layout do menu dos objetos
        # Contém a lista de objetos e botão de criar objetos
        self.left_objects_layout = QVBoxLayout()  
        self.left_objects_layout.addWidget(self.create_object_point_amount_widget)  
        self.left_objects_layout.addWidget(self.create_object_button)
        self.left_objects_layout.addWidget(object_list)
        self.left_objects_menu = QGroupBox("Objetos")
        self.left_objects_menu.setLayout(self.left_objects_layout)

        # Layout do menu de zooms
        # Contém todos os botões de zoom
        self.left_zoom_layout = QHBoxLayout()
        self.left_zoom_layout.addWidget(self.zoom_in_button)
        self.left_zoom_layout.addWidget(self.zoom_out_button)
        self.left_zoom_menu = QGroupBox("Zoom")
        self.left_zoom_menu.setLayout(self.left_zoom_layout)

        # Layout do menu de navegação
        # Contém todos os botões de navegação
        self.left_nav_layout = QGridLayout()
        self.left_nav_layout.addWidget(self.nav_up_button, 1, 2)
        self.left_nav_layout.addWidget(self.nav_left_button, 2, 1)
        self.left_nav_layout.addWidget(self.nav_right_button, 2, 3)
        self.left_nav_layout.addWidget(self.nav_down_button, 3, 2)
        self.left_nav_menu = QGroupBox("Navegação")
        self.left_nav_menu.setLayout(self.left_nav_layout)

        # Layout do menu
        # Contém lista de objetos e funções de zoom e navegação
        self.left_menu_layout = QVBoxLayout()
        self.left_menu_layout.addWidget(self.left_objects_menu)
        self.left_menu_layout.addWidget(self.left_zoom_menu)
        self.left_menu_layout.addWidget(self.left_nav_menu)
        self.left_menu = QGroupBox()
        self.left_menu.setLayout(self.left_menu_layout)

        # Layout do viewport
        # Contém a parte gráfica do viewport
        self.viewport_layout = QVBoxLayout()
        self.viewport_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.viewport_layout.addWidget(self.viewport)
        self.main_widget = QGroupBox("Viewport")
        self.main_widget.setLayout(self.viewport_layout)

        # Layout do log
        # Contém a paret textual do log
        self.log_layout = QVBoxLayout()
        self.log_layout.addWidget(self.logTextBox.widget)
        self.log_widget = QGroupBox("Logs")
        self.log_widget.setLayout(self.log_layout)

        # Layout da interface de usuario
        # Contém o menu de funções e objetos 
        self.main_ui_layout = QHBoxLayout()
        self.main_ui_layout.addWidget(self.left_menu, 1)
        self.main_ui_layout.addWidget(self.main_widget, 3)
        self.main_ui = QWidget()    
        self.main_ui.setLayout(self.main_ui_layout)

        # Janela principal
        # Contém interface de usuario e parte de log
        self.window_layout = QVBoxLayout()
        self.window_layout.addWidget(self.main_ui, 10)
        self.window_layout.addWidget(self.log_widget, 1)
        self.window_ui = QWidget()
        self.window_ui.setLayout(self.window_layout)

        self.setWindowTitle("Computação Gráfica")
        self.setCentralWidget(self.window_ui)
        
        logging.info('programa iniciado')

    def zoom_In(self):
        self.viewport.scale(1.1, 1.1)
        logging.info('zoom in de 10%')

    def zoom_Out(self):
        self.viewport.scale(1/1.1, 1/1.1)
        logging.info('zoom out de 10%')

    def nav_left(self):
        current_rect = self.scene.sceneRect()
        self.scene.setSceneRect(QRect(current_rect.x()+20, current_rect.y(), 
                                      current_rect.width()+20, current_rect.height()))
        logging.info('window deslocada')

    def nav_right(self):
        current_rect = self.scene.sceneRect()
        self.scene.setSceneRect(QRect(current_rect.x()-20, current_rect.y(), 
                                      current_rect.width()-20, current_rect.height()))
        logging.info('window deslocada')

    def nav_up(self):
        current_rect = self.scene.sceneRect()
        self.scene.setSceneRect(QRect(current_rect.x(), current_rect.y()+20, 
                                      current_rect.width(), current_rect.height()+20))
        logging.info('window deslocada')

    def nav_down(self):
        current_rect = self.scene.sceneRect()
        self.scene.setSceneRect(QRect(current_rect.x(), current_rect.y()-20, 
                                      current_rect.width(), current_rect.height()-20))
        logging.info('window deslocada')

    def update_plot(self):
        # Não atualiza se display_file for vazio
        if len(display_file) != 0:
            self.scene.clear()
            for w in display_file:
                points = w.get_points()
                
                if len(points) == 1:
                    # transformed_points = self.viewport_transform(points[0])
                    # self.scene.addLine(transformed_points[0], transformed_points[1],
                    #                    transformed_points[0], transformed_points[1])
                    self.scene.addLine(points[0].x(), self.scene.height() - points[0].y(),
                                       points[0].x(), self.scene.height() - points[0].y())
                else:
                    for i in range(len(points)-1):
                        # f_transformed_points = self.viewport_transform(points[i])
                        # l_transformed_points = self.viewport_transform(points[i+1])
                        # self.scene.addLine(f_transformed_points[0], f_transformed_points[1],
                        #                 l_transformed_points[0], l_transformed_points[1])
                        self.scene.addLine(points[i].x(), self.scene.height() - points[i].y(),
                                       points[i+1].x(), self.scene.height() - points[i+1].y())

    def viewport_transform(self, point):
        xvp = ((point.x() - self.scene.sceneRect().left())
                /(self.scene.sceneRect().right() - self.scene.sceneRect().left())
                *(self.viewport.width() - self.viewport.x()))
        yvp = (1 - ((point.y() - self.scene.sceneRect().top())
                /(self.scene.sceneRect().bottom() - self.scene.sceneRect().top()))
                *(self.viewport.height() - self.viewport.y()))
        return (xvp, yvp)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    object_list = QListWidget()
    display_file = []
    window = MainWindow()
    window.show()
    sys.exit(app.exec())