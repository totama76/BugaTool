"""
Entidad de programa
Representa un programa de control en la base de datos
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ProgramEntity:
    """Entidad de programa para la base de datos"""
    
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    min_pressure: float = 0.0
    max_pressure: float = 100.0
    time_to_min_pressure: int = 5  # en minutos
    program_duration: int = 30  # en minutos
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'min_pressure': self.min_pressure,
            'max_pressure': self.max_pressure,
            'time_to_min_pressure': self.time_to_min_pressure,
            'program_duration': self.program_duration,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_db_row(cls, row) -> 'ProgramEntity':
        """Crea una entidad desde una fila de base de datos"""
        return cls(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            min_pressure=float(row['min_pressure']),
            max_pressure=float(row['max_pressure']),
            time_to_min_pressure=int(row['time_to_min_pressure']),
            program_duration=int(row['program_duration']),
            created_by=row['created_by'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
            is_active=bool(row['is_active'])
        )