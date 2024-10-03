import sys, logging
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from display_file import DisplayFile
from window import Window
from objects import WireFrame, Point
from objhandler import ObjHandler
from transform_functions import *
from clipping_functions import *

class QTextEditLogger(logging.Handler):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class NewObjectDialog(QWidget):
    def __init__(self, point_amount: int, normalized_matrix: numpy.ndarray):
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
        self.buttonCreateObject.clicked.connect(lambda : self.new_Object(point_amount, normalized_matrix))
        self.file_label = QLabel("Nome do arquivo")
        self.file_name = QLineEdit()
        self.file_open_button = QPushButton("Ler arquivo")
        self.file_open_button.clicked.connect(lambda: self.open_file(self.file_name.text(), normalized_matrix))
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
        
        if point_amount >= 3:
            self.type_label = QLabel("Tipo do Objeto")
            self.type_button_1 = QRadioButton("Arame")
            self.type_button_2 = QRadioButton("Preenchido")
            self.type_button_1.setChecked(True)
            self.type_button_layout = QHBoxLayout()
            self.type_button_layout.addWidget(self.type_label, 2)
            self.type_button_layout.addWidget(self.type_button_1, 1)
            self.type_button_layout.addWidget(self.type_button_2, 1)
            self.type_button_widget = QWidget()
            self.type_button_widget.setLayout(self.type_button_layout)
            self.layout.addWidget(self.type_button_widget)

        for n in range(point_amount):
            self.layout.addWidget(self.point_widget[n])

        self.layout.addWidget(self.buttonCreateObject)
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_name)
        self.layout.addWidget(self.file_open_button)
        self.setLayout(self.layout)
        self.setWindowTitle("Novo Objeto")
    
    @Slot()
    def new_Point(self, n: int) -> None:
        x = int(self.x_coord[n].text())
        y = int(self.y_coord[n].text())
        self.points.append(Point(x, y))
    
    @Slot()
    def new_Object(self, point_ammount: int, normalized_matrix: numpy.ndarray) -> None:
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
            obj = WireFrame(self.name_entry.text().upper(), self.points)
            obj.apply_normalized(normalized_matrix)
            screen.draw_object(obj)
            screen.update_objects_names()
            message = ("wireframe "+obj.get_name()+"<"
                       +obj.get_type()+"> criado em "
                       +obj.get_str_points())
            logging.info(message)
            self.close()

    @Slot()
    def open_file(self, file_name: str, normalized_matrix: numpy.ndarray) -> None:
        handler = ObjHandler()
        new_objects = handler.open_file(file_name)
        for obj in new_objects:
            obj.apply_normalized(normalized_matrix)
            screen.draw_object(obj)
            screen.update_objects_names()
            message = ("wireframe "+obj.get_name()+"<"
                       +obj.get_type()+"> criado em "
                       +obj.get_str_points())
            logging.info(message)
        self.close()
    

