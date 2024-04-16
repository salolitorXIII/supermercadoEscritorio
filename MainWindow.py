import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QVBoxLayout, QLabel, QWidget
from Stock import Stock


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Menú Principal')
        verClientesAction = QAction('Ver Clientes', self)
        verClientesAction.triggered.connect(self.verClientes)
    
        verEmpleadosAction = QAction('Ver Empleados', self)
        verEmpleadosAction.triggered.connect(self.verEmpleados)

        verProductosAction = QAction('Ver Productos', self)
        verProductosAction.triggered.connect(self.verProductos)

        verCategoriasAction = QAction('Ver Categorías', self)
        verCategoriasAction.triggered.connect(self.verCategorias)

        verStockAction = QAction('Ver Stock', self)
        verStockAction.triggered.connect(self.verStock)
        self.stock_view = Stock()

        verPedidosAction = QAction('Ver Pedidos', self)
        verPedidosAction.triggered.connect(self.verPedidos)

        # Top menu
        menubar = self.menuBar()

        clientesMenu = menubar.addMenu('Clientes')
        clientesMenu.addAction(verClientesAction)

        empleadosMenu = menubar.addMenu('Empleados')
        empleadosMenu.addAction(verEmpleadosAction)

        productosMenu = menubar.addMenu('Productos')
        productosSubMenu = QMenu('Productos', self)
        productosSubMenu.addAction(verProductosAction)
        productosSubMenu.addAction(verCategoriasAction)
        productosSubMenu.addAction(verStockAction)
        productosMenu.addMenu(productosSubMenu)

        pedidosMenu = menubar.addMenu('Pedidos')
        pedidosMenu.addAction(verPedidosAction)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.layout.addWidget(QLabel('¡Bienvenido! Seleccione una opción del menú.'))
        self.showMaximized()

    def verClientes(self):
        self.layout.removeWidget(self.central_widget.findChild(QWidget))
        self.layout.addWidget(QLabel('Vista de Clientes'))

    def verEmpleados(self):
        self.layout.removeWidget(self.central_widget.findChild(QWidget))
        self.layout.addWidget(QLabel('Vista de Empleados'))

    def verProductos(self):
        self.layout.removeWidget(self.central_widget.findChild(QWidget))
        self.layout.addWidget(QLabel('Vista de Productos'))

    def verCategorias(self):
        self.layout.removeWidget(self.central_widget.findChild(QWidget))
        self.layout.addWidget(QLabel('Vista de Categorías'))

    def verStock(self):
        self.layout.removeWidget(self.central_widget.findChild(QWidget))
        self.stock_view.actualizarStock()
        self.layout.addWidget(self.stock_view)
        

    def verPedidos(self):
        self.layout.removeWidget(self.central_widget.findChild(QWidget))
        self.layout.addWidget(QLabel('Vista de Pedidos'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
