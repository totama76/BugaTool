"""
Repositorio de ejecuciones
Gestiona las operaciones CRUD para ejecuciones de programas
"""

from datetime import datetime
from typing import Optional, List
from data.database.connection import DatabaseConnection
from data.entities.execution_entity import ExecutionEntity

class ExecutionRepository:
    """Repositorio para gestión de ejecuciones"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_execution(self, execution: ExecutionEntity) -> Optional[ExecutionEntity]:
        """Crea una nueva ejecución"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO program_executions (
                    program_id, user_id, status, min_pressure_reached,
                    max_pressure_exceeded, stopped_manually, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                execution.program_id,
                execution.user_id,
                execution.status,
                execution.min_pressure_reached,
                execution.max_pressure_exceeded,
                execution.stopped_manually,
                execution.notes
            ))
            
            execution_id = cursor.lastrowid
            conn.commit()
            
            return self.get_execution_by_id(execution_id)
            
        except Exception as e:
            print(f"Error creando ejecución: {e}")
            conn.rollback()
            return None
    
    def get_execution_by_id(self, execution_id: int) -> Optional[ExecutionEntity]:
        """Obtiene una ejecución por su ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM program_executions WHERE id = ?', (execution_id,))
            row = cursor.fetchone()
            
            if row:
                return ExecutionEntity.from_db_row(row)
            return None
            
        except Exception as e:
            print(f"Error obteniendo ejecución por ID: {e}")
            return None
    
    def update_execution(self, execution: ExecutionEntity) -> bool:
        """Actualiza una ejecución existente"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE program_executions 
                SET end_time = ?, status = ?, min_pressure_reached = ?,
                    max_pressure_exceeded = ?, stopped_manually = ?, notes = ?
                WHERE id = ?
            ''', (
                execution.end_time.isoformat() if execution.end_time else None,
                execution.status,
                execution.min_pressure_reached,
                execution.max_pressure_exceeded,
                execution.stopped_manually,
                execution.notes,
                execution.id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error actualizando ejecución: {e}")
            conn.rollback()
            return False
    
    def get_executions_by_program(self, program_id: int) -> List[ExecutionEntity]:
        """Obtiene todas las ejecuciones de un programa"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM program_executions 
                WHERE program_id = ? 
                ORDER BY start_time DESC
            ''', (program_id,))
            
            rows = cursor.fetchall()
            return [ExecutionEntity.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"Error obteniendo ejecuciones por programa: {e}")
            return []
    
    def get_recent_executions(self, limit: int = 10) -> List[ExecutionEntity]:
        """Obtiene las ejecuciones más recientes"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM program_executions 
                ORDER BY start_time DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            return [ExecutionEntity.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"Error obteniendo ejecuciones recientes: {e}")
            return []
    
    def record_pressure_reading(self, execution_id: int, pressure_value: float) -> bool:
        """Registra una lectura de presión durante la ejecución"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO pressure_readings (execution_id, pressure_value)
                VALUES (?, ?)
            ''', (execution_id, pressure_value))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error registrando lectura de presión: {e}")
            conn.rollback()
            return False