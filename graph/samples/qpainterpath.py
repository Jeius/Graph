from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QApplication, QWidget

class PathDrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QPainterPath Example")
        self.resize(400, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create a QPainterPath and define the path
        path = QPainterPath()
        path.moveTo(50, 50)  # Move to the initial position
        path.lineTo(150, 50)  # Draw a line to (150, 50)
        path.lineTo(150, 150)  # Draw a line to (150, 150)
        path.lineTo(50, 150)  # Draw a line to (50, 150)
        path.closeSubpath()  # Close the path to form a complete rectangle

        # Draw the path using the painter
        painter.setPen(QPen(Qt.blue, 3))  # Set the pen color and thickness
        painter.drawPath(path)

        # Draw a second path: an ellipse
        ellipse_path = QPainterPath()
        ellipse_path.addEllipse(QPointF(200, 100), 50, 75)  # Center at (200, 100), radiusX=50, radiusY=75
        painter.setPen(QPen(Qt.red, 2))
        painter.drawPath(ellipse_path)

# PyQt application setup
app = QApplication([])
window = PathDrawingWidget()
window.show()
app.exec()
