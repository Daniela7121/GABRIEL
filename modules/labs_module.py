from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class LabsModule(QWidget):
    def __init__(self, bd_config, parent=None):
        super().__init__(parent)
        bd_config = bd_config
        self.init_ui()
        self.load_labs_data()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Laboratorios")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()
        
        self.lab_search = QLineEdit()
        self.lab_search.setPlaceholderText("Buscar laboratorios...")
        self.lab_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")
        
        self.lab_filter = QComboBox()
        self.lab_filter.addItems(["Todos", "Operativos", "En mantenimiento", "Por tipo"])
        self.lab_filter.setStyleSheet("padding: 8px;")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        search_btn.clicked.connect(self.filter_laboratorios)
        
        tool_layout.addWidget(self.lab_search)
        tool_layout.addWidget(self.lab_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.lab_table = QTableWidget(0, 5)
        self.lab_table.setHorizontalHeaderLabels(["ID", "Nombre", "Ubicación", "Tipo", "Estado"])
        self.lab_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.lab_table.horizontalHeader().setStretchLastSection(True)
        self.lab_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.lab_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lab_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.lab_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Laboratorio", self.add_laboratorio),
            ("Editar Laboratorio", self.edit_laboratorio),
            ("Cambiar Estado", self.toggle_laboratorio_status),
            ("Exportar a CSV", self.export_laboratorios)
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
            ["1", "Laboratorio Central", "1er piso", "Análisis Clínicos", "Operativo"],
            ["2", "Laboratorio de Imágenes", "Sótano", "Radiología", "Operativo"],
            ["3", "Laboratorio de Patología", "2do piso", "Biopsias", "En mantenimiento"],
            ["4", "Laboratorio de Microbiología", "3er piso", "Microbiología", "Operativo"]
        ]
        
        self.lab_table.setRowCount(0)
        for lab in sample_data:
            row = self.lab_table.rowCount()
            self.lab_table.insertRow(row)
            for col, data in enumerate(lab):
                item = QTableWidgetItem(data)
                if col == 4:  # Columna de estado
                    if data == "Operativo":
                        item.setForeground(QColor(39, 174, 96))  # Verde
                    else:
                        item.setForeground(QColor(243, 156, 18))  # Naranja
                self.lab_table.setItem(row, col, item)

    def filter_laboratorios(self):
        search_text = self.lab_search.text().lower()
        filter_type = self.lab_filter.currentText()
        
        for row in range(self.lab_table.rowCount()):
            match = True
            name = self.lab_table.item(row, 1).text().lower()
            lab_type = self.lab_table.item(row, 3).text().lower()
            status = self.lab_table.item(row, 4).text()
            
            if search_text and search_text not in name:
                match = False
            if filter_type == "Operativos" and status != "Operativo":
                match = False
            if filter_type == "En mantenimiento" and status != "En mantenimiento":
                match = False
            if filter_type == "Por tipo" and search_text not in lab_type:
                match = False
                
            self.lab_table.setRowHidden(row, not match)

    def add_laboratorio(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Laboratorio")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit()),
            ("Ubicación:", QLineEdit()),
            ("Tipo:", QComboBox()),
            ("Estado:", QComboBox()),
        ]
        
        fields[2][1].addItems(["Análisis Clínicos", "Radiología", "Patología", "Microbiología", "Hematología"])
        fields[3][1].addItems(["Operativo", "En mantenimiento"])
        
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
                row = self.lab_table.rowCount()
                self.lab_table.insertRow(row)
                self.lab_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                for col, dato in enumerate(datos, start=1):
                    item = QTableWidgetItem(dato)
                    if col == 4:  # Columna de estado
                        if dato == "Operativo":
                            item.setForeground(QColor(39, 174, 96))
                        else:
                            item.setForeground(QColor(243, 156, 18))
                    self.lab_table.setItem(row, col, item)
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_laboratorio(self):
        selected_row = self.lab_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un laboratorio para editar.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Laboratorio")
        dialog.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        fields = [
            ("Nombre:", QLineEdit(self.lab_table.item(selected_row, 1).text())),
            ("Ubicación:", QLineEdit(self.lab_table.item(selected_row, 2).text())),
            ("Tipo:", QComboBox()),
            ("Estado:", QComboBox()),
        ]
        
        fields[2][1].addItems(["Análisis Clínicos", "Radiología", "Patología", "Microbiología", "Hematología"])
        fields[2][1].setCurrentText(self.lab_table.item(selected_row, 3).text())
        
        fields[3][1].addItems(["Operativo", "En mantenimiento"])
        fields[3][1].setCurrentText(self.lab_table.item(selected_row, 4).text())
        
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
                        if dato == "Operativo":
                            item.setForeground(QColor(39, 174, 96))
                        else:
                            item.setForeground(QColor(243, 156, 18))
                    self.lab_table.setItem(selected_row, col, item)
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def toggle_laboratorio_status(self):
        selected_row = self.lab_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un laboratorio para cambiar su estado.")
            return

        current_status = self.lab_table.item(selected_row, 4).text()
        new_status = "En mantenimiento" if current_status == "Operativo" else "Operativo"
        
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            f"¿Cambiar estado del laboratorio a '{new_status}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            item = QTableWidgetItem(new_status)
            if new_status == "Operativo":
                item.setForeground(QColor(39, 174, 96))
            else:
                item.setForeground(QColor(243, 156, 18))
            self.lab_table.setItem(selected_row, 4, item)

    def export_laboratorios(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Laboratorios a CSV", 
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
                for col in range(self.lab_table.columnCount()):
                    headers.append(self.lab_table.horizontalHeaderItem(col).text())
                f.write(",".join(headers) + "\n")
                
                # Escribir datos
                for row in range(self.lab_table.rowCount()):
                    row_data = []
                    for col in range(self.lab_table.columnCount()):
                        item = self.lab_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    f.write(",".join(row_data) + "\n")
                    
            QMessageBox.information(self, "Éxito", "Los datos se exportaron correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{str(e)}")