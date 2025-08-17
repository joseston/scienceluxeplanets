# TikTok Planets System - Sistema de Planetas para Lives

## Información del Proyecto

**Aplicación de visualización en tiempo real** que genera planetas y cuerpos celestes personalizados basados en las donaciones recibidas durante transmisiones en vivo de TikTok. Cada donador obtiene un planeta con su nombre que crece según el valor de sus donaciones acumuladas.

## Concepto Principal

### Para el streamer:
- Herramienta de monetización que incentiva donaciones mediante visualización científica interactiva
- Panel de control intuitivo para gestión manual de donaciones
- Estadísticas de sesión en tiempo real

### Para los donadores: 
- Experiencia única de "crear" y nombrar su propio planeta/cuerpo celeste
- Representación visual persistente y evolutiva
- Sistema de progresión claro y atractivo

## Estructura Básica Implementada

```
app/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Documentación
├── 
├── src/                   # Código fuente principal
│   ├── core/              # Lógica central del negocio
│   │   ├── session_manager.py     # Gestión de sesiones de streaming
│   │   └── planet_system.py       # Sistema principal de planetas
│   │
│   ├── models/            # Modelos de datos
│   │   ├── planet.py              # Modelo de planeta individual
│   │   └── donation.py            # Modelo de donación
│   │
│   ├── database/          # Gestión de persistencia
│   │   └── database_manager.py    # Manager SQLite
│   │
│   ├── ui/                # Interfaz de usuario
│   │   ├── main_window.py         # Ventana principal
│   │   ├── planet_display.py      # Display de planetas
│   │   └── control_panel.py       # Panel de control
│   │
│   └── utils/             # Utilidades
│       ├── config.py              # Gestión de configuración
│       └── animations.py          # Sistema de animaciones
│
├── assets/                # Recursos gráficos y sonoros
│   └── README.md          # Guía de estructura de assets
│
├── config/                # Archivos de configuración
│   ├── default_config.json        # Configuración por defecto
│   └── README.md          # Documentación de configuraciones
│
└── tests/                 # Pruebas del sistema
    └── README.md          # Plan de testing
```

## Características Implementadas

### Sistema de Planetas
- ✅ Modelo de planeta con evolución basada en donaciones
- ✅ Tipos de planetas: Mercury → Earth → Jupiter → Star → Stellar System → Galaxy
- ✅ Sistema de carrusel horizontal (máximo 4 planetas visibles)
- ✅ Persistencia en base de datos SQLite por sesión

### Gestión de Donaciones
- ✅ Modelo de donación con tabla de conversión de regalos TikTok
- ✅ Valores predefinidos para regalos comunes
- ✅ Soporte para valores personalizados
- ✅ Historial completo de donaciones por donador

### Interfaz de Usuario
- ✅ Panel de control para entrada manual de donaciones
- ✅ Display de planetas con efectos visuales básicos
- ✅ Información de sesión y estadísticas
- ✅ Sistema de configuración flexible

### Base de Datos
- ✅ Esquema SQLite para planetas y donaciones
- ✅ Gestión de sesiones independientes
- ✅ Carga y persistencia automática

## Futuras Implementaciones Planeadas

### Fase 1 - Mejoras Visuales
- 🔄 Animaciones suaves de transición entre posiciones
- 🔄 Efectos especiales por tipo de planeta (anillos, brillo, texturas)
- 🔄 Sistema de partículas para efectos atmosféricos
- 🔄 Fondo estrellado animado con nebulosas
- 🔄 Temas visuales personalizables

### Fase 2 - Automatización
- 🔄 Detección automática de donaciones (API no oficial de TikTok)
- 🔄 Integración con TikTok Live Studio
- 🔄 Configuración automática de captura de pantalla
- 🔄 Sincronización en tiempo real

### Fase 3 - Funcionalidades Avanzadas
- 🔄 Sistema de sonidos personalizados por evento
- 🔄 Modo "competencia" con ranking de donadores
- 🔄 Exportar imagen del "universo" al final del live
- 🔄 Órbitas animadas y sistemas planetarios complejos
- 🔄 Efectos especiales para donaciones masivas

### Fase 4 - Escalabilidad
- 🔄 Soporte para múltiples plataformas (YouTube, Twitch)
- 🔄 Sistema de plugins para personalizaciones
- 🔄 API REST para integraciones externas
- 🔄 Dashboard web para estadísticas avanzadas
- 🔄 Sistema de backup en la nube

## Sistema de Conversión de Regalos

| Donación | Tipo de Planeta | Coins Requeridos |
|----------|----------------|------------------|
| 1-9 coins | Mercury | Muy pequeño |
| 10-49 coins | Earth | Mediano |
| 50-99 coins | Jupiter | Grande |
| 100-499 coins | Star | Muy grande con brillo |
| 500-999 coins | Stellar System | Sistema múltiple |
| 1000+ coins | Galaxy | Máximo nivel |

## Instalación y Uso

### Requisitos
- Python 3.8+
- pygame 2.5.2+
- sqlite3 (incluido en Python)

### Instalación
```bash
cd app
pip install -r requirements.txt
```

### Ejecución
```bash
python main.py
```

## Arquitectura Técnica

### Stack Principal
- **Lenguaje**: Python 3.8+
- **Renderizado**: pygame (con posible migración a PyQt para UI más compleja)
- **Base de datos**: SQLite (local por sesión)
- **Configuración**: JSON con sistema de configuración flexible

### Patrones de Diseño
- **MVC**: Separación clara entre modelos, vistas y controladores
- **Observer**: Para actualizaciones de UI en tiempo real
- **Strategy**: Para diferentes algoritmos de animación y efectos
- **Factory**: Para creación de diferentes tipos de planetas

### Consideraciones de Rendimiento
- Renderizado optimizado para 60 FPS
- Gestión eficiente de memoria para sesiones largas
- Base de datos indexada para búsquedas rápidas
- Sistema de cache para texturas y efectos

---

**Estado del Proyecto**: Estructura básica completada ✅  
**Próximo Milestone**: Implementación de efectos visuales y animaciones  
**Fecha de Última Actualización**: Agosto 2025
