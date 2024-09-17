import sys, logging
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.Qt import *

from display_file import DisplayFile
from window import Window
from objects import WireFrame, Point

class QTextEditLogger(logging.Handler):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class NewObjectDialog(QWidget):
    def __init__(self, point_amount: int):
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
    def new_Point(self, n: int) -> None:
        x = int(self.x_coord[n].text())
        y = int(self.y_coord[n].text())
        self.points.append(Point(x, y))
    
    @Slot()
    def new_Object(self, point_ammount: int) -> None:
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

            object = WireFrame(self.name_entry.text().upper(), self.points)
            window.get_display_file().add_object(object)

            screen.update_objects_names()
            screen.update_plot()

            message = ("wireframe "+object.get_name()+"<"
                       +object.get_type()+"> criado em "
                       +object.get_str_points())
            
            logging.info(message)
            self.close()
    

class SubWindows():
    def open_NewObjectDialog(self, point_amount: int):
        self.new_window = NewObjectDialog(point_amount)
        self.new_window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Janelas Extras
        self.subWindows = SubWindows()

        # Cenário
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor('grey'))

        # Viewport
        self.viewport = QGraphicsView(self.scene)
        # self.viewport.setFixedSize(QSize(800,600))
        self.viewport.centerOn(window.get_center().get_x(), window.get_center().get_y())
        self.viewport.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.viewport.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pen = QPen()

        # Interface de Log
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
        # self.scene.addRect(1000, 75, 600, 450)

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
        self.nav_center_button = QPushButton("center")
        self.nav_left_button.clicked.connect(self.nav_left)
        self.nav_right_button.clicked.connect(self.nav_right)
        self.nav_up_button.clicked.connect(self.nav_up)
        self.nav_down_button.clicked.connect(self.nav_down)
        self.nav_center_button.clicked.connect(self.nav_center)

        # Botões das funções de transformação
        self.angle_label = QLabel("degrees")
        self.angle_simbol_label = QLabel("°")
        self.point_x_label = QLabel("X")
        self.point_y_label = QLabel("Y")
        self.angle_entry = QLineEdit()
        self.point_x_entry = QLineEdit()
        self.point_y_entry = QLineEdit()
        self.translate_button = QPushButton("translate")
        self.schedule_button = QPushButton("schedule")
        self.rotate_world_button = QPushButton("world")
        self.rotate_object_button = QPushButton("object")
        self.rotate_point_button = QPushButton("point")

        # Inicio dos layouts
        # Layout do menu dos objetos
        # Contém a lista de objetos e botão de criar objetos
        self.object_names = QListWidget()
        self.left_objects_layout = QVBoxLayout()  
        self.left_objects_layout.addWidget(self.create_object_point_amount_widget)  
        self.left_objects_layout.addWidget(self.create_object_button)
        self.left_objects_layout.addWidget(self.object_names)
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
        self.left_nav_layout.addWidget(self.nav_center_button, 2, 2)
        self.left_nav_menu = QGroupBox("Navegação")
        self.left_nav_menu.setLayout(self.left_nav_layout)

        # Layout do menu de transformações
        # Contém todos os widgets de transformações
        self.point_layout = QGridLayout()
        self.point_layout.addWidget(self.point_x_label, 1, 1)
        self.point_layout.addWidget(self.point_x_entry, 2, 1)
        self.point_layout.addWidget(self.point_y_label, 1, 2)
        self.point_layout.addWidget(self.point_y_entry, 2, 2)
        self.point_menu = QGroupBox("Ponto")
        self.point_menu.setLayout(self.point_layout)

        self.angle_layout = QGridLayout()
        self.angle_layout.addWidget(self.angle_label, 1,1)
        self.angle_layout.addWidget(self.angle_entry,2,1)
        self.angle_layout.addWidget(self.angle_simbol_label,2,2)
        self.angle_menu = QGroupBox("Ângulo")
        self.angle_menu.setLayout(self.angle_layout)

        self.entry_transform_layout = QHBoxLayout()
        self.entry_transform_layout.addWidget(self.point_menu)
        self.entry_transform_layout.addWidget(self.angle_menu)
        self.entry_transform_menu = QWidget()
        self.entry_transform_menu.setLayout(self.entry_transform_layout)

        self.left_schedule_translate_layout = QHBoxLayout()
        self.left_schedule_translate_layout.addWidget(self.translate_button)
        self.left_schedule_translate_layout.addWidget(self.schedule_button)
        self.left_schedule_translate_menu = QGroupBox("Deslocamento")
        self.left_schedule_translate_menu.setLayout(self.left_schedule_translate_layout)

        self.rotate_layout = QHBoxLayout()
        self.rotate_layout.addWidget(self.rotate_world_button)
        self.rotate_layout.addWidget(self.rotate_object_button)
        self.rotate_layout.addWidget(self.rotate_point_button)
        self.rotate_menu = QGroupBox("Rotação")
        self.rotate_menu.setLayout(self.rotate_layout)

        self.left_transform_layout = QVBoxLayout()
        self.left_transform_layout.addWidget(self.entry_transform_menu)
        self.left_transform_layout.addWidget(self.left_schedule_translate_menu)
        self.left_transform_layout.addWidget(self.rotate_menu)
        self.left_transform_menu = QGroupBox("Transformações")
        self.left_transform_menu.setLayout(self.left_transform_layout)

        # Layout do menu
        # Contém lista de objetos e funções de zoom e navegação
        self.left_menu_layout = QVBoxLayout()
        self.left_menu_layout.addWidget(self.left_objects_menu)
        self.left_menu_layout.addWidget(self.left_zoom_menu)
        self.left_menu_layout.addWidget(self.left_nav_menu)
        self.left_menu_layout.addWidget(self.left_transform_menu)
        self.left_menu = QGroupBox()
        self.left_menu.setLayout(self.left_menu_layout)

        # Layout do viewport
        # Contém a parte gráfica do viewport
        self.viewport_layout = QVBoxLayout()
        self.viewport_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.viewport_layout.addWidget(self.viewport)
        self.main_widget = QGroupBox("Viewport")
        self.main_widget.setFixedSize(QSize(800, 800))
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

        self.draw_lines_coords()
        
        logging.info('programa iniciado')

    def draw_lines_coords(self):
        self.pen.setWidth(2)
        self.pen.setColor(QColor("black"))
        self.pen_coords = QPen()
        self.scene.addLine(-10000, window.get_center().get_y(), 10000, window.get_center().get_y(), self.pen)
        self.scene.addLine(window.get_center().get_x(), -10000, window.get_center().get_x(), 10000, self.pen)

    def zoom_In(self) -> None:
        if self.viewport.transform().m11() >= 10:
            logging.info('zoom máximo atingido')
        else:
            self.viewport.scale(1.1, 1.1)
            logging.info('zoom in de 10%')

    def zoom_Out(self) -> None:
        if self.viewport.transform().m11() <= 0.1:
            logging.info('zoom mínimo atingido')
        else:
            self.viewport.scale(0.9, 0.9)
            logging.info('zoom out de 10%')

    def nav_center(self) -> None:
        shift = window.get_shift()
        window.set_xmax(window.get_xmax() - shift.get_x())
        window.set_xmin(window.get_xmin() - shift.get_x())
        window.set_ymax(window.get_ymax() - shift.get_y())
        window.set_ymin(window.get_ymin() - shift.get_y())
        shift.set_x(0)
        shift.set_y(0)
        window.update_center()

        self.viewport.centerOn(window.get_center().get_x(), window.get_center().get_y())

        logging.info('window deslocada')

    def nav_left(self) -> None:
        window.set_xmax(window.get_xmax() + 20)
        window.set_xmin(window.get_xmin() + 20)
        shift = window.get_shift()
        shift.set_x(shift.get_x() + 20)
        window.update_center()

        self.viewport.centerOn(window.get_center().get_x(), window.get_center().get_y())

        logging.info('window deslocada')

    def nav_right(self) -> None:
        window.set_xmax(window.get_xmax() - 20)
        window.set_xmin(window.get_xmin() - 20)
        shift = window.get_shift()
        shift.set_x(shift.get_x() - 20)
        window.update_center()

        self.viewport.centerOn(window.get_center().get_x(), window.get_center().get_y())

        logging.info('window deslocada')

    def nav_up(self) -> None:
        window.set_ymax(window.get_ymax() + 15)
        window.set_ymin(window.get_ymin() + 15)
        shift = window.get_shift()
        shift.set_y(shift.get_y() + 15)
        window.update_center()

        self.viewport.centerOn(window.get_center().get_x(), window.get_center().get_y())

        logging.info('window deslocada')

    def nav_down(self) -> None:
        window.set_ymax(window.get_ymax() - 15)
        window.set_ymin(window.get_ymin() - 15)
        shift = window.get_shift()
        shift.set_y(shift.get_y() - 15)
        window.update_center()

        self.viewport.centerOn(window.get_center().get_x(), window.get_center().get_y())

        logging.info('window deslocada')

    def update_objects_names(self) -> None:
        self.object_names.clear()
        for obj in window.get_display_file().get_objects():
            self.object_names.addItem(QListWidgetItem(obj.get_name()))

    def update_plot(self) -> None:
        self.scene.clear()
        for object in window.get_display_file().get_objects():
            points = object.get_points()
            if len(points) == 1:
                transformed_point = self.viewport_transform(points[0])
                self.scene.addLine(transformed_point.get_x(), transformed_point.get_y(),
                                   transformed_point.get_x(), transformed_point.get_y())
                # self.scene.addLine(points[0].get_x(), self.scene.height() - points[0].get_y(),
                #                     points[0].get_x(), self.scene.height() - points[0].get_y())
            else:
                for i in range(len(points)-1):
                    first_transformed_point = self.viewport_transform(points[i])
                    last_transformed_point = self.viewport_transform(points[i+1])
                    self.scene.addLine(first_transformed_point.get_x(), first_transformed_point.get_y(),
                                    last_transformed_point.get_x(), last_transformed_point.get_y())
                    # self.scene.addLine(points[i].get_x(), self.scene.height() - points[i].get_y(),
                    #                 points[i+1].get_x(), self.scene.height() - points[i+1].get_y())

    def viewport_transform(self, point: Point) -> Point:
        xvp = (point.get_x() - window.get_xmin())
        xvp = xvp / (window.get_xmax() - window.get_xmin())
        xvp = xvp * (self.viewport.sceneRect().right() - self.viewport.sceneRect().left())
        
        yvp = (point.get_y() - window.get_ymin())
        yvp = yvp / (window.get_ymax() - window.get_ymin())
        yvp = 1 - yvp
        yvp = yvp * (self.viewport.sceneRect().bottom() - self.viewport.sceneRect().top())
        
        transformed_point = Point(xvp, yvp)

        return transformed_point
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window(-400,-300,400,300, DisplayFile())
    
    screen = MainWindow()
    screen.show()

    sys.exit(app.exec())