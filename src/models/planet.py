# Planet Model - Representa un planeta individual
# Cada planeta pertenece a un donador y evoluciona según sus donaciones

import datetime
from typing import List, Dict
from enum import Enum

class PlanetType(Enum):
    """
    Tipos de planetas según valor de donaciones acumuladas
    
    Futuras expansiones:
    - Planetas especiales por eventos (cumpleaños, aniversarios)
    - Planetas únicos por donaciones masivas
    - Planetas con características especiales (anillos, lunas)
    """
    MERCURY = "mercury"      # 1-9 coins
    EARTH = "earth"          # 10-49 coins  
    JUPITER = "jupiter"      # 50-99 coins
    STAR = "star"           # 100-499 coins
    STELLAR_SYSTEM = "stellar_system"  # 500-999 coins
    GALAXY = "galaxy"       # 1000+ coins

class Planet:
    """
    Representa un planeta individual con sus propiedades y historia
    
    Futuras características:
    - Texturas personalizadas por tipo
    - Efectos de partículas (atmósfera, anillos)
    - Rotación y animaciones orbitales
    - Sonidos únicos por tipo de planeta
    - Colores personalizables por donador
    """
    
    # Tabla de conversión de coins a tipos de planeta
    TYPE_THRESHOLDS = {
        1: PlanetType.MERCURY,
        10: PlanetType.EARTH,
        50: PlanetType.JUPITER,
        100: PlanetType.STAR,
        500: PlanetType.STELLAR_SYSTEM,
        1000: PlanetType.GALAXY
    }
    
    def __init__(self, donor_name: str):
        self.donor_name = donor_name
        self.total_value = 0
        self.planet_type = PlanetType.MERCURY
        self.created_at = datetime.datetime.now()
        self.last_updated = datetime.datetime.now()
        self.donations_history: List['Donation'] = []
        
        # Propiedades visuales futuras
        self.position_x = 0
        self.position_y = 0
        self.size = self._calculate_size()
        self.color = self._get_default_color()
    
    def add_donation(self, donation: 'Donation'):
        """
        Añade una nueva donación y actualiza el planeta
        
        Futuras mejoras:
        - Efectos especiales al evolucionar de tipo
        - Mensajes personalizados por milestone
        - Registro de fecha/hora de cada donación
        """
        self.donations_history.append(donation)
        self.total_value += donation.value
        self.last_updated = datetime.datetime.now()
        
        # Actualizar tipo de planeta según nuevo valor
        old_type = self.planet_type
        self.planet_type = self._determine_planet_type()
        
        # Si cambió de tipo, actualizar propiedades visuales
        if old_type != self.planet_type:
            self.size = self._calculate_size()
            self.color = self._get_default_color()
    
    def _determine_planet_type(self) -> PlanetType:
        """Determina el tipo de planeta según el valor total"""
        for threshold in sorted(self.TYPE_THRESHOLDS.keys(), reverse=True):
            if self.total_value >= threshold:
                return self.TYPE_THRESHOLDS[threshold]
        return PlanetType.MERCURY
    
    def _calculate_size(self) -> int:
        """
        Calcula el tamaño visual del planeta
        
        Futuras mejoras:
        - Escalado logarítmico para valores muy grandes
        - Tamaños máximos para mantener proporción en pantalla
        - Animaciones de crecimiento suaves
        """
        size_mapping = {
            PlanetType.MERCURY: 30,
            PlanetType.EARTH: 50,
            PlanetType.JUPITER: 80,
            PlanetType.STAR: 120,
            PlanetType.STELLAR_SYSTEM: 150,
            PlanetType.GALAXY: 200
        }
        return size_mapping.get(self.planet_type, 30)
    
    def _get_default_color(self) -> tuple:
        """
        Obtiene el color por defecto según tipo de planeta
        
        Futuras personalizaciones:
        - Colores únicos por donador
        - Gradientes y texturas
        - Efectos de brillo para tipos especiales
        """
        color_mapping = {
            PlanetType.MERCURY: (169, 169, 169),  # Gris
            PlanetType.EARTH: (100, 149, 237),    # Azul
            PlanetType.JUPITER: (255, 140, 0),    # Naranja
            PlanetType.STAR: (255, 255, 0),       # Amarillo
            PlanetType.STELLAR_SYSTEM: (255, 20, 147),  # Rosa
            PlanetType.GALAXY: (138, 43, 226)     # Violeta
        }
        return color_mapping.get(self.planet_type, (169, 169, 169))
    
    def get_display_info(self) -> Dict:
        """
        Retorna información para mostrar en pantalla
        
        Futuras adiciones:
        - Estadísticas de donaciones
        - Tiempo desde última actualización
        - Ranking entre donadores
        """
        return {
            "name": self.donor_name,
            "type": self.planet_type.value,
            "total_value": self.total_value,
            "size": self.size,
            "color": self.color,
            "position": (self.position_x, self.position_y),
            "donations_count": len(self.donations_history)
        }
