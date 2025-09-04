r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Ashfall"

# Game-specific settings
GAME_NAME = "Ashfall"
GAME_SLOGAN = "A Post-Apocalyptic Western MUD"

# Maximum player level
MAX_PLAYER_LEVEL = 50

# Character creation settings
MULTISESSION_MODE = 0  # One session per account
MAX_NR_CHARACTERS = 1  # One character per account initially

# Time settings
IN_GAME_TIME_FACTOR = 1.0  # Real time = game time

# Combat settings
COMBAT_TIMEOUT = 30  # Seconds before combat times out
COMBAT_ANNOUNCE_ROUNDS = True

# Experience and leveling
BASE_EXP_GAIN = 100
LEVEL_EXP_MULTIPLIER = 1.2

# Remort settings
REQUIRED_REMORTS_FOR_ADVANCED_CLASS = 50

# Default home location (will be created if it doesn't exist)
DEFAULT_HOME = None


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
