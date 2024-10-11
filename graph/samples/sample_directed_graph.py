from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QPen, QBrush, QPolygonF, QPainter, QPainterPath
from PyQt5.QtWidgets import QApplication, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsScene, QGraphicsView

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
        painter.drawLine(line)


def create_ellipse(x, y, width=30, height=30, color=Qt.green):
    """Helper function to create a QGraphicsEllipseItem at the specified position."""
    ellipse = QGraphicsEllipseItem(0, 0, width, height)
    ellipse.setPos(x - width / 2, y - height / 2)  # Center the ellipse at (x, y)
    ellipse.setBrush(QBrush(color))
    return ellipse


def calculate_line_between_ellipses(ellipse1:QGraphicsEllipseItem, ellipse2:QGraphicsEllipseItem):
    """Calculate the line that connects the borders of two ellipses."""
    # Calculate center points of the ellipses
    center1 = QPointF(ellipse1.rect().width() / 2,
                      ellipse1.rect().height() / 2)
    center2 = QPointF(ellipse2.rect().width() / 2,
                      ellipse2.rect().height() / 2)

    # Calculate the direction line from center1 to center2
    path = QPainterPath()
    path.moveTo(ellipse1.mapToScene(center1))
    path.lineTo(ellipse2.mapToScene(center2))

    # Calculate intersection points with the ellipse boundaries
    line_from_ellipse1 = ellipse1.shape().intersected(path).boundingRect().center()
    line_to_ellipse2 = ellipse2.shape().intersected(path).boundingRect().center()

    # Create a line connecting the boundaries of the ellipses
    final_line = QLineF(line_from_ellipse1, line_to_ellipse2)
    return final_line


# PyQt setup
app = QApplication([])

# Create a scene and a view
scene = QGraphicsScene()
view = QGraphicsView(scene)

# Create two ellipses representing vertices
ellipse1 = create_ellipse(100, 100, color=Qt.red)
ellipse2 = create_ellipse(300, 300, color=Qt.blue)

# Add ellipses to the scene
scene.addItem(ellipse1)
scene.addItem(ellipse2)

# Calculate the line between the two ellipses
line_between = calculate_line_between_ellipses(ellipse1, ellipse2)

# Create the custom ArrowLineItem
arrow_line = ArrowLineItem(line_between)
scene.addItem(arrow_line)

# Set up and show the view
view.setRenderHint(QPainter.Antialiasing)  # Optional: enable anti-aliasing for smoother lines
view.show()
app.exec()
