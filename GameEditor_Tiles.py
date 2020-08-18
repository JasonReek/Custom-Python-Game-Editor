from PySide2.QtWidgets import (QGraphicsItem, QGraphicsItemGroup, QGraphicsPixmapItem)
from PySide2.QtGui import (QPixmap, QTransform)
from PySide2.QtCore import (QRectF, Qt, QRect, QLineF, QSize, QPointF)
from GameEditor_Globals import MD, LayerKeys
from enum import Enum

class Tiles:
    def __init__(self, scene):
        self._scene = scene
        self._tile_w = 32
        self._tile_h = 32
        self._current_tilemap = ""
        self._on_canvas = {}
        self._tile_items = {}
        self._z_level= 1
        self._layers = {
            "Layer 1": {LayerKeys.ITEM_GROUP: QGraphicsItemGroup(), LayerKeys.ITEM_LIST: {}, LayerKeys.ITEM_TMAP_POS_LIST: {}, LayerKeys.VISIBLE: True, LayerKeys.Z_LEVEL: 1}
        }
        self._current_layer = "Layer 1"
        self._scene.addItem(self._layers["Layer 1"][LayerKeys.ITEM_GROUP])
        self._layers["Layer 1"][LayerKeys.ITEM_GROUP].setZValue(self._layers["Layer 1"][LayerKeys.Z_LEVEL])

    # CREATE NEW LAYER 
    def createNewLayer(self, layer):
        self._z_level -= 1
        # Create New Item Group
        self._layers[layer] = {LayerKeys.ITEM_GROUP: QGraphicsItemGroup(), LayerKeys.ITEM_LIST: {}, LayerKeys.ITEM_TMAP_POS_LIST: {}, LayerKeys.VISIBLE: True, LayerKeys.Z_LEVEL: self._z_level}
        # Set Z Level
        self._layers[layer][LayerKeys.ITEM_GROUP].setZValue(self._layers[layer][LayerKeys.Z_LEVEL])
        # Add Item Group to Scene
        self._scene.addItem(self._layers[layer][LayerKeys.ITEM_GROUP])

    # Locates where to paint tile on to the canvas based on 
    # the mouse position. 
    def findTilePos(self, x, y):
        x_off = x % self._tile_w
        y_off = y  % self._tile_h
        new_x = x - x_off 
        new_y = y - y_off 

        return(new_x, new_y)
    
    # Paints the tile on to the canvas.
    def paintTile(self, tilemaps, current_tilemap, x, y, tilemap_x, tilemap_y, tilemap_w=32, tilemap_h=32):
        self._current_tilemap = current_tilemap
        # Position and dimension of tile in the tile map.
        tile_item = None 
        tile_from_map = (tilemap_x, tilemap_y)
        clip_space = QRect(tilemap_x, tilemap_y, tilemap_w, tilemap_h)
        tile = tilemaps[self._current_tilemap].copy(clip_space)
       
        tile_pos = self.findTilePos(x, y)
        '''
        if tile_pos in self._on_canvas.keys():
            self._on_canvas[tile_pos] = tile_from_map
            self._scene.removeItem(self._tile_items[tile_pos])
        else:
            self._on_canvas[tile_pos] = tile_from_map
        '''
        
        if tile_pos in self._layers[self._current_layer][LayerKeys.ITEM_LIST]:
            self._layers[self._current_layer][LayerKeys.ITEM_GROUP].removeFromGroup(self._layers[self._current_layer][LayerKeys.ITEM_LIST][tile_pos])
            self._scene.removeItem(self._layers[self._current_layer][LayerKeys.ITEM_LIST][tile_pos])
        self._layers[self._current_layer][LayerKeys.ITEM_TMAP_POS_LIST][tile_pos] = tile_from_map
        
        #self._tile_items[tile_pos] = self._scene.addPixmap(tile)
        #self._tile_items[tile_pos].setPos(tile_pos[0], tile_pos[1])
        tile_item = QGraphicsPixmapItem(tile)
        tile_item.setPos(tile_pos[0], tile_pos[1])
        self._layers[self._current_layer][LayerKeys.ITEM_GROUP].addToGroup(tile_item)
        self._layers[self._current_layer][LayerKeys.ITEM_LIST][tile_pos] = tile_item
        
        #self._scene.addItem(tile_item)

    def removeLayer(self, layer_key_name):
        self._scene.removeItem(self._layers[layer_key_name][LayerKeys.ITEM_GROUP])
        
    def clearAll(self):
        for tile_pos in self._on_canvas:
            self._scene.removeItem(self._tile_items[tile_pos])
        self._tile_items.clear()    
        self._on_canvas.clear()

    def dragUpRight(self, tilemaps, x, y, tile_x, tile_y, start_x, last_x, start_y, last_y):
        for drag_x in range(start_x, x+32, 32):
            for drag_y in range(y, start_y+32, 32):
                self.paintTile(tilemaps, self._current_tilemap, drag_x, drag_y, tile_x, tile_y)

    def dragDownRight(self, tilemaps, x, y, tile_x, tile_y, start_x, last_x, start_y, last_y):
        for drag_x in range(start_x, x+32, 32):
            for drag_y in range(start_y, y+32, 32):
                self.paintTile(tilemaps, self._current_tilemap, drag_x, drag_y, tile_x, tile_y)

    def dragUpLeft(self, tilemaps, x, y, tile_x, tile_y, start_x, last_x, start_y, last_y):
        for drag_x in range(x, start_x+32, 32):
            for drag_y in range(y, start_y+32, 32):
                self.paintTile(tilemaps, self._current_tilemap, drag_x, drag_y, tile_x, tile_y)

    def dragDownLeft(self, tilemaps, x, y, tile_x, tile_y, start_x, last_x, start_y, last_y):
        for drag_x in range(x, start_x+32, 32):
            for drag_y in range(start_y, y+32, 32):
                self.paintTile(tilemaps, self._current_tilemap, drag_x, drag_y, tile_x, tile_y)

    # Removes tile from canvas 
    def removeTile(self, x, y):
        tile_pos = self.findTilePos(x, y)
        self._layers[self._current_layer][LayerKeys.ITEM_GROUP].removeFromGroup(self._layers[self._current_layer][LayerKeys.ITEM_LIST][tile_pos])
        self._scene.removeItem(self._layers[self._current_layer][LayerKeys.ITEM_LIST][tile_pos])

    def setLayerVisibility(self, layer, visible):
        self._layers[layer][LayerKeys.VISIBLE] = visible
        if visible:
            self._scene.addItem(self._layers[layer][LayerKeys.ITEM_GROUP])
        else:
            self._scene.removeItem(self._layers[self._current_layer][LayerKeys.ITEM_GROUP])

    def dragPaint(self, tilemap, x, y, tile_x, tile_y, start_x, last_x, start_y, last_y):
        if x >= last_x and x >= start_x:
            self.paintTile(tilemap, self._current_tilemap, x, y, tile_x, tile_y)         
        elif x <= last_x and x <= start_x:
            self.paintTile(tilemap, self._current_tilemap, x, y, tile_x, tile_y)
        
        elif y <= last_y and y <= start_y:
            self.paintTile(tilemap, self._current_tilemap, x, y, tile_x, tile_y)
        
        elif y >= last_y and y >= start_y:
            self.paintTile(tilemap, self._current_tilemap, x, y, tile_x, tile_y)
    
    # Returns the tile map and tile positions for the world.     
    def getTiles(self):
        return self._on_canvas

    def getCurrentTilemap(self):
        return self._current_tilemap
    
    def setCurrentTilemap(self, tilemap):
        self._current_tilemap = tilemap

    def getTilemaps(self):
        return self._tilemaps

    def getTileBrushPixMap(self, tilemap_x=16, tilemap_y=0, tilemap_w=16, tilemap_h=16):
        if self._current_tile is not None:
            self._scene.removeItem(self._current_tile)
        clip_space = QRect(tilemap_x, tilemap_y, tilemap_w, tilemap_h)
        clipped = self._tilemaps[self._current_tilemap].copy(clip_space)
        clipped = clipped.scaled(QSize(clipped.size().width()*2, clipped.size().height()*2))
        return clipped
        

    



