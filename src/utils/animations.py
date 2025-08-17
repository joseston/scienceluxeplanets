# Animation Utilities - Funciones para animaciones y efectos visuales
# Proporciona herramientas para crear transiciones y efectos suaves

import math
import pygame
from typing import Tuple, Callable

class AnimationEasing:
    """
    Funciones de easing para animaciones suaves
    
    Futuras funciones de easing:
    - Elastic (rebote)
    - Bounce (pelota que rebota)
    - Back (sobrepasa y regresa)
    - Cubic-bezier personalizada
    """
    
    @staticmethod
    def linear(t: float) -> float:
        """Interpolación lineal simple"""
        return t
    
    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Entrada suave cuadrática"""
        return t * t
    
    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Salida suave cuadrática"""
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Entrada y salida suave cuadrática"""
        return 2 * t * t if t < 0.5 else 1 - 2 * (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Entrada suave cúbica"""
        return t * t * t
    
    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Salida suave cúbica"""
        return 1 - math.pow(1 - t, 3)

class Animator:
    """
    Clase para gestionar animaciones de objetos
    
    Futuras mejoras:
    - Animaciones en cadena (sequences)
    - Animaciones simultáneas (parallel)
    - Callbacks de inicio/fin de animación
    - Pausa y reanudación de animaciones
    - Animaciones basadas en física
    """
    
    def __init__(self):
        self.animations = []
    
    def animate_value(self, start_value: float, end_value: float, 
                     duration: float, easing: Callable = AnimationEasing.linear) -> 'ValueAnimation':
        """
        Crea una animación de valor numérico
        
        Futuras animaciones:
        - Animación de colores (RGB)
        - Animación de vectores 2D/3D
        - Animación de transformaciones
        """
        animation = ValueAnimation(start_value, end_value, duration, easing)
        self.animations.append(animation)
        return animation
    
    def animate_position(self, start_pos: Tuple[float, float], 
                        end_pos: Tuple[float, float], duration: float,
                        easing: Callable = AnimationEasing.ease_out_quad) -> 'PositionAnimation':
        """
        Crea una animación de posición 2D
        
        Futuras animaciones de posición:
        - Trayectorias curvas (bezier)
        - Animación orbital
        - Seguimiento de caminos personalizados
        """
        animation = PositionAnimation(start_pos, end_pos, duration, easing)
        self.animations.append(animation)
        return animation
    
    def update(self, delta_time: float):
        """
        Actualiza todas las animaciones activas
        
        Futuras optimizaciones:
        - Pool de objetos para evitar garbage collection
        - Priorización de animaciones visibles
        - Interpolación temporal adaptativa
        """
        # Actualizar animaciones activas
        for animation in self.animations[:]:  # Copia para modificar durante iteración
            animation.update(delta_time)
            if animation.is_finished():
                self.animations.remove(animation)
    
    def clear_animations(self):
        """Limpia todas las animaciones activas"""
        self.animations.clear()

class ValueAnimation:
    """
    Animación de un valor numérico simple
    
    Futuras mejoras:
    - Interpolación de enteros vs flotantes
    - Callbacks de actualización
    - Reversa automática (ping-pong)
    """
    
    def __init__(self, start_value: float, end_value: float, 
                 duration: float, easing: Callable):
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.easing = easing
        self.elapsed_time = 0.0
        self.current_value = start_value
        self.finished = False
    
    def update(self, delta_time: float):
        """Actualiza la animación"""
        if self.finished:
            return
        
        self.elapsed_time += delta_time
        
        if self.elapsed_time >= self.duration:
            self.current_value = self.end_value
            self.finished = True
        else:
            t = self.elapsed_time / self.duration
            eased_t = self.easing(t)
            self.current_value = self.start_value + (self.end_value - self.start_value) * eased_t
    
    def get_value(self) -> float:
        """Retorna el valor actual de la animación"""
        return self.current_value
    
    def is_finished(self) -> bool:
        """Verifica si la animación ha terminado"""
        return self.finished

class PositionAnimation:
    """
    Animación de posición 2D
    
    Futuras mejoras:
    - Rotación durante movimiento
    - Efectos de trail/estela
    - Colisión durante animación
    """
    
    def __init__(self, start_pos: Tuple[float, float], 
                 end_pos: Tuple[float, float], duration: float, easing: Callable):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.easing = easing
        self.elapsed_time = 0.0
        self.current_pos = start_pos
        self.finished = False
    
    def update(self, delta_time: float):
        """Actualiza la animación de posición"""
        if self.finished:
            return
        
        self.elapsed_time += delta_time
        
        if self.elapsed_time >= self.duration:
            self.current_pos = self.end_pos
            self.finished = True
        else:
            t = self.elapsed_time / self.duration
            eased_t = self.easing(t)
            
            x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * eased_t
            y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * eased_t
            self.current_pos = (x, y)
    
    def get_position(self) -> Tuple[float, float]:
        """Retorna la posición actual"""
        return self.current_pos
    
    def is_finished(self) -> bool:
        """Verifica si la animación ha terminado"""
        return self.finished

class ParticleSystem:
    """
    Sistema básico de partículas para efectos visuales
    
    Futuras mejoras:
    - Diferentes tipos de partículas (fuego, humo, estrellas)
    - Física de partículas (gravedad, viento)
    - Texturas personalizadas para partículas
    - Emisores con formas específicas
    - Colisiones de partículas
    """
    
    def __init__(self, max_particles: int = 100):
        self.max_particles = max_particles
        self.particles = []
    
    def emit_burst(self, position: Tuple[float, float], count: int, 
                  speed_range: Tuple[float, float] = (50, 150),
                  color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Emite una ráfaga de partículas desde una posición
        
        Futuras configuraciones:
        - Dirección preferencial de emisión
        - Variación de tamaño de partículas
        - Tiempo de vida variable
        - Efectos de fade out
        """
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            
            # Ángulo aleatorio
            angle = math.radians(math.random() * 360)
            speed = speed_range[0] + math.random() * (speed_range[1] - speed_range[0])
            
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            particle = {
                'x': position[0],
                'y': position[1],
                'vx': velocity_x,
                'vy': velocity_y,
                'life': 1.0,
                'max_life': 1.0 + math.random() * 2.0,
                'color': color,
                'size': 2 + math.random() * 3
            }
            self.particles.append(particle)
    
    def update(self, delta_time: float):
        """
        Actualiza todas las partículas del sistema
        
        Futuras físicas:
        - Gravedad aplicada a partículas
        - Resistencia del aire
        - Fuerzas externas (viento, magnetismo)
        """
        for particle in self.particles[:]:
            # Actualizar posición
            particle['x'] += particle['vx'] * delta_time
            particle['y'] += particle['vy'] * delta_time
            
            # Actualizar tiempo de vida
            particle['life'] -= delta_time
            
            # Remover partículas muertas
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def render(self, surface: pygame.Surface):
        """
        Renderiza todas las partículas en la superficie
        
        Futuras mejoras de rendering:
        - Blending modes (additive, multiply)
        - Sprites personalizados
        - Efectos de blur
        """
        for particle in self.particles:
            # Calcular alpha basado en tiempo de vida
            alpha = int(255 * (particle['life'] / particle['max_life']))
            alpha = max(0, min(255, alpha))
            
            # Crear superficie con alpha
            particle_surface = pygame.Surface((int(particle['size']) * 2, int(particle['size']) * 2), pygame.SRCALPHA)
            color_with_alpha = (*particle['color'], alpha)
            pygame.draw.circle(particle_surface, color_with_alpha, 
                             (int(particle['size']), int(particle['size'])), 
                             int(particle['size']))
            
            # Dibujar en superficie principal
            surface.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
    
    def clear(self):
        """Limpia todas las partículas"""
        self.particles.clear()
