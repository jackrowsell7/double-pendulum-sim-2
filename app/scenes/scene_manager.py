"""
SceneManager - Manages the application's scenes and scene transitions
"""

class Scene:
    """
    Base interface for all scenes in the application
    Each scene represents a distinct screen or state in the application
    """
    
    def initialize(self, surface, config_manager):
        """
        Initialize the scene with required resources
        
        Args:
            surface: The pygame surface to render on
            config_manager: The application's configuration manager
        """
        pass
        
    def update(self, dt):
        """
        Update scene logic
        
        Args:
            dt: Delta time in seconds since last update
        """
        pass
        
    def render(self):
        """Render the scene to its surface"""
        pass
        
    def handle_event(self, event):
        """
        Process pygame events
        
        Args:
            event: The pygame event to handle
        """
        pass
        
    def cleanup(self):
        """Release scene resources"""
        pass


class SceneManager:
    """
    Manages scenes and transitions between them
    """
    
    def __init__(self, surface, config_manager):
        """
        Initialize the scene manager
        
        Args:
            surface: The pygame surface to render on
            config_manager: The application's configuration manager
        """
        self.surface = surface
        self.config_manager = config_manager
        self.scenes = {}  # Maps scene names to scene classes
        self.current_scene = None
        self.current_scene_name = None
        
    def register_scene(self, name, scene_class):
        """
        Register a scene with the scene manager
        
        Args:
            name: Unique name for the scene
            scene_class: Class of the scene to register
        """
        self.scenes[name] = scene_class
        print(f"Registered scene: {name}")
        
    def change_scene(self, scene_name):
        """
        Change to a different scene
        
        Args:
            scene_name: Name of the scene to change to
            
        Returns:
            bool: True if successful, False if scene not found
        """
        # Check if the requested scene exists
        if scene_name not in self.scenes:
            print(f"Scene not found: {scene_name}")
            return False
            
        # Clean up current scene if one exists
        if self.current_scene is not None:
            self.current_scene.cleanup()
            
        # Create new scene instance
        scene_class = self.scenes[scene_name]
        self.current_scene = scene_class()
        self.current_scene_name = scene_name
        
        # Initialize the new scene
        self.current_scene.initialize(self.surface, self.config_manager)
        
        print(f"Changed to scene: {scene_name}")
        return True
        
    def update(self, dt):
        """
        Update the current scene
        
        Args:
            dt: Delta time in seconds since last update
        """
        if self.current_scene is not None:
            self.current_scene.update(dt)
            
    def render(self):
        """Render the current scene"""
        if self.current_scene is not None:
            self.current_scene.render()
            
    def handle_event(self, event):
        """
        Pass an event to the current scene
        
        Args:
            event: The pygame event to handle
        """
        if self.current_scene is not None:
            self.current_scene.handle_event(event)
            
    def get_current_scene_name(self):
        """
        Get the name of the current scene
        
        Returns:
            str: Name of the current scene or None if no scene is active
        """
        return self.current_scene_name
        
    def cleanup(self):
        """Clean up all scenes and resources"""
        if self.current_scene is not None:
            self.current_scene.cleanup()
            self.current_scene = None
            self.current_scene_name = None