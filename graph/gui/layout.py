from PyQt5.QtWidgets import QHBoxLayout, QGraphicsScene
from PyQt5.QtGui import QPainter

from graph.model.graph import Graph

from .view import View
from .side_panel import SidePanel

class MainLayout():
    def __init__(self) -> None:
        self.main_layout = QHBoxLayout()
        self.graph = Graph()

        scene = QGraphicsScene()   # QGraphicsScene where the vertices and edges are rendered
        self.workspace = View(self.graph, scene)
        self.workspace.setStyleSheet("background-color: #8f8f8f")
        self.workspace.setRenderHint(QPainter.Antialiasing)

        self.side_panel = SidePanel(self.graph, scene)

        self.main_layout.addLayout(self.side_panel)
        self.main_layout.addWidget(self.workspace, stretch=1)