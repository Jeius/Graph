import math
from typing import List
from PyQt5 import QtWidgets, QtCore

from .vertex import Vertex
from .edge import Edge
from ..algorithm.djisktra import Djisktra
from ..algorithm.floyd import FloydWarshall

class Graph(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.vertices: List[Vertex] = []  # List of the vertices
        self.selected_vertices: List[Vertex] = []  # List of selected vertices
        self.edges: List[Edge] = []  # List of edges
        self.adjacency_matrix: List[List[float]] = []  # Adjacency matrix

        self.dijkstra = Djisktra(self.vertices)
        self.floyd_warshall = FloydWarshall(self.vertices)

        self.is_adding_vertex = False  # Flag to enable adding vertex
        self.is_adding_edge = False  # Flag to enable adding edge
        self.is_using_dijsktra = False  # Flag to enable Dijkstra algorithm
        self.is_using_floyd = False  # Flag to enable Floyd-Warshall algorithm

    def create_vertex(self, scene_position: QtCore.QPointF) -> Vertex:
        """Create a vertex at a specified position."""
        diameter = 30
        radius = diameter / 2
        position = QtCore.QPointF(scene_position.x() - radius, scene_position.y() - radius)

        vertex = Vertex(self._create_id(), 0, 0, diameter, diameter)
        vertex.setPos(position)  # Position
        self.vertices.append(vertex)
        return vertex

    def create_adjacency_matrix(self) -> None:
        """Create the adjacency matrix based on vertices and edges."""
        size = len(self.vertices)
        if size == 0:
            return

        self.adjacency_matrix = [[math.inf] * size for _ in range(size)]
        id_to_index = {vertex.id: index for index, vertex in enumerate(self.vertices)}

        for vertex in self.vertices:
            for edge in vertex.edges:
                if vertex == edge.start_vertex:
                    index_a = id_to_index[edge.start_vertex.id]
                    index_b = id_to_index[edge.end_vertex.id]

                    if edge.weight != math.inf:
                        self.adjacency_matrix[index_a][index_b] = edge.weight

                # Set diagonal to zero
                self.adjacency_matrix[index_a][index_a] = 0
                self.adjacency_matrix[index_b][index_b] = 0

    def create_edge(self) -> None:
        """Create an edge between selected vertices."""
        if not self.is_adding_edge:
            return

        if not self.selectedItems():
            self.selected_vertices.clear()

        for item in self.selectedItems():
            if isinstance(item, Vertex):
                vertex = item
                if not self.selected_vertices:
                    self.selected_vertices.append(vertex)
                else:
                    start = self.selected_vertices.pop()
                    end = vertex
                    edge = Edge(start, end)

                    if self._has_duplicate(edge):
                        return

                    self.edges.append(edge)
                    start.add_edge(edge)
                    end.add_edge(edge)
                    self.addItem(edge)
                    self._set_curved_edge(edge)
                vertex.setSelected(True)

    def _set_curved_edge(self, edge: Edge) -> None:
        """Set the edge to be curved if it has a duplicate."""
        start = edge.start_vertex
        end = edge.get_opposite(start)
        opposite_edge = Edge(end, start)

        if self._has_duplicate(opposite_edge):
            edge.is_curve = True
            self._get_duplicate(opposite_edge).is_curve = True
        else:
            edge.is_curve = False

    def _create_id(self) -> int:
        """Create a new unique ID for a vertex."""
        return 1 if not self.vertices else self.vertices[-1].id + 1

    def delete_selected(self) -> None:
        """Delete selected items from the graph."""
        for vertex in self.vertices.copy():
            if vertex.isSelected():
                self.vertices.remove(vertex)
                self._remove_edges(vertex)

        for edge in self.edges.copy():
            if edge.isSelected():
                self._remove_edge(edge)

    def _remove_edges(self, vertex: Vertex) -> None:
        """Remove edges associated with a given vertex."""
        for vertex_edge in vertex.edges:
            neighbor = vertex_edge.get_opposite(vertex)
            for neighbor_edge in neighbor.edges.copy():
                if neighbor_edge.get_opposite(neighbor) == vertex:
                    neighbor.remove_edge(neighbor_edge)
                    self.edges.remove(neighbor_edge)

    def _remove_edge(self, edge: Edge) -> None:
        """Remove a specified edge from the graph."""
        edge.start_vertex.edges.remove(edge)
        edge.end_vertex.edges.remove(edge)
        self.edges.remove(edge)

    def _remove_items(self):
        for item in self.items():
            self.removeItem(item)

    def get_complement(self) -> None:
        """Get the complement of the graph."""
        self.edges.clear()

        for vertex in self.vertices:
            neighbors = {edge.get_opposite(vertex) for edge in vertex.edges}
            complement_vertices = [v for v in self.vertices if v not in neighbors and v != vertex]
            vertex.edges.clear()

            for complement_vertex in complement_vertices:
                complement_edge = Edge(vertex, complement_vertex)
                if not self._has_duplicate(complement_edge):
                    self.edges.append(complement_edge)
                    vertex.add_edge(complement_edge)
                else:
                    vertex.add_edge(self._get_duplicate(complement_edge))

    def _get_duplicate(self, new_edge: Edge) -> Edge:
        """Get a duplicate edge if it exists."""
        return next((edge for edge in self.edges if new_edge == edge), None)

    def _has_duplicate(self, new_edge: Edge) -> bool:
        """Check if the edge already exists."""
        return any(new_edge == edge for edge in self.edges)

    def reset(self) -> None:
        """Reset the graph to its initial state."""
        self.vertices.clear()
        self.adjacency_matrix.clear()
        self.edges.clear()
        self.is_adding_edge = False
        self.is_adding_vertex = False
        self.is_using_dijsktra = False

    def show_path(self, start: Vertex | None, goal: Vertex | None) -> None:
        """Highlight the path from start to goal using the chosen algorithm."""
        self.set_highlight_items(False)

        if not start or not goal:
            return

        goal.set_highlight(True, 1)
        start.set_highlight(True, 0)

        try:
            paths = None
            if self.is_using_floyd:
                paths = self.floyd_warshall.paths
            elif self.is_using_dijsktra:
                paths = self.dijkstra.paths

            if not paths:
                return

            path = list(paths[(self.vertices.index(start), self.vertices.index(goal))]) if self.is_using_floyd else list(paths[self.vertices.index(goal)])

            while len(path) > 1:
                start = self.vertices[path.pop(0)]
                end = self.vertices[path[0]]
                edge = self._get_duplicate(Edge(start, end))
                if edge is not None:
                    edge.is_highlighted = True

        except Exception:
            self._show_invalid_path()

        for item in self.items():
            item.update()

    def _show_invalid_path(self) -> None:
        """Show a message box indicating no path was found."""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setWindowTitle("Invalid Path")
        msg_box.setText("No path found.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()

    def unselect_items(self) -> None:
        """Unselect all selected items."""
        for item in self.selectedItems():
            item.setSelected(False)

    def set_highlight_items(self, flag: bool) -> None:
        """Set highlight status for edges and vertices."""
        for edge in self.edges:
            edge.is_highlighted = flag
        for vertex in self.vertices:
            vertex.set_highlight(flag, None)

    def use_dijkstra(self) -> None:
        """Use Dijkstra's algorithm to find paths."""
        if self.is_using_dijsktra:
            for item in self.selectedItems():
                if isinstance(item, Vertex):
                    self.dijkstra.find_path(item, self.adjacency_matrix)

    def use_floyd(self) -> None:
        """Use Floyd-Warshall algorithm to find paths."""
        if self.is_using_floyd:
            self.floyd_warshall.find_path(self.adjacency_matrix)

    def update(self) -> None:
        """Update the scene to reflect the current state of vertices and edges."""
        self._remove_items()
        
        for vertex in self.vertices:
            self.addItem(vertex)
            vertex.update()

        for edge in self.edges:
            self.addItem(edge)
            self._set_curved_edge(edge)
            edge.update()

        super().update()
