from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

from graph.model.graph import Graph

class View(QtWidgets.QGraphicsView):
    def __init__(self, graph: Graph, layout: QtWidgets.QVBoxLayout, updateSidePanel, updateMenu):
        super().__init__(graph)
        self.graph = graph
        self.graph.setSceneRect(0, 0, 1280, 840)  # Size of the scene
        self.graph.selectionChanged.connect(self.selectPoint)

        self.updateSidePanel = updateSidePanel
        self.updateMenu = updateMenu

        self.doneButton = QtWidgets.QPushButton()
        self.doneButton.setText("Done")
        self.doneButton.setFixedSize(QtCore.QSize(80, 30))
        self.doneButton.setVisible(False)
        self.doneButton.clicked.connect(self.doneButtonCallback)

        layout.addWidget(self.doneButton, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        layout.addWidget(self, stretch=1)
    
        self.setStyleSheet("background-color: #8f8f8f")
        self.setRenderHint(QtGui.QPainter.Antialiasing)           

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
        self.graph.createEdge()
        self.graph.useDjisktra()
        self.updateSidePanel()
        self.graph.showPath(None, None)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.doneButtonCallback()
        else:
            super().keyPressEvent(event)

    def update(self):
        self.graph.update()
        self.updateSidePanel()
        super().update()

    def setAdding(self, isAdding: bool):
        self.graph.unSelectItems()
        self.doneButton.setVisible(isAdding)
        if not isAdding:
            self.graph.isAddingVertex = isAdding
            self.graph.isAddingEdge = isAdding
        self.updateSidePanel()

    def findPath(self, algorithm):
        self.graph.unSelectItems()
        self.graph.setHighlightItems(False)

        if algorithm == "djikstra":
            self.doneButton.setVisible(True)
            self.graph.isUsingDjisktra = True
            self.graph.isUsingFloyd = False
            self.graph.floyd.reset()
            self.graph.useDjisktra()
        elif algorithm == "floyd":
            self.doneButton.setVisible(True)
            self.graph.isUsingDjisktra = False
            self.graph.isUsingFloyd = True
            self.graph.djisktra.reset()
            self.graph.useFloyd()
        else:
            self.doneButton.setVisible(False)
            self.graph.isUsingDjisktra = False
            self.graph.isUsingFloyd = False
        self.update()
        
    def doneButtonCallback(self):
        if self.graph.isAddingEdge or self.graph.isAddingVertex:
                self.setAdding(False)
        if self.graph.isUsingDjisktra or self.graph.isUsingFloyd:
            self.findPath(None)
            self.graph.showPath(None, None)
        self.update()
        self.updateMenu()
