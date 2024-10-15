from PyQt5 import QtCore, QtGui, QtWidgets
from graph.model.graph import Graph

class GraphView(QtWidgets.QGraphicsView):
    def __init__(self, graph: Graph, layout: QtWidgets.QVBoxLayout, update_side_panel, update_menu):
        super().__init__(graph)
        self.graph = graph
        self.graph.setSceneRect(0, 0, 1280, 840)  # Size of the scene
        self.graph.selectionChanged.connect(self.select_point)

        self.update_side_panel = update_side_panel
        self.update_menu = update_menu

        self.done_button = QtWidgets.QPushButton("Done")
        self.done_button.setFixedSize(QtCore.QSize(80, 30))
        self.done_button.setVisible(False)
        self.done_button.clicked.connect(self.done_button_callback)

        layout.addWidget(self.done_button, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        layout.addWidget(self, stretch=1)

        self.setStyleSheet("background-color: #8f8f8f")
        self.setRenderHint(QtGui.QPainter.Antialiasing)

    def mousePressEvent(self, event):
        """Handle mouse press events to add vertices or unselect items."""
        if event.button() == QtCore.Qt.LeftButton and self.graph.is_adding_vertex:
            click_position = event.pos()  # Get the position in view coordinates
            scene_position = self.mapToScene(click_position)  # Convert to scene coordinates
            self.graph.create_vertex(scene_position)  # Add a vertex to the graph
        elif event.button() == QtCore.Qt.RightButton:
            self.graph.unselect_items()

        self.update()  
        super().mousePressEvent(event)

    def paintEvent(self, event):
        """Enable antialiasing to smoothen the edges."""
        painter = QtGui.QPainter(self.viewport())
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        super().paintEvent(event)

    def select_point(self):
        """Select the point in the graph."""
        self.graph.create_edge()
        self.graph.use_dijkstra()
        self.update_side_panel()
        self.graph.show_path(None, None)

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == QtCore.Qt.Key_Escape:
            self.done_button_callback()
        else:
            super().keyPressEvent(event)

    def update(self):
        """Update the graph and side panel."""
        self.graph.update()
        self.update_side_panel()
        super().update()

    def set_adding(self, is_adding: bool):
        """Set the state of adding vertices or edges."""
        self.graph.unselect_items()
        self.done_button.setVisible(is_adding)
        if not is_adding:
            self.graph.is_adding_vertex = False
            self.graph.is_adding_edge = False
        self.update_side_panel()

    def find_path(self, algorithm: str):
        """Find a path using the specified algorithm."""
        self.graph.unselect_items()
        self.graph.set_highlight_items(False)

        if algorithm == "dijkstra":
            self.done_button.setVisible(True)
            self.graph.is_using_dijsktra = True
            self.graph.is_using_floyd = False
            self.graph.floyd_warshall.reset()
            self.graph.use_dijkstra()
        elif algorithm == "floyd":
            self.done_button.setVisible(True)
            self.graph.is_using_dijsktra = False
            self.graph.is_using_floyd = True
            self.graph.dijkstra.reset()
            self.graph.use_floyd()
        else:
            self.done_button.setVisible(False)
            self.graph.is_using_dijsktra = False
            self.graph.is_using_floyd = False

        self.update()

    def done_button_callback(self):
        """Handle the done button callback."""
        if self.graph.is_adding_edge or self.graph.is_adding_vertex:
            self.set_adding(False)
        
        if self.graph.is_using_dijsktra or self.graph.is_using_floyd:
            self.find_path(None)
            self.graph.show_path(None, None)

        self.update()
        self.update_menu()
