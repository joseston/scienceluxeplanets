# Test Suite for TikTok Planets System
# Pruebas unitarias y de integración

## Estructura de pruebas:

### /unit/
- test_planet.py         # Pruebas del modelo Planet
- test_donation.py       # Pruebas del modelo Donation  
- test_planet_system.py  # Pruebas del sistema de planetas
- test_database.py       # Pruebas de base de datos
- test_config.py         # Pruebas de configuración

### /integration/
- test_ui_integration.py      # Pruebas de integración UI
- test_database_integration.py # Pruebas de persistencia
- test_session_flow.py        # Pruebas de flujo completo

### /performance/
- test_rendering_performance.py # Pruebas de rendimiento gráfico
- test_database_performance.py  # Pruebas de rendimiento BD
- test_memory_usage.py          # Pruebas de uso de memoria

## Futuras pruebas:
- test_api_integration.py       # Pruebas con API de TikTok
- test_stress_testing.py        # Pruebas de estrés con muchas donaciones
- test_visual_regression.py     # Pruebas de regresión visual
- test_cross_platform.py        # Pruebas multiplataforma
