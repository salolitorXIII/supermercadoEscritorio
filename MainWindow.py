import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QVBoxLayout, QLabel, QWidget
from Productos.Stock import Stock
from Productos.Categorias import Categorias

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Menú Principal')
        self.views = {}
        self.createViews()

        verClientesAction = QAction('Ver Clientes', self)
        verClientesAction.triggered.connect(self.showView('Clientes'))
    
        verEmpleadosAction = QAction('Ver Empleados', self)
        verEmpleadosAction.triggered.connect(self.showView('Empleados'))

        verCategoriasAction = QAction('Ver Categorías', self)
        verCategoriasAction.triggered.connect(self.showView('Categorias'))

        verStockAction = QAction('Ver Stock', self)
        verStockAction.triggered.connect(self.showView('Stock'))

        verPedidosAction = QAction('Ver Pedidos', self)
        verPedidosAction.triggered.connect(self.showView('Pedidos'))

        # Top menu
        menubar = self.menuBar()

        clientesMenu = menubar.addMenu('Clientes')
        clientesMenu.addAction(verClientesAction)

        empleadosMenu = menubar.addMenu('Empleados')
        empleadosMenu.addAction(verEmpleadosAction)

        productosMenu = menubar.addMenu('Productos')
        productosSubMenu = QMenu('Productos', self)
        productosSubMenu.addAction(verCategoriasAction)
        productosSubMenu.addAction(verStockAction)
        productosMenu.addMenu(productosSubMenu)

        pedidosMenu = menubar.addMenu('Pedidos')
        pedidosMenu.addAction(verPedidosAction)

        self.showMaximized()

    def createViews(self):
        self.views['Clientes'] = QLabel('Vista de Clientes')
        self.views['Empleados'] = QLabel('Vista de Empleados')
        self.views['Categorias'] = Categorias()
        self.views['Stock'] = Stock()
        self.views['Pedidos'] = QLabel('Vista de Pedidos')

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
