from PySide2.QtWidgets import (QListWidgetItem, QColorDialog, QSizePolicy, QStylePainter, QStyle, QStyleOptionTab, QTabBar, QAbstractItemView, QListWidget, QPushButton, QDialog, QWidget, QHBoxLayout, QMenu, QAction, QFormLayout, QHBoxLayout, QLineEdit)
from PySide2.QtCore import Qt, QEvent, QPoint, QObject
from GameEditor_Globals import LayerKeys
from GameEditor_CustomWidgets import HorizontalFiller
import operator

class LayerTabBar(QTabBar):
    def __init__(self, parent, layers):
        super(LayerTabBar, self).__init__(parent)
        self.installEventFilter(self)
        self._layers = layers
    
    def eventFilter(self, QObject, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                x = event.x()
                y = event.y()
                index = self.tabAt(QPoint(x,y))
                print(x, y, index)
                if index > -1:
                    self._layers.leftClickLayerMenu(x, y, self)
        return False 

class RenameLayerPrompt(QDialog):
    def __init__(self, old_layer_name, parent=None):
        super(RenameLayerPrompt, self).__init__(parent)
        self.setWindowTitle('Rename Layer: '+'"'+str(old_layer_name)+'"')
        layout = QFormLayout()
        button_row = QWidget(self)
        button_layout = QHBoxLayout(button_row) 
        self._canceled = True 
        self._enter_button = QPushButton("Enter") 
        self._cancel_button = QPushButton("Cancel") 
        self._enter_button.clicked.connect(self.enter)
        self._cancel_button.clicked.connect(self.close)

        button_layout.addWidget(HorizontalFiller())
        button_layout.addWidget(self._cancel_button)
        button_layout.addWidget(self._enter_button)
        
        self._new_layer_name_entry = QLineEdit(self) 
        self._new_layer_name_entry.setPlaceholderText(old_layer_name)
        layout.addRow("Enter new layer name:", self._new_layer_name_entry)
        layout.addRow(button_row)
        self.setLayout(layout)
    
    def enter(self):
        self._canceled = False 
        self.close()
    
    def getNewName(self):
        return self._new_layer_name_entry.text()

class LayerList(QListWidget):
    def __init__(self, layers, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        self._layers = layers
    
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            x = event.x()
            y = event.y()
            item = self.itemAt(QPoint(x,y))
            if item is not None:
                self._layers.leftClickLayerMenu(x, y, self)
        return super(LayerList, self).eventFilter(source, event) 
           
class Layers:
    def __init__(self, parent, tiles):
        self._parent = parent  
        self._layer_tabs = LayerTabBar(parent, self)
        
        self._layer_tabs.setMovable(True)
        self._layer_tabs.setContentsMargins(0,0,0,0)
        self._add_layer_button = QPushButton("+")
        self._add_layer_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._add_layer_button.setFixedWidth(35)
        self._add_layer_button.clicked.connect(self.addNewLayerTab)
        self._layer_tabs_row = QWidget(parent)
        self._layer_tabs_layout = QHBoxLayout(self._layer_tabs_row)
        self._layer_tabs_layout.setSpacing(0)
        self._layer_tabs_layout.setContentsMargins(0,0,0,0)
        self._layer_tabs_layout.addWidget(self._layer_tabs)
        self._layer_tabs_layout.addWidget(self._add_layer_button)
        self.DEFAULT_TAB_COLOR = "#EFEFEF"
        
        self._tiles = tiles 
        self._layers_widget = LayerList(self)

        layer_1 = QListWidgetItem("Layer 1")
        layer_1.setFlags(layer_1.flags() | Qt.ItemIsUserCheckable)
        layer_1.setCheckState(Qt.Checked)
        layer_1.setText("Layer 1 (Selected)")
        self._layers_widget.addItem(layer_1)

        # Stores the Layer properties 
        self._layers = {"Layer 1": {LayerKeys.NAME: "Layer 1", LayerKeys.LIST_ITEM: layer_1, LayerKeys.REMOVABLE: False, LayerKeys.TAB_COLOR: self.DEFAULT_TAB_COLOR}
        
        }
        self._layer_tabs.setStyleSheet('''
                QTabBar::tab {{}}
                QTabBar::tab:selected {{background-color: {color}; border: 1px solid #777777; border-radius: 4px;}}
            '''.format(color=self._layers["Layer 1"][LayerKeys.TAB_COLOR]))
        
        self._tab_change = False 
        self._list_change = False 
        
        self._plus_button = QPushButton("+", parent)
        self._plus_button.setFixedSize(20, 20)
        
        first_layer = "Layer 1"
        self._active_layer = first_layer
        self._layer_tab_names = {}
        self._layer_tab_indexes = {}
        tab_index = self._layer_tabs.addTab(first_layer)
        self._add_tab_index = 2
        self.lockTabs()

        

        # SIGNAL METHODS 
        self._layers_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self._layers_widget.itemDoubleClicked.connect(self.doubleClickLayerItem)
        self._layers_widget.itemChanged.connect(self.layerVisibility)
        self._plus_button.clicked.connect(self.addNewLayerTab)
        self._layer_tabs.currentChanged.connect(self.changeTabLayer)
        self._layer_tabs.tabMoved.connect(self.layerTabMoved)

        self.tabColors = {
            0: 'green', 
            1: 'red', 
            2: 'yellow', 
            3: 'orange', 
            4: 'blue', 
            }

    def getLayerIndex(self, layer_name):
        for layer_index in range(0, self._layer_tabs.count()):
            if self._layer_tabs.tabText(layer_index) == layer_name:
                return layer_index
    
    def getLayerName(self, layer_index):
        return self._layer_tabs.tabText(layer_index)

    def addLayerListItem(self, layer_name, z_level):
        layer_key_name = self.getLayerKeyName(layer_name)
        layer_item = QListWidgetItem(layer_name)
        layer_item.setFlags(layer_item.flags() | Qt.ItemIsUserCheckable)
        if self._tiles._layers[layer_key_name][LayerKeys.VISIBLE]:
            layer_item.setCheckState(Qt.Checked)
        else:
            layer_item.setCheckState(Qt.Unchecked)
        self._layers[layer_key_name][LayerKeys.LIST_ITEM] = layer_item
        self._tiles._layers[layer_key_name][LayerKeys.Z_LEVEL] = z_level
        self._tiles._layers[layer_key_name][LayerKeys.ITEM_GROUP].setZValue(z_level)
        if layer_name == self._layers[self._active_layer][LayerKeys.NAME]:
            layer_item.setText(layer_name+" (Selected)")
        self._layers_widget.addItem(layer_item)
    
    def setLayerZLevel(self, layer_name, z_level):
        layer_key_name = self.getLayerKeyName(layer_name)
        self._tiles._layers[layer_key_name][LayerKeys.ITEM_GROUP].setZValue(z_level)
    
    def setLayerVisibility(self, layer_name, visible):
        layer_key_name = self.getLayerKeyName(layer_name)
        self._tiles._layers[layer_key_name][LayerKeys.VISIBLE] = visible
        if visible:
            self._layers[layer_key_name][LayerKeys.LIST_ITEM].setCheckState(Qt.Checked)
        else:
            self._layers[layer_key_name][LayerKeys.LIST_ITEM].setCheckState(Qt.Unchecked)
    
    def lockTabs(self):
        for tab_index in range(0, self._layer_tabs.count()):    
            layer_key_name = self.getLayerKeyName(self.getLayerName(tab_index))
            layer_name = self.getLayerName(tab_index)
            if LayerKeys.CLOSE_BUTTON not in self._layers.keys():
                self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON] = QPushButton("×", self._parent)
                self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON].setFixedWidth(25)
                self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON].setFlat(True)
                self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON].setContentsMargins(0,0,0,0)
                self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON].clicked.connect(self._removeLayerTab(layer_name))
                self._layer_tabs.setTabButton(tab_index, self._layer_tabs.RightSide, self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON])
            if not self._layers[layer_key_name][LayerKeys.REMOVABLE]:
                self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON].setDisabled(True)

    def setLayerRemovable(self, layer_name, removable):
        layer_key_name = self.getLayerKeyName(layer_name)
        self._layers[layer_key_name][LayerKeys.REMOVABLE] = removable
        self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON].setEnabled(True)
        
    def _removeLayerTab(self, layer_name):
        def removeLayerTab():
            layer_index = self.getLayerIndex(layer_name)
            layer_key_name = self.getLayerKeyName(layer_name)
            # Change active layer if it is removed.
            if layer_key_name == self._active_layer:
                self._active_layer = self.getLayerKeyName(self.getLayerName(layer_index-1))
            self._layer_tabs.removeTab(layer_index)
            self._tiles.removeLayer(layer_key_name)
            
            self._layers[layer_key_name].clear()
            self._tiles._layers[layer_key_name].clear()
            del self._layers[layer_key_name]
            del self._tiles._layers[layer_key_name]
            self._layers_widget.clear()
            for tab_index in range(0, self._layer_tabs.count()):
                ln = self._layer_tabs.tabText(tab_index)
                self.addLayerListItem(ln, tab_index*-1)
        return removeLayerTab

    def getLayerKeyName(self, layer_name):
        for layer_key, layer_properties in self._layers.items():
            if layer_properties[LayerKeys.NAME] == layer_name:
                return layer_key
        return None 
    
    def _changeLayerName(self, old_layer_name):
        def changeLayerName():
            new_name_dialog = RenameLayerPrompt(old_layer_name, self._parent)
            new_name_dialog.exec_() 
            if not new_name_dialog._canceled:
                new_layer_name = new_name_dialog.getNewName()
                layer_key_name = self.getLayerKeyName(old_layer_name)
                layer_index = self.getLayerIndex(old_layer_name)
                self._layers[layer_key_name][LayerKeys.NAME] = new_layer_name
                self._layer_tabs.setTabText(layer_index, new_layer_name)
                if self._active_layer == layer_key_name:
                    self._layers[layer_key_name][LayerKeys.LIST_ITEM].setText(new_layer_name+" (Selected)")
                else:
                    self._layers[layer_key_name][LayerKeys.LIST_ITEM].setText(new_layer_name)
                self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON].clicked.disconnect()
                self._layers[layer_key_name][LayerKeys.CLOSE_BUTTON].clicked.connect(self._removeLayerTab(new_layer_name))
        return changeLayerName

    def _changeTabColor(self, layer_key_name):
        def changeTabColor():
            layer_name = self._layers[layer_key_name][LayerKeys.NAME]
            color_dialog = QColorDialog()
            color = color_dialog.getColor()
            if color.isValid():
                hex_color = color.name()
                self._layers[layer_key_name][LayerKeys.TAB_COLOR] = hex_color
                index = self.getLayerIndex(layer_name)
                self._layer_tabs.setCurrentIndex(index)
                self._layer_tabs.setStyleSheet('''
                    QTabBar::tab {{}}
                    QTabBar::tab:selected {{background-color: {color}; border: 1px solid #777777; border-radius: 4px;}}
                '''.format(color=self._layers[layer_key_name][LayerKeys.TAB_COLOR]))
                
        return changeTabColor

    def _resetTabColor(self, layer_key_name):
        def resetTabColor():
            layer_name = self._layers[layer_key_name][LayerKeys.NAME]
            self._layers[layer_key_name][LayerKeys.TAB_COLOR] = self.DEFAULT_TAB_COLOR
            index = self.getLayerIndex(layer_name)
            self._layer_tabs.setCurrentIndex(index)
            self._layer_tabs.setStyleSheet('''
                QTabBar::tab {{}}
                QTabBar::tab:selected {{background-color: {color}; border: 1px solid #777777; border-radius: 4px;}}
            '''.format(color=self._layers[layer_key_name][LayerKeys.TAB_COLOR]))
        return resetTabColor

    def layerTabMoved(self, to_index, from_index):
        layer_moved_name = self._layer_tabs.tabText(self._layer_tabs.currentIndex())
        self._layers_widget.clear()
        for tab_index in range(0, self._layer_tabs.count()):
            layer_name = self._layer_tabs.tabText(tab_index)
            self.addLayerListItem(layer_name, tab_index*-1)

    def changeActiveLayerTab(self, layer_name):
        self._active_layer = self.getLayerKeyName(layer_name)
        self._layer_tabs.setCurrentIndex(self.getLayerIndex(layer_name))
    
    def layerVisibility(self):
        for layer_key_name, layer_properties in self._layers.items():
            # VISIBLE
            if layer_properties[LayerKeys.LIST_ITEM].checkState():
                if not self._tiles._layers[layer_key_name][LayerKeys.VISIBLE]:
                    self._tiles._scene.addItem(self._tiles._layers[layer_key_name][LayerKeys.ITEM_GROUP])
                    self._tiles._layers[layer_key_name][LayerKeys.VISIBLE] = True 
            else:
                if self._tiles._layers[layer_key_name][LayerKeys.VISIBLE]:
                    self._tiles._scene.removeItem(self._tiles._layers[layer_key_name][LayerKeys.ITEM_GROUP])
                    self._tiles._layers[layer_key_name][LayerKeys.VISIBLE] = False
    
    def getLayerKeyNameFromItem(self, item):
        for layer_key, layer_properties in self._layers.items():
            if layer_properties[LayerKeys.LIST_ITEM] == item:
                return layer_key
        return None 
    
    def getLayerNameFromItem(self, item):
        for layer_key, layer_properties in self._layers.items():
            if layer_properties[LayerKeys.LIST_ITEM] is item:
                return layer_properties[LayerKeys.NAME]
        return None 

    def leftClickLayerMenu(self, x, y, widget):
        old_layer_name = ""
        if isinstance(widget, QListWidget):
            item = widget.itemAt(QPoint(x,y))
            old_layer_name = self.getLayerNameFromItem(item)
        elif isinstance(widget, QTabBar):
            index = self._layer_tabs.tabAt(QPoint(x,y))
            if index > -1:
                old_layer_name = self.getLayerName(index)
        layer_key_name = self.getLayerKeyName(old_layer_name)
        menu = QMenu(self._parent)
        rename_action = QAction("Rename Layer", self._parent)
        rename_action.triggered.connect(self._changeLayerName(old_layer_name))
        change_color_action = QAction("Change Tab Color", self._parent)
        change_color_action.triggered.connect(self._changeTabColor(layer_key_name))
        reset_color_action = QAction("Reset Tab Color", self._parent)
        reset_color_action.triggered.connect(self._resetTabColor(layer_key_name))
        menu.addSection("Layer Options")
        menu.addAction(rename_action)
        menu.addAction(change_color_action)
        menu.addAction(reset_color_action)
        menu.exec_(widget.mapToGlobal(QPoint(x, y)))

    def doubleClickLayerItem(self):
        if not self._tab_change:
            if "Selected" not in self._layers_widget.currentItem().text():
                layer_name = self._layers_widget.currentItem().text()
                layer_key_name = self.getLayerKeyName(layer_name)
                self._list_change = True
                for lkn in self._layers:
                    ln = self._layers[lkn][LayerKeys.NAME]
                    self._layers[lkn][LayerKeys.LIST_ITEM].setText(ln)
                self._layers[layer_key_name][LayerKeys.LIST_ITEM].setText(layer_name+" (Selected)")
                self._tiles._current_layer = layer_key_name
                self.changeActiveLayerTab(layer_name)
                self._list_change = False 

    def getNewTabIndex(self):
        index = 1
        layer = "Layer"
        new_layer_key = ' '.join([layer,str(index)])
        while new_layer_key in self._layers.keys():
            index += 1
            new_layer_key = ' '.join([layer,str(index)])
        return index

    def addNewLayerTab(self):
        if not self._list_change:
            self._add_tab_index = self.getNewTabIndex()
            layer_name = " ".join(["Layer", str(self._add_tab_index)])
            layer_item = QListWidgetItem(layer_name)
            layer_item.setFlags(layer_item.flags() | Qt.ItemIsUserCheckable)
            layer_item.setCheckState(Qt.Checked)
            self._layers_widget.addItem(layer_item)
            self._layers[layer_name] = {LayerKeys.NAME: layer_name, LayerKeys.LIST_ITEM: layer_item, LayerKeys.REMOVABLE: True, LayerKeys.TAB_COLOR: self.DEFAULT_TAB_COLOR}
            
            # ADD LAYER TO TILES 
            self._tiles.createNewLayer(layer_name)

            # ADD LAYER TAB INDEX TO TAB NAME KEYS 
            tab_index = self._layer_tabs.addTab(layer_name)

            self.lockTabs()
 
    # switching the active layer when clicking on a tab. 
    def changeTabLayer(self, index):
        if not self._list_change:
            self._tab_change = True 
            layer_name = self.getLayerName(index)
            layer_key_name = self.getLayerKeyName(layer_name)
            self._active_layer = self.getLayerKeyName(layer_name)
            for lkn in self._layers:
                ln = self._layers[lkn][LayerKeys.NAME]
                self._layers[lkn][LayerKeys.LIST_ITEM].setText(ln)
            self._layers[self._active_layer][LayerKeys.LIST_ITEM].setText(layer_name+" (Selected)")
            self._tiles._current_layer = self._active_layer
            self._layer_tabs.setCurrentIndex(self.getLayerIndex(layer_name))
            self._layer_tabs.setStyleSheet('''
                QTabBar::tab {{}}
                QTabBar::tab:selected {{background-color: {color}; border: 1px solid #777777; border-radius: 4px;}}
            '''.format(color=self._layers[layer_key_name][LayerKeys.TAB_COLOR]))
            self._tab_change = False

    # Returns the layer tab widget.
    def getTabs(self):
        return self._layer_tabs_row