#!/usr/bin/env python3
"""
Punto de entrada principal del Sistema de Control de Presión
Fecha: 2025-06-16 15:35:16 UTC
Autor: Sistema desarrollado para totama76
"""

import sys
import os
from pathlib import Path

def main():
    """Función principal de la aplicación"""
    try:
        # Configurar el path antes de cualquier importación
        project_root = Path(__file__).parent
        src_path = project_root / "src"
        sys.path.insert(0, str(src_path))
        
        # Verificar PyQt6 de forma correcta
        try:
            from PyQt6.QtCore import PYQT_VERSION_STR
            print(f"PyQt6 encontrado: {PYQT_VERSION_STR}")
        except ImportError as e:
            print(f"Error: PyQt6 no está instalado correctamente. {e}")
            print("Ejecute: pip install PyQt6")
            return 1
        
        # Importar y ejecutar la aplicación
        from presentation.main_app import PressureControlApp
        
        print("Iniciando Sistema de Control de Presión...")
        app = PressureControlApp(sys.argv)
        return app.run()
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())