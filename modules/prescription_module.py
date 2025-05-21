from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QDialogButtonBox, QHBoxLayout, QLineEdit, QComboBox, QMessageBox,
    QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from fpdf import FPDF
from datetime import datetime
import mysql.connector
import os

class IMSSPrescriptionPDF(FPDF):
    def header(self):
        if os.path.exists('imss.png'):
            try:
                self.image('imss.png', 10, 8, 30)
            except:
                pass
        self.set_font('Arial', 'B', 14)
        self.cell(0, 6, 'INSTITUTO MEXICANO DEL SEGURO SOCIAL', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'SEGURIDAD Y SOLIDARIDAD SOCIAL', 0, 1, 'C')
        self.ln(5)
        self.set_font('Arial', 'B', 11)
        self.cell(0, 6, 'DIRECCIÓN DE PRESTACIONES MÉDICAS', 0, 1, 'C')
        self.ln(5)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 8, 'RECETA INDIVIDUAL', 0, 1, 'C')
        self.ln(8)

    def prescription_body(self, data):
        try:
            fecha_obj = datetime.strptime(data['fecha'], '%Y-%m-%d')
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            fecha_formateada = f"{dias[fecha_obj.weekday()]} {fecha_obj.day} de {meses[fecha_obj.month-1]} del {fecha_obj.year}"
        except:
            fecha_formateada = data['fecha']

        self.set_font('Arial', '', 10)
        self.cell(0, 6, f"Fecha: {fecha_formateada}", 0, 1)
        self.ln(2)
        self.cell(45, 6, f"NSS : {data.get('nss', '')}", 0, 0)
        self.cell(45, 6, f"A.MED.: {data.get('amed', '')}", 0, 1)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, data.get('paciente', ''), 0, 1, 'C')
        if data.get('curp'):
            self.set_font('Arial', '', 10)
            self.cell(0, 6, f"CURP: {data['curp']}", 0, 1, 'C')
        self.cell(60, 6, f"DELEGACIÓN: {data.get('delegacion', '')}", 0, 0)
        self.cell(60, 6, f"UNIDAD-UMF NO. {data.get('unidad', '')}", 0, 0)
        self.cell(60, 6, f"CONSULTORIO: {data.get('consultorio', '')}", 0, 1)
        self.cell(60, 6, f"TURNO: {data.get('turno', '')}", 0, 0)
        if data.get('clave_postal'):
            self.cell(0, 6, f"CVE PTAL {data['clave_postal']}", 0, 1)
        else:
            self.ln(6)
        self.ln(5)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, f"Folio : {data.get('folio', '')}", 0, 1, 'C')
        self.ln(5)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 6, "ESTA RECETA NO SE SURTIRÁ DESPUÉS DE LAS 72 HORAS DE SU EXPEDICIÓN", 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 10)
        medicamentos = data.get('medicamentos', '')
        self.multi_cell(0, 6, medicamentos)
        self.ln(10)
        self.set_font('Arial', '', 10)
        self.cell(0, 6, "Nombre y firma del médico", 0, 1)
        self.cell(60, 6, data.get('doctor', ''), 0, 0)
        if data.get('cedula_medico'):
            self.cell(40, 6, f"Cédula Profesional {data['cedula_medico']}", 0, 0)
        if data.get('matricula_medico'):
            self.cell(0, 6, f"Matrícula {data['matricula_medico']}", 0, 1)
        self.ln(15)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(0, 4,
            "El IMSS pensando en ti y valorando tú tiempo, hoy cuenta con trámites digitales para que no hagas más filas,\n"
            "Visita www.imss.gob.mx/servicios-digitales o descarga la 'App IMSS digital' y realiza tus trámites desde Internet\n"
            "de una manera rápida y sencilla.", 0, 'C')
        self.ln(5)
        self.set_font('Arial', 'B', 10)
        self.cell(0, 6, "PACIENTE", 0, 1, 'C')
        self.line(self.get_x() + 70, self.get_y(), self.get_x() + 140, self.get_y())


class PrescriptionModule(QWidget):
    def __init__(self, db_config, parent=None):
        super().__init__(parent)
        self.db_config = db_config
        self.patients = []
        self.doctors = []
        self.load_users()
        self.setup_ui()
        self.load_recetas_data()

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def load_users(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT rol_id, nombre FROM roles WHERE nombre IN ('Paciente', 'Doctor')")
            roles = {nombre: rol_id for rol_id, nombre in cursor.fetchall()}
            if 'Paciente' in roles:
                cursor.execute("SELECT usuario_id, nombre FROM usuarios WHERE estado='activo' AND rol_id=%s ORDER BY nombre", (roles['Paciente'],))
                self.patients = cursor.fetchall()
            if 'Doctor' in roles:
                cursor.execute("SELECT usuario_id, nombre FROM usuarios WHERE estado='activo' AND rol_id=%s ORDER BY nombre", (roles['Doctor'],))
                self.doctors = cursor.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los usuarios:\n{e}")
        finally:
            cursor.close()
            conn.close()

    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Sistema de Recetas Médicas IMSS")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels([
            "ID", "Folio", "Paciente", "Doctor", "Fecha", "Medicamentos", "Indicaciones",
            "Estado", "NSS", "A. MED", "Delegación", "Unidad", "Consultorio", "Turno"
        ])
        self.table.setColumnHidden(0, True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Nueva Receta")
        btn_edit = QPushButton("Editar")
        btn_delete = QPushButton("Eliminar")
        btn_pdf = QPushButton("Generar PDF")

        btn_add.clicked.connect(self.add_record)
        btn_edit.clicked.connect(self.edit_record)
        btn_delete.clicked.connect(self.delete_record)
        btn_pdf.clicked.connect(self.generate_selected_pdf)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_pdf)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_recetas_data(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT r.receta_id, r.folio, 
                       p.nombre AS paciente, d.nombre AS doctor,
                      r.fecha, r.medicamentos, r.indicaciones,
                      r.estado, r.nss, r.amed, r.delegacion, r.unidad, r.consultorio, r.turno
                FROM recetas r
                JOIN usuarios p ON r.paciente_id = p.usuario_id
                JOIN usuarios d ON r.doctor_id = d.usuario_id
                ORDER BY r.fecha DESC
            """)
            records = cursor.fetchall()
            self.table.setRowCount(0)
            for row_data in records:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(row_data['receta_id'])))
                self.table.setItem(row, 1, QTableWidgetItem(str(row_data['folio'])))
                self.table.setItem(row, 2, QTableWidgetItem(row_data['paciente']))
                self.table.setItem(row, 3, QTableWidgetItem(row_data['doctor']))
                self.table.setItem(row, 4, QTableWidgetItem(row_data['fecha'].strftime("%Y-%m-%d") if row_data['fecha'] else ""))
                self.table.setItem(row, 5, QTableWidgetItem(row_data['medicamentos']))
                self.table.setItem(row, 6, QTableWidgetItem(row_data['indicaciones']))
                self.table.setItem(row, 7, QTableWidgetItem(row_data['estado']))
                self.table.setItem(row, 8, QTableWidgetItem(row_data['nss']))
                self.table.setItem(row, 9, QTableWidgetItem(row_data['amed']))
                self.table.setItem(row, 10, QTableWidgetItem(row_data['delegacion']))
                self.table.setItem(row, 11, QTableWidgetItem(row_data['unidad']))
                self.table.setItem(row, 12, QTableWidgetItem(row_data['consultorio']))
                self.table.setItem(row, 13, QTableWidgetItem(row_data['turno']))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar las recetas:\n{e}")
        finally:
            cursor.close()
            conn.close()

    def add_record(self):
        self.edit_record(new=True)

    def edit_record(self, new=False):
        if not new:
            current_row = self.table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Error", "Seleccione una receta para editar.")
                return
            receta_id = self.table.item(current_row, 0).text()
        else:
            receta_id = None

        dialog = QDialog(self)
        dialog.setWindowTitle("Nueva Receta" if new else "Editar Receta")
        form_layout = QFormLayout(dialog)

        # Campos formulario
        folio_edit = QLineEdit()
        folio_edit.setMaxLength(50)
        fecha_edit = QLineEdit()
        fecha_edit.setPlaceholderText("YYYY-MM-DD")
        medicamentos_edit = QLineEdit()
        indicaciones_edit = QLineEdit()
        nss_edit = QLineEdit()
        amed_edit = QLineEdit()
        delegacion_edit = QLineEdit()
        unidad_edit = QLineEdit()
        consultorio_edit = QLineEdit()
        turno_edit = QLineEdit()
        curp_edit = QLineEdit()
        clave_postal_edit = QLineEdit()
        cedula_medico_edit = QLineEdit()
        matricula_medico_edit = QLineEdit()

        paciente_combo = QComboBox()
        paciente_combo.addItem("--Seleccione--", None)
        for uid, name in self.patients:
            paciente_combo.addItem(name, uid)

        doctor_combo = QComboBox()
        doctor_combo.addItem("--Seleccione--", None)
        for uid, name in self.doctors:
            doctor_combo.addItem(name, uid)

        estado_combo = QComboBox()
        estado_combo.addItems(["activo", "cancelado"])

        # Agregar campos al formulario
        form_layout.addRow("Folio:", folio_edit)
        form_layout.addRow("Paciente:", paciente_combo)
        form_layout.addRow("Doctor:", doctor_combo)
        form_layout.addRow("Fecha (YYYY-MM-DD):", fecha_edit)
        form_layout.addRow("Medicamentos:", medicamentos_edit)
        form_layout.addRow("Indicaciones:", indicaciones_edit)
        form_layout.addRow("Estado:", estado_combo)
        form_layout.addRow("NSS:", nss_edit)
        form_layout.addRow("A. MED:", amed_edit)
        form_layout.addRow("Delegación:", delegacion_edit)
        form_layout.addRow("Unidad:", unidad_edit)
        form_layout.addRow("Consultorio:", consultorio_edit)
        form_layout.addRow("Turno:", turno_edit)
        form_layout.addRow("CURP:", curp_edit)
        form_layout.addRow("Clave Postal:", clave_postal_edit)
        form_layout.addRow("Cédula Médico:", cedula_medico_edit)
        form_layout.addRow("Matrícula Médico:", matricula_medico_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        form_layout.addWidget(buttons)

        # Cargar datos si es edición
        if not new:
            try:
                conn = self.get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM recetas WHERE receta_id = %s", (receta_id,))
                record = cursor.fetchone()
                if record:
                    folio_edit.setText(str(record.get('folio', '')))
                    fecha_edit.setText(record.get('fecha', '').strftime("%Y-%m-%d") if record.get('fecha') else '')
                    medicamentos_edit.setText(record.get('medicamentos', ''))
                    indicaciones_edit.setText(record.get('indicaciones', ''))
                    nss_edit.setText(record.get('nss', ''))
                    amed_edit.setText(record.get('amed', ''))
                    delegacion_edit.setText(record.get('delegacion', ''))
                    unidad_edit.setText(record.get('unidad', ''))
                    consultorio_edit.setText(record.get('consultorio', ''))
                    turno_edit.setText(record.get('turno', ''))
                    curp_edit.setText(record.get('curp', ''))
                    clave_postal_edit.setText(record.get('clave_postal', ''))
                    cedula_medico_edit.setText(record.get('cedula_medico', ''))
                    matricula_medico_edit.setText(record.get('matricula_medico', ''))
                    estado_combo.setCurrentText(record.get('estado', 'activo'))
                    # Seleccionar paciente
                    index_p = paciente_combo.findData(record.get('paciente_id'))
                    if index_p >= 0:
                        paciente_combo.setCurrentIndex(index_p)
                    # Seleccionar doctor
                    index_d = doctor_combo.findData(record.get('doctor_id'))
                    if index_d >= 0:
                        doctor_combo.setCurrentIndex(index_d)
                else:
                    QMessageBox.warning(self, "Error", "Receta no encontrada.")
                    dialog.reject()
                    return
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar la receta:\n{e}")
                dialog.reject()
                return
            finally:
                cursor.close()
                conn.close()

        def save_record():
            # Validaciones básicas
            if not folio_edit.text().strip():
                QMessageBox.warning(dialog, "Error", "Folio es obligatorio.")
                return
            if paciente_combo.currentData() is None:
                QMessageBox.warning(dialog, "Error", "Seleccione un paciente.")
                return
            if doctor_combo.currentData() is None:
                QMessageBox.warning(dialog, "Error", "Seleccione un doctor.")
                return
            # Validar fecha
            try:
                datetime.strptime(fecha_edit.text(), "%Y-%m-%d")
            except ValueError:
                QMessageBox.warning(dialog, "Error", "Fecha no tiene formato válido (YYYY-MM-DD).")
                return

            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                if new:
                    cursor.execute("""
                        INSERT INTO recetas (
                            folio, paciente_id, doctor_id, fecha, medicamentos, indicaciones, estado,
                            nss, amed, delegacion, unidad, consultorio, turno, curp, clave_postal,
                            cedula_medico, matricula_medico
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        folio_edit.text(), paciente_combo.currentData(), doctor_combo.currentData(),
                        fecha_edit.text(), medicamentos_edit.text(), indicaciones_edit.text(),
                        estado_combo.currentText(), nss_edit.text(), amed_edit.text(),
                        delegacion_edit.text(), unidad_edit.text(), consultorio_edit.text(),
                        turno_edit.text(), curp_edit.text(), clave_postal_edit.text(),
                        cedula_medico_edit.text(), matricula_medico_edit.text()
                    ))
                else:
                    cursor.execute("""
                        UPDATE recetas SET
                            folio=%s, paciente_id=%s, doctor_id=%s, fecha=%s, medicamentos=%s, indicaciones=%s,
                            estado=%s, nss=%s, amed=%s, delegacion=%s, unidad=%s, consultorio=%s,
                            turno=%s, curp=%s, clave_postal=%s, cedula_medico=%s, matricula_medico=%s
                        WHERE receta_id=%s
                    """, (
                        folio_edit.text(), paciente_combo.currentData(), doctor_combo.currentData(),
                        fecha_edit.text(), medicamentos_edit.text(), indicaciones_edit.text(),
                        estado_combo.currentText(), nss_edit.text(), amed_edit.text(),
                        delegacion_edit.text(), unidad_edit.text(), consultorio_edit.text(),
                        turno_edit.text(), curp_edit.text(), clave_postal_edit.text(),
                        cedula_medico_edit.text(), matricula_medico_edit.text(),
                        receta_id
                    ))
                conn.commit()
                QMessageBox.information(dialog, "Éxito", "Receta guardada correctamente.")
                dialog.accept()
                self.load_recetas_data()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"No se pudo guardar la receta:\n{e}")
            finally:
                cursor.close()
                conn.close()

        buttons.accepted.connect(save_record)
        buttons.rejected.connect(dialog.reject)

        dialog.exec_()

    def delete_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una receta para eliminar.")
            return
        receta_id = self.table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirmar eliminación",
                                     "¿Está seguro de eliminar la receta seleccionada?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM recetas WHERE receta_id=%s", (receta_id,))
                conn.commit()
                QMessageBox.information(self, "Éxito", "Receta eliminada correctamente.")
                self.load_recetas_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la receta:\n{e}")
            finally:
                cursor.close()
                conn.close()

    def generate_selected_pdf(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una receta para generar PDF.")
            return
        receta_id = self.table.item(current_row, 0).text()
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT r.*, p.nombre AS paciente, d.nombre AS doctor
                FROM recetas r
                JOIN usuarios p ON r.paciente_id = p.usuario_id
                JOIN usuarios d ON r.doctor_id = d.usuario_id
                WHERE r.receta_id = %s
            """, (receta_id,))
            data = cursor.fetchone()
            if not data:
                QMessageBox.warning(self, "Error", "Receta no encontrada.")
                return
            pdf = IMSSPrescriptionPDF()
            pdf.add_page()
            pdf.prescription_body(data)
            filename = f"Receta_{data['folio']}_{data['paciente'].replace(' ', '_')}.pdf"
            pdf.output(filename)
            QMessageBox.information(self, "PDF generado", f"PDF guardado como {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el PDF:\n{e}")
        finally:
            cursor.close()
            conn.close()
