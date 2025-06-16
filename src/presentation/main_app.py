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
        # Pasar el servicio de autenticación al controlador de programas
        self.program_controller = ProgramController(self.auth_controller.auth_service)
        
        # Inicializar base de datos
        print("Inicializando base de datos...")
        self._initialize_database()
        
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
        self.engine.rootContext().setContextProperty("i18nManager", self.i18n_manager)
        
        # Cargar la interfaz principal
        self.engine.load(QUrl.fromLocalFile(str(qml_file)))
        
        if not self.engine.rootObjects():
            raise RuntimeError("Error al cargar la interfaz QML")
        
        print("Interfaz QML cargada correctamente.")
    
    def run(self):
        """Ejecuta la aplicación"""
        print("Iniciando bucle principal de la aplicación...")
        return self.app.exec()