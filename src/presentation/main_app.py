"""
Aplicación principal PyQt6
Gestiona la ventana principal y la carga de componentes QML
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import qmlRegisterType, QQmlApplicationEngine
from PyQt6.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QIcon

# Importaciones absolutas corregidas
from utils.config_loader import ConfigLoader
from utils.i18n_manager import I18nManager
from presentation.controllers.main_controller import MainController
from presentation.controllers.auth_controller import AuthController
from presentation.controllers.program_controller import ProgramController
from presentation.controllers.execution_controller import ExecutionController

class PressureControlApp:
    """Aplicación principal del sistema de control de presión"""
    
    def __init__(self, argv):
        """Inicializa la aplicación PyQt6"""
        print("Inicializando aplicación PyQt6...")
        self.app = QApplication(argv)
        self.engine = QQmlApplicationEngine()
        
        print("Cargando configuración...")
        self.config_loader = ConfigLoader()
        self.i18n_manager = I18nManager()
        
        print("Inicializando controladores...")
        self.main_controller = MainController()
        self.auth_controller = AuthController()
        # Pasar el servicio de autenticación a los demás controladores
        self.program_controller = ProgramController(self.auth_controller.auth_service)
        self.execution_controller = ExecutionController(self.auth_controller.auth_service)
        
        # Conectar servicios entre controladores
        self.main_controller.set_execution_service(self.execution_controller.get_execution_service())
        
        # Inicializar base de datos
        print("Inicializando base de datos...")
        self._initialize_database()
        
        # Configurar verificación de ejecuciones después del login
        self._setup_execution_verification()
        
        self._setup_application()
        self._register_qml_types()
        self._load_main_qml()
        print("Aplicación inicializada correctamente.")
    
    def _initialize_database(self):
        """Inicializa la base de datos"""
        try:
            from data.database.connection import DatabaseConnection
            db = DatabaseConnection()
            print("Base de datos inicializada correctamente")
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")
    
    def _setup_execution_verification(self):
        """Configura la verificación de ejecuciones después del login"""
        try:
            # Conectar señal de login exitoso para verificar ejecuciones
            self.auth_controller.loginResult.connect(self._on_login_success)
            print("Verificación de ejecuciones configurada para después del login")
            
        except Exception as e:
            print(f"Error configurando verificación de ejecuciones: {e}")
    
    def _on_login_success(self, success: bool, message: str):
        """Maneja el resultado del login y verifica ejecuciones si es exitoso"""
        if success:
            print("Login exitoso, verificando ejecuciones incompletas...")
            # Pequeño delay para asegurar que el login se complete
            QTimer.singleShot(500, self._check_incomplete_executions_after_login)
    
    def _check_incomplete_executions_after_login(self):
        """Verifica ejecuciones incompletas después del login exitoso"""
        try:
            execution_service = self.execution_controller.get_execution_service()
            incomplete_info = execution_service.check_for_incomplete_execution()
            
            if incomplete_info and incomplete_info.get('should_resume'):
                execution = incomplete_info['execution']
                program = incomplete_info['program']
                
                print(f"Ejecución incompleta encontrada después del login: {program.name}")
                
                # Resumir la ejecución
                if execution_service.resume_execution(execution, program):
                    # Notificar a QML que debe mostrar la ejecución
                    self.engine.rootContext().setContextProperty("shouldShowExecutionAfterLogin", True)
                    self.engine.rootContext().setContextProperty("resumedProgramAfterLogin", program.to_dict())
                    
                    # Emitir señal para que QML maneje la navegación
                    self.execution_controller.executionResumed.emit(program.to_dict())
                else:
                    # Si no se puede resumir, marcar como detenida
                    from datetime import datetime
                    execution.status = 'stopped'
                    execution.stopped_manually = True
                    execution.end_time = datetime.now()
                    execution_service.execution_repository.update_execution(execution)
                    print("No se pudo resumir la ejecución, marcada como detenida")
            else:
                print("No se encontraron ejecuciones incompletas")
                self.engine.rootContext().setContextProperty("shouldShowExecutionAfterLogin", False)
                self.engine.rootContext().setContextProperty("resumedProgramAfterLogin", None)
                
        except Exception as e:
            print(f"Error verificando ejecuciones después del login: {e}")
            self.engine.rootContext().setContextProperty("shouldShowExecutionAfterLogin", False)
            self.engine.rootContext().setContextProperty("resumedProgramAfterLogin", None)
    
    def _setup_application(self):
        """Configura propiedades básicas de la aplicación"""
        self.app.setApplicationName("Pressure Control System")
        self.app.setApplicationVersion("0.1.0")
        self.app.setOrganizationName("totama76")
        
        # Cargar configuración inicial
        config = self.config_loader.load_config()
        print(f"Configuración cargada: {config.get('language', 'es')}")
        
        # Configurar idioma inicial
        default_language = config.get('language', 'es')
        self.i18n_manager.set_language(default_language)
        
        # Configurar icono si existe
        icon_path = Path(__file__).parent.parent.parent / "assets" / "images" / "logo.png"
        if icon_path.exists():
            self.app.setWindowIcon(QIcon(str(icon_path)))
    
    def _register_qml_types(self):
        """Registra tipos personalizados para QML"""
        # Registrar controladores
        qmlRegisterType(MainController, "PressureControl", 1, 0, "MainController")
        qmlRegisterType(AuthController, "PressureControl", 1, 0, "AuthController")
        qmlRegisterType(ProgramController, "PressureControl", 1, 0, "ProgramController")
        qmlRegisterType(ExecutionController, "PressureControl", 1, 0, "ExecutionController")
        print("Tipos QML registrados.")
    
    def _load_main_qml(self):
        """Carga el archivo QML principal"""
        qml_file = Path(__file__).parent / "qml" / "main.qml"
        
        if not qml_file.exists():
            raise FileNotFoundError(f"Archivo QML principal no encontrado: {qml_file}")
        
        print(f"Cargando interfaz QML desde: {qml_file}")
        
        # Exponer controladores al contexto QML
        self.engine.rootContext().setContextProperty("mainController", self.main_controller)
        self.engine.rootContext().setContextProperty("authController", self.auth_controller)
        self.engine.rootContext().setContextProperty("programController", self.program_controller)
        self.engine.rootContext().setContextProperty("executionController", self.execution_controller)
        self.engine.rootContext().setContextProperty("i18nManager", self.i18n_manager)
        
        # Inicializar propiedades de ejecución resumida (se actualizarán después del login)
        self.engine.rootContext().setContextProperty("shouldShowExecutionAfterLogin", False)
        self.engine.rootContext().setContextProperty("resumedProgramAfterLogin", None)
        
        # Cargar la interfaz principal
        self.engine.load(QUrl.fromLocalFile(str(qml_file)))
        
        if not self.engine.rootObjects():
            raise RuntimeError("Error al cargar la interfaz QML")
        
        print("Interfaz QML cargada correctamente.")
    
    def run(self):
        """Ejecuta la aplicación"""
        print("Iniciando bucle principal de la aplicación...")
        return self.app.exec()