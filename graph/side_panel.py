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

        self.complement_button = QPushButton("Show Complement")
        self.complement_button.clicked.connect(self.toggleShowComplement)
        self.complement_button.setCursor(Qt.PointingHandCursor)
        self.addWidget(self.complement_button, alignment=Qt.AlignCenter)

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

        self.vertex_button = QPushButton("Add vertex")
        self.edge_button = QPushButton("Add edge")
        self.delete_button = QPushButton("Delete")
        self.clear_button = QPushButton("Clear All")

        self.vertex_button.setFixedSize(button_size)
        self.vertex_button.clicked.connect(self.toggleAddVertex)
        self.vertex_button.setCursor(Qt.PointingHandCursor)

        self.edge_button.setFixedSize(button_size)
        self.edge_button.clicked.connect(self.toggleAddEdge)
        self.edge_button.setCursor(Qt.PointingHandCursor)

        self.delete_button.setFixedSize(button_size)
        self.delete_button.clicked.connect(self.deleteSelected)
        self.delete_button.setCursor(Qt.PointingHandCursor)

        self.clear_button.setFixedSize(button_size)
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.vertex_button, alignment=Qt.AlignLeft)
        layout.addWidget(self.edge_button, alignment=Qt.AlignLeft)
        layout.addWidget(self.delete_button, alignment=Qt.AlignLeft)
        layout.addWidget(self.clear_button, alignment=Qt.AlignLeft)

        return layout
    
    def toggleAddVertex(self):
        self.graph.is_adding_vertex = not self.graph.is_adding_vertex
        self.graph.is_adding_edge = False
        self.update()

    def toggleAddEdge(self):
        self.graph.is_adding_edge = not self.graph.is_adding_edge
        self.graph.is_adding_vertex = False
        self.update()

    def toggleShowComplement(self):
        self.graph.show_complement = not self.graph.show_complement
        self.graph.getComplement()
        self.update()
        self.updateWorkspace()

    def clear(self):
        self.graph.clear()
        self.scene.clear()
        self.update()

    def matrix(self):
        self.matrix_textbox.clear()  # Clean the textbox of the matrix
        
        size = len(self.graph.vertices)
        if size == 0:
            return

        self.graph.matrix = [[0 for _ in range(size)] for _ in range(size)]  # Intiallize matrix with zeros
        vertex_id_to_index = {vertex.id: index for index, vertex in enumerate(self.graph.vertices)}

        for vertex in self.graph.vertices:
            for edge in vertex.edges:
                # Find the index of the connected vertices
                indexA = vertex_id_to_index[edge.vertexA.id]
                indexB = vertex_id_to_index[edge.vertexB.id]

                # Set the corresponding entries in the matrix to 1
                self.graph.matrix[indexA][indexB] = 1
                self.graph.matrix[indexB][indexA] = 1 
        
        for row in self.graph.matrix:
            self.matrix_textbox.append(' '.join(map(str, row)))

    def deleteSelected(self):
        # Delete the selected items from the graph
        for vertex in self.graph.vertices.copy():  # Iterate from a copy
            if vertex.isSelected():
                self.graph.vertices.remove(vertex)
                
                for edge1 in vertex.edges:
                    neighbor = edge1.getOpposite(vertex)

                    for edge in neighbor.edges.copy():
                        if edge.getOpposite(neighbor) == vertex:
                            edge in neighbor.edges and neighbor.edges.remove(edge)
                            edge in self.graph.edges and self.graph.edges.remove(edge)
                            del edge
            del vertex

        for edge in self.graph.edges.copy(): # Iterate from a copy
            if edge.isSelected():
                edge in edge.vertexA.edges and edge.vertexA.edges.remove(edge)
                edge in edge.vertexB.edges and edge.vertexB.edges.remove(edge)
                self.graph.edges.remove(edge)
                del edge

        self.update()
        self.updateWorkspace()

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
        active_style = ''' 
        QPushButton {
        background-color: #348133;
        }
        QPushButton:hover {
            background-color: #488e47; 
        }
        '''

        inactive_style = '''
        QPushButton {
        background-color: #3a3a3a;
        }
        QPushButton:hover {
            background-color: #444444; 
        }
        '''
    
        if self.graph.is_adding_vertex:   # Change the add vertex button color
            self.vertex_button.setStyleSheet(active_style)
        else:
            self.vertex_button.setStyleSheet(inactive_style)

        if self.graph.is_adding_edge:   # Change the add edge button color
            self.edge_button.setStyleSheet(active_style)
        else:
            self.edge_button.setStyleSheet(inactive_style)

        if self.graph.show_complement:
            self.complement_button.setStyleSheet(active_style)
        else:
            self.complement_button.setStyleSheet(inactive_style)

        # Disable complement button when adding vertex or edges
        if self.graph.is_adding_vertex or self.graph.is_adding_edge:
            self.complement_button.setDisabled(True)
        else: 
            self.complement_button.setDisabled(False)

    def updateWorkspace(self):
        # Clear the workspace first
        for item in self.scene.items():
            self.scene.removeItem(item)

        # Add vertices to the scene
        for vertex in self.graph.vertices:
            vertex.addLabel()
            self.scene.addItem(vertex)

        # Add edges to the scene
        for edge in self.graph.edges:
            self.scene.addItem(edge)