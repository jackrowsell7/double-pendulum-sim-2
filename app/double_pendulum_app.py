"""
DoublePendulumApp - Main application controller for the Double Pendulum Simulation
"""

import pygame
import pygame_gui
import os
import json
from app.config.config_manager import ConfigManager
from app.scenes.scene_manager import SceneManager
from app.scenes.home_scene import HomeScene
from app.scenes.simulation_scene import SimulationScene
from app.scenes.settings_scene import SettingsScene
from app.scenes.information_scene import InformationScene
from app.util.scene_navigation import initialize_navigator

class DoublePendulumApp:
    """
    Main application controller that manages the entire double pendulum simulation
    """
    
    def __init__(self):
        """Initialize class attributes"""
        self.running = False
        self.clock = None
        self.main_surface = None
        self.config_manager = None
        self.scene_manager = None
        self.fps = 60  # Default frame rate

    def initialize(self):
        """
        Set up pygame, load configurations, and initialize scene manager
        """
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("Double Pendulum Simulation")
        
        # Create clock for managing frame rate
        self.clock = pygame.time.Clock()
        
        # Initialize configuration manager
        self.config_manager = ConfigManager("settings.json")
        self.config_manager.initialize()
        
        # Load settings
        settings = self.config_manager.load_configuration()
        self.fps = settings.get("fps", 60)
        screen_width = settings.get("screen_width", 1024)
        screen_height = settings.get("screen_height", 768)
        
        # Create display surface
        self.main_surface = pygame.display.set_mode(
            (screen_width, screen_height), 
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        
        # Initialize scene manager
        self.scene_manager = SceneManager(self.main_surface, self.config_manager)
        
        # Initialize scene navigation utility
        initialize_navigator(self.scene_manager)
        
        # Register scenes
        self._register_scenes()
        
        # Set initial scene
        self.scene_manager.change_scene("home")
        
        # Set running flag
        self.running = True
        
        print("Application initialized successfully")

    def _register_scenes(self):
        """
        Register all application scenes with the scene manager
        """
        self.scene_manager.register_scene("home", HomeScene)
        self.scene_manager.register_scene("simulation", SimulationScene)
        self.scene_manager.register_scene("settings", SettingsScene)
        self.scene_manager.register_scene("information", InformationScene)

    def run(self):
        """
        Main application loop - controls the program flow
        """
        while self.running:
            # Calculate delta time in seconds
            dt = self.clock.tick(self.fps) / 1000.0
            
            # Process events
            self._process_events()
            
            # Update current scene
            self.scene_manager.update(dt)
            
            # Render current scene
            self.scene_manager.render()
            
            # Update display
            pygame.display.flip()

    def _process_events(self):
        """
        Handle global pygame events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Pass event to current scene
            self.scene_manager.handle_event(event)

    def exit(self):
        """
        Clean up resources and prepare for application shutdown
        """
        # Save settings
        if self.config_manager:
            self.config_manager.save_configuration()
            
        # Clean up scenes
        if self.scene_manager:
            self.scene_manager.cleanup()
        
        print("Application shutdown complete")