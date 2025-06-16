"""
Entidad de ejecución de programa
Representa una ejecución de programa en la base de datos
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ExecutionEntity:
    """Entidad de ejecución de programa para la base de datos"""
    
    id: Optional[int] = None
    program_id: int = 0
    user_id: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str = "running"  # 'running', 'completed', 'stopped', 'error'
    min_pressure_reached: bool = False
    max_pressure_exceeded: bool = False
    stopped_manually: bool = False
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'id': self.id,
            'program_id': self.program_id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'min_pressure_reached': self.min_pressure_reached,
            'max_pressure_exceeded': self.max_pressure_exceeded,
            'stopped_manually': self.stopped_manually,
            'notes': self.notes
        }
    
    @classmethod
    def from_db_row(cls, row) -> 'ExecutionEntity':
        """Crea una entidad desde una fila de base de datos"""
        return cls(
            id=row['id'],
            program_id=row['program_id'],
            user_id=row['user_id'],
            start_time=datetime.fromisoformat(row['start_time']) if row['start_time'] else None,
            end_time=datetime.fromisoformat(row['end_time']) if row['end_time'] else None,
            status=row['status'],
            min_pressure_reached=bool(row['min_pressure_reached']),
            max_pressure_exceeded=bool(row['max_pressure_exceeded']),
            stopped_manually=bool(row['stopped_manually']),
            notes=row['notes']
        )