
from PyQt5 import QtCore, QtGui, QtWidgets
from ..model.graph import Graph
from ..model.edge import Edge
from ..gui.view import View
from .side_panel import TopPanel

class UI_MainWindow(object):
    def __init__(self, MainWindow: QtWidgets.QMainWindow) -> None:
        self.mainWindow = MainWindow
        self.mainWindow.setObjectName("mainWindow")

        self.mainLayout = QtWidgets.QHBoxLayout()
        viewLayout = QtWidgets.QVBoxLayout()

        self.graph = Graph()
        self.topPanel = TopPanel(self.graph)
        self.view = View(self.graph, viewLayout, self.topPanel.update, self.updateMenuActions)
        
        self.mainLayout.addLayout(self.topPanel)
        self.mainLayout.addLayout(viewLayout, stretch=1)

        self.setUpMenuBar()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)
        self.centralwidget.setLayout(self.mainLayout)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        
        self.menuAdd.setTitle(_translate("MainWindow", "Add"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuDelete.setTitle(_translate("MainWindow", "Delete"))
        self.menuShow.setTitle(_translate("MainWindow", "Show"))
        self.subMenuShowPath.setTitle(_translate("MainWindow", "Path"))

        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Delete"))

        self.actionDeleteAll.setText(_translate("MainWindow", "Delete All"))
        self.actionDeleteAll.setShortcut(_translate("MainWindow", "Ctrl+Delete"))

        self.actionAddEdge.setText(_translate("MainWindow", "Add Edge"))
        self.actionAddEdge.setShortcut(_translate("MainWindow", "Alt+E"))

        self.actionAddVertex.setText(_translate("MainWindow", "Add Vertex"))
        self.actionAddVertex.setShortcut(_translate("MainWindow", "Alt+V"))

        self.actionEditWeight.setText(_translate("MainWindow", "Edit Weight"))
        self.actionEditWeight.setShortcut(_translate("MainWindow", "Alt+W"))

        self.actionShowComplement.setText(_translate("MainWindow", "Complement"))
        self.actionShowComplement.setShortcut(_translate("MainWindow", "C"))

        self.actionDjisktra.setText(_translate("MainWindow", "Djisktra"))
        self.actionDjisktra.setShortcut(_translate("MainWindow", "D"))
        self.actionFloyd.setText(_translate("MainWindow", "Floyd"))
        self.actionFloyd.setShortcut(_translate("MainWindow", "F"))

    def setUpMenuBar(self):
        self.centralwidget = QtWidgets.QWidget(self.mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mainWindow.setCentralWidget(self.centralwidget)

        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(self.mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")

        # Menu items
        self.menuAdd = QtWidgets.QMenu(self.menubar)
        self.menuAdd.setObjectName("menuAdd")

        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        self.menuDelete = QtWidgets.QMenu(self.menubar)
        self.menuDelete.setObjectName("menuDelete")

        self.menuShow = QtWidgets.QMenu(self.menubar)
        self.menuShow.setObjectName("menuShow")

        self.subMenuShowPath = QtWidgets.QMenu(self.menuShow)
        self.subMenuShowPath.setObjectName("subMenuShowPath")

        self.mainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self.mainWindow)
        self.statusbar.setObjectName("statusbar")
        self.mainWindow.setStatusBar(self.statusbar)

        # Menu Actions
        self.actionAddVertex = QtWidgets.QAction(self.mainWindow)
        self.actionAddVertex.setObjectName("actionAddVertex")

        self.actionAddEdge = QtWidgets.QAction(self.mainWindow)
        self.actionAddEdge.setObjectName("actionAddEdge")

        self.actionEditWeight = QtWidgets.QAction(self.mainWindow)
        self.actionEditWeight.setObjectName("actionEditWeight")

        self.actionDelete = QtWidgets.QAction(self.mainWindow)
        self.actionDelete.setObjectName("actionDelete")

        self.actionDeleteAll = QtWidgets.QAction(self.mainWindow)
        self.actionDeleteAll.setObjectName("actionDeleteAll")

        self.actionShowComplement = QtWidgets.QAction(self.mainWindow)
        self.actionShowComplement.setObjectName("actionShowComplement")

        self.actionShowPath = QtWidgets.QAction(self.mainWindow)
        self.actionShowPath.setObjectName("actionShowComplement")

        self.actionDjisktra = QtWidgets.QAction(self.mainWindow)
        self.actionDjisktra.setObjectName("actionShowVertexSet")

        self.actionFloyd = QtWidgets.QAction(self.mainWindow)
        self.actionFloyd.setObjectName("actionShowEdgeSet")

        self.menuAdd.addAction(self.actionAddVertex)
        self.menuAdd.addAction(self.actionAddEdge)

        self.menuEdit.addAction(self.actionEditWeight)

        self.menuDelete.addAction(self.actionDelete)
        self.menuDelete.addAction(self.actionDeleteAll)

        self.subMenuShowPath.addAction(self.actionDjisktra)
        self.subMenuShowPath.addAction(self.actionFloyd)

        self.menuShow.addMenu(self.subMenuShowPath)
        self.menuShow.addAction(self.actionShowComplement)

        self.menubar.addAction(self.menuAdd.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuDelete.menuAction())
        self.menubar.addAction(self.menuShow.menuAction())

        # Setting callbacks to actions
        self.actionAddVertex.triggered.connect(lambda: self.addCallback("vertex"))
        self.actionAddEdge.triggered.connect(lambda: self.addCallback("edge"))
        self.actionEditWeight.triggered.connect(self.editCallback)
        self.actionDelete.triggered.connect(lambda: self.deleteCallback("delete"))
        self.actionDeleteAll.triggered.connect(lambda: self.deleteCallback("clear"))
        self.actionShowComplement.triggered.connect(self.showComplementCallback)
        self.actionDjisktra.triggered.connect(self.djisktraCallback)
        self.actionFloyd.triggered.connect(self.floydCallback)

        self.updateMenuActions()

    def addCallback(self, action):
        if action == "vertex":
            self.graph.isAddingVertex = True
            self.graph.isAddingEdge = False
        elif action == "edge":
            self.graph.isAddingEdge = True
            self.graph.isAddingVertex = False
        else:
            self.graph.isAddingVertex = False
            self.graph.isAddingEdge = False

        self.graph.isUsingDjisktra = False
        self.graph.isUsingFloyd = False
        self.graph.unSelectItems()
        self.view.setAdding(True)
        self.update()

    def deleteCallback(self, action):
        selected_items = self.graph.selectedItems()

        # For delete action
        if action == "delete":
            if not selected_items:  # Check if no items are selected
                # Show alert dialog
                msg_box = QtWidgets.QMessageBox()
                msg_box.setIcon(QtWidgets.QMessageBox.Warning)
                msg_box.setWindowTitle("No Selection")
                msg_box.setText("Select an item to delete first.")
                msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg_box.exec_()
                return
            
            # Show confirmation dialog before deletion
            confirm_box = QtWidgets.QMessageBox()
            confirm_box.setIcon(QtWidgets.QMessageBox.Question)
            confirm_box.setWindowTitle("Confirm Deletion")
            confirm_box.setText("Are you sure you want to delete the selected items?")
            confirm_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            confirm_box.setDefaultButton(QtWidgets.QMessageBox.No)
            
            result = confirm_box.exec_()

            if result == QtWidgets.QMessageBox.Yes:
                self.graph.delete()  # Perform deletion

        # For clear action
        elif action == "clear":
            # Show confirmation dialog before clearing
            confirm_box = QtWidgets.QMessageBox()
            confirm_box.setIcon(QtWidgets.QMessageBox.Question)
            confirm_box.setWindowTitle("Confirm Delete All")
            confirm_box.setText("Are you sure you want to delete all items?")
            confirm_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            confirm_box.setDefaultButton(QtWidgets.QMessageBox.No)

            result = confirm_box.exec_()

            if result == QtWidgets.QMessageBox.Yes:
                self.graph.reset()  # Perform clearing
                self.view.doneButton.setVisible(False)

        self.update()

    def editCallback(self):
        selected_items = self.graph.selectedItems()
        
        if not selected_items:  # Check if no items are selected
            # Show alert dialog
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle("No Edge Selected")
            msg_box.setText("Select an edge first to edit the weight.")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.exec_()
            return

        # Continue with editing if there are selected items
        for item in selected_items:
            if isinstance(item, Edge):
                item.editWeight()
                self.update()

    def showComplementCallback(self):
        self.graph.djisktra.reset()
        self.graph.floyd.reset()
        self.graph.isUsingDjisktra = False
        self.graph.isUsingFloyd = False
        self.view.doneButton.setVisible(False)
        self.graph.setHighlightItems(False)
        self.graph.getComplement()
        self.update()

    def djisktraCallback(self):
        if not self.graph.isAddingEdge and not self.graph.isAddingVertex:
            self.view.findPath("djikstra")

    def floydCallback(self):
        if not self.graph.isAddingEdge and not self.graph.isAddingVertex:
            self.view.findPath("floyd")

    def updateMenuActions(self):
        if not self.graph.vertices:
            self.actionEditWeight.setEnabled(False)
            self.actionDelete.setEnabled(False)
            self.actionDeleteAll.setEnabled(False)
        else:
            self.actionEditWeight.setEnabled(True)
            self.actionDelete.setEnabled(True)
            self.actionDeleteAll.setEnabled(True)

        if not self.graph.edges:
            self.actionShowComplement.setEnabled(False)
            self.actionShowPath.setEnabled(False)
            self.actionEditWeight.setEnabled(False)
            self.actionDjisktra.setEnabled(False)
            self.actionFloyd.setEnabled(False)
        else: 
            self.actionShowComplement.setEnabled(True)
            self.actionShowPath.setEnabled(True)
            self.actionEditWeight.setEnabled(True)
            self.actionDjisktra.setEnabled(True)
            self.actionFloyd.setEnabled(True)

    def update(self):
        self.topPanel.update()
        self.view.update()
        self.graph.update()
        self.updateMenuActions()