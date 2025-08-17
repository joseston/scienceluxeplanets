# TikTok Planets System
# Sistema de Planetas para Lives de TikTok

Aplicación de visualización en tiempo real que genera planetas personalizados basados en donaciones de TikTok Live.

## Características Principales
- Visualización de planetas en carrusel horizontal
- Sistema de crecimiento basado en donaciones acumuladas
- Interfaz de control manual para streamers
- Base de datos SQLite para persistencia por sesión

## Instalación
```bash
pip install -r requirements.txt
```

## Uso
```bash
python main.py
```

## Estructura del Proyecto
```
app/
├── main.py                 # Punto de entrada principal
├── src/
│   ├── core/              # Lógica central del negocio
│   ├── models/            # Modelos de datos
│   ├── ui/                # Interfaz de usuario
│   ├── database/          # Gestión de base de datos
│   └── utils/             # Utilidades y helpers
├── assets/                # Recursos gráficos y sonidos
├── config/                # Archivos de configuración
└── tests/                 # Pruebas unitarias
```

## Futuras Implementaciones
- Detección automática de donaciones (API TikTok)
- Efectos visuales avanzados y animaciones
- Sistema de sonidos personalizados
- Modo competencia con ranking
- Exportación de universo al final del live
- Órbitas animadas y efectos especiales
