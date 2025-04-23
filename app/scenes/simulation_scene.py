"""
Simulation scene implementation for the double pendulum simulation.
Provides interactive controls and visualization of the pendulum physics.
"""

import pygame
import pygame_gui
import math
from app.scenes.scene_manager import Scene
from app.physics.pendulum_physics import PhysicsEngine, PendulumSystem, PendulumParams
from app.util.scene_navigation import change_scene

class SimulationScene(Scene):
    """
    Simulation scene with interactive pendulum visualization and controls
    """
    
    def __init__(self):
        """Initialize simulation scene attributes"""
        self.surface = None
        self.config_manager = None
        self.ui_manager = None
        self.ui_widgets = {}
        self.physics_engine = None
        self.pendulum_system = None
        self.is_running = False
        self.simulation_speed = 1.0
        self.show_grid = True
        self.theme_colors = {}
        self.background_color = (240, 240, 245)  # Default light theme
        
        # Simulation variables
        self.dragging = False
        self.selected_pendulum_id = None
        
        # Fonts
        self.title_font = None
        self.text_font = None
        self.small_font = None
        
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
        self.title_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 18)
        self.small_font = pygame.font.SysFont('Arial', 14)
        
        # Initialize physics engine
        self.physics_engine = PhysicsEngine()
        gravity = self.config_manager.get_setting("simulation.gravity", 9.81)
        self.physics_engine.initialize(gravity)
        
        # Initialize pendulum system
        self.pendulum_system = PendulumSystem()
        self.pendulum_system.initialize()
        
        # Create default pendulum
        self._create_default_pendulum()
        
        # Create UI elements
        self._create_ui_elements()
        
        # Show grid by default
        self.show_grid = self.config_manager.get_setting("show_grid", True)
        
        print("Simulation scene initialized")
        
    def _create_default_pendulum(self):
        """Create the default pendulum with settings from config"""
        params = PendulumParams(
            offset_x=0,
            offset_y=0,
            length1=self.config_manager.get_setting("simulation.default_length1", 120),
            length2=self.config_manager.get_setting("simulation.default_length2", 120),
            mass1=self.config_manager.get_setting("simulation.default_mass1", 10),
            mass2=self.config_manager.get_setting("simulation.default_mass2", 10),
            angle1=self.config_manager.get_setting("simulation.default_angle1", 0.8),
            angle2=self.config_manager.get_setting("simulation.default_angle2", 0.5),
            velocity1=self.config_manager.get_setting("simulation.default_velocity1", 0),
            velocity2=self.config_manager.get_setting("simulation.default_velocity2", 0),
            path_color=tuple(self.config_manager.get_setting("simulation.default_path_color", [0, 128, 255])),
            path_duration=self.config_manager.get_setting("simulation.default_path_duration", 2.0),
            show_wire=self.config_manager.get_setting("simulation.default_show_wire", True)
        )
        
        self.pendulum_system.create_pendulum(params)
        
    def _create_ui_elements(self):
        """Create simulation UI controls"""
        # Control panel background
        panel_rect = pygame.Rect(10, 10, 280, self.surface.get_height() - 20)
        panel = pygame_gui.elements.UIPanel(
            relative_rect=panel_rect,
            manager=self.ui_manager
        )
        self.ui_widgets["panel"] = panel
        
        # Simulation controls
        title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 20, 260, 30),
            text="Simulation Controls",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["title_label"] = title_label
        
        # Start/stop button
        toggle_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 60, 120, 40),
            text="Start",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["toggle_button"] = toggle_button
        
        # Reset button
        reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(150, 60, 120, 40),
            text="Reset",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["reset_button"] = reset_button
        
        # Speed controls
        speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 110, 260, 20),
            text="Simulation Speed",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["speed_label"] = speed_label
        
        speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(20, 140, 260, 20),
            start_value=1.0,
            value_range=(0.1, 10.0),
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["speed_slider"] = speed_slider
        
        # Parameter controls
        params_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 170, 260, 20),
            text="Pendulum Parameters",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["params_label"] = params_label
        
        # Gravity
        gravity_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 200, 120, 20),
            text="Gravity:",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["gravity_label"] = gravity_label
        
        gravity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 200, 120, 20),
            start_value=self.physics_engine.get_gravity(),
            value_range=(0.0, 20.0),
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["gravity_slider"] = gravity_slider
        
        # Length controls
        length1_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 230, 120, 20),
            text="Length 1:",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["length1_label"] = length1_label
        
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        length1_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 230, 120, 20),
            start_value=selected_pendulum.length1 if selected_pendulum else 120,
            value_range=(10, 200),
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["length1_slider"] = length1_slider
        
        length2_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 260, 120, 20),
            text="Length 2:",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["length2_label"] = length2_label
        
        length2_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 260, 120, 20),
            start_value=selected_pendulum.length2 if selected_pendulum else 120,
            value_range=(10, 200),
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["length2_slider"] = length2_slider
        
        # Mass controls
        mass1_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 290, 120, 20),
            text="Mass 1:",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["mass1_label"] = mass1_label
        
        mass1_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 290, 120, 20),
            start_value=selected_pendulum.mass1 if selected_pendulum else 10,
            value_range=(1, 20),
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["mass1_slider"] = mass1_slider
        
        mass2_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 320, 120, 20),
            text="Mass 2:",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["mass2_label"] = mass2_label
        
        mass2_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 320, 120, 20),
            start_value=selected_pendulum.mass2 if selected_pendulum else 10,
            value_range=(1, 20),
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["mass2_slider"] = mass2_slider
        
        # Initial angle controls
        angle1_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 350, 120, 20),
            text="Angle 1:",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["angle1_label"] = angle1_label
        
        angle1_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 350, 120, 20),
            start_value=selected_pendulum.angle1 if selected_pendulum else 0.8,
            value_range=(-math.pi, math.pi),
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["angle1_slider"] = angle1_slider
        
        angle2_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 380, 120, 20),
            text="Angle 2:",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["angle2_label"] = angle2_label
        
        angle2_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 380, 120, 20),
            start_value=selected_pendulum.angle2 if selected_pendulum else 0.5,
            value_range=(-math.pi, math.pi),
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["angle2_slider"] = angle2_slider
        
        # Path options
        path_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 410, 260, 20),
            text="Path Options",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["path_label"] = path_label
        
        # Path duration
        duration_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 440, 120, 20),
            text="Path Duration:",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["duration_label"] = duration_label
        
        duration_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 440, 120, 20),
            start_value=selected_pendulum.path_tracer.max_points / 60 if selected_pendulum else 2.0,
            value_range=(0.1, 10.0),
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["duration_slider"] = duration_slider
        
        # Path color picker (simplified)
        color_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 470, 120, 20),
            text="Path Color:",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["color_label"] = color_label
        
        # Create color buttons
        color_buttons_rect = pygame.Rect(150, 470, 120, 20)
        colors = [
            ((0, 128, 255), "Blue"),
            ((255, 0, 0), "Red"),
            ((0, 255, 0), "Green"),
            ((255, 255, 0), "Yellow")
        ]
        
        for i, (color, name) in enumerate(colors):
            btn_width = color_buttons_rect.width // len(colors)
            color_btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    color_buttons_rect.x + i * btn_width, 
                    color_buttons_rect.y, 
                    btn_width, 
                    color_buttons_rect.height
                ),
                text="",
                manager=self.ui_manager,
                container=panel,
                object_id=f"color_btn_{i}"
            )
            # Store color with button for reference
            color_btn.color = color
            self.ui_widgets[f"color_btn_{i}"] = color_btn
        
        # Toggle wire visibility
        wire_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 500, 260, 30),
            text="Toggle Wire Visibility",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["wire_checkbox"] = wire_checkbox
        
        # Toggle grid visibility
        grid_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 540, 260, 30),
            text="Toggle Grid",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["grid_checkbox"] = grid_checkbox
        
        # Multiple pendulums
        pendulum_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 580, 260, 20),
            text="Pendulum Management",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["pendulum_label"] = pendulum_label
        
        add_pendulum_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 610, 120, 30),
            text="Add Pendulum",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["add_pendulum_button"] = add_pendulum_button
        
        remove_pendulum_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(150, 610, 120, 30),
            text="Remove",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["remove_pendulum_button"] = remove_pendulum_button
        
        # Return to menu button
        return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, panel.relative_rect.height - 50, 260, 40),
            text="Return to Menu",
            manager=self.ui_manager,
            container=panel
        )
        self.ui_widgets["return_button"] = return_button
        
    def update(self, dt):
        """
        Update simulation logic
        
        Args:
            dt: Delta time in seconds since last update
        """
        # Update UI manager
        self.ui_manager.update(dt)
        
        # Skip physics update if paused
        if self.is_running:
            # Scale dt by simulation speed
            scaled_dt = dt * self.simulation_speed
            
            # Update physics engine
            self.physics_engine.update(scaled_dt)
            
            # Update pendulum system
            self.pendulum_system.update(scaled_dt, self.physics_engine.get_gravity())
            
    def render(self):
        """Render the simulation to the surface"""
        # Clear the screen
        self.surface.fill(self.background_color)
        
        # Draw grid if enabled
        if self.show_grid:
            self._draw_grid()
        
        # Render pendulum system
        self.pendulum_system.render(self.surface)
        
        # Draw UI elements
        self.ui_manager.draw_ui(self.surface)
        
        # Draw status text
        status_text = f"Status: {'Running' if self.is_running else 'Paused'} | Speed: {self.simulation_speed:.1f}x | Gravity: {self.physics_engine.get_gravity():.1f}"
        
        # Draw status text with background
        status_surface = self.text_font.render(status_text, True, self.theme_colors["text"])
        status_rect = status_surface.get_rect()
        status_rect.bottomright = (self.surface.get_width() - 10, self.surface.get_height() - 10)
        
        # Add background for status text
        bg_rect = status_rect.copy()
        bg_rect.inflate_ip(20, 10)
        pygame.draw.rect(self.surface, (*self.theme_colors["background"], 200), bg_rect, border_radius=5)
        
        # Draw text
        self.surface.blit(status_surface, status_rect)
        
    def _draw_grid(self):
        """Draw reference grid on the simulation surface"""
        width, height = self.surface.get_width(), self.surface.get_height()
        grid_color = self.theme_colors["grid"]
        grid_spacing = 50
        
        # Vertical lines
        for x in range(300, width, grid_spacing):  # Start after control panel
            pygame.draw.line(
                self.surface,
                grid_color,
                (x, 0),
                (x, height),
                1
            )
            
        # Horizontal lines
        for y in range(0, height, grid_spacing):
            pygame.draw.line(
                self.surface,
                grid_color,
                (300, y),  # Start after control panel
                (width, y),
                1
            )
            
        # Draw center point (anchor)
        center_x, center_y = width // 2, height // 2
        pygame.draw.circle(self.surface, self.theme_colors["primary"], (center_x, center_y), 5)
        
    def handle_event(self, event):
        """
        Process pygame events
        
        Args:
            event: The pygame event to handle
        """
        # Process UI events
        self.ui_manager.process_events(event)
        
        # Mouse events for dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if click is in simulation area (not on UI panel)
            if event.pos[0] > 300:  # UI panel width
                self._handle_simulation_click(event.pos)
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and event.pos[0] > 300:
                self._handle_simulation_drag(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self._handle_simulation_release()
                
        # Handle UI interactions
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.ui_widgets.get("toggle_button"):
                    self.toggle_simulation()
                elif event.ui_element == self.ui_widgets.get("reset_button"):
                    self.reset_simulation()
                elif event.ui_element == self.ui_widgets.get("wire_checkbox"):
                    self.toggle_wire_visibility()
                elif event.ui_element == self.ui_widgets.get("grid_checkbox"):
                    self.toggle_grid_visibility()
                elif event.ui_element == self.ui_widgets.get("add_pendulum_button"):
                    self.add_pendulum()
                elif event.ui_element == self.ui_widgets.get("remove_pendulum_button"):
                    self.remove_selected_pendulum()
                elif event.ui_element == self.ui_widgets.get("return_button"):
                    change_scene("home")
                # Color buttons
                elif "color_btn_" in event.ui_element.object_ids:
                    self.set_path_color(event.ui_element.color)
                    
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.ui_widgets.get("speed_slider"):
                    self.simulation_speed = event.value
                elif event.ui_element == self.ui_widgets.get("gravity_slider"):
                    self.physics_engine.set_gravity(event.value)
                elif event.ui_element == self.ui_widgets.get("length1_slider"):
                    self.update_pendulum_parameter("length1", event.value)
                elif event.ui_element == self.ui_widgets.get("length2_slider"):
                    self.update_pendulum_parameter("length2", event.value)
                elif event.ui_element == self.ui_widgets.get("mass1_slider"):
                    self.update_pendulum_parameter("mass1", event.value)
                elif event.ui_element == self.ui_widgets.get("mass2_slider"):
                    self.update_pendulum_parameter("mass2", event.value)
                elif event.ui_element == self.ui_widgets.get("angle1_slider"):
                    self.update_pendulum_parameter("angle1", event.value)
                elif event.ui_element == self.ui_widgets.get("angle2_slider"):
                    self.update_pendulum_parameter("angle2", event.value)
                elif event.ui_element == self.ui_widgets.get("duration_slider"):
                    self.update_path_duration(event.value)
                
    def toggle_simulation(self):
        """Toggle simulation between running and paused states"""
        self.is_running = not self.is_running
        
        # Update button text
        if self.ui_widgets.get("toggle_button"):
            self.ui_widgets["toggle_button"].set_text("Pause" if self.is_running else "Start")
            
    def reset_simulation(self):
        """Reset the pendulum to its initial state"""
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        if selected_pendulum:
            # Reset the pendulum
            selected_pendulum.reset()
            
            # Update UI sliders to match reset values
            if self.ui_widgets.get("length1_slider"):
                self.ui_widgets["length1_slider"].set_current_value(selected_pendulum.length1)
            if self.ui_widgets.get("length2_slider"):
                self.ui_widgets["length2_slider"].set_current_value(selected_pendulum.length2)
            if self.ui_widgets.get("mass1_slider"):
                self.ui_widgets["mass1_slider"].set_current_value(selected_pendulum.mass1)
            if self.ui_widgets.get("mass2_slider"):
                self.ui_widgets["mass2_slider"].set_current_value(selected_pendulum.mass2)
            if self.ui_widgets.get("angle1_slider"):
                self.ui_widgets["angle1_slider"].set_current_value(selected_pendulum.angle1)
            if self.ui_widgets.get("angle2_slider"):
                self.ui_widgets["angle2_slider"].set_current_value(selected_pendulum.angle2)
                
    def update_pendulum_parameter(self, param_name, value):
        """
        Update a parameter for the selected pendulum
        
        Args:
            param_name: Name of the parameter to update
            value: New value for the parameter
        """
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        if not selected_pendulum:
            return
            
        if param_name == "length1":
            selected_pendulum.set_length(1, value)
        elif param_name == "length2":
            selected_pendulum.set_length(2, value)
        elif param_name == "mass1":
            selected_pendulum.set_mass(1, value)
        elif param_name == "mass2":
            selected_pendulum.set_mass(2, value)
        elif param_name == "angle1":
            selected_pendulum.set_angle(1, value)
        elif param_name == "angle2":
            selected_pendulum.set_angle(2, value)
            
    def toggle_wire_visibility(self):
        """Toggle visibility of pendulum wires/rods"""
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        if selected_pendulum:
            selected_pendulum.toggle_wire_visibility()
            
    def toggle_grid_visibility(self):
        """Toggle grid visibility"""
        self.show_grid = not self.show_grid
        self.config_manager.set_setting("show_grid", self.show_grid)
        
    def set_path_color(self, color):
        """
        Set path tracer color
        
        Args:
            color: RGB color tuple
        """
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        if selected_pendulum:
            selected_pendulum.path_tracer.set_color(*color)
            
    def update_path_duration(self, duration):
        """
        Update path trace duration
        
        Args:
            duration: Duration in seconds
        """
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        if selected_pendulum:
            selected_pendulum.path_tracer.set_duration(duration)
            
    def add_pendulum(self):
        """Add a new pendulum to the simulation"""
        # Create with slight offset from existing pendulums for visibility
        offset_x = 0
        offset_y = 0
        
        # If there are existing pendulums, offset the new one slightly
        if self.pendulum_system.get_pendulum_count() > 0:
            offset_x = (self.pendulum_system.get_pendulum_count() % 3) * 20 - 20
            offset_y = (self.pendulum_system.get_pendulum_count() // 3) * 20 - 20
            
        # Create with default parameters but different color
        colors = [
            (0, 128, 255),    # Blue
            (255, 0, 0),      # Red
            (0, 255, 0),      # Green
            (255, 255, 0),    # Yellow
            (255, 0, 255),    # Magenta
            (0, 255, 255)     # Cyan
        ]
        
        color_index = self.pendulum_system.get_pendulum_count() % len(colors)
        
        params = PendulumParams(
            offset_x=offset_x,
            offset_y=offset_y,
            length1=self.config_manager.get_setting("simulation.default_length1", 120),
            length2=self.config_manager.get_setting("simulation.default_length2", 120),
            mass1=self.config_manager.get_setting("simulation.default_mass1", 10),
            mass2=self.config_manager.get_setting("simulation.default_mass2", 10),
            angle1=self.config_manager.get_setting("simulation.default_angle1", 0.8),
            angle2=self.config_manager.get_setting("simulation.default_angle2", 0.5),
            velocity1=self.config_manager.get_setting("simulation.default_velocity1", 0),
            velocity2=self.config_manager.get_setting("simulation.default_velocity2", 0),
            path_color=colors[color_index],
            path_duration=self.config_manager.get_setting("simulation.default_path_duration", 2.0),
            show_wire=self.config_manager.get_setting("simulation.default_show_wire", True)
        )
        
        # Create and select the new pendulum
        new_pendulum = self.pendulum_system.create_pendulum(params)
        
        # Update UI to match new pendulum
        self._update_ui_for_selected_pendulum()
        
    def remove_selected_pendulum(self):
        """Remove the currently selected pendulum"""
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        if selected_pendulum and self.pendulum_system.get_pendulum_count() > 1:
            self.pendulum_system.remove_pendulum(selected_pendulum.id)
            
            # Select the first available pendulum
            if self.pendulum_system.get_pendulum_count() > 0:
                first_id = next(iter(self.pendulum_system.pendulums.keys()))
                self.pendulum_system.select_pendulum(first_id)
                
            # Update UI for newly selected pendulum
            self._update_ui_for_selected_pendulum()
            
    def _update_ui_for_selected_pendulum(self):
        """Update UI controls to match the selected pendulum's properties"""
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        if not selected_pendulum:
            return
            
        # Update sliders to match pendulum properties
        if self.ui_widgets.get("length1_slider"):
            self.ui_widgets["length1_slider"].set_current_value(selected_pendulum.length1)
        if self.ui_widgets.get("length2_slider"):
            self.ui_widgets["length2_slider"].set_current_value(selected_pendulum.length2)
        if self.ui_widgets.get("mass1_slider"):
            self.ui_widgets["mass1_slider"].set_current_value(selected_pendulum.mass1)
        if self.ui_widgets.get("mass2_slider"):
            self.ui_widgets["mass2_slider"].set_current_value(selected_pendulum.mass2)
        if self.ui_widgets.get("angle1_slider"):
            self.ui_widgets["angle1_slider"].set_current_value(selected_pendulum.angle1)
        if self.ui_widgets.get("angle2_slider"):
            self.ui_widgets["angle2_slider"].set_current_value(selected_pendulum.angle2)
        if self.ui_widgets.get("duration_slider"):
            self.ui_widgets["duration_slider"].set_current_value(
                selected_pendulum.path_tracer.max_points / 60)  # Convert points to seconds
                
    def _handle_simulation_click(self, pos):
        """
        Handle mouse click in the simulation area
        
        Args:
            pos: (x, y) mouse position
        """
        # Try to select a pendulum at the clicked position
        pendulum = self.pendulum_system.try_select_pendulum_at_position(
            pos, (self.surface.get_width() // 2, self.surface.get_height() // 2))
            
        if pendulum:
            # Start dragging if a pendulum was selected
            self.dragging = pendulum.start_drag(
                pos, (self.surface.get_width() // 2, self.surface.get_height() // 2))
                
            # Update UI to reflect selected pendulum
            self._update_ui_for_selected_pendulum()
            
    def _handle_simulation_drag(self, pos):
        """
        Handle mouse drag in the simulation area
        
        Args:
            pos: (x, y) mouse position
        """
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        if selected_pendulum and self.dragging:
            selected_pendulum.update_drag(
                pos, (self.surface.get_width() // 2, self.surface.get_height() // 2))
                
            # Update UI sliders to match the new pendulum state
            if self.ui_widgets.get("angle1_slider"):
                self.ui_widgets["angle1_slider"].set_current_value(selected_pendulum.angle1)
            if self.ui_widgets.get("angle2_slider"):
                self.ui_widgets["angle2_slider"].set_current_value(selected_pendulum.angle2)
            if self.ui_widgets.get("length1_slider"):
                self.ui_widgets["length1_slider"].set_current_value(selected_pendulum.length1)
            if self.ui_widgets.get("length2_slider"):
                self.ui_widgets["length2_slider"].set_current_value(selected_pendulum.length2)
                
    def _handle_simulation_release(self):
        """Handle mouse release at the end of a drag operation"""
        selected_pendulum = self.pendulum_system.get_selected_pendulum()
        if selected_pendulum:
            selected_pendulum.end_drag()
            
        # End dragging state
        self.dragging = False
        
    def cleanup(self):
        """Release scene resources"""
        # Clean up UI manager
        self.ui_manager = None