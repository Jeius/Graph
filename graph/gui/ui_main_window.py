
from PyQt5 import QtCore, QtGui, QtWidgets
from ..model.graph import Graph
from ..gui.view import View
from ..gui.top_panel import TopPanel

class UI_MainWindow(object):
    def __init__(self, MainWindow: QtWidgets.QMainWindow) -> None:
        self.mainWindow = MainWindow
        self.mainWindow.setObjectName("mainWindow")

        self.graph = Graph()
        self.view = View(self.graph)
        self.topPanel = TopPanel(self.graph)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.topPanel)
        self.mainLayout.addWidget(self.view, stretch=1)

        self.setUpMenuBar()
        self.retranslateUi(self.mainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)
        self.centralwidget.setLayout(self.mainLayout)

    def clicked(self, text):
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        
        self.menuAdd.setTitle(_translate("MainWindow", "Add"))
        self.menuDelete.setTitle(_translate("MainWindow", "Delete"))
        self.menuShow.setTitle(_translate("MainWindow", "Show"))
        self.subMenuShowPath.setTitle(_translate("MainWindow", "Path"))

        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Delete"))

        self.actionDeleteAll.setText(_translate("MainWindow", "Delete All"))
        self.actionDeleteAll.setShortcut(_translate("MainWindow", "Ctrl+Delete"))

        self.actionAddEdge.setText(_translate("MainWindow", "Add Edge"))
        self.actionAddEdge.setShortcut(_translate("MainWindow", "Alt+V"))

        self.actionAddVertex.setText(_translate("MainWindow", "Add Vertex"))
        self.actionAddVertex.setShortcut(_translate("MainWindow", "Alt+E"))

        self.actionShowComplement.setText(_translate("MainWindow", "Complement"))
        self.actionShowComplement.setShortcut(_translate("MainWindow", "C"))

        self.actionDjisktra.setText(_translate("MainWindow", "Djisktra"))
        self.actionFloyd.setText(_translate("MainWindow", "Floyd"))

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

        self.menuDelete.addAction(self.actionDelete)
        self.menuDelete.addAction(self.actionDeleteAll)

        self.subMenuShowPath.addAction(self.actionDjisktra)
        self.subMenuShowPath.addAction(self.actionFloyd)

        self.menuShow.addMenu(self.subMenuShowPath)
        self.menuShow.addAction(self.actionShowComplement)

        self.menubar.addAction(self.menuAdd.menuAction())
        self.menubar.addAction(self.menuDelete.menuAction())
        self.menubar.addAction(self.menuShow.menuAction())

        # Setting callbacks to actions
        self.actionAddVertex.triggered.connect(lambda: self.clicked("AddVertex was clicked"))
        self.actionAddEdge.triggered.connect(lambda: self.clicked("AddEdge was clicked"))
        self.actionDelete.triggered.connect(lambda: self.clicked("Delete was clicked"))
        self.actionDeleteAll.triggered.connect(lambda: self.clicked("DeleteAll was clicked"))