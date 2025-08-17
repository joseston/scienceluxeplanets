# Session Manager - Gestiona las sesiones de streaming
# Controla la creación, actualización y persistencia de sesiones

import sqlite3
import datetime
from typing import Optional
from ..database.database_manager import DatabaseManager

class SessionManager:
    """
    Gestiona las sesiones de streaming y coordina la base de datos
    
    Futuras implementaciones:
    - Guardar estadísticas de sesión
    - Exportar resumen de donaciones
    - Historial de sesiones anteriores
    - Integración con APIs de TikTok para métricas
    """
    
    def __init__(self):
        self.session_id: Optional[str] = None
        self.session_start_time: Optional[datetime.datetime] = None
        self.db_manager = DatabaseManager()
        self.create_new_session()
    
    def create_new_session(self) -> str:
        """
        Crea una nueva sesión de streaming
        """
        self.session_id = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_start_time = datetime.datetime.now()
        
        # Inicializar base de datos para la sesión
        self.db_manager.initialize_session_database(self.session_id)
        
        return self.session_id
    
    def get_session_stats(self) -> dict:
        """
        Obtiene estadísticas de la sesión actual
        
        Futuras métricas:
        - Total de donadores únicos
        - Valor total de donaciones
        - Planeta más grande
        - Tiempo de sesión activo
        """
        return {
            "session_id": self.session_id,
            "start_time": self.session_start_time,
            "total_planets": self.db_manager.get_planet_count(),
            "total_donations": self.db_manager.get_total_donation_value()
        }
    
    def close_session(self):
        """
        Cierra la sesión actual y libera recursos
        
        Futuras implementaciones:
        - Exportar resumen de sesión
        - Guardar screenshot final del universo
        - Generar reporte de donaciones
        """
        if self.db_manager:
            self.db_manager.close()
        
        self.session_id = None
        self.session_start_time = None
