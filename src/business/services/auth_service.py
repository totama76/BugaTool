"""
Servicio de autenticación
Gestiona la autenticación y autorización de usuarios
"""

from typing import Optional
from data.repositories.user_repository import UserRepository
from data.entities.user_entity import UserEntity

class AuthService:
    """Servicio de autenticación y autorización"""
    
    def __init__(self):
        self.user_repository = UserRepository()
        self.current_user: Optional[UserEntity] = None
    
    def login(self, username: str, password: str) -> bool:
        """Autentica un usuario"""
        try:
            user = self.user_repository.verify_password(username, password)
            if user:
                self.current_user = user
                print(f"Usuario autenticado: {user.username} ({user.role})")
                return True
            
            print("Credenciales incorrectas")
            return False
            
        except Exception as e:
            print(f"Error en login: {e}")
            return False
    
    def logout(self):
        """Cierra la sesión del usuario actual"""
        if self.current_user:
            print(f"Usuario {self.current_user.username} cerró sesión")
            self.current_user = None
    
    def is_authenticated(self) -> bool:
        """Verifica si hay un usuario autenticado"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[UserEntity]:
        """Obtiene el usuario actual"""
        return self.current_user
    
    def is_admin(self) -> bool:
        """Verifica si el usuario actual es administrador"""
        return (self.current_user is not None and 
                self.current_user.role == 'admin')
    
    def is_user(self) -> bool:
        """Verifica si el usuario actual es usuario normal"""
        return (self.current_user is not None and 
                self.current_user.role == 'user')
    
    def can_manage_users(self) -> bool:
        """Verifica si el usuario puede gestionar otros usuarios"""
        return self.is_admin()
    
    def can_manage_programs(self) -> bool:
        """Verifica si el usuario puede gestionar programas"""
        return self.is_admin()
    
    def can_execute_programs(self) -> bool:
        """Verifica si el usuario puede ejecutar programas"""
        return self.is_authenticated()
    
    def get_user_role_display(self) -> str:
        """Obtiene el rol del usuario en formato legible"""
        if not self.current_user:
            return "No autenticado"
        
        role_map = {
            'admin': 'Administrador',
            'user': 'Usuario'
        }
        
        return role_map.get(self.current_user.role, self.current_user.role)