# Database Manager - Gestión de base de datos SQLite
# Maneja la persistencia de planetas y donaciones por sesión

import sqlite3
import json
import datetime
from typing import List, Dict, Optional
from ..models.planet import Planet
from ..models.donation import Donation

class DatabaseManager:
    """
    Gestiona la base de datos SQLite para persistencia de sesiones
    
    Futuras mejoras:
    - Backup automático de sesiones
    - Migración de esquemas de base de datos
    - Exportación a formatos externos (CSV, JSON)
    - Índices para búsquedas rápidas en sesiones grandes
    - Compresión de datos para sesiones muy largas
    """
    
    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.current_session_id: Optional[str] = None
    
    def initialize_session_database(self, session_id: str):
        """
        Inicializa la base de datos para una nueva sesión
        
        Futuras tablas:
        - session_settings (configuración por sesión)
        - planet_interactions (historial de cambios)
        - performance_metrics (estadísticas de rendimiento)
        """
        self.current_session_id = session_id
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
        # Crear tablas si no existen
        self._create_tables()
    
    def _create_tables(self):
        """Crea las tablas necesarias en la base de datos"""
        cursor = self.connection.cursor()
        
        # Tabla de planetas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS planets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                donor_name TEXT NOT NULL,
                total_value INTEGER NOT NULL,
                planet_type TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                position_x INTEGER DEFAULT 0,
                position_y INTEGER DEFAULT 0,
                UNIQUE(session_id, donor_name)
            )
        """)
        
        # Tabla de donaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                donor_name TEXT NOT NULL,
                gift_type TEXT NOT NULL,
                value INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        
        # Tabla de sesiones (futura)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                start_time TEXT NOT NULL,
                end_time TEXT,
                total_donations INTEGER DEFAULT 0,
                total_value INTEGER DEFAULT 0,
                unique_donors INTEGER DEFAULT 0
            )
        """)
        
        self.connection.commit()
    
    def save_planet(self, planet: Planet) -> bool:
        """
        Guarda o actualiza un planeta en la base de datos
        
        Futuras mejoras:
        - Versionado de cambios de planetas
        - Triggers para actualizar estadísticas automáticamente
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO planets 
                (session_id, donor_name, total_value, planet_type, created_at, last_updated, position_x, position_y)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.current_session_id,
                planet.donor_name,
                planet.total_value,
                planet.planet_type.value,
                planet.created_at.isoformat(),
                planet.last_updated.isoformat(),
                planet.position_x,
                planet.position_y
            ))
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving planet: {e}")
            return False
    
    def save_donation(self, donation: Donation) -> bool:
        """
        Guarda una donación en la base de datos
        
        Futuras validaciones:
        - Prevenir donaciones duplicadas
        - Validar rangos de valores
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO donations 
                (session_id, donor_name, gift_type, value, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.current_session_id,
                donation.donor_name,
                donation.gift_type,
                donation.value,
                donation.timestamp.isoformat()
            ))
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving donation: {e}")
            return False
    
    def load_session_planets(self) -> List[Planet]:
        """
        Carga todos los planetas de la sesión actual
        
        Futuras optimizaciones:
        - Carga paginada para sesiones grandes
        - Cache en memoria para acceso rápido
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT * FROM planets 
                WHERE session_id = ? 
                ORDER BY last_updated DESC
            """, (self.current_session_id,))
            
            planets = []
            for row in cursor.fetchall():
                planet = Planet(row['donor_name'])
                planet.total_value = row['total_value']
                planet.planet_type = Planet.PlanetType(row['planet_type'])
                planet.created_at = datetime.datetime.fromisoformat(row['created_at'])
                planet.last_updated = datetime.datetime.fromisoformat(row['last_updated'])
                planet.position_x = row['position_x']
                planet.position_y = row['position_y']
                
                # Cargar historial de donaciones
                planet.donations_history = self.load_planet_donations(planet.donor_name)
                
                planets.append(planet)
            
            return planets
        except sqlite3.Error as e:
            print(f"Error loading planets: {e}")
            return []
    
    def load_planet_donations(self, donor_name: str) -> List[Donation]:
        """Carga todas las donaciones de un donador específico"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT * FROM donations 
                WHERE session_id = ? AND donor_name = ?
                ORDER BY timestamp ASC
            """, (self.current_session_id, donor_name))
            
            donations = []
            for row in cursor.fetchall():
                donation = Donation(row['donor_name'], row['gift_type'], row['value'])
                donation.timestamp = datetime.datetime.fromisoformat(row['timestamp'])
                donations.append(donation)
            
            return donations
        except sqlite3.Error as e:
            print(f"Error loading donations: {e}")
            return []
    
    def get_planet_count(self) -> int:
        """Retorna el número total de planetas en la sesión"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM planets WHERE session_id = ?", (self.current_session_id,))
            return cursor.fetchone()[0]
        except sqlite3.Error:
            return 0
    
    def get_total_donation_value(self) -> int:
        """Retorna el valor total de todas las donaciones en la sesión"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT SUM(value) FROM donations WHERE session_id = ?", (self.current_session_id,))
            result = cursor.fetchone()[0]
            return result if result else 0
        except sqlite3.Error:
            return 0
    
    def close(self):
        """
        Cierra la conexión a la base de datos
        
        Futuras acciones de cleanup:
        - Actualizar estadísticas finales de sesión
        - Crear backup automático
        - Limpiar datos temporales
        """
        if self.connection:
            self.connection.close()
            self.connection = None
