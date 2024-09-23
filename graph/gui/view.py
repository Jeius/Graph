from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

from graph.model.graph import Graph

class View(QtWidgets.QGraphicsView):
    def __init__(self, graph: Graph, layout: QtWidgets.QVBoxLayout, updateTopPanel):
        super().__init__(graph)
        self.graph = graph
        self.graph.setSceneRect(0, 0, 1280, 840)  # Size of the scene
        self.graph.selectionChanged.connect(self.selectPoint)

        self.updateTopPanel = updateTopPanel

        self.doneButton = QtWidgets.QPushButton()
        self.doneButton.setText("Done")
        self.doneButton.setFixedSize(QtCore.QSize(80, 30))
        self.doneButton.setVisible(False)
        self.doneButton.clicked.connect(self.doneButtonCallback)

        layout.addWidget(self.doneButton, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        layout.addWidget(self, stretch=1)
    
        self.setStyleSheet("background-color: #8f8f8f")
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
    def createEdge(self):
        # If not adding edge, stops the function
        if not self.graph.isAddingEdge:
            return

        if len(self.graph.selectedItems()) == 0:
            self.graph.selected_vertices.clear()

        # Loop through all selected items in the scene
        for item in self.graph.selectedItems():
            if isinstance(item, QtWidgets.QGraphicsEllipseItem):
                line = self.graph.createEdge(item)
                if isinstance(line, QtWidgets.QGraphicsLineItem):
                    self.graph.addItem(line)
                    item.setSelected(False)

    def findPath(self):
        from ..model.vertex import Vertex
        if self.graph.isSelectingVertex:
            for item in self.graph.selectedItems():
                if isinstance(item, Vertex):
                    self.graph.djisktra.findPath(item, self.graph.adjacencyMatrix)

    def mousePressEvent(self, event):
        # Get the position where the mouse was clicked
        if event.button() == Qt.LeftButton and self.graph.isAddingVertex: 
            click_position = event.pos()  # Get the position in view coordinates
            scene_position = self.mapToScene(click_position)  # Convert to scene coordinates
            
            self.graph.createVertex(scene_position)  # Add a vertex to the vertices
        elif event.button() == Qt.RightButton:  
            self.graph.unSelectItems()
        self.update()  
        super().mousePressEvent(event)
        
    def paintEvent(self, event):
        # Enable antialiasing to smoothen the edges
        painter = QtGui.QPainter(self.viewport())
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        super().paintEvent(event)

    def selectPoint(self):
        self.createEdge()
        self.findPath()
        self.updateTopPanel()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.graph.isAddingEdge or self.graph.isAddingVertex:
                self.setAdding(False)
            if self.graph.isSelectingVertex:
                self.useDjisktra(False)
        else:
            super().keyPressEvent(event)
        self.update()

    def update(self):
        self.graph.update()
        self.updateTopPanel()
        super().update()

    def setAdding(self, isAdding: bool):
        self.graph.unSelectItems()
        self.doneButton.setVisible(isAdding)
        if not isAdding:
            self.graph.isAddingVertex = isAdding
            self.graph.isAddingEdge = isAdding
        self.updateTopPanel()

    def useDjisktra(self, isSelecting: bool):
        self.doneButton.setVisible(isSelecting)
        self.graph.isSelectingVertex = isSelecting
        

    def doneButtonCallback(self):
        self.setAdding(False)
        self.useDjisktra(False)
        
