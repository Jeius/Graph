from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QBoxLayout, QGraphicsScene
from PyQt5.QtGui import QPainter
from graph import Workspace, SidePanel, GraphModel

class MainLayout():
    
    def __init__(self) -> None:
        self.main_layout = QHBoxLayout()
        self.graph = GraphModel()

        scene = QGraphicsScene()
        self.workspace = Workspace(scene, self.graph)
        self.workspace.setStyleSheet("border: 2px solid #555555; background-color: #3a3a3a")
        self.workspace.setRenderHint(QPainter.Antialiasing)

        self.side_panel = SidePanel(self.graph, scene)

        self.main_layout.addLayout(self.side_panel)
        self.main_layout.addWidget(self.workspace, stretch=1)