from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsScene

from graph.model.graph_model import Graph

class Workspace(QGraphicsView):
    def __init__(self, graph: Graph, scene: QGraphicsScene):
        super().__init__(scene)
        self.scene = scene
        self.scene.setSceneRect(0, 0, 1280, 840)  # Size of the scene
        self.scene.selectionChanged.connect(self.selectPoint)

        self.graph = graph
        
    def mousePressEvent(self, event):
        # Get the position where the mouse was clicked
        if event.button() == Qt.LeftButton and self.graph.is_adding_vertex:  # Check if the left mouse button was clicked
            click_position = event.pos()  # Get the position in view coordinates
            scene_position = self.mapToScene(click_position)  # Convert to scene coordinates
            
            self.graph.createVertex(scene_position)  # Add a vertex to the vertices
            
            self.updateWorkspace()  

        elif event.button() == Qt.RightButton:  # Check if the right mouse button was clicked
            for item in self.scene.selectedItems():
                item.setSelected(False)

        # Call the parent class's mousePressEvent to ensure default behavior
        super().mousePressEvent(event)
        

    def paintEvent(self, event):
        # Enable antialiasing to smoothen the edges
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing, True)
        super().paintEvent(event)

    def selectPoint(self):
        # If not adding edge, stops the function
        if not self.graph.is_adding_edge:
            return

        if len(self.scene.selectedItems()) == 0:
            self.graph.selected_vertices.clear()

        # Loop through all selected items in the scene
        for item in self.scene.selectedItems():
            if isinstance(item, QGraphicsEllipseItem):
                line = self.graph.createEdge(item)
                if isinstance(line, QGraphicsLineItem):
                    self.scene.addItem(line)
                    item.setSelected(False)
        
    def updateWorkspace(self):
        # Clear the workspace first
        for item in self.scene.items():
            self.scene.removeItem(item)

        # Add vertices to the scene
        for vertex in self.graph.vertices:
            vertex.addLabel()
            self.scene.addItem(vertex)
                
        # Add edges to the scene
        for edge in self.graph.edges:
            self.scene.addItem(edge)