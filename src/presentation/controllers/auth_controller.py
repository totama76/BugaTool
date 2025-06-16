"""
Controlador de autenticación
Gestiona la comunicación entre la UI y los servicios de autenticación
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from business.services.auth_service import AuthService

class AuthController(QObject):
    """Controlador de autenticación para la interfaz"""
    
    # Señales
    loginResult = pyqtSignal(bool, str)  # success, message
    userChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_service = AuthService()
    
    @pyqtSlot(str, str)
    def login(self, username: str, password: str):
        """Intenta autenticar al usuario"""
        try:
            if not username.strip() or not password.strip():
                self.loginResult.emit(False, "Usuario y contraseña son requeridos")
                return
            
            success = self.auth_service.login(username.strip(), password)
            
            if success:
                self.userChanged.emit()
                role = self.auth_service.get_user_role_display()
                self.loginResult.emit(True, f"Bienvenido, {username} ({role})")
            else:
                self.loginResult.emit(False, "Usuario o contraseña incorrectos")
                
        except Exception as e:
            print(f"Error en login: {e}")
            self.loginResult.emit(False, "Error interno del sistema")
    
    @pyqtSlot()
    def logout(self):
        """Cierra la sesión del usuario"""
        self.auth_service.logout()
        self.userChanged.emit()
    
    def get_is_authenticated(self) -> bool:
        """Verifica si hay usuario autenticado"""
        return self.auth_service.is_authenticated()
    
    def get_current_username(self) -> str:
        """Obtiene el nombre del usuario actual"""
        user = self.auth_service.get_current_user()
        return user.username if user else ""
    
    def get_current_role(self) -> str:
        """Obtiene el rol del usuario actual"""
        return self.auth_service.get_user_role_display()
    
    def get_can_manage_programs(self) -> bool:
        """Verifica si puede gestionar programas"""
        return self.auth_service.can_manage_programs()
    
    def get_can_manage_users(self) -> bool:
        """Verifica si puede gestionar usuarios"""
        return self.auth_service.can_manage_users()
    
    # Propiedades para QML
    isAuthenticated = pyqtProperty(bool, get_is_authenticated, notify=userChanged)
    currentUsername = pyqtProperty(str, get_current_username, notify=userChanged)
    currentRole = pyqtProperty(str, get_current_role, notify=userChanged)
    canManagePrograms = pyqtProperty(bool, get_can_manage_programs, notify=userChanged)
    canManageUsers = pyqtProperty(bool, get_can_manage_users, notify=userChanged)