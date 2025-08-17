# Control Panel - Panel de control para el streamer
# Interfaz para ingresar donaciones manualmente durante el live

import pygame
import pygame_gui
from typing import Dict, Optional
from ..core.planet_system import PlanetSystem
from ..models.donation import Donation

class ControlPanel:
    """
    Panel de control para que el streamer gestione donaciones manualmente
    
    Futuras mejoras:
    - Integración con API de TikTok para donaciones automáticas
    - Preset de donadores frecuentes
    - Historial de donaciones con búsqueda
    - Atajos de teclado personalizables
    - Modo "donación rápida" con botones predefinidos
    - Estadísticas en tiempo real
    """
    
    def __init__(self, planet_system: PlanetSystem, panel_width: int, panel_height: int):
        self.planet_system = planet_system
        self.width = panel_width
        self.height = panel_height
        self.surface = pygame.Surface((self.width, self.height))
        
        # Estado del panel
        self.new_donation_pending = False
        self.pending_donation_data: Optional[Dict] = None
        
        # Elementos de UI (simulados con pygame básico por ahora)
        self.font_large = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 20)
        self.font_small = pygame.font.Font(None, 16)
        
        # Estado de entrada de texto
        self.input_donor_name = ""
        self.input_active = False
        self.selected_gift = "rose"
        self.custom_value = ""
        
        # Colores
        self.bg_color = (40, 40, 50)
        self.button_color = (70, 70, 90)
        self.button_hover_color = (90, 90, 110)
        self.text_color = (255, 255, 255)
        self.input_color = (60, 60, 80)
        
        # Configuración de layout
        self.setup_layout()
    
    def setup_layout(self):
        """
        Configura el layout del panel de control
        
        Futuras mejoras:
        - Layout responsive
        - Temas visuales personalizables
        - Configuración guardada por usuario
        """
        self.title_rect = pygame.Rect(10, 10, self.width - 20, 30)
        self.donor_input_rect = pygame.Rect(10, 60, self.width - 20, 30)
        self.gift_selector_rect = pygame.Rect(10, 110, self.width - 20, 30)
        self.value_input_rect = pygame.Rect(10, 160, self.width - 20, 30)
        self.submit_button_rect = pygame.Rect(10, 210, self.width - 20, 40)
        self.history_rect = pygame.Rect(10, 270, self.width - 20, self.height - 280)
    
    def update(self, delta_time: int):
        """
        Actualiza el estado del panel de control
        
        Futuras actualizaciones:
        - Validación en tiempo real de campos
        - Autocompletado de nombres de donadores
        - Sugerencias de valores basadas en historial
        """
        pass
    
    def render(self) -> pygame.Surface:
        """
        Renderiza el panel de control completo
        
        Futuras mejoras de UI:
        - Iconos para diferentes tipos de regalos
        - Indicadores visuales de estado
        - Animaciones de feedback
        """
        # Limpiar superficie
        self.surface.fill(self.bg_color)
        
        # Título
        self._render_title()
        
        # Campos de entrada
        self._render_input_fields()
        
        # Botones
        self._render_buttons()
        
        # Historial/estadísticas
        self._render_history_panel()
        
        return self.surface
    
    def _render_title(self):
        """Renderiza el título del panel"""
        title_text = "Control de Donaciones"
        text_surface = self.font_large.render(title_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.title_rect.centerx, self.title_rect.centery))
        self.surface.blit(text_surface, text_rect)
    
    def _render_input_fields(self):
        """
        Renderiza los campos de entrada de datos
        
        Futuras mejoras:
        - Validación visual en tiempo real
        - Placeholder text
        - Autocompletado dropdown
        """
        # Campo nombre del donador
        pygame.draw.rect(self.surface, self.input_color, self.donor_input_rect)
        pygame.draw.rect(self.surface, self.text_color, self.donor_input_rect, 2)
        
        label = self.font_medium.render("Nombre del donador:", True, self.text_color)
        self.surface.blit(label, (self.donor_input_rect.x, self.donor_input_rect.y - 25))
        
        donor_text = self.font_medium.render(self.input_donor_name, True, self.text_color)
        self.surface.blit(donor_text, (self.donor_input_rect.x + 5, self.donor_input_rect.y + 5))
        
        # Selector de regalo
        pygame.draw.rect(self.surface, self.input_color, self.gift_selector_rect)
        pygame.draw.rect(self.surface, self.text_color, self.gift_selector_rect, 2)
        
        gift_label = self.font_medium.render("Tipo de regalo:", True, self.text_color)
        self.surface.blit(gift_label, (self.gift_selector_rect.x, self.gift_selector_rect.y - 25))
        
        gift_text = self.font_medium.render(self.selected_gift.replace("_", " ").title(), True, self.text_color)
        self.surface.blit(gift_text, (self.gift_selector_rect.x + 5, self.gift_selector_rect.y + 5))
        
        # Campo valor personalizado (opcional)
        pygame.draw.rect(self.surface, self.input_color, self.value_input_rect)
        pygame.draw.rect(self.surface, self.text_color, self.value_input_rect, 2)
        
        value_label = self.font_medium.render("Valor personalizado (opcional):", True, self.text_color)
        self.surface.blit(value_label, (self.value_input_rect.x, self.value_input_rect.y - 25))
        
        value_text = self.font_medium.render(self.custom_value, True, self.text_color)
        self.surface.blit(value_text, (self.value_input_rect.x + 5, self.value_input_rect.y + 5))
    
    def _render_buttons(self):
        """
        Renderiza botones de acción
        
        Futuros botones:
        - Presets de donaciones comunes
        - Botón de "última donación"
        - Botones de acceso rápido por tipo de regalo
        """
        # Botón principal de envío
        button_color = self.button_hover_color if self._can_submit() else self.button_color
        pygame.draw.rect(self.surface, button_color, self.submit_button_rect)
        pygame.draw.rect(self.surface, self.text_color, self.submit_button_rect, 2)
        
        button_text = "Crear/Actualizar Planeta"
        text_surface = self.font_medium.render(button_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.submit_button_rect.center)
        self.surface.blit(text_surface, text_rect)
        
        # Botones de regalo rápido (futuro)
        self._render_quick_gift_buttons()
    
    def _render_quick_gift_buttons(self):
        """
        Renderiza botones de acceso rápido para regalos comunes
        
        Futuros botones:
        - Rosa (1 coin)
        - Corazón (5 coins)
        - Helado (15 coins)
        - Auto (500 coins)
        """
        quick_gifts = [("Rosa", "rose", 1), ("Corazón", "finger_heart", 5), ("Auto", "sports_car", 500)]
        button_width = (self.width - 40) // 3
        button_height = 25
        y_pos = 260
        
        for i, (name, gift_type, value) in enumerate(quick_gifts):
            x_pos = 10 + i * (button_width + 10)
            button_rect = pygame.Rect(x_pos, y_pos, button_width, button_height)
            
            pygame.draw.rect(self.surface, self.button_color, button_rect)
            pygame.draw.rect(self.surface, self.text_color, button_rect, 1)
            
            text = f"{name} ({value})"
            text_surface = self.font_small.render(text, True, self.text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.surface.blit(text_surface, text_rect)
    
    def _render_history_panel(self):
        """
        Renderiza panel de historial y estadísticas
        
        Futuras estadísticas:
        - Lista de donadores recientes
        - Total de la sesión
        - Donador más generoso
        - Gráfico de donaciones por tiempo
        """
        # Marco del panel
        pygame.draw.rect(self.surface, self.input_color, self.history_rect)
        pygame.draw.rect(self.surface, self.text_color, self.history_rect, 2)
        
        # Título del historial
        history_title = "Estadísticas de Sesión"
        title_surface = self.font_medium.render(history_title, True, self.text_color)
        self.surface.blit(title_surface, (self.history_rect.x + 5, self.history_rect.y + 5))
        
        # Estadísticas básicas
        visible_planets = self.planet_system.get_visible_planets()
        total_value = self.planet_system.get_total_session_value()
        
        stats_y = self.history_rect.y + 35
        stats = [
            f"Planetas activos: {len(visible_planets)}",
            f"Valor total: {total_value} coins",
            f"Donadores únicos: {len(self.planet_system.planets)}"
        ]
        
        for i, stat in enumerate(stats):
            stat_surface = self.font_small.render(stat, True, self.text_color)
            self.surface.blit(stat_surface, (self.history_rect.x + 5, stats_y + i * 20))
        
        # Lista de planetas recientes (futuro)
        self._render_recent_planets_list()
    
    def _render_recent_planets_list(self):
        """
        Renderiza lista de planetas más recientes
        
        Futuras mejoras:
        - Scroll para listas largas
        - Click para editar planeta
        - Indicadores de tiempo desde última donación
        """
        list_y = self.history_rect.y + 120
        recent_planets = self.planet_system.get_visible_planets()[-5:]  # Últimos 5
        
        for i, planet in enumerate(recent_planets):
            if list_y + (i * 25) < self.history_rect.bottom - 20:
                planet_info = f"{planet.donor_name}: {planet.total_value} coins"
                planet_surface = self.font_small.render(planet_info, True, self.text_color)
                self.surface.blit(planet_surface, (self.history_rect.x + 5, list_y + (i * 25)))
    
    def handle_event(self, event: pygame.event.Event):
        """
        Maneja eventos del panel de control
        
        Futuros eventos:
        - Drag & drop para reordenar
        - Atajos de teclado
        - Gestos de mouse
        """
        if event.type == pygame.KEYDOWN:
            self._handle_keyboard_input(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
    
    def _handle_keyboard_input(self, event: pygame.event.Event):
        """
        Maneja entrada de teclado para campos de texto
        
        Futuras mejoras:
        - Navegación con Tab entre campos
        - Autocompletado con teclas de flecha
        - Validación en tiempo real
        """
        if event.key == pygame.K_RETURN:
            if self._can_submit():
                self._submit_donation()
        elif event.key == pygame.K_BACKSPACE:
            if self.input_active:
                self.input_donor_name = self.input_donor_name[:-1]
        else:
            if self.input_active and event.unicode.isprintable():
                self.input_donor_name += event.unicode
    
    def _handle_mouse_click(self, event: pygame.event.Event):
        """
        Maneja clicks del mouse en elementos del panel
        
        Futuros elementos interactivos:
        - Dropdown para selección de regalos
        - Botones de preset de valores
        - Lista de donadores recientes clickeable
        """
        mouse_pos = event.pos
        # Ajustar posición relativa al panel (asumiendo que está en x=800)
        relative_pos = (mouse_pos[0] - 800, mouse_pos[1])
        
        if self.donor_input_rect.collidepoint(relative_pos):
            self.input_active = True
        elif self.submit_button_rect.collidepoint(relative_pos):
            if self._can_submit():
                self._submit_donation()
        else:
            self.input_active = False
    
    def _can_submit(self) -> bool:
        """Verifica si se puede enviar una donación"""
        return len(self.input_donor_name.strip()) > 0
    
    def _submit_donation(self):
        """
        Envía una nueva donación al sistema
        
        Futuras validaciones:
        - Verificar formato de nombre
        - Validar valor personalizado
        - Confirmar donaciones muy grandes
        """
        custom_val = None
        if self.custom_value.strip() and self.custom_value.strip().isdigit():
            custom_val = int(self.custom_value.strip())
        
        self.pending_donation_data = {
            "donor_name": self.input_donor_name.strip(),
            "gift_type": self.selected_gift,
            "custom_value": custom_val
        }
        self.new_donation_pending = True
        
        # Limpiar campos después del envío
        self.input_donor_name = ""
        self.custom_value = ""
        self.input_active = False
    
    def has_new_donation(self) -> bool:
        """Verifica si hay una nueva donación pendiente"""
        return self.new_donation_pending
    
    def get_new_donation(self) -> Dict:
        """Retorna y limpia la donación pendiente"""
        donation_data = self.pending_donation_data
        self.new_donation_pending = False
        self.pending_donation_data = None
        return donation_data
