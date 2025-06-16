"""
Gestor de internacionalización
Maneja múltiples idiomas del sistema
"""

import os
from pathlib import Path
from typing import Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal

class I18nManager(QObject):
    """Gestor de internacionalización para múltiples idiomas"""
    
    # Señal emitida cuando cambia el idioma
    languageChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Obtener ruta del proyecto desde este archivo
        self.project_root = Path(__file__).parent.parent.parent
        self.i18n_dir = self.project_root / "config" / "i18n"
        self.current_language = 'es'
        self.translations = {}
        self.supported_languages = ['es', 'en', 'fr']
        
        print(f"I18nManager inicializado. Directorio i18n: {self.i18n_dir}")
        
        # Cargar traducciones iniciales
        self._load_translations()
    
    def _load_translations(self):
        """Carga todas las traducciones disponibles"""
        self.translations = {}
        
        try:
            import yaml
            yaml_available = True
        except ImportError:
            print("Warning: PyYAML no disponible, usando traducciones básicas")
            yaml_available = False
        
        for lang in self.supported_languages:
            if yaml_available:
                lang_file = self.i18n_dir / f"{lang}.yaml"
                if lang_file.exists():
                    try:
                        with open(lang_file, 'r', encoding='utf-8') as f:
                            import yaml
                            self.translations[lang] = yaml.safe_load(f) or {}
                        print(f"Traducciones {lang} cargadas desde archivo")
                    except Exception as e:
                        print(f"Error cargando idioma {lang}: {e}")
                        self.translations[lang] = self._get_basic_translations(lang)
                else:
                    print(f"Archivo de idioma no encontrado: {lang_file}")
                    self.translations[lang] = self._get_basic_translations(lang)
            else:
                self.translations[lang] = self._get_basic_translations(lang)
    
    def _get_basic_translations(self, lang: str) -> Dict[str, Any]:
        """Traducciones básicas de respaldo"""
        if lang == 'es':
            return {
                'main': {
                    'pressure_control': 'Control de Presión',
                    'current_pressure': 'Presión Actual',
                    'start_simulation': 'Iniciar Simulación',
                    'stop_simulation': 'Detener Simulación'
                },
                'status': {
                    'ready': 'Listo',
                    'simulation_active': 'Simulación activa',
                    'simulation_stopped': 'Simulación detenida'
                }
            }
        elif lang == 'en':
            return {
                'main': {
                    'pressure_control': 'Pressure Control',
                    'current_pressure': 'Current Pressure',
                    'start_simulation': 'Start Simulation',
                    'stop_simulation': 'Stop Simulation'
                },
                'status': {
                    'ready': 'Ready',
                    'simulation_active': 'Simulation active',
                    'simulation_stopped': 'Simulation stopped'
                }
            }
        else:  # fr
            return {
                'main': {
                    'pressure_control': 'Contrôle de Pression',
                    'current_pressure': 'Pression Actuelle',
                    'start_simulation': 'Démarrer Simulation',
                    'stop_simulation': 'Arrêter Simulation'
                },
                'status': {
                    'ready': 'Prêt',
                    'simulation_active': 'Simulation active',
                    'simulation_stopped': 'Simulation arrêtée'
                }
            }
    
    def set_language(self, language: str):
        """Establece el idioma actual"""
        if language in self.supported_languages:
            if self.current_language != language:
                self.current_language = language
                self.languageChanged.emit(language)
                print(f"Idioma cambiado a: {language}")
        else:
            print(f"Idioma no soportado: {language}")
    
    def get_text(self, key: str, default: str = None) -> str:
        """Obtiene un texto traducido por su clave"""
        try:
            # Obtener traducciones del idioma actual
            current_translations = self.translations.get(self.current_language, {})
            
            # Buscar la clave (soporta claves anidadas con punto)
            keys = key.split('.')
            value = current_translations
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    value = None
                    break
            
            # Si se encontró la traducción, devolverla
            if value is not None and isinstance(value, str):
                return value
            
            # Si no se encontró, intentar con español como fallback
            if self.current_language != 'es':
                es_translations = self.translations.get('es', {})
                value = es_translations
                for k in keys:
                    if isinstance(value, dict) and k in value:
                        value = value[k]
                    else:
                        value = None
                        break
                
                if value is not None and isinstance(value, str):
                    return value
            
            # Si no hay traducción, devolver default o la clave
            return default if default is not None else key
            
        except Exception as e:
            print(f"Error obteniendo traducción para '{key}': {e}")
            return default if default is not None else key
    
    def get_supported_languages(self) -> list:
        """Devuelve la lista de idiomas soportados"""
        return self.supported_languages.copy()
    
    def get_current_language(self) -> str:
        """Devuelve el idioma actual"""
        return self.current_language