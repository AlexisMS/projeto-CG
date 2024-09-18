import sys, logging, math
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
#from PySide6.Qt import *

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

            obj = WireFrame(self.name_entry.text().upper(), self.points)
            
            # self.windows.get_display_file().add_object(obj)
            screen.draw_object(obj)
            screen.update_objects_names()

            message = ("wireframe "+obj.get_name()+"<"
                       +obj.get_type()+"> criado em "
                       +obj.get_str_points())
            
            logging.info(message)
            self.close()
    

class SubWindows():
    def open_NewObjectDialog(self, point_amount: int):
        self.new_window = NewObjectDialog(point_amount)
        self.new_window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cria window
        self.windows = Window(-400,-300,400,300, DisplayFile())

        # Janelas Extras
        self.subWindows = SubWindows()

        # Cenário
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor('grey'))
        self.scene.setSceneRect(0,-0,800,600)

        # Viewport
        self.viewport = QGraphicsView(self.scene)
        # self.viewport.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.viewport.setFixedSize(800, 600)
        self.viewport.setMinimumHeight(0)
        self.viewport.setMinimumWidth(0)
        self.viewport.setMaximumHeight(600)
        self.viewport.setMaximumWidth(800)
        # self.viewport.centerOn(self.windows.get_center().get_x(), self.windows.get_center().get_y())
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
        self.translate_button.clicked.connect(self.translate)
        self.schedule_button.clicked.connect(self.schedule)
        self.rotate_object_button.clicked.connect(self.rotate_object)
        self.rotate_world_button.clicked.connect(self.rotate_world)
        self.rotate_point_button.clicked.connect(self.rotate_point)

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
        # self.main_widget.setFixedSize(QSize(810, 610))
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
        self.windows_layout = QVBoxLayout()
        self.windows_layout.addWidget(self.main_ui, 10)
        self.windows_layout.addWidget(self.log_widget, 1)
        self.windows_ui = QWidget()
        self.windows_ui.setLayout(self.windows_layout)

        self.setWindowTitle("Computação Gráfica")
        self.setCentralWidget(self.windows_ui)

        self.draw_lines_coords()
        
        print(self.viewport.minimumWidth(), self.viewport.maximumWidth())
        print(self.viewport.minimumHeight(), self.viewport.maximumHeight())
        print(self.windows.get_xmin(), self.windows.get_ymin())
        print(self.windows.get_xmax(), self.windows.get_ymax())

        logging.info('programa iniciado')

    def draw_lines_coords(self):
        self.pen.setWidth(2)
        self.pen.setColor(QColor("black"))
        x1 = self.viewport_transform(Point(-10000, self.windows.get_center().get_y()))
        x2 = self.viewport_transform(Point(10000, self.windows.get_center().get_y()))

        y1 = self.viewport_transform(Point(self.windows.get_center().get_x(), -10000))
        y2 = self.viewport_transform(Point(self.windows.get_center().get_x(), 10000))

        self.scene.addLine(x1.get_x(), x1.get_y(), x2.get_x(), x2.get_y(), self.pen)
        self.scene.addLine(y1.get_x(), y1.get_y(), y2.get_x(), y2.get_y(), self.pen)

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
        shift = self.windows.get_shift()
        self.windows.set_xmax(self.windows.get_xmax() - shift.get_x())
        self.windows.set_xmin(self.windows.get_xmin() - shift.get_x())
        self.windows.set_ymax(self.windows.get_ymax() - shift.get_y())
        self.windows.set_ymin(self.windows.get_ymin() - shift.get_y())
        shift.set_x(0)
        shift.set_y(0)
        self.windows.update_center()
        
        self.viewport.setSceneRect(0, 0, 800, 600)
        # self.viewport.centerOn(self.windows.get_center().get_x(), self.windows.get_center().get_y())

        logging.info('window centralizada')

    def nav_left(self) -> None:
        self.windows.set_xmax(self.windows.get_xmax() + 20)
        self.windows.set_xmin(self.windows.get_xmin() + 20)
        shift = self.windows.get_shift()
        shift.set_x(shift.get_x() + 20)
        self.windows.update_center()

        rect = self.viewport.sceneRect()
        self.viewport.setSceneRect(rect.left()+20, rect.top(), 800, 600)
        # self.viewport.centerOn(self.windows.get_center().get_x(), self.windows.get_center().get_y())

        logging.info('window deslocada')

    def nav_right(self) -> None:
        self.windows.set_xmax(self.windows.get_xmax() - 20)
        self.windows.set_xmin(self.windows.get_xmin() - 20)
        shift = self.windows.get_shift()
        shift.set_x(shift.get_x() - 20)
        self.windows.update_center()

        rect = self.viewport.sceneRect()
        self.viewport.setSceneRect(rect.left()-20, rect.top(), 800, 600)
        # self.viewport.centerOn(self.windows.get_center().get_x(), self.windows.get_center().get_y())

        logging.info('window deslocada')

    def nav_up(self) -> None:
        self.windows.set_ymax(self.windows.get_ymax() + 15)
        self.windows.set_ymin(self.windows.get_ymin() + 15)
        shift = self.windows.get_shift()
        shift.set_y(shift.get_y() + 15)
        self.windows.update_center()

        rect = self.viewport.sceneRect()
        self.viewport.setSceneRect(rect.left(), rect.top()+15, 800, 600)
        # self.viewport.centerOn(self.windows.get_center().get_x(), self.windows.get_center().get_y())

        logging.info('window deslocada')

    def nav_down(self) -> None:
        self.windows.set_ymax(self.windows.get_ymax() - 15)
        self.windows.set_ymin(self.windows.get_ymin() - 15)
        shift = self.windows.get_shift()
        shift.set_y(shift.get_y() - 15)
        self.windows.update_center()

        rect = self.viewport.sceneRect()
        self.viewport.setSceneRect(rect.left(), rect.top()-15, 800, 600)
        # self.viewport.centerOn(self.windows.get_center().get_x(), self.windows.get_center().get_y())

        logging.info('window deslocada')

    def update_objects_names(self) -> None:
        self.object_names.clear()
        for obj in self.windows.get_display_file().get_objects():
            self.object_names.addItem(QListWidgetItem(obj.get_name()))

    def draw(self, obj: WireFrame):
        self.pen.setWidth(1)
        self.pen.setColor(QColor("white"))

        if obj.get_type() == 1:
            point = obj.get_points()[0]
            
            transformed_point = self.viewport_transform(point)

            self.scene.addLine(
                transformed_point.get_x(), transformed_point.get_y(),
                transformed_point.get_x(), transformed_point.get_y(), self.pen)
            
        elif obj.get_type() == 2:
            first_point = obj.get_points()[0]
            last_point = obj.get_points()[-1]

            first_transformed_point = self.viewport_transform(first_point)
            last_transformed_point = self.viewport_transform(last_point)

            self.scene.addLine(
                first_transformed_point.get_x(), first_transformed_point.get_y(),
                last_transformed_point.get_x(), last_transformed_point.get_y(), self.pen)
            
        else:
            first_point = obj.get_points()[0]
            last_point = obj.get_points()[-1]

            first_transformed_point = self.viewport_transform(first_point)
            last_transformed_point = self.viewport_transform(last_point)
            
            for i in range(len(obj.get_points())-1):
                f_point = obj.get_points()[i]
                l_point = obj.get_points()[i+1]

                f_transformed_point = self.viewport_transform(f_point)
                l_transformed_point = self.viewport_transform(l_point)

                self.scene.addLine(
                f_transformed_point.get_x(), f_transformed_point.get_y(),
                l_transformed_point.get_x(), l_transformed_point.get_y(), self.pen)

            self.scene.addLine(
                last_transformed_point.get_x(), last_transformed_point.get_y(),
                first_transformed_point.get_x(), first_transformed_point.get_y(), self.pen)
            
    def draw_object(self, obj: WireFrame):
        self.draw(obj)
        self.windows.get_display_file().add_object(obj)

    def viewport_transform(self, point: Point) -> Point:
        xvp = (point.get_x() - self.windows.get_xmin())
        xvp = xvp / (self.windows.get_xmax() - self.windows.get_xmin())
        xvp = xvp * (self.viewport.maximumWidth() - self.viewport.minimumWidth())
        
        yvp = (point.get_y() - self.windows.get_ymin())
        yvp = yvp / (self.windows.get_ymax() - self.windows.get_ymin())
        yvp = 1 - yvp
        yvp = yvp * (self.viewport.maximumHeight() - self.viewport.minimumHeight())
        
        transformed_point = Point(xvp, yvp)

        return transformed_point
    
    def selected_object(self) -> WireFrame:
        obj = self.windows.get_display_file().get_object(self.object_names.currentItem().text())
        logging.info('objeto selecionado:'+ obj.get_name() + " em " +obj.get_str_points())
        return obj
    
    def redraw_objects(self):
        self.scene.clear()
        self.draw_lines_coords()
        objects = self.windows.get_display_file().get_objects()
        for obj in objects:
            self.draw(obj)

    def translate(self):
        if self.object_names.currentItem() == None:
            logging.info("selecione um objeto")
        else:
            obj = self.selected_object()
            print(type(obj))
            translate_point = Point(int(self.point_x_entry.text()), int(self.point_y_entry.text()))
            for point in obj.get_points():
                point.set_x(point.get_x() + translate_point.get_x())
                point.set_y(point.get_y() + translate_point.get_y())
            self.redraw_objects()
            logging.info("translação de (" + str(translate_point.get_x()) + "," + str(translate_point.get_y()) + ") aplicada")
            logging.info("objeto transladado " + obj.get_name() +  " em " + obj.get_str_points())

    def schedule(self):
        if self.object_names.currentItem() == None:
            logging.info("selecione um objeto")
        else:
            obj = self.selected_object()
            point = Point(int(self.point_x_entry.text()), int(self.point_y_entry.text()))
            obj.transform_scaling(point.get_x(), point.get_y())
            obj.apply_transform()
            obj.reset_transform()
            self.redraw_objects()

    def rotate_object(self):
        if self.object_names.currentItem() == None:
            logging.info("selecione um objeto")
        else:
            obj = self.selected_object()
            angle = float(self.angle_entry.text())
            obj.transform_basic_rotation(angle)
            obj.apply_transform()
            obj.reset_transform()
            self.redraw_objects()

    def rotate_world(self):
        if self.object_names.currentItem() == None:
            logging.info("selecione um objeto")
        else:
            obj = self.selected_object()
            angle = math.radians(float(self.angle_entry.text()))
            for point in obj.get_points():
                px = point.get_x()
                py = point.get_y()
                point.set_x((px*math.cos(angle)) - (py*math.sin(angle)))
                point.set_y((px*math.sin(angle)) - (py*math.cos(angle)))
                # point.set_x((px*math.cos(angle))+(py*math.sin(angle)))
                # point.set_y((py*math.cos(angle))-(px*math.sin(angle)))

            self.redraw_objects()
            logging.info("rotação de " + str(angle) + " radianos (" + self.angle_entry.text() +" º) aplicada")
            logging.info("objeto rotacionado " + obj.get_name() +  " em " + obj.get_str_points())

    def rotate_point(self):
        pass
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    
    screen = MainWindow()
    screen.show()

    sys.exit(app.exec())