# Documentación de Arquitectura - Herramienta de Pruebas AFD

## Resumen
La Herramienta de Pruebas AFD ha sido reestructurada siguiendo **principios SOLID** y **prácticas de código limpio** para mejorar la mantenibilidad, testabilidad y extensibilidad. El archivo monolítico `streamlit_app.py` (680 líneas) ha sido refactorizado en una arquitectura modular con clara separación de responsabilidades.

## Cómo Ejecutar la Aplicación

### Requisitos del Sistema
- Python 3.9 o superior
- Graphviz instalado en el sistema

### Comandos de Ejecución

#### 1. Verificar la Instalación
```bash
# Verificar que Python está disponible
python3 --version

# Verificar que Streamlit está instalado
python3 -m streamlit --version

# Verificar que la aplicación se puede importar correctamente
python3 -c "import streamlit_app; print('✅ Aplicación lista para ejecutar!')"
```

#### 2. Ejecutar la Aplicación
```bash
# Comando básico
streamlit run streamlit_app.py

# Ejecutar en puerto específico
python3 -m streamlit run streamlit_app.py --server.port 8501

# Ejecutar en modo headless (sin abrir navegador automáticamente)
python3 -m streamlit run streamlit_app.py --server.headless true

# Ejecutar con recarga automática en desarrollo
streamlit run streamlit_app.py --server.runOnSave true
```

#### 3. Acceder a la Aplicación
- **URL Local**: http://localhost:8501
- **URL de Red**: http://192.168.x.x:8501 (mostrada en la terminal)

### Funcionalidades Principales

#### 🎯 Crear Autómatas
1. **Configurar Alfabeto**: Define símbolos (ej: 0,1)
2. **Definir Estados**: Crea estados (ej: q0,q1,q2)
3. **Establecer Estado Inicial**: Selecciona punto de inicio
4. **Marcar Estados Finales**: Define estados de aceptación
5. **Agregar Transiciones**: Usa el formulario interactivo

#### 🔍 Probar Cadenas
1. **Entrada**: Escribe la cadena a probar
2. **Simulación**: Ejecuta paso a paso
3. **Resultado**: Ve si es aceptada o rechazada
4. **Trace**: Observa el camino de ejecución

#### 📊 Visualización
- **Grafo Interactivo**: Representación visual del autómata
- **Tabla de Transiciones**: Vista tabular de la función δ
- **Quintupla**: Definición formal del autómata

#### 💾 Importar/Exportar
- **Formatos**: JSON y XML
- **Importar**: Carga autómatas desde archivos
- **Exportar**: Guarda tu trabajo

## Nueva Estructura de Directorios

```
.
├── README.md                         # Documentación principal en español
├── ARCHITECTURE.md                   # Este archivo de arquitectura
├── requirements.txt                  # Dependencias de Python
├── streamlit_app.py                  # Punto de entrada principal (limpio y minimal)
├── core/                            # Lógica de dominio (núcleo de la aplicación)
│   ├── __init__.py
│   ├── algorithms/                  # Algoritmos de autómatas
│   │   ├── __init__.py
│   │   └── dfa/                     # Algoritmos específicos para AFD
│   │       ├── __init__.py
│   │       ├── dfa_simulator.py     # Simulador principal de AFD
│   │       ├── simulation_step.py   # Representación de pasos de simulación
│   │       ├── step_by_step_simulation.py  # Simulación paso a paso
│   │       └── string_generator.py  # Generador de cadenas aceptadas
│   └── models/                      # Modelos de datos del dominio
│       ├── __init__.py
│       ├── automaton.py             # Modelo principal del autómata
│       ├── state.py                 # Modelo de estado
│       └── transition.py            # Modelo de transición
└── ui/                              # NUEVO: Capa de interfaz de usuario modular
    ├── __init__.py
    ├── components/                  # Componentes de UI (capa de presentación)
    │   ├── __init__.py
    │   ├── sidebar_component.py     # Barra lateral de configuración
    │   ├── visualization_component.py  # Visualización del autómata
    │   ├── transitions_editor_component.py  # Editor de transiciones
    │   └── simulation_component.py  # Componente de simulación y pruebas
    ├── services/                    # Servicios de lógica de negocio
    │   ├── __init__.py
    │   ├── session_state_manager.py # Gestión centralizada del estado
    │   ├── automaton_builder.py     # Constructor de objetos autómata
    │   └── import_export_service.py # Servicio de importación/exportación
    ├── styles/                      # Estilos y apariencia
    │   ├── __init__.py
    │   └── app_styles.py           # Definiciones CSS
    └── utils/                       # Funciones utilitarias
        ├── __init__.py
        └── visualization_utils.py   # Utilidades de visualización
```

