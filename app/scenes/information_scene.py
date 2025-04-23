"""
Information scene implementation for the double pendulum simulation.
Provides educational content and usage instructions.
"""

import pygame
import pygame_gui
from app.scenes.scene_manager import Scene
from app.util.scene_navigation import change_scene

class InformationScene(Scene):
    """
    Information scene that provides educational content and usage instructions
    """
    
    def __init__(self):
        """Initialize scene attributes"""
        self.surface = None
        self.config_manager = None
        self.ui_manager = None
        self.info_widgets = {}
        self.title_font = None
        self.text_font = None
        self.background_color = (240, 240, 245)  # Default light theme
        self.theme_colors = {}
        self.current_section = 0
        self.info_sections = []
        self.section_texts = []
        
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
        self.text_font = pygame.font.SysFont('Arial', 20)
        
        # Define information sections
        self._define_info_sections()
        
        # Create UI elements
        self._create_ui_elements()
        
        print("Information scene initialized")
        
    def _define_info_sections(self):
        """Define the content for information sections"""
        # Section titles
        self.info_sections = [
            "About Double Pendulums",
            "The Physics Behind It",
            "Application Features",
            "How to Use the Simulation",
            "Understanding Chaos Theory"
        ]
        
        # Section content texts
        self.section_texts = [
            # About Double Pendulums
            """A double pendulum consists of two pendulums attached end to end. While it might seem simple, 
its motion is remarkably complex and demonstrates chaotic behavior.

This educational tool allows you to visualize and experiment with the fascinating dynamics of a double pendulum
system. You can adjust various parameters and observe how they affect the pendulum's motion.

The double pendulum is a classic example of a chaotic system - a system that is highly sensitive to initial 
conditions. Even tiny differences in starting position or velocity can lead to completely different paths 
over time, making long-term prediction impossible despite the system being completely deterministic.""",

            # The Physics Behind It
            """The motion of a double pendulum is governed by a set of coupled differential equations derived
from Lagrangian mechanics.

These equations account for:
• The angles of both pendulum arms
• The angular velocities
• The masses of both bobs
• The lengths of both rods
• Gravitational force

This simulation uses a numerical integration technique called the Velocity Verlet method, which provides good
energy conservation properties. This is important because in a physical double pendulum, total energy should
remain constant (ignoring air resistance).

The equations of motion are complex and nonlinear, which gives rise to the chaotic behavior observed. Small
changes in initial conditions can lead to drastically different trajectories.""",

            # Application Features
            """This application offers several features to help you explore double pendulum physics:

• Start/Stop/Reset controls to manage simulation flow
• Adjustable simulation speed
• Ability to modify pendulum parameters:
  - Rod lengths
  - Bob masses
  - Initial angles
  - Gravitational force
• Interactive drag-and-drop manipulation
• Path tracing with customizable duration and color
• Option to hide the connecting wires/rods
• Support for multiple pendulums for comparison
• Light and dark visual themes
• Grid reference for better visual tracking

All settings can be adjusted in real-time, allowing you to see the immediate effects of your changes.""",

            # How to Use the Simulation
            """Getting started with the simulation:

1. From the main menu, click "Start Simulation" to open the simulation screen.
2. Use the control panel on the left side to adjust parameters.
3. Click the "Start" button to begin the simulation.
4. Drag and drop the pendulum bobs to set custom initial positions.

Changing Parameters:
• Use the sliders to adjust pendulum properties
• Toggle wire visibility with the appropriate button
• Change path color using the color selection buttons
• Adjust path duration to control how long trails remain visible

Adding Multiple Pendulums:
• Click "Add Pendulum" to create additional pendulums
• Click on a pendulum to select it before modifying its parameters
• Use the "Remove" button to remove the selected pendulum

Remember that small changes to initial conditions can produce dramatically different results!""",

            # Understanding Chaos Theory
            """The double pendulum is a perfect demonstration of chaos theory in action.

Key characteristics of chaotic systems include:

1. Extreme sensitivity to initial conditions (the "butterfly effect")
2. Unpredictability over long time periods
3. Complex, non-repeating patterns
4. Deterministic nature (governed by specific equations)

Despite the chaotic motion, the system follows strict physical laws. The unpredictability doesn't come from
randomness but from the system's sensitivity to initial conditions.

With this simulation, you can observe how two pendulums with nearly identical starting positions will
eventually follow completely different paths. This divergence occurs exponentially over time.

Chaos theory has applications in weather forecasting, economics, population dynamics, and many other
fields where complex, nonlinear systems are studied."""
        ]
        
    def _create_ui_elements(self):
        """Create information UI elements"""
        # Create panel for information content
        panel_width = 800
        panel_height = 600
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
        self.info_widgets["panel"] = panel
        
        # Information title (changes with section)
        title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 20, panel_width, 40),
            text=self.info_sections[self.current_section],
            manager=self.ui_manager,
            container=panel
        )
        self.info_widgets["title_label"] = title_label
        
        # Information text area
        text_box = pygame_gui.elements.UITextBox(
            html_text=self.section_texts[self.current_section],
            relative_rect=pygame.Rect(50, 80, panel_width - 100, panel_height - 180),
            manager=self.ui_manager,
            container=panel
        )
        self.info_widgets["text_box"] = text_box
        
        # Navigation buttons
        prev_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(50, panel_height - 80, 120, 40),
            text="Previous",
            manager=self.ui_manager,
            container=panel
        )
        self.info_widgets["prev_button"] = prev_button
        
        next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width - 170, panel_height - 80, 120, 40),
            text="Next",
            manager=self.ui_manager,
            container=panel
        )
        self.info_widgets["next_button"] = next_button
        
        # Return to menu button
        return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width // 2 - 60, panel_height - 80, 120, 40),
            text="Return",
            manager=self.ui_manager,
            container=panel
        )
        self.info_widgets["return_button"] = return_button
        
        # Section indicator
        section_indicator = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, panel_height - 30, panel_width, 20),
            text=f"Section {self.current_section + 1} of {len(self.info_sections)}",
            manager=self.ui_manager,
            container=panel
        )
        self.info_widgets["section_indicator"] = section_indicator
        
        # Update button states based on current section
        self._update_button_states()
        
    def _update_button_states(self):
        """Update navigation button states based on current section"""
        # Disable previous button if on first section
        if self.info_widgets.get("prev_button"):
            self.info_widgets["prev_button"].disable() if self.current_section == 0 else self.info_widgets["prev_button"].enable()
            
        # Disable next button if on last section
        if self.info_widgets.get("next_button"):
            self.info_widgets["next_button"].disable() if self.current_section == len(self.info_sections) - 1 else self.info_widgets["next_button"].enable()
            
    def _navigate_to_section(self, section_index):
        """
        Navigate to a specific information section
        
        Args:
            section_index: Index of the section to navigate to
        """
        # Validate section index
        if section_index < 0 or section_index >= len(self.info_sections):
            return
            
        # Update current section
        self.current_section = section_index
        
        # Update title
        if self.info_widgets.get("title_label"):
            self.info_widgets["title_label"].set_text(self.info_sections[self.current_section])
            
        # Update text content
        if self.info_widgets.get("text_box"):
            self.info_widgets["text_box"].html_text = self.section_texts[self.current_section]
            self.info_widgets["text_box"].rebuild()
            
        # Update section indicator
        if self.info_widgets.get("section_indicator"):
            self.info_widgets["section_indicator"].set_text(f"Section {self.current_section + 1} of {len(self.info_sections)}")
            
        # Update button states
        self._update_button_states()
        
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
                if event.ui_element == self.info_widgets.get("prev_button"):
                    self._navigate_to_section(self.current_section - 1)
                elif event.ui_element == self.info_widgets.get("next_button"):
                    self._navigate_to_section(self.current_section + 1)
                elif event.ui_element == self.info_widgets.get("return_button"):
                    change_scene("home")
                    
    def cleanup(self):
        """Release scene resources"""
        # Clean up UI manager
        self.ui_manager = None