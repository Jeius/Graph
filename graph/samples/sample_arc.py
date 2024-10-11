from PyQt5 import QtWidgets, QtGui, QtCore

class CurvedLineItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, start_point, control_point, end_point):
        super().__init__()

        # Create a QPainterPath
        path = QtGui.QPainterPath()
        path.moveTo(start_point)
        path.quadTo(control_point, end_point)  # Quadratic Bezier curve

        # Set the path to this item
        self.setPath(path)

        # Optionally, set a pen for drawing the curve
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2))

class CurvedCubicLineItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, start_point, control_point1, control_point2, end_point):
        super().__init__()

        # Create a QPainterPath
        path = QtGui.QPainterPath()
        path.moveTo(start_point)
        path.cubicTo(control_point1, control_point2, end_point)  # Cubic Bezier curve

        # Set the path to this item
        self.setPath(path)

        # Optionally, set a pen for drawing the curve
        self.setPen(QtGui.QPen(QtCore.Qt.blue, 2))

# PyQt window setup
class CurvedLineExample(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()
        
        scene = QtWidgets.QGraphicsScene(self)
        self.setScene(scene)

        # Define points for the quadratic bezier curve
        start_point = QtCore.QPointF(50, 150)
        control_point = QtCore.QPointF(150, 50)
        end_point = QtCore.QPointF(250, 150)

        # Add a quadratic bezier curve item to the scene
        curve = CurvedLineItem(start_point, control_point, end_point)
        scene.addItem(curve)

        # Define points for the cubic bezier curve
        control_point1 = QtCore.QPointF(100, 50)
        control_point2 = QtCore.QPointF(200, 250)
        
        # Add a cubic bezier curve item to the scene
        cubic_curve = CurvedCubicLineItem(start_point, control_point1, control_point2, end_point)
        scene.addItem(cubic_curve)

        # Set up the view
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setSceneRect(0, 0, 300, 300)

# Main application
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = CurvedLineExample()
    window.show()
    app.exec_()
