import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QTextEdit, QWidget, QGridLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QAction,
                                QTabWidget, QOpenGLWidget, QGroupBox, QScrollArea, QScroller, QDockWidget, QFrame)
from PySide2.QtCore import (Qt)
from PySide2.QtGui import (QIcon)
from GameEditor_TopMenu import TopMenu
from GameEditor_WorldCanvas import WorldCanvas
from GameEditor_Gallery import Gallery
from GameEditor_CustomWidgets import HorizontalFiller, VerticalFiller

class Window(QMainWindow, TopMenu):
    def __init__(self, parent=None):
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QIcon("icon_maybe_BIG.ico"))
        self.app.setStyle("Fusion")
        super(Window, self).__init__(parent)

        # Main Layout for Editor
        self._main_widget = QWidget(self)
        self._main_layout = QGridLayout(self._main_widget)

        self._scroll = QScrollArea()
        self._tilemap_scroll = QScrollArea()

        self.setWindowTitle("Game Editor")
        
        self._gallery = Gallery()
        self._gallery_frame = QFrame(self)
        self._world_canvas = WorldCanvas(self._gallery, self)

        gallery_layout = QGridLayout(self._gallery_frame)
        gallery_layout.addWidget(self._gallery)
        
        buttons = QWidget(self)
        buttons_layout = QGridLayout(buttons)
        buttons_layout.addWidget(self._world_canvas._last_tilemap_button, 0, 0)
        buttons_layout.addWidget(self._world_canvas._next_tilemap_button, 0, 1)
        buttons_layout.addWidget(self._world_canvas._gallery_grid_chkbox, 0, 2)
        buttons_layout.addWidget(HorizontalFiller(), 0, 3)
        buttons_layout.addWidget(self._world_canvas._load_tilemap_button, 0, 4)
        gallery_layout.addWidget(buttons)
        gallery_layout.addWidget(VerticalFiller())
        self._gallery_dock = QDockWidget("Tilemaps", self)
        self._gallery_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self._tilemap_scroll.setWidget(self._gallery_frame)
        self._gallery_dock.setWidget(self._tilemap_scroll)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._gallery_dock)

        self._layers_dock = QDockWidget("Map Layers", self)
        self._layers_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self._layers_dock.setWidget(self._world_canvas._layers._layers_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._layers_dock)

        # Add top menu
        TopMenu.__init__(self)
        self._world_canvas.setPaintTools(self._paint_tools)
        
        # World Canvas Layout 

        # Canvas Top Section
        canvas_bot_section = QWidget(self)
        canvas_bot_section_layout = QGridLayout(canvas_bot_section)
        canvas_bot_section_layout.addWidget(QLabel(" Map Coordinates: "), 0, 0)
        canvas_bot_section_layout.addWidget(self._world_canvas._map_coords_label, 0, 1)
        canvas_bot_section_layout.addWidget(HorizontalFiller(), 0, 2)

        self._world_canvas_widget = QWidget(self)
        self._world_canvas_layout = QGridLayout(self._world_canvas_widget)
        self._world_canvas_layout.addWidget(self._world_canvas, 0, 0)
        self._world_canvas_layout.addWidget(canvas_bot_section, 1, 0)
        
        self._world_canvas_layout.addWidget(HorizontalFiller(),1,1)
        self._world_canvas_layout.addWidget(VerticalFiller(),2,0)
        
    
        self._main_layout.addWidget(self._world_canvas_widget, 0, 0)
    
        self._scroll.setWidget(self._main_widget)
        self.setCentralWidget(self._scroll)

    def start(self):
        self.showMaximized()
        
        sys.exit(self.app.exec_())
 
if __name__ == "__main__":
    window = Window()
    window.start()
