"""
Repositorio de usuarios
Gestiona las operaciones CRUD para usuarios
"""

import bcrypt
from datetime import datetime
from typing import Optional, List
from data.database.connection import DatabaseConnection
from data.entities.user_entity import UserEntity

class UserRepository:
    """Repositorio para gestión de usuarios"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_user(self, user: UserEntity, password: str) -> Optional[UserEntity]:
        """Crea un nuevo usuario"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Hash de la contraseña
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, full_name, email, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user.username,
                password_hash,
                user.role,
                user.full_name,
                user.email,
                user.is_active
            ))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            # Devolver el usuario creado
            return self.get_user_by_id(user_id)
            
        except Exception as e:
            print(f"Error creando usuario: {e}")
            conn.rollback()
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        """Obtiene un usuario por su ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            
            if row:
                return UserEntity.from_db_row(row)
            return None
            
        except Exception as e:
            print(f"Error obteniendo usuario por ID: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[UserEntity]:
        """Obtiene un usuario por su nombre de usuario"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,))
            row = cursor.fetchone()
            
            if row:
                return UserEntity.from_db_row(row)
            return None
            
        except Exception as e:
            print(f"Error obteniendo usuario por username: {e}")
            return None
    
    def verify_password(self, username: str, password: str) -> Optional[UserEntity]:
        """Verifica las credenciales de un usuario"""
        try:
            user = self.get_user_by_username(username)
            if not user:
                return None
            
            # Verificar contraseña
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                # Actualizar último login
                self.update_last_login(user.id)
                return user
            
            return None
            
        except Exception as e:
            print(f"Error verificando contraseña: {e}")
            return None
    
    def update_last_login(self, user_id: int) -> bool:
        """Actualiza la fecha de último login"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error actualizando último login: {e}")
            return False
    
    def get_all_users(self) -> List[UserEntity]:
        """Obtiene todos los usuarios activos"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY username')
            rows = cursor.fetchall()
            
            return [UserEntity.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"Error obteniendo todos los usuarios: {e}")
            return []
    
    def update_user(self, user: UserEntity) -> bool:
        """Actualiza un usuario existente"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users 
                SET full_name = ?, email = ?, role = ?, is_active = ?
                WHERE id = ?
            ''', (
                user.full_name,
                user.email,
                user.role,
                user.is_active,
                user.id
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error actualizando usuario: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Desactiva un usuario (soft delete)"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error desactivando usuario: {e}")
            return False