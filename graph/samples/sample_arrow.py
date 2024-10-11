from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygonF
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsView, QGraphicsScene, QApplication


class ArrowLineItem(QGraphicsLineItem):
    def __init__(self, line, parent=None):
        super().__init__(line, parent)
        self.setPen(QPen(Qt.black, 2))  # Customize the line color and thickness as needed

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)

        # Draw the line
        line = self.line()
        painter.setPen(self.pen())

        # Calculate the arrowhead points
        arrow_size = 10
        angle = line.angle()  # Get the angle of the line in degrees

        # Calculate the arrowhead points
        p1 = line.p2()  # End point of the line
        p2 = QPointF(
            p1.x() + arrow_size * -1 * (line.dx() / line.length()) - arrow_size * (line.dy() / line.length()),
            p1.y() + arrow_size * -1 * (line.dy() / line.length()) + arrow_size * (line.dx() / line.length())
        )
        p3 = QPointF(
            p1.x() + arrow_size * -1 * (line.dx() / line.length()) + arrow_size * (line.dy() / line.length()),
            p1.y() + arrow_size * -1 * (line.dy() / line.length()) - arrow_size * (line.dx() / line.length())
        )

        # Create a polygon to represent the arrowhead
        arrow_head = QPolygonF([p1, p2, p3])

        # Draw the arrowhead
        painter.setBrush(QBrush(Qt.black))  # Customize the arrowhead color as needed
        painter.drawPolygon(arrow_head)


# PyQt setup
app = QApplication([])

# Create a scene and a view
scene = QGraphicsScene()
view = QGraphicsView(scene)

# Create a line and add the custom ArrowLineItem
line_item = ArrowLineItem(QLineF(QPointF(50, 50), QPointF(200, 200)))  # Define the line's start and end points
scene.addItem(line_item)

# Set up and show the view
view.setRenderHint(QPainter.Antialiasing)  # Optional: enable anti-aliasing for smoother lines
view.show()
app.exec()
