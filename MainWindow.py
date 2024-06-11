from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QVBoxLayout, QLabel, QWidget
from Productos.Stock import Stock
from Productos.Categorias import Categorias
from Proveedores.Proveedores import Proveedores
from Pedidos.Pedidos import Pedidos
from Entregas.Entregas import Entregas
from Database import Database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle('Menú Principal')
        self.views = {}
        self.createViews()

        # Top menu
        menubar = self.menuBar()

        # MENU PRODUCTOS: CATEGORIAS Y STOCK
        verCategoriasAction = QAction('Ver Categorías', self)
        verCategoriasAction.triggered.connect(self.showView('Categorias'))

        verStockAction = QAction('Ver Stock', self)
        verStockAction.triggered.connect(self.showView('Stock'))

        productosMenu = menubar.addMenu('Productos')
        productosSubMenu = QMenu('Productos', self)
        productosSubMenu.addAction(verCategoriasAction)
        productosSubMenu.addAction(verStockAction)
        productosMenu.addMenu(productosSubMenu)


        # MENU PROVEEDORES: PROVEEDORES
        verProveedoresAction = QAction('Ver Proveedores', self)
        verProveedoresAction.triggered.connect(self.showView('Proveedores'))

        proveedoresMenu = menubar.addMenu('Proveedores')
        proveedoresMenu.addAction(verProveedoresAction)


        # MENU PEDIDOS: PEDIDOS
        verPedidosAction = QAction('Ver Pedidos', self)
        verPedidosAction.triggered.connect(self.showView('Pedidos'))

        pedidosMenu = menubar.addMenu('Pedidos')
        pedidosMenu.addAction(verPedidosAction)


        # MENU ENTREGAS: ENTREGAS
        verEntregasAction = QAction('Ver Entregas', self)
        verEntregasAction.triggered.connect(self.showView('Entregas'))
        entregasMenu = menubar.addMenu('Entregas')
        entregasMenu.addAction(verEntregasAction)


        # MENU EMPLEADOS: EMPLEADOS
        if Database().activeUser == "admin@supermercadosl.com":
            verEmpleadosAction = QAction('Ver Empleados', self)
            verEmpleadosAction.triggered.connect(self.showView('Empleados'))
            empleadosMenu = menubar.addMenu('Empleados')
            empleadosMenu.addAction(verEmpleadosAction)


        self.showMaximized()

    def createViews(self):
        if Database().activeUser == "admin@supermercadosl.com":
            self.views['Empleados'] = QLabel('Vista de Empleados')
        self.views['Categorias'] = Categorias()
        self.views['Stock'] = Stock()
        self.views['Proveedores'] = Proveedores()
        self.views['Pedidos'] = Pedidos()
        self.views['Entregas'] = Entregas()

        layout = QVBoxLayout()
        for view in self.views.values():
            layout.addWidget(view)
            view.hide()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def showView(self, view_name):
        def show():
            for name, view in self.views.items():
                if name == view_name:
                    view.show()
                else:
                    view.hide()
        return show