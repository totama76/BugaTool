"""
Servicio de gestión de programas
Implementa las reglas de negocio para programas
"""

from typing import Optional, List, Dict, Any
from data.repositories.program_repository import ProgramRepository
from data.entities.program_entity import ProgramEntity
from .auth_service import AuthService

class ProgramService:
    """Servicio de gestión de programas con validaciones de negocio"""
    
    def __init__(self, auth_service: AuthService):
        self.program_repository = ProgramRepository()
        self.auth_service = auth_service
    
    def create_program(self, program_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo programa con validaciones"""
        try:
            # Verificar permisos
            if not self.auth_service.can_manage_programs():
                return {
                    'success': False,
                    'message': 'No tiene permisos para crear programas',
                    'program': None
                }
            
            # Validar datos
            validation_result = self._validate_program_data(program_data)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'message': validation_result['message'],
                    'program': None
                }
            
            # Verificar nombre único
            if not self.program_repository.validate_program_name_unique(program_data['name']):
                return {
                    'success': False,
                    'message': f"Ya existe un programa con el nombre '{program_data['name']}'",
                    'program': None
                }
            
            # Crear entidad
            current_user = self.auth_service.get_current_user()
            program = ProgramEntity(
                name=program_data['name'],
                description=program_data.get('description', ''),
                min_pressure=float(program_data['min_pressure']),
                max_pressure=float(program_data['max_pressure']),
                time_to_min_pressure=int(program_data['time_to_min_pressure']),
                program_duration=int(program_data['program_duration']),
                created_by=current_user.id if current_user else None,
                is_active=True
            )
            
            # Guardar en base de datos
            created_program = self.program_repository.create_program(program)
            
            if created_program:
                return {
                    'success': True,
                    'message': f"Programa '{created_program.name}' creado exitosamente",
                    'program': created_program
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al guardar el programa en la base de datos',
                    'program': None
                }
                
        except Exception as e:
            print(f"Error en create_program: {e}")
            return {
                'success': False,
                'message': 'Error interno del sistema',
                'program': None
            }
    
    def update_program(self, program_id: int, program_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un programa existente"""
        try:
            # Verificar permisos
            if not self.auth_service.can_manage_programs():
                return {
                    'success': False,
                    'message': 'No tiene permisos para modificar programas',
                    'program': None
                }
            
            # Verificar que el programa existe
            existing_program = self.program_repository.get_program_by_id(program_id)
            if not existing_program:
                return {
                    'success': False,
                    'message': 'Programa no encontrado',
                    'program': None
                }
            
            # Validar datos
            validation_result = self._validate_program_data(program_data)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'message': validation_result['message'],
                    'program': None
                }
            
            # Verificar nombre único (excluyendo el programa actual)
            if not self.program_repository.validate_program_name_unique(
                program_data['name'], program_id
            ):
                return {
                    'success': False,
                    'message': f"Ya existe otro programa con el nombre '{program_data['name']}'",
                    'program': None
                }
            
            # Actualizar entidad
            existing_program.name = program_data['name']
            existing_program.description = program_data.get('description', '')
            existing_program.min_pressure = float(program_data['min_pressure'])
            existing_program.max_pressure = float(program_data['max_pressure'])
            existing_program.time_to_min_pressure = int(program_data['time_to_min_pressure'])
            existing_program.program_duration = int(program_data['program_duration'])
            
            # Guardar cambios
            success = self.program_repository.update_program(existing_program)
            
            if success:
                updated_program = self.program_repository.get_program_by_id(program_id)
                return {
                    'success': True,
                    'message': f"Programa '{updated_program.name}' actualizado exitosamente",
                    'program': updated_program
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al actualizar el programa',
                    'program': None
                }
                
        except Exception as e:
            print(f"Error en update_program: {e}")
            return {
                'success': False,
                'message': 'Error interno del sistema',
                'program': None
            }
    
    def delete_program(self, program_id: int) -> Dict[str, Any]:
        """Elimina (desactiva) un programa"""
        try:
            # Verificar permisos
            if not self.auth_service.can_manage_programs():
                return {
                    'success': False,
                    'message': 'No tiene permisos para eliminar programas'
                }
            
            # Verificar que el programa existe
            existing_program = self.program_repository.get_program_by_id(program_id)
            if not existing_program:
                return {
                    'success': False,
                    'message': 'Programa no encontrado'
                }
            
            # Eliminar
            success = self.program_repository.delete_program(program_id)
            
            if success:
                return {
                    'success': True,
                    'message': f"Programa '{existing_program.name}' eliminado exitosamente"
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al eliminar el programa'
                }
                
        except Exception as e:
            print(f"Error en delete_program: {e}")
            return {
                'success': False,
                'message': 'Error interno del sistema'
            }
    
    def get_all_programs(self) -> List[ProgramEntity]:
        """Obtiene todos los programas disponibles"""
        try:
            if self.auth_service.is_authenticated():
                return self.program_repository.get_all_programs()
            return []
            
        except Exception as e:
            print(f"Error obteniendo programas: {e}")
            return []
    
    def get_program_by_id(self, program_id: int) -> Optional[ProgramEntity]:
        """Obtiene un programa por ID"""
        try:
            if self.auth_service.is_authenticated():
                return self.program_repository.get_program_by_id(program_id)
            return None
            
        except Exception as e:
            print(f"Error obteniendo programa: {e}")
            return None
    
    def search_programs(self, search_term: str) -> List[ProgramEntity]:
        """Busca programas por término"""
        try:
            if self.auth_service.is_authenticated():
                return self.program_repository.search_programs(search_term)
            return []
            
        except Exception as e:
            print(f"Error buscando programas: {e}")
            return []
    
    def _validate_program_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida los datos del programa"""
        try:
            # Validar campos requeridos
            required_fields = ['name', 'min_pressure', 'max_pressure', 
                             'time_to_min_pressure', 'program_duration']
            
            for field in required_fields:
                if field not in data or data[field] is None or str(data[field]).strip() == '':
                    return {
                        'valid': False,
                        'message': f'El campo {field} es requerido'
                    }
            
            # Validar nombre
            name = str(data['name']).strip()
            if len(name) < 3:
                return {
                    'valid': False,
                    'message': 'El nombre debe tener al menos 3 caracteres'
                }
            if len(name) > 100:
                return {
                    'valid': False,
                    'message': 'El nombre no puede exceder 100 caracteres'
                }
            
            # Validar presiones
            try:
                min_pressure = float(data['min_pressure'])
                max_pressure = float(data['max_pressure'])
            except (ValueError, TypeError):
                return {
                    'valid': False,
                    'message': 'Las presiones deben ser números válidos'
                }
            
            if min_pressure < 0:
                return {
                    'valid': False,
                    'message': 'La presión mínima no puede ser negativa'
                }
            
            if max_pressure <= min_pressure:
                return {
                    'valid': False,
                    'message': 'La presión máxima debe ser mayor que la mínima'
                }
            
            if max_pressure > 200:  # Límite de seguridad
                return {
                    'valid': False,
                    'message': 'La presión máxima no puede exceder 200 PSI'
                }
            
            # Validar tiempos
            try:
                time_to_min = int(data['time_to_min_pressure'])
                duration = int(data['program_duration'])
            except (ValueError, TypeError):
                return {
                    'valid': False,
                    'message': 'Los tiempos deben ser números enteros válidos'
                }
            
            if time_to_min < 1:
                return {
                    'valid': False,
                    'message': 'El tiempo para alcanzar presión mínima debe ser al menos 1 minuto'
                }
            
            if duration < time_to_min:
                return {
                    'valid': False,
                    'message': 'La duración total debe ser mayor que el tiempo para alcanzar presión mínima'
                }
            
            if duration > 1440:  # 24 horas máximo
                return {
                    'valid': False,
                    'message': 'La duración no puede exceder 24 horas (1440 minutos)'
                }
            
            return {'valid': True, 'message': 'Datos válidos'}
            
        except Exception as e:
            print(f"Error validando datos: {e}")
            return {
                'valid': False,
                'message': 'Error validando los datos del programa'
            }