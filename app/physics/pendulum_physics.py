"""
Physics engine implementation for the double pendulum simulation
Handles the mathematical modeling of pendulum dynamics
"""

import math
import numpy as np
from collections import deque
import pygame

class PhysicsEngine:
    """
    Core physics engine that manages time stepping and physical constants
    """
    
    def __init__(self):
        """Initialize the physics engine with default values"""
        self.gravity = 9.81  # Default gravity (m/s²)
        self.time_step = 0.01  # Default physics time step
        
    def initialize(self, default_gravity=9.81):
        """
        Initialize the physics engine
        
        Args:
            default_gravity: Initial gravity value
        """
        self.gravity = default_gravity
        print(f"Physics engine initialized with gravity: {self.gravity}")
        
    def update(self, dt):
        """
        Update physics state
        
        Args:
            dt: Delta time in seconds
        """
        # Physics engine internal state update
        # This method doesn't do much in this implementation as the actual
        # physics calculations happen in the pendulum system
        pass
        
    def set_gravity(self, gravity):
        """
        Set the gravity constant
        
        Args:
            gravity: Gravity value in m/s²
        """
        self.gravity = gravity
        
    def set_time_step(self, step):
        """
        Set the physics time step
        
        Args:
            step: Time step value in seconds
        """
        self.time_step = step
        
    def get_gravity(self):
        """
        Get the current gravity value
        
        Returns:
            float: Current gravity value
        """
        return self.gravity
        
    def get_time_step(self):
        """
        Get the current time step
        
        Returns:
            float: Current time step
        """
        return self.time_step


class PendulumParams:
    """
    Container class for pendulum parameters
    """
    
    def __init__(self, offset_x=0, offset_y=0, length1=120, length2=120, 
                mass1=10, mass2=10, angle1=math.pi/4, angle2=math.pi/4,
                velocity1=0, velocity2=0, path_color=(0, 128, 255), 
                path_duration=2.0, show_wire=True):
        """
        Initialize pendulum parameters
        
        Args:
            offset_x: X-coordinate offset from anchor point
            offset_y: Y-coordinate offset from anchor point
            length1: Length of first pendulum rod
            length2: Length of second pendulum rod
            mass1: Mass of first pendulum bob
            mass2: Mass of second pendulum bob
            angle1: Initial angle of first pendulum (in radians)
            angle2: Initial angle of second pendulum (in radians)
            velocity1: Initial angular velocity of first pendulum
            velocity2: Initial angular velocity of second pendulum
            path_color: RGB color tuple for path tracer
            path_duration: Duration for path trace visibility in seconds
            show_wire: Whether to show the pendulum wire/rod
        """
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.length1 = length1
        self.length2 = length2
        self.mass1 = mass1
        self.mass2 = mass2
        self.angle1 = angle1
        self.angle2 = angle2
        self.velocity1 = velocity1
        self.velocity2 = velocity2
        self.path_color = path_color
        self.path_duration = path_duration
        self.show_wire = show_wire
        
    def clone(self):
        """
        Create a copy of the parameters
        
        Returns:
            PendulumParams: A copy of these parameters
        """
        return PendulumParams(
            self.offset_x, self.offset_y,
            self.length1, self.length2,
            self.mass1, self.mass2,
            self.angle1, self.angle2,
            self.velocity1, self.velocity2,
            self.path_color, self.path_duration,
            self.show_wire
        )


