"""
Controlador de gestión de programas
Gestiona la comunicación entre la UI y los servicios de programas
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from business.services.program_service import ProgramService
from business.services.auth_service import AuthService

class ProgramController(QObject):
    """Controlador de gestión de programas para la interfaz"""
    
    # Señales
    programsChanged = pyqtSignal()
    operationResult = pyqtSignal(bool, str)  # success, message
    programSelected = pyqtSignal('QVariant')  # program data
    
    def __init__(self, auth_service: AuthService, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.program_service = ProgramService(auth_service)
        self._programs = []
        self._current_program = None
        self._search_term = ""
        
        # Cargar programas iniciales
        self.refresh_programs()
    
    @pyqtSlot(str, str, float, float, int, int)
    def create_program(self, name: str, description: str, min_pressure: float, 
                      max_pressure: float, time_to_min: int, duration: int):
        """Crea un nuevo programa"""
        try:
            program_data = {
                'name': name.strip(),
                'description': description.strip(),
                'min_pressure': min_pressure,
                'max_pressure': max_pressure,
                'time_to_min_pressure': time_to_min,
                'program_duration': duration
            }
            
            result = self.program_service.create_program(program_data)
            
            if result['success']:
                self.refresh_programs()
                self.operationResult.emit(True, result['message'])
            else:
                self.operationResult.emit(False, result['message'])
                
        except Exception as e:
            print(f"Error en create_program: {e}")
            self.operationResult.emit(False, "Error interno del sistema")
    
    @pyqtSlot(int, str, str, float, float, int, int)
    def update_program(self, program_id: int, name: str, description: str, 
                      min_pressure: float, max_pressure: float, time_to_min: int, duration: int):
        """Actualiza un programa existente"""
        try:
            program_data = {
                'name': name.strip(),
                'description': description.strip(),
                'min_pressure': min_pressure,
                'max_pressure': max_pressure,
                'time_to_min_pressure': time_to_min,
                'program_duration': duration
            }
            
            result = self.program_service.update_program(program_id, program_data)
            
            if result['success']:
                self.refresh_programs()
                self.operationResult.emit(True, result['message'])
            else:
                self.operationResult.emit(False, result['message'])
                
        except Exception as e:
            print(f"Error en update_program: {e}")
            self.operationResult.emit(False, "Error interno del sistema")
    
    @pyqtSlot(int)
    def delete_program(self, program_id: int):
        """Elimina un programa"""
        try:
            result = self.program_service.delete_program(program_id)
            
            if result['success']:
                self.refresh_programs()
                self.operationResult.emit(True, result['message'])
            else:
                self.operationResult.emit(False, result['message'])
                
        except Exception as e:
            print(f"Error en delete_program: {e}")
            self.operationResult.emit(False, "Error interno del sistema")
    
    @pyqtSlot(int)
    def select_program(self, program_id: int):
        """Selecciona un programa para edición"""
        try:
            program = self.program_service.get_program_by_id(program_id)
            if program:
                self._current_program = program
                # Convertir a diccionario para QML
                program_dict = program.to_dict()
                self.programSelected.emit(program_dict)
            else:
                self.operationResult.emit(False, "Programa no encontrado")
                
        except Exception as e:
            print(f"Error en select_program: {e}")
            self.operationResult.emit(False, "Error interno del sistema")
    
    @pyqtSlot()
    def refresh_programs(self):
        """Actualiza la lista de programas"""
        try:
            if self._search_term:
                programs = self.program_service.search_programs(self._search_term)
            else:
                programs = self.program_service.get_all_programs()
            
            # Convertir a lista de diccionarios para QML
            self._programs = [program.to_dict() for program in programs]
            self.programsChanged.emit()
            
        except Exception as e:
            print(f"Error en refresh_programs: {e}")
            self._programs = []
            self.programsChanged.emit()
    
    @pyqtSlot(str)
    def search_programs(self, search_term: str):
        """Busca programas por término"""
        self._search_term = search_term.strip()
        self.refresh_programs()
    
    @pyqtSlot()
    def clear_search(self):
        """Limpia la búsqueda"""
        self._search_term = ""
        self.refresh_programs()
    
    def get_programs(self) -> list:
        """Obtiene la lista de programas para QML"""
        return self._programs
    
    def get_can_manage(self) -> bool:
        """Verifica si puede gestionar programas"""
        return self.auth_service.can_manage_programs()
    
    def get_can_execute(self) -> bool:
        """Verifica si puede ejecutar programas"""
        return self.auth_service.can_execute_programs()
    
    # Propiedades para QML
    programs = pyqtProperty('QVariantList', get_programs, notify=programsChanged)
    canManage = pyqtProperty(bool, get_can_manage)
    canExecute = pyqtProperty(bool, get_can_execute)