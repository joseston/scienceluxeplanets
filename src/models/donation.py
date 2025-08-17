# Donation Model - Representa una donación individual
# Almacena información de cada regalo recibido durante el live

import datetime
from typing import Dict

class Donation:
    """
    Representa una donación individual recibida durante el stream
    
    Futuras expansiones:
    - Metadatos adicionales (país del donador, hora exacta)
    - Categorización por tipo de evento (donación regular, raid, etc.)
    - Integración con sistema de logros y recompensas
    - Tracking de donadores recurrentes
    """
    
    # Valores de conversión de regalos TikTok a coins
    # NOTA: Estos valores son preliminares y deben ajustarse según precios reales
    GIFT_VALUES = {
        "rose": 1,           # Rosa - regalo básico
        "perfume": 5,        # Perfume - regalo intermedio
        "finger_heart": 5,   # Corazón con dedos
        "glow_stick": 10,    # Vara luminosa
        "ice_cream": 15,     # Helado
        "heart_me": 25,      # Heart Me
        "birthday_cake": 50, # Pastel de cumpleaños
        "motorcycle": 100,   # Motocicleta
        "sports_car": 500,   # Auto deportivo
        "yacht": 1000,       # Yate
        "rocket": 2000,      # Cohete
        "castle": 5000       # Castillo
    }
    
    def __init__(self, donor_name: str, gift_type: str, custom_value: int = None):
        self.donor_name = donor_name
        self.gift_type = gift_type.lower()
        self.timestamp = datetime.datetime.now()
        
        # Usar valor personalizado o buscar en tabla de conversión
        if custom_value is not None:
            self.value = custom_value
        else:
            self.value = self.GIFT_VALUES.get(self.gift_type, 1)
        
        # Metadata futura
        self.session_id = None  # Para asociar con sesión específica
        self.is_first_donation = False  # Si es primera donación del usuario
    
    def get_display_name(self) -> str:
        """
        Retorna nombre formateado para mostrar en UI
        
        Futuras mejoras:
        - Emojis por tipo de regalo
        - Colores especiales para regalos caros
        - Animaciones especiales
        """
        return self.gift_type.replace("_", " ").title()
    
    def to_dict(self) -> Dict:
        """
        Convierte la donación a diccionario para almacenamiento
        
        Futuras adiciones:
        - Geolocalización del donador
        - Contexto del chat (mensaje asociado)
        - Información de la sesión
        """
        return {
            "donor_name": self.donor_name,
            "gift_type": self.gift_type,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "display_name": self.get_display_name()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Donation':
        """Crea una donación desde diccionario almacenado"""
        donation = cls(data["donor_name"], data["gift_type"], data["value"])
        donation.timestamp = datetime.datetime.fromisoformat(data["timestamp"])
        return donation
    
    @classmethod
    def get_available_gifts(cls) -> Dict[str, int]:
        """
        Retorna lista de regalos disponibles con sus valores
        
        Futuras mejoras:
        - Actualización automática desde API de TikTok
        - Regalos estacionales o especiales
        - Personalización por streamer
        """
        return cls.GIFT_VALUES.copy()
    
    def __str__(self) -> str:
        return f"{self.donor_name}: {self.get_display_name()} ({self.value} coins)"
    
    def __repr__(self) -> str:
        return f"Donation(donor='{self.donor_name}', gift='{self.gift_type}', value={self.value})"
