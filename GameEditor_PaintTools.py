
from PySide2.QtWidgets import (QWidget, QOpenGLWidget, QGraphicsView, QGraphicsScene, QOpenGLWidget, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, 
                               QGridLayout, QPushButton, QScrollArea, QAction, QScroller, QToolBar, QToolButton)
from PySide2.QtGui import (QPixmap, QPainter, QFont, QColor, qRgb, QIcon, QPainterPath, QTransform, QCursor)
from PySide2.QtCore import (QRectF, Qt, QRect, QLineF, QSize, QPointF)
from GameEditor_Globals import Brushes


class PaintTools:
    def __init__(self, main):
        self._paint_tool_icons_loc = "resources/paint_tool_icons.png"
        self._paint_tool_icons = None
        self.loadIcons(self._paint_tool_icons_loc)
        
        # Current active brush being used in the map editor. 
        self._active_brush = Brushes.NONE 
        self._icon_size = 64 

        # Pencil Brush 
        self._pencil_brush = QAction("Pencil Brush", main)
        self._pencil_brush.setCheckable(True)
        pencil_icon = self.getIcon(0, 0)
        self._pencil_brush.setIcon(pencil_icon)
        self._pencil_brush.triggered.connect(self.changeActiveBrush(Brushes.PENCIL, self._pencil_brush))

        # Tile Drag Brush
        self._tile_drag_brush = QAction("Tile Drag Brush", main)
        self._tile_drag_brush.setCheckable(True)
        tile_drag_icon = self.getIcon(64, 0)
        self._tile_drag_brush.setIcon(tile_drag_icon)
        self._tile_drag_brush.triggered.connect(self.changeActiveBrush(Brushes.TILE_DRAG, self._tile_drag_brush))

        # Eraser Brush
        self._eraser_brush = QAction("Eraser Brush", main)
        self._eraser_brush.setCheckable(True)
        eraser_icon = self.getIcon(self._icon_size*6, 0)
        self._eraser_brush.setIcon(eraser_icon)
        self._eraser_brush.triggered.connect(self.changeActiveBrush(Brushes.ERASER, self._eraser_brush))
        # The last brush used
        self._last_brush_used = None
    
    # Changes the active brush depending on which brush tool button was pressed. 
    def changeActiveBrush(self, brush, tool_button):
        def activeBrush():
            if tool_button.isChecked():
                if self._last_brush_used != None and self._last_brush_used != tool_button:
                    self._last_brush_used.setChecked(False)
                self._active_brush = brush
                self._last_brush_used = tool_button
            else:
                self._active_brush = Brushes.NONE
        return activeBrush    

    def loadIcons(self, file_path, scale=2):
        self._paint_tool_icons = QPixmap(file_path)
        #self._paint_tool_icons = self._paint_tool_icons.scaled(QSize(self._paint_tool_icons.size().width()*scale, self._paint_tool_icons.size().height()*scale))

    def getIcon(self, x, y, w=64, h=64):
        clip_space = QRect(x, y, w, h)
        clipped = self._paint_tool_icons.copy(clip_space)
        icon = QIcon()
        icon.addPixmap(clipped)
        return icon    
    
    def currentActiveBrush(self):
        return self._active_brush