class SubWindows():
    def open_NewObjectDialog(self, point_amount: int, normalized_matrix: numpy.ndarray):
        self.new_window = NewObjectDialog(point_amount, normalized_matrix)
        self.new_window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.windows = Window(-380,-280,380,280, DisplayFile()) # Window
        self.subWindows = SubWindows() # Janelas Extras
        self.scene = QGraphicsScene() # Cenário
        self.scene.setBackgroundBrush(QColor('grey'))
        # self.scene.setSceneRect(0,0,800,600)
        self.viewport = QGraphicsView(self.scene) # Viewport
        self.viewport.setFixedSize(800,600)
        self.viewport.setMinimumHeight(0)
        self.viewport.setMinimumWidth(0)
        self.viewport.setMaximumHeight(600)
        self.viewport.setMaximumWidth(800)
        self.viewport.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.viewport.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pen = QPen()

        self.logTextBox = QTextEditLogger()# Interface de Log
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
        self.create_object_button.clicked.connect(lambda : self.subWindows.open_NewObjectDialog(self.create_object_point_amount.value(), self.windows.get_normalization_matrix()))

        # Interface de clipping
        self.clipping_button_1 = QRadioButton("Liang-Barsky")
        self.clipping_button_2 = QRadioButton("outro_metodo")
        self.clipping_button_1.setChecked(True)
        self.clipping_button_layout = QVBoxLayout()
        self.clipping_button_layout.addWidget(self.clipping_button_1)
        self.clipping_button_layout.addWidget(self.clipping_button_2)
        self.clipping_button_menu = QGroupBox("Clipping")
        self.clipping_button_menu.setLayout(self.clipping_button_layout)

        # SOMENTE PARA TESTES
        # self.scene.addRect(1000, 75, 600, 450)

        # Botões referentes a função de zoom
        self.zoom_in_button = QPushButton("+")
        self.zoom_out_button = QPushButton("-")
        self.zoom_in_button.clicked.connect(self.zoom_In)
        self.zoom_out_button.clicked.connect(self.zoom_Out)

        # Botões referentes a função de navegação
        self.nav_left_button = QPushButton("esquerda")
        self.nav_right_button = QPushButton("direita")
        self.nav_up_button = QPushButton("cima")
        self.nav_down_button = QPushButton("baixo")
        self.nav_center_button = QPushButton("centro")
        self.nav_left_button.clicked.connect(self.nav_left)
        self.nav_right_button.clicked.connect(self.nav_right)
        self.nav_up_button.clicked.connect(self.nav_up)
        self.nav_down_button.clicked.connect(self.nav_down)
        self.nav_center_button.clicked.connect(self.nav_center)

        # Botões das funções de transformação
        self.angle_label = QLabel("graus")
        self.angle_simbol_label = QLabel("°")
        self.point_x_label = QLabel("X")
        self.point_y_label = QLabel("Y")
        self.angle_entry = QLineEdit()
        self.point_x_entry = QLineEdit()
        self.point_y_entry = QLineEdit()
        self.translate_button = QPushButton("translação")
        self.schedule_button = QPushButton("escalonamento")
        self.rotate_world_button = QPushButton("mundo")
        self.rotate_object_button = QPushButton("objeto")
        self.rotate_point_button = QPushButton("ponto")
        self.rotate_window_button = QPushButton("janela")
        self.translate_button.clicked.connect(self.translate)
        self.schedule_button.clicked.connect(self.schedule)
        self.rotate_object_button.clicked.connect(self.rotate_object)
        self.rotate_world_button.clicked.connect(self.rotate_world)
        self.rotate_point_button.clicked.connect(self.rotate_point)
        self.rotate_window_button.clicked.connect(self.rotate_window)

        # partes do salvamento de arquivo
        self.file_name_label = QLabel("Nome do Arquivo")
        self.file_name_entry = QLineEdit()
        self.file_save_button = QPushButton("Salvar")
        self.file_save_button.clicked.connect(lambda : self.save_file(self.file_name_entry.text(), self.windows.get_display_file().get_objects()))

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

        self.rotate_layout = QGridLayout()
        self.rotate_layout.addWidget(self.rotate_world_button, 1, 1)
        self.rotate_layout.addWidget(self.rotate_object_button, 1, 2)
        self.rotate_layout.addWidget(self.rotate_point_button, 1, 3)
        self.rotate_layout.addWidget(self.rotate_window_button, 2, 1, 1, 3)
        self.rotate_menu = QGroupBox("Rotação")
        self.rotate_menu.setLayout(self.rotate_layout)

        self.left_transform_layout = QVBoxLayout()
        self.left_transform_layout.addWidget(self.entry_transform_menu)
        self.left_transform_layout.addWidget(self.left_schedule_translate_menu)
        self.left_transform_layout.addWidget(self.rotate_menu)
        self.left_transform_menu = QGroupBox("Transformações")
        self.left_transform_menu.setLayout(self.left_transform_layout)

        # Layout do menu de salvar em arquivo
        self.left_file_layout = QVBoxLayout()
        self.left_file_layout.addWidget(self.file_name_label)
        self.left_file_layout.addWidget(self.file_name_entry)
        self.left_file_layout.addWidget(self.file_save_button)
        self.left_file_menu = QGroupBox("Salvar em Arquivo")
        self.left_file_menu.setLayout(self.left_file_layout)

        # Layout do menu
        # Contém lista de objetos e funções de zoom e navegação
        self.left_menu_layout = QVBoxLayout()
        self.left_menu_layout.addWidget(self.clipping_button_menu)
        self.left_menu_layout.addWidget(self.left_objects_menu)
        self.left_menu_layout.addWidget(self.left_zoom_menu)
        self.left_menu_layout.addWidget(self.left_nav_menu)
        self.left_menu_layout.addWidget(self.left_transform_menu)
        self.left_menu_layout.addWidget(self.left_file_menu)
        self.left_menu = QGroupBox()
        self.left_menu.setLayout(self.left_menu_layout)

        # Layout do viewport
        # Contém a parte gráfica do viewport
        self.viewport_layout = QVBoxLayout()
        self.viewport_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.viewport_layout.addWidget(self.viewport)
        self.viewport_widget = QGroupBox("Viewport")
        # self.main_widget.setFixedSize(QSize(810, 610))
        self.viewport_widget.setLayout(self.viewport_layout)

        # Layout do log
        # Contém a parte textual do log
        self.log_layout = QVBoxLayout()
        self.log_layout.addWidget(self.logTextBox.widget)
        self.log_widget = QGroupBox("Logs")
        self.log_widget.setLayout(self.log_layout)

        # Log e Viewport
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.viewport_widget, 5)
        self.main_layout.addWidget(self.log_widget, 1)
        self.main_widget = QGroupBox()
        self.main_widget.setLayout(self.main_layout)

        # Janela principal
        # Contém interface de usuario e parte de log
        self.main_ui_layout = QHBoxLayout()
        self.main_ui_layout.addWidget(self.left_menu, 1)
        self.main_ui_layout.addWidget(self.main_widget, 3)
        self.main_ui = QWidget()    
        self.main_ui.setLayout(self.main_ui_layout)
        self.setWindowTitle("Computação Gráfica")
        self.setCentralWidget(self.main_ui)

        self.windows.update_normalization_matrix()
        self.draw_default_forms()
        self.zoom_Out()

        logging.info('programa iniciado')

    # Desenha as linhas x e y
    def draw_default_forms(self):

        line1 = WireFrame("line1",
                          [Point(-10000, self.windows.get_center().get_y()),
                           Point(10000, self.windows.get_center().get_y())])
        line1.apply_normalized(self.windows.get_normalization_matrix())
        line2 = WireFrame("line2",
                          [Point(self.windows.get_center().get_x(), -10000),
                           Point(self.windows.get_center().get_x(), 10000)])
        line2.apply_normalized(self.windows.get_normalization_matrix())
        self.pen.setWidth(1)
        self.pen.setColor(QColor("white"))
        self.scene.addRect(0, 0, 800, 600, self.pen)
        self.draw(line1)
        self.draw(line2)

    # Aumenta o zoom
    def zoom_In(self) -> None:
        if self.viewport.transform().m11() >= 10:
            logging.info('zoom máximo atingido')
        else:
            self.viewport.scale(1.1, 1.1)
            logging.info('zoom in de 10%')

    # Diminui o zoom
    def zoom_Out(self) -> None:
        if self.viewport.transform().m11() <= 0.1:
            logging.info('zoom mínimo atingido')
        else:
            self.viewport.scale(0.9, 0.9)
            logging.info('zoom out de 10%')

    # Navega para o centro
    def nav_center(self) -> None:
        shift = self.windows.get_shift()
        shift.set_x(0)
        shift.set_y(0)
        self.windows.update_normalization_matrix()
        self.redraw_objects()
        logging.info('window centralizada')

    # Navega para esquerda
    def nav_left(self) -> None:
        shift = self.windows.get_shift()
        shift.set_x(shift.get_x() - 20)
        self.windows.update_normalization_matrix()
        self.redraw_objects()
        logging.info('window deslocada para esquerda')

    # Navega para direita
    def nav_right(self) -> None:
        shift = self.windows.get_shift()
        shift.set_x(shift.get_x() + 20)
        self.windows.update_normalization_matrix()
        self.redraw_objects()
        logging.info('window deslocada para direita')

    # Navega para cima
    def nav_up(self) -> None:
        shift = self.windows.get_shift()
        shift.set_y(shift.get_y() + 15)
        self.windows.update_normalization_matrix()
        self.redraw_objects()
        logging.info('window deslocada para cima')

    # Navega para baixo
    def nav_down(self) -> None:
        shift = self.windows.get_shift()
        shift.set_y(shift.get_y() - 15)
        self.windows.update_normalization_matrix()
        self.redraw_objects()
        logging.info('window deslocada para baixo')

    # Atualiza a lista de objetos
    def update_objects_names(self) -> None:
        self.object_names.clear()
        for obj in self.windows.get_display_file().get_objects():
            self.object_names.addItem(QListWidgetItem(obj.get_name()))
    
    # Desenha um objeto
    def draw(self, obj: WireFrame):
        self.pen.setWidth(1)
        self.pen.setColor(QColor("white"))
        if obj.get_type() == '1':
            point = obj.get_normalized_points()[0]
            transformed_point = self.viewport_transform(point)
            self.scene.addLine(
                transformed_point.get_x(), transformed_point.get_y(),
                transformed_point.get_x(), transformed_point.get_y(), self.pen)
        elif obj.get_type() == '2':
            first_point = obj.get_normalized_points()[0]
            last_point = obj.get_normalized_points()[-1]
            # Clipagem Liang-Barsky
            if self.clipping_button_1.isChecked():
                visible, first_point, last_point = liang_barsky(first_point, last_point)
                if visible:
                    first_transformed_point = self.viewport_transform(first_point)
                    last_transformed_point = self.viewport_transform(last_point)
                    self.scene.addLine(
                        first_transformed_point.get_x(), first_transformed_point.get_y(),
                        last_transformed_point.get_x(), last_transformed_point.get_y(), self.pen)
            # Clipagem 
            else:
                first_transformed_point = self.viewport_transform(first_point)
                last_transformed_point = self.viewport_transform(last_point)
                self.scene.addLine(
                    first_transformed_point.get_x(), first_transformed_point.get_y(),
                    last_transformed_point.get_x(), last_transformed_point.get_y(), self.pen)
        else:
            first_point = obj.get_normalized_points()[0]
            last_point = obj.get_normalized_points()[-1]
            first_transformed_point = self.viewport_transform(first_point)
            last_transformed_point = self.viewport_transform(last_point)
            for i in range(len(obj.get_normalized_points())-1):
                f_point = obj.get_normalized_points()[i]
                l_point = obj.get_normalized_points()[i+1]
                f_transformed_point = self.viewport_transform(f_point)
                l_transformed_point = self.viewport_transform(l_point)
                self.scene.addLine(
                f_transformed_point.get_x(), f_transformed_point.get_y(),
                l_transformed_point.get_x(), l_transformed_point.get_y(), self.pen)
            self.scene.addLine(
                last_transformed_point.get_x(), last_transformed_point.get_y(),
                first_transformed_point.get_x(), first_transformed_point.get_y(), self.pen)
    
    # Desenha um objeto
    def draw_object(self, obj: WireFrame):
        self.draw(obj)
        self.windows.get_display_file().add_object(obj)

    # Transformada de viewport
    def viewport_transform(self, point: Point) -> Point:
        xvp = (point.get_x() - (-1))
        xvp = xvp / (1 - (-1))
        xvp = xvp * (self.viewport.maximumWidth() - self.viewport.minimumWidth())
        yvp = (point.get_y() - (-1))
        yvp = yvp / (1 - (-1))
        yvp = 1 - yvp
        yvp = yvp * (self.viewport.maximumHeight() - self.viewport.minimumHeight())
        transformed_point = Point(xvp, yvp)
        return transformed_point
    
    # Detecta objeto selecionado
    def selected_object(self) -> WireFrame:
        obj = self.windows.get_display_file().get_object(self.object_names.currentItem().text())
        logging.info('objeto selecionado:'+ obj.get_name() + " em " +obj.get_str_points())
        return obj
    
    # Redesenha todos os objetos
    def redraw_objects(self):
        self.scene.clear()
        self.windows.update_normalization_matrix()
        self.draw_default_forms()
        objects = self.windows.get_display_file().get_objects()
        for obj in objects:
            obj.clear_normalized_points()
            obj.apply_normalized(self.windows.get_normalization_matrix())
            self.draw(obj)

    # Translada um objeto
    def translate(self):
        if self.object_names.currentItem() == None:
            logging.info("selecione um objeto")
        else:
            obj = self.selected_object()
            translate_point = Point(int(self.point_x_entry.text()), int(self.point_y_entry.text()))
            for point in obj.get_points():
                point.set_x(point.get_x() + translate_point.get_x())
                point.set_y(point.get_y() + translate_point.get_y())
            self.redraw_objects()
            logging.info("objeto" + obj.get_name() +
                         "transladado em (" +str(translate_point.get_x())+","+str(translate_point.get_y())+")")

    # Escalona um objeto
    def schedule(self):
        if self.object_names.currentItem() == None:
            logging.info("selecione um objeto")
        else:
            obj = self.selected_object()
            point = Point(float(self.point_x_entry.text()), float(self.point_y_entry.text()))
            matrix = transform_scaling(point.get_x(), point.get_y(), obj.get_center())
            obj.update_transform(matrix)
            obj.apply_transform()
            obj.reset_transform()
            self.redraw_objects()
            logging.info("objeto" + obj.get_name() +
                         "escalonado em (" +str(point.get_x())+","+str(point.get_y())+")")

    # Rotaciona um objeto pelo seu centro
    def rotate_object(self):
        if self.object_names.currentItem() == None:
            logging.info("selecione um objeto")
        else:
            obj = self.selected_object()
            angle = float(self.angle_entry.text())
            matrix = transform_rotation(-angle, obj.get_center())
            obj.update_transform(matrix)
            obj.apply_transform()
            obj.reset_transform()
            self.redraw_objects()
            logging.info("objeto" + obj.get_name() +
                         "rotacionado a partir do centro do objeto")

    # Rotaciona um objeto pelo centro do mundo
    def rotate_world(self):
        if self.object_names.currentItem() == None:
            logging.info("selecione um objeto")
        else:
            obj = self.selected_object()
            angle = float(self.angle_entry.text())
            matrix = transform_rotation(-angle, Point(0,0))
            obj.update_transform(matrix)
            obj.apply_transform()
            obj.reset_transform()
            self.redraw_objects()
            logging.info("objeto" + obj.get_name() +
                         "rotacionado a partir do centro do mundo")

    # Rotaciona um objeto pelo ponto dado
    def rotate_point(self):
        pivot_x = int(self.point_x_entry.text())
        pivot_y = int(self.point_y_entry.text())
        pivot = Point(pivot_x,pivot_y) 
        if self.object_names.currentItem() == None:
            logging.info("selecione um objeto")
        else:
            obj = self.selected_object()
            angle = float(self.angle_entry.text())
            matrix = transform_rotation(-angle, pivot)
            obj.update_transform(matrix)
            obj.apply_transform()
            obj.reset_transform()
            self.redraw_objects()
            logging.info("objeto" + obj.get_name() +
                         "rotacionado a partir do ponto (" +str(pivot_x)+","+str(pivot_y)+")")

    # Rotaciona a janela
    def rotate_window(self):
        angle = float(self.angle_entry.text())
        self.windows.set_angle(angle)
        self.windows.update_normalization_matrix()
        self.redraw_objects()
        logging.info('window rotacionada')

    # Salva o arquivo de objetos
    def save_file(self, file_name: str, objects: list[WireFrame]):
        handler = ObjHandler()
        handler.save_file(file_name, objects)
        logging.info("arquivo " + file_name + " criado")
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = MainWindow()
    screen.show()
    sys.exit(app.exec())