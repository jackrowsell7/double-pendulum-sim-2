"""
Settings scene implementation for the double pendulum simulation.
Provides options to customize the application.
"""

import pygame
import pygame_gui
from app.scenes.scene_manager import Scene
from app.util.scene_navigation import change_scene

class SettingsScene(Scene):
    """
    Settings scene that allows users to customize application settings
    """
    
    def __init__(self):
        """Initialize scene attributes"""
        self.surface = None
        self.config_manager = None
        self.ui_manager = None
        self.settings_widgets = {}
        self.title_font = None
        self.text_font = None
        self.background_color = (240, 240, 245)  # Default light theme
        self.theme_colors = {}
        self.modified_settings = {}
        
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
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 24)
        
        # Create UI elements
        self._create_ui_elements()
        
        # Initialize modified settings with current values
        self.modified_settings = {}
        
        print("Settings scene initialized")
        
    def _create_ui_elements(self):
        """Create settings UI controls"""
        # Create panel to contain all settings widgets
        panel_width = 600
        panel_height = 500
        panel_rect = pygame.Rect(
            (self.surface.get_width() - panel_width) // 2,
            (self.surface.get_height() - panel_height) // 2,
            panel_width,
            panel_height
        )
        
        panel = pygame_gui.elements.UIPanel(
            relative_rect=panel_rect,
            manager=self.ui_manager
        )
        self.settings_widgets["panel"] = panel
        
        # Settings title
        title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 20, panel_width, 40),
            text="Settings",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["title_label"] = title_label
        
        # Theme selection
        theme_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 80, 200, 30),
            text="Theme:",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["theme_label"] = theme_label
        
        # Current theme
        current_theme = self.config_manager.get_setting("theme", "light")
        
        # Light theme button
        light_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(250, 80, 120, 30),
            text="Light",
            manager=self.ui_manager,
            container=panel,
            object_id="light_theme_button"
        )
        if current_theme == "light":
            light_button.select()
        self.settings_widgets["light_button"] = light_button
        
        # Dark theme button
        dark_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(380, 80, 120, 30),
            text="Dark",
            manager=self.ui_manager,
            container=panel,
            object_id="dark_theme_button"
        )
        if current_theme == "dark":
            dark_button.select()
        self.settings_widgets["dark_button"] = dark_button
        
        # Screen resolution settings
        resolution_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 130, 200, 30),
            text="Screen Resolution:",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["resolution_label"] = resolution_label
        
        # Current resolution
        current_width = self.config_manager.get_setting("screen_width", 1024)
        current_height = self.config_manager.get_setting("screen_height", 768)
        
        # Resolution options
        resolutions = [
            "1024x768",
            "1280x720",
            "1366x768",
            "1600x900",
            "1920x1080"
        ]
        
        resolution_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=resolutions,
            starting_option=f"{current_width}x{current_height}",
            relative_rect=pygame.Rect(250, 130, 250, 30),
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["resolution_dropdown"] = resolution_dropdown
        
        # Frame rate settings
        fps_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 180, 200, 30),
            text="Frame Rate:",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["fps_label"] = fps_label
        
        # Current FPS
        current_fps = self.config_manager.get_setting("fps", 60)
        
        fps_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(250, 180, 250, 30),
            start_value=current_fps,
            value_range=(30, 120),
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["fps_slider"] = fps_slider
        
        fps_value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(510, 180, 40, 30),
            text=str(current_fps),
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["fps_value_label"] = fps_value_label
        
        # Default simulation settings
        sim_settings_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 230, 500, 30),
            text="Default Simulation Settings:",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["sim_settings_label"] = sim_settings_label
        
        # Gravity
        gravity_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(70, 270, 180, 30),
            text="Default Gravity:",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["gravity_label"] = gravity_label
        
        # Current gravity
        current_gravity = self.config_manager.get_setting("simulation.gravity", 9.81)
        
        gravity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(250, 270, 250, 30),
            start_value=current_gravity,
            value_range=(0.0, 20.0),
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["gravity_slider"] = gravity_slider
        
        gravity_value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(510, 270, 60, 30),
            text=f"{current_gravity:.2f}",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["gravity_value_label"] = gravity_value_label
        
        # Default path duration
        path_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(70, 310, 180, 30),
            text="Default Path Duration:",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["path_label"] = path_label
        
        # Current path duration
        current_path_duration = self.config_manager.get_setting("simulation.default_path_duration", 2.0)
        
        path_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(250, 310, 250, 30),
            start_value=current_path_duration,
            value_range=(0.1, 10.0),
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["path_slider"] = path_slider
        
        path_value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(510, 310, 60, 30),
            text=f"{current_path_duration:.1f}s",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["path_value_label"] = path_value_label
        
        # Buttons for saving and canceling changes
        save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(150, panel_height - 60, 120, 40),
            text="Save Settings",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["save_button"] = save_button
        
        cancel_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(330, panel_height - 60, 120, 40),
            text="Cancel",
            manager=self.ui_manager,
            container=panel
        )
        self.settings_widgets["cancel_button"] = cancel_button
        
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
        
        # Handle UI interactions
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.settings_widgets.get("light_button"):
                    self._change_theme("light")
                elif event.ui_element == self.settings_widgets.get("dark_button"):
                    self._change_theme("dark")
                elif event.ui_element == self.settings_widgets.get("save_button"):
                    self._save_settings()
                    change_scene("home")
                elif event.ui_element == self.settings_widgets.get("cancel_button"):
                    change_scene("home")
                    
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.settings_widgets.get("resolution_dropdown"):
                    self._change_resolution(event.text)
                    
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.settings_widgets.get("fps_slider"):
                    self._update_fps(event.value)
                elif event.ui_element == self.settings_widgets.get("gravity_slider"):
                    self._update_gravity(event.value)
                elif event.ui_element == self.settings_widgets.get("path_slider"):
                    self._update_path_duration(event.value)
                    
    def _change_theme(self, theme_name):
        """
        Change application theme

        Args:
            theme_name: Name of the theme to apply (light/dark)
        """
        # Store in modified settings
        self.modified_settings["theme"] = theme_name

        # Apply theme colors to preview
        self.theme_colors = self.config_manager.apply_theme(theme_name)
        self.background_color = self.theme_colors["background"]

    def _change_resolution(self, resolution_text):
        """
        Change screen resolution
        
        Args:
            resolution_text: Resolution in format "widthxheight"
        """
        try:
            width, height = map(int, resolution_text.split("x"))
            self.modified_settings["screen_width"] = width
            self.modified_settings["screen_height"] = height
        except (ValueError, AttributeError):
            print(f"Invalid resolution format: {resolution_text}")
            
    def _update_fps(self, value):
        """
        Update FPS setting
        
        Args:
            value: New FPS value
        """
        # Round to nearest integer
        fps = int(round(value))
        
        # Update display
        fps_value_label = self.settings_widgets.get("fps_value_label")
        if fps_value_label:
            fps_value_label.set_text(str(fps))
            
        # Store in modified settings
        self.modified_settings["fps"] = fps
        
    def _update_gravity(self, value):
        """
        Update default gravity setting
        
        Args:
            value: New gravity value
        """
        # Update display
        gravity_value_label = self.settings_widgets.get("gravity_value_label")
        if gravity_value_label:
            gravity_value_label.set_text(f"{value:.2f}")
            
        # Store in modified settings
        self.modified_settings["simulation.gravity"] = value
        
    def _update_path_duration(self, value):
        """
        Update default path duration setting
        
        Args:
            value: New path duration in seconds
        """
        # Update display
        path_value_label = self.settings_widgets.get("path_value_label")
        if path_value_label:
            path_value_label.set_text(f"{value:.1f}s")
            
        # Store in modified settings
        self.modified_settings["simulation.default_path_duration"] = value
        
    def _save_settings(self):
        """Save modified settings to configuration"""
        # Apply settings to configuration manager
        for key, value in self.modified_settings.items():
            self.config_manager.set_setting(key, value)
            
        # Save to file
        self.config_manager.save_configuration()
        print("Settings saved")
        
    def cleanup(self):
        """Release scene resources"""
        # Clean up UI manager
        self.ui_manager = None