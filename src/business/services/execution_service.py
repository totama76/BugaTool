"""
Servicio de ejecución de programas
Gestiona la ejecución en tiempo real de programas de control
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Optional, Callable, Dict, Any, List
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl

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
    alarmTriggered = pyqtSignal(str, str)  # alarm_type ('red'/'green'), message
    phaseChanged = pyqtSignal(str)  # phase ('setup', 'running', 'completed')
    
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
        
        # Control de fases
        self.execution_phase = "setup"  # 'setup', 'running', 'completed'
        self.min_pressure_reached = False
        self.program_start_time: Optional[datetime] = None  # Cuando empieza realmente el programa
        self.program_elapsed_seconds = 0  # Tiempo real del programa (sin setup)
        
        # Configurar sonidos de alarma
        self._setup_alarms()
        
        print("ExecutionService inicializado")
    
    def _setup_alarms(self):
        """Configura los sonidos de alarma"""
        try:
            self.alarm_sound = QSoundEffect()
            # Usar sonido del sistema si existe, sino generar tono
            self.alarm_sound.setSource(QUrl.fromLocalFile(""))  # Se configurará dinámicamente
            self.alarm_sound.setVolume(0.7)
            print("Sistema de alarmas configurado")
        except Exception as e:
            print(f"Warning: No se pudo configurar el sistema de sonido: {e}")
            self.alarm_sound = None
    
    def _play_alarm(self, alarm_type: str):
        """Reproduce alarma según el tipo"""
        try:
            if self.alarm_sound:
                # Configurar frecuencia según tipo de alarma
                if alarm_type == "red":
                    # Sonido de alarma (agudo, repetitivo)
                    self.alarm_sound.setLoopCount(3)
                elif alarm_type == "green":
                    # Sonido de finalización (grave, una vez)
                    self.alarm_sound.setLoopCount(1)
                
                self.alarm_sound.play()
            else:
                # Fallback: beep del sistema
                print(f"\a")  # Beep del sistema
        except Exception as e:
            print(f"Error reproduciendo alarma: {e}")
            print(f"\a")  # Fallback beep

    def clean_phantom_executions(self) -> int:
        """Limpia ejecuciones fantasma (con más de 24 horas sin actualizar)"""
        try:
            conn = self.execution_repository.db.get_connection()
            cursor = conn.cursor()
            
            # Buscar ejecuciones 'running' con más de 24 horas de antigüedad
            cursor.execute('''
                SELECT id, program_id, start_time FROM program_executions 
                WHERE status = 'running' 
                AND end_time IS NULL 
                AND datetime(start_time, '+24 hours') < datetime('now')
            ''')
            
            phantom_executions = cursor.fetchall()
            cleaned_count = 0
            
            for row in phantom_executions:
                execution_id = row['id']
                program_id = row['program_id']
                start_time = row['start_time']
                
                print(f"Limpiando ejecución fantasma ID: {execution_id}, Programa ID: {program_id}, Inicio: {start_time}")
                
                # Marcar como detenida manualmente
                cursor.execute('''
                    UPDATE program_executions 
                    SET status = 'stopped', 
                        end_time = datetime('now'),
                        stopped_manually = 1,
                        notes = 'Limpieza automática - ejecución fantasma'
                    WHERE id = ?
                ''', (execution_id,))
                
                cleaned_count += 1
            
            conn.commit()
            
            if cleaned_count > 0:
                print(f"Se limpiaron {cleaned_count} ejecuciones fantasma")
            
            return cleaned_count
            
        except Exception as e:
            print(f"Error limpiando ejecuciones fantasma: {e}")
            return 0

    def check_for_incomplete_execution(self) -> Optional[Dict[str, Any]]:
        """Verifica si hay una ejecución incompleta al iniciar la aplicación"""
        try:
            # Primero, limpiar ejecuciones fantasma
            cleaned = self.clean_phantom_executions()
            if cleaned > 0:
                print(f"Limpiadas {cleaned} ejecuciones fantasma antes de verificar")
            
            # Buscar ejecuciones en estado 'running' sin end_time (últimas 4 horas)
            conn = self.execution_repository.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM program_executions 
                WHERE status = 'running' 
                AND end_time IS NULL 
                AND datetime(start_time, '+4 hours') > datetime('now')
                ORDER BY start_time DESC 
                LIMIT 1
            ''')
            
            row = cursor.fetchone()
            
            if row:
                execution = ExecutionEntity.from_db_row(row)
                program = self.program_repository.get_program_by_id(execution.program_id)
                
                if program:
                    # Verificar si la ejecución es reciente (menos de 4 horas)
                    time_diff = datetime.now() - execution.start_time
                    
                    if time_diff.total_seconds() < 4 * 3600:  # 4 horas
                        print(f"Ejecución válida encontrada: ID {execution.id}, Programa: {program.name}")
                        print(f"Tiempo transcurrido: {time_diff}")
                        
                        return {
                            'execution': execution,
                            'program': program,
                            'should_resume': True
                        }
                    else:
                        # Ejecución muy antigua, marcar como detenida
                        print(f"Ejecución muy antigua encontrada (>{time_diff}), marcando como detenida")
                        execution.status = 'stopped'
                        execution.stopped_manually = True
                        execution.end_time = datetime.now()
                        execution.notes = 'Detenida automáticamente por tiempo excedido'
                        self.execution_repository.update_execution(execution)
                else:
                    # Programa no existe, limpiar ejecución
                    print(f"Programa no encontrado para ejecución {execution.id}, limpiando...")
                    execution.status = 'stopped'
                    execution.stopped_manually = True
                    execution.end_time = datetime.now()
                    execution.notes = 'Programa asociado no encontrado'
                    self.execution_repository.update_execution(execution)
            
            return None
            
        except Exception as e:
            print(f"Error verificando ejecuciones incompletas: {e}")
            return None

    def validate_execution_state(self) -> bool:
        """Valida que el estado interno coincida con la base de datos"""
        try:
            if not self.is_running or not self.current_execution:
                return True
            
            # Verificar en base de datos
            db_execution = self.execution_repository.get_execution_by_id(self.current_execution.id)
            
            if not db_execution:
                print("Ejecución no encontrada en BD, limpiando estado interno")
                self._reset_execution_state()
                return False
            
            if db_execution.status != 'running':
                print(f"Ejecución en BD no está en running (estado: {db_execution.status}), limpiando estado interno")
                self._reset_execution_state()
                return False
            
            # Verificar que el programa aún existe
            if not self.program_repository.get_program_by_id(db_execution.program_id):
                print("Programa asociado no existe, deteniendo ejecución")
                self.stop_program_execution(manual_stop=True)
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validando estado de ejecución: {e}")
            self._reset_execution_state()
            return False

    def start_program_execution(self, program_id: int) -> Dict[str, Any]:
        """Inicia la ejecución de un programa"""
        try:
            # Validar estado antes de empezar
            self.validate_execution_state()
            
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
            self.program_elapsed_seconds = 0
            
            # Configurar control de presión
            self.current_pressure = 0.0
            self.target_pressure = program.min_pressure
            self.min_pressure_reached = False
            self.program_start_time = None
            
            # Calcular incremento de presión para alcanzar presión mínima en el tiempo especificado
            if program.time_to_min_pressure > 0:
                self.pressure_increment = program.min_pressure / (program.time_to_min_pressure * 60)  # PSI por segundo
            else:
                self.pressure_increment = 1.0
            
            # Configurar fase inicial
            self.execution_phase = "setup"
            self.phaseChanged.emit("setup")
            
            # Iniciar timer de ejecución
            self.execution_timer.start()
            
            # Emitir señales
            self.executionStarted.emit(created_execution.id)
            self.statusUpdated.emit(f"Iniciando programa: {program.name} - Subiendo a presión mínima...")
            
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
            
            if not manual_stop:
                # Programa completado - alarma verde
                self._play_alarm("green")
                self.alarmTriggered.emit("green", f"Programa {program_name} completado exitosamente")
                self.phaseChanged.emit("completed")
            
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
            # Validar estado cada 30 segundos
            if self.elapsed_seconds % 30 == 0:
                if not self.validate_execution_state():
                    return
            
            if not self.is_running or not self.current_program or not self.current_execution:
                return
            
            self.elapsed_seconds += 1
            
            if self.execution_phase == "setup":
                # FASE SETUP: Subir a presión mínima
                self._handle_setup_phase()
            elif self.execution_phase == "running":
                # FASE RUNNING: Programa en ejecución
                self._handle_running_phase()
            
            # Registrar lectura de presión
            self.execution_repository.record_pressure_reading(
                self.current_execution.id, 
                self.current_pressure
            )
            
            # Emitir señal de presión actualizada
            self.pressureUpdated.emit(self.current_pressure)
            
        except Exception as e:
            print(f"Error en paso de ejecución: {e}")
            self.stop_program_execution(manual_stop=True)
    
    def _handle_setup_phase(self):
        """Maneja la fase de setup (subida a presión mínima)"""
        time_to_min_seconds = self.current_program.time_to_min_pressure * 60
        
        # Subir presión gradualmente
        self.current_pressure += self.pressure_increment
        self.current_pressure = min(self.current_pressure, self.current_program.min_pressure)
        
        # Verificar si se alcanzó la presión mínima
        if self.current_pressure >= self.current_program.min_pressure:
            if not self.min_pressure_reached:
                # Primera vez que se alcanza la presión mínima
                self.min_pressure_reached = True
                self.current_execution.min_pressure_reached = True
                self.program_start_time = datetime.now()
                self.execution_phase = "running"
                self.phaseChanged.emit("running")
                self.statusUpdated.emit(f"Presión mínima alcanzada - Iniciando programa...")
                print(f"Presión mínima alcanzada en {self.elapsed_seconds} segundos")
                return
        
        # Verificar timeout para alcanzar presión mínima
        if self.elapsed_seconds >= time_to_min_seconds:
            # ALARMA: No se alcanzó presión mínima a tiempo
            self._play_alarm("red")
            alarm_msg = f"ALARMA: No se alcanzó presión mínima ({self.current_program.min_pressure} PSI) en {self.current_program.time_to_min_pressure} min"
            self.alarmTriggered.emit("red", alarm_msg)
            self.statusUpdated.emit(alarm_msg)
            print(alarm_msg)
        
        # Actualizar progreso en fase setup
        progress_percentage = min(100, int((self.current_pressure / self.current_program.min_pressure) * 100))
        remaining_setup = max(0, time_to_min_seconds - self.elapsed_seconds)
        
        self.progressUpdated.emit(self.elapsed_seconds, remaining_setup, progress_percentage)
        
        setup_msg = f"Subiendo presión: {self.current_pressure:.1f}/{self.current_program.min_pressure} PSI"
        setup_msg += f" | Tiempo: {self.elapsed_seconds//60:02d}:{self.elapsed_seconds%60:02d}"
        setup_msg += f" | Restante: {remaining_setup//60:02d}:{remaining_setup%60:02d}"
        self.statusUpdated.emit(setup_msg)
    
    def _handle_running_phase(self):
        """Maneja la fase de running (programa en ejecución)"""
        if not self.program_start_time:
            return
        
        # Calcular tiempo real del programa
        self.program_elapsed_seconds = int((datetime.now() - self.program_start_time).total_seconds())
        total_duration_seconds = self.current_program.program_duration * 60
        remaining_seconds = max(0, total_duration_seconds - self.program_elapsed_seconds)
        
        # Calcular progreso del programa
        progress_percentage = min(100, int((self.program_elapsed_seconds / total_duration_seconds) * 100))
        
        # Control de presión: mantener entre mín y máx con variaciones
        import random
        variation = random.uniform(-0.8, 1.2)  # Variación controlada
        self.current_pressure += variation
        
        # Verificar límites de presión
        pressure_ok = True
        
        if self.current_pressure < self.current_program.min_pressure:
            # ALARMA: Presión por debajo del mínimo
            self._play_alarm("red")
            alarm_msg = f"ALARMA: Presión por debajo del mínimo ({self.current_pressure:.1f} < {self.current_program.min_pressure} PSI)"
            self.alarmTriggered.emit("red", alarm_msg)
            pressure_ok = False
            
        elif self.current_pressure > self.current_program.max_pressure:
            # ALARMA: Presión por encima del máximo
            self._play_alarm("red")
            alarm_msg = f"ALARMA: Presión por encima del máximo ({self.current_pressure:.1f} > {self.current_program.max_pressure} PSI)"
            self.alarmTriggered.emit("red", alarm_msg)
            self.current_execution.max_pressure_exceeded = True
            pressure_ok = False
        
        # Mantener presión en rango válido para simulación
        self.current_pressure = max(self.current_program.min_pressure * 0.9, 
                                  min(self.current_program.max_pressure * 1.1, self.current_pressure))
        
        # Emitir progreso del programa
        self.progressUpdated.emit(self.program_elapsed_seconds, remaining_seconds, progress_percentage)
        
        # Actualizar mensaje de estado
        minutes_elapsed = self.program_elapsed_seconds // 60
        seconds_elapsed = self.program_elapsed_seconds % 60
        minutes_remaining = remaining_seconds // 60
        seconds_remaining = remaining_seconds % 60
        
        status_msg = f"EJECUTANDO: {minutes_elapsed:02d}:{seconds_elapsed:02d} / "
        status_msg += f"Restante: {minutes_remaining:02d}:{seconds_remaining:02d} / "
        status_msg += f"Presión: {self.current_pressure:.1f} PSI"
        
        if not pressure_ok:
            status_msg += " ⚠️ ALARMA"
        
        self.statusUpdated.emit(status_msg)
        
        # Verificar fin de programa
        if self.program_elapsed_seconds >= total_duration_seconds:
            self.stop_program_execution(manual_stop=False)
    
    def _reset_execution_state(self):
        """Reinicia el estado de ejecución"""
        self.current_execution = None
        self.current_program = None
        self.is_running = False
        self.start_time = None
        self.elapsed_seconds = 0
        self.program_elapsed_seconds = 0
        self.current_pressure = 0.0
        self.target_pressure = 0.0
        self.pressure_increment = 0.0
        self.execution_phase = "setup"
        self.min_pressure_reached = False
        self.program_start_time = None
    
    def get_current_execution_info(self) -> Dict[str, Any]:
        """Obtiene información de la ejecución actual"""
        if not self.is_running or not self.current_execution or not self.current_program:
            return {
                'is_running': False,
                'execution_id': None,
                'program_name': None,
                'elapsed_seconds': 0,
                'current_pressure': 0.0,
                'phase': 'setup'
            }
        
        return {
            'is_running': True,
            'execution_id': self.current_execution.id,
            'program_name': self.current_program.name,
            'elapsed_seconds': self.program_elapsed_seconds if self.execution_phase == "running" else self.elapsed_seconds,
            'current_pressure': self.current_pressure,
            'program_duration': self.current_program.program_duration * 60,
            'min_pressure': self.current_program.min_pressure,
            'max_pressure': self.current_program.max_pressure,
            'phase': self.execution_phase,
            'min_pressure_reached': self.min_pressure_reached
        }
    
    def get_execution_history(self, limit: int = 10) -> List[ExecutionEntity]:
        """Obtiene el historial de ejecuciones"""
        return self.execution_repository.get_recent_executions(limit)
    
    def resume_execution(self, execution: ExecutionEntity, program: ProgramEntity) -> bool:
        """Resume una ejecución interrumpida"""
        try:
            self.current_execution = execution
            self.current_program = program
            self.is_running = True
            self.start_time = execution.start_time
            
            # Calcular tiempo transcurrido
            elapsed_time = datetime.now() - execution.start_time
            self.elapsed_seconds = int(elapsed_time.total_seconds())
            
            # Configurar estado según el progreso
            if execution.min_pressure_reached:
                self.execution_phase = "running"
                self.min_pressure_reached = True
                self.program_start_time = execution.start_time  # Aproximación
                self.program_elapsed_seconds = max(0, self.elapsed_seconds - (program.time_to_min_pressure * 60))
            else:
                self.execution_phase = "setup"
                self.min_pressure_reached = False
                self.program_start_time = None
                self.program_elapsed_seconds = 0
            
            # Configurar presión (valor aproximado)
            if self.min_pressure_reached:
                self.current_pressure = program.min_pressure + (program.max_pressure - program.min_pressure) * 0.6
            else:
                progress = min(1.0, self.elapsed_seconds / (program.time_to_min_pressure * 60))
                self.current_pressure = program.min_pressure * progress
            
            # Reiniciar timer
            self.execution_timer.start()
            
            # Emitir señales
            self.executionStarted.emit(execution.id)
            self.phaseChanged.emit(self.execution_phase)
            self.statusUpdated.emit(f"Resumiendo ejecución del programa: {program.name}")
            
            print(f"Ejecución resumida - Programa: {program.name}, Fase: {self.execution_phase}")
            
            return True
            
        except Exception as e:
            print(f"Error resumiendo ejecución: {e}")
            return False