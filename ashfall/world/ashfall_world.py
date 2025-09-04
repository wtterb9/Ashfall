"""
Ashfall MUD World Builder
Creates the post-apocalyptic western themed world
"""

from evennia.utils.create import create_object
from evennia.utils.search import search_object
from evennia.objects.objects import DefaultRoom, DefaultExit
from typeclasses.rooms import Room
from typeclasses.exits import Exit
from typeclasses.items import *


def create_ashfall_world():
    """Create the Ashfall MUD world"""
    
    # Create the starting area - a ruined suburban neighborhood
    neighborhood = create_object(Room, key="Ruined Neighborhood", 
                               aliases=["neighborhood", "suburbs"])
    neighborhood.db.desc = """
The remains of what was once a typical American suburban neighborhood, now
devastated by nuclear war and decades of decay. Rows of houses stand in
various states of destruction - some completely collapsed, others with
walls missing and roofs caved in. The streets are cracked and overgrown
with weeds, and the occasional stop sign still stands, rusted and bent.

A faded "Welcome to Ashfall" sign lies broken on the ground, its letters
barely legible. To the north, a partially standing house offers some
shelter. To the south, the remains of a convenience store can be seen.
Eastward, a rusted water tower leans precariously, while to the west,
the main road stretches toward the city ruins.
"""
    
    # Create exits from neighborhood (will be connected later)
    north_exit = create_object(Exit, key="north", aliases=["n"], 
                              location=neighborhood, destination=None)
    south_exit = create_object(Exit, key="south", aliases=["s"], 
                              location=neighborhood, destination=None)
    east_exit = create_object(Exit, key="east", aliases=["e"], 
                             location=neighborhood, destination=None)
    west_exit = create_object(Exit, key="west", aliases=["w"], 
                             location=neighborhood, destination=None)
    
    # Create the abandoned house
    abandoned_house = create_object(Room, key="Abandoned House", 
                          aliases=["house", "home"])
    abandoned_house.db.desc = """
The interior of what was once a typical American home, now a shell of its
former self. The living room furniture is overturned and covered in dust,
the television screen shattered. Family photos still hang on the walls,
their faces faded and cracked, silent witnesses to a life that once was.

The kitchen is a mess of broken dishes and rusted appliances. The refrigerator
stands open and empty, its door hanging loose on broken hinges. Upstairs,
the bedrooms are in similar disarray, with mattresses torn and dressers
overturned. The air is thick with dust and the smell of decay.
"""
    
    # Create the convenience store
    convenience_store = create_object(Room, key="Ruined Convenience Store", 
                                 aliases=["store", "shop", "convenience"])
    convenience_store.db.desc = """
The convenience store has been thoroughly looted over the years. Empty shelves
line the walls, their metal frames rusted and bent. The coolers that once
held drinks are now empty and broken, their glass doors shattered. The
floor is littered with debris - broken bottles, torn packaging, and the
occasional piece of pre-war currency.

The cash register sits on the counter, its drawer long since emptied.
The security cameras that once watched over the store now hang from
their mounts, their lenses cracked and useless. A few items might
still be found among the ruins, but most of value has long since
been taken by scavengers.
"""
    
    # Create the water tower area
    water_tower = create_object(Room, key="Water Tower", 
                               aliases=["tower", "water"])
    water_tower.db.desc = """
The water tower stands as a rusted monument to the neighborhood's past
prosperity. Its metal sides are pitted and corroded, and the tank itself
is empty and dry. The ladder that once led to the top is broken and
dangerous, with several rungs missing entirely.

From here, you can see the extent of the destruction - suburban homes
reduced to rubble, streets cracked and broken, and the endless wasteland
beyond. The wind carries the sound of creaking metal and the occasional
screech of a scavenger bird. In the distance, the ruins of a major
city can be seen on the horizon.
"""
    
    # Create the main road
    main_road = create_object(Room, key="Main Road", 
                               aliases=["road", "highway"])
    main_road.db.desc = """
The main road stretches westward toward the city ruins, its asphalt
cracked and broken by years of neglect and the harsh elements.
Abandoned vehicles line the sides of the road, their tires flat and
windows shattered. Some have been stripped of anything valuable,
while others remain relatively intact, frozen in time.

The road signs that once guided travelers now hang broken and bent,
their messages faded and unreadable. The occasional traffic light
still stands, its glass shattered and its lights forever dark.
This was once a busy thoroughfare, but now it serves only as a
path for the few survivors who dare to travel these dangerous lands.
"""
    
    # Create the city ruins
    city_ruins = create_object(Room, key="City Ruins", 
                             aliases=["city", "ruins", "downtown"])
    city_ruins.db.desc = """
The skeletal remains of what was once a major American city, now reduced
to towering piles of rubble and twisted metal. Skyscrapers that once
reached toward the sky now lie in broken heaps, their steel frames
exposed and rusted. The streets are choked with debris, and the
occasional intact building stands as a lonely monument to the past.

The air is thick with dust and the smell of decay. The sound of
collapsing masonry echoes occasionally from the ruins, a reminder
that this place is still dangerous. Despite the destruction,
valuable pre-war technology and resources can still be found
among the rubble for those brave enough to search.
"""
    
    # Create the radiation zone
    radiation_zone = create_object(Room, key="Radiation Zone", 
                                  aliases=["rad", "zone", "hotspot"])
    radiation_zone.db.desc = """
This area is heavily contaminated with radiation from the nuclear
war that destroyed the old world. The ground glows faintly in
places, and the air shimmers with distorted light. Strange
mutations can be seen in the few plants that manage to survive
here, their forms twisted and unnatural.

The radiation is dangerous to unprotected travelers, but the area
is also rich in pre-war technology and resources. Military
bunkers and research facilities can be found here, their
contents potentially valuable to survivors. Only those with
proper protection should venture here, and even then, not for long.
"""
    
    # Create the underground bunker
    bunker = create_object(Room, key="Underground Bunker", 
                            aliases=["bunker", "shelter", "basement"])
    bunker.db.desc = """
The entrance to an underground bunker, its heavy steel door hanging
open on broken hinges. The air is cool and damp, and the sound
of dripping water echoes from somewhere deep within. The walls
are lined with pipes and conduits, many of them broken or
disconnected.

This bunker was built during the Cold War era, designed to protect
its occupants from nuclear attack. Now it stands as a testament
to the futility of such preparations. The tunnels are dark and
treacherous, but they may still contain valuable supplies,
weapons, or other resources for those brave enough to explore.
"""
    
    # Connect the rooms
    # Neighborhood connections
    north_exit.destination = abandoned_house
    south_exit.destination = convenience_store
    east_exit.destination = water_tower
    west_exit.destination = main_road
    
    # Create reverse exits
    create_object(Exit, key="south", aliases=["s"], 
                 location=abandoned_house, destination=neighborhood)
    create_object(Exit, key="north", aliases=["n"], 
                 location=convenience_store, destination=neighborhood)
    create_object(Exit, key="west", aliases=["w"], 
                 location=water_tower, destination=neighborhood)
    create_object(Exit, key="east", aliases=["e"], 
                 location=main_road, destination=neighborhood)
    
    # Main road connections
    create_object(Exit, key="west", aliases=["w"], 
                 location=main_road, destination=city_ruins)
    create_object(Exit, key="east", aliases=["e"], 
                 location=city_ruins, destination=main_road)
    
    # City ruins connections
    create_object(Exit, key="north", aliases=["n"], 
                 location=city_ruins, destination=radiation_zone)
    create_object(Exit, key="south", aliases=["s"], 
                 location=radiation_zone, destination=city_ruins)
    
    create_object(Exit, key="east", aliases=["e"], 
                 location=city_ruins, destination=bunker)
    create_object(Exit, key="west", aliases=["w"], 
                 location=bunker, destination=city_ruins)
    
    # Create some items in the world
    create_items_in_world()
    
    return neighborhood


