from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class OfficesModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Consultorios")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()
        
        self.office_search = QLineEdit()
        self.office_search.setPlaceholderText("Buscar consultorios...")
        self.office_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")
        
        self.office_filter = QComboBox()
        self.office_filter.addItems(["Todos", "Disponibles", "Ocupados", "Por especialidad", "En mantenimiento"])
        self.office_filter.setStyleSheet("padding: 8px;")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)
        search_btn.clicked.connect(self.filter_consultorios)
        
        tool_layout.addWidget(self.office_search)
        tool_layout.addWidget(self.office_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.office_table = QTableWidget(0, 5)
        self.office_table.setHorizontalHeaderLabels(["ID", "Nombre", "Ubicación", "Especialidad", "Estado"])
        self.office_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #1ABC9C;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.office_table.horizontalHeader().setStretchLastSection(True)
        self.office_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.office_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.office_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.office_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Consultorio", self.add_consultorio),
            ("Editar Consultorio", self.edit_consultorio),
            ("Cambiar Estado", self.toggle_consultorio_status),
            ("Exportar a CSV", self.export_consultorios)
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
            ["1", "Consultorio 101", "1er piso", "Cardiología", "Disponible"],
            ["2", "Consultorio 205", "2do piso", "Pediatría", "Ocupado"],
            ["3", "Consultorio 310", "3er piso", "Neurología", "Disponible"],
            ["4", "Consultorio 412", "4to piso", "Dermatología", "En mantenimiento"]
        ]
        
        self.office_table.setRowCount(0)
        for office in sample_data:
            row = self.office_table.rowCount()
            self.office_table.insertRow(row)
            for col, data in enumerate(office):
                item = QTableWidgetItem(data)
                if col == 4:  # Columna de estado
                    if data == "Disponible":
                        item.setForeground(QColor(39, 174, 96))
                    elif data == "Ocupado":
                        item.setForeground(QColor(192, 57, 43))
                    else:
                        item.setForeground(QColor(243, 156, 18))  # Naranja para mantenimiento
                self.office_table.setItem(row, col, item)

    def filter_consultorios(self):
        search_text = self.office_search.text().lower()
        filter_type = self.office_filter.currentText()
        
        for row in range(self.office_table.rowCount()):
            match = True
            name = self.office_table.item(row, 1).text().lower()
            specialty = self.office_table.item(row, 3).text().lower()
            status = self.office_table.item(row, 4).text()
            
            if search_text and search_text not in name:
                match = False
            if filter_type == "Disponibles" and status != "Disponible":
                match = False
            if filter_type == "Ocupados" and status != "Ocupado":
                match = False
            if filter_type == "En mantenimiento" and status != "En mantenimiento":
                match = False
            if filter_type == "Por especialidad" and search_text not in specialty:
                match = False
                
            self.office_table.setRowHidden(row, not match)

    def add_consultorio(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Consultorio")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit()),
            ("Ubicación:", QLineEdit()),
            ("Especialidad:", QComboBox()),
            ("Estado:", QComboBox()),
        ]
        
        fields[2][1].addItems(["Cardiología", "Pediatría", "Neurología", "Dermatología", "General"])
        fields[3][1].addItems(["Disponible", "Ocupado", "En mantenimiento"])
        
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
                row = self.office_table.rowCount()
                self.office_table.insertRow(row)
                self.office_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                for col, dato in enumerate(datos, start=1):
                    item = QTableWidgetItem(dato)
                    if col == 4:  # Columna de estado
                        if dato == "Disponible":
                            item.setForeground(QColor(39, 174, 96))
                        elif dato == "Ocupado":
                            item.setForeground(QColor(192, 57, 43))
                        else:
                            item.setForeground(QColor(243, 156, 18))
                    self.office_table.setItem(row, col, item)
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_consultorio(self):
        selected_row = self.office_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un consultorio para editar.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Consultorio")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit(self.office_table.item(selected_row, 1).text())),
            ("Ubicación:", QLineEdit(self.office_table.item(selected_row, 2).text())),
            ("Especialidad:", QComboBox()),
            ("Estado:", QComboBox()),
        ]
        
        fields[2][1].addItems(["Cardiología", "Pediatría", "Neurología", "Dermatología", "General"])
        fields[2][1].setCurrentText(self.office_table.item(selected_row, 3).text())
        
        fields[3][1].addItems(["Disponible", "Ocupado", "En mantenimiento"])
        fields[3][1].setCurrentText(self.office_table.item(selected_row, 4).text())
        
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
                    item = QTableWidgetItem(dato)
                    if col == 4:  # Columna de estado
                        if dato == "Disponible":
                            item.setForeground(QColor(39, 174, 96))
                        elif dato == "Ocupado":
                            item.setForeground(QColor(192, 57, 43))
                        else:
                            item.setForeground(QColor(243, 156, 18))
                    self.office_table.setItem(selected_row, col, item)
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def toggle_consultorio_status(self):
        selected_row = self.office_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un consultorio para cambiar su estado.")
            return

        current_status = self.office_table.item(selected_row, 4).text()
        statuses = ["Disponible", "Ocupado", "En mantenimiento"]
        current_index = statuses.index(current_status)
        new_status = statuses[(current_index + 1) % len(statuses)]
        
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            f"¿Cambiar estado del consultorio a '{new_status}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            item = QTableWidgetItem(new_status)
            if new_status == "Disponible":
                item.setForeground(QColor(39, 174, 96))
            elif new_status == "Ocupado":
                item.setForeground(QColor(192, 57, 43))
            else:
                item.setForeground(QColor(243, 156, 18))
            self.office_table.setItem(selected_row, 4, item)

    def export_consultorios(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Consultorios a CSV", 
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
                for col in range(self.office_table.columnCount()):
                    headers.append(self.office_table.horizontalHeaderItem(col).text())
                f.write(",".join(headers) + "\n")
                
                # Escribir datos
                for row in range(self.office_table.rowCount()):
                    row_data = []
                    for col in range(self.office_table.columnCount()):
                        item = self.office_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    f.write(",".join(row_data) + "\n")
                    
            QMessageBox.information(self, "Éxito", "Los datos se exportaron correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{str(e)}")