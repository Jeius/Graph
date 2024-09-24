from PyQt5 import QtCore, QtGui, QtWidgets
from ..model.graph import Graph

class TopPanel(QtWidgets.QVBoxLayout):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.addLayout(self.graphInfo())
        self.addWidget(self.separator("horizontal"))
        self.addLayout(self.adjMatrix(), stretch=1)
        self.addWidget(self.separator("horizontal"))
        self.addLayout(self.pathTable(), stretch=1)

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
        self.matrixTable = QtWidgets.QTableWidget()
        self.matrixTable.horizontalHeader().setVisible(False) 
        self.matrixTable.verticalHeader().setVisible(False)    
        self.matrixTable.setShowGrid(False)

        layout.addWidget(matrixLabel, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.matrixTable, stretch=1)
        return layout
    
    def pathTable(self):
        layout = QtWidgets.QVBoxLayout()
        pathLabel = QtWidgets.QLabel("Path Table")
        horizontalHeaders = ["Start", "Goal", "Distance"]
        columns = len(horizontalHeaders)

        self.pathTableWidget = QtWidgets.QTableWidget()
        self.pathTableWidget.setColumnCount(columns)
        self.pathTableWidget.setHorizontalHeaderLabels(horizontalHeaders)
        self.pathTableWidget.verticalHeader().sectionClicked.connect(self.pathTableCallback)
        self.pathTableWidget.resizeColumnsToContents()

        layout.addWidget(pathLabel, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.pathTableWidget, stretch=1)

        return layout
    
    def pathTableCallback(self, rowIndex):
        # Get the vertex id
        startVertexId = 0
        goalVertexId = 0
        
        startItem = self.pathTableWidget.item(rowIndex, 0)
        goalItem = self.pathTableWidget.item(rowIndex, 1)
        if startItem is not None and goalItem is not None:
            startVertexId = int(startItem.text())
            goalVertexId = int(goalItem.text())

        startVertex = next((v for v in self.graph.vertices if v.id == startVertexId), None)
        goalVertex = next((v for v in self.graph.vertices if v.id == goalVertexId), None)

        if startVertex is not None and goalVertex is not None:
            self.graph.showPath(startVertex, goalVertex)

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
        # Update Adjacency Matrix
        self._updateMatrix()

        # Update Path Table
        try:
            if self.graph.isUsingDjisktra:
                self._updatePathTableDjisktra()
            else:
                self._updatePathTableFloyd()
        except Exception as e:
            print(str(e))

        # Update the textboxes
        self.orderTextbox.setText(str(len(self.graph.vertices)))
        self.sizeTextbox.setText(str(len(self.graph.edges)))
        self._updateVertexSet()
        self._updateEdgeSet()

        # Update Degrees
        for vertex in self.graph.vertices:
            vertex.update()
        super().update()

    def _updateVertexSet(self):
        vertices = self.graph.vertices
        vertex_set = []
        for vertex in vertices:
            vertex_set.append(str(vertex.id))
        self.vertexSetTextbox.clear()
        self.vertexSetTextbox.append("V(G) = {" + ', '.join(map(str, vertex_set)) + '}')

    def _updateEdgeSet(self):
        edges = self.graph.edges
        edge_set = []
        for edge in edges:
            vertexA_id = edge.vertexA.id
            vertexB_id = edge.vertexB.id
            edge_set.append(f"({str(vertexA_id)}, {str(vertexB_id)})")
        self.edgeSetTextbox.clear()
        self.edgeSetTextbox.append("E(G) = {" + ', '.join(map(str, edge_set)) + '}')

    def _updateMatrix(self):
        self.graph.createAdjMatrix()
        self.matrixTable.clear()
        matrix = self.graph.adjacencyMatrix

        self.matrixTable.setRowCount(len(matrix))
        self.matrixTable.setColumnCount(len(matrix[0]) if matrix else 0)

        for rowIndex, row in enumerate(matrix):
            for columnIndex, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))  
                self.matrixTable.setItem(rowIndex, columnIndex, item)
                self.matrixTable.setColumnWidth(columnIndex, 1)
            
    def _updatePathTableDjisktra(self):
        self.pathTableWidget.setRowCount(0)

        paths = self.graph.djisktra.paths
        if not paths:
            return
        
        vertices = self.graph.vertices
        startVertex = self.graph.djisktra.startVertex
        distances = self.graph.djisktra.distances

        rows = len(vertices) - 1 if vertices else 0
        verticalHeaders = ["Show Path"] * rows

        self.pathTableWidget.setRowCount(rows)
        self.pathTableWidget.setVerticalHeaderLabels(verticalHeaders)
        

        rowIndex = 0
        for goalVertex in vertices:
            if startVertex != goalVertex:
                startItem = QtWidgets.QTableWidgetItem(str(startVertex.id)) 
                startItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                goalItem = QtWidgets.QTableWidgetItem(str(goalVertex.id)) 
                goalItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                distanceItem = QtWidgets.QTableWidgetItem(str(distances[vertices.index(goalVertex)])) 
                distanceItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            
                self.pathTableWidget.setItem(rowIndex, 0, startItem)
                self.pathTableWidget.setItem(rowIndex, 1, goalItem)
                self.pathTableWidget.setItem(rowIndex, 2, distanceItem)
                rowIndex += 1

    def _updatePathTableFloyd(self):
        self.pathTableWidget.setRowCount(0)

        paths = self.graph.floyd.paths
        if not paths:
            return

        vertices = self.graph.vertices
        distances = self.graph.floyd.distances

        rows = len(vertices) * (len(vertices) - 1)
        verticalHeaders = ["Show Path"] * rows

        self.pathTableWidget.setRowCount(rows)
        self.pathTableWidget.setVerticalHeaderLabels(verticalHeaders)

        rowIndex = 0
        for startVertex in vertices:
            for goalVertex in vertices:
                if startVertex != goalVertex:
                    startIndex = vertices.index(startVertex)
                    goalIndex = vertices.index(goalVertex)

                    startItem = QtWidgets.QTableWidgetItem(str(startVertex.id)) 
                    startItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    goalItem = QtWidgets.QTableWidgetItem(str(goalVertex.id)) 
                    goalItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    distanceItem = QtWidgets.QTableWidgetItem(str(distances[startIndex][goalIndex])) 
                    distanceItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                
                    self.pathTableWidget.setItem(rowIndex, 0, startItem)
                    self.pathTableWidget.setItem(rowIndex, 1, goalItem)
                    self.pathTableWidget.setItem(rowIndex, 2, distanceItem)
                    rowIndex += 1