"""
Cargador de configuración del sistema
Maneja archivos YAML de configuración
"""

import os
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    """Cargador de configuración del sistema"""
    
    def __init__(self):
        # Obtener ruta del proyecto desde este archivo
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
        self.settings_file = self.config_dir / "settings.yaml"
        self.defaults_file = self.config_dir / "defaults.yaml"
        
        print(f"ConfigLoader inicializado. Directorio config: {self.config_dir}")
    
    def load_config(self) -> Dict[str, Any]:
        """Carga la configuración principal del sistema"""
        try:
            # Intentar importar yaml
            try:
                import yaml
            except ImportError:
                print("Warning: PyYAML no disponible, usando configuración mínima")
                return self._get_minimal_config()
            
            # Cargar valores por defecto primero
            defaults = self._load_defaults()
            
            # Cargar configuración principal si existe
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                
                # Combinar defaults con configuración del usuario
                config = {**defaults, **user_config}
            else:
                config = defaults
            
            print(f"Configuración cargada exitosamente")
            return config
            
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return self._get_minimal_config()
    
    def _load_defaults(self) -> Dict[str, Any]:
        """Carga los valores por defecto"""
        try:
            import yaml
            if self.defaults_file.exists():
                with open(self.defaults_file, 'r', encoding='utf-8') as f:
                    defaults = yaml.safe_load(f) or {}
                    print(f"Defaults cargados desde archivo")
                    return defaults
            else:
                print(f"Archivo defaults no encontrado: {self.defaults_file}")
                return self._get_minimal_config()
        except Exception as e:
            print(f"Error cargando defaults: {e}")
            return self._get_minimal_config()
    
    def _get_minimal_config(self) -> Dict[str, Any]:
        """Configuración mínima de respaldo"""
        print("Usando configuración mínima de respaldo")
        return {
            'language': 'es',
            'pressure_unit': 'PSI',
            'time_unit': 'minutes',
            'theme': 'default',
            'screen_width': 800,
            'screen_height': 480,
            'default_program': {
                'min_pressure': 10.0,
                'max_pressure': 80.0,
                'time_to_min_pressure': 5,
                'program_duration': 30
            }
        }
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Guarda la configuración actual"""
        try:
            import yaml
            # Crear directorio si no existe
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            print("Configuración guardada exitosamente")
            return True
            
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False