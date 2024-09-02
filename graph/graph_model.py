from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QFont, QPen, QColor, QBrush

class Vertex(QGraphicsEllipseItem):
    def __init__(self, id, x, y, width, height, graph):
        super().__init__(x, y, width, height)
        self.edges = []

        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)  # Make the item movable
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)  # Allow the item to be selectable
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges, True)  # Notify of position changes
        self.setCursor(Qt.PointingHandCursor)  # Set cursor shape when hovering over the item
        self.setToolTip(f"Degree: {str(len(self.edges))}")
        self.setZValue(10)
        
        self.is_moving = False  # Flag to track dragging state
        self.id = id
        self.graph = graph

        # Create a QGraphicsTextItem for the text
        self.text_item = QGraphicsTextItem(str(id), self)
        font = QFont("Inter", 11, QFont.Bold)  # Set the font and size
        self.text_item.setFont(font)
        
        # Position the text in the center of the ellipse
        self.updateLabelPosition()

    def paint(self, painter, option, widget=None):
        # Default pen and brush
        pen = QPen(Qt.black, 2)
        brush = QBrush(QColor("#3db93a"))

        # Check if the item is selected
        if self.isSelected():
            # Set the pen and brush for the selected state
            pen = QPen(Qt.black, 2)  
            brush = QBrush(QColor("#86f986"))  # Lightgreen fill

        # Apply the pen and brush
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(self.rect())
    

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)  # Change cursor to closed hand when dragging
            self.is_moving = True
            self.mousePressPos = event.scenePos()  # Capture the initial mouse position
            self.itemPressPos = self.pos()  # Capture the initial position of the ellipse
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_moving:
            # Calculate the new position of the ellipse based on mouse movement
            new_position = self.itemPressPos + (event.scenePos() - self.mousePressPos)
            self.setPos(new_position)
            
            for edge in self.edges:
                edge.moveEndpoints()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.PointingHandCursor)  # Change cursor back to open hand after dragging
            self.is_moving = False
        super().mouseReleaseEvent(event)

    def updateLabelPosition(self):
        # Center the text within the ellipse
        rect = self.rect()
        text_rect = self.text_item.boundingRect()
        x = rect.width() / 2 - text_rect.width() / 2
        y = rect.height() / 2 - text_rect.height() / 2
        self.text_item.setPos(x, y)
    
    def getPosition(self):
        # Gets the position of the vertex in the scene
        rect = self.rect()
        center_x = self.scenePos().x() + rect.width() / 2
        center_y = self.scenePos().y() + rect.height() / 2
        return QPointF(center_x, center_y)
    
    def addEdge(self, edge):
        self.edges.append(edge)
        self.update()

    def update(self):
        self.setToolTip(f"Degree: {str(len(self.edges))}")


class Edge(QGraphicsLineItem):
    def __init__(self, ellipseA, ellipseB):
        self.vertexA = ellipseA
        self.vertexB = ellipseB

        # Get the position of the two ellipses
        pointA = self.vertexA.getPosition()
        pointB = self.vertexB.getPosition()

        # Create a QGraphicsLineItem from centerA to centerB
        super().__init__(pointA.x(), pointA.y(), pointB.x(), pointB.y())
        
        self.setFlag(QGraphicsLineItem.ItemIsSelectable, True)  # Allow the item to be selectable
        self.setCursor(Qt.PointingHandCursor)
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(0)
    
    def moveEndpoints(self):
         # Get the position of the two ellipses
        pointA = self.vertexA.getPosition()
        pointB = self.vertexB.getPosition()
        
        new_line = QLineF(pointA, pointB)
        self.setLine(new_line)
    
    def getOpposite(self, vertex):
        if vertex == self.vertexA:
            return self.vertexB
        else:
            return self.vertexA
        
    def paint(self, painter, option, widget=None):
        pen = QPen(Qt.black, 2)

        # Check if the item is selected
        if self.isSelected(): 
            pen = QPen(Qt.white, 2)  # Lightgreen fill

        # Apply the pen and brush
        painter.setPen(pen)
        painter.drawLine(self.line())
        


class GraphModel():
    def __init__(self):
        self.vertices = []
        self.selected_vertices = []
        self.edges = []

        self.is_adding_vertex = False  # Flag to enable adding vertex
        self.is_adding_edge = False    # Flag to enable adding edge

    def addVertex(self, scene_position):
        # Define the diameter of the circle
        diameter = 30
        radius = diameter / 2
        position = QPointF(scene_position.x() - radius, scene_position.y() - radius)
        
        ellipse = Vertex(self.getId(), 0, 0, diameter, diameter, self)
        ellipse.setPos(position)  # Position
        ellipse.setBrush(QColor("#3db93a"))  # Fill color
        ellipse.setPen(QPen(Qt.black, 2))  # Border

        self.vertices.append(ellipse)

        return ellipse
    
    def addEdge(self, vertex):
        if len(self.selected_vertices) == 0:
            self.selected_vertices.append(vertex)
            return None
        else:
            vertexA = self.selected_vertices.pop()
            vertexB = vertex
            edge = Edge(vertexA, vertexB)
            self.edges.append(edge)
            vertexA.addEdge(edge)
            vertexB.addEdge(edge)
            return edge

    def getId(self):
        if len(self.vertices) == 0:
            return 1
        else:
            return self.vertices[-1].id + 1
        