class PathTracer:
    """
    Tracks and renders the path of a pendulum bob
    """
    
    def __init__(self, max_points=500, color=(0, 128, 255)):
        """
        Initialize the path tracer
        
        Args:
            max_points: Maximum number of points to store
            color: RGB color tuple for the path
        """
        self.points = deque(maxlen=max_points)
        self.max_points = max_points
        self.color = color
        self.visible = True
        
    def initialize(self, max_points, color):
        """
        Initialize or reinitialize the path tracer
        
        Args:
            max_points: Maximum number of points to store
            color: RGB color tuple for the path
        """
        self.max_points = max_points
        self.points = deque(maxlen=max_points)
        self.color = color
        
    def add_point(self, x, y):
        """
        Add a point to the path
        
        Args:
            x: X-coordinate
            y: Y-coordinate
        """
        if self.visible:
            self.points.append((x, y))
            
    def clear(self):
        """Clear all points from the path"""
        self.points.clear()
        
    def set_color(self, r, g, b):
        """
        Set the path color
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
        """
        self.color = (r, g, b)
        
    def set_duration(self, seconds, fps=60):
        """
        Set the path duration by adjusting the number of stored points
        
        Args:
            seconds: Duration in seconds
            fps: Frames per second of the simulation
        """
        self.max_points = int(seconds * fps)
        new_points = deque(maxlen=self.max_points)
        
        # Preserve existing points up to the new maximum
        for i, point in enumerate(self.points):
            if i < self.max_points:
                new_points.append(point)
                
        self.points = new_points
        
    def render(self, surface):
        """
        Render the path to a surface
        
        Args:
            surface: Pygame surface to render on
        """
        if not self.visible or len(self.points) < 2:
            return
            
        # Draw path with fading opacity
        points_list = list(self.points)
        for i in range(1, len(points_list)):
            # Calculate opacity based on position in the path
            # Newer points are more opaque
            alpha = int(255 * (i / len(points_list)))
            
            # Create color with alpha
            color = (*self.color, alpha)
            
            # Draw line segment
            pygame.draw.line(surface, color, points_list[i-1], points_list[i], 2)


