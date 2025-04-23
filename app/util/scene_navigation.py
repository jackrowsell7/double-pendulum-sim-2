"""
Scene navigation utilities for the double pendulum simulation
"""

# Global reference to the scene manager
_scene_manager = None

def initialize_navigator(scene_manager):
    """
    Initialize the scene navigator with a reference to the scene manager
    
    Args:
        scene_manager: The application's SceneManager instance
    """
    global _scene_manager
    _scene_manager = scene_manager
    
def change_scene(scene_name):
    """
    Change to a different scene
    
    Args:
        scene_name: Name of the scene to change to
        
    Returns:
        bool: True if successful, False if not
    """
    global _scene_manager
    if _scene_manager is None:
        print("Error: Scene navigator not initialized")
        return False
        
    return _scene_manager.change_scene(scene_name)
    
def get_current_scene_name():
    """
    Get the name of the current scene
    
    Returns:
        str: Name of the current scene or None if not available
    """
    global _scene_manager
    if _scene_manager is None:
        return None
        
    return _scene_manager.get_current_scene_name()