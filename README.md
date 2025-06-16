# Sistema de Control de Presión para Raspberry Pi

**Fecha de Estado:** 2025-06-16 15:21:55 UTC  
**Versión:** 0.1.0  
**Desarrollado para:** totama76

## Descripción del Proyecto

Sistema de control electrónico de presión diseñado para ejecutarse autónomamente en Raspberry Pi con interfaz táctil de 7 pulgadas. Implementa una arquitectura de 3 capas con PyQt6 + QML para una interfaz moderna y atractiva.

## Funcionalidades Operativas (Estado Actual)

### ✅ Implementadas en esta versión:

1. **Estructura Base del Proyecto**
   - Arquitectura de 3 capas (Presentación, Negocio, Datos)
   - Configuración modular con PyQt6 + QML

2. **Interfaz Gráfica Inicial**
   - Aplicación PyQt6 con interfaz QML moderna
   - Gauge circular animado para visualización de presión
   - Diseño responsive optimizado para pantalla táctil 7"
   - Gradientes y efectos visuales atractivos

3. **Sistema de Configuración**
   - Cargador de configuración YAML
   - Valores por defecto configurables
   - Configuración de unidades, colores y parámetros

4. **Internacionalización (i18n)**
   - Soporte para 3 idiomas: Español, Inglés, Francés
   - Sistema de traducciones basado en YAML
   - Cambio dinámico de idioma

5. **Simulación de Datos**
   - Simulador de lecturas de presión en tiempo real
   - Actualización cada segundo con variaciones aleatorias
   - Controles para iniciar/detener simulación

## Nuevas Funcionalidades Añadidas

- **Primera implementación:** Sistema base completo con interfaz moderna
- Gauge de presión circular con animaciones suaves
- Sistema de configuración extensible
- Base para internacionalización completa

## Requisitos Aplicados Hasta el Momento

### Arquitectura y Tecnología ✅
- ✅ Lenguaje: Python
- ✅ Arquitectura de 3 capas implementada
- ✅ Interfaz local (no web) con PyQt6 + QML
- ✅ Preparado para SQLite (capa de datos)
- ✅ Optimizado para Raspberry Pi

### Configuración y Personalización ✅
- ✅ Archivo de configuración YAML
- ✅ Configuración de unidades (presión/tiempo)
- ✅ Valores por defecto para programas
- ✅ Configuración de colores de alarmas
- ✅ Soporte para logotipo personalizable
- ✅ Internacionalización (ES/EN/FR)

### Interfaz de Usuario ✅
- ✅ Optimizada para pantalla táctil 7"
- ✅ Visualización de presión en tiempo real
- ✅ Simulación de datos para desarrollo
- ✅ Interfaz moderna y atractiva

## Estructura del Proyecto

```
pressure_control_system/
├── config/                    # Configuraciones
│   ├── defaults.yaml         # Valores por defecto
│   └── i18n/                 # Traducciones
├── src/                      # Código fuente
│   ├── presentation/         # Capa de presentación (PyQt6/QML)
│   ├── business/            # Lógica de negocio (pendiente)
│   ├── data/                # Acceso a datos (pendiente)
│   ├── hardware/            # Interfaz hardware (pendiente)
│   └── utils/               # Utilidades
├── assets/                  # Recursos estáticos
├── requirements.txt         # Dependencias
└── main.py                 # Punto de entrada
```

## Instalación y Ejecución

### Dependencias
```bash
pip install -r requirements.txt
```

### Ejecución
```bash
python main.py
```

## Próximos Pasos Planificados

1. **Capa de Datos:** Implementar SQLite y repositorios
2. **Gestión de Usuarios:** Sistema de autenticación y roles
3. **Gestión de Programas:** CRUD completo
4. **Hardware Integration:** Sensores y actuadores reales
5. **Ejecución de Programas:** Lógica de control completa

## Tecnologías Utilizadas

- **Python 3.8+**
- **PyQt6** - Framework GUI
- **QML** - Interfaz moderna y fluida
- **PyYAML** - Configuración
- **SQLite** - Base de datos (próximamente)

## Notas de Desarrollo

- La aplicación está configurada para modo de simulación durante desarrollo
- La interfaz está optimizada para resolución 800x480 (pantalla táctil 7")
- El sistema mantiene toda la funcionalidad existente al agregar nuevas características
- Desarrollo incremental siguiendo los requisitos especificados

---
**Desarrollado incrementalmente para totama76**