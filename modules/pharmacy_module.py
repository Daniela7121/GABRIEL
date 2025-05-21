from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox, QInputDialog
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class PharmacyModule(QWidget):
    def __init__(self, bd_config, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_pharmacy_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Farmacia")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()
        
        self.pharmacy_search = QLineEdit()
        self.pharmacy_search.setPlaceholderText("Buscar medicamentos...")
        self.pharmacy_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")
        
        self.pharmacy_filter = QComboBox()
        self.pharmacy_filter.addItems(["Todos", "Disponibles", "Bajo stock", "Por tipo"])
        self.pharmacy_filter.setStyleSheet("padding: 8px;")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        search_btn.clicked.connect(self.filter_pharmacy)
        
        tool_layout.addWidget(self.pharmacy_search)
        tool_layout.addWidget(self.pharmacy_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.pharmacy_table = QTableWidget(0, 6)
        self.pharmacy_table.setHorizontalHeaderLabels(["ID", "Medicamento", "Tipo", "Cantidad", "Precio", "Estado"])
        self.pharmacy_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #27AE60;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.pharmacy_table.horizontalHeader().setStretchLastSection(True)
        self.pharmacy_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.pharmacy_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.pharmacy_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.pharmacy_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Medicamento", self.add_medicine),
            ("Editar Medicamento", self.edit_medicine),
            ("Actualizar Stock", self.update_stock),
            ("Exportar a CSV", self.export_pharmacy)
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
            ["1", "Paracetamol", "Analgésico", "100", "5.00", "Disponible"],
            ["2", "Amoxicilina", "Antibiótico", "50", "12.50", "Disponible"],
            ["3", "Omeprazol", "Antiácido", "75", "8.75", "Bajo stock"],
            ["4", "Ibuprofeno", "Antiinflamatorio", "25", "6.25", "Disponible"]
        ]
        
        self.pharmacy_table.setRowCount(0)
        for med in sample_data:
            row = self.pharmacy_table.rowCount()
            self.pharmacy_table.insertRow(row)
            for col, data in enumerate(med):
                item = QTableWidgetItem(data)
                if col == 5:  # Columna de estado
                    if data == "Disponible":
                        item.setForeground(QColor(39, 174, 96))
                    else:
                        item.setForeground(QColor(243, 156, 18))
                self.pharmacy_table.setItem(row, col, item)

    def filter_pharmacy(self):
        search_text = self.pharmacy_search.text().lower()
        filter_type = self.pharmacy_filter.currentText()
        
        for row in range(self.pharmacy_table.rowCount()):
            match = True
            medicine = self.pharmacy_table.item(row, 1).text().lower()
            med_type = self.pharmacy_table.item(row, 2).text().lower()
            quantity = int(self.pharmacy_table.item(row, 3).text())
            status = self.pharmacy_table.item(row, 5).text()
            
            if search_text and search_text not in medicine:
                match = False
            if filter_type == "Disponibles" and status != "Disponible":
                match = False
            if filter_type == "Bajo stock" and (quantity >= 50 or status == "Disponible"):
                match = False
            if filter_type == "Por tipo" and search_text not in med_type:
                match = False
                
            self.pharmacy_table.setRowHidden(row, not match)

    def add_medicine(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Medicamento")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Medicamento:", QLineEdit()),
            ("Tipo:", QComboBox()),
            ("Cantidad:", QLineEdit()),
            ("Precio:", QLineEdit()),
        ]
        
        fields[1][1].addItems(["Analgésico", "Antibiótico", "Antiácido", "Antiinflamatorio", "Antihistamínico"])
        
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
                try:
                    quantity = int(datos[2])
                    price = float(datos[3])
                    status = "Bajo stock" if quantity < 50 else "Disponible"
                    
                    row = self.pharmacy_table.rowCount()
                    self.pharmacy_table.insertRow(row)
                    self.pharmacy_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                    for col, dato in enumerate(datos[:2], start=1):
                        self.pharmacy_table.setItem(row, col, QTableWidgetItem(dato))
                    
                    self.pharmacy_table.setItem(row, 3, QTableWidgetItem(str(quantity)))
                    self.pharmacy_table.setItem(row, 4, QTableWidgetItem(f"{price:.2f}"))
                    
                    status_item = QTableWidgetItem(status)
                    status_item.setForeground(QColor(39, 174, 96) if status == "Disponible" else QColor(243, 156, 18))
                    self.pharmacy_table.setItem(row, 5, status_item)
                except ValueError:
                    QMessageBox.warning(self, "Error", "Cantidad y Precio deben ser valores numéricos.")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_medicine(self):
        selected_row = self.pharmacy_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un medicamento para editar.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Medicamento")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Medicamento:", QLineEdit(self.pharmacy_table.item(selected_row, 1).text())),
            ("Tipo:", QComboBox()),
            ("Cantidad:", QLineEdit(self.pharmacy_table.item(selected_row, 3).text())),
            ("Precio:", QLineEdit(self.pharmacy_table.item(selected_row, 4).text())),
        ]
        
        fields[1][1].addItems(["Analgésico", "Antibiótico", "Antiácido", "Antiinflamatorio", "Antihistamínico"])
        fields[1][1].setCurrentText(self.pharmacy_table.item(selected_row, 2).text())
        
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
                try:
                    quantity = int(datos[2])
                    price = float(datos[3])
                    status = "Bajo stock" if quantity < 50 else "Disponible"
                    
                    for col, dato in enumerate(datos[:2], start=1):
                        self.pharmacy_table.setItem(selected_row, col, QTableWidgetItem(dato))
                    
                    self.pharmacy_table.setItem(selected_row, 3, QTableWidgetItem(str(quantity)))
                    self.pharmacy_table.setItem(selected_row, 4, QTableWidgetItem(f"{price:.2f}"))
                    
                    status_item = QTableWidgetItem(status)
                    status_item.setForeground(QColor(39, 174, 96) if status == "Disponible" else QColor(243, 156, 18))
                    self.pharmacy_table.setItem(selected_row, 5, status_item)
                except ValueError:
                    QMessageBox.warning(self, "Error", "Cantidad y Precio deben ser valores numéricos.")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def update_stock(self):
        selected_row = self.pharmacy_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un medicamento para actualizar stock.")
            return

        current_qty = int(self.pharmacy_table.item(selected_row, 3).text())
        new_qty, ok = QInputDialog.getInt(
            self, 
            "Actualizar Stock", 
            "Ingrese la nueva cantidad:", 
            current_qty, 
            0, 
            1000, 
            1
        )
        
        if ok:
            status = "Bajo stock" if new_qty < 50 else "Disponible"
            self.pharmacy_table.setItem(selected_row, 3, QTableWidgetItem(str(new_qty)))
            
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor(39, 174, 96) if status == "Disponible" else QColor(243, 156, 18))
            self.pharmacy_table.setItem(selected_row, 5, status_item)

    def export_pharmacy(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Inventario a CSV", 
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
                for col in range(self.pharmacy_table.columnCount()):
                    headers.append(self.pharmacy_table.horizontalHeaderItem(col).text())
                f.write(",".join(headers) + "\n")
                
                # Escribir datos
                for row in range(self.pharmacy_table.rowCount()):
                    row_data = []
                    for col in range(self.pharmacy_table.columnCount()):
                        item = self.pharmacy_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    f.write(",".join(row_data) + "\n")
                    
            QMessageBox.information(self, "Éxito", "Los datos se exportaron correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{str(e)}")