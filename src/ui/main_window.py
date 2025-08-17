# Main Window - Ventana principal de la aplicación
# Combina la vista de planetas para stream y el panel de control

import pygame
import sys
from typing import Optional
from ..core.session_manager import SessionManager
from ..core.planet_system import PlanetSystem
from .planet_display import PlanetDisplay
from .control_panel import ControlPanel

class MainWindow:
    """
    Ventana principal que gestiona la interfaz completa de la aplicación
    
    Futuras mejoras:
    - Ventanas separadas para stream y control
    - Modo fullscreen para capturas de pantalla
    - Configuración de resolución por preset de streaming
    - Temas visuales personalizables
    - Atajos de teclado para funciones rápidas
    """
    
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.planet_system = PlanetSystem()
        
        # Obtener tamaño de pantalla dinámicamente
        pygame.init()
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        
        # Configuración de ventana RESPONSIVE para TikTok Live
        # Usar un porcentaje de la pantalla para asegurar que quepa
        max_width = min(720, int(screen_width * 0.4))   # Máximo 720px o 40% del ancho
        max_height = min(1000, int(screen_height * 0.85)) # Máximo 1000px o 85% del alto
        
        # Mantener proporción vertical pero adaptable
        self.window_width = max_width
        self.window_height = max_height
        self.fps = 60
        
        # Crear ventana con tamaño calculado dinámicamente
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("TikTok Planets System - Responsive Layout")
        self.clock = pygame.time.Clock()
        
        # Componentes de UI para layout VERTICAL con OVERLAY
        self.planet_display = PlanetDisplay(self.planet_system, 
                                          display_width=self.window_width, 
                                          display_height=self.window_height,  # Pantalla completa
                                          layout_mode="vertical")
        self.control_panel = ControlPanel(self.planet_system, 
                                        panel_width=self.window_width,  # Pantalla completa para overlay
                                        panel_height=self.window_height)
        
        # Estado de la aplicación
        self.running = True
        self.last_update_time = 0
    
    def run(self):
        """
        Loop principal de la aplicación
        
        Futuras optimizaciones:
        - Rendering diferencial (solo actualizar cambios)
        - Múltiples hilos para UI y lógica
        - Gestión de memoria para sesiones largas
        """
        while self.running:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_update_time
            self.last_update_time = current_time
            
            # Procesar eventos
            self._handle_events()
            
            # Actualizar componentes
            self._update(delta_time)
            
            # Renderizar
            self._render()
            
            # Control de FPS
            self.clock.tick(self.fps)
    
    def _handle_events(self):
        """
        Gestiona todos los eventos de entrada
        
        Futuros eventos:
        - Atajos de teclado para donaciones rápidas
        - Arrastrar y soltar para reordenar planetas
        - Zoom y pan en la vista de planetas
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Delegar eventos a componentes
            self.control_panel.handle_event(event)
            self.planet_display.handle_event(event)
            
            # Eventos globales de teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_F11:
                    self._toggle_fullscreen()
                elif event.key == pygame.K_F5:
                    self._refresh_display()
    
    def _update(self, delta_time: int):
        """
        Actualiza la lógica de la aplicación
        
        Futuras actualizaciones:
        - Animaciones de transición entre estados
        - Efectos de partículas
        - Sincronización con datos externos
        """
        self.control_panel.update(delta_time)
        self.planet_display.update(delta_time)
        
        # Verificar si hay nuevas donaciones procesadas
        if self.control_panel.has_new_donation():
            donation_data = self.control_panel.get_new_donation()
            self._process_new_donation(donation_data)
    
    def _render(self):
        """
        Renderiza todos los componentes en pantalla VERTICAL con OVERLAY
        
        Layout para TikTok Live:
        - Fondo completo: Display de planetas (pantalla completa)
        - Overlay: Controles flotantes en zona libre (sin panel inferior)
        """
        # Limpiar pantalla con fondo espacial
        self.screen.fill((10, 10, 20))  # Azul espacial muy oscuro
        
        # Renderizar display de planetas en PANTALLA COMPLETA
        planet_surface = self.planet_display.render()
        self.screen.blit(planet_surface, (0, 0))
        
        # Renderizar controles OVERLAY pequeño en posición específica
        control_surface = self.control_panel.render()
        # Posicionar el overlay pequeño en la zona libre (círculo naranja)
        overlay_pos = (self.control_panel.overlay_x, self.control_panel.overlay_y)
        self.screen.blit(control_surface, overlay_pos)
        
        # NO hay línea divisoria - todo es overlay
        
        # Información de sesión (opcional, en esquina superior izquierda)
        self._render_session_info()
        
        # Actualizar display
        pygame.display.flip()
    
    def _process_new_donation(self, donation_data: dict):
        """
        Procesa una nueva donación recibida del panel de control
        
        Futuras validaciones:
        - Verificación de datos de entrada
        - Logging de donaciones para auditoría
        - Triggers para efectos especiales
        """
        donor_name = donation_data["donor_name"]
        gift_type = donation_data["gift_type"]
        custom_value = donation_data.get("custom_value")
        
        # Crear planeta o actualizar existente
        planet = self.planet_system.add_donation(donor_name, gift_type, custom_value)
        
        # Guardar en base de datos
        self.session_manager.db_manager.save_planet(planet)
        if planet.donations_history:
            last_donation = planet.donations_history[-1]
            self.session_manager.db_manager.save_donation(last_donation)
    
    def _render_session_info(self):
        """
        Renderiza información básica de sesión en esquina superior
        Simplificado para TikTok Live - solo info esencial
        """
        font = pygame.font.Font(None, 20)  # Fuente más pequeña
        stats = self.session_manager.get_session_stats()
        
        # Info compacta en una línea
        info_text = f"Planetas: {stats['total_planets']} | {stats['total_donations']} coins"
        text_surface = font.render(info_text, True, (255, 255, 255))
        
        # Fondo semi-transparente para legibilidad
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10)
        background_rect = text_rect.inflate(10, 5)
        
        # Superficie con alpha para fondo
        bg_surface = pygame.Surface(background_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 128))  # Negro semi-transparente
        
        self.screen.blit(bg_surface, background_rect.topleft)
        self.screen.blit(text_surface, text_rect.topleft)
    
    def _toggle_fullscreen(self):
        """
        Alterna entre modo ventana y pantalla completa
        
        Futuro: Recordar preferencia del usuario
        """
        pygame.display.toggle_fullscreen()
    
    def _refresh_display(self):
        """
        Refresca la pantalla manualmente
        
        Futuro: Recargar datos desde base de datos
        """
        pass
