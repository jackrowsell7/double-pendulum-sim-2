"""
Home scene implementation for the double pendulum simulation.
Provides the main menu and navigation to other scenes.
"""

import pygame
import pygame_gui
from app.scenes.scene_manager import Scene
from app.util.scene_navigation import change_scene

class HomeScene(Scene):
    """
    Home scene that serves as the main menu
    """
    
    def __init__(self):
        """Initialize scene attributes"""
        self.surface = None
        self.config_manager = None
        self.ui_manager = None
        self.menu_buttons = []
        self.title_font = None
        self.text_font = None
        self.background_color = (240, 240, 245)  # Default light theme
        self.theme_colors = {}
        
    def initialize(self, surface, config_manager):
        """
        Initialize the scene with required resources
        
        Args:
            surface: The pygame surface to render on
            config_manager: The application's configuration manager
        """
        self.surface = surface
        self.config_manager = config_manager
        
        # Initialize UI manager
        self.ui_manager = pygame_gui.UIManager(
            (surface.get_width(), surface.get_height()))
        
        # Load theme colors
        theme_name = self.config_manager.get_setting("theme", "light")
        self.theme_colors = self.config_manager.apply_theme(theme_name)
        self.background_color = self.theme_colors["background"]
        
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 60, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 24)
        
        # Create UI elements
        self._create_ui_elements()
        
        print("Home scene initialized")
        
    def _create_ui_elements(self):
        """Create UI buttons and elements"""
        button_width = 300
        button_height = 60
        center_x = self.surface.get_width() // 2
        start_y = 300
        spacing = 80
        
        # Create simulation button
        simulation_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (center_x - button_width // 2, start_y),
                (button_width, button_height)
            ),
            text="Start Simulation",
            manager=self.ui_manager
        )
        self.menu_buttons.append(simulation_button)
        
        # Create settings button
        settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (center_x - button_width // 2, start_y + spacing),
                (button_width, button_height)
            ),
            text="Settings",
            manager=self.ui_manager
        )
        self.menu_buttons.append(settings_button)
        
        # Create information button
        info_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (center_x - button_width // 2, start_y + spacing * 2),
                (button_width, button_height)
            ),
            text="Information",
            manager=self.ui_manager
        )
        self.menu_buttons.append(info_button)
        
        # Create exit button
        exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (center_x - button_width // 2, start_y + spacing * 3),
                (button_width, button_height)
            ),
            text="Exit",
            manager=self.ui_manager
        )
        self.menu_buttons.append(exit_button)
        
    def update(self, dt):
        """
        Update scene logic
        
        Args:
            dt: Delta time in seconds since last update
        """
        # Update UI manager
        self.ui_manager.update(dt)
        
    def render(self):
        """Render the scene to its surface"""
        # Clear the screen
        self.surface.fill(self.background_color)
        
        # Draw title
        title_text = self.title_font.render('Double Pendulum Simulation', 
                                          True, self.theme_colors["text"])
        title_rect = title_text.get_rect(center=(self.surface.get_width() // 2, 150))
        self.surface.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.text_font.render('An Educational Physics Tool', 
                                           True, self.theme_colors["text"])
        subtitle_rect = subtitle_text.get_rect(center=(self.surface.get_width() // 2, 210))
        self.surface.blit(subtitle_text, subtitle_rect)
        
        # Draw UI elements
        self.ui_manager.draw_ui(self.surface)
        
    def handle_event(self, event):
        """
        Process pygame events
        
        Args:
            event: The pygame event to handle
        """
        # Process UI events
        self.ui_manager.process_events(event)
        
        # Handle button clicks
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.menu_buttons[0]:
                    # Simulation button clicked
                    change_scene("simulation")
                elif event.ui_element == self.menu_buttons[1]:
                    # Settings button clicked
                    change_scene("settings")
                elif event.ui_element == self.menu_buttons[2]:
                    # Information button clicked
                    change_scene("information")
                elif event.ui_element == self.menu_buttons[3]:
                    # Exit button clicked
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    
    def cleanup(self):
        """Release scene resources"""
        # Clean up UI manager
        self.ui_manager = None