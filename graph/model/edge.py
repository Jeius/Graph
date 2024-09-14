from typing import List
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPen



class Edge(QGraphicsLineItem):
    from .vertex import Vertex
    def __init__(self, ellipseA: Vertex, ellipseB: Vertex):
        self.vertexA = ellipseA
        self.vertexB = ellipseB

        # Get the position of the two ellipses
        pointA = self.vertexA.getPosition()
        pointB = self.vertexB.getPosition()

        # Create a QGraphicsLineItem from centerA to centerB
        super().__init__(pointA.x(), pointA.y(), pointB.x(), pointB.y())
        
        self.setFlag(QGraphicsLineItem.ItemIsSelectable, True)  # Allow the item to be selectable
        self.setCursor(Qt.PointingHandCursor)  # Set the mouse cursor into pointing hand when hovering the edge
        self.setPen(QPen(Qt.black, 2))   # Set the edge color and thickness
        self.setZValue(0)  # Render the edge below the vertex

    def __eq__(self, other_edge):
        # Check if two edges are equal regardless of vertex order
        return (self.vertexA == other_edge.vertexA and self.vertexB == other_edge.vertexB) or \
               (self.vertexA == other_edge.vertexB and self.vertexB == other_edge.vertexA)
    
    def moveEndpoints(self):
        # Get the position of the two ellipses
        pointA = self.vertexA.getPosition()
        pointB = self.vertexB.getPosition()
        
        # Create a line
        new_line = QLineF(pointA, pointB)
        self.setLine(new_line)
    
    def getOpposite(self, vertex):
        # Return the neighbor of the vertex
        if vertex == self.vertexA:
            return self.vertexB
        else:
            return self.vertexA
        
    def paint(self, painter, option, widget=None):
        # Override the paint method to change the 
        # appearance of the edge when selected

        pen = QPen(Qt.black, 2)  # Default

        # Check if the item is selected
        if self.isSelected(): 
            pen = QPen(Qt.white, 2)  # Lightgreen fill

        # Apply the pen and brush
        painter.setPen(pen)
        painter.drawLine(self.line())
    