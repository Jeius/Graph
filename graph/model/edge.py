import math
from PyQt5 import QtCore, QtGui, QtWidgets

class Edge(QtWidgets.QGraphicsLineItem):
    from .vertex import Vertex

    def __init__(self, ellipseA: Vertex, ellipseB: Vertex):
        super().__init__()

        self.vertexA = ellipseA
        self.vertexB = ellipseB
        self.weight = math.inf

        # Get the position of the two ellipses
        pointA = self.vertexA.getPosition()
        pointB = self.vertexB.getPosition()

        # Create a QGraphicsLineItem from centerA to centerB
        self.setLine(QtCore.QLineF(pointA, pointB))
        
        self.setFlag(QtWidgets.QGraphicsLineItem.ItemIsSelectable, True)  
        self.setCursor(QtCore.Qt.PointingHandCursor)  
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2))   # Set the edge color and thickness
        self.setZValue(0)  # Render the edge below the vertex

    def __eq__(self, other_edge):
        # Check if two edges are equal regardless of vertex order
        if isinstance(other_edge, Edge):
            return (self.vertexA == other_edge.vertexA and self.vertexB == other_edge.vertexB) or \
                   (self.vertexA == other_edge.vertexB and self.vertexB == other_edge.vertexA)

    def getOpposite(self, vertex):
        # Return the neighbor of the vertex
        if vertex == self.vertexA:
            return self.vertexB
        else:
            return self.vertexA

    def paint(self, painter, option, widget=None):
        # Get the position of the two ellipses
        pointA = self.vertexA.getPosition()
        pointB = self.vertexB.getPosition()

        # Create a line
        new_line = QtCore.QLineF(pointA, pointB)
        self.setLine(new_line)
        self.addLabel()
        
        # Override the paint method to change the appearance of the edge when selected
        pen = QtGui.QPen(QtCore.Qt.black, 2)  # Default

        # Check if the item is selected
        if self.isSelected():
            pen = QtGui.QPen(QtCore.Qt.white, 2)  # Change color if selected

        # Apply the pen and brush
        painter.setPen(pen)
        painter.drawLine(self.line())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.showContextMenu(event.pos())
        super().mousePressEvent(event)

    def showContextMenu(self, pos):
        # Create a context menu
        menu = QtWidgets.QMenu()

        edit_action = menu.addAction("Edit Weight")
        edit_action.triggered.connect(self.editWeight)

        # Show the menu at the mouse position
        global_pos = self.mapToScene(pos).toPoint()
        menu.exec_(self.scene().views()[0].mapToGlobal(global_pos))

    def editWeight(self):
        input_dialog = QtWidgets.QInputDialog()
        input_dialog.setWindowTitle("Edge")
        input_dialog.setLabelText("Enter the new weight:")

        # Remove the question mark by disabling the ContextHelpButtonHint flag
        input_dialog.setWindowFlags(input_dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        if input_dialog.exec_() == QtWidgets.QDialog.Accepted:
            weight = input_dialog.textValue()
            self.weight = int(weight) if weight.isdigit() and int(weight) >= 0 else math.inf
            self.addLabel()

    def addLabel(self):
        self.weightLabel = EdgeLabel(0, 0, 30, 30, self.editWeight, self)
        self.weightLabel.setBrush(QtGui.QBrush(QtGui.QColor("#8f8f8f")))
        self.weightLabel.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        if self.weight != math.inf:
            self.weightLabel.setLabel(self.weight)
            midpoint = self.line().pointAt(0.5)
            # Position the weight label above the midpoint
            self.weightLabel.setPos(midpoint.x() - self.weightLabel.boundingRect().width() / 2, 
                                    midpoint.y() - 15)
            self.weightLabel.setVisible(True)
        else:
            self.weightLabel.setVisible(False)


class EdgeLabel(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x: float, y: float, w: float, h: float, editWeight, 
                 parent: QtWidgets.QGraphicsItem | None = ...):
        super().__init__(x, y, w, h, parent)
        self.editWeight = editWeight
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.showContextMenu(event.pos())
        super().mousePressEvent(event)

    def setLabel(self, label):
        # Create a QGraphicsTextItem for the label
        self.label = QtWidgets.QGraphicsTextItem(str(label), self)
        font = QtGui.QFont("Inter", 10, QtGui.QFont.Bold)  # Set the font and size
        self.label.setFont(font)

        # Center the text within the ellipse
        rect = self.rect()
        text_rect = self.label.boundingRect()
        x = rect.width() / 2 - text_rect.width() / 2
        y = rect.height() / 2 - text_rect.height() / 2
        self.label.setPos(x, y)

    def showContextMenu(self, pos):
        # Create a context menu
        menu = QtWidgets.QMenu()

        edit_action = menu.addAction("Edit Weight")
        edit_action.triggered.connect(self.editWeight)

        # Show the menu at the mouse position
        global_pos = self.mapToScene(pos).toPoint()
        menu.exec_(self.scene().views()[0].mapToGlobal(global_pos))