# Main entry point for TikTok Planets System
# Aplicación principal que inicia el sistema de planetas para TikTok Lives

import sys
import pygame
from src.ui.main_window import MainWindow
from src.core.session_manager import SessionManager

def main():
    """
    Punto de entrada principal de la aplicación
    """
    # Inicializar pygame
    pygame.init()
    
    # Crear gestor de sesión
    session_manager = SessionManager()
    
    # Crear ventana principal
    main_window = MainWindow(session_manager)
    
    # Ejecutar loop principal
    main_window.run()
    
    # Cleanup
    pygame.quit()
    session_manager.close_session()

if __name__ == "__main__":
    main()
