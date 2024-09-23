
from PyQt5 import QtCore, QtGui, QtWidgets
from ..model.graph import Graph
from ..model.edge import Edge
from ..gui.view import View
from ..gui.top_panel import TopPanel

class UI_MainWindow(object):
    def __init__(self, MainWindow: QtWidgets.QMainWindow) -> None:
        self.mainWindow = MainWindow
        self.mainWindow.setObjectName("mainWindow")

        self.mainLayout = QtWidgets.QHBoxLayout()
        viewLayout = QtWidgets.QVBoxLayout()

        self.graph = Graph()
        self.topPanel = TopPanel(self.graph)
        self.view = View(self.graph, viewLayout, self.topPanel.update)
        
        self.mainLayout.addLayout(self.topPanel)
        self.mainLayout.addLayout(viewLayout, stretch=1)

        self.setUpMenuBar()
        self.retranslateUi(self.mainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)
        self.centralwidget.setLayout(self.mainLayout)

    def retranslateUi(self, MainWindow):
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
        self.graph.unSelectItems()
        self.view.setAdding(True)

    def deleteCallback(self, action):
        if action == "delete":
            self.graph.delete()
        elif action == "clear":
            self.graph.clear()
        self.topPanel.update()
        self.view.update()

    def editCallback(self):
        for item in self.graph.selectedItems():
            if isinstance(item, Edge):
                item.editWeight()

    def showComplementCallback(self):
        self.graph.getComplement()
        self.topPanel.update()
        self.view.update()

    def djisktraCallback(self):
        self.view.useDjisktra(True)

    def floydCallback(self):
        pass

