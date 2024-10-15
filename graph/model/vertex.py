from typing import List, Optional
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QPen, QColor, QBrush

class Vertex(QGraphicsEllipseItem):
    def __init__(self, vertex_id: int, x: float, y: float, width: float, height: float):
        from .edge import Edge  # Local import to avoid circular imports

        self.edges: List[Edge] = []  # Stores the edges of this vertex
        self.is_moving = False  # Flag to track dragging state
        self.id = vertex_id  # Vertex ID for the label
        self.is_highlighted = False  # Highlight state
        self.highlight_color: Optional[QColor] = None  # Color used when highlighted

        # Initialize QGraphicsEllipseItem for the vertex
        super().__init__(x, y, width, height)

        self.setFlags()  # Set item flags
        self.setToolTip(f"Degree: {len(self.edges)}")  # Tooltip showing the degree
        self.add_label()  # Create a text label inside the vertex

    def setFlags(self) -> None:
        """Set the flags for the vertex item."""
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges, True)
        self.setCursor(Qt.PointingHandCursor)

    def add_label(self) -> None:
        """Create and center the label inside the vertex."""
        self.label = QGraphicsTextItem(str(self.id), self)
        font = QFont("Inter", 11, QFont.Bold)  # Font and size
        self.label.setFont(font)

        # Center the text within the ellipse
        rect = self.rect()
        text_rect = self.label.boundingRect()
        x = (rect.width() - text_rect.width()) / 2
        y = (rect.height() - text_rect.height()) / 2
        self.label.setPos(x, y)

    def get_position(self) -> QPointF:
        """Get the position of the vertex in the scene."""
        return self.mapToScene(self.boundingRect().center())

    def add_edge(self, edge) -> None:
        """Add a new edge to the vertex."""
        self.edges.append(edge)
        self.update_tooltip()  # Update the tooltip to show the current degree

    def remove_edge(self, edge) -> None:
        """Remove a edge to the vertex."""
        self.edges.remove(edge)
        self.update_tooltip()  # Update the tooltip to show the current degree

    def set_highlight(self, flag: bool, color_index: Optional[int] = None) -> None:
        """Set highlight state and color."""
        colors = [QColor("#42ffd9"), QColor("#FF6E64")]
        self.is_highlighted = flag
        if flag and color_index is not None:
            self.highlight_color = colors[color_index]

    def update_tooltip(self) -> None:
        """Update the tooltip to reflect the current degree."""
        self.setToolTip(f"Degree: {len(self.edges)}")
        self.add_label()  # Update the label position

    def paint(self, painter, option, widget=None) -> None:
        """Override paint to customize vertex appearance based on selection and highlight state."""
        pen = QPen(Qt.black, 2)
        brush = self.get_brush_color()

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(self.rect())

    def get_brush_color(self) -> QBrush:
        """Get the appropriate brush color based on selection and highlight state."""
        if self.isSelected():
            return QBrush(QColor("#86f986"))  # Light green fill when selected
        elif self.is_highlighted:
            return QBrush(self.highlight_color)
        else:
            return QBrush(QColor("#3db93a"))  # Default color

    def mousePressEvent(self, event) -> None:
        """Handle mouse press events to start dragging the vertex."""
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)  # Change cursor to closed hand while dragging
            self.is_moving = True
            self.mouse_press_pos = event.scenePos()  # Store initial mouse position
            self.item_press_pos = self.pos()  # Store initial vertex position
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move events to drag the vertex."""
        if self.is_moving:
            new_position = self.item_press_pos + (event.scenePos() - self.mouse_press_pos)
            self.setPos(new_position)  # Update vertex position
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Handle mouse release events to stop dragging the vertex."""
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.PointingHandCursor)  # Change cursor back to open hand
            self.is_moving = False
        super().mouseReleaseEvent(event)

    def update(self):
        self.add_label()
        self.update_tooltip()
        super().update()