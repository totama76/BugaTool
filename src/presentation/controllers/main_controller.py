"""
Controlador principal de la aplicación
Gestiona la comunicación entre QML y la lógica de negocio
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, pyqtProperty

# Simulación de datos para desarrollo inicial
import random
import time

class MainController(QObject):
    """Controlador principal para la interfaz QML"""
    
    # Señales para notificar cambios a QML
    currentPressureChanged = pyqtSignal(float)
    systemStatusChanged = pyqtSignal(str)
    alarmStateChanged = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_pressure = 0.0
        self._system_status = "Listo"
        self._alarm_active = False
        self._is_simulation_active = True
        
        # Timer para simulación de lecturas de presión
        self._simulation_timer = QTimer()
        self._simulation_timer.timeout.connect(self._simulate_pressure_reading)
        
        if self._is_simulation_active:
            self._simulation_timer.start(1000)  # Actualizar cada segundo
    
    @pyqtSlot()
    def startSimulation(self):
        """Inicia la simulación de lecturas de presión"""
        if not self._simulation_timer.isActive():
            self._simulation_timer.start(1000)
            self._is_simulation_active = True
            self.set_system_status("Simulación activa")
    
    @pyqtSlot()
    def stopSimulation(self):
        """Detiene la simulación de lecturas de presión"""
        if self._simulation_timer.isActive():
            self._simulation_timer.stop()
            self._is_simulation_active = False
            self.set_system_status("Simulación detenida")
    
    def _simulate_pressure_reading(self):
        """Simula una lectura de sensor de presión"""
        # Simulación básica: variación aleatoria entre 0 y 100
        base_pressure = 50.0
        variation = random.uniform(-10.0, 10.0)
        new_pressure = max(0.0, min(100.0, base_pressure + variation))
        
        self.set_current_pressure(new_pressure)
    
    # Propiedades accesibles desde QML
    def get_current_pressure(self):
        return self._current_pressure
    
    def set_current_pressure(self, value):
        if self._current_pressure != value:
            self._current_pressure = value
            self.currentPressureChanged.emit(value)
    
    def get_system_status(self):
        return self._system_status
    
    def set_system_status(self, status):
        if self._system_status != status:
            self._system_status = status
            self.systemStatusChanged.emit(status)
    
    def get_alarm_state(self):
        return self._alarm_active
    
    def set_alarm_state(self, state):
        if self._alarm_active != state:
            self._alarm_active = state
            self.alarmStateChanged.emit(state)
    
    # Propiedades para QML usando el método tradicional
    currentPressure = pyqtProperty(float, get_current_pressure, notify=currentPressureChanged)
    systemStatus = pyqtProperty(str, get_system_status, notify=systemStatusChanged)
    alarmState = pyqtProperty(bool, get_alarm_state, notify=alarmStateChanged)