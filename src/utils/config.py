# Configuration Utilities - Manejo de configuración del sistema
# Gestiona configuraciones, presets y preferencias del usuario

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    """
    Gestiona la configuración del sistema de planetas
    
    Futuras configuraciones:
    - Temas visuales personalizables
    - Resoluciones de pantalla predefinidas
    - Configuración de valores de regalos por región
    - Preferencias de efectos visuales
    - Configuración de streaming (OBS, resolución)
    - Perfiles de configuración por streamer
    """
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_default_config()
        self.load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """
        Carga configuración por defecto del sistema
        
        Futuras configuraciones por defecto:
        - Múltiples temas (espacial, científico, minimalista)
        - Configuraciones regionales (precios TikTok por país)
        - Presets de calidad (alta, media, baja)
        """
        return {
            "display": {
                "width": 1200,
                "height": 800,
                "fps": 60,
                "fullscreen": False,
                "planet_display_width": 800,
                "planet_display_height": 600,
                "max_visible_planets": 4
            },
            "visual": {
                "theme": "space",
                "show_planet_names": True,
                "show_planet_values": True,
                "show_background_stars": True,
                "enable_planet_effects": True,
                "animation_speed": 1.0
            },
            "donations": {
                "default_gift_values": {
                    "rose": 1,
                    "perfume": 5,
                    "finger_heart": 5,
                    "glow_stick": 10,
                    "ice_cream": 15,
                    "heart_me": 25,
                    "birthday_cake": 50,
                    "motorcycle": 100,
                    "sports_car": 500,
                    "yacht": 1000,
                    "rocket": 2000,
                    "castle": 5000
                },
                "auto_save": True,
                "session_backup": True
            },
            "ui": {
                "font_size_large": 24,
                "font_size_medium": 20,
                "font_size_small": 16,
                "panel_width": 400,
                "enable_quick_buttons": True
            }
        }
    
    def load_config(self) -> bool:
        """
        Carga configuración desde archivo
        
        Futuras mejoras:
        - Validación de esquema de configuración
        - Migración automática entre versiones
        - Backup de configuraciones anteriores
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge con configuración por defecto
                    self._merge_config(self.config, loaded_config)
                return True
        except Exception as e:
            print(f"Error loading config: {e}")
        return False
    
    def save_config(self) -> bool:
        """
        Guarda configuración actual a archivo
        
        Futuras mejoras:
        - Backup antes de guardar
        - Compresión de configuraciones grandes
        - Encriptación de configuraciones sensibles
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Obtiene valor de configuración usando notación de punto
        Ejemplo: get("display.width") retorna config["display"]["width"]
        
        Futuras mejoras:
        - Validación de tipos de dato
        - Configuraciones dinámicas
        - Cache de valores frecuentemente accedidos
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> bool:
        """
        Establece valor de configuración usando notación de punto
        
        Futuras validaciones:
        - Verificar tipos de dato esperados
        - Validar rangos de valores numéricos
        - Callbacks para cambios de configuración
        """
        keys = key_path.split('.')
        config = self.config
        
        try:
            # Navegar hasta el penúltimo nivel
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # Establecer el valor final
            config[keys[-1]] = value
            return True
        except Exception:
            return False
    
    def _merge_config(self, default: Dict, loaded: Dict):
        """
        Combina configuración cargada con valores por defecto
        
        Futuras mejoras:
        - Detección de configuraciones obsoletas
        - Actualización automática de formato
        - Preservar configuraciones personalizadas
        """
        for key, value in loaded.items():
            if key in default:
                if isinstance(default[key], dict) and isinstance(value, dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
    
    def get_display_config(self) -> Dict:
        """Retorna configuración específica de display"""
        return self.get("display", {})
    
    def get_visual_config(self) -> Dict:
        """Retorna configuración específica de efectos visuales"""
        return self.get("visual", {})
    
    def get_donation_values(self) -> Dict:
        """Retorna tabla de valores de donaciones"""
        return self.get("donations.default_gift_values", {})
    
    def update_gift_value(self, gift_type: str, value: int):
        """
        Actualiza el valor de un tipo de regalo específico
        
        Futuras mejoras:
        - Historial de cambios de precios
        - Sincronización con APIs oficiales
        - Alertas de cambios significativos
        """
        self.set(f"donations.default_gift_values.{gift_type}", value)
        self.save_config()
    
    def reset_to_defaults(self):
        """
        Resetea toda la configuración a valores por defecto
        
        Futuras mejoras:
        - Backup antes de resetear
        - Reset selectivo por secciones
        - Confirmación de usuario
        """
        self.config = self._load_default_config()
        self.save_config()


# Instancia global de configuración
config_manager = ConfigManager()
