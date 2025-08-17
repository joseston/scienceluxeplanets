# Planet System Core - Lógica principal del sistema de planetas
# Gestiona la creación, actualización y visualización de planetas

from typing import List, Dict, Optional
from ..models.planet import Planet
from ..models.donation import Donation

class PlanetSystem:
    """
    Sistema principal que gestiona todos los planetas y sus interacciones
    
    Futuras implementaciones:
    - Sistema de órbitas animadas
    - Efectos especiales para donaciones grandes
    - Colisiones y interacciones entre planetas
    - Sistema de lunas para planetas grandes
    - Efectos de partículas y atmósferas
    """
    
    def __init__(self):
        self.planets: List[Planet] = []
        self.visible_planets: List[Planet] = []
        self.max_visible_planets: int = 4
    
    def add_donation(self, donor_name: str, gift_type: str, value: int) -> Planet:
        """
        Procesa una nueva donación y actualiza o crea planeta
        
        Futuras mejoras:
        - Efectos de sonido personalizados por tipo de regalo
        - Animaciones de transformación cuando cambia tipo de planeta
        - Sistema de logros por donaciones múltiples
        """
        # Buscar planeta existente del donador
        existing_planet = self.find_planet_by_donor(donor_name)
        
        if existing_planet:
            # Actualizar planeta existente
            donation = Donation(donor_name, gift_type, value)
            existing_planet.add_donation(donation)
            # Mover a posición más reciente
            self._move_to_recent_position(existing_planet)
            return existing_planet
        else:
            # Crear nuevo planeta
            new_planet = Planet(donor_name)
            donation = Donation(donor_name, gift_type, value)
            new_planet.add_donation(donation)
            self.planets.append(new_planet)
            self._add_to_visible_carousel(new_planet)
            return new_planet
    
    def find_planet_by_donor(self, donor_name: str) -> Optional[Planet]:
        """Busca un planeta por nombre del donador"""
        for planet in self.planets:
            if planet.donor_name.lower() == donor_name.lower():
                return planet
        return None
    
    def get_visible_planets(self) -> List[Planet]:
        """Retorna los planetas actualmente visibles en el carrusel"""
        return self.visible_planets.copy()
    
    def _move_to_recent_position(self, planet: Planet):
        """
        Mueve un planeta a la posición más reciente (derecha)
        
        Futuras animaciones:
        - Transición suave de posiciones
        - Efectos de zoom cuando se actualiza
        - Brillo temporal para destacar actualización
        """
        if planet in self.visible_planets:
            self.visible_planets.remove(planet)
        self.visible_planets.append(planet)
        
        # Mantener límite de planetas visibles
        if len(self.visible_planets) > self.max_visible_planets:
            self.visible_planets.pop(0)
    
    def _add_to_visible_carousel(self, planet: Planet):
        """
        Añade un nuevo planeta al carrusel visible
        
        Futuras animaciones:
        - Entrada desde la derecha con efecto slide
        - Efecto de aparición gradual
        - Sonido de "nuevo planeta creado"
        """
        self.visible_planets.append(planet)
        
        # Mantener límite de planetas visibles
        if len(self.visible_planets) > self.max_visible_planets:
            self.visible_planets.pop(0)
    
    def get_total_session_value(self) -> int:
        """
        Calcula el valor total de todas las donaciones de la sesión
        
        Futuras métricas:
        - Promedio de donación por persona
        - Donador más generoso
        - Tipo de regalo más popular
        """
        return sum(planet.total_value for planet in self.planets)
