from PySide2.QtWidgets import (QDialog, QColorDialog, QFileDialog, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QWidget, QLabel, QFrame, QSizePolicy, QGroupBox)
from PySide2.QtGui import (QIntValidator)

class BreakLine(QFrame):
    def __init__(self):
        super(BreakLine, self).__init__()
        self.setFrameShape(self.HLine)
        self.setFrameShadow(self.Sunken)

class VerticalFiller(QWidget):
    def __init__(self):
        super(VerticalFiller, self).__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

class HorizontalFiller(QWidget):
    def __init__(self):
        super(HorizontalFiller, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

class TileMapDialog(QDialog):
    def __init__(self):
        super(TileMapDialog, self).__init__()
        layout = QGridLayout(self)
        self.setWindowTitle("Load Tilemap Settings")
        self._int_validator = QIntValidator()
        self._not_canceled = True  

        # Tilemap File Path
        browse_tile_map_layout = QGridLayout()
        self._group_box_tile_browse = QGroupBox("Load Tilemap .png")
        self._group_box_tile_browse.setLayout(browse_tile_map_layout) 
        self._load_tilemap_label = QLabel("Tilemap:")
        self._load_tilemap_path_entry = QLineEdit() 
        self._load_tilemap_path_entry.setFixedWidth(350)
        self._load_tilemap_button = QPushButton("Browse for Tilemap") 
        self._load_tilemap_button.clicked.connect(self.openTileMapFile)

        # Tile Width and Height
        tile_map_dimensions_layout = QGridLayout()
        self._group_box_tile_dimensions = QGroupBox("Tilemap Dimensions")
        self._group_box_tile_dimensions.setLayout(tile_map_dimensions_layout)
        self._tile_width_label = QLabel("Tile Width:")
        self._tile_width_entry = QLineEdit("16")
        self._tile_width_entry.setValidator(self._int_validator)
        self._tile_height_label = QLabel("Tile Height:")
        self._tile_height_entry = QLineEdit("16")
        self._tile_height_entry.setValidator(self._int_validator)

        # Scale
        tile_map_scale_layout = QGridLayout()
        self._group_box_tile_scale = QGroupBox("Tile Scale")
        self._group_box_tile_scale.setLayout(tile_map_scale_layout)
        self._scale_label = QLabel("Scale:")
        self._scale_entry = QLineEdit("1")
        self._scale_entry.setValidator(self._int_validator)

        browse_tile_map_layout.addWidget(self._load_tilemap_label,0,0)
        browse_tile_map_layout.addWidget(self._load_tilemap_path_entry, 1, 0)
        browse_tile_map_layout.addWidget(self._load_tilemap_button, 1, 1)

        tile_map_dimensions_layout.addWidget(self._tile_width_label, 2, 0)
        tile_map_dimensions_layout.addWidget(self._tile_height_label, 2, 1)
        tile_map_dimensions_layout.addWidget(self._tile_width_entry, 3, 0)
        tile_map_dimensions_layout.addWidget(self._tile_height_entry, 3, 1)

        tile_map_scale_layout.addWidget(self._scale_label, 4, 0)
        tile_map_scale_layout.addWidget(self._scale_entry, 5, 0)
        tile_map_scale_layout.addWidget(HorizontalFiller(), 5, 1)

        buttons = QWidget() 
        buttons_layout = QHBoxLayout(buttons)
        self._enter_button = QPushButton("Enter")
        self._enter_button.clicked.connect(self.close) 
        self._cancel_button = QPushButton("Cancel")
        self._cancel_button.clicked.connect(self.cancel)
        buttons_layout.addWidget(self._enter_button)
        buttons_layout.addWidget(self._cancel_button) 

        layout.addWidget(self._group_box_tile_browse, 0, 0)
        layout.addWidget(self._group_box_tile_dimensions, 1, 0)
        layout.addWidget(self._group_box_tile_scale, 2, 0)
        layout.addWidget(buttons, 3, 0)
        self.setLayout(layout)


    def openTileMapFile(self):
        file_path = QFileDialog.getOpenFileName(self, "Open Tilemap", ".", "Image Files (*.png)")[0]
        self._load_tilemap_path_entry.setText(file_path)
        
    def getTileMapInfo(self):
        if self._not_canceled:
            return self._load_tilemap_path_entry.text(), int(self._tile_width_entry.text()), int(self._tile_height_entry.text()), int(self._scale_entry.text())
        return "", 16, 16, 1
    
    def cancel(self):
        self._not_canceled = False 
        self.close()

    def isNotCanceled(self):
        return self._not_canceled


           