## Aplicación de Principios SOLID

### 1. Principio de Responsabilidad Única (SRP)
Cada clase y módulo tiene una única responsabilidad bien definida:

- **`SessionStateManager`**: Solo gestiona el estado de sesión de Streamlit
- **`AutomatonBuilder`**: Solo construye objetos Automaton desde diferentes fuentes
- **`ImportExportService`**: Solo maneja operaciones de importación/exportación
- **`VisualizationComponent`**: Solo maneja la representación visual
- **`SimulationComponent`**: Solo maneja simulación y pruebas
- **`SidebarComponent`**: Solo gestiona la interfaz de la barra lateral

### 2. Principio Abierto/Cerrado (OCP)
- Los componentes están abiertos para extensión pero cerrados para modificación
- Nuevos formatos de exportación se pueden agregar a `ImportExportService` sin cambiar código existente
- Nuevos tipos de visualización se pueden agregar a `VisualizationUtils`
- Nuevos componentes se pueden agregar sin modificar los existentes

### 3. Principio de Sustitución de Liskov (LSP)
- Todas las clases de servicio implementan interfaces consistentes
- Los componentes pueden ser fácilmente intercambiados o extendidos sin romper funcionalidad

### 4. Principio de Segregación de Interfaces (ISP)
- Cada servicio proporciona interfaces enfocadas y cohesivas
- Los componentes solo dependen de los métodos que realmente usan
- Ningún componente es forzado a depender de funcionalidad no utilizada

### 5. Principio de Inversión de Dependencias (DIP)
- Los módulos de alto nivel (componentes) no dependen de módulos de bajo nivel (servicios)
- Ambos dependen de abstracciones (interfaces claras)
- Las dependencias fluyen hacia adentro hacia la lógica de dominio

## Capas de la Arquitectura

### 1. Capa de Presentación (`ui/components/`)
**Responsabilidad**: Componentes de interfaz de usuario y manejo de interacciones

- **`SidebarComponent`**: Panel de configuración, UI de importar/exportar
- **`VisualizationComponent`**: Visualización de grafos, información del autómata, tablas de transición
- **`TransitionsEditorComponent`**: Interfaz de gestión de transiciones
- **`SimulationComponent`**: Interfaz de pruebas de cadenas y simulación

### 2. Capa de Servicios (`ui/services/`)
**Responsabilidad**: Coordinación de lógica de negocio y transformación de datos

- **`SessionStateManager`**: Gestión centralizada del estado de sesión
- **`AutomatonBuilder`**: Convierte entre formatos de datos y objetos de dominio
- **`ImportExportService`**: Operaciones de archivos y conversiones de formato

### 3. Capa de Utilidades (`ui/utils/`)
**Responsabilidad**: Funciones puras y utilidades auxiliares

- **`VisualizationUtils`**: Utilidades de creación de grafos

### 4. Capa de Estilos (`ui/styles/`)
**Responsabilidad**: Apariencia de la aplicación y temas

- **`app_styles.py`**: Definiciones CSS y funciones de estilo

### 5. Capa de Dominio (`core/`)
**Responsabilidad**: Lógica de negocio central (sin cambios del original)

- Lógica de simulación de autómatas y generación de cadenas
- Modelos de dominio (State, Transition, Automaton)

## Beneficios de la Nueva Arquitectura

### ✅ Mantenibilidad
- **Antes**: Archivo único de 680 líneas con responsabilidades mezcladas
- **Después**: Estructura modular con límites claros (archivo más grande: ~150 líneas)

### ✅ Testabilidad
- Cada componente puede ser probado unitariamente de forma independiente
- Los servicios tienen interfaces claras para mocking
- La lógica de negocio está separada de las preocupaciones de UI

### ✅ Reutilización
- Los componentes pueden ser reutilizados en diferentes contextos
- Los servicios pueden ser usados independientemente
- La separación clara permite extracción fácil

