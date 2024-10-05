import math
from PyQt5 import QtCore, QtGui, QtWidgets

class Edge(QtWidgets.QGraphicsLineItem):
    from .vertex import Vertex

    def __init__(self, ellipseA: Vertex, ellipseB: Vertex):
        super().__init__()

        self.vertexA = ellipseA
        self.vertexB = ellipseB
        self.weight = math.inf
        self.isHighlighted = False

        # Get the position of the two ellipses
        pointA = self.vertexA.getPosition()
        pointB = self.vertexB.getPosition()

        # Create a QGraphicsLineItem from centerA to centerB
        self.setLine(QtCore.QLineF(pointA, pointB))
        
        self.setFlag(QtWidgets.QGraphicsLineItem.ItemIsSelectable, True)  
        self.setCursor(QtCore.Qt.PointingHandCursor)  
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2))   # Set the edge color and thickness
        self._addLabel()

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
        # Create a line
        line = self._createLine(self.vertexA, self.vertexB)
        self.setLine(line)
        self.prepareGeometryChange()
        self._updateLabelPos(self.weightLabel)
        
        # Override the paint method to change the appearance of the edge when selected
        pen = QtGui.QPen(QtCore.Qt.black, 2)  # Default
        brush = QtGui.QBrush(QtCore.Qt.black)

        # Check if the item is selected
        if self.isSelected():
            pen = QtGui.QPen(QtCore.Qt.white, 2)  # Change color if selected
            brush = QtGui.QBrush(QtCore.Qt.white)
        else:
            if self.isHighlighted:
                pen = QtGui.QPen(QtGui.QColor("#42ffd9"), 4)
                brush = QtGui.QBrush(QtGui.QColor("#42ffd9"))

        # Calculate the arrowhead points
        arrow_size = 7
        angle = line.angle()  # Get the angle of the line in degrees
        line_length = line.length()
        p1 = line.p2()  # End point of the line

        if line_length == 0:
            p2 = p3 = p1  
        else:
            # Calculate the arrowhead points
            p2 = QtCore.QPointF(
                p1.x() + arrow_size * -1 * (line.dx() / line.length()) - arrow_size * (line.dy() / line.length()),
                p1.y() + arrow_size * -1 * (line.dy() / line.length()) + arrow_size * (line.dx() / line.length())
            )
            p3 = QtCore.QPointF(
                p1.x() + arrow_size * -1 * (line.dx() / line.length()) + arrow_size * (line.dy() / line.length()),
                p1.y() + arrow_size * -1 * (line.dy() / line.length()) - arrow_size * (line.dx() / line.length())
            )

        # Create a polygon to represent the arrowhead
        arrow_head = QtGui.QPolygonF([p1, p2, p3])

        # Apply the pen and brush
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPolygon(arrow_head)
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
            self._addLabel()

    def _addLabel(self):
        self.weightLabel = QtWidgets.QGraphicsTextItem(self)
        self.weightLabel.setFont(QtGui.QFont("Inter", 11, QtGui.QFont.Bold))
        self.weightLabel.adjustSize()  # Adjust size to fit the text
       
        if self.weight != math.inf:
            self.weightLabel.setPlainText(str(self.weight))
            self._updateLabelPos(self.weightLabel)
            self.weightLabel.setVisible(True)
        else:
            self.weightLabel.setVisible(False)

    def _createLine(self, vertexA:Vertex, vertexB:Vertex):
        def shape_in_scene_coordinates(item):
            local_shape = item.shape()  
            scene_shape = QtGui.QPainterPath()
            
            # Map each point in the local shape to scene coordinates
            for i in range(local_shape.elementCount()):
                element = local_shape.elementAt(i)
                scene_point = item.mapToScene(QtCore.QPointF(element.x, element.y))
                if i == 0:
                    scene_shape.moveTo(scene_point)
                else:
                    scene_shape.lineTo(scene_point)
            return scene_shape

        def find_intersection(line_item, ellipse_item):
            line_shape_scene = shape_in_scene_coordinates(line_item)
            ellipse_shape_scene = shape_in_scene_coordinates(ellipse_item)
            
            # Find intersection between the two shapes in scene coordinates
            intersection_path = ellipse_shape_scene.intersected(line_shape_scene)
            
            if not intersection_path.isEmpty():
                return intersection_path.boundingRect().center()
            else:
                return None 

        line = QtCore.QLineF(vertexA.getPosition(), vertexB.getPosition())
        self.setLine(line)
        
        # Calculate intersection points with the ellipse boundaries
        intersectionA = find_intersection(self, vertexA)
        intersectionB = find_intersection(self, vertexB)

        final_line = QtCore.QLineF(intersectionA, intersectionB)
        return final_line

    def _updateLabelPos(self, label: QtWidgets.QGraphicsTextItem):
         # Get the line's endpoints
        line = self.line()
        p1 = line.p1()
        p2 = line.p2()

        # Calculate the direction of the line
        direction = QtCore.QPointF(p1.x() - p2.x(), p1.y() - p2.y())

        # Normalize the direction
        length = (direction.x() ** 2 + direction.y() ** 2) ** 0.5
        if length == 0:
            return  # Avoid division by zero if the points are the same
        direction /= length

        # Calculate the point 10 pixels of the way from p2 to p1
        t = 25  # 25px
        point_on_line = p2 + direction * t

        # Get the perpendicular direction (90 degrees)
        perpendicular = QtCore.QPointF(-direction.y(), direction.x())

        # Calculate the position for the label (10 pixels away)
        label_position = point_on_line + perpendicular * 15
        center_label_pos = QtCore.QPointF(label_position - label.boundingRect().center())

        label.setPos(center_label_pos)

    def setHighlight(self, flag):
        self.isHighlighted = flag

    def update(self):
        self._addLabel()
        super().update()


        