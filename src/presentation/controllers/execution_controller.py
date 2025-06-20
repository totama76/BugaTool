"""
Controlador de ejecución de programas
Gestiona la comunicación entre la UI y el servicio de ejecución
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from business.services.execution_service import ExecutionService
from business.services.auth_service import AuthService

class ExecutionController(QObject):
    """Controlador de ejecución de programas para la interfaz"""
    
    # Señales
    executionStarted = pyqtSignal(int)  # execution_id
    executionFinished = pyqtSignal(int, str)  # execution_id, status
    progressUpdated = pyqtSignal(int, int, int)  # elapsed, remaining, percentage
    statusChanged = pyqtSignal(str)  # status message
    operationResult = pyqtSignal(bool, str)  # success, message
    executionStateChanged = pyqtSignal()  # Para actualizar propiedades
    cleanupCompleted = pyqtSignal(int)  # cantidad de ejecuciones limpiadas
    executionResumed = pyqtSignal('QVariant')  # program data when execution is resumed
    
    def __init__(self, auth_service: AuthService, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.execution_service = ExecutionService(auth_service)
        
        # Conectar señales del servicio
        self.execution_service.executionStarted.connect(self.executionStarted.emit)
        self.execution_service.executionFinished.connect(self._on_execution_finished)
        self.execution_service.pressureUpdated.connect(self._on_pressure_updated)
        self.execution_service.progressUpdated.connect(self.progressUpdated.emit)
        self.execution_service.statusUpdated.connect(self.statusChanged.emit)
        
        print("ExecutionController inicializado")
    
    @pyqtSlot(int)
    def start_execution(self, program_id: int):
        """Inicia la ejecución de un programa"""
        try:
            result = self.execution_service.start_program_execution(program_id)
            
            if result['success']:
                self.executionStateChanged.emit()
                self.operationResult.emit(True, result['message'])
            else:
                self.operationResult.emit(False, result['message'])
                
        except Exception as e:
            print(f"Error en start_execution: {e}")
            self.operationResult.emit(False, "Error interno del sistema")
    
    @pyqtSlot()
    def stop_execution(self):
        """Detiene la ejecución actual"""
        try:
            result = self.execution_service.stop_program_execution(manual_stop=True)
            
            if result['success']:
                self.executionStateChanged.emit()
                self.operationResult.emit(True, result['message'])
            else:
                self.operationResult.emit(False, result['message'])
                
        except Exception as e:
            print(f"Error en stop_execution: {e}")
            self.operationResult.emit(False, "Error interno del sistema")
    
    @pyqtSlot()
    def clean_phantom_executions(self):
        """Limpia ejecuciones fantasma manualmente"""
        try:
            cleaned_count = self.execution_service.clean_phantom_executions()
            
            self.cleanupCompleted.emit(cleaned_count)
            
            if cleaned_count > 0:
                self.operationResult.emit(True, f"Se limpiaron {cleaned_count} ejecuciones fantasma")
            else:
                self.operationResult.emit(True, "No se encontraron ejecuciones fantasma para limpiar")
                
        except Exception as e:
            print(f"Error en clean_phantom_executions: {e}")
            self.operationResult.emit(False, "Error interno del sistema")
    
    @pyqtSlot()
    def validate_execution_state(self):
        """Valida el estado actual de ejecución"""
        try:
            is_valid = self.execution_service.validate_execution_state()
            
            if not is_valid:
                self.executionStateChanged.emit()
                self.operationResult.emit(True, "Estado de ejecución validado y corregido")
            else:
                self.operationResult.emit(True, "Estado de ejecución válido")
                
        except Exception as e:
            print(f"Error en validate_execution_state: {e}")
            self.operationResult.emit(False, "Error interno del sistema")
    
    @pyqtSlot(result='QVariant')
    def get_current_execution_info(self):
        """Obtiene información de la ejecución actual - MÉTODO SLOT PARA QML"""
        try:
            if not self.execution_service:
                print("execution_service no disponible")
                return None
            
            info = self.execution_service.get_current_execution_info()
            print(f"Información de ejecución obtenida: {info}")
            return info
            
        except Exception as e:
            print(f"Error obteniendo información de ejecución: {e}")
            return None
    
    def _on_execution_finished(self, execution_id: int, status: str):
        """Maneja el fin de una ejecución"""
        self.executionStateChanged.emit()
        self.executionFinished.emit(execution_id, status)
    
    def _on_pressure_updated(self, pressure: float):
        """Maneja actualización de presión"""
        # Esta señal se reenvía al MainController para actualizar el gauge
        pass
    
    def get_is_running(self) -> bool:
        """Verifica si hay una ejecución en curso"""
        info = self.execution_service.get_current_execution_info()
        return info['is_running']
    
    def get_current_program_name(self) -> str:
        """Obtiene el nombre del programa en ejecución"""
        info = self.execution_service.get_current_execution_info()
        return info.get('program_name', '')
    
    def get_current_pressure(self) -> float:
        """Obtiene la presión actual"""
        info = self.execution_service.get_current_execution_info()
        return info.get('current_pressure', 0.0)
    
    def get_execution_service(self):
        """Obtiene el servicio de ejecución para integración con MainController"""
        return self.execution_service
    
    # Propiedades para QML
    isRunning = pyqtProperty(bool, get_is_running, notify=executionStateChanged)
    currentProgramName = pyqtProperty(str, get_current_program_name, notify=executionStateChanged)
    currentPressure = pyqtProperty(float, get_current_pressure, notify=executionStateChanged)