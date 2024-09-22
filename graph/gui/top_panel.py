from PyQt5 import QtCore, QtGui, QtWidgets
from ..model.graph import Graph

class TopPanel(QtWidgets.QHBoxLayout):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.addLayout(self.graphInfo())
        self.addWidget(self.separator("vertical"))
        self.addLayout(self.adjMatrix(), stretch=1)
        self.addWidget(self.separator("vertical"))
        self.addLayout(self.pathTable(), stretch=2)

    def graphInfo(self):
        # Displays the graph order and size
        layout = QtWidgets.QGridLayout()
        small = QtCore.QSize(70, 30)
        medium = QtCore.QSize(180, 45)

        sizeLabel = QtWidgets.QLabel("Size")
        self.sizeTextbox = QtWidgets.QTextEdit()
        self.sizeTextbox.setFixedSize(small)
        self.sizeTextbox.setReadOnly(True)

        orderLabel = QtWidgets.QLabel("Order")
        self.orderTextbox = QtWidgets.QTextEdit()
        self.orderTextbox.setFixedSize(small)
        self.orderTextbox.setReadOnly(True)

        vertexSetLabel = QtWidgets.QLabel("Vertex Set")
        self.vertexSetTextbox = QtWidgets.QTextEdit()
        self.vertexSetTextbox.setFixedSize(medium)
        self.vertexSetTextbox.setReadOnly(True)
        self.vertexSetTextbox.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        edgeSetLabel = QtWidgets.QLabel("Edge Set")
        self.edgeSetTextbox = QtWidgets.QTextEdit()
        self.edgeSetTextbox.setFixedSize(medium)
        self.edgeSetTextbox.setReadOnly(True)
        self.edgeSetTextbox.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        layout.addWidget(orderLabel, 0, 0)
        layout.addWidget(self.orderTextbox, 0, 1)
        layout.addWidget(sizeLabel, 1, 0)
        layout.addWidget(self.sizeTextbox, 1, 1)
        layout.addWidget(vertexSetLabel, 2, 0)
        layout.addWidget(self.vertexSetTextbox, 2, 1)
        layout.addWidget(edgeSetLabel, 3, 0)
        layout.addWidget(self.edgeSetTextbox, 3, 1)

        return layout
    
    def adjMatrix(self):
        layout = QtWidgets.QVBoxLayout()

        matrixLabel = QtWidgets.QLabel("Adjacency Matrix")
        self.matrixTextbox = QtWidgets.QTextEdit()
        self.matrixTextbox.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.matrixTextbox.setReadOnly(True)
        self.matrixTextbox.setFixedHeight(160)

        layout.addWidget(matrixLabel, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.matrixTextbox)
        return layout
    
    def pathTable(self):
        layout = QtWidgets.QVBoxLayout()

        pathLabel = QtWidgets.QLabel("Path Table")
        self.pathTextbox = QtWidgets.QTextEdit()
        self.pathTextbox.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.pathTextbox.setReadOnly(True)
        self.pathTextbox.setFixedHeight(160)

        layout.addWidget(pathLabel, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.pathTextbox)

        return layout
    
    def separator(self, orientation):
        separator = QtWidgets.QFrame()
        if orientation == "vertical":
            separator.setFrameShape(QtWidgets.QFrame.VLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)
            # separator.setStyleSheet("border: 1px solid #616161;")
        elif orientation == "horizontal":
            separator.setFrameShape(QtWidgets.QFrame.HLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        return separator
    
    def update(self):
        def updateVertexSet():
            vertices = self.graph.vertices
            vertex_set = []
            for vertex in vertices:
                vertex_set.append(str(vertex.id))
            self.vertexSetTextbox.clear()
            self.vertexSetTextbox.append("V(G) = {" + ', '.join(map(str, vertex_set)) + '}')

        def updateEdgeSet():
            edges = self.graph.edges
            edge_set = []
            for edge in edges:
                vertexA_id = edge.vertexA.id
                vertexB_id = edge.vertexB.id
                edge_set.append(f"({str(vertexA_id)}, {str(vertexB_id)})")
            self.edgeSetTextbox.clear()
            self.edgeSetTextbox.append("E(G) = {" + ', '.join(map(str, edge_set)) + '}')

        # Update Adjacency Matrix
        self.graph.createAdjMatrix()
        self.matrixTextbox.clear()
        for row in self.graph.adj_matrix:
            self.matrixTextbox.append(' '.join(map(str, row)))

        # Update the textboxes
        self.orderTextbox.setText(str(len(self.graph.vertices)))
        self.sizeTextbox.setText(str(len(self.graph.edges)))
        updateVertexSet()
        updateEdgeSet()

        # Update Degrees
        for vertex in self.graph.vertices:
            vertex.update()


