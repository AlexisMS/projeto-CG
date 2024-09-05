import sys, logging
from PySide6.QtCore import Qt, QSize, QPoint, QLine, Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QLabel, QGroupBox, QGraphicsScene, QGraphicsView, QPlainTextEdit, QLayout, QMainWindow, QGraphicsLineItem, QLineEdit

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

if __name__ == '__main__':
    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.setBackgroundBrush(QColor('grey'))

    subWindows = SubWindows()

    #features
    viewport = QGraphicsView(scene)
    viewport.setFixedSize(QSize(800,600))

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

    #layouts
    left_menu_layout = QVBoxLayout()    
    left_menu_layout.addWidget(create_object_button)
    left_menu_layout.addWidget(object_list)
    left_menu = QGroupBox("Objetos")
    left_menu.setLayout(left_menu_layout)

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