"""
Repositorio de programas
Gestiona las operaciones CRUD para programas de control
"""

from datetime import datetime
from typing import Optional, List
from data.database.connection import DatabaseConnection
from data.entities.program_entity import ProgramEntity

class ProgramRepository:
    """Repositorio para gestión de programas"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_program(self, program: ProgramEntity) -> Optional[ProgramEntity]:
        """Crea un nuevo programa"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO programs (
                    name, description, min_pressure, max_pressure, 
                    time_to_min_pressure, program_duration, created_by, is_active
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                program.name,
                program.description,
                program.min_pressure,
                program.max_pressure,
                program.time_to_min_pressure,
                program.program_duration,
                program.created_by,
                program.is_active
            ))
            
            program_id = cursor.lastrowid
            conn.commit()
            
            # Devolver el programa creado
            return self.get_program_by_id(program_id)
            
        except Exception as e:
            print(f"Error creando programa: {e}")
            conn.rollback()
            return None
    
    def get_program_by_id(self, program_id: int) -> Optional[ProgramEntity]:
        """Obtiene un programa por su ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM programs WHERE id = ?', (program_id,))
            row = cursor.fetchone()
            
            if row:
                return ProgramEntity.from_db_row(row)
            return None
            
        except Exception as e:
            print(f"Error obteniendo programa por ID: {e}")
            return None
    
    def get_program_by_name(self, name: str) -> Optional[ProgramEntity]:
        """Obtiene un programa por su nombre"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM programs WHERE name = ? AND is_active = 1', (name,))
            row = cursor.fetchone()
            
            if row:
                return ProgramEntity.from_db_row(row)
            return None
            
        except Exception as e:
            print(f"Error obteniendo programa por nombre: {e}")
            return None
    
    def get_all_programs(self, include_inactive: bool = False) -> List[ProgramEntity]:
        """Obtiene todos los programas"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            if include_inactive:
                cursor.execute('SELECT * FROM programs ORDER BY created_at DESC')
            else:
                cursor.execute('SELECT * FROM programs WHERE is_active = 1 ORDER BY created_at DESC')
            
            rows = cursor.fetchall()
            return [ProgramEntity.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"Error obteniendo todos los programas: {e}")
            return []
    
    def get_programs_by_user(self, user_id: int) -> List[ProgramEntity]:
        """Obtiene todos los programas creados por un usuario"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM programs 
                WHERE created_by = ? AND is_active = 1 
                ORDER BY created_at DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            return [ProgramEntity.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"Error obteniendo programas por usuario: {e}")
            return []
    
    def update_program(self, program: ProgramEntity) -> bool:
        """Actualiza un programa existente"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE programs 
                SET name = ?, description = ?, min_pressure = ?, max_pressure = ?,
                    time_to_min_pressure = ?, program_duration = ?, 
                    updated_at = CURRENT_TIMESTAMP, is_active = ?
                WHERE id = ?
            ''', (
                program.name,
                program.description,
                program.min_pressure,
                program.max_pressure,
                program.time_to_min_pressure,
                program.program_duration,
                program.is_active,
                program.id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error actualizando programa: {e}")
            conn.rollback()
            return False
    
    def delete_program(self, program_id: int) -> bool:
        """Desactiva un programa (soft delete)"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE programs 
                SET is_active = 0, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (program_id,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error desactivando programa: {e}")
            conn.rollback()
            return False
    
    def search_programs(self, search_term: str) -> List[ProgramEntity]:
        """Busca programas por nombre o descripción"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            search_pattern = f"%{search_term}%"
            cursor.execute('''
                SELECT * FROM programs 
                WHERE is_active = 1 
                AND (name LIKE ? OR description LIKE ?)
                ORDER BY created_at DESC
            ''', (search_pattern, search_pattern))
            
            rows = cursor.fetchall()
            return [ProgramEntity.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"Error buscando programas: {e}")
            return []
    
    def validate_program_name_unique(self, name: str, exclude_id: int = None) -> bool:
        """Valida que el nombre del programa sea único"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            if exclude_id:
                cursor.execute('''
                    SELECT COUNT(*) FROM programs 
                    WHERE name = ? AND is_active = 1 AND id != ?
                ''', (name, exclude_id))
            else:
                cursor.execute('''
                    SELECT COUNT(*) FROM programs 
                    WHERE name = ? AND is_active = 1
                ''', (name,))
            
            count = cursor.fetchone()[0]
            return count == 0
            
        except Exception as e:
            print(f"Error validando nombre único: {e}")
            return False