# Control Panel - Panel de control para el streamer (VERSIÓN CORREGIDA)
# Interfaz para ingresar donaciones manualmente durante el live

import pygame
import pygame_gui
from typing import Dict, Optional, List
from enum import Enum

class InputField:
    """Clase para manejar campos de entrada individuales"""
    def __init__(self, name: str, rect: pygame.Rect, field_type: str = "text"):
        self.name = name
        self.rect = rect
        self.field_type = field_type  # "text", "select", "number"
        self.value = ""
        self.is_active = False
        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_timer = 0
        
        # Para campos de selección
        self.options = []
        self.selected_index = 0
        self.dropdown_open = False

class ControlPanel:
    """
    Panel de control para que el streamer gestione donaciones manualmente
    CON SISTEMA DE ENTRADA COMPLETAMENTE FUNCIONAL
    """
    
    def __init__(self, planet_system, panel_width: int, panel_height: int):

          # Opciones de regalos
        self.gift_options = [
            ("Rosa", "rose", 1),
            ("Perfume", "perfume", 5),
            ("Corazón", "finger_heart", 5),
            ("Vara Luminosa", "glow_stick", 10),
            ("Helado", "ice_cream", 15),
            ("Heart Me", "heart_me", 25),
            ("Pastel", "birthday_cake", 50),
            ("Motocicleta", "motorcycle", 100),
            ("Auto Deportivo", "sports_car", 500),
            ("Yate", "yacht", 1000),
            ("Cohete", "rocket", 2000),
            ("Castillo", "castle", 5000)
        ]
        

        self.planet_system = planet_system
        self.width = panel_width
        self.height = panel_height
        self.surface = pygame.Surface((self.width, self.height))
        
        # Estado del panel
        self.new_donation_pending = False
        self.pending_donation_data: Optional[Dict] = None
        
        # Fuentes
        self.font_large = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 20)
        self.font_small = pygame.font.Font(None, 16)
        
        # Colores
        self.bg_color = (40, 40, 50)
        self.button_color = (70, 70, 90)
        self.button_hover_color = (90, 90, 110)
        self.text_color = (255, 255, 255)
        self.input_color = (60, 60, 80)
        self.input_active_color = (80, 120, 160)  # Color cuando está activo
        self.input_border_color = (120, 120, 140)
        self.input_active_border_color = (160, 200, 255)  # Borde cuando está activo
        
        # Configurar campos de entrada
        self.setup_input_fields()
        
        # Estado de entrada
        self.active_field = None
        self.cursor_blink_timer = 0
        
      
        self.setup_layout()
    
    def setup_input_fields(self):
        """Configura todos los campos de entrada"""
        self.input_fields = {
            "donor_name": InputField("donor_name", pygame.Rect(10, 60, self.width - 20, 30), "text"),
            "gift_type": InputField("gift_type", pygame.Rect(10, 110, self.width - 20, 30), "select"),
            "custom_value": InputField("custom_value", pygame.Rect(10, 160, self.width - 20, 30), "number")
        }
        
        # Configurar opciones para el selector de regalos
        self.input_fields["gift_type"].options = [gift[0] for gift in self.gift_options]
        self.input_fields["gift_type"].value = self.gift_options[0][0]
    
    def setup_layout(self):
        """Configura el layout del panel de control"""
        self.title_rect = pygame.Rect(10, 10, self.width - 20, 30)
        self.submit_button_rect = pygame.Rect(10, 210, self.width - 20, 40)
        self.quick_buttons_rect = pygame.Rect(10, 260, self.width - 20, 30)
        self.history_rect = pygame.Rect(10, 300, self.width - 20, self.height - 310)
    
    def update(self, delta_time: int):
        """Actualiza el estado del panel de control"""
        # Actualizar cursor parpadeante
        self.cursor_blink_timer += delta_time
        if self.cursor_blink_timer >= 500:  # Parpadear cada 500ms
            self.cursor_blink_timer = 0
            if self.active_field:
                self.input_fields[self.active_field].cursor_visible = not self.input_fields[self.active_field].cursor_visible
    
    def render(self) -> pygame.Surface:
        """Renderiza el panel de control completo"""
        # Limpiar superficie
        self.surface.fill(self.bg_color)
        
        # Título
        self._render_title()
        
        # Campos de entrada
        self._render_input_fields()
        
        # Botones
        self._render_buttons()
        
        # Botones rápidos
        self._render_quick_buttons()
        
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
        """Renderiza todos los campos de entrada con indicadores visuales"""
        # Campo nombre del donador
        self._render_single_field("donor_name", "Nombre del donador:")
        
        # Campo tipo de regalo
        self._render_single_field("gift_type", "Tipo de regalo:")
        
        # Campo valor personalizado
        self._render_single_field("custom_value", "Valor personalizado (opcional):")
    
    def _render_single_field(self, field_name: str, label: str):
        """Renderiza un campo individual con su label"""
        field = self.input_fields[field_name]
        
        # Determinar colores según estado
        bg_color = self.input_active_color if field.is_active else self.input_color
        border_color = self.input_active_border_color if field.is_active else self.input_border_color
        border_width = 3 if field.is_active else 2
        
        # Renderizar label
        label_surface = self.font_medium.render(label, True, self.text_color)
        self.surface.blit(label_surface, (field.rect.x, field.rect.y - 25))
        
        # Renderizar campo
        pygame.draw.rect(self.surface, bg_color, field.rect)
        pygame.draw.rect(self.surface, border_color, field.rect, border_width)
        
        # Renderizar texto
        display_text = field.value
        if field.field_type == "select" and field.dropdown_open:
            display_text += " ▼"
        elif field.field_type == "select":
            display_text += " ▽"
        
        text_surface = self.font_medium.render(display_text, True, self.text_color)
        text_x = field.rect.x + 5
        text_y = field.rect.y + (field.rect.height - text_surface.get_height()) // 2
        self.surface.blit(text_surface, (text_x, text_y))
        
        # Renderizar cursor si está activo
        if field.is_active and field.cursor_visible and field.field_type != "select":
            cursor_x = text_x + text_surface.get_width() + 2
            cursor_y = field.rect.y + 5
            pygame.draw.line(self.surface, self.text_color, 
                           (cursor_x, cursor_y), (cursor_x, cursor_y + 20), 2)
        
        # Renderizar dropdown si está abierto
        if field.field_type == "select" and field.dropdown_open:
            self._render_dropdown(field)
    
    def _render_dropdown(self, field: InputField):
        """Renderiza el dropdown del selector de regalos"""
        dropdown_height = min(len(field.options) * 25, 200)
        dropdown_rect = pygame.Rect(field.rect.x, field.rect.bottom, field.rect.width, dropdown_height)
        
        # Fondo del dropdown
        pygame.draw.rect(self.surface, (50, 50, 60), dropdown_rect)
        pygame.draw.rect(self.surface, self.input_border_color, dropdown_rect, 2)
        
        # Opciones
        for i, option in enumerate(field.options[:8]):  # Mostrar máximo 8 opciones
            option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.y + i * 25, dropdown_rect.width, 25)
            
            # Highlight si está seleccionado
            if i == field.selected_index:
                pygame.draw.rect(self.surface, (80, 120, 160), option_rect)
            
            # Texto de la opción
            option_text = self.font_small.render(option, True, self.text_color)
            text_x = option_rect.x + 5
            text_y = option_rect.y + (option_rect.height - option_text.get_height()) // 2
            self.surface.blit(option_text, (text_x, text_y))
    
    def _render_buttons(self):
        """Renderiza botones de acción"""
        # Botón principal de envío
        button_color = self.button_hover_color if self._can_submit() else self.button_color
        pygame.draw.rect(self.surface, button_color, self.submit_button_rect)
        pygame.draw.rect(self.surface, self.text_color, self.submit_button_rect, 2)
        
        button_text = "Crear/Actualizar Planeta"
        text_surface = self.font_medium.render(button_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.submit_button_rect.center)
        self.surface.blit(text_surface, text_rect)
    
    def _render_quick_buttons(self):
        """Renderiza botones de acceso rápido para regalos comunes"""
        quick_gifts = [("Rosa (1)", 0), ("Corazón (5)", 2), ("Auto (500)", 8)]
        button_width = (self.width - 40) // 3
        button_height = 25
        
        for i, (name, gift_index) in enumerate(quick_gifts):
            x_pos = 10 + i * (button_width + 10)
            button_rect = pygame.Rect(x_pos, self.quick_buttons_rect.y, button_width, button_height)
            
            pygame.draw.rect(self.surface, self.button_color, button_rect)
            pygame.draw.rect(self.surface, self.text_color, button_rect, 1)
            
            text_surface = self.font_small.render(name, True, self.text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.surface.blit(text_surface, text_rect)
    
    def _render_history_panel(self):
        """Renderiza panel de historial y estadísticas"""
        # Marco del panel
        pygame.draw.rect(self.surface, (35, 35, 45), self.history_rect)
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
        
        # Lista de planetas recientes
        self._render_recent_planets_list()
    
    def _render_recent_planets_list(self):
        """Renderiza lista de planetas más recientes"""
        list_y = self.history_rect.y + 120
        recent_planets = self.planet_system.get_visible_planets()[-5:]  # Últimos 5
        
        for i, planet in enumerate(recent_planets):
            if list_y + (i * 25) < self.history_rect.bottom - 20:
                planet_info = f"{planet.donor_name}: {planet.total_value} coins ({planet.planet_type.value})"
                planet_surface = self.font_small.render(planet_info[:40] + "..." if len(planet_info) > 40 else planet_info, True, self.text_color)
                self.surface.blit(planet_surface, (self.history_rect.x + 5, list_y + (i * 25)))
    
    def handle_event(self, event: pygame.event.Event):
        """Maneja eventos del panel de control"""
        if event.type == pygame.KEYDOWN:
            self._handle_keyboard_input(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
    
    def _handle_keyboard_input(self, event: pygame.event.Event):
        """Maneja entrada de teclado para campos de texto"""
        if not self.active_field:
            return
        
        active_field_obj = self.input_fields[self.active_field]
        
        if event.key == pygame.K_RETURN:
            if self._can_submit():
                self._submit_donation()
            return
        elif event.key == pygame.K_TAB:
            self._cycle_active_field()
            return
        elif event.key == pygame.K_ESCAPE:
            self._deactivate_all_fields()
            return
        
        # Manejar entrada específica por tipo de campo
        if active_field_obj.field_type == "select":
            self._handle_select_input(event, active_field_obj)
        elif active_field_obj.field_type == "text":
            self._handle_text_input(event, active_field_obj)
        elif active_field_obj.field_type == "number":
            self._handle_number_input(event, active_field_obj)
    
    def _handle_text_input(self, event: pygame.event.Event, field: InputField):
        """Maneja entrada de texto normal"""
        if event.key == pygame.K_BACKSPACE:
            field.value = field.value[:-1]
        elif event.unicode.isprintable() and len(field.value) < 30:
            field.value += event.unicode
    
    def _handle_number_input(self, event: pygame.event.Event, field: InputField):
        """Maneja entrada de números"""
        if event.key == pygame.K_BACKSPACE:
            field.value = field.value[:-1]
        elif event.unicode.isdigit() and len(field.value) < 10:
            field.value += event.unicode
    
    def _handle_select_input(self, event: pygame.event.Event, field: InputField):
        """Maneja entrada para campos de selección"""
        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
            field.dropdown_open = not field.dropdown_open
        elif event.key == pygame.K_UP and field.dropdown_open:
            field.selected_index = max(0, field.selected_index - 1)
            field.value = field.options[field.selected_index]
        elif event.key == pygame.K_DOWN and field.dropdown_open:
            field.selected_index = min(len(field.options) - 1, field.selected_index + 1)
            field.value = field.options[field.selected_index]
    
    def _handle_mouse_click(self, event: pygame.event.Event):
        """Maneja clicks del mouse en elementos del panel"""
        mouse_pos = event.pos
        # Ajustar posición relativa al panel (asumiendo que está en x=800)
        relative_pos = (mouse_pos[0] - 800, mouse_pos[1])
        
        # Verificar click en campos de entrada
        clicked_field = None
        for field_name, field in self.input_fields.items():
            if field.rect.collidepoint(relative_pos):
                clicked_field = field_name
                break
        
        if clicked_field:
            self._activate_field(clicked_field)
        elif self.submit_button_rect.collidepoint(relative_pos):
            if self._can_submit():
                self._submit_donation()
        else:
            # Click en botones rápidos
            self._check_quick_button_click(relative_pos)
            # Desactivar campos si click fuera
            self._deactivate_all_fields()
    
    def _check_quick_button_click(self, pos):
        """Verifica click en botones rápidos"""
        quick_gifts = [("Rosa (1)", 0), ("Corazón (5)", 2), ("Auto (500)", 8)]
        button_width = (self.width - 40) // 3
        button_height = 25
        
        for i, (name, gift_index) in enumerate(quick_gifts):
            x_pos = 10 + i * (button_width + 10)
            button_rect = pygame.Rect(x_pos, self.quick_buttons_rect.y, button_width, button_height)
            
            if button_rect.collidepoint(pos):
                # Aplicar regalo rápido
                self.input_fields["gift_type"].value = self.gift_options[gift_index][0]
                self.input_fields["gift_type"].selected_index = gift_index
                break
    
    def _activate_field(self, field_name: str):
        """Activa un campo específico"""
        # Desactivar todos los campos
        for field in self.input_fields.values():
            field.is_active = False
            field.dropdown_open = False
        
        # Activar el campo seleccionado
        self.active_field = field_name
        self.input_fields[field_name].is_active = True
        self.input_fields[field_name].cursor_visible = True
    
    def _deactivate_all_fields(self):
        """Desactiva todos los campos"""
        self.active_field = None
        for field in self.input_fields.values():
            field.is_active = False
            field.dropdown_open = False
    
    def _cycle_active_field(self):
        """Cicla entre los campos con Tab"""
        field_names = list(self.input_fields.keys())
        if not self.active_field:
            self._activate_field(field_names[0])
        else:
            current_index = field_names.index(self.active_field)
            next_index = (current_index + 1) % len(field_names)
            self._activate_field(field_names[next_index])
    
    def _can_submit(self) -> bool:
        """Verifica si se puede enviar una donación"""
        return len(self.input_fields["donor_name"].value.strip()) > 0
    
    def _submit_donation(self):
        """Envía una nueva donación al sistema"""
        donor_name = self.input_fields["donor_name"].value.strip()
        selected_gift_name = self.input_fields["gift_type"].value
        custom_value_str = self.input_fields["custom_value"].value.strip()
        
        # Encontrar el regalo seleccionado
        selected_gift = None
        for gift in self.gift_options:
            if gift[0] == selected_gift_name:
                selected_gift = gift
                break
        
        if not selected_gift:
            selected_gift = self.gift_options[0]  # Default a rosa
        
        # Usar valor personalizado si se proporcionó
        custom_val = None
        if custom_value_str and custom_value_str.isdigit():
            custom_val = int(custom_value_str)
        
        self.pending_donation_data = {
            "donor_name": donor_name,
            "gift_type": selected_gift[1],  # El código interno del regalo
            "custom_value": custom_val
        }
        self.new_donation_pending = True
        
        # Limpiar campos después del envío
        self.input_fields["donor_name"].value = ""
        self.input_fields["custom_value"].value = ""
        self._deactivate_all_fields()
    
    def has_new_donation(self) -> bool:
        """Verifica si hay una nueva donación pendiente"""
        return self.new_donation_pending
    
    def get_new_donation(self) -> Dict:
        """Retorna y limpia la donación pendiente"""
        donation_data = self.pending_donation_data
        self.new_donation_pending = False
        self.pending_donation_data = None
        return donation_data