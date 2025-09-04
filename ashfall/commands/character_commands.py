"""
Character creation and management commands for Ashfall MUD
"""

from evennia import Command
from evennia.utils import create, search
from django.conf import settings


class CmdChooseClass(Command):
    """
    Choose your character class
    
    Usage:
        chooseclass <class>
        
    Available classes:
        warrior - Strong fighters with high hit points and combat abilities
        mage - Masters of magic with high intelligence and mana
        cleric - Divine spellcasters with wisdom and healing abilities
        thief - Agile rogues with high dexterity and stealth
        psionicist - Mentalists with psychic powers and balanced stats
    """
    
    key = "chooseclass"
    aliases = ["class", "choose"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Usage: chooseclass <class>")
            self.caller.msg("Available classes: warrior, mage, cleric, thief, psionicist")
            return
            
        class_name = self.args.lower().strip()
        valid_classes = ['warrior', 'mage', 'cleric', 'thief', 'psionicist']
        
        if class_name not in valid_classes:
            self.caller.msg(f"Invalid class. Available classes: {', '.join(valid_classes)}")
            return
            
        if self.caller.get_class_name() != "None":
            self.caller.msg(f"You are already a {self.caller.get_class_name()}!")
            return
            
        if self.caller.set_class(class_name):
            self.caller.msg(f"You have chosen the {class_name} class!")
            self.caller.msg("Your stats have been adjusted based on your class choice.")
            self.caller.msg("Use 'stats' to see your current statistics.")
        else:
            self.caller.msg("Failed to set class. Please try again.")


class CmdStats(Command):
    """
    Display your character statistics
    
    Usage:
        stats
    """
    
    key = "stats"
    aliases = ["stat", "score"]
    locks = "cmd:all()"
    
    def func(self):
        self.caller.msg(self.caller.get_stat_display())


class CmdRemort(Command):
    """
    Remort your character to gain power
    
    Usage:
        remort
        
    You must be at maximum level (50) to remort.
    Each remort increases your potential power.
    After 50 remorts, you can choose an advanced class.
    """
    
    key = "remort"
    locks = "cmd:all()"
    
    def func(self):
        if self.caller.remort():
            self.caller.msg("Remort successful!")
        else:
            self.caller.msg("You must reach maximum level before you can remort!")


class CmdAdvancedClass(Command):
    """
    Choose an advanced class (requires 50 remorts)
    
    Usage:
        advancedclass <class>
        
    Available advanced classes by base class:
        Warrior: warlord, juggernaut
        Mage: warlock, arcanist
        Cleric: inquisitor, hierophant
        Thief: assassin, ashstalker
        Psionicist: mindreaver, seer
    """
    
    key = "advancedclass"
    aliases = ["advclass", "advanced"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Usage: advancedclass <class>")
            if self.caller.can_choose_advanced_class():
                class_name = self.caller.get_class_name()
                valid_classes = self.caller.get_valid_advanced_classes(class_name)
                self.caller.msg(f"Available advanced classes for {class_name}: {', '.join(valid_classes)}")
            else:
                self.caller.msg("You need 50 remorts to choose an advanced class!")
            return
            
        advanced_class = self.args.lower().strip()
        
        if self.caller.set_advanced_class(advanced_class):
            self.caller.msg("Advanced class set successfully!")
        else:
            self.caller.msg("Failed to set advanced class.")


class CmdLevel(Command):
    """
    Display level and experience information
    
    Usage:
        level
    """
    
    key = "level"
    aliases = ["lvl", "exp"]
    locks = "cmd:all()"
    
    def func(self):
        level = self.caller.get_level()
        exp = self.caller.get_experience()
        remorts = self.caller.get_remorts()
        
        if level < getattr(settings, 'MAX_PLAYER_LEVEL', 50):
            next_level_exp = self.caller.get_exp_for_level(level + 1)
            exp_needed = next_level_exp - exp
            self.caller.msg(f"Level: {level} | Experience: {exp} | Remorts: {remorts}")
            self.caller.msg(f"Experience needed for next level: {exp_needed}")
        else:
            self.caller.msg(f"Level: {level} (MAX) | Experience: {exp} | Remorts: {remorts}")
            self.caller.msg("You are at maximum level! Use 'remort' to advance further.")


class CmdClasses(Command):
    """
    Display information about available classes
    
    Usage:
        classes
    """
    
    key = "classes"
    aliases = ["classlist"]
    locks = "cmd:all()"
    
    def func(self):
        self.caller.msg("""
Available Starting Classes:

Warrior - Strong fighters with high hit points and combat abilities
  +2 Strength, +1 Constitution, +20 HP
  Advanced: Warlord, Juggernaut

Mage - Masters of magic with high intelligence and mana
  +3 Intelligence, +50 Mana
  Advanced: Warlock, Arcanist

Cleric - Divine spellcasters with wisdom and healing abilities
  +3 Wisdom, +30 Mana, +10 HP
  Advanced: Inquisitor, Hierophant

Thief - Agile rogues with high dexterity and stealth
  +3 Dexterity, +10 HP
  Advanced: Assassin, Ashstalker

Psionicist - Mentalists with psychic powers and balanced stats
  +2 Intelligence, +2 Wisdom, +40 Mana, +10 HP
  Advanced: Mindreaver, Seer

Use 'chooseclass <class>' to select your class.
Use 'advancedclass <class>' to select advanced class (requires 50 remorts).
""")


class CmdRest(Command):
    """
    Rest to recover hit points and mana
    
    Usage:
        rest
    """
    
    key = "rest"
    aliases = ["sleep"]
    locks = "cmd:all()"
    
    def func(self):
        if self.caller.db.is_combat:
            self.caller.msg("You cannot rest while in combat!")
            return
            
        if self.caller.db.is_resting:
            self.caller.msg("You are already resting.")
            return
            
        self.caller.db.is_resting = True
        self.caller.msg("You sit down and rest.")
        self.caller.location.msg_contents(f"{self.caller.key} sits down to rest.", exclude=self.caller)
        
        # Start recovery process
        self.caller.start_recovery()


class CmdStand(Command):
    """
    Stand up from resting
    
    Usage:
        stand
    """
    
    key = "stand"
    locks = "cmd:all()"
    
    def func(self):
        if not self.caller.db.is_resting:
            self.caller.msg("You are not resting.")
            return
            
        self.caller.db.is_resting = False
        self.caller.msg("You stand up.")
        self.caller.location.msg_contents(f"{self.caller.key} stands up.", exclude=self.caller)