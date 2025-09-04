"""
Ashfall MUD World Builder
Creates the post-apocalyptic western themed world
"""

from evennia import create_object, search_object
from evennia.objects.objects import DefaultRoom, DefaultExit
from typeclasses.rooms import Room
from typeclasses.exits import Exit
from typeclasses.items import *


def create_ashfall_world():
    """Create the Ashfall MUD world"""
    
    # Create the starting area - a ruined town
    town_square = create_object(Room, key="Town Square", 
                               aliases=["square", "town"])
    town_square.db.desc = """
The heart of what was once a thriving frontier town, now reduced to rubble and ash.
Broken buildings line the dusty streets, their windows shattered and doors hanging
loose on rusted hinges. A weathered wooden sign creaks in the hot wind, its faded
paint barely readable: "Welcome to Ashfall."

To the north, a partially collapsed saloon still stands, its swinging doors now
motionless. To the south, the remains of a general store offer little more than
broken shelves and scattered debris. Eastward, a rusted water tower leans precariously,
while to the west, the town's main street stretches into the distance.
"""
    
    # Create exits from town square
    create_object(Exit, key="north", aliases=["n"], 
                 location=town_square, destination=None)
    create_object(Exit, key="south", aliases=["s"], 
                 location=town_square, destination=None)
    create_object(Exit, key="east", aliases=["e"], 
                 location=town_square, destination=None)
    create_object(Exit, key="west", aliases=["w"], 
                 location=town_square, destination=None)
    
    # Create the saloon
    saloon = create_object(Room, key="Broken Saloon", 
                          aliases=["saloon", "bar"])
    saloon.db.desc = """
The saloon's interior is a shadow of its former glory. Dusty tables and chairs
are scattered about, some overturned, others broken beyond repair. The bar itself
is cracked and splintered, its mirror shattered into countless pieces that still
cling to the wall like jagged teeth.

A piano sits in the corner, its keys yellowed and cracked, silent forever.
The swinging doors that once welcomed travelers now hang broken and still.
The air is thick with the smell of old wood, dust, and something else - perhaps
the lingering memory of better times.
"""
    
    # Create the general store
    general_store = create_object(Room, key="Ruined General Store", 
                                 aliases=["store", "shop"])
    general_store.db.desc = """
The general store has been picked clean by scavengers and time. Empty shelves
line the walls, their wood warped and splintered. Broken glass crunches underfoot
as you step through the debris. A few items remain scattered about - mostly
useless junk, but perhaps something of value might be found among the ruins.

The cash register sits open and empty on the counter, its drawer long since
looted. Dust motes dance in the shafts of light that filter through the
broken windows, creating an almost ethereal atmosphere in this place of
abandoned commerce.
"""
    
    # Create the water tower area
    water_tower = create_object(Room, key="Water Tower", 
                               aliases=["tower", "water"])
    water_tower.db.desc = """
The water tower stands as a rusted monument to the town's past prosperity.
Its metal sides are pitted and corroded, and the tank itself is empty and
dry. The ladder that once led to the top is broken and dangerous, with
several rungs missing entirely.

From here, you can see the extent of the town's destruction - buildings
reduced to rubble, streets cracked and broken, and the endless wasteland
beyond. The wind carries the sound of creaking metal and the occasional
screech of a scavenger bird.
"""
    
    # Create the main street
    main_street = create_object(Room, key="Main Street", 
                               aliases=["street", "road"])
    main_street.db.desc = """
The main street of Ashfall stretches westward, its asphalt cracked and
broken by years of neglect and the harsh elements. Abandoned vehicles
line the sides of the road, their tires flat and windows shattered.
Some have been stripped of anything valuable, while others remain
relatively intact, frozen in time.

The buildings along the street tell the story of a town that once
thrived - a bank with its vault door hanging open, a hotel with
its rooms exposed to the elements, and various shops and businesses
that have long since been abandoned or destroyed.
"""
    
    # Create the wasteland
    wasteland = create_object(Room, key="Wasteland", 
                             aliases=["desert", "waste"])
    wasteland.db.desc = """
The wasteland stretches endlessly in all directions, a barren landscape
of sand, rock, and twisted metal. The ground is littered with the
remains of the old world - rusted cars, broken machinery, and the
occasional skeleton of some unfortunate soul who didn't make it.

The air is hot and dry, and the sun beats down mercilessly from a
cloudless sky. In the distance, you can see the faint outline of
mountains, and perhaps the ruins of other settlements. This is a
harsh land, where only the strong and resourceful survive.
"""
    
    # Create the radiation zone
    radiation_zone = create_object(Room, key="Radiation Zone", 
                                  aliases=["rad", "zone"])
    radiation_zone.db.desc = """
This area is heavily contaminated with radiation from the old war.
The ground glows faintly in places, and the air shimmers with
distorted light. Strange mutations can be seen in the few plants
that manage to survive here, their forms twisted and unnatural.

The radiation is dangerous to unprotected travelers, but the area
is also rich in pre-war technology and resources. Only those with
proper protection should venture here, and even then, not for long.
"""
    
    # Create the old mine
    old_mine = create_object(Room, key="Old Mine", 
                            aliases=["mine", "cave"])
    old_mine.db.desc = """
The entrance to an old mine shaft, its wooden supports creaking
ominously in the darkness. The air is cool and damp, and the
sound of dripping water echoes from somewhere deep within.

The mine was once a source of wealth for the town, but now it
stands as a dangerous reminder of the past. The tunnels are
dark and treacherous, but they may still contain valuable
minerals or other resources for those brave enough to explore.
"""
    
    # Connect the rooms
    # Town Square connections
    town_square.exits.get("north").destination = saloon
    town_square.exits.get("south").destination = general_store
    town_square.exits.get("east").destination = water_tower
    town_square.exits.get("west").destination = main_street
    
    # Create reverse exits
    create_object(Exit, key="south", aliases=["s"], 
                 location=saloon, destination=town_square)
    create_object(Exit, key="north", aliases=["n"], 
                 location=general_store, destination=town_square)
    create_object(Exit, key="west", aliases=["w"], 
                 location=water_tower, destination=town_square)
    create_object(Exit, key="east", aliases=["e"], 
                 location=main_street, destination=town_square)
    
    # Main street connections
    create_object(Exit, key="west", aliases=["w"], 
                 location=main_street, destination=wasteland)
    create_object(Exit, key="east", aliases=["e"], 
                 location=wasteland, destination=main_street)
    
    # Wasteland connections
    create_object(Exit, key="north", aliases=["n"], 
                 location=wasteland, destination=radiation_zone)
    create_object(Exit, key="south", aliases=["s"], 
                 location=radiation_zone, destination=wasteland)
    
    create_object(Exit, key="east", aliases=["e"], 
                 location=wasteland, destination=old_mine)
    create_object(Exit, key="west", aliases=["w"], 
                 location=old_mine, destination=wasteland)
    
    # Create some items in the world
    create_items_in_world()
    
    return town_square


