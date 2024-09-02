from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsEllipseItem

class Workspace(QGraphicsView):
    def __init__(self, scene, graph):
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
            
            # Add the circle to the scene
            self.scene.addItem(self.graph.addVertex(scene_position))

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
                line = self.graph.addEdge(item)
                if line != None:
                    self.scene.addItem(line)
                    item.setSelected(False)
        