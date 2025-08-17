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
        # DIMENSIONES ORIGINALES para referencia de posicionamiento
        self.screen_width = panel_width  
        self.screen_height = panel_height
        
        # SUPERFICIE PEQUEÑA solo para el overlay - RESPONSIVE
        self.overlay_width = 150   # Tamaño real del overlay
        self.overlay_height = 100  # Tamaño real del overlay
        
        # Posición RESPONSIVE - calculada según tamaño de pantalla
        # Posicionar en la esquina superior derecha con margen
        margin_x = 20
        margin_y = 60
        self.overlay_x = self.screen_width - self.overlay_width - margin_x
        self.overlay_y = margin_y
        
        # Superficie PEQUEÑA con transparencia
        self.surface = pygame.Surface((self.overlay_width, self.overlay_height), pygame.SRCALPHA)
        
        # Estado del panel
        self.new_donation_pending = False
        self.pending_donation_data: Optional[Dict] = None
        
        # Fuentes MUY PEQUEÑAS para overlay compacto
        self.font_large = pygame.font.Font(None, 16)   # Muy reducido
        self.font_medium = pygame.font.Font(None, 14)  # Muy reducido
        self.font_small = pygame.font.Font(None, 12)   # Muy reducido
        
        # Colores optimizados para contraste en móvil
        self.bg_color = (25, 25, 35)  # Más oscuro
        self.button_color = (60, 60, 80)
        self.button_hover_color = (80, 80, 100)
        self.text_color = (255, 255, 255)
        self.input_color = (45, 45, 65)
        self.input_active_color = (60, 100, 140)
        self.input_border_color = (100, 100, 120)
        self.input_active_border_color = (140, 180, 220)
        
        # Configurar campos de entrada para LAYOUT OVERLAY EN ZONA LIBRE
        self.setup_overlay_layout()
        
        # Estado de entrada
        self.active_field = None
        self.cursor_blink_timer = 0
        
        # Configurar layout overlay (NO el layout viejo)
        self.setup_overlay_layout()
        
    def setup_overlay_layout(self):
        """
        Configura layout overlay COMPACTO - coordenadas relativas al overlay
        """
        # Posiciones RELATIVAS al overlay pequeño (0,0 = esquina overlay)
        start_x = 5    # Padding interno del overlay
        start_y = 5    # Padding interno del overlay
        control_width = self.overlay_width - 10   # Ancho menos padding
        control_height = 18   # Altura de campos
        spacing = 4           # Espacio entre campos
        
        # Solo 3 campos: nombre, valor y botón (eliminamos tipo de regalo)
        self.input_fields = {
            "donor_name": InputField("donor_name", 
                                   pygame.Rect(start_x, start_y, control_width, control_height), "text"),
            "custom_value": InputField("custom_value", 
                                     pygame.Rect(start_x, start_y + control_height + spacing, 
                                               control_width, control_height), "number")
        }
        
        # Botón crear/actualizar - más pequeño
        self.submit_button_rect = pygame.Rect(start_x, start_y + (control_height + spacing) * 2,
                                            control_width, control_height + 4)
        
    def setup_input_fields_horizontal(self):
        """
        Configura campos de entrada en LAYOUT HORIZONTAL para panel inferior
        Optimizado para pantalla vertical de TikTok
        """
        # Calculamos anchos para 3 columnas principales + botón
        field_width = (self.width - 60) // 4  # 4 elementos con espacios
        button_width = field_width
        margin = 10
        y_pos = 30  # Una sola fila
        
        self.input_fields = {
            "donor_name": InputField("donor_name", 
                                   pygame.Rect(margin, y_pos, field_width, 35), "text"),
            "gift_type": InputField("gift_type", 
                                  pygame.Rect(margin + field_width + 10, y_pos, field_width, 35), "select"),
            "custom_value": InputField("custom_value", 
                                     pygame.Rect(margin + (field_width + 10) * 2, y_pos, field_width, 35), "number")
        }
        
        # Configurar opciones para el selector de regalos
        self.input_fields["gift_type"].options = [gift[0] for gift in self.gift_options]
        self.input_fields["gift_type"].value = self.gift_options[0][0]
        
        # Botón de envío en la misma fila
        self.submit_button_rect = pygame.Rect(margin + (field_width + 10) * 3, y_pos, button_width, 35)
        
        # Layout horizontal compacto
        self.setup_layout_horizontal()
        
    def setup_layout_horizontal(self):
        """Configura el layout HORIZONTAL COMPACTO para panel inferior"""
        self.title_rect = pygame.Rect(10, 5, self.width - 20, 20)  # Título más pequeño
        
        # ELIMINAMOS el área de estadísticas como solicitas
        # self.history_rect = None  # Comentado
    
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
    
    # MÉTODO COMENTADO - NO SE USA EN OVERLAY
    # def setup_layout(self):
    #     """Configura el layout del panel de control"""
    #     self.title_rect = pygame.Rect(10, 10, self.width - 20, 30)
    #     self.submit_button_rect = pygame.Rect(10, 210, self.width - 20, 40)
    #     self.quick_buttons_rect = pygame.Rect(10, 260, self.width - 20, 30)
    #     self.history_rect = pygame.Rect(10, 300, self.width - 20, self.height - 310)
    
    def update(self, delta_time: int):
        """Actualiza el estado del panel de control"""
        # Actualizar cursor parpadeante
        self.cursor_blink_timer += delta_time
        if self.cursor_blink_timer >= 500:  # Parpadear cada 500ms
            self.cursor_blink_timer = 0
            if self.active_field:
                self.input_fields[self.active_field].cursor_visible = not self.input_fields[self.active_field].cursor_visible
    
    def render(self) -> pygame.Surface:
        """Renderiza controles overlay en zona libre - SIN panel inferior"""
        # Limpiar superficie como transparente/invisible
        self.surface.fill((0, 0, 0, 0))  # Completamente transparente
        
        # Renderizar controles overlay en zona libre
        self._render_overlay_controls()
        
        return self.surface
    
    def _render_overlay_controls(self):
        """Renderiza controles compactos en zona libre (overlay)"""
        # Campo nombre del donador
        field = self.input_fields["donor_name"]
        self._render_overlay_field(field, "Nombre:")
        
        # Campo valor personalizado  
        field = self.input_fields["custom_value"]
        self._render_overlay_field(field, "Coins:")
        
        # Botón crear/actualizar
        self._render_overlay_button()
    
    def _render_overlay_field(self, field: 'InputField', label: str):
        """Renderiza un campo individual en el overlay - COMPACTO"""
        # Fondo semi-transparente más pequeño
        overlay_bg = pygame.Surface((field.rect.width, field.rect.height))
        overlay_bg.set_alpha(180)
        overlay_bg.fill((40, 40, 60))
        self.surface.blit(overlay_bg, field.rect)
        
        # Borde más fino
        border_color = (100, 150, 200) if field.is_active else (80, 80, 100)
        pygame.draw.rect(self.surface, border_color, field.rect, 1)
        
        # Label MUY compacto arriba del campo
        label_surface = self.font_small.render(label, True, (180, 180, 180))
        label_y = field.rect.y - 14  # Más cerca del campo
        self.surface.blit(label_surface, (field.rect.x, label_y))
        
        # Texto del campo más pequeño
        text_surface = self.font_small.render(field.value, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.left = field.rect.x + 3  # Menos padding
        text_rect.centery = field.rect.centery
        self.surface.blit(text_surface, text_rect)
        
        # Cursor parpadeante si está activo
        if field.is_active and field.cursor_visible:
            cursor_x = text_rect.right + 2
            cursor_y1 = field.rect.y + 5
            cursor_y2 = field.rect.bottom - 5
            pygame.draw.line(self.surface, (255, 255, 255), (cursor_x, cursor_y1), (cursor_x, cursor_y2), 1)
    
    def _render_overlay_button(self):
        """Renderiza el botón en el overlay - COMPACTO"""
        # Verificar si se puede enviar
        can_submit = self._can_submit_overlay()
        button_color = (60, 120, 180) if can_submit else (60, 60, 80)
        
        # Fondo del botón más transparente
        overlay_bg = pygame.Surface((self.submit_button_rect.width, self.submit_button_rect.height))
        overlay_bg.set_alpha(200)
        overlay_bg.fill(button_color)
        self.surface.blit(overlay_bg, self.submit_button_rect)
        
        # Borde más fino
        pygame.draw.rect(self.surface, (150, 150, 150), self.submit_button_rect, 1)
        
        # Texto del botón más pequeño
        button_text = "Crear"  # Texto más corto
        text_surface = self.font_small.render(button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.submit_button_rect.center)
        self.surface.blit(text_surface, text_rect)
    
    def _can_submit_overlay(self) -> bool:
        """Verifica si se puede enviar con los campos overlay"""
        donor_name = self.input_fields["donor_name"].value.strip()
        return len(donor_name) > 0
        
        # Campos de entrada en horizontal
        self._render_input_fields()
        
        # Botón de envío (ya está en la misma fila)
        self._render_buttons()
        
        # ELIMINADO: Botones rápidos (comentar si se necesitan después)
        # self._render_quick_buttons()
        
        # ELIMINADO: Historial/estadísticas (como solicitaste)
        # self._render_history_panel()
        
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
        """Maneja eventos del panel de control overlay"""
        if event.type == pygame.KEYDOWN:
            self._handle_keyboard_input_overlay(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click_overlay(event)
    
    def _handle_mouse_click_overlay(self, event: pygame.event.Event):
        """Maneja clicks del mouse en controles overlay - COORDENADAS AJUSTADAS"""
        mouse_pos = event.pos
        
        # Ajustar coordenadas del mouse relativas al overlay
        relative_mouse_x = mouse_pos[0] - self.overlay_x
        relative_mouse_y = mouse_pos[1] - self.overlay_y
        relative_pos = (relative_mouse_x, relative_mouse_y)
        
        # Verificar si el click está dentro del área del overlay
        if (0 <= relative_mouse_x <= self.overlay_width and 
            0 <= relative_mouse_y <= self.overlay_height):
            
            # Verificar click en campos de entrada
            for field_name, field in self.input_fields.items():
                if field.rect.collidepoint(relative_pos):
                    self._activate_field(field_name)
                    return
            
            # Verificar click en botón
            if self.submit_button_rect.collidepoint(relative_pos):
                if self._can_submit_overlay():
                    self._submit_donation_overlay()
                return
        
        # Click fuera del overlay - desactivar campos
        self._deactivate_all_fields()
    
    def _handle_keyboard_input_overlay(self, event: pygame.event.Event):
        """Maneja entrada de teclado para campos overlay"""
        if not self.active_field:
            return
        
        active_field_obj = self.input_fields[self.active_field]
        
        if event.key == pygame.K_RETURN:
            if self._can_submit_overlay():
                self._submit_donation_overlay()
            return
        elif event.key == pygame.K_TAB:
            self._cycle_active_field_overlay()
            return
        elif event.key == pygame.K_ESCAPE:
            self._deactivate_all_fields()
            return
        
        # Manejar entrada según tipo de campo
        if active_field_obj.field_type == "text":
            self._handle_text_input(event, active_field_obj)
        elif active_field_obj.field_type == "number":
            self._handle_number_input(event, active_field_obj)
    
    def _cycle_active_field_overlay(self):
        """Cicla entre campos en el overlay"""
        field_names = ["donor_name", "custom_value"]
        if self.active_field is None:
            self._activate_field(field_names[0])
        else:
            current_index = field_names.index(self.active_field)
            next_index = (current_index + 1) % len(field_names)
            self._activate_field(field_names[next_index])
    
    def _submit_donation_overlay(self):
        """Envía donación usando datos del overlay"""
        donor_name = self.input_fields["donor_name"].value.strip()
        custom_value_str = self.input_fields["custom_value"].value.strip()
        
        # Usar valor personalizado o valor por defecto (1 coin = rosa)
        custom_value = None
        if custom_value_str and custom_value_str.isdigit():
            custom_value = int(custom_value_str)
        
        self.pending_donation_data = {
            "donor_name": donor_name,
            "gift_type": "custom",  # Tipo genérico
            "custom_value": custom_value if custom_value else 1  # Default 1 coin
        }
        self.new_donation_pending = True
        
        # Limpiar campos después del envío
        self.input_fields["donor_name"].value = ""
        self.input_fields["custom_value"].value = ""
        self._deactivate_all_fields()
    
    def _activate_field(self, field_name: str):
        """Activa un campo específico"""
        # Desactivar todos los campos
        for field in self.input_fields.values():
            field.is_active = False
            field.cursor_visible = True
        
        # Activar el campo especificado
        if field_name in self.input_fields:
            self.input_fields[field_name].is_active = True
            self.active_field = field_name
    
    def _deactivate_all_fields(self):
        """Desactiva todos los campos"""
        for field in self.input_fields.values():
            field.is_active = False
        self.active_field = None
    
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
        """Maneja clicks del mouse en elementos del panel - LAYOUT HORIZONTAL INFERIOR"""
        mouse_pos = event.pos
        
        # Para layout vertical: el panel está en la parte inferior
        # Necesitamos calcular la posición relativa al panel de control
        planet_display_height = int(1280 * 0.7)  # 70% de la altura total
        relative_pos = (mouse_pos[0], mouse_pos[1] - planet_display_height)
        
        # Verificar que el click está dentro del área del panel
        if relative_pos[1] < 0 or relative_pos[1] > self.height:
            return
        
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
            # COMENTADO: Click en botones rápidos (eliminados por ahora)
            # self._check_quick_button_click(relative_pos)
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