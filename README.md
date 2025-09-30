# Herramienta de Pruebas de Autómatas Finitos

Una herramienta completa desarrollada en Python para crear, visualizar y probar Autómatas Finitos Deterministas (AFD) con una interfaz web interactiva.

## Características

- **Visualización Interactiva**: Gráficos de autómatas usando Graphviz
- **Soporte para AFD**: Crea y prueba Autómatas Finitos Deterministas
- **Simulación en Tiempo Real**: Prueba cadenas con retroalimentación instantánea de aceptación/rechazo
- **Ejecución Paso a Paso**: Rastrea la ejecución del autómata paso a paso
- **Generación de Cadenas**: Genera automáticamente cadenas aceptadas por el autómata
- **Plantillas de Ejemplo**: Inicio rápido con autómatas de ejemplo predefinidos
- **Importar/Exportar**: Soporte para formatos JSON y XML

## Inicio Rápido

### Requisitos Previos
- Python 3.9 o superior
- Graphviz instalado en el sistema

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Ejecución de la Aplicación

1. **Ejecutar la aplicación (comando recomendado):**
   ```bash
   python3 -m streamlit run streamlit_app.py
   ```

2. **Con parámetros personalizados:**
   ```bash
   python3 -m streamlit run streamlit_app.py --server.port 8502 --server.headless true
   ```

3. **Método alternativo (si el anterior no funciona):**
   ```bash
   streamlit run streamlit_app.py
   ```

**Nota:** Es posible que veas una advertencia sobre urllib3 y SSL - esto es normal y no afecta el funcionamiento de la aplicación.


### 3. Abrir en el Navegador
La aplicación se abrirá automáticamente en `http://localhost:8501`

### 4. Comenzar
Haz clic en "📘 AFD de Ejemplo" para cargar un autómata de ejemplo que acepta cadenas terminadas en '01'

## Arquitectura del Proyecto

```
automaton-test-tool/
├── streamlit_app.py          # Punto de entrada principal
├── core/                     # Lógica de dominio
│   ├── algorithms/
│   │   └── dfa/             # Algoritmos de simulación AFD
│   │       ├── dfa_simulator.py
│   │       ├── step_by_step_simulation.py
│   │       ├── simulation_step.py
│   │       └── string_generator.py
│   └── models/              # Modelos de datos
│       ├── automaton.py
│       ├── state.py
│       └── transition.py
├── ui/                      # Capa de interfaz de usuario
│   ├── components/          # Componentes de UI
│   │   ├── sidebar_component.py
│   │   ├── visualization_component.py
│   │   ├── transitions_editor_component.py
│   │   └── simulation_component.py
│   ├── services/           # Servicios de lógica de negocio
│   │   ├── session_state_manager.py
│   │   ├── automaton_builder.py
│   │   └── import_export_service.py
│   ├── styles/             # Estilos y apariencia
│   │   └── app_styles.py
│   └── utils/              # Utilidades
│       └── visualization_utils.py
├── requirements.txt         # Dependencias de Python
├── README.md               # Este archivo
└── ARCHITECTURE.md         # Documentación de arquitectura
```

## Cómo Usar la Aplicación

### Configuración del Autómata
1. **Alfabeto**: Define los símbolos que puede procesar el autómata (ej: 0,1)
2. **Estados**: Crea los estados del autómata (ej: q0,q1,q2)
3. **Estado Inicial**: Selecciona el estado donde comienza la simulación
4. **Estados Finales**: Marca los estados de aceptación

### Definir Transiciones
1. Ve a la sección "🔄 Transiciones"
2. Usa el formulario para agregar nuevas transiciones:
   - **Desde**: Estado origen
   - **Símbolo**: Símbolo de entrada
   - **Hacia**: Estado destino
3. Haz clic en "➕ Agregar" para añadir la transición
4. Las transiciones existentes se muestran con opción de eliminar

### Probar Cadenas
1. Ve a la pestaña "🚀 Simulación"
2. Ingresa una cadena de prueba
3. Haz clic en "🚀 Ejecutar Simulación"
4. La aplicación mostrará:
   - Proceso paso a paso de la evaluación
   - Estado final alcanzado
   - Resultado: ACEPTADA ✅ o RECHAZADA ❌

### Generar Cadenas Automáticamente
1. Ve a la pestaña "📝 Generar Cadenas"
2. Haz clic en "🎯 Generar Cadenas Aceptadas"
3. La aplicación generará las primeras 10 cadenas aceptadas por el autómata

### Importar/Exportar Autómatas
- **Importar**: Sube archivos JSON o XML con definiciones de autómatas
- **Exportar**: Descarga tu autómata en formato JSON o XML

## Stack Tecnológico

- **Frontend**: Streamlit (Framework web de Python)
- **Visualización**: Graphviz (Renderizado profesional de grafos)
- **Backend**: Python puro con arquitectura de dominio limpia
- **Arquitectura**: Principios SOLID, separación de responsabilidades

## Ejemplos

### AFD de Ejemplo Incluido
La aplicación incluye un AFD de ejemplo que:
- **Acepta**: Cadenas que terminan en "01"
- **Estados**: q0 (inicial), q1, q2 (final)
- **Ejemplos de cadenas aceptadas**: "01", "101", "001", "1001"
- **Ejemplos de cadenas rechazadas**: "1", "10", "11", "000"

## 🔧 Comandos de Desarrollo

### Verificar Instalación
```bash
python3 -c "import streamlit_app; print('✅ Instalación exitosa!')"
```

### Ejecutar en Modo Desarrollo
```bash
streamlit run streamlit_app.py --server.runOnSave true
```

### Verificar Estructura del Proyecto
```bash
tree -I "__pycache__"
```

## Contribuir

1. Haz fork del repositorio
2. Crea una rama para tu característica
3. Realiza tus cambios
4. Envía un pull request