class Pendulum:
    """
    Models a double pendulum with physics calculations and rendering
    """
    
    def __init__(self, pendulum_id):
        """
        Initialize the pendulum with a unique ID
        
        Args:
            pendulum_id: Unique identifier for this pendulum
        """
        self.id = pendulum_id
        self.path_tracer = PathTracer()
        self.initial_state = None
        
        # Physical state
        self.offset_x = 0
        self.offset_y = 0
        self.length1 = 120
        self.length2 = 120
        self.mass1 = 10
        self.mass2 = 10
        self.angle1 = math.pi/4
        self.angle2 = math.pi/4
        self.velocity1 = 0
        self.velocity2 = 0
        self.acceleration1 = 0
        self.acceleration2 = 0
        
        # Cartesian positions
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        
        # Visual properties
        self.show_wire = True
        
        # Drag state
        self.dragging = False
        self.drag_joint = 0  # 0: not dragging, 1: first joint, 2: second joint
        
    def initialize(self, params):
        """
        Initialize or reset the pendulum with parameters
        
        Args:
            params: PendulumParams object with initial values
        """
        # Store initial parameters for reset
        self.initial_state = params.clone()
        
        # Set physical properties
        self.offset_x = params.offset_x
        self.offset_y = params.offset_y
        self.length1 = params.length1
        self.length2 = params.length2
        self.mass1 = params.mass1
        self.mass2 = params.mass2
        self.angle1 = params.angle1
        self.angle2 = params.angle2
        self.velocity1 = params.velocity1
        self.velocity2 = params.velocity2
        self.show_wire = params.show_wire
        
        # Initialize path tracer
        fps = 60  # Assumed FPS, can be adjusted
        max_points = int(params.path_duration * fps)
        self.path_tracer.initialize(max_points, params.path_color)
        
        # Calculate initial positions
        self._calculate_cartesian_positions()
        
    def update(self, dt, gravity):
        """
        Update pendulum physics
        
        Args:
            dt: Delta time in seconds
            gravity: Gravity value to use for calculations
        """
        if self.dragging:
            # Skip physics update when being dragged
            return
            
        # Perform Velocity Verlet integration
        self._velocity_verlet_step(dt, gravity)
        
        # Calculate Cartesian positions from angles
        self._calculate_cartesian_positions()
        
        # We won't add the point here anymore - it will be done in render
        # to ensure screen coordinates are used
        
    def render(self, surface):
        """
        Render the pendulum to a surface
        
        Args:
            surface: Pygame surface to render on
        """
        # Calculate anchor point (center of screen + offset)
        anchor_x = surface.get_width() // 2 + self.offset_x
        anchor_y = surface.get_height() // 2 + self.offset_y
        
        # Convert to screen coordinates
        screen_x1 = anchor_x + self.x1
        screen_y1 = anchor_y + self.y1
        screen_x2 = anchor_x + self.x2
        screen_y2 = anchor_y + self.y2
        
        # Add point to path tracer for the second bob using screen coordinates
        if not self.dragging:
            self.path_tracer.add_point(screen_x2, screen_y2)
        
        # Render path
        self.path_tracer.render(surface)
        
        # Draw pendulum wires if enabled
        if self.show_wire:
            # Draw first pendulum rod
            pygame.draw.line(surface, (100, 100, 100), 
                            (anchor_x, anchor_y), (screen_x1, screen_y1), 2)
            # Draw second pendulum rod
            pygame.draw.line(surface, (100, 100, 100), 
                            (screen_x1, screen_y1), (screen_x2, screen_y2), 2)
        
        # Draw anchor point
        pygame.draw.circle(surface, (150, 150, 150), (anchor_x, anchor_y), 6)
        
        # Draw first bob
        pygame.draw.circle(surface, (200, 100, 100), (screen_x1, screen_y1), 
                          int(self.mass1 * 0.8))
        
        # Draw second bob
        pygame.draw.circle(surface, (100, 100, 200), (screen_x2, screen_y2), 
                          int(self.mass2 * 0.8))
        
    def reset(self):
        """Reset pendulum to initial state"""
        if self.initial_state:
            self.initialize(self.initial_state)
            
    def set_length(self, rod, value):
        """
        Set pendulum rod length
        
        Args:
            rod: Rod index (1 or 2)
            value: New length
        """
        if rod == 1:
            self.length1 = value
        else:
            self.length2 = value
            
        self._calculate_cartesian_positions()
        
    def set_mass(self, bob, value):
        """
        Set pendulum bob mass
        
        Args:
            bob: Bob index (1 or 2)
            value: New mass
        """
        if bob == 1:
            self.mass1 = value
        else:
            self.mass2 = value
            
    def set_angle(self, joint, value):
        """
        Set pendulum angle
        
        Args:
            joint: Joint index (1 or 2)
            value: New angle in radians
        """
        if joint == 1:
            self.angle1 = value
        else:
            self.angle2 = value
            
        self._calculate_cartesian_positions()
        
    def set_velocity(self, joint, value):
        """
        Set pendulum angular velocity
        
        Args:
            joint: Joint index (1 or 2)
            value: New angular velocity
        """
        if joint == 1:
            self.velocity1 = value
        else:
            self.velocity2 = value
            
    def toggle_wire_visibility(self):
        """Toggle visibility of the pendulum rods"""
        self.show_wire = not self.show_wire
        
    def start_drag(self, position, screen_center):
        """
        Start dragging a pendulum bob
        
        Args:
            position: (x, y) mouse position
            screen_center: (x, y) center of the screen
            
        Returns:
            bool: True if drag started, False otherwise
        """
        # Adjust position to be relative to anchor point
        anchor_x = screen_center[0] + self.offset_x
        anchor_y = screen_center[1] + self.offset_y
        
        # Calculate screen positions of bobs
        screen_x1 = anchor_x + self.x1
        screen_y1 = anchor_y + self.y1
        screen_x2 = anchor_x + self.x2
        screen_y2 = anchor_y + self.y2
        
        # Check if mouse is near second bob (check this first as it's usually on top)
        dx2 = position[0] - screen_x2
        dy2 = position[1] - screen_y2
        dist2 = math.sqrt(dx2*dx2 + dy2*dy2)
        
        if dist2 <= max(10, self.mass2):
            self.dragging = True
            self.drag_joint = 2
            return True
        
        # Check if mouse is near first bob
        dx1 = position[0] - screen_x1
        dy1 = position[1] - screen_y1
        dist1 = math.sqrt(dx1*dx1 + dy1*dy1)
        
        if dist1 <= max(10, self.mass1):
            self.dragging = True
            self.drag_joint = 1
            return True
            
        return False
        
    def update_drag(self, position, screen_center):
        """
        Update pendulum position during drag
        
        Args:
            position: (x, y) mouse position
            screen_center: (x, y) screen center
        """
        if not self.dragging:
            return
            
        # Adjust position to be relative to anchor point
        anchor_x = screen_center[0] + self.offset_x
        anchor_y = screen_center[1] + self.offset_y
        rel_x = position[0] - anchor_x
        rel_y = position[1] - anchor_y
        
        if self.drag_joint == 1:
            # Dragging first bob
            # Calculate new angle based on mouse position
            self.angle1 = math.atan2(rel_y, rel_x)
            
            # Adjust length if needed (can be disabled for fixed length)
            new_length = math.sqrt(rel_x*rel_x + rel_y*rel_y)
            if new_length > 10:  # Minimum length
                self.length1 = new_length
                
            # Reset velocities
            self.velocity1 = 0
            self.velocity2 = 0
            
        elif self.drag_joint == 2:
            # Dragging second bob
            # We need to find the angle that puts the second bob at the mouse position
            # This is more complex as it depends on both angles and lengths
            
            # First, calculate position of first bob
            self._calculate_cartesian_positions()
            first_bob_x = self.x1
            first_bob_y = self.y1
            
            # Position of second bob relative to first bob
            rel_to_first_x = rel_x - first_bob_x
            rel_to_first_y = rel_y - first_bob_y
            
            # Calculate new angle for second pendulum
            self.angle2 = math.atan2(rel_to_first_y, rel_to_first_x)
            
            # Adjust length if needed (can be disabled for fixed length)
            new_length = math.sqrt(rel_to_first_x*rel_to_first_x + rel_to_first_y*rel_to_first_y)
            if new_length > 10:  # Minimum length
                self.length2 = new_length
                
            # Reset velocities
            self.velocity1 = 0
            self.velocity2 = 0
            
        # Update cartesian positions
        self._calculate_cartesian_positions()
        
    def end_drag(self):
        """End the drag operation"""
        self.dragging = False
        self.drag_joint = 0
        
        # Clear path when drag ends
        self.path_tracer.clear()
        
    def _velocity_verlet_step(self, dt, gravity):
        """
        Perform a velocity Verlet integration step for accurate physics
        
        Args:
            dt: Time step
            gravity: Gravity value
        """
        # Save current accelerations
        accel1_old = self._calculate_acceleration1(gravity)
        accel2_old = self._calculate_acceleration2(gravity)
        
        # Half-step velocity update
        self.velocity1 += 0.5 * accel1_old * dt
        self.velocity2 += 0.5 * accel2_old * dt
        
        # Full-step position update
        self.angle1 += self.velocity1 * dt
        self.angle2 += self.velocity2 * dt
        
        # Normalize angles to [-π, π] range
        self.angle1 = ((self.angle1 + math.pi) % (2 * math.pi)) - math.pi
        self.angle2 = ((self.angle2 + math.pi) % (2 * math.pi)) - math.pi
        
        # Calculate new accelerations after position update
        accel1_new = self._calculate_acceleration1(gravity)
        accel2_new = self._calculate_acceleration2(gravity)
        
        # Complete velocity update
        self.velocity1 += 0.5 * accel1_new * dt
        self.velocity2 += 0.5 * accel2_new * dt
        
    def _calculate_acceleration1(self, gravity):
        """
        Calculate angular acceleration for the first pendulum
        Based on the equations of motion for a double pendulum
        
        Args:
            gravity: Gravity value
            
        Returns:
            float: Angular acceleration
        """
        # Double pendulum equation variables
        g = gravity
        m1 = self.mass1
        m2 = self.mass2
        l1 = self.length1
        l2 = self.length2
        a1 = self.angle1
        a2 = self.angle2
        v1 = self.velocity1
        v2 = self.velocity2
        
        # Double pendulum equations of motion for first pendulum
        # Using the Lagrangian formulation
        num1 = -g * (2 * m1 + m2) * math.sin(a1)
        num2 = -m2 * g * math.sin(a1 - 2 * a2)
        num3 = -2 * math.sin(a1 - a2) * m2 * (v2**2 * l2 + v1**2 * l1 * math.cos(a1 - a2))
        den = l1 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2))
        
        return (num1 + num2 + num3) / den
        
    def _calculate_acceleration2(self, gravity):
        """
        Calculate angular acceleration for the second pendulum
        Based on the equations of motion for a double pendulum
        
        Args:
            gravity: Gravity value
            
        Returns:
            float: Angular acceleration
        """
        # Double pendulum equation variables
        g = gravity
        m1 = self.mass1
        m2 = self.mass2
        l1 = self.length1
        l2 = self.length2
        a1 = self.angle1
        a2 = self.angle2
        v1 = self.velocity1
        v2 = self.velocity2
        
        # Double pendulum equations of motion for second pendulum
        # Using the Lagrangian formulation
        num1 = 2 * math.sin(a1 - a2)
        num2 = v1**2 * l1 * (m1 + m2) + g * (m1 + m2) * math.cos(a1)
        num3 = v2**2 * l2 * m2 * math.cos(a1 - a2)
        den = l2 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2))
        
        return num1 * (num2 + num3) / den
        
    def _calculate_cartesian_positions(self):
        """
        Calculate Cartesian (x,y) positions from pendulum angles
        """
        # First pendulum bob position
        self.x1 = self.length1 * math.sin(self.angle1)
        self.y1 = self.length1 * math.cos(self.angle1)
        
        # Second pendulum bob position (relative to first)
        self.x2 = self.x1 + self.length2 * math.sin(self.angle2)
        self.y2 = self.y1 + self.length2 * math.cos(self.angle2)
        
    def calculate_energy(self, gravity):
        """
        Calculate the total energy of the pendulum system
        
        Args:
            gravity: Gravity value
            
        Returns:
            tuple: (kinetic energy, potential energy, total energy)
        """
        # Physical constants
        g = gravity
        m1 = self.mass1
        m2 = self.mass2
        l1 = self.length1
        l2 = self.length2
        a1 = self.angle1
        a2 = self.angle2
        v1 = self.velocity1
        v2 = self.velocity2
        
        # Calculate positions
        x1 = l1 * math.sin(a1)
        y1 = -l1 * math.cos(a1)  # Negative as y increases downward
        x2 = x1 + l2 * math.sin(a2)
        y2 = y1 - l2 * math.cos(a2)
        
        # Calculate velocities in Cartesian coordinates
        vx1 = l1 * v1 * math.cos(a1)
        vy1 = l1 * v1 * math.sin(a1)
        vx2 = vx1 + l2 * v2 * math.cos(a2)
        vy2 = vy1 + l2 * v2 * math.sin(a2)
        
        # Kinetic energy: KE = 0.5 * m * v^2
        ke1 = 0.5 * m1 * (vx1**2 + vy1**2)
        ke2 = 0.5 * m2 * (vx2**2 + vy2**2)
        kinetic_energy = ke1 + ke2
        
        # Potential energy: PE = m * g * h
        # Note: height is measured from the anchor point
        pe1 = m1 * g * (y1 + l1)  # Adjusted for coordinate system
        pe2 = m2 * g * (y2 + l1 + l2)
        potential_energy = pe1 + pe2
        
        # Total energy
        total_energy = kinetic_energy + potential_energy
        
        return (kinetic_energy, potential_energy, total_energy)


