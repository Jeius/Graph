import math
from PyQt5 import QtCore, QtGui, QtWidgets

class Edge(QtWidgets.QGraphicsPathItem):
    from .vertex import Vertex

    def __init__(self, start: Vertex, end: Vertex):
        super().__init__()
        self.start_vertex = start
        self.end_vertex = end
        self.weight = math.inf
        self.is_highlighted = False
        self.is_curve = False

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2))  # Default edge color and thickness
        self._update_path()
        self._add_label()
        self._add_arrow_head()

    def __eq__(self, other):
        return isinstance(other, Edge) and \
               (self.start_vertex == other.start_vertex and self.end_vertex == other.end_vertex)

    def get_opposite(self, vertex: Vertex):
        return self.end_vertex if vertex == self.start_vertex else self.start_vertex

    def get_control_point(self, offset=60):
        p1 = self.start_vertex.get_position()
        p2 = self.end_vertex.get_position()
        direction = QtCore.QPointF(p1.x() - p2.x(), p1.y() - p2.y())
        length = (direction.x() ** 2 + direction.y() ** 2) ** 0.5
        if length == 0:
            return QtCore.QPointF(p1.x(), p1.y())  # Avoid returning a null point

        direction /= length  # Normalize the direction

        return QtCore.QPointF(
            (p1.x() + p2.x()) / 2 - offset * direction.y(),
            (p1.y() + p2.y()) / 2 + offset * direction.x()
        )

    def show_context_menu(self, pos):
        menu = QtWidgets.QMenu()
        edit_action = menu.addAction("Edit Weight")
        edit_action.triggered.connect(self.edit_weight)
        global_pos = self.mapToScene(pos).toPoint()
        menu.exec_(self.scene().views()[0].mapToGlobal(global_pos))

    def edit_weight(self):
        input_dialog = QtWidgets.QInputDialog()
        input_dialog.setWindowTitle("Edge")
        input_dialog.setLabelText("Enter the new weight:")
        input_dialog.setWindowFlags(input_dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        if input_dialog.exec_() == QtWidgets.QDialog.Accepted:
            weight = input_dialog.textValue()
            self.weight = int(weight) if weight.isdigit() and int(weight) >= 0 else math.inf
            self._add_label()

    def paint(self, painter, option, widget=None):
        self._update_path()
        self._update_label(self.weight_label)
        self._update_arrow_head()

        pen_color = QtCore.Qt.black  # Default pen color
        if self.isSelected():
            pen_color = QtCore.Qt.white  # White if selected
        elif self.is_highlighted:
            pen_color = QtGui.QColor("#42ffd9")  # Custom color when highlighted

        painter.setPen(QtGui.QPen(pen_color, 2))
        painter.drawPath(self.path())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.show_context_menu(event.pos())
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        self.is_highlighted = True
        self.update()  # Trigger a repaint to apply the highlight effect
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.is_highlighted = False
        self.update()  # Trigger a repaint to reset the highlight effect
        super().hoverLeaveEvent(event)

    def _add_label(self):
        self.weight_label = QtWidgets.QGraphicsTextItem(self)
        self.weight_label.setFont(QtGui.QFont("Inter", 11, QtGui.QFont.Bold))
        self.weight_label.setVisible(self.weight != math.inf)

        if self.weight != math.inf:
            self.weight_label.setPlainText(str(self.weight))
            self._update_label(self.weight_label)

    def _add_arrow_head(self, arrow_size=7):
        self.arrow_head = QtWidgets.QGraphicsPolygonItem(self)
        self.arrow_head.setFlag(QtWidgets.QGraphicsPolygonItem.ItemSendsGeometryChanges, True)
        self._update_arrow_head(arrow_size)

    def _update_arrow_head(self, arrow_size=7):
        pen_color = QtCore.Qt.black
        if self.isSelected():
            pen_color = QtCore.Qt.white
        elif self.is_highlighted:
            pen_color = QtGui.QColor("#42ffd9")

        brush = QtGui.QBrush(pen_color)
        self.arrow_head.setBrush(brush)
        self.arrow_head.setPen(QtGui.QPen(pen_color))

        p1 = self.path().elementAt(self.path().elementCount() - 1)
        p1 = QtCore.QPointF(p1.x, p1.y)

        # Calculate the direction vector for arrowhead
        if self.path().elementCount() > 1:
            p0 = self.path().elementAt(self.path().elementCount() - 2)
            p0 = QtCore.QPointF(p0.x, p0.y)
        else:
            p0 = p1  # Degenerate case

        direction = p1 - p0
        length = (direction.x() ** 2 + direction.y() ** 2) ** 0.5
        if length == 0:
            return  # Avoid division by zero

        direction /= length  # Normalize the direction

        p2 = QtCore.QPointF(
            p1.x() + arrow_size * (-direction.x() - direction.y()),
            p1.y() + arrow_size * (-direction.y() + direction.x())
        )
        p3 = QtCore.QPointF(
            p1.x() + arrow_size * (-direction.x() + direction.y()),
            p1.y() + arrow_size * (-direction.y() - direction.x())
        )

        self.arrow_head.setPolygon(QtGui.QPolygonF([p1, p2, p3]))

    def _update_path(self):
        start = self.start_vertex.get_position()
        end = self.end_vertex.get_position()
        control_point = self.get_control_point()

        path = QtGui.QPainterPath()
        path.moveTo(start)
        path.lineTo(end) if not self.is_curve else path.quadTo(control_point, end)
        self.setPath(path)

        # Adjust path for intersections with vertex ellipses
        self._shorten_path(start, end, control_point)

    def _shorten_path(self, start, end, control_point, offset=10):
        def find_intersection(path_item, vertex_item):
            path_shape = path_item.shape()
            scene_shape = QtGui.QPainterPath()

            for i in range(path_shape.elementCount()):
                element = path_shape.elementAt(i)
                scene_point = vertex_item.mapToScene(QtCore.QPointF(element.x, element.y))
                if i == 0:
                    scene_shape.moveTo(scene_point)
                else:
                    scene_shape.lineTo(scene_point)

            return scene_shape.boundingRect().center() if not scene_shape.isEmpty() else None


        start_intersection = find_intersection(self, self.start_vertex)
        end_intersection = find_intersection(self, self.end_vertex)
        path = QtGui.QPainterPath()

        if self.is_curve:
            start = self._adjust_curve_point(control_point, start_intersection, offset)
            end = self._adjust_curve_point(control_point, end_intersection, offset)
            path.moveTo(start)
            path.quadTo(control_point, end)
        else:
            line = QtCore.QLineF(start, end)
            start = line.pointAt(offset / line.length())
            end = line.pointAt(1 - offset / line.length())
            path.moveTo(start)
            path.lineTo(end)

        self.setPath(path)

    def _adjust_curve_point(self, control_point, intersection_point, offset):
        line_to_intersection = QtCore.QLineF(control_point, intersection_point)
        return line_to_intersection.pointAt(1 - offset / line_to_intersection.length())

    def _update_label(self, label: QtWidgets.QGraphicsTextItem):
        label_position = self.get_control_point(15) if not self.is_curve else self.get_control_point()
        center = QtCore.QPointF(label_position - label.boundingRect().center())
        label.setPos(center)

    def update(self):
        self._add_label()
        self._add_arrow_head()
        self._update_path()
        self._update_label()
        self._update_arrow_head()