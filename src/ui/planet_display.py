# Planet Display - Componente que renderiza los planetas en carrusel
# Muestra los planetas visibles para captura en TikTok Live

import pygame
import math
from typing import List
from ..core.planet_system import PlanetSystem
from ..models.planet import Planet

class PlanetDisplay:
    """
    Componente de visualización de planetas en carrusel horizontal
    
    Futuras mejoras:
    - Efectos de transición suaves entre posiciones
    - Animaciones de rotación de planetas
    - Efectos de partículas (atmósferas, anillos)
    - Zoom dinámico según tamaño de planeta
    - Efectos de iluminación y sombras
    - Fondos de nebulosas y estrellas animadas
    """
    
    def __init__(self, planet_system: PlanetSystem, display_width: int, display_height: int):
        self.planet_system = planet_system
        self.width = display_width
        self.height = display_height
        self.surface = pygame.Surface((self.width, self.height))
        
        # Configuración visual
        self.background_color = (10, 10, 20)  # Azul espacial muy oscuro
        self.max_visible_planets = 4
        self.planet_spacing = self.width // (self.max_visible_planets + 1)
        
        # Configuración de animaciones
        self.animation_speed = 2.0
        self.rotation_speed = 0.5
        self.current_rotation = 0
        
        # Efectos visuales futuros
        self.show_orbits = False
        self.show_names = True
        self.show_values = True
        self.particle_effects = False
    
    def update(self, delta_time: int):
        """
        Actualiza animaciones y efectos visuales
        
        Futuras animaciones:
        - Transiciones suaves cuando aparecen nuevos planetas
        - Efectos de pulsación para planetas recién actualizados
        - Movimiento orbital para sistemas estelares
        """
        # Actualizar rotación global (para efectos de fondo)
        self.current_rotation += self.rotation_speed * (delta_time / 1000.0)
        if self.current_rotation >= 360:
            self.current_rotation = 0
        
        # Futuras actualizaciones de animaciones de planetas individuales
    
    def render(self) -> pygame.Surface:
        """
        Renderiza todos los planetas visibles en el carrusel
        
        Futuras mejoras de rendering:
        - Shaders para efectos visuales avanzados
        - Capas separadas para diferentes elementos
        - Optimización de rendering para planetas fuera de pantalla
        """
        # Limpiar superficie
        self.surface.fill(self.background_color)
        
        # Renderizar fondo estrellado (futuro)
        self._render_background()
        
        # Obtener planetas visibles
        visible_planets = self.planet_system.get_visible_planets()
        
        # Renderizar cada planeta
        for i, planet in enumerate(visible_planets):
            self._render_planet(planet, i)
        
        # Efectos de overlay (futuro)
        self._render_overlay_effects()
        
        return self.surface
    
    def _render_planet(self, planet: Planet, position_index: int):
        """
        Renderiza un planeta individual en su posición del carrusel
        
        Futuras mejoras:
        - Texturas específicas por tipo de planeta
        - Efectos de brillo y atmósfera
        - Anillos para planetas grandes
        - Lunas orbitando para sistemas complejos
        """
        # Calcular posición en carrusel
        x = (position_index + 1) * self.planet_spacing
        y = self.height // 2
        
        # Obtener propiedades visuales del planeta
        display_info = planet.get_display_info()
        size = display_info["size"]
        color = display_info["color"]
        
        # Renderizar planeta base
        pygame.draw.circle(self.surface, color, (x, y), size)
        
        # Efectos visuales adicionales según tipo
        self._render_planet_effects(planet, x, y, size)
        
        # Renderizar nombre del donador
        if self.show_names:
            self._render_planet_name(planet, x, y - size - 30)
        
        # Renderizar valor de donaciones
        if self.show_values:
            self._render_planet_value(planet, x, y + size + 20)
    
    def _render_planet_effects(self, planet: Planet, x: int, y: int, size: int):
        """
        Renderiza efectos especiales según el tipo de planeta
        
        Efectos futuros por tipo:
        - Mercury: Superficie rocosa y cráteres
        - Earth: Continentes y océanos
        - Jupiter: Bandas de colores y gran mancha roja
        - Star: Efectos de brillo y llamaradas
        - Stellar System: Múltiples estrellas orbitando
        - Galaxy: Forma espiral con brazos
        """
        planet_type = planet.planet_type
        
        if planet_type.value == "star":
            # Efecto de brillo para estrellas
            for i in range(3):
                alpha = 50 - (i * 15)
                glow_size = size + (i * 10)
                # Crear superficie temporal con alpha
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*planet.color, alpha), (glow_size, glow_size), glow_size)
                self.surface.blit(glow_surface, (x - glow_size, y - glow_size))
        
        elif planet_type.value == "jupiter":
            # Anillos para Júpiter
            ring_color = (200, 150, 100, 100)
            ring_surface = pygame.Surface((size * 3, size // 4), pygame.SRCALPHA)
            pygame.draw.ellipse(ring_surface, ring_color, ring_surface.get_rect())
            self.surface.blit(ring_surface, (x - size * 1.5, y - size // 8))
        
        elif planet_type.value == "galaxy":
            # Efecto espiral para galaxias (simplificado)
            for angle in range(0, 360, 30):
                spiral_x = x + math.cos(math.radians(angle)) * (size * 0.7)
                spiral_y = y + math.sin(math.radians(angle)) * (size * 0.3)
                pygame.draw.circle(self.surface, (255, 255, 255, 150), (int(spiral_x), int(spiral_y)), 3)
    
    def _render_planet_name(self, planet: Planet, x: int, y: int):
        """
        Renderiza el nombre del donador sobre el planeta
        
        Futuras mejoras:
        - Fuentes personalizables
        - Colores basados en tipo de planeta
        - Efectos de texto (sombras, brillos)
        """
        font = pygame.font.Font(None, 24)
        text_surface = font.render(planet.donor_name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x, y))
        self.surface.blit(text_surface, text_rect)
    
    def _render_planet_value(self, planet: Planet, x: int, y: int):
        """
        Renderiza el valor total de donaciones bajo el planeta
        
        Futuras mejoras:
        - Formato de números con separadores
        - Iconos de monedas
        - Animaciones cuando el valor cambia
        """
        font = pygame.font.Font(None, 20)
        value_text = f"{planet.total_value} coins"
        text_surface = font.render(value_text, True, (200, 200, 200))
        text_rect = text_surface.get_rect(center=(x, y))
        self.surface.blit(text_surface, text_rect)
    
    def _render_background(self):
        """
        Renderiza fondo estrellado animado
        
        Futuras mejoras:
        - Estrellas parpadeantes
        - Nebulosas de colores
        - Movimiento de paralaje
        - Meteoritos ocasionales
        """
        # Placeholder para estrellas estáticas
        import random
        random.seed(42)  # Seed fijo para estrellas consistentes
        
        for _ in range(50):
            star_x = random.randint(0, self.width)
            star_y = random.randint(0, self.height)
            star_size = random.randint(1, 2)
            pygame.draw.circle(self.surface, (255, 255, 255), (star_x, star_y), star_size)
    
    def _render_overlay_effects(self):
        """
        Renderiza efectos de overlay como transiciones y partículas
        
        Futuros efectos:
        - Partículas de polvo espacial
        - Efectos de transición al aparecer/desaparecer planetas
        - Indicadores de actividad reciente
        """
        pass
    
    def handle_event(self, event: pygame.event.Event):
        """
        Maneja eventos específicos del display de planetas
        
        Futuros controles:
        - Click en planeta para ver detalles
        - Scroll para hacer zoom
        - Arrastrar para rotar vista
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Verificar si se hizo click en algún planeta
            self._handle_planet_click(mouse_x, mouse_y)
    
    def _handle_planet_click(self, mouse_x: int, mouse_y: int):
        """
        Maneja clicks en planetas individuales
        
        Futuras acciones:
        - Mostrar detalles del donador
        - Centrar planeta en vista
        - Mostrar historial de donaciones
        """
        pass