class PendulumSystem:
    """
    Manages multiple pendulums and provides a unified interface for the simulation
    """
    
    def __init__(self):
        """Initialize the pendulum system"""
        self.pendulums = {}  # Dictionary of pendulum_id -> Pendulum
        self.selected_pendulum = None
        self.next_pendulum_id = 0
        
    def initialize(self):
        """Initialize the pendulum system"""
        # Clear any existing pendulums
        self.pendulums.clear()
        self.selected_pendulum = None
        self.next_pendulum_id = 0
        
        print("Pendulum system initialized")
        
    def update(self, dt, gravity):
        """
        Update all pendulums in the system
        
        Args:
            dt: Delta time in seconds
            gravity: Gravity value to use
        """
        for pendulum in self.pendulums.values():
            pendulum.update(dt, gravity)
            
    def render(self, surface):
        """
        Render all pendulums to a surface
        
        Args:
            surface: Pygame surface to render on
        """
        for pendulum in self.pendulums.values():
            pendulum.render(surface)
            
    def create_pendulum(self, params):
        """
        Create a new pendulum with given parameters
        
        Args:
            params: PendulumParams object with initial values
            
        Returns:
            Pendulum: The newly created pendulum
        """
        pendulum_id = self.next_pendulum_id
        self.next_pendulum_id += 1
        
        pendulum = Pendulum(pendulum_id)
        pendulum.initialize(params)
        
        self.pendulums[pendulum_id] = pendulum
        
        # Select the newly created pendulum
        self.selected_pendulum = pendulum
        
        print(f"Created pendulum with ID: {pendulum_id}")
        return pendulum
        
    def remove_pendulum(self, pendulum_id):
        """
        Remove a pendulum from the system
        
        Args:
            pendulum_id: ID of the pendulum to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if pendulum_id in self.pendulums:
            # If removing the selected pendulum, clear selection
            if self.selected_pendulum and self.selected_pendulum.id == pendulum_id:
                self.selected_pendulum = None
                
            # Remove the pendulum
            del self.pendulums[pendulum_id]
            print(f"Removed pendulum with ID: {pendulum_id}")
            return True
        else:
            print(f"Pendulum with ID {pendulum_id} not found")
            return False
            
    def select_pendulum(self, pendulum_id):
        """
        Select a pendulum by ID
        
        Args:
            pendulum_id: ID of the pendulum to select
            
        Returns:
            Pendulum: The selected pendulum or None if not found
        """
        if pendulum_id in self.pendulums:
            self.selected_pendulum = self.pendulums[pendulum_id]
            print(f"Selected pendulum with ID: {pendulum_id}")
            return self.selected_pendulum
        else:
            print(f"Pendulum with ID {pendulum_id} not found")
            return None
            
    def get_pendulum_by_id(self, pendulum_id):
        """
        Get a pendulum by ID
        
        Args:
            pendulum_id: ID of the pendulum to get
            
        Returns:
            Pendulum: The pendulum or None if not found
        """
        return self.pendulums.get(pendulum_id)
        
    def get_selected_pendulum(self):
        """
        Get the currently selected pendulum
        
        Returns:
            Pendulum: The selected pendulum or None if none selected
        """
        return self.selected_pendulum
        
    def get_pendulum_count(self):
        """
        Get the number of pendulums in the system
        
        Returns:
            int: Number of pendulums
        """
        return len(self.pendulums)
        
    def clear(self):
        """Remove all pendulums from the system"""
        self.pendulums.clear()
        self.selected_pendulum = None
        print("Cleared all pendulums")
        
    def try_select_pendulum_at_position(self, position, screen_center):
        """
        Try to select a pendulum by position
        
        Args:
            position: (x, y) position to check
            screen_center: (x, y) center of the screen
            
        Returns:
            Pendulum: The selected pendulum or None if none at position
        """
        # Check each pendulum
        for pendulum in self.pendulums.values():
            # Adjust position to be relative to anchor point
            anchor_x = screen_center[0] + pendulum.offset_x
            anchor_y = screen_center[1] + pendulum.offset_y
            
            # Calculate screen positions of bobs
            screen_x1 = anchor_x + pendulum.x1
            screen_y1 = anchor_y + pendulum.y1
            screen_x2 = anchor_x + pendulum.x2
            screen_y2 = anchor_y + pendulum.y2
            
            # Check if position is near second bob
            dx2 = position[0] - screen_x2
            dy2 = position[1] - screen_y2
            dist2 = math.sqrt(dx2*dx2 + dy2*dy2)
            
            if dist2 <= max(10, pendulum.mass2):
                self.selected_pendulum = pendulum
                return pendulum
            
            # Check if position is near first bob
            dx1 = position[0] - screen_x1
            dy1 = position[1] - screen_y1
            dist1 = math.sqrt(dx1*dx1 + dy1*dy1)
            
            if dist1 <= max(10, pendulum.mass1):
                self.selected_pendulum = pendulum
                return pendulum
                
        # No pendulum found at position
        return None