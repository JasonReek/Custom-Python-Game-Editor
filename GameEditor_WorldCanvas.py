
from PySide2.QtWidgets import (QAbstractItemView, QWidget, QLabel, QOpenGLWidget, QGraphicsView, QGraphicsScene, QOpenGLWidget, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, 
                               QGridLayout, QPushButton, QScrollArea, QScroller, QToolBar, QToolButton, QCheckBox, QComboBox, QListWidget, QListWidgetItem, QTabBar)
from PySide2.QtGui import (QPixmap, QPainter, QFont, QColor, qRgb, QBrush, QPainterPath, QTransform, QCursor, QPen)
from PySide2.QtCore import (QRectF, Qt, QRect, QLineF, QSize, QPointF, QEvent)

from GameEditor_Globals import MD, Brushes, LayerKeys
from GameEditor_Tiles import Tiles
from GameEditor_CustomWidgets import TileMapDialog, HorizontalFiller
from GameEditor_Layers import Layers

class WorldScene(QGraphicsScene):
    def __init__(self):
        super(WorldScene, self).__init__()
        
class WorldView(QGraphicsView):
    def __init__(self):
        super(WorldView, self).__init__()
        self.setupViewport(QOpenGLWidget())
        self._canvas = None 
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._drag = False 

        self._start_x = -1
        self._start_y = -1
        self._last_x = -1
        self._last_y = -1
        self._mouse_direction = MD.NONE
        self._last_mouse_direction = MD.NONE
        self._erase = False 
        self._paint = False
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover)

    # EVENT HANDELING HERE 
    def event(self, event):
        if event.type() == QEvent.HoverMove:
            tile_pos = self._canvas._tiles.findTilePos(event.pos().x(), event.pos().y())
            try:
                if tile_pos != None:
                    tile_pos_text = ', '.join(["X: "+str(tile_pos[0]), "Y: "+str(tile_pos[1])])
                    self._canvas._map_coords_label.setText(tile_pos_text)
            except Exception as e:
                print(str(e))
        return super().event(event) 
 
    def pointToCanvas(self, canvas):
        self._canvas = canvas 

    def mousePressEvent(self, event):
    
        #self._canvas._show_grid = not self._canvas._show_grid
        #print(list(self._canvas._scene.items()))
        active_brush = self._canvas._paint_tools.currentActiveBrush()
        if event.button() == Qt.LeftButton:
            tile_x, tile_y = self._canvas._gallery.getCurrentTileSelection()
            if active_brush == Brushes.PENCIL or active_brush == Brushes.TILE_DRAG:
                self._canvas._tiles.paintTile(self._canvas._gallery._tilemaps, self._canvas._gallery._current_tilemap, event.pos().x(), event.pos().y(), tile_x, tile_y)
            
            elif active_brush == Brushes.ERASER:
                self._canvas._tiles.removeTile(event.pos().x(), event.pos().y())

        elif event.button() == Qt.RightButton:
            pass
            #self._canvas._tiles.clearAll()
            #self._canvas._tiles.removeTile(event.pos().x(), event.pos().y())
        #print(list(self._canvas._scene.items()))
        #print(self._canvas._tiles.getTiles())
        #self._canvas.setCursor(QCursor(self._canvas._tiles.getTileBrushPixMap()))
 
    def mouseMoveEvent(self, event):
        active_brush = self._canvas._paint_tools.currentActiveBrush()
        if event.buttons() == Qt.LeftButton:
            if not self._drag:
                self._drag = True
                x, y = self._canvas._gallery.findTilePos(event.pos().x(), event.pos().y())
                self._start_x = x
                self._start_y = y
                self._last_x = x 
                self._last_y = y
                
            if self._drag and active_brush == Brushes.PENCIL or active_brush == Brushes.ERASER:
                tile_x, tile_y = self._canvas._gallery.getCurrentTileSelection()
                x, y = self._canvas._gallery.findTilePos(event.pos().x(), event.pos().y())

                if x > self._last_x:
                    self._mouse_direction = MD.RIGHT
                elif x < self._last_x:
                    self._mouse_direction = MD.LEFT
                elif y < self._last_y:
                    self._mouse_direction = MD.UP
                elif y > self._last_y:
                    self._mouse_direction = MD.DOWN
                    
                if active_brush == Brushes.PENCIL:
                    self._canvas._tiles.dragPaint(self._canvas._gallery._tilemaps, x, y, tile_x, tile_y, self._start_x, self._start_y, self._last_x, self._last_y)
                elif active_brush == Brushes.ERASER:
                    self._canvas._tiles.removeTile(x, y)

            elif self._drag and active_brush == Brushes.TILE_DRAG:
                tile_x, tile_y = self._canvas._gallery.getCurrentTileSelection()
                x, y = self._canvas._gallery.findTilePos(event.pos().x(), event.pos().y())

                # LOWER RIGHT REGION---------------------------------------------------------------------------------------------------------------------------------------------
                if (x >= self._last_x and x > self._start_x) and (y >= self._last_y and y > self._start_y):
                    self._canvas._tiles.dragDownRight(self._canvas._gallery._tilemaps, x, y, tile_x, tile_y, self._start_x, self._last_x, self._start_y, self._last_y)
            
                #----------------------------------------------------------------------------------------------------------------------------------------------------------------
                
                # UPPER RIGHT REGION---------------------------------------------------------------------------------------------------------------------------------------------
                if (x >= self._last_x and x > self._start_x) and (y <= self._last_y and y < self._start_y):
                    self._canvas._tiles.dragUpRight(self._canvas._gallery._tilemaps, x, y, tile_x, tile_y, self._start_x, self._last_x, self._start_y, self._last_y)
            
                #----------------------------------------------------------------------------------------------------------------------------------------------------------------

                # LOWER LEFT REGION---------------------------------------------------------------------------------------------------------------------------------------------
                if (x <= self._last_x and x < self._start_x) and (y >= self._last_y and y > self._start_y):
                    self._canvas._tiles.dragDownLeft(self._canvas._gallery._tilemaps, x, y, tile_x, tile_y, self._start_x, self._last_x, self._start_y, self._last_y)
            
                #----------------------------------------------------------------------------------------------------------------------------------------------------------------
                
                # UPPER LEFT REGION---------------------------------------------------------------------------------------------------------------------------------------------
                if (x <= self._last_x and x < self._start_x) and (y <= self._last_y and y < self._start_y):
                    self._canvas._tiles.dragUpLeft(self._canvas._gallery._tilemaps, x, y, tile_x, tile_y, self._start_x, self._last_x, self._start_y, self._last_y)
                #----------------------------------------------------------------------------------------------------------------------------------------------------------------
            
            if active_brush == Brushes.PENCIL or active_brush == Brushes.TILE_DRAG:
                self._last_mouse_direction = self._mouse_direction
                self._last_x = x
                self._last_y = y
                self._erase = False 

    def mouseReleaseEvent(self, event):
        self._drag = False 
        self._mouse_direction = MD.NONE
        self._last_mouse_direction = MD.NONE

    def drawBackground(self, painter, rect):
        background_brush = QBrush(QColor("#AAAAAA"), Qt.SolidPattern)
        switch = True 
        tile_interval = 32
        switch = False
        for x in range(0, self.size().width(), 16): 
            for y in range(0, self.size().height(), 16):
                switch = not switch
                if switch:
                    painter.fillRect(x, y, 16, 16, QColor(Qt.white))
                else:
                    painter.fillRect(x, y, 16, 16, QColor("#EDEDED"))
    
    def drawForeground(self, painter, rect):
        if self._canvas._canvas_grid:
            painter.setPen("#000000")
            for x in range(0, self.size().width(), 32): 
                for y in range(0, self.size().height(), 32):
                    painter.drawRect(x, y, 32, 32)
       
