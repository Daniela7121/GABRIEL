import inspect
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QStackedWidget, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QIcon

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Administrador")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #ECF0F1;")
        self.init_ui()
        
    def init_ui(self):
        menu_items = [
            "Panel Principal", "Usuarios", "Hospitales", "Auditoría", "Doctores", 
            "Pacientes", "Administrativo", "Consultorios", "Laboratorios", 
            "Citas", "Farmacia", "Facturacion", "Cerrar Sesión"
        ]
        
        icons = {
            "Panel Principal": "dashboard",
            "Usuarios": "user",
            "Hospitales": "hospital",
            "Auditoría": "document",
            "Doctores": "doctors",
            "Pacientes": "patient",
            "Administrativo": "admin",
            "Consultorios": "office",
            "Laboratorios": "lab",
            "Citas": "calendar",
            "Farmacia": "pharmacy",
            "Facturacion": "billing",
            "Cerrar Sesión": "logout"
        }
        
        self.menu = QListWidget()
        self.menu.setFixedWidth(220)
        self.menu.setStyleSheet("""
            QListWidget {
                background-color: #2C3E50;
                color: white;
                border: none;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #34495E;
            }
            QListWidget::item:selected {
                background-color: #3498DB;
                font-weight: bold;
            }
        """)
        
        for item in menu_items:
            icon_name = icons.get(item, "folder")
            icon = QIcon.fromTheme(icon_name)
            list_item = QListWidgetItem(icon, item)
            self.menu.addItem(list_item)
        
        self.menu.currentRowChanged.connect(self.display_view)

        self.stack = QStackedWidget(self)

        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '12345678',
            'database': 'hospitales',
            'port': 3306,
        }

        # Importar módulos
        from modules.dashboard_module import DashboardModule
        from modules.users_module import UsersModule
        from modules.hospitals_module import HospitalsModule
        from modules.audit_module import AuditModule
        from modules.doctors_module import DoctorsModule
        from modules.patients_module import PatientsModule
        from modules.administrative_module import AdministrativeModule
        from modules.offices_module import OfficesModule
        from modules.labs_module import LabsModule
        from modules.appointments_module import AppointmentsModule
        from modules.pharmacy_module import PharmacyModule
        from modules.billing_module import BillingModule

        modules = [
            DashboardModule,
            UsersModule,
            HospitalsModule,
            AuditModule,
            DoctorsModule,
            PatientsModule,
            AdministrativeModule,
            OfficesModule,
            LabsModule,
            AppointmentsModule,
            PharmacyModule,
            BillingModule
        ]

        for ModuleClass in modules:
            # Inspeccionamos si el __init__ acepta db_config
            sig = inspect.signature(ModuleClass.__init__)
            if 'db_config' in sig.parameters:
                widget = ModuleClass(db_config)
            else:
                widget = ModuleClass()
            self.stack.addWidget(widget)

        # Para "Cerrar Sesión" añadimos un widget vacío
        self.stack.addWidget(QWidget())

        layout = QHBoxLayout()
        layout.addWidget(self.menu)
        layout.addWidget(self.stack)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.menu.setCurrentRow(0)

    def display_view(self, index):
        if index == 12:  # Cerrar Sesión
            reply = QMessageBox.question(
                self, 'Cerrar Sesión',
                '¿Está seguro que desea cerrar sesión?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.close()
                from views.login_view import LoginWindow
                self.login_window = LoginWindow()
                self.login_window.show()
            else:
                current_index = self.stack.currentIndex()
                self.menu.blockSignals(True)
                self.menu.setCurrentRow(current_index)
                self.menu.blockSignals(False)
        else:
            self.stack.setCurrentIndex(index)
