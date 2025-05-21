from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class AdministrativeModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Personal Administrativo")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()
        
        self.admin_search = QLineEdit()
        self.admin_search.setPlaceholderText("Buscar administrativos...")
        self.admin_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")
        
        self.admin_filter = QComboBox()
        self.admin_filter.addItems(["Todos", "Activos", "Inactivos", "Por puesto"])
        self.admin_filter.setStyleSheet("padding: 8px;")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        search_btn.clicked.connect(self.filter_administrativos)
        
        tool_layout.addWidget(self.admin_search)
        tool_layout.addWidget(self.admin_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.admin_table = QTableWidget(0, 6)
        self.admin_table.setHorizontalHeaderLabels(["ID", "Nombre", "Puesto", "Teléfono", "Email", "Estado"])
        self.admin_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #E74C3C;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.admin_table.horizontalHeader().setStretchLastSection(True)
        self.admin_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.admin_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.admin_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.admin_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Administrativo", self.add_administrativo),
            ("Editar Administrativo", self.edit_administrativo),
            ("Cambiar Estado", self.toggle_administrativo_status),
            ("Exportar a CSV", self.export_administrativos)
        ]
        
        for text, handler in actions:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2C3E50;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 8px;
                    font-weight: bold;
                    margin-right: 10px;
                }
                QPushButton:hover {
                    background-color: #34495E;
                }
            """)
            btn.clicked.connect(handler)
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_sample_data(self):
        sample_data = [
            ["1", "Roberto Sánchez", "Recepcionista", "555-3001", "rsanchez@clinica.com", "Activo"],
            ["2", "Laura Díaz", "Secretaria", "555-3002", "ldiaz@clinica.com", "Activo"],
            ["3", "Pedro Vargas", "Contador", "555-3003", "pvargas@clinica.com", "Inactivo"],
            ["4", "Marta Rojas", "Gerente", "555-3004", "mrojas@clinica.com", "Activo"]
        ]
        
        self.admin_table.setRowCount(0)
        for admin in sample_data:
            row = self.admin_table.rowCount()
            self.admin_table.insertRow(row)
            for col, data in enumerate(admin):
                item = QTableWidgetItem(data)
                if col == 5:  # Columna de estado
                    item.setForeground(QColor(39, 174, 96)) if data == "Activo" else item.setForeground(QColor(192, 57, 43))
                self.admin_table.setItem(row, col, item)

    def filter_administrativos(self):
        search_text = self.admin_search.text().lower()
        filter_type = self.admin_filter.currentText()
        
        for row in range(self.admin_table.rowCount()):
            match = True
            name = self.admin_table.item(row, 1).text().lower()
            position = self.admin_table.item(row, 2).text()
            status = self.admin_table.item(row, 5).text()
            
            if search_text and search_text not in name:
                match = False
            if filter_type == "Activos" and status != "Activo":
                match = False
            if filter_type == "Inactivos" and status != "Inactivo":
                match = False
            if filter_type == "Por puesto" and position.lower() != search_text:
                match = False
                
            self.admin_table.setRowHidden(row, not match)

    def add_administrativo(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Administrativo")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit()),
            ("Puesto:", QComboBox()),
            ("Teléfono:", QLineEdit()),
            ("Email:", QLineEdit()),
        ]
        
        fields[1][1].addItems(["Recepcionista", "Secretaria", "Contador", "Gerente", "Administrador"])
        
        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(100)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            datos = [field[1].text() if not isinstance(field[1], QComboBox) else field[1].currentText() 
                    for field in fields]
            
            if all(datos):
                row = self.admin_table.rowCount()
                self.admin_table.insertRow(row)
                self.admin_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                for col, dato in enumerate(datos, start=1):
                    self.admin_table.setItem(row, col, QTableWidgetItem(dato))
                self.admin_table.setItem(row, 5, QTableWidgetItem("Activo"))
                self.admin_table.item(row, 5).setForeground(QColor(39, 174, 96))
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_administrativo(self):
        selected_row = self.admin_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un administrativo para editar.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Administrativo")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit(self.admin_table.item(selected_row, 1).text())),
            ("Puesto:", QComboBox()),
            ("Teléfono:", QLineEdit(self.admin_table.item(selected_row, 3).text())),
            ("Email:", QLineEdit(self.admin_table.item(selected_row, 4).text())),
        ]
        
        fields[1][1].addItems(["Recepcionista", "Secretaria", "Contador", "Gerente", "Administrador"])
        fields[1][1].setCurrentText(self.admin_table.item(selected_row, 2).text())
        
        for label_text, input_field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(100)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            datos = [field[1].text() if not isinstance(field[1], QComboBox) else field[1].currentText() 
                    for field in fields]
            
            if all(datos):
                for col, dato in enumerate(datos, start=1):
                    self.admin_table.setItem(selected_row, col, QTableWidgetItem(dato))
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def toggle_administrativo_status(self):
        selected_row = self.admin_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un administrativo para cambiar su estado.")
            return

        current_status = self.admin_table.item(selected_row, 5).text()
        new_status = "Inactivo" if current_status == "Activo" else "Activo"
        
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            f"¿Está seguro que desea cambiar el estado del administrativo a {new_status}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.admin_table.setItem(selected_row, 5, QTableWidgetItem(new_status))
            color = QColor(39, 174, 96) if new_status == "Activo" else QColor(192, 57, 43)
            self.admin_table.item(selected_row, 5).setForeground(color)

    def export_administrativos(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Administrativos a CSV", 
            "", 
            "CSV Files (*.csv)", 
            options=options
        )
        
        if not file_name:
            return
            
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                # Escribir encabezados
                headers = []
                for col in range(self.admin_table.columnCount()):
                    headers.append(self.admin_table.horizontalHeaderItem(col).text())
                f.write(",".join(headers) + "\n")
                
                # Escribir datos
                for row in range(self.admin_table.rowCount()):
                    row_data = []
                    for col in range(self.admin_table.columnCount()):
                        item = self.admin_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    f.write(",".join(row_data) + "\n")
                    
            QMessageBox.information(self, "Éxito", "Los datos se exportaron correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{str(e)}")