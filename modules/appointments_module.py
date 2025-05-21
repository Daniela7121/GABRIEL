from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QComboBox, QDateEdit, QTimeEdit
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate, QTime

class AppointmentsModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Citas Médicas")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        tool_layout = QHBoxLayout()
        
        self.appointment_search = QLineEdit()
        self.appointment_search.setPlaceholderText("Buscar citas...")
        self.appointment_search.setStyleSheet("padding: 8px; border: 1px solid #DDE1E7; border-radius: 6px;")
        
        self.appointment_filter = QComboBox()
        self.appointment_filter.addItems(["Todas", "Confirmadas", "Pendientes", "Canceladas", "Por fecha"])
        self.appointment_filter.setStyleSheet("padding: 8px;")
        
        search_btn = QPushButton("Buscar")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #E67E22;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D35400;
            }
        """)
        search_btn.clicked.connect(self.filter_appointments)
        
        tool_layout.addWidget(self.appointment_search)
        tool_layout.addWidget(self.appointment_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.appointment_table = QTableWidget(0, 7)
        self.appointment_table.setHorizontalHeaderLabels(["ID", "Paciente", "Doctor", "Fecha", "Hora", "Motivo", "Estado"])
        self.appointment_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #E67E22;
                color: white;
                font-weight: bold;
                height: 30px;
                padding-left: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.appointment_table.horizontalHeader().setStretchLastSection(True)
        self.appointment_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.appointment_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.appointment_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.appointment_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Cita", self.add_appointment),
            ("Editar Cita", self.edit_appointment),
            ("Cambiar Estado", self.toggle_appointment_status),
            ("Exportar a CSV", self.export_appointments)
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
            ["1", "Juan Pérez", "Dr. Carlos García", "15/05/2023", "10:00", "Consulta rutinaria", "Confirmada"],
            ["2", "María Gómez", "Dra. Ana López", "16/05/2023", "11:30", "Control niño sano", "Confirmada"],
            ["3", "Carlos Ruiz", "Dr. Luis Martínez", "17/05/2023", "09:15", "Dolor de cabeza", "Cancelada"],
            ["4", "Ana Torres", "Dra. Sofía Ramírez", "18/05/2023", "14:00", "Examen de piel", "Pendiente"]
        ]
        
        self.appointment_table.setRowCount(0)
        for appt in sample_data:
            row = self.appointment_table.rowCount()
            self.appointment_table.insertRow(row)
            for col, data in enumerate(appt):
                item = QTableWidgetItem(data)
                if col == 6:  # Columna de estado
                    if data == "Confirmada":
                        item.setForeground(QColor(39, 174, 96))
                    elif data == "Pendiente":
                        item.setForeground(QColor(243, 156, 18))
                    else:
                        item.setForeground(QColor(192, 57, 43))
                self.appointment_table.setItem(row, col, item)

    def filter_appointments(self):
        search_text = self.appointment_search.text().lower()
        filter_type = self.appointment_filter.currentText()
        
        for row in range(self.appointment_table.rowCount()):
            match = True
            patient = self.appointment_table.item(row, 1).text().lower()
            doctor = self.appointment_table.item(row, 2).text().lower()
            date = self.appointment_table.item(row, 3).text()
            status = self.appointment_table.item(row, 6).text()
            
            if search_text and (search_text not in patient and search_text not in doctor):
                match = False
            if filter_type == "Confirmadas" and status != "Confirmada":
                match = False
            if filter_type == "Pendientes" and status != "Pendiente":
                match = False
            if filter_type == "Canceladas" and status != "Cancelada":
                match = False
            if filter_type == "Por fecha" and search_text not in date:
                match = False
                
            self.appointment_table.setRowHidden(row, not match)

    def add_appointment(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Cita")
        dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        fields = [
            ("Paciente:", QLineEdit()),
            ("Doctor:", QComboBox()),
            ("Fecha:", QDateEdit(QDate.currentDate())),
            ("Hora:", QTimeEdit(QTime.currentTime())),
            ("Motivo:", QLineEdit()),
            ("Estado:", QComboBox()),
        ]
        
        # Sample doctors
        fields[1][1].addItems(["Dr. Carlos García", "Dra. Ana López", "Dr. Luis Martínez", "Dra. Sofía Ramírez"])
        fields[5][1].addItems(["Confirmada", "Pendiente", "Cancelada"])
        
        # Configure date and time formats
        fields[2][1].setDisplayFormat("dd/MM/yyyy")
        fields[3][1].setDisplayFormat("HH:mm")
        
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
            datos = [
                fields[0][1].text(),  # Paciente
                fields[1][1].currentText(),  # Doctor
                fields[2][1].date().toString("dd/MM/yyyy"),  # Fecha
                fields[3][1].time().toString("HH:mm"),  # Hora
                fields[4][1].text(),  # Motivo
                fields[5][1].currentText()  # Estado
            ]
            
            if all(datos):
                row = self.appointment_table.rowCount()
                self.appointment_table.insertRow(row)
                self.appointment_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                for col, dato in enumerate(datos, start=1):
                    item = QTableWidgetItem(dato)
                    if col == 6:  # Columna de estado
                        if dato == "Confirmada":
                            item.setForeground(QColor(39, 174, 96))
                        elif dato == "Pendiente":
                            item.setForeground(QColor(243, 156, 18))
                        else:
                            item.setForeground(QColor(192, 57, 43))
                    self.appointment_table.setItem(row, col, item)
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def edit_appointment(self):
        selected_row = self.appointment_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione una cita para editar.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Cita")
        dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        
        # Parse existing date and time
        current_date = QDate.fromString(self.appointment_table.item(selected_row, 3).text(), "dd/MM/yyyy")
        current_time = QTime.fromString(self.appointment_table.item(selected_row, 4).text(), "HH:mm")
        
        fields = [
            ("Paciente:", QLineEdit(self.appointment_table.item(selected_row, 1).text())),
            ("Doctor:", QComboBox()),
            ("Fecha:", QDateEdit(current_date)),
            ("Hora:", QTimeEdit(current_time)),
            ("Motivo:", QLineEdit(self.appointment_table.item(selected_row, 5).text())),
            ("Estado:", QComboBox()),
        ]
        
        # Sample doctors
        fields[1][1].addItems(["Dr. Carlos García", "Dra. Ana López", "Dr. Luis Martínez", "Dra. Sofía Ramírez"])
        fields[1][1].setCurrentText(self.appointment_table.item(selected_row, 2).text())
        
        fields[5][1].addItems(["Confirmada", "Pendiente", "Cancelada"])
        fields[5][1].setCurrentText(self.appointment_table.item(selected_row, 6).text())
        
        # Configure date and time formats
        fields[2][1].setDisplayFormat("dd/MM/yyyy")
        fields[3][1].setDisplayFormat("HH:mm")
        
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
            datos = [
                fields[0][1].text(),  # Paciente
                fields[1][1].currentText(),  # Doctor
                fields[2][1].date().toString("dd/MM/yyyy"),  # Fecha
                fields[3][1].time().toString("HH:mm"),  # Hora
                fields[4][1].text(),  # Motivo
                fields[5][1].currentText()  # Estado
            ]
            
            if all(datos):
                for col, dato in enumerate(datos, start=1):
                    item = QTableWidgetItem(dato)
                    if col == 6:  # Columna de estado
                        if dato == "Confirmada":
                            item.setForeground(QColor(39, 174, 96))
                        elif dato == "Pendiente":
                            item.setForeground(QColor(243, 156, 18))
                        else:
                            item.setForeground(QColor(192, 57, 43))
                    self.appointment_table.setItem(selected_row, col, item)
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def toggle_appointment_status(self):
        selected_row = self.appointment_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione una cita para cambiar su estado.")
            return

        current_status = self.appointment_table.item(selected_row, 6).text()
        statuses = ["Pendiente", "Confirmada", "Cancelada"]
        current_index = statuses.index(current_status) if current_status in statuses else 0
        new_status = statuses[(current_index + 1) % len(statuses)]
        
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            f"¿Cambiar estado de la cita a '{new_status}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            item = QTableWidgetItem(new_status)
            if new_status == "Confirmada":
                item.setForeground(QColor(39, 174, 96))
            elif new_status == "Pendiente":
                item.setForeground(QColor(243, 156, 18))
            else:
                item.setForeground(QColor(192, 57, 43))
            self.appointment_table.setItem(selected_row, 6, item)

    def export_appointments(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Citas a CSV", 
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
                for col in range(self.appointment_table.columnCount()):
                    headers.append(self.appointment_table.horizontalHeaderItem(col).text())
                f.write(",".join(headers) + "\n")
                
                # Escribir datos
                for row in range(self.appointment_table.rowCount()):
                    row_data = []
                    for col in range(self.appointment_table.columnCount()):
                        item = self.appointment_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    f.write(",".join(row_data) + "\n")
                    
            QMessageBox.information(self, "Éxito", "Los datos se exportaron correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{str(e)}")