"""
World initialization script for Ashfall MUD
"""

from evennia import Script
from world.ashfall_world import create_ashfall_world


class WorldInitScript(Script):
    """
    Script that initializes the Ashfall world when the server starts
    """
    
    def at_script_creation(self):
        """Called when script is created"""
        self.key = "world_init"
        self.desc = "Initializes the Ashfall MUD world"
        self.interval = 0  # Run once
        self.repeats = 0   # Don't repeat
        self.persistent = False
        
    def at_repeat(self):
        """Called when script repeats (which it won't)"""
        pass
        
    def at_start(self):
        """Called when script starts"""
        # Check if world already exists
        from evennia import search_object
        
        neighborhood = search_object("Ruined Neighborhood")
        if neighborhood:
            self.obj.msg("World already exists, skipping initialization.")
            return
            
        # Create the world
        self.obj.msg("Initializing Ashfall MUD world...")
        starting_room = create_ashfall_world()
        self.obj.msg(f"World initialized! Starting room: {starting_room.key}")
        
        # Stop the script
        self.stop()