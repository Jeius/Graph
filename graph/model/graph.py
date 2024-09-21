from typing import List
from PyQt5 import QtGui, QtWidgets, QtCore

from .vertex import Vertex
from .edge import Edge

class Graph(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.vertices: List[Vertex] = []  # List of the vertices
        self.selected_vertices: List[Vertex] = []   # List of the selected vertices
        self.edges: List[Edge] = []     # List of edges
        self.adj_matrix = []     # Adjacency matrix

        self.isAddingVertex = False  # Flag to enable adding vertex
        self.isAddingEdge = False    # Flag to enable adding edge

    def createVertex(self, scene_position: QtCore.QPointF):
        # Define the diameter of the circle
        diameter = 30
        radius = diameter / 2
        position = QtCore.QPointF(scene_position.x() - radius, scene_position.y() - radius)
        
        ellipse = Vertex(self.getId(), 0, 0, diameter, diameter)
        ellipse.setPos(position)  # Position

        self.vertices.append(ellipse)

        return ellipse
    
    def hasDuplicate(self, new_edge: Edge):
        for edge in self.edges:
            if new_edge == edge:
                return True
        
        return False
    
    def getDuplicate(self, new_edge: Edge):
        for edge in self.edges:
            if new_edge == edge:
                return edge

    def createEdge(self, vertex: Vertex):
        if len(self.selected_vertices) == 0:
            self.selected_vertices.append(vertex)
            return
        else:
            vertexA = self.selected_vertices.pop()
            vertexB = vertex
            edge = Edge(vertexA, vertexB)
            
            if not self.hasDuplicate(edge):
                vertexA.addEdge(edge)
                vertexB.addEdge(edge)
                self.edges.append(edge)
                return edge
            else:
                return

    def getId(self):
        if len(self.vertices) == 0:
            return 1
        else:
            return self.vertices[-1].id + 1
        
    def clear(self):
        self.vertices.clear()
        self.adj_matrix.clear()
        self.edges.clear()

    def getComplement(self):
        self.edges.clear()

        for vertex in self.vertices:
            neighbors = []
            for edge in vertex.edges:
                neighbor = edge.getOpposite(vertex)
                neighbors.append(neighbor)
            
            complement_vertices = [v for v in self.vertices if v not in neighbors and v != vertex]
            vertex.edges.clear()

            for complement_vertex in complement_vertices:
                complement_edge = Edge(vertex, complement_vertex)

                if not self.hasDuplicate(complement_edge):
                    self.edges.append(complement_edge)
                    vertex.addEdge(complement_edge)
                else:
                    vertex.addEdge(self.getDuplicate(complement_edge))
    
  