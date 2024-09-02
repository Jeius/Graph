from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton

class SidePanel(QVBoxLayout):
    textbox_size = QSize(70, 30)

    def __init__(self, graph, scene):
        super().__init__()
        self.graph = graph  # Graph object
        self.scene = scene

        self.row = QHBoxLayout()  # Layout for buttons and graph info
        
        matrix_label = QLabel("Adjacency Matrix")
        self.matrix_textbox = QTextEdit()
        self.matrix_textbox.setWordWrapMode(QTextOption.NoWrap)
        self.matrix_textbox.setReadOnly(True)

        self.row.addLayout(self.buttons())
        self.row.addLayout(self.graphInfo())

        self.addLayout(self.row)
        self.addSpacing(20)
        self.addWidget(matrix_label)
        self.addWidget(self.matrix_textbox, stretch=2)


    def graphInfo(self):
        # Displays the graph order and size
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()

        size_label = QLabel("Size")
        order_label = QLabel("Order")

        self.size_textbox = QTextEdit()
        self.size_textbox.setFixedSize(self.textbox_size)
        self.size_textbox.setReadOnly(True)

        self.order_textbox = QTextEdit()
        self.order_textbox.setFixedSize(self.textbox_size)
        self.order_textbox.setReadOnly(True)

        row1.addWidget(order_label, alignment=Qt.AlignRight, stretch=1)
        row1.addWidget(self.order_textbox)
        row2.addWidget(size_label, alignment=Qt.AlignRight, stretch=1)
        row2.addWidget(self.size_textbox)
        
        layout.addLayout(row1)
        layout.addLayout(row2)

        return layout
    
    
    def buttons(self):
        button_size = QSize(100, 30)
        layout = QVBoxLayout()

        self.vertex = QPushButton("Add vertex")
        self.edge = QPushButton("Add edge")
        self.delete = QPushButton("Delete")

        self.vertex.setFixedSize(button_size)
        self.vertex.clicked.connect(self.addVertex)
        self.vertex.setCursor(Qt.PointingHandCursor)

        self.edge.setFixedSize(button_size)
        self.edge.clicked.connect(self.addEdge)
        self.edge.setCursor(Qt.PointingHandCursor)

        self.delete.setFixedSize(button_size)
        self.delete.clicked.connect(self.deleteSelected)
        self.delete.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.vertex, alignment=Qt.AlignLeft)
        layout.addWidget(self.edge, alignment=Qt.AlignLeft)
        layout.addWidget(self.delete, alignment=Qt.AlignLeft)

        return layout
    
    def addVertex(self):
        self.graph.is_adding_vertex = not self.graph.is_adding_vertex
        self.graph.is_adding_edge = False
        self.update()

    def addEdge(self):
        self.graph.is_adding_edge = not self.graph.is_adding_edge
        self.graph.is_adding_vertex = False
        self.update()

    def matrix(self):
        size = len(self.graph.vertices)
        if size == 0:
            return

        matrix = [[0 for _ in range(size)] for _ in range(size)]  # Intiallize matrix with zeros
        self.matrix_textbox.clear()  # Clean the textbox of the matrix
        vertex_id_to_index = {vertex.id: index for index, vertex in enumerate(self.graph.vertices)}

        for vertex in self.graph.vertices:
            for edge in vertex.edges:
                # Find the index of the connected vertices
                indexA = vertex_id_to_index[edge.vertexA.id]
                indexB = vertex_id_to_index[edge.vertexB.id]

                # Set the corresponding entries in the matrix to 1
                matrix[indexA][indexB] = 1
                matrix[indexB][indexA] = 1 
        
        for row in matrix:
            self.matrix_textbox.append(' '.join(map(str, row)))

    def deleteSelected(self):
        # Delete the selected items from the graph
        for vertex in self.graph.vertices[:]:  # Iterate from a copy
            if vertex.isSelected():
                self.graph.vertices.remove(vertex)
                self.scene.removeItem(vertex)
                
                for edge1 in vertex.edges:
                    neighbor = edge1.getOpposite(vertex)

                    for edge in neighbor.edges[:]:
                        if edge.getOpposite(neighbor) == vertex:
                            neighbor.edges.remove(edge)
                            self.graph.edges.remove(edge)
                            self.scene.removeItem(edge)
                            del edge
            del vertex

        for edge in self.graph.edges[:]: # Iterate from a copy
            if edge.isSelected():
                edge.vertexA.edges.remove(edge)
                edge.vertexB.edges.remove(edge)
                self.graph.edges.remove(edge)
                self.scene.removeItem(edge)
                del edge

        self.update()

    def update(self):
        # Update the textboxes
        self.order_textbox.setText(str(len(self.graph.vertices)))
        self.size_textbox.setText(str(len(self.graph.edges)))

        # Unselect selected vertices
        self.graph.selected_vertices.clear()
        for item in self.scene.selectedItems():
            item.setSelected(False)

        # Update Matrix
        self.matrix()

        # Update Degrees
        for vertex in self.graph.vertices:
            vertex.update()

        # Update Button Color
        if self.graph.is_adding_vertex:   # Change the add vertex button color
            self.vertex.setStyleSheet("background-color: #50c04e")
        else:
            self.vertex.setStyleSheet("background-color: #3a3a3a")

        if self.graph.is_adding_edge:   # Change the add edge button color
            self.edge.setStyleSheet("background-color: #50c04e")
        else:
            self.edge.setStyleSheet("background-color: #3a3a3a")

