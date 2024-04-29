from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from Database import Database

class Categorias(QWidget):
    def __init__(self):
        super().__init__()
        self.currentPage = 0
        self.pageSize = 20
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Top
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)

        anadir_categoria_button = QPushButton("Añadir Categoría")
        anadir_categoria_button.clicked.connect(self.anadirCategoria)
        top_layout.addWidget(anadir_categoria_button)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar")
        self.search_field.setMinimumWidth(200)
        self.search_field.returnPressed.connect(self.buscarCategoria)
        top_layout.addWidget(self.search_field)

        buscar_button = QPushButton("Buscar")
        buscar_button.clicked.connect(self.buscarCategoria)
        top_layout.addWidget(buscar_button)
        layout.addLayout(top_layout)

        # Center
        self.table_categorias = QTableWidget()
        self.table_categorias.setColumnCount(2)
        self.table_categorias.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.table_categorias.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_categorias.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table_categorias)

        # Pagination
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Anterior")
        self.prev_button.clicked.connect(self.showPrevPage)
        self.next_button = QPushButton("Siguiente")
        self.next_button.clicked.connect(self.showNextPage)
        self.page_label = QLabel()
        pagination_layout.addStretch(1)
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addStretch(1)
        layout.addLayout(pagination_layout)

        self.actualizarCategorias()

    def actualizarCategorias(self):
        totalItems = Database().getCategoriasCount()
        self.totalPages = (totalItems // self.pageSize) + 1
        self.showPage()

    def showPage(self):
        startIndex = self.currentPage * self.pageSize
        categorias = Database().getCategorias(startIndex, self.pageSize)
        
        self.table_categorias.setRowCount(0)
        for row, categoria in enumerate(categorias):
            self.table_categorias.insertRow(row)
            self.table_categorias.setItem(row, 0, QTableWidgetItem(str(categoria.get("_id"))))
            self.table_categorias.setItem(row, 1, QTableWidgetItem(categoria.get("nombre")))
        self.page_label.setText(f"Página {self.currentPage + 1} de {self.totalPages}")

    def showPrevPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.showPage()

    def showNextPage(self):
        if self.currentPage < self.totalPages - 1:
            self.currentPage += 1
            self.showPage()

    def buscarCategoria(self):
        termino = self.search_field.text().strip().lower()
        categorias = Database().buscarCategoria(termino)
        self.table_categorias.setRowCount(0)
        for row, categoria in enumerate(categorias):
            self.table_categorias.insertRow(row)
            self.table_categorias.setItem(row, 0, QTableWidgetItem(str(categoria.get("_id"))))
            self.table_categorias.setItem(row, 1, QTableWidgetItem(categoria.get("nombre")))
        self.page_label.setText(f"Resultados de la búsqueda")

    def anadirCategoria(self):
        pass