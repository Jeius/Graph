from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QGraphicsScene
from .graph_model import GraphModel

class SidePanel(QVBoxLayout):
    textbox_size = QSize(70, 30)

    def __init__(self, graph_model: GraphModel, scene: QGraphicsScene):
        super().__init__()
        self.graph_model = graph_model  # Graph object
        self.scene = scene  # QGraphicsScene where the vertices and edges are rendered

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
        # Create the buttons for adding and deleting graph objects
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
        # Method callback for the addVertex button
        self.graph_model.is_adding_vertex = not self.graph_model.is_adding_vertex
        self.graph_model.is_adding_edge = False
        self.update()

    def toggleAddEdge(self):
        # Method callback for the addEdge button
        self.graph_model.is_adding_edge = not self.graph_model.is_adding_edge
        self.graph_model.is_adding_vertex = False
        self.update()

    def toggleShowComplement(self):
        # Method callback for showComplement button
        self.graph_model.getComplement()
        self.update()
        self.updateWorkspace()

    def clear(self):
        # Method callback for the clear button
        self.graph_model.clear()
        self.scene.clear()
        self.update()

    def createMatrix(self):
        # Create the adjacency matrix of the graph
        self.matrix_textbox.clear()  # Clean the textbox of the matrix
        
        # Terminate the execution if there are no vertices
        size = len(self.graph_model.vertices)
        if size == 0:
            return

        # Intiallize matrix with zeros
        self.graph_model.adj_matrix = [[0 for _ in range(size)] for _ in range(size)]  

        # Create a dictionary of index values with the vertex ids as keys
        vertex_id_to_index = {vertex.id: index for index, vertex in enumerate(self.graph_model.vertices)}

        for vertex in self.graph_model.vertices:
            for edge in vertex.edges:
                # Find the index of the connected vertices
                indexA = vertex_id_to_index[edge.vertexA.id]
                indexB = vertex_id_to_index[edge.vertexB.id]

                # Set the corresponding entries in the matrix to 1
                self.graph_model.adj_matrix[indexA][indexB] = 1
                self.graph_model.adj_matrix[indexB][indexA] = 1 
        
        # Render the matrix to the matrix_textbox
        for row in self.graph_model.adj_matrix:
            self.matrix_textbox.append(' '.join(map(str, row)))

    def deleteSelected(self):
        # Method callback for the delete button
        # Delete the selected items from the graph

        # Iterate from the vertices if the selected item is a vertex
        for vertex in self.graph_model.vertices.copy():  # Iterate from a copy
            if vertex.isSelected():
                # Remove from the list of vertices
                self.graph_model.vertices.remove(vertex) 
                
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
                            neighbor_edge in self.graph_model.edges and self.graph_model.edges.remove(neighbor_edge)
                            del neighbor_edge   # Deleting the edge to save memory
            del vertex  # Deleting the vertex to save memory

        # Iterate from the edges if the selected item is an edge
        for edge in self.graph_model.edges.copy(): # Iterate from a copy
            if edge.isSelected():
                # Remove the edge in both endpoints
                edge in edge.vertexA.edges and edge.vertexA.edges.remove(edge)
                edge in edge.vertexB.edges and edge.vertexB.edges.remove(edge)
                self.graph_model.edges.remove(edge)
                del edge

        # Update the reflect the changes
        self.update()
        self.updateWorkspace()

    def update(self):
        # Update the textboxes
        self.order_textbox.setText(str(len(self.graph_model.vertices)))
        self.size_textbox.setText(str(len(self.graph_model.edges)))

        # Unselect selected vertices
        self.graph_model.selected_vertices.clear()
        for item in self.scene.selectedItems():
            item.setSelected(False)

        # Update Matrix
        self.createMatrix()

        # Update Degrees
        for vertex in self.graph_model.vertices:
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
    
        if self.graph_model.is_adding_vertex:   # Change the add vertex button color
            self.vertex_button.setStyleSheet(active_style)
        else:
            self.vertex_button.setStyleSheet(inactive_style)

        if self.graph_model.is_adding_edge:   # Change the add edge button color
            self.edge_button.setStyleSheet(active_style)
        else:
            self.edge_button.setStyleSheet(inactive_style)

        # Disable complement button when adding vertex or edges
        if self.graph_model.is_adding_vertex or self.graph_model.is_adding_edge:
            self.complement_button.setDisabled(True)
        else: 
            self.complement_button.setDisabled(False)

    def updateWorkspace(self):
        # Clear the workspace first
        for item in self.scene.items():
            self.scene.removeItem(item)

        # Add vertices to the scene
        for vertex in self.graph_model.vertices:
            vertex.addLabel()
            self.scene.addItem(vertex)

        # Add edges to the scene
        for edge in self.graph_model.edges:
            self.scene.addItem(edge)