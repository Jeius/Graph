from PyQt5 import QtCore, QtGui, QtWidgets
from ..model.graph import Graph
from ..model.edge import Edge
from ..gui.view import GraphView
from .side_panel import SidePanel


class UI_MainWindow:
    def __init__(self, main_window: QtWidgets.QMainWindow) -> None:
        self.main_window = main_window
        self.main_window.setObjectName("main_window")

        self.setup_layout()
        self.setup_menu_bar()
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)
        self.central_widget.setLayout(self.main_layout)

    def setup_layout(self):
        """Sets up the main layout of the window."""
        self.main_layout = QtWidgets.QHBoxLayout()
        view_layout = QtWidgets.QVBoxLayout()

        self.graph = Graph()
        self.top_panel = SidePanel(self.graph)
        self.view = GraphView(self.graph, view_layout, self.top_panel.update, self.update_menu_actions)

        self.main_layout.addLayout(self.top_panel)
        self.main_layout.addLayout(view_layout, stretch=1)

    def retranslate_ui(self):
        """Sets the text and shortcuts for UI elements."""
        _translate = QtCore.QCoreApplication.translate
        titles = {
            self.menu_add: "Add",
            self.menu_edit: "Edit",
            self.menu_delete: "Delete",
            self.menu_show: "Show",
            self.submenu_show_path: "Path",
        }
        actions = {
            self.action_delete: ("Delete", "Delete"),
            self.action_delete_all: ("Delete All", "Ctrl+Delete"),
            self.action_add_edge: ("Add Edge", "Alt+E"),
            self.action_add_vertex: ("Add Vertex", "Alt+V"),
            self.action_edit_weight: ("Edit Weight", "Alt+W"),
            self.action_show_complement: ("Complement", "C"),
            self.action_dijkstra: ("Dijkstra", "D"),
            self.action_floyd: ("Floyd", "F"),
        }

        for menu, title in titles.items():
            menu.setTitle(_translate("MainWindow", title))

        for action, (text, shortcut) in actions.items():
            action.setText(_translate("MainWindow", text))
            action.setShortcut(_translate("MainWindow", shortcut))

    def setup_menu_bar(self):
        """Sets up the menu bar and connects menu actions."""
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.central_widget.setObjectName("central_widget")
        self.main_window.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(self.main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menu_bar.setObjectName("menu_bar")
        self.main_window.setMenuBar(self.menu_bar)

        # Menus and actions
        self.setup_menus()
        self.setup_actions()

        self.update_menu_actions()

    def setup_menus(self):
        """Initializes the menus."""
        self.menu_add = QtWidgets.QMenu(self.menu_bar)
        self.menu_edit = QtWidgets.QMenu(self.menu_bar)
        self.menu_delete = QtWidgets.QMenu(self.menu_bar)
        self.menu_show = QtWidgets.QMenu(self.menu_bar)
        self.submenu_show_path = QtWidgets.QMenu(self.menu_show)

        self.menu_bar.addMenu(self.menu_add)
        self.menu_bar.addMenu(self.menu_edit)
        self.menu_bar.addMenu(self.menu_delete)
        self.menu_bar.addMenu(self.menu_show)

    def setup_actions(self):
        """Initializes the actions and connects them to callbacks."""
        self.action_add_vertex = QtWidgets.QAction(self.main_window)
        self.action_add_edge = QtWidgets.QAction(self.main_window)
        self.action_edit_weight = QtWidgets.QAction(self.main_window)
        self.action_delete = QtWidgets.QAction(self.main_window)
        self.action_delete_all = QtWidgets.QAction(self.main_window)
        self.action_show_complement = QtWidgets.QAction(self.main_window)
        self.action_dijkstra = QtWidgets.QAction(self.main_window)
        self.action_floyd = QtWidgets.QAction(self.main_window)

        # Add actions to menus
        self.menu_add.addAction(self.action_add_vertex)
        self.menu_add.addAction(self.action_add_edge)
        self.menu_edit.addAction(self.action_edit_weight)
        self.menu_delete.addAction(self.action_delete)
        self.menu_delete.addAction(self.action_delete_all)
        self.submenu_show_path.addAction(self.action_dijkstra)
        self.submenu_show_path.addAction(self.action_floyd)
        self.menu_show.addMenu(self.submenu_show_path)
        self.menu_show.addAction(self.action_show_complement)

        # Connect actions to methods
        self.action_add_vertex.triggered.connect(lambda: self.add_callback("vertex"))
        self.action_add_edge.triggered.connect(lambda: self.add_callback("edge"))
        self.action_edit_weight.triggered.connect(self.edit_callback)
        self.action_delete.triggered.connect(lambda: self.delete_callback("delete"))
        self.action_delete_all.triggered.connect(lambda: self.delete_callback("clear"))
        self.action_show_complement.triggered.connect(self.show_complement_callback)
        self.action_dijkstra.triggered.connect(self.dijkstra_callback)
        self.action_floyd.triggered.connect(self.floyd_callback)

    def add_callback(self, action):
        """Handles the add actions for vertex and edge."""
        self.graph.is_adding_vertex = action == "vertex"
        self.graph.is_adding_edge = action == "edge"
        self.graph.is_using_dijkstra = self.graph.is_using_floyd = False
        self.graph.unselect_items()
        self.view.set_adding(True)
        self.update()

    def delete_callback(self, action):
        """Handles the delete and clear actions."""
        selected_items = self.graph.selectedItems()

        if action == "delete" and not selected_items:
            self.show_message_box("No Selection", "Select an item to delete first.")
            return

        if action == "delete":
            if self.confirm_action("Confirm Deletion", "Are you sure you want to delete the selected items?"):
                self.graph.delete_selected()
        elif action == "clear":
            if self.confirm_action("Confirm Delete All", "Are you sure you want to delete all items?"):
                self.graph.reset()
                self.view.done_button.setVisible(False)

        self.update()

    def edit_callback(self):
        """Handles the editing of edge weights."""
        selected_items = self.graph.selectedItems()
        if not selected_items:
            self.show_message_box("No Edge Selected", "Select an edge first to edit the weight.")
            return

        for item in selected_items:
            if isinstance(item, Edge):
                item.edit_weight()
                self.update()

    def show_complement_callback(self):
        """Shows the complement of the current graph."""
        self.graph.dijkstra.reset()
        self.graph.floyd_warshall.reset()
        self.graph.is_using_dijsktra = self.graph.is_using_floyd = False
        self.view.done_button.setVisible(False)
        self.graph.set_highlight_items(False)
        self.graph.get_complement()
        self.update()

    def dijkstra_callback(self):
        """Handles the Dijkstra algorithm callback."""
        if not self.graph.is_adding_edge and not self.graph.is_adding_vertex:
            self.view.find_path("dijkstra")

    def floyd_callback(self):
        """Handles the Floyd algorithm callback."""
        if not self.graph.is_adding_edge and not self.graph.is_adding_vertex:
            self.view.find_path("floyd")

    def update_menu_actions(self):
        """Updates the status of menu actions based on the graph state."""
        has_vertices = bool(self.graph.vertices)
        has_edges = bool(self.graph.edges)

        self.action_edit_weight.setEnabled(has_vertices)
        self.action_delete.setEnabled(has_vertices)
        self.action_delete_all.setEnabled(has_vertices)
        self.action_show_complement.setEnabled(has_edges)
        self.action_dijkstra.setEnabled(has_edges)
        self.action_floyd.setEnabled(has_edges)

    def update(self):
        """Updates the UI components."""
        self.top_panel.update()
        self.view.update()
        self.graph.update()
        self.update_menu_actions()

    def show_message_box(self, title, message):
        """Displays a message box."""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()

    def confirm_action(self, title, message):
        """Shows a confirmation dialog."""
        confirm_box = QtWidgets.QMessageBox()
        confirm_box.setIcon(QtWidgets.QMessageBox.Question)
        confirm_box.setWindowTitle(title)
        confirm_box.setText(message)
        confirm_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        confirm_box.setDefaultButton(QtWidgets.QMessageBox.No)
        result = confirm_box.exec_()
        return result == QtWidgets.QMessageBox.Yes
