# Ashfall MUD

A post-apocalyptic MUD set in the western hemisphere (USA/Canada) after nuclear war, built with Evennia.

## Setting

Ashfall takes place in a post-apocalyptic world where nuclear war has devastated North America. Players are survivors in a ruined suburban neighborhood, exploring the remains of civilization and fighting for survival in a harsh wasteland.

## Character Classes

### Starting Classes
- **Warrior**: Strong fighters with high hit points and combat abilities
- **Mage**: Masters of magic with high intelligence and mana
- **Cleric**: Divine spellcasters with wisdom and healing abilities
- **Thief**: Agile rogues with high dexterity and stealth
- **Psionicist**: Mentalists with psychic powers and balanced stats

### Advanced Classes (Requires 50 remorts)
- **Warrior → Warlord/Juggernaut**: Enhanced combat specialists
- **Mage → Warlock/Arcanist**: Master spellcasters
- **Cleric → Inquisitor/Hierophant**: Divine champions
- **Thief → Assassin/Ashstalker**: Shadow warriors
- **Psionicist → Mindreaver/Seer**: Mental masters

## Game Features

### Combat System
- Real-time combat similar to tbaMUD
- Weapon-based damage with dice rolls
- Armor class and hit bonuses
- Automatic combat timers

### Character Progression
- Level cap: 50
- Experience-based leveling
- Remort system for advanced classes
- Stat increases on level up

### Spells and Abilities
- Class-specific spells and skills
- Mana-based spellcasting
- Psionic powers for psionicists
- Stealth skills for thieves

### World Areas
- **Ruined Neighborhood**: Starting area with abandoned houses
- **Convenience Store**: Looted store with basic supplies
- **Water Tower**: Overlook with view of the wasteland
- **Main Road**: Highway leading to city ruins
- **City Ruins**: Dangerous urban wasteland
- **Radiation Zone**: High-risk area with valuable loot
- **Underground Bunker**: Military facility with advanced gear

### Items and Equipment
- Post-apocalyptic weapons (rusty pipes, scrap metal clubs, laser pistols)
- Radiation suits and combat armor
- Medical supplies and radiation treatment
- Bottle caps as currency
- Energy cells for energy weapons

## Commands

### Character Management
- `chooseclass <class>` - Choose your character class
- `stats` - Display character statistics
- `remort` - Remort your character (requires level 50)
- `advancedclass <class>` - Choose advanced class (requires 50 remorts)
- `level` - Show level and experience information
- `classes` - List available classes

### Combat
- `kill <target>` - Attack another character
- `flee` - Attempt to flee from combat
- `cast <spell>` - Cast a spell
- `skills` - Display skills and spells
- `wield <weapon>` - Equip a weapon
- `wear <armor>` - Wear armor
- `equipment` - Show equipped items

### Movement and Interaction
- `look` - Look at your surroundings
- `go <direction>` - Move in a direction
- `get <item>` - Pick up an item
- `drop <item>` - Drop an item
- `inventory` - Show your inventory
- `say <message>` - Say something
- `rest` - Rest to recover health and mana

## Installation and Running

1. Install Evennia: `pip install evennia`
2. Navigate to the ashfall directory
3. Run: `evennia migrate` (first time only)
4. Run: `evennia start` to start the server
5. Connect via telnet to localhost:4000 or web browser to localhost:4001

## Development

The MUD is built using Evennia, a Python-based MUD framework. Key files:
- `typeclasses/characters.py` - Character class with stats, combat, and progression
- `commands/` - All game commands
- `world/ashfall_world.py` - World creation and areas
- `typeclasses/items.py` - Weapons, armor, and items
- `server/conf/settings.py` - Game configuration

## Credits

Built with Evennia MUD framework. Setting inspired by post-apocalyptic fiction and games.