"""
Servicio de ejecución de programas
Gestiona la ejecución en tiempo real de programas de control
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Optional, Callable, Dict, Any
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from data.repositories.execution_repository import ExecutionRepository
from data.repositories.program_repository import ProgramRepository
from data.entities.execution_entity import ExecutionEntity
from data.entities.program_entity import ProgramEntity
from .auth_service import AuthService

class ExecutionService(QObject):
    """Servicio de ejecución de programas con control en tiempo real"""
    
    # Señales para comunicación con la interfaz
    executionStarted = pyqtSignal(int)  # execution_id
    executionFinished = pyqtSignal(int, str)  # execution_id, status
    pressureUpdated = pyqtSignal(float)  # current_pressure
    progressUpdated = pyqtSignal(int, int, int)  # elapsed_seconds, remaining_seconds, progress_percentage
    statusUpdated = pyqtSignal(str)  # status_message
    
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.execution_repository = ExecutionRepository()
        self.program_repository = ProgramRepository()
        
        # Estado de ejecución
        self.current_execution: Optional[ExecutionEntity] = None
        self.current_program: Optional[ProgramEntity] = None
        self.is_running = False
        self.start_time: Optional[datetime] = None
        
        # Timer para control de ejecución
        self.execution_timer = QTimer()
        self.execution_timer.timeout.connect(self._execution_step)
        self.execution_timer.setInterval(1000)  # 1 segundo
        
        # Variables de control de presión
        self.current_pressure = 0.0
        self.target_pressure = 0.0
        self.pressure_increment = 0.0
        self.elapsed_seconds = 0
        
        print("ExecutionService inicializado")
    
    def start_program_execution(self, program_id: int) -> Dict[str, Any]:
        """Inicia la ejecución de un programa"""
        try:
            # Verificar permisos
            if not self.auth_service.can_execute_programs():
                return {
                    'success': False,
                    'message': 'No tiene permisos para ejecutar programas'
                }
            
            # Verificar que no haya otra ejecución en curso
            if self.is_running:
                return {
                    'success': False,
                    'message': 'Ya hay un programa en ejecución'
                }
            
            # Obtener el programa
            program = self.program_repository.get_program_by_id(program_id)
            if not program:
                return {
                    'success': False,
                    'message': 'Programa no encontrado'
                }
            
            # Crear registro de ejecución
            current_user = self.auth_service.get_current_user()
            execution = ExecutionEntity(
                program_id=program.id,
                user_id=current_user.id if current_user else 0,
                status='running'
            )
            
            created_execution = self.execution_repository.create_execution(execution)
            if not created_execution:
                return {
                    'success': False,
                    'message': 'Error al crear registro de ejecución'
                }
            
            # Configurar ejecución
            self.current_execution = created_execution
            self.current_program = program
            self.is_running = True
            self.start_time = datetime.now()
            self.elapsed_seconds = 0
            
            # Configurar control de presión
            self.current_pressure = 0.0
            self.target_pressure = program.min_pressure
            
            # Calcular incremento de presión para alcanzar presión mínima en el tiempo especificado
            if program.time_to_min_pressure > 0:
                self.pressure_increment = program.min_pressure / (program.time_to_min_pressure * 60)  # PSI por segundo
            else:
                self.pressure_increment = 1.0
            
            # Iniciar timer de ejecución
            self.execution_timer.start()
            
            # Emitir señales
            self.executionStarted.emit(created_execution.id)
            self.statusUpdated.emit(f"Iniciando programa: {program.name}")
            
            print(f"Ejecución iniciada - Programa: {program.name}, ID: {created_execution.id}")
            
            return {
                'success': True,
                'message': f'Programa "{program.name}" iniciado correctamente',
                'execution_id': created_execution.id
            }
            
        except Exception as e:
            print(f"Error iniciando ejecución: {e}")
            return {
                'success': False,
                'message': 'Error interno del sistema'
            }
    
    def stop_program_execution(self, manual_stop: bool = True) -> Dict[str, Any]:
        """Detiene la ejecución actual"""
        try:
            if not self.is_running or not self.current_execution:
                return {
                    'success': False,
                    'message': 'No hay ninguna ejecución en curso'
                }
            
            # Detener timer
            self.execution_timer.stop()
            
            # Actualizar registro de ejecución
            self.current_execution.end_time = datetime.now()
            self.current_execution.status = 'stopped' if manual_stop else 'completed'
            self.current_execution.stopped_manually = manual_stop
            
            self.execution_repository.update_execution(self.current_execution)
            
            # Estado final
            execution_id = self.current_execution.id
            program_name = self.current_program.name if self.current_program else "Programa"
            
            # Limpiar estado
            self._reset_execution_state()
            
            # Emitir señales
            status = 'stopped' if manual_stop else 'completed'
            self.executionFinished.emit(execution_id, status)
            
            message = f"Programa {program_name} "
            message += "detenido manualmente" if manual_stop else "completado"
            self.statusUpdated.emit(message)
            
            print(f"Ejecución {status} - ID: {execution_id}")
            
            return {
                'success': True,
                'message': message
            }
            
        except Exception as e:
            print(f"Error deteniendo ejecución: {e}")
            return {
                'success': False,
                'message': 'Error interno del sistema'
            }
    
    def _execution_step(self):
        """Paso de ejecución ejecutado cada segundo"""
        try:
            if not self.is_running or not self.current_program or not self.current_execution:
                return
            
            self.elapsed_seconds += 1
            total_duration_seconds = self.current_program.program_duration * 60
            remaining_seconds = total_duration_seconds - self.elapsed_seconds
            
            # Calcular progreso
            progress_percentage = min(100, int((self.elapsed_seconds / total_duration_seconds) * 100))
            
            # Control de presión por fases
            time_to_min_seconds = self.current_program.time_to_min_pressure * 60
            
            if self.elapsed_seconds <= time_to_min_seconds:
                # Fase 1: Subir a presión mínima
                self.current_pressure += self.pressure_increment
                self.current_pressure = min(self.current_pressure, self.current_program.min_pressure)
                self.target_pressure = self.current_program.min_pressure
                
                if self.current_pressure >= self.current_program.min_pressure:
                    self.current_execution.min_pressure_reached = True
                    
            else:
                # Fase 2: Mantener presión mínima con variaciones hacia la máxima
                pressure_range = self.current_program.max_pressure - self.current_program.min_pressure
                
                # Variación controlada de presión
                import random
                variation = random.uniform(-0.5, 1.5)  # Tendencia ascendente
                self.current_pressure += variation
                
                # Limitar presión
                self.current_pressure = max(self.current_program.min_pressure, 
                                          min(self.current_program.max_pressure, self.current_pressure))
                
                if self.current_pressure >= self.current_program.max_pressure:
                    self.current_execution.max_pressure_exceeded = True
            
            # Registrar lectura de presión
            self.execution_repository.record_pressure_reading(
                self.current_execution.id, 
                self.current_pressure
            )
            
            # Emitir señales de actualización
            self.pressureUpdated.emit(self.current_pressure)
            self.progressUpdated.emit(self.elapsed_seconds, remaining_seconds, progress_percentage)
            
            # Actualizar mensaje de estado
            minutes_elapsed = self.elapsed_seconds // 60
            seconds_elapsed = self.elapsed_seconds % 60
            minutes_remaining = remaining_seconds // 60
            seconds_remaining = remaining_seconds % 60
            
            status_msg = f"Ejecutando: {minutes_elapsed:02d}:{seconds_elapsed:02d} / "
            status_msg += f"Restante: {minutes_remaining:02d}:{seconds_remaining:02d} / "
            status_msg += f"Presión: {self.current_pressure:.1f} PSI"
            
            self.statusUpdated.emit(status_msg)
            
            # Verificar fin de programa
            if self.elapsed_seconds >= total_duration_seconds:
                self.stop_program_execution(manual_stop=False)
            
        except Exception as e:
            print(f"Error en paso de ejecución: {e}")
            self.stop_program_execution(manual_stop=True)
    
    def _reset_execution_state(self):
        """Reinicia el estado de ejecución"""
        self.current_execution = None
        self.current_program = None
        self.is_running = False
        self.start_time = None
        self.elapsed_seconds = 0
        self.current_pressure = 0.0
        self.target_pressure = 0.0
        self.pressure_increment = 0.0
    
    def get_current_execution_info(self) -> Dict[str, Any]:
        """Obtiene información de la ejecución actual"""
        if not self.is_running or not self.current_execution or not self.current_program:
            return {
                'is_running': False,
                'execution_id': None,
                'program_name': None,
                'elapsed_seconds': 0,
                'current_pressure': 0.0
            }
        
        return {
            'is_running': True,
            'execution_id': self.current_execution.id,
            'program_name': self.current_program.name,
            'elapsed_seconds': self.elapsed_seconds,
            'current_pressure': self.current_pressure,
            'program_duration': self.current_program.program_duration * 60,
            'min_pressure': self.current_program.min_pressure,
            'max_pressure': self.current_program.max_pressure
        }
    
    def get_execution_history(self, limit: int = 10) -> List[ExecutionEntity]:
        """Obtiene el historial de ejecuciones"""
        return self.execution_repository.get_recent_executions(limit)