class WorldCanvas(QWidget):
    def __init__(self, gallery, main):
        super(WorldCanvas, self).__init__()
        self.setParent(main)
        self._main = main 
        self._layout = QGridLayout(self)
        self._gallery = gallery
        self._paint_tools = None 
        self._last_tilemap_button = QPushButton("❮ Last Tilemap", main)
        self._next_tilemap_button = QPushButton("Next Tilemap ❯", main)
        self._next_tilemap_button.clicked.connect(self.nextTilemap)
        self._last_tilemap_button.clicked.connect(self.lastTilemap)
        self._gallery_grid_chkbox = QCheckBox("Grid", main)
        self._gallery_grid_chkbox.stateChanged.connect(self.galleryGridStateChange)
        self._canvas_grid = False 
        self.setFixedWidth(820)
        self.setFixedHeight(695)
        
        self._scene = WorldScene()
        self._scene.setSceneRect(0, 0, 800, 640)
        self._tiles = Tiles(self._scene)
        self._view = WorldView()
        self._view.setScene(self._scene)
        self._view.pointToCanvas(self)
        
        self._show_grid = False
        self._map_coords_label = QLabel("X: , Y: ")

        self._load_tilemap_button = QPushButton("Add Tilemap", main) 
        self._load_tilemap_button.clicked.connect(self.openTileMapFile)

        # LAYERS
        self._layers = Layers(main, self._tiles)
        self._layout.setSpacing(0)
   
        self._layout.addWidget(self._layers.getTabs(), 0, 0)
        self._layout.addWidget(HorizontalFiller(), 0, 1)
        self._layout.addWidget(self._view)

    def galleryGridStateChange(self):
        self._gallery._gallery_grid = self._gallery_grid_chkbox.isChecked()

    def setPaintTools(self, paint_tools):
        self._paint_tools = paint_tools
    
    def nextTilemap(self):
        current_tilemap = self._gallery.getCurrentTilemap()
        tilemaps = list(self._gallery.getTilemaps().keys())
        index = tilemaps.index(current_tilemap)
        if index < len(tilemaps)-1:
            index += 1
            self._gallery.setCurrentTilemap(tilemaps[index])
            self._gallery.paintTileMap()
            self._tiles.setCurrentTilemap(tilemaps[index])
    
    def lastTilemap(self):
        current_tilemap = self._gallery.getCurrentTilemap()
        tilemaps = list(self._gallery.getTilemaps().keys())
        index = tilemaps.index(current_tilemap)
        if index > 0:
            index -= 1
            self._gallery.setCurrentTilemap(tilemaps[index])
            self._gallery.paintTileMap()
            self._tiles.setCurrentTilemap(tilemaps[index])

    def openTileMapFile(self):
        tilemap_dialog = TileMapDialog()
        file_path = ""

        tile_scale = 1
        tilemap_dialog.exec_()
        temp_tile_w = self._gallery._tile_w
        temp_tile_h = self._gallery._tile_h
        if tilemap_dialog.isNotCanceled():
            file_path, self._gallery._tile_w, self._gallery._tile_h, tile_scale = tilemap_dialog.getTileMapInfo()
            if file_path != "" and file_path not in self._gallery._tilemaps.keys():
                self._gallery.loadTileMap(file_path, scale=tile_scale)
                self._gallery.paintTileMap()
            else:
                self._tile_w = temp_tile_w
                self._tile_h = temp_tile_h

    def paintMap(self):
        for x in range(0, 800, 32):
            for y in range(0, 640, 32):
                clip_space = QRect(0, 0, 16, 16)
                clipped = self.p_m.copy(clip_space)
                clipped = clipped.scaled(QSize(clipped.size().width()*2, clipped.size().height()*2))
                item = self._scene.addPixmap(clipped)
                item.setPos(x, y)

    def paintEvent(self, event):
        pass
        #self._scene.clear()
        #self.paintMap()
          

