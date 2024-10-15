from PyQt5 import QtCore, QtGui, QtWidgets
from ..model.graph import Graph

class SidePanel(QtWidgets.QVBoxLayout):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.addLayout(self.graph_info())
        self.addWidget(self.separator("horizontal"))
        self.addLayout(self.adj_matrix(), stretch=1)
        self.addWidget(self.separator("horizontal"))
        self.addLayout(self.path_table(), stretch=1)

    def graph_info(self):
        # Displays the graph order and size
        layout = QtWidgets.QGridLayout()
        small_size = QtCore.QSize(70, 30)
        medium_size = QtCore.QSize(180, 45)

        labels_and_boxes = [
            ("Order", small_size), 
            ("Size", small_size), 
            ("Vertex Set", medium_size), 
            ("Edge Set", medium_size)
        ]

        self.order_textbox = self.create_read_only_textbox(small_size)
        self.size_textbox = self.create_read_only_textbox(small_size)
        self.vertex_set_textbox = self.create_read_only_textbox(medium_size, line_wrap=QtWidgets.QTextEdit.NoWrap)
        self.edge_set_textbox = self.create_read_only_textbox(medium_size, line_wrap=QtWidgets.QTextEdit.NoWrap)

        textboxes = [self.order_textbox, self.size_textbox, self.vertex_set_textbox, self.edge_set_textbox]

        for (label, _), textbox in zip(labels_and_boxes, textboxes):
            layout.addWidget(QtWidgets.QLabel(label), layout.rowCount(), 0)
            layout.addWidget(textbox, layout.rowCount() - 1, 1)

        return layout

    def create_read_only_textbox(self, size: QtCore.QSize, line_wrap=None):
        textbox = QtWidgets.QTextEdit()
        textbox.setFixedSize(size)
        textbox.setReadOnly(True)
        if line_wrap is not None:
            textbox.setLineWrapMode(line_wrap)
        return textbox

    def adj_matrix(self):
        layout = QtWidgets.QVBoxLayout()
        matrix_label = QtWidgets.QLabel("Adjacency Matrix")

        self.matrix_table = QtWidgets.QTableWidget()
        self.matrix_table.setShowGrid(False)
        self.matrix_table.horizontalHeader().setVisible(False)
        self.matrix_table.verticalHeader().setVisible(False)

        layout.addWidget(matrix_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.matrix_table, stretch=1)
        return layout

    def path_table(self):
        layout = QtWidgets.QVBoxLayout()
        path_label = QtWidgets.QLabel("Path Table")
        self.path_table_widget = QtWidgets.QTableWidget()

        horizontal_headers = ["Start", "Goal", "Distance"]
        self.path_table_widget.setColumnCount(len(horizontal_headers))
        self.path_table_widget.setHorizontalHeaderLabels(horizontal_headers)
        self.path_table_widget.verticalHeader().sectionClicked.connect(self.path_table_callback)
        self.path_table_widget.resizeColumnsToContents()

        layout.addWidget(path_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.path_table_widget, stretch=1)
        return layout

    def path_table_callback(self, row_index):
        start_item = self.path_table_widget.item(row_index, 0)
        goal_item = self.path_table_widget.item(row_index, 1)

        if start_item is not None and goal_item is not None:
            start_vertex_id = int(start_item.text())
            goal_vertex_id = int(goal_item.text())

            start_vertex = self.get_vertex_by_id(start_vertex_id)
            goal_vertex = self.get_vertex_by_id(goal_vertex_id)

            if start_vertex and goal_vertex:
                self.graph.show_path(start_vertex, goal_vertex)

    def get_vertex_by_id(self, vertex_id):
        return next((v for v in self.graph.vertices if v.id == vertex_id), None)

    def separator(self, orientation):
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine if orientation == "horizontal" else QtWidgets.QFrame.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        return separator

    def update(self):
        self._update_matrix()
        self._update_path_table()
        self._update_textboxes()
        super().update()

    def _update_textboxes(self):
        self.order_textbox.setText(str(len(self.graph.vertices)))
        self.size_textbox.setText(str(len(self.graph.edges)))
        self._update_vertex_set()
        self._update_edge_set()

    def _update_vertex_set(self):
        vertex_set = {str(vertex.id) for vertex in self.graph.vertices}
        self.vertex_set_textbox.setPlainText("V(G) = {" + ', '.join(vertex_set) + '}')

    def _update_edge_set(self):
        edge_set = {f"({edge.start_vertex.id}, {edge.end_vertex.id})" for edge in self.graph.edges}
        self.edge_set_textbox.setPlainText("E(G) = {" + ', '.join(edge_set) + '}')

    def _update_matrix(self):
        self.graph.create_adjacency_matrix()
        self.matrix_table.clear()
        matrix = self.graph.adjacency_matrix

        self.matrix_table.setRowCount(len(matrix))
        self.matrix_table.setColumnCount(len(matrix[0]) if matrix else 0)

        for row_index, row in enumerate(matrix):
            for column_index, value in enumerate(row):
                self.matrix_table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(str(value)))

    def _update_path_table(self):
        if self.graph.is_using_dijsktra:
            self._update_path_table_dijkstra()
        else:
            self._update_path_table_floyd()

    def _update_path_table_dijkstra(self):
        self.path_table_widget.setRowCount(0)
        paths = self.graph.dijkstra.paths
        if not paths:
            return

        vertices = self.graph.vertices
        start_vertex = self.graph.dijkstra.start_vertex
        distances = self.graph.dijkstra.distances

        rows = len(vertices) - 1
        self.path_table_widget.setRowCount(rows)
        self.path_table_widget.setVerticalHeaderLabels(["Show Path"] * rows)

        row_index = 0
        for goal_vertex in vertices:
            if start_vertex != goal_vertex:
                self._add_path_table_row(row_index, start_vertex, goal_vertex, distances[vertices.index(goal_vertex)])
                row_index += 1

    def _add_path_table_row(self, row_index, start_vertex, goal_vertex, distance):
        start_item = self.create_table_widget_item(start_vertex.id)
        goal_item = self.create_table_widget_item(goal_vertex.id)
        distance_item = self.create_table_widget_item(distance)

        self.path_table_widget.setItem(row_index, 0, start_item)
        self.path_table_widget.setItem(row_index, 1, goal_item)
        self.path_table_widget.setItem(row_index, 2, distance_item)

    def create_table_widget_item(self, text):
        item = QtWidgets.QTableWidgetItem(str(text))
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        return item

    def _update_path_table_floyd(self):
        self.path_table_widget.setRowCount(0)
        paths = self.graph.floyd_warshall.paths
        if not paths:
            return

        vertices = self.graph.vertices
        distances = self.graph.floyd_warshall.distances

        rows = len(vertices) * (len(vertices) - 1)
        self.path_table_widget.setRowCount(rows)
        self.path_table_widget.setVerticalHeaderLabels(["Show Path"] * rows)

        row_index = 0
        for start_vertex in vertices:
            for goal_vertex in vertices:
                if start_vertex != goal_vertex:
                    start_index = vertices.index(start_vertex)
                    goal_index = vertices.index(goal_vertex)

                    self._add_path_table_row(row_index, start_vertex, goal_vertex, distances[start_index][goal_index])
                    row_index += 1
