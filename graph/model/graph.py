import math
from typing import List
from PyQt5 import QtGui, QtWidgets, QtCore

from .vertex import Vertex
from .edge import Edge
from ..algorithm.djisktra import Djisktra
from ..algorithm.floyd import FloydWarshall

class Graph(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.vertices: List[Vertex] = []  # List of the vertices
        self.selected_vertices: List[Vertex] = []   # List of the selected vertices
        self.edges: List[Edge] = []     # List of edges
        self.adjacencyMatrix: list[list[float]] = []     # Adjacency matrix
        
        self.djisktra = Djisktra(self.vertices)
        self.floyd = FloydWarshall(self.vertices)

        self.isAddingVertex = False  # Flag to enable adding vertex
        self.isAddingEdge = False    # Flag to enable adding edge
        self.isUsingDjisktra = False  # Flag to enable djisktra algorithm
        self.isUsingFloyd = False     # Flag to enable floyd algorithm

    def createVertex(self, scene_position: QtCore.QPointF):
        # Define the diameter of the circle
        diameter = 30
        radius = diameter / 2
        position = QtCore.QPointF(scene_position.x() - radius, scene_position.y() - radius)
        
        vertex = Vertex(self.createID(), 0, 0, diameter, diameter)
        vertex.setPos(position)  # Position

        self.vertices.append(vertex)

        return vertex
    
    def createAdjMatrix(self):
        # Terminate the execution if there are no vertices
        size = len(self.vertices)
        if size == 0:
            return

        # Intiallize matrix with zeros
        self.adjacencyMatrix = [[math.inf for _ in range(size)] for _ in range(size)]  

        # Create a dictionary of index values with the vertex ids as keys
        idToIndex = {vertex.id: index for index, vertex in enumerate(self.vertices)}

        for vertex in self.vertices:
            for edge in vertex.edges:
                # Find the index of the connected vertices
                indexA = idToIndex[edge.vertexA.id]
                indexB = idToIndex[edge.vertexB.id]
                
                if edge.weight != math.inf:
                    self.adjacencyMatrix[indexA][indexB] = edge.weight
                    self.adjacencyMatrix[indexB][indexA] = edge.weight
        
                self.adjacencyMatrix[indexA][indexA] = 0
                self.adjacencyMatrix[indexB][indexB] = 0               

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

    def createID(self):
        if len(self.vertices) == 0:
            return 1
        else:
            return self.vertices[-1].id + 1

    def delete(self):
        # Delete the selected items from the graph
        # Iterate from the vertices if the selected item is a vertex
        for vertex in self.vertices.copy():  # Iterate from a copy
            if vertex.isSelected():
                # Remove from the list of vertices
                self.vertices.remove(vertex) 
                
                # Also remove the edges from its neighbor that was connected 
                # to the vertex
                for vertex_edge in vertex.edges:
                    neighbor = vertex_edge.getOpposite(vertex)

                    for neighbor_edge in neighbor.edges.copy():
                        # Get the opposite of the neighbor, this means that 
                        # the opposite will most likely be the vertex
                        v = neighbor_edge.getOpposite(neighbor)

                        # Check if it is true, 
                        # then remove the edge in the neighbor's edges
                        if v == vertex:
                            neighbor_edge in neighbor.edges and neighbor.edges.remove(neighbor_edge)
                            neighbor_edge in self.edges and self.edges.remove(neighbor_edge)
                            del neighbor_edge   # Deleting the edge to save memory
            del vertex  # Deleting the vertex to save memory

        # Iterate from the edges if the selected item is an edge
        for edge in self.edges.copy(): # Iterate from a copy
            if edge.isSelected():
                # Remove the edge in both endpoints
                edge in edge.vertexA.edges and edge.vertexA.edges.remove(edge)
                edge in edge.vertexB.edges and edge.vertexB.edges.remove(edge)
                self.edges.remove(edge)
                del edge

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
    
    def getDuplicate(self, new_edge: Edge):
        for edge in self.edges:
            if new_edge == edge:
                return edge 

    def hasDuplicate(self, new_edge: Edge):
        for edge in self.edges:
            if new_edge == edge:
                return True
        return False

    def reset(self):
        self.vertices.clear()
        self.adjacencyMatrix.clear()
        self.edges.clear()
        self.isAddingEdge = False
        self.isAddingVertex = False
        self.isUsingDjisktra = False

    def showPath(self, start: Vertex | None, goal: Vertex | None):
        # Unhighlight items first
        self.setHighlightItems(False)

        if start == None and goal == None:
            return
        
        # Select the start and highlight the goal
        goal.setHighlight(True, 1)
        start.setHighlight(True, 0)

        try:
            if self.isUsingFloyd:
                paths = self.floyd.paths
                if not paths:
                    return
                startIndex = self.vertices.index(start)
                goalIndex = self.vertices.index(goal)
                path = list(paths[(startIndex, goalIndex)])

                while len(path) > 1:
                    vertexA = self.vertices[path.pop(0)]
                    vertexB = self.vertices[path[0]]
                    newEdge = Edge(vertexA, vertexB)
                    edge = self.getDuplicate(newEdge)
                    if edge is not None:
                        edge.setHighlight(True)

            elif self.isUsingDjisktra:
                paths = self.djisktra.paths
                if not paths:
                    return
                path = list(paths[self.vertices.index(goal)])

                while len(path) > 1:
                    vertexA = self.vertices[path.pop(0)]
                    vertexB = self.vertices[path[0]]
                    newEdge = Edge(vertexA, vertexB)
                    edge = self.getDuplicate(newEdge)
                    if edge is not None:
                        edge.setHighlight(True)
        except Exception as e:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle("Invalid Path")
            msg_box.setText("No path found.")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.exec_()

        for item in self.items():
            item.update()
                
    def unSelectItems(self):
        for item in self.selectedItems():
            item.setSelected(False)

    def setHighlightItems(self, flag: bool):
        for edge in self.edges:
            edge.setHighlight(flag)
        for vertex in self.vertices:
            vertex.setHighlight(flag, None)

    def useDjisktra(self):
        if self.isUsingDjisktra:
            for item in self.selectedItems():
                if isinstance(item, Vertex):
                    self.djisktra.findPath(item, self.adjacencyMatrix)

    def useFloyd(self):
        if self.isUsingFloyd:
            self.floyd.findPath(self.adjacencyMatrix)

    def update(self):
        # Clear the view first
        for item in self.items():
            self.removeItem(item)

        # Add vertices to the scene
        for vertex in self.vertices:
            self.addItem(vertex)
            vertex.update()
                
        # Add edges to the scene
        for edge in self.edges:
            self.addItem(edge)
            edge.update()

        super().update()