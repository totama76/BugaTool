"""
Controlador principal de la aplicación
Gestiona la simulación de datos y la integración con otros controladores
"""

import random
import math
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
        
        # Variables para simulación mejorada
        self.simulation_time = 0
        self.target_pressure = 50.0  # Presión objetivo base
        self.pressure_trend = 1  # 1 para subir, -1 para bajar
        self.last_direction_change = 0
        self.noise_amplitude = 2.0  # Amplitud del ruido
        
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
            
        print("Iniciando simulación de presión con variaciones realistas")
        self.is_simulation_running = True
        self.simulation_time = 0
        self._current_pressure = random.uniform(10.0, 25.0)  # Presión inicial aleatoria
        self.target_pressure = random.uniform(40.0, 70.0)  # Objetivo inicial
        self.pressure_trend = 1
        self.last_direction_change = 0
        
        self.simulation_timer.start()
    
    @pyqtSlot()
    def stopSimulation(self):
        """Detiene la simulación de presión"""
        print("Deteniendo simulación de presión")
        self.is_simulation_running = False
        self.simulation_timer.stop()
        self._current_pressure = 0.0
        self.simulation_time = 0
        self.pressureChanged.emit(self._current_pressure)
    
    def _update_simulation(self):
        """Actualiza los valores de simulación con comportamiento realista"""
        if not self.is_simulation_running:
            return
            
        # Verificar si hay una ejecución real en curso
        if self.execution_service and self.execution_service.is_running:
            # Si hay ejecución real, detener simulación
            self.stopSimulation()
            return
        
        self.simulation_time += 1
        
        # Cambiar objetivo periódicamente para crear variaciones interesantes
        if self.simulation_time % 15 == 0:  # Cada 15 segundos
            self.target_pressure = random.uniform(30.0, 80.0)
            print(f"Nueva presión objetivo: {self.target_pressure:.1f} PSI")
        
        # Calcular diferencia hacia el objetivo
        pressure_diff = self.target_pressure - self._current_pressure
        
        # Cambiar tendencia si está muy lejos del objetivo
        if abs(pressure_diff) > 20:
            self.pressure_trend = 1 if pressure_diff > 0 else -1
            self.last_direction_change = self.simulation_time
        
        # Cambio de dirección ocasional para simular fluctuaciones reales
        if self.simulation_time - self.last_direction_change > random.randint(8, 15):
            if random.random() < 0.3:  # 30% probabilidad de cambio
                self.pressure_trend *= -1
                self.last_direction_change = self.simulation_time
                print(f"Cambio de tendencia a {'subida' if self.pressure_trend > 0 else 'bajada'}")
        
        # Calcular variación base hacia el objetivo
        base_change = pressure_diff * 0.1 * self.pressure_trend
        
        # Añadir ruido realista
        noise = random.gauss(0, self.noise_amplitude)
        
        # Añadir oscilación sinusoidal para simular fluctuaciones del sistema
        oscillation = math.sin(self.simulation_time * 0.3) * 1.5
        
        # Variación final
        total_change = base_change + noise + oscillation
        
        # Aplicar cambio con amortiguación
        self._current_pressure += total_change * 0.7
        
        # Limitar valores realistas (0-100 PSI)
        self._current_pressure = max(0.0, min(100.0, self._current_pressure))
        
        # Añadir fluctuaciones menores adicionales
        micro_variation = random.uniform(-0.5, 0.5)
        self._current_pressure += micro_variation
        
        # Asegurar límites finales
        self._current_pressure = max(0.0, min(100.0, self._current_pressure))
        
        # Emitir señal de cambio
        self.pressureChanged.emit(self._current_pressure)
        
        # Log ocasional para debugging
        if self.simulation_time % 10 == 0:
            print(f"Simulación - Tiempo: {self.simulation_time}s, Presión: {self._current_pressure:.1f} PSI, Objetivo: {self.target_pressure:.1f} PSI")
    
    def _on_execution_pressure_updated(self, pressure: float):
        """Maneja actualización de presión desde ejecución real"""
        self._current_pressure = pressure
        self.pressureChanged.emit(self._current_pressure)
    
    def get_current_pressure(self) -> float:
        """Obtiene la presión actual"""
        return self._current_pressure
    
    # Propiedades para QML
    currentPressure = pyqtProperty(float, get_current_pressure, notify=pressureChanged)