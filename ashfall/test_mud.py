#!/usr/bin/env python
"""
Test script for Ashfall MUD
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.conf.settings')
django.setup()

# Now we can import Evennia components
from evennia.utils.create import create_object
from evennia.utils.search import search_object
from world.ashfall_world import create_ashfall_world

def main():
    print("Creating Ashfall MUD world...")
    
    # Check if world already exists
    neighborhood = search_object("Ruined Neighborhood")
    if neighborhood:
        print("World already exists!")
        return
    
    # First create a basic room to serve as home
    from typeclasses.rooms import Room
    home_room = create_object(Room, key="Limbo", 
                             aliases=["limbo", "home"])
    home_room.db.desc = "A featureless void. This is where new characters start."
    
    # Create the world
    starting_room = create_ashfall_world()
    print(f"World created! Starting room: {starting_room.key}")
    
    # Create a test character
    from typeclasses.characters import Character
    char = create_object(Character, key="TestChar", 
                        aliases=["test", "char"])
    char.db.desc = "A survivor of the wasteland, ready to face whatever challenges await."
    char.move_to(starting_room)
    
    print(f"Test character created: {char.key}")
    print("Ashfall MUD is ready!")

if __name__ == "__main__":
    main()