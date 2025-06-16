"""
Controlador principal de la aplicación
Gestiona la simulación de datos y la integración con otros controladores
"""

import random
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot, pyqtProperty

class MainController(QObject):
    """Controlador principal para la simulación y control"""
    
    pressureChanged = pyqtSignal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Timer para simulación
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self._update_simulation)
        self.simulation_timer.setInterval(1000)  # 1 segundo
        
        # Estado de simulación
        self.is_simulation_running = False
        self._current_pressure = 0.0
        
        # Referencia al servicio de ejecución (se asignará desde main_app)
        self.execution_service = None
        
        print("MainController inicializado")
    
    def set_execution_service(self, execution_service):
        """Establece la referencia al servicio de ejecución"""
        self.execution_service = execution_service
        
        # Conectar señal de presión del servicio de ejecución
        if self.execution_service:
            self.execution_service.pressureUpdated.connect(self._on_execution_pressure_updated)
            print("ExecutionService conectado al MainController")
    
    @pyqtSlot()
    def startSimulation(self):
        """Inicia la simulación de presión"""
        if self.execution_service and self.execution_service.is_running:
            print("No se puede iniciar simulación: hay un programa ejecutándose")
            return
            
        print("Iniciando simulación de presión")
        self.is_simulation_running = True
        self.simulation_timer.start()
    
    @pyqtSlot()
    def stopSimulation(self):
        """Detiene la simulación de presión"""
        print("Deteniendo simulación de presión")
        self.is_simulation_running = False
        self.simulation_timer.stop()
        self._current_pressure = 0.0
        self.pressureChanged.emit(self._current_pressure)
    
    def _update_simulation(self):
        """Actualiza los valores de simulación"""
        if not self.is_simulation_running:
            return
            
        # Verificar si hay una ejecución real en curso
        if self.execution_service and self.execution_service.is_running:
            # Si hay ejecución real, detener simulación
            self.stopSimulation()
            return
        
        # Generar variación de presión simulada
        variation = random.uniform(-2.0, 3.0)
        self._current_pressure += variation
        
        # Limitar valores
        self._current_pressure = max(0.0, min(100.0, self._current_pressure))
        
        # Emitir señal de cambio
        self.pressureChanged.emit(self._current_pressure)
    
    def _on_execution_pressure_updated(self, pressure: float):
        """Maneja actualización de presión desde ejecución real"""
        self._current_pressure = pressure
        self.pressureChanged.emit(self._current_pressure)
    
    def get_current_pressure(self) -> float:
        """Obtiene la presión actual"""
        return self._current_pressure
    
    # Propiedades para QML
    currentPressure = pyqtProperty(float, get_current_pressure, notify=pressureChanged)