"""
Entidad de usuario
Representa un usuario en la base de datos
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserEntity:
    """Entidad de usuario para la base de datos"""
    
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    role: str = "user"  # 'admin' o 'user'
    full_name: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'role': self.role,
            'full_name': self.full_name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_db_row(cls, row) -> 'UserEntity':
        """Crea una entidad desde una fila de base de datos"""
        return cls(
            id=row['id'],
            username=row['username'],
            password_hash=row['password_hash'],
            role=row['role'],
            full_name=row['full_name'],
            email=row['email'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            last_login=datetime.fromisoformat(row['last_login']) if row['last_login'] else None,
            is_active=bool(row['is_active'])
        )