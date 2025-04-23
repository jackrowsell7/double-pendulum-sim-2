"""
ConfigManager - Handles loading, saving, and applying application settings
"""

import os
import json

class ConfigManager:
    """
    Manages configuration settings for the double pendulum simulation application
    """
    
    def __init__(self, config_file_name):
        """
        Initialize the configuration manager
        
        Args:
            config_file_name: Name of the configuration file
        """
        self.config_file_name = config_file_name
        self.settings = {}
        self.themes = {
            "light": {
                "background": (240, 240, 245),
                "text": (30, 30, 30),
                "primary": (0, 120, 215),
                "secondary": (0, 170, 170),
                "accent": (200, 0, 100),
                "grid": (200, 200, 200)
            },
            "dark": {
                "background": (30, 30, 35),
                "text": (220, 220, 220),
                "primary": (0, 150, 255),
                "secondary": (0, 200, 200),
                "accent": (255, 50, 100),
                "grid": (60, 60, 60)
            }
        }
        
    def initialize(self):
        """Initialize the configuration manager and load default settings"""
        # Set default settings
        self.settings = {
            # Application settings
            "theme": "light",
            "screen_width": 1024,
            "screen_height": 768,
            "fps": 60,
            "show_grid": True,
            
            # Simulation defaults
            "simulation.gravity": 9.81,
            "simulation.default_length1": 120,
            "simulation.default_length2": 120,
            "simulation.default_mass1": 10,
            "simulation.default_mass2": 10,
            "simulation.default_angle1": 0.8,
            "simulation.default_angle2": 0.5,
            "simulation.default_velocity1": 0,
            "simulation.default_velocity2": 0,
            "simulation.default_path_color": [0, 128, 255],
            "simulation.default_path_duration": 2.0,
            "simulation.default_show_wire": True
        }
        
        # Load settings from file if it exists
        if os.path.exists(self.config_file_name):
            self.load_configuration()
            
        print("ConfigManager initialized")
        
    def load_configuration(self):
        """
        Load configuration from file
        
        Returns:
            dict: The loaded settings dictionary
        """
        try:
            if os.path.exists(self.config_file_name):
                with open(self.config_file_name, 'r') as f:
                    loaded_settings = json.load(f)
                    # Update settings, keeping defaults for any missing values
                    for key, value in loaded_settings.items():
                        self.settings[key] = value
                print(f"Settings loaded from {self.config_file_name}")
            else:
                print(f"Config file not found: {self.config_file_name}, using defaults")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading configuration: {e}")
            
        return self.settings
        
    def save_configuration(self):
        """
        Save current configuration to file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.config_file_name, 'w') as f:
                json.dump(self.settings, f, indent=4)
            print(f"Settings saved to {self.config_file_name}")
            return True
        except IOError as e:
            print(f"Error saving configuration: {e}")
            return False
            
    def get_setting(self, key, default=None):
        """
        Get a setting value by key
        
        Args:
            key: The setting key
            default: Default value if setting not found
            
        Returns:
            The setting value or default if not found
        """
        return self.settings.get(key, default)
        
    def set_setting(self, key, value):
        """
        Set a setting value
        
        Args:
            key: The setting key
            value: The value to set
        """
        self.settings[key] = value
        
    def apply_theme(self, theme_name):
        """
        Apply a theme and return its color scheme
        
        Args:
            theme_name: The name of the theme to apply
            
        Returns:
            dict: The theme's color scheme
        """
        # Set theme name in settings
        self.set_setting("theme", theme_name)
        
        # Get the theme colors (default to light if not found)
        theme_colors = self.themes.get(theme_name, self.themes["light"])
        
        return theme_colors