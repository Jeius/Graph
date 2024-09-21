from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

from graph.model.graph import Graph

class View(QtWidgets.QGraphicsView):
    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.graph = graph
        self.graph.setSceneRect(0, 0, 1280, 840)  # Size of the scene
        self.graph.selectionChanged.connect(self.selectPoint)
        self.setStyleSheet("background-color: #8f8f8f")
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
    def mousePressEvent(self, event):
        # Get the position where the mouse was clicked
        if event.button() == Qt.LeftButton and self.graph.isAddingVertex:  # Check if the left mouse button was clicked
            click_position = event.pos()  # Get the position in view coordinates
            scene_position = self.mapToScene(click_position)  # Convert to scene coordinates
            
            self.graph.createVertex(scene_position)  # Add a vertex to the vertices
            
            self.update()  

        elif event.button() == Qt.RightButton:  # Check if the right mouse button was clicked
            for item in self.graph.selectedItems():
                item.setSelected(False)

        # Call the parent class's mousePressEvent to ensure default behavior
        super().mousePressEvent(event)
        
    def paintEvent(self, event):
        # Enable antialiasing to smoothen the edges
        painter = QtGui.QPainter(self.viewport())
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        super().paintEvent(event)

    def selectPoint(self):
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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.graph.isAddingEdge or self.graph.isAddingVertex:
                self.graph.isAddingVertex = False
                self.graph.isAddingEdge = False

                for item in self.graph.selectedItems():
                    item.setSelected(False)
        else:
            super().keyPressEvent(event)

    def update(self):
        # Clear the workspace first
        for item in self.graph.items():
            self.graph.removeItem(item)

        # Add vertices to the scene
        for vertex in self.graph.vertices:
            vertex.addLabel()
            self.graph.addItem(vertex)
                
        # Add edges to the scene
        for edge in self.graph.edges:
            self.graph.addItem(edge)