def create_items_in_world():
    """Create items scattered throughout the world"""
    
    # Items in neighborhood
    neighborhood = search_object("Ruined Neighborhood")[0]
    rusty_pipe = create_object(RustyPipe, key="rusty pipe", 
                              aliases=["pipe", "weapon"])
    rusty_pipe.move_to(neighborhood, quiet=True)
    
    # Items in abandoned house
    abandoned_house = search_object("Abandoned House")[0]
    leather_duster = create_object(LeatherDuster, key="leather duster", 
                                  aliases=["duster", "coat"])
    leather_duster.move_to(abandoned_house, quiet=True)
    
    # Items in convenience store
    convenience_store = search_object("Ruined Convenience Store")[0]
    water_canteen = create_object(WaterCanteen, key="water canteen", 
                                 aliases=["canteen", "water"])
    water_canteen.move_to(convenience_store, quiet=True)
    
    medkit = create_object(Medkit, key="medical kit", 
                          aliases=["medkit", "med"])
    medkit.move_to(convenience_store, quiet=True)
    
    # Items in city ruins
    city_ruins = search_object("City Ruins")[0]
    scrap_metal_club = create_object(ScrapMetalClub, key="scrap metal club", 
                                    aliases=["club", "weapon"])
    scrap_metal_club.move_to(city_ruins, quiet=True)
    
    # Items in radiation zone
    radiation_zone = search_object("Radiation Zone")[0]
    radiation_suit = create_object(RadiationSuit, key="radiation suit", 
                                  aliases=["suit", "armor"])
    radiation_suit.move_to(radiation_zone, quiet=True)
    
    rad_away = create_object(RadAway, key="rad-away", 
                            aliases=["medicine", "rad"])
    rad_away.move_to(radiation_zone, quiet=True)
    
    # Items in bunker
    bunker = search_object("Underground Bunker")[0]
    laser_pistol = create_object(LaserPistol, key="laser pistol", 
                                aliases=["pistol", "laser"])
    laser_pistol.move_to(bunker, quiet=True)
    
    energy_cell = create_object(EnergyCell, key="energy cell", 
                               aliases=["cell", "battery"])
    energy_cell.move_to(bunker, quiet=True)
    
    # Currency scattered around
    caps1 = create_object(Caps, key="bottle cap", aliases=["cap"])
    caps1.move_to(neighborhood, quiet=True)
    
    caps2 = create_object(Caps, key="bottle cap", aliases=["cap"])
    caps2.move_to(abandoned_house, quiet=True)
    
    caps3 = create_object(Caps, key="bottle cap", aliases=["cap"])
    caps3.move_to(convenience_store, quiet=True)


def create_starting_character():
    """Create a starting character for testing"""
    from evennia import create_object
    from typeclasses.characters import Character
    
    char = create_object(Character, key="TestChar", 
                        aliases=["test", "char"])
    char.db.desc = "A survivor of the wasteland, ready to face whatever challenges await."
    
    # Move to neighborhood
    neighborhood = search_object("Ruined Neighborhood")[0]
    char.move_to(neighborhood)
    
    return char


if __name__ == "__main__":
    # Create the world when this script is run
    starting_room = create_ashfall_world()
    print(f"Ashfall world created! Starting room: {starting_room.key}")