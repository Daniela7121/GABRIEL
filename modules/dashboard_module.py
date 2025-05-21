import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QSizePolicy, QGridLayout, QListWidget, QListWidgetItem,
    QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime


class DashboardModule(QWidget):
    def __init__(self, db_config, parent=None):
        super().__init__(parent)
        self.db_config = db_config
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Dashboard Principal")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        data = self.fetch_data()

        # --- Estadísticas principales ---
        stats = [
            ("Usuarios", str(data.get('usuarios', 0))),
            ("Hospitales", str(data.get('hospitales', 0))),
            ("Doctores", str(data.get('doctores', 0))),
            ("Pacientes", str(data.get('pacientes', 0))),
            ("Citas hoy", str(data.get('citas_hoy', 0))),
            ("Medicamentos", str(data.get('medicamentos', 0))),
            ("Consultorios", str(data.get('consultorios', 0))),
            ("Laboratorios", str(data.get('laboratorios', 0))),
        ]

        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        for i, (label, value) in enumerate(stats):
            card = self.create_stat_card(label, value)
            stats_grid.addWidget(card, i // 4, i % 4)
        layout.addLayout(stats_grid)

        # --- Gráfica ---
        chart_frame = QFrame()
        chart_frame.setStyleSheet("background-color: white; border-radius: 10px;")
        chart_layout = QVBoxLayout(chart_frame)
        chart_title = QLabel("Citas por Día (últimos 7 días)")
        chart_title.setFont(QFont("Arial", 14, QFont.Bold))
        chart_title.setAlignment(Qt.AlignCenter)
        chart_layout.addWidget(chart_title)

        chart_canvas = self.create_chart(data.get("citas_por_dia", {}))
        chart_layout.addWidget(chart_canvas)

        layout.addWidget(chart_frame)

        # --- Actividades recientes ---
        activity_frame = QFrame()
        activity_frame.setStyleSheet("background-color: white; border-radius: 10px;")
        activity_layout = QVBoxLayout(activity_frame)

        activity_title = QLabel("Actividades recientes")
        activity_title.setFont(QFont("Arial", 14, QFont.Bold))
        activity_title.setAlignment(Qt.AlignCenter)

        activity_list = QListWidget()
        for actividad in data.get("actividades", []):
            item = QListWidgetItem(actividad)
            activity_list.addItem(item)

        activity_layout.addWidget(activity_title)
        activity_layout.addWidget(activity_list)
        layout.addWidget(activity_frame)

    def create_stat_card(self, label, value):
        card = QFrame()
        card.setFrameShape(QFrame.Box)
        card.setLineWidth(1)
        card.setStyleSheet("background-color: white; border-radius: 10px;")
        card.setMinimumWidth(180)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(card)

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Bold))
        value_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(label)
        text_label.setFont(QFont("Arial", 12))
        text_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(value_label)
        layout.addWidget(text_label)

        return card

    def create_chart(self, citas_por_dia):
        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)

        fechas = list(citas_por_dia.keys())
        valores = list(citas_por_dia.values())

        ax.plot(fechas, valores, marker='o')
        ax.set_title("Citas registradas")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Cantidad")
        ax.grid(True)
        fig.tight_layout()

        return FigureCanvas(fig)

    def fetch_data(self):
        data = {
            'usuarios': 0, 'hospitales': 0, 'doctores': 0, 'pacientes': 0,
            'citas_hoy': 0, 'medicamentos': 0, 'consultorios': 0, 'laboratorios': 0,
            'citas_por_dia': {}, 'actividades': []
        }
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE estado='activo';")
            data['usuarios'] = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM hospitales;")
            data['hospitales'] = cursor.fetchone()['total']

            cursor.execute("""
                SELECT COUNT(*) AS total FROM usuarios u
                JOIN roles r ON u.rol_id = r.rol_id
                WHERE r.nombre = 'doctor' AND u.estado='activo';
            """)
            data['doctores'] = cursor.fetchone()['total']

            cursor.execute("""
                SELECT COUNT(*) AS total FROM usuarios u
                JOIN roles r ON u.rol_id = r.rol_id
                WHERE r.nombre = 'paciente' AND u.estado='activo';
            """)
            data['pacientes'] = cursor.fetchone()['total']

            cursor.execute("""
                SELECT COUNT(*) AS total FROM citas
                WHERE DATE(fecha_hora) = CURDATE() AND estado != 'cancelada';
            """)
            data['citas_hoy'] = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM medicamentos;")
            data['medicamentos'] = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM consultorios;")
            data['consultorios'] = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM laboratorios;")
            data['laboratorios'] = cursor.fetchone()['total']

            # Citas por día (últimos 7 días)
            cursor.execute("""
                SELECT DATE(fecha_hora) as fecha, COUNT(*) as total
                FROM citas
                WHERE fecha_hora >= CURDATE() - INTERVAL 6 DAY
                GROUP BY DATE(fecha_hora)
                ORDER BY fecha;
            """)
            citas = cursor.fetchall()
            fechas = [(datetime.date.today() - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
            data['citas_por_dia'] = {f: 0 for f in fechas}
            for row in citas:
                data['citas_por_dia'][row['fecha'].strftime("%Y-%m-%d")] = row['total']

            # Actividades recientes (simulado)
            cursor.execute("""
                SELECT CONCAT(u.nombre, ' realizó una acción el ', DATE_FORMAT(NOW(), '%d-%m-%Y')) AS actividad
                FROM usuarios u
                ORDER BY u.usuario_id DESC
                LIMIT 5;
            """)
            rows = cursor.fetchall()
            data['actividades'] = [r['actividad'] for r in rows]

            cursor.close()
            conn.close()
        except Error as e:
            QMessageBox.critical(self, "Error Base de Datos", f"No se pudieron obtener los datos:\n{e}")

        return data