def create_items_in_world():
    """Create items scattered throughout the world"""
    
    # Items in town square
    town_square = search_object("Town Square")[0]
    rusty_pipe = create_object(RustyPipe, key="rusty pipe", 
                              aliases=["pipe", "weapon"])
    rusty_pipe.move_to(town_square, quiet=True)
    
    # Items in saloon
    saloon = search_object("Broken Saloon")[0]
    leather_duster = create_object(LeatherDuster, key="leather duster", 
                                  aliases=["duster", "coat"])
    leather_duster.move_to(saloon, quiet=True)
    
    # Items in general store
    general_store = search_object("Ruined General Store")[0]
    water_canteen = create_object(WaterCanteen, key="water canteen", 
                                 aliases=["canteen", "water"])
    water_canteen.move_to(general_store, quiet=True)
    
    medkit = create_object(Medkit, key="medical kit", 
                          aliases=["medkit", "med"])
    medkit.move_to(general_store, quiet=True)
    
    # Items in wasteland
    wasteland = search_object("Wasteland")[0]
    scrap_metal_club = create_object(ScrapMetalClub, key="scrap metal club", 
                                    aliases=["club", "weapon"])
    scrap_metal_club.move_to(wasteland, quiet=True)
    
    # Items in radiation zone
    radiation_zone = search_object("Radiation Zone")[0]
    radiation_suit = create_object(RadiationSuit, key="radiation suit", 
                                  aliases=["suit", "armor"])
    radiation_suit.move_to(radiation_zone, quiet=True)
    
    rad_away = create_object(RadAway, key="rad-away", 
                            aliases=["medicine", "rad"])
    rad_away.move_to(radiation_zone, quiet=True)
    
    # Items in old mine
    old_mine = search_object("Old Mine")[0]
    laser_pistol = create_object(LaserPistol, key="laser pistol", 
                                aliases=["pistol", "laser"])
    laser_pistol.move_to(old_mine, quiet=True)
    
    energy_cell = create_object(EnergyCell, key="energy cell", 
                               aliases=["cell", "battery"])
    energy_cell.move_to(old_mine, quiet=True)
    
    # Currency scattered around
    caps1 = create_object(Caps, key="bottle cap", aliases=["cap"])
    caps1.move_to(town_square, quiet=True)
    
    caps2 = create_object(Caps, key="bottle cap", aliases=["cap"])
    caps2.move_to(saloon, quiet=True)
    
    caps3 = create_object(Caps, key="bottle cap", aliases=["cap"])
    caps3.move_to(general_store, quiet=True)


def create_starting_character():
    """Create a starting character for testing"""
    from evennia import create_object
    from typeclasses.characters import Character
    
    char = create_object(Character, key="TestChar", 
                        aliases=["test", "char"])
    char.db.desc = "A survivor of the wasteland, ready to face whatever challenges await."
    
    # Move to town square
    town_square = search_object("Town Square")[0]
    char.move_to(town_square)
    
    return char


if __name__ == "__main__":
    # Create the world when this script is run
    starting_room = create_ashfall_world()
    print(f"Ashfall world created! Starting room: {starting_room.key}")