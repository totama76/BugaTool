"""
Gestor de conexión a la base de datos SQLite
Singleton para manejo centralizado de conexiones
"""

import sqlite3
import threading
from pathlib import Path
from typing import Optional

class DatabaseConnection:
    """Gestor singleton de conexión a SQLite"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.db_path = None
            self.connection = None
            self._setup_database()
    
    def _setup_database(self):
        """Configura la base de datos"""
        # Crear directorio de datos
        project_root = Path(__file__).parent.parent.parent.parent
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)
        
        self.db_path = data_dir / "pressure_control.db"
        print(f"Base de datos configurada en: {self.db_path}")
        
        # Crear las tablas si no existen
        self._initialize_tables()
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        if self.connection is None:
            self.connection = sqlite3.connect(
                str(self.db_path), 
                check_same_thread=False
            )
            self.connection.row_factory = sqlite3.Row  # Para acceso por nombre de columna
        return self.connection
    
    def _initialize_tables(self):
        """Crea las tablas iniciales de la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    full_name TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Tabla de programas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS programs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    min_pressure REAL NOT NULL,
                    max_pressure REAL NOT NULL,
                    time_to_min_pressure INTEGER NOT NULL,
                    program_duration INTEGER NOT NULL,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Tabla de ejecuciones de programas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS program_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    program_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    status TEXT DEFAULT 'running',
                    min_pressure_reached BOOLEAN DEFAULT 0,
                    max_pressure_exceeded BOOLEAN DEFAULT 0,
                    stopped_manually BOOLEAN DEFAULT 0,
                    notes TEXT,
                    FOREIGN KEY (program_id) REFERENCES programs (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Tabla de lecturas de presión
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pressure_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id INTEGER,
                    pressure_value REAL NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (execution_id) REFERENCES program_executions (id)
                )
            ''')
            
            conn.commit()
            print("Tablas de base de datos inicializadas correctamente")
            
            # Crear usuario administrador por defecto si no existe
            self._create_default_admin()
            
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")
            if conn:
                conn.rollback()
    
    def _create_default_admin(self):
        """Crea un usuario administrador por defecto"""
        try:
            # Verificar si bcrypt está disponible
            try:
                import bcrypt
            except ImportError:
                print("Warning: bcrypt no disponible, no se puede crear usuario administrador")
                return
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verificar si ya existe un administrador
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            admin_count = cursor.fetchone()[0]
            
            if admin_count == 0:
                # Crear usuario admin por defecto
                default_password = "admin123"
                password_hash = bcrypt.hashpw(
                    default_password.encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role, full_name, is_active)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', password_hash, 'admin', 'Administrador', 1))
                
                conn.commit()
                print("Usuario administrador por defecto creado:")
                print("  Usuario: admin")
                print("  Contraseña: admin123")
                
        except Exception as e:
            print(f"Error creando usuario administrador: {e}")
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            self.connection = None