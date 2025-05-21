from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QFrame, QHBoxLayout, QMessageBox, QFileDialog, QComboBox, QDialog, QFormLayout,
    QDateEdit, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate
import mysql.connector
from datetime import datetime


class PatientForm(QDialog):
    def __init__(self, db, patient_data=None):
        super().__init__()
        self.db = db
        self.patient_data = patient_data
        self.setWindowTitle("Agregar / Editar Paciente")
        self.setMinimumWidth(400)
        layout = QFormLayout()

        self.nombre = QLineEdit()
        self.email = QLineEdit()
        self.fecha_nacimiento = QDateEdit()
        self.fecha_nacimiento.setCalendarPopup(True)
        self.fecha_nacimiento.setDate(QDate.currentDate())

        self.genero = QComboBox()
        self.genero.addItems(['masculino', 'femenino', 'otro', 'prefiero_no_decirlo'])

        self.tipo_sangre = QComboBox()
        self.tipo_sangre.addItems(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'desconocido'])

        self.altura = QDoubleSpinBox()
        self.altura.setSuffix(" cm")
        self.altura.setMaximum(250)

        self.peso = QDoubleSpinBox()
        self.peso.setSuffix(" kg")
        self.peso.setMaximum(500)

        self.direccion = QLineEdit()
        self.telefono = QLineEdit()
        self.contacto_emergencia_nombre = QLineEdit()
        self.contacto_emergencia_telefono = QLineEdit()
        self.seguro_medico = QLineEdit()
        self.numero_poliza = QLineEdit()

        layout.addRow("Nombre:", self.nombre)
        layout.addRow("Email:", self.email)
        layout.addRow("Fecha de Nacimiento:", self.fecha_nacimiento)
        layout.addRow("Género:", self.genero)
        layout.addRow("Tipo de Sangre:", self.tipo_sangre)
        layout.addRow("Altura:", self.altura)
        layout.addRow("Peso:", self.peso)
        layout.addRow("Dirección:", self.direccion)
        layout.addRow("Teléfono:", self.telefono)
        layout.addRow("Contacto Emergencia:", self.contacto_emergencia_nombre)
        layout.addRow("Tel. Emergencia:", self.contacto_emergencia_telefono)
        layout.addRow("Seguro Médico:", self.seguro_medico)
        layout.addRow("No. Póliza:", self.numero_poliza)

        self.save_btn = QPushButton("Guardar")
        self.save_btn.clicked.connect(self.save_patient)
        layout.addRow(self.save_btn)

        if patient_data:
            self.load_data()

        self.setLayout(layout)

    def load_data(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, u.nombre, u.email FROM pacientes p
            JOIN usuarios u ON u.usuario_id = p.usuario_id
            WHERE p.paciente_id = %s
        """, (self.patient_data['paciente_id'],))
        row = cursor.fetchone()
        if row:
            self.nombre.setText(row["nombre"])
            self.email.setText(row["email"])
            self.fecha_nacimiento.setDate(QDate.fromString(str(row["fecha_nacimiento"]), "yyyy-MM-dd"))
            self.genero.setCurrentText(row["genero"])
            self.tipo_sangre.setCurrentText(row["tipo_sangre"])
            self.altura.setValue(float(row["altura"] or 0))
            self.peso.setValue(float(row["peso"] or 0))
            self.direccion.setText(row["direccion"] or "")
            self.telefono.setText(row["telefono"] or "")
            self.contacto_emergencia_nombre.setText(row["contacto_emergencia_nombre"] or "")
            self.contacto_emergencia_telefono.setText(row["contacto_emergencia_telefono"] or "")
            self.seguro_medico.setText(row["seguro_medico"] or "")
            self.numero_poliza.setText(row["numero_poliza_seguro"] or "")
        cursor.close()

    def save_patient(self):
        try:
            cursor = self.db.cursor()
            if self.patient_data:
                # Update
                cursor.execute("UPDATE usuarios SET nombre=%s, email=%s WHERE usuario_id=%s",
                               (self.nombre.text(), self.email.text(), self.patient_data['usuario_id']))
                cursor.execute("""
                    UPDATE pacientes SET fecha_nacimiento=%s, genero=%s, tipo_sangre=%s, altura=%s,
                        peso=%s, direccion=%s, telefono=%s, contacto_emergencia_nombre=%s,
                        contacto_emergencia_telefono=%s, seguro_medico=%s, numero_poliza_seguro=%s
                    WHERE usuario_id=%s
                """, (
                    self.fecha_nacimiento.date().toString("yyyy-MM-dd"), self.genero.currentText(),
                    self.tipo_sangre.currentText(), self.altura.value(), self.peso.value(),
                    self.direccion.text(), self.telefono.text(), self.contacto_emergencia_nombre.text(),
                    self.contacto_emergencia_telefono.text(), self.seguro_medico.text(), self.numero_poliza.text(),
                    self.patient_data['usuario_id']
                ))
            else:
                # Insert
                cursor.execute("""
                    INSERT INTO usuarios (nombre, email, contrasena, rol_id)
                    VALUES (%s, %s, %s, %s)
                """, (self.nombre.text(), self.email.text(), '123456', 3))  # rol_id 3 para pacientes
                usuario_id = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO pacientes (usuario_id, fecha_nacimiento, genero, tipo_sangre, altura,
                        peso, direccion, telefono, contacto_emergencia_nombre, contacto_emergencia_telefono,
                        seguro_medico, numero_poliza_seguro)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    usuario_id,
                    self.fecha_nacimiento.date().toString("yyyy-MM-dd"),
                    self.genero.currentText(), self.tipo_sangre.currentText(),
                    self.altura.value(), self.peso.value(), self.direccion.text(), self.telefono.text(),
                    self.contacto_emergencia_nombre.text(), self.contacto_emergencia_telefono.text(),
                    self.seguro_medico.text(), self.numero_poliza.text()
                ))

            self.db.commit()
            QMessageBox.information(self, "Éxito", "Paciente guardado correctamente.")
            self.accept()
        except Exception as e:
            self.db.rollback()
            QMessageBox.critical(self, "Error", str(e))


class PatientsModule(QWidget):
    def __init__(self, db_config, parent=None):
        super().__init__(parent)
        self.db_config = db_config
        self.db = mysql.connector.connect(**self.db_config)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Gestión de Pacientes")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        tool_frame = QFrame()
        tool_layout = QHBoxLayout()

        self.patient_search = QLineEdit()
        self.patient_search.setPlaceholderText("Buscar por nombre o ID...")
        self.patient_filter = QComboBox()
        self.patient_filter.addItems(["Todos", "Activos", "Inactivos"])

        search_btn = QPushButton("Buscar")
        search_btn.clicked.connect(self.filter_patients)

        tool_layout.addWidget(self.patient_search)
        tool_layout.addWidget(self.patient_filter)
        tool_layout.addWidget(search_btn)
        tool_frame.setLayout(tool_layout)
        layout.addWidget(tool_frame)

        self.patient_table = QTableWidget(0, 6)
        self.patient_table.setHorizontalHeaderLabels(["ID", "Nombre", "Género", "Edad", "Teléfono", "Estado"])
        self.patient_table.horizontalHeader().setStretchLastSection(True)
        self.patient_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.patient_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.patient_table)

        btn_layout = QHBoxLayout()
        actions = [
            ("Agregar Paciente", self.add_patient),
            ("Editar Paciente", self.edit_patient),
            ("Cambiar Estado", self.toggle_patient_status),
            ("Exportar a CSV", self.export_patients)
        ]
        for text, handler in actions:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_data(self):
        cursor = self.db.cursor()
        query = """
            SELECT p.paciente_id, u.nombre, p.genero,
                   TIMESTAMPDIFF(YEAR, p.fecha_nacimiento, CURDATE()) AS edad,
                   p.telefono, IF(u.estado='activo', 'Activo', 'Inactivo'), p.usuario_id
            FROM pacientes p
            JOIN usuarios u ON p.usuario_id = u.usuario_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        self.patient_table.setRowCount(0)
        for row_data in results:
            row = self.patient_table.rowCount()
            self.patient_table.insertRow(row)
            for col, data in enumerate(row_data[:6]):
                item = QTableWidgetItem(str(data))
                if col == 5:
                    item.setForeground(QColor(39, 174, 96) if data == "Activo" else QColor(192, 57, 43))
                self.patient_table.setItem(row, col, item)
            self.patient_table.setRowHeight(row, 30)
        cursor.close()

    def get_selected_patient(self):
        row = self.patient_table.currentRow()
        if row < 0:
            return None
        return {
            "paciente_id": int(self.patient_table.item(row, 0).text()),
            "usuario_id": self.get_usuario_id(int(self.patient_table.item(row, 0).text()))
        }

    def get_usuario_id(self, paciente_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT usuario_id FROM pacientes WHERE paciente_id=%s", (paciente_id,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def add_patient(self):
        dialog = PatientForm(self.db)
        if dialog.exec_():
            self.load_data()

    def edit_patient(self):
        data = self.get_selected_patient()
        if not data:
            QMessageBox.warning(self, "Advertencia", "Selecciona un paciente.")
            return
        dialog = PatientForm(self.db, patient_data=data)
        if dialog.exec_():
            self.load_data()

    def toggle_patient_status(self):
        data = self.get_selected_patient()
        if not data:
            QMessageBox.warning(self, "Advertencia", "Selecciona un paciente.")
            return
        cursor = self.db.cursor()
        cursor.execute("SELECT estado FROM usuarios WHERE usuario_id = %s", (data['usuario_id'],))
        estado_actual = cursor.fetchone()[0]
        nuevo_estado = "inactivo" if estado_actual == "activo" else "activo"
        cursor.execute("UPDATE usuarios SET estado = %s WHERE usuario_id = %s", (nuevo_estado, data['usuario_id']))
        self.db.commit()
        cursor.close()
        self.load_data()

    def filter_patients(self):
        search = self.patient_search.text().lower()
        status_filter = self.patient_filter.currentText()
        for row in range(self.patient_table.rowCount()):
            name = self.patient_table.item(row, 1).text().lower()
            id_ = self.patient_table.item(row, 0).text().lower()
            estado = self.patient_table.item(row, 5).text()
            visible = True
            if search and search not in name and search not in id_:
                visible = False
            if status_filter == "Activos" and estado != "Activo":
                visible = False
            elif status_filter == "Inactivos" and estado != "Inactivo":
                visible = False
            self.patient_table.setRowHidden(row, not visible)

    def export_patients(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Exportar Pacientes", "", "CSV Files (*.csv)")
        if not file_name:
            return
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                headers = [self.patient_table.horizontalHeaderItem(i).text() for i in range(self.patient_table.columnCount())]
                file.write(",".join(headers) + "\n")
                for row in range(self.patient_table.rowCount()):
                    row_data = [self.patient_table.item(row, col).text() for col in range(self.patient_table.columnCount())]
                    file.write(",".join(row_data) + "\n")
            QMessageBox.information(self, "Éxito", "Pacientes exportados correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar:\n{str(e)}")
