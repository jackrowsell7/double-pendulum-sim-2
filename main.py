"""
Double Pendulum Simulation
An educational physics simulation that demonstrates chaos theory and double pendulum dynamics
"""

import os
import sys
import pygame
from app.double_pendulum_app import DoublePendulumApp

def main():
    """
    Application entry point
    """
    # Initialize pygame
    pygame.init()
    
    # Create and initialize the application
    app = DoublePendulumApp()
    app.initialize()
    
    try:
        # Run the application
        app.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up resources
        app.exit()
        pygame.quit()
        
    print("Application closed successfully")
    
if __name__ == "__main__":
    main()