from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QPen, QBrush, QPainter
from PyQt5.QtWidgets import QApplication, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsScene, QGraphicsView, QLabel


def add_label_to_line(scene, line, text):
    """Adds a label 5 pixels away from the line at a 90-degree angle."""
    # Get the line's endpoints
    p1 = line.p1()
    p2 = line.p2()

    # Calculate the point 10% of the way from p1 to p2
    t = 0.15  # 10%
    point_on_line = QPointF(p1.x() + t * (p2.x() - p1.x()), 
                            p1.y() + t * (p2.y() - p1.y()))


    # Calculate the direction of the line
    direction = QPointF(p2.x() - p1.x(), p2.y() - p1.y())

    # Normalize the direction
    length = (direction.x() ** 2 + direction.y() ** 2) ** 0.5
    if length == 0:
        return  # Avoid division by zero if the points are the same
    direction /= length

    # Get the perpendicular direction (90 degrees)
    perpendicular = QPointF(-direction.y(), direction.x())

    # Calculate the position for the label (5 pixels away)
    label_position = point_on_line + perpendicular * 10

    # Create a label
    label = QLabel(text)
    label.setAttribute(Qt.WA_TransparentForMouseEvents)  # Make it transparent for mouse events
    label.setStyleSheet("background-color: white; border: none")  # Optional styling
    label.adjustSize()  # Adjust size to fit the text

    # Set the label position
    label.setGeometry(label.x(), label.y(), label.width(), label.height())
    
    # Add the label to the scene
    scene.addWidget(label)
    label.move(int(label_position.x() - label.width() / 2), int(label_position.y() - label.height() / 2))


# Example usage in a PyQt application
app = QApplication([])

# Create a scene and a view
scene = QGraphicsScene()
view = QGraphicsView(scene)

# Create two ellipses representing vertices
ellipse1 = QGraphicsEllipseItem(0, 0, 30, 30)
ellipse1.setPos(300, 100)
ellipse1.setBrush(QBrush(Qt.red))

ellipse2 = QGraphicsEllipseItem(0, 0, 30, 30)
ellipse2.setPos(300, 300)
ellipse2.setBrush(QBrush(Qt.blue))

# Add ellipses to the scene
scene.addItem(ellipse1)
scene.addItem(ellipse2)

# Create a line between the two ellipses
line_between = QLineF(ellipse1.sceneBoundingRect().center(), ellipse2.sceneBoundingRect().center())
line_item = QGraphicsLineItem(line_between)
line_item.setPen(QPen(Qt.black, 2))
scene.addItem(line_item)

# Add a label to the line
add_label_to_line(scene, line_between, "4")

# Set up and show the view
view.setRenderHint(QPainter.Antialiasing)  # Optional: enable anti-aliasing for smoother lines
view.show()
app.exec()