### ✅ Extensibilidad
- Nuevos formatos de importación/exportación: agregar a `ImportExportService`
- Nuevos tipos de visualización: extender `VisualizationUtils`
- Nuevos componentes: crear en `ui/components/`
- Nuevos tipos de simulación: extender `SimulationComponent`

### ✅ Legibilidad
- Cada archivo tiene un propósito único y claro
- Las dependencias son explícitas y mínimas
- La organización del código coincide con el modelo mental

## Comandos de Verificación y Mantenimiento

### Verificar Estructura del Proyecto
```bash
# Mostrar estructura completa
tree -I "__pycache__"

# Contar líneas de código por componente
find ui/ -name "*.py" -exec wc -l {} + | sort -n

# Verificar imports
python3 -c "import streamlit_app; print('✅ Todos los imports funcionan correctamente')"
```

### Comandos de Desarrollo
```bash
# Ejecutar con recarga automática
streamlit run streamlit_app.py --server.runOnSave true

# Ejecutar en modo desarrollo con logs detallados
streamlit run streamlit_app.py --logger.level debug

# Verificar que no hay errores de sintaxis
python3 -m py_compile streamlit_app.py
find ui/ -name "*.py" -exec python3 -m py_compile {} \;
```

## Ejemplos de Uso para Desarrolladores

### Agregar un Nuevo Formato de Exportación
```python
# En ui/services/import_export_service.py
@staticmethod
def export_to_yaml() -> str:
    """Exportar AFD actual a formato YAML."""
    # Implementación aquí
    pass
```

### Agregar un Nuevo Componente
```python
# Nuevo archivo: ui/components/statistics_component.py
class StatisticsComponent:
    @staticmethod
    def render():
        """Renderizar estadísticas del autómata."""
        # Implementación aquí
        pass

# En streamlit_app.py, agregar a render_main_content():
StatisticsComponent.render()
```

### Extender el Estado de Sesión
```python
# En ui/services/session_state_manager.py
@staticmethod
def get_automaton_statistics() -> Dict:
    """Obtener estadísticas calculadas para el autómata actual."""
    # Implementación aquí
    pass
```

## Guía de Migración

El archivo monolítico original fue eliminado después de verificar que la nueva estructura mantiene 100% de compatibilidad funcional mientras proporciona una arquitectura mucho más limpia.

### Cambios Clave Realizados
1. **Punto de Entrada Principal**: `streamlit_app.py` ahora orquesta componentes en lugar de contener toda la lógica
2. **Estado de Sesión**: Centralizado en `SessionStateManager` en lugar de estar disperso
3. **Componentes UI**: Divididos en componentes enfocados y reutilizables
4. **Lógica de Negocio**: Extraída en clases de servicio
5. **Estilos**: Separados en módulo dedicado

### Ejecutar la Aplicación
El comando de ejecución sigue siendo el mismo:
```bash
streamlit run streamlit_app.py
```

La aplicación mantiene la misma funcionalidad y experiencia de usuario mientras proporciona un código base mucho más mantenible.

## Mejoras Futuras Habilitadas

La nueva arquitectura hace que estas mejoras sean mucho más fáciles de implementar:

1. **Múltiples Tipos de Autómatas**: Agregar componentes NFA, PDA junto a AFD
2. **Sistema de Plugins**: Cargar componentes adicionales dinámicamente
3. **Suite de Pruebas**: Pruebas unitarias comprehensivas para cada componente
4. **Capa de API**: Extraer servicios para uso en APIs web
5. **Múltiples UIs**: Usar servicios con diferentes frameworks frontend
6. **Integración de Base de Datos**: Agregar capa de persistencia sin afectar UI
7. **Colaboración en Tiempo Real**: Agregar soporte WebSocket a servicios
8. **Monitoreo de Rendimiento**: Agregar recolección de métricas a servicios

Esta transformación de arquitectura proporciona una base sólida para desarrollo futuro mientras mantiene código limpio y mantenible.

---

## Resumen Final

La **Herramienta de Pruebas AFD** ha sido exitosamente refactorizada de un archivo monolítico de 680 líneas a una arquitectura modular que sigue principios SOLID y prácticas de código limpio. La aplicación mantiene toda su funcionalidad original mientras proporciona una base de código más mantenible, extensible y fácil de entender.