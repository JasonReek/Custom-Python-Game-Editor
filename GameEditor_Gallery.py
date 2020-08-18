from PySide2.QtWidgets import (QWidget, QLabel, QOpenGLWidget, QGraphicsView, QGraphicsScene, QOpenGLWidget, QGridLayout, QPushButton, QFileDialog)
from PySide2.QtGui import (QPixmap, QTransform, QPen, QColor, QBrush, QImage)
from PySide2.QtCore import (QRectF, Qt, QRect, QLineF, QSize, QPointF)
from collections import OrderedDict

class GalleryScene(QGraphicsScene):
    def __init__(self):
        super(GalleryScene, self).__init__()

class GalleryView(QGraphicsView):
    def __init__(self):
        super(GalleryView, self).__init__()
        self.setupViewport(QOpenGLWidget())
        self._gallery = None 
 
    def pointToGallery(self, gallery):
        self._gallery = gallery 
    
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
        if self._gallery._gallery_grid:
            painter.setPen("#000000")
            for x in range(0, self.size().width(), 32): 
                for y in range(0, self.size().height(), 32):
                    painter.drawRect(x, y, 32, 32)

   
    def mousePressEvent(self, event):
    
        #self._canvas._show_grid = not self._canvas._show_grid
        #print(list(self._canvas._scene.items()))
        if event.button() == Qt.LeftButton:
            new_x, new_y = self._gallery.findTilePos(event.pos().x(), event.pos().y())
            self._gallery.drawInvertedSelection(event.pos().x(), event.pos().y(), new_x, new_y)
            self._gallery.selectTile(new_x, new_y)
            self._gallery._tile_selection = (new_x, new_y)
        elif event.button() == Qt.RightButton:
            pass
        #print(self._canvas._tiles.getTiles())
        #self._canvas.setCursor(QCursor(self._canvas._tiles.getTileBrushPixMap()))

class Gallery(QWidget):
    def __init__(self):
        super(Gallery, self).__init__()
        self._tile_w = 32
        self._tile_h = 32
        self._scene = GalleryScene()
        self._view = GalleryView()
        self._view.setScene(self._scene)
        self._view.pointToGallery(self)
        self._tilemaps = OrderedDict()
        self._current_tilemap = ""
        self._current_tilemap_item = None 
        self.layout = QGridLayout(self)
        self._selection_rect = None 
        self._tile_selection = (0, 0) 
        self._tile_selection_invert = None
        self._current_selection_border = None  
        self._current_selection_fill = None
        self._gallery_grid = False 
        self.layout.addWidget(self._view)
        self.loadTileMap("Content\\Tilesets\\Tilemap.png", scale=2)
        self.paintTileMap()
        self.drawInvertedSelection()
        
    # Loads the tile map (.png) file, and stores in a dictionary for use.
    def loadTileMap(self, file_path, scale=1):
        try:
            loaded_tilemap = QPixmap(file_path)
            loaded_tilemap = loaded_tilemap.scaled(QSize(loaded_tilemap.size().width()*scale, loaded_tilemap.size().height()*scale))
            self._tilemaps[file_path] = loaded_tilemap
            self._current_tilemap = file_path
    
        except Exception as e:
            print("Failed to load image "+str(e))
    
    def drawInvertedSelection(self, x=0, y=0, tilemap_x=0, tilemap_y=0, tilemap_w=32, tilemap_h=32):
        offset = 1
        clip_space_border = QRect(tilemap_x, tilemap_y, tilemap_w, tilemap_h)
        clip_space_fill = QRect(tilemap_x+3, tilemap_y+3, tilemap_w-6, tilemap_h-6)
        clipped_border = self._tilemaps[self._current_tilemap].copy(clip_space_border)
        clipped_fill = self._tilemaps[self._current_tilemap].copy(clip_space_fill)
        image = clipped_border.toImage()
        image.invertPixels()
        invert_selection = QPixmap()
        invert_selection.convertFromImage(image)
        tile_pos = self.findTilePos(x, y)
        if self._current_selection_border is not None and self._current_selection_fill is not None:
            self._scene.removeItem(self._current_selection_border)
            self._scene.removeItem(self._current_selection_fill)
        self._current_selection_border = self._scene.addPixmap(invert_selection)
        self._current_selection_fill = self._scene.addPixmap(clipped_fill)
        self._current_selection_border.setPos(tile_pos[0], tile_pos[1])
        self._current_selection_fill.setPos(tile_pos[0]+3, tile_pos[1]+3)
    
    def getCurrentTileSelection(self):
        return self._tile_selection[0], self._tile_selection[1]
    
    def getCurrentTilemap(self):
        return self._current_tilemap
    
    def setCurrentTilemap(self, tilemap):
        self._current_tilemap = tilemap

    def getTilemaps(self):
        return self._tilemaps
    # Locates where to paint tile on to the canvas based on 
    # the mouse position. 
    def findTilePos(self, x, y):
        x_off = x % self._tile_w
        y_off = y  % self._tile_h
        new_x = x - x_off 
        new_y = y - y_off 

        return(new_x, new_y)
    
    def selectTile(self, x, y):
        pen = QPen()
        pen.setColor(QColor(0x00, 0x32, 0x32, 0x60))
        pen.setWidth(4)
        new_x, new_y = self.findTilePos(x, y)
        selection_rect = QRect(new_x, new_y, self._tile_w, self._tile_h)
        
        if self._selection_rect is not None:
            self._scene.removeItem(self._selection_rect)
        self._selection_rect = self._scene.addRect(selection_rect, pen)
   
    def paintTileMap(self):
        tilemap = self._tilemaps[self._current_tilemap]
        tm_w = tilemap.size().width()
        tm_h = tilemap.size().height()
        self.setFixedWidth(tm_w+20)
        self.setFixedHeight(tm_h+20)
        self._scene.setSceneRect(0, 0, tm_w, tm_h)
        
        if self._current_tilemap_item is not None:
            self._current_tilemap_item = self._scene.itemAt(float(0), float(0), QTransform())
            self._scene.removeItem(self._current_tilemap_item)
        item = self._scene.addPixmap(tilemap)

        
               