from PyQt5.QtWidgets import QHBoxLayout, QGraphicsScene
from PyQt5.QtGui import QPainter
from graph import Workspace, SidePanel, GraphModel

class MainLayout():
    def __init__(self) -> None:
        self.main_layout = QHBoxLayout()
        self.graph = GraphModel()

        scene = QGraphicsScene()   # QGraphicsScene where the vertices and edges are rendered
        self.workspace = Workspace(self.graph, scene)
        self.workspace.setStyleSheet("border: 2px solid #555555; background-color: #3a3a3a")
        self.workspace.setRenderHint(QPainter.Antialiasing)

        self.side_panel = SidePanel(self.graph, scene)

        self.main_layout.addLayout(self.side_panel)
        self.main_layout.addWidget(self.workspace, stretch=1)