"""
Movement and basic interaction commands for Ashfall MUD
"""

from evennia import Command
from evennia.utils import search


class CmdLook(Command):
    """
    Look at something or your surroundings
    
    Usage:
        look
        look <object>
        look <direction>
    """
    
    key = "look"
    aliases = ["l"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            # Look at room
            self.caller.msg(self.caller.location.return_appearance(self.caller))
            return
            
        # Look at specific object or direction
        target = self.caller.search(self.args)
        if target:
            self.caller.msg(target.return_appearance(self.caller))
        else:
            # Check if it's a direction
            direction = self.args.lower()
            if direction in ['north', 'south', 'east', 'west', 'up', 'down', 'n', 's', 'e', 'w', 'u', 'd']:
                # Look in direction
                exit = self.caller.location.exits.get(direction)
                if exit:
                    self.caller.msg(f"You look {direction} and see {exit.destination.key}.")
                else:
                    self.caller.msg(f"You look {direction} but see nothing special.")
            else:
                self.caller.msg(f"You don't see '{self.args}' here.")


class CmdGo(Command):
    """
    Move in a direction
    
    Usage:
        go <direction>
        <direction>
    """
    
    key = "go"
    aliases = ["north", "south", "east", "west", "up", "down", "n", "s", "e", "w", "u", "d"]
    locks = "cmd:all()"
    
    def func(self):
        if self.cmdstring == "go":
            if not self.args:
                self.caller.msg("Go where?")
                return
            direction = self.args.lower()
        else:
            direction = self.cmdstring.lower()
            
        # Check if in combat
        if self.caller.db.is_combat:
            self.caller.msg("You cannot move while in combat!")
            return
            
        # Find exit
        exit = self.caller.location.exits.get(direction)
        if not exit:
            self.caller.msg("You cannot go that way.")
            return
            
        # Move
        self.caller.move_to(exit.destination)
        self.caller.msg(f"You go {direction}.")
        self.caller.location.msg_contents(f"{self.caller.key} arrives from the {self.get_reverse_direction(direction)}.", 
                                        exclude=self.caller)
        
        # Look at new location
        self.caller.msg(self.caller.location.return_appearance(self.caller))
    
    def get_reverse_direction(self, direction):
        """Get reverse direction for arrival message"""
        reverse_dirs = {
            'north': 'south', 'south': 'north',
            'east': 'west', 'west': 'east',
            'up': 'down', 'down': 'up',
            'n': 'south', 's': 'north',
            'e': 'west', 'w': 'east',
            'u': 'down', 'd': 'up'
        }
        return reverse_dirs.get(direction, 'unknown')


class CmdGet(Command):
    """
    Pick up an object
    
    Usage:
        get <object>
        get all
    """
    
    key = "get"
    aliases = ["take", "pickup"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Get what?")
            return
            
        if self.args.lower() == "all":
            # Get all items in room
            items = [obj for obj in self.caller.location.contents 
                    if obj != self.caller and not obj.has_account]
            if not items:
                self.caller.msg("There is nothing here to get.")
                return
            for item in items:
                self.get_item(item)
        else:
            item = self.caller.search(self.args)
            if item:
                self.get_item(item)
    
    def get_item(self, item):
        """Get a specific item"""
        if item.has_account:
            self.caller.msg("You cannot get other players!")
            return
            
        if item.move_to(self.caller):
            self.caller.msg(f"You get {item.key}.")
            self.caller.location.msg_contents(f"{self.caller.key} gets {item.key}.", 
                                            exclude=self.caller)
        else:
            self.caller.msg(f"You cannot get {item.key}.")


class CmdDrop(Command):
    """
    Drop an object
    
    Usage:
        drop <object>
        drop all
    """
    
    key = "drop"
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Drop what?")
            return
            
        if self.args.lower() == "all":
            # Drop all items
            items = [obj for obj in self.caller.contents 
                    if not obj.has_account and obj != self.caller]
            if not items:
                self.caller.msg("You have nothing to drop.")
                return
            for item in items:
                self.drop_item(item)
        else:
            item = self.caller.search(self.args)
            if item:
                self.drop_item(item)
    
    def drop_item(self, item):
        """Drop a specific item"""
        if item.has_account:
            self.caller.msg("You cannot drop other players!")
            return
            
        if item.move_to(self.caller.location):
            self.caller.msg(f"You drop {item.key}.")
            self.caller.location.msg_contents(f"{self.caller.key} drops {item.key}.", 
                                            exclude=self.caller)
        else:
            self.caller.msg(f"You cannot drop {item.key}.")


class CmdInventory(Command):
    """
    Display your inventory
    
    Usage:
        inventory
    """
    
    key = "inventory"
    aliases = ["i", "inv"]
    locks = "cmd:all()"
    
    def func(self):
        items = [obj for obj in self.caller.contents 
                if not obj.has_account and obj != self.caller]
        
        if not items:
            self.caller.msg("You are carrying nothing.")
            return
            
        self.caller.msg("You are carrying:")
        for item in items:
            self.caller.msg(f"  {item.key}")


class CmdSay(Command):
    """
    Say something
    
    Usage:
        say <message>
    """
    
    key = "say"
    aliases = ["'"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Say what?")
            return
            
        message = self.args
        self.caller.msg(f"You say, \"{message}\"")
        self.caller.location.msg_contents(f"{self.caller.key} says, \"{message}\"", 
                                        exclude=self.caller)


class CmdShout(Command):
    """
    Shout something (heard by everyone in the area)
    
    Usage:
        shout <message>
    """
    
    key = "shout"
    aliases = ["yell"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Shout what?")
            return
            
        message = self.args
        self.caller.msg(f"You shout, \"{message}\"")
        
        # Send to all characters in the area
        for char in self.caller.location.contents:
            if char.has_account and char != self.caller:
                char.msg(f"{self.caller.key} shouts, \"{message}\"")


class CmdEmote(Command):
    """
    Perform an emote
    
    Usage:
        emote <action>
    """
    
    key = "emote"
    aliases = [":", "pose"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Emote what?")
            return
            
        action = self.args
        self.caller.msg(f"You {action}")
        self.caller.location.msg_contents(f"{self.caller.key} {action}", 
                                        exclude=self.caller)


class CmdWho(Command):
    """
    List who is online
    
    Usage:
        who
    """
    
    key = "who"
    locks = "cmd:all()"
    
    def func(self):
        from evennia import AccountDB
        
        online_accounts = AccountDB.objects.filter(is_online=True)
        
        if not online_accounts:
            self.caller.msg("No one is online.")
            return
            
        self.caller.msg("Players online:")
        for account in online_accounts:
            if account.character:
                char = account.character
                level = char.get_level()
                class_name = char.get_class_name()
                self.caller.msg(f"  {char.key} (Level {level} {class_name})")
            else:
                self.caller.msg(f"  {account.key} (No character)")


class CmdHelp(Command):
    """
    Get help on commands
    
    Usage:
        help
        help <command>
    """
    
    key = "help"
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("""
Available commands:
  Character: chooseclass, stats, remort, advancedclass, level, classes
  Combat: kill, flee, cast, skills, wield, unwield, wear, remove, equipment
  Movement: look, go, get, drop, inventory
  Social: say, shout, emote, who
  System: help, quit
  
Use 'help <command>' for more information on a specific command.
""")
        else:
            # Look up specific command help
            cmd_name = self.args.lower()
            cmd = self.caller.cmdset.get(cmd_name)
            if cmd:
                self.caller.msg(cmd.__doc__ or f"No help available for '{cmd_name}'.")
            else:
                self.caller.msg(f"No command found: '{cmd_name}'")


class CmdQuit(Command):
    """
    Quit the game
    
    Usage:
        quit
    """
    
    key = "quit"
    aliases = ["exit", "logout"]
    locks = "cmd:all()"
    
    def func(self):
        self.caller.msg("Goodbye!")
        self.caller.location.msg_contents(f"{self.caller.key} has left the game.", 
                                        exclude=self.caller)
        self.caller.account.disconnect()