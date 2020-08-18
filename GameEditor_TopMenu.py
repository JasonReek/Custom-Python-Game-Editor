from PySide2.QtWidgets import (QAction)
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Qt, QSize, QRect
from GameThread import*
from GameEditor_PaintTools import (PaintTools)
from enum import Enum

class TopMenu:
    def __init__(self):
        #***********
        # Window Menu 
        #-------------------------------------------------------------------
        self.main_menu = self.menuBar()

        # Menu - File:
        #-------------------------------------------------------------------
        self.file_menu = self.main_menu.addMenu("File")

        ## File -> Run game - Runs the game.
        self.game_win_command = QAction("Run Game", self)
        self.game_win_command.triggered.connect(self.runGameWindow)
        self._game_win_is_running = False 
        self.file_menu.addAction(self.game_win_command)
        self.file_menu.addSeparator()
        
        ## File -> Exit - Closes the editor window.
        self.exit_command = QAction("Exit", self)
        self.exit_command.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_command)

        # Menu - Edit
        #-------------------------------------------------------------------
        self.edit_menu = self.main_menu.addMenu("Edit")

        ## Edit -> Show Grid - Displays grid on world canvas space.
        self.show_grid_command = QAction("Show Grid", self)
        self.show_grid_command.triggered.connect(self.showGrid)
        self.edit_menu.addAction(self.show_grid_command)
        self.grid_showing = False 

        # Menu - Tools
        #-------------------------------------------------------------------
        self.tool_menu = self.main_menu.addMenu("Tools")

        self.gallery_tool_command = QAction("Gallery", self)
        self.tool_menu.addAction(self._gallery_dock.toggleViewAction())
        self.layer_tool_command = QAction("Map Layers", self)
        self.tool_menu.addAction(self._layers_dock.toggleViewAction())

        #***********
        # Tile Paint Tool Bar 
        #------------------------------------------------------------------- 
        self._paint_tools = PaintTools(self)
        self._paint_toolbar = self.addToolBar("Tile Paint Tools")
        
        # Pencil Brush         
        self._paint_toolbar.addAction(self._paint_tools._pencil_brush)

        # Tile Drag Brush
        self._paint_toolbar.addAction(self._paint_tools._tile_drag_brush)

        # Erase Brush
        self._paint_toolbar.addAction(self._paint_tools._eraser_brush) 


    # Method for running the game. 
    def runGameWindow(self):
        try:
            global game_thread
            if not isGameRunning():
                game_thread = GameWindowThread("GameThread")
                game_thread.start()
                self._game_win_is_running = True
            else:
                self._game_win_is_running = False 
            
        except Exception as e:
            print("Run Game Error - "+str(e))
    

    # Method for showing grid on world map.
    def showGrid(self):
        try:
            if self._world_canvas._canvas_grid:
                self.show_grid_command.setText("Show Grid")
                self._world_canvas._canvas_grid = False  
            else:
                self.show_grid_command.setText("Hide Grid")
                self._world_canvas._canvas_grid = True
        except Exception as e:
            print("Grid Show Error - "+str(e))