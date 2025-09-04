"""
Combat commands for Ashfall MUD
"""

from evennia import Command
from evennia.utils import search
import random


class CmdKill(Command):
    """
    Attack another character or creature
    
    Usage:
        kill <target>
        kill <target> with <weapon>
    """
    
    key = "kill"
    aliases = ["attack", "hit", "fight"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Kill what?")
            return
            
        # Parse target and weapon
        args = self.args.split()
        target_name = args[0]
        weapon = None
        
        if "with" in args:
            with_index = args.index("with")
            target_name = " ".join(args[:with_index])
            weapon = " ".join(args[with_index + 1:])
        
        # Find target
        target = self.caller.search(target_name)
        if not target:
            return
            
        if target == self.caller:
            self.caller.msg("You can't attack yourself!")
            return
            
        if not target.has_account:
            self.caller.msg("You can only attack other players or creatures.")
            return
            
        # Check if already in combat
        if self.caller.db.is_combat:
            self.caller.msg("You are already in combat!")
            return
            
        # Start combat
        self.caller.start_combat(target, weapon)
        self.caller.msg(f"You attack {target.key}!")
        target.msg(f"{self.caller.key} attacks you!")
        self.caller.location.msg_contents(f"{self.caller.key} attacks {target.key}!", 
                                        exclude=[self.caller, target])


class CmdFlee(Command):
    """
    Flee from combat
    
    Usage:
        flee
    """
    
    key = "flee"
    aliases = ["run", "escape"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.caller.db.is_combat:
            self.caller.msg("You are not in combat!")
            return
            
        # 50% chance to flee successfully
        if random.random() < 0.5:
            self.caller.end_combat()
            self.caller.msg("You successfully flee from combat!")
            self.caller.location.msg_contents(f"{self.caller.key} flees from combat!", 
                                            exclude=self.caller)
        else:
            self.caller.msg("You fail to flee from combat!")


class CmdCast(Command):
    """
    Cast a spell
    
    Usage:
        cast <spell>
        cast <spell> at <target>
    """
    
    key = "cast"
    aliases = ["spell"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Cast what spell?")
            return
            
        # Parse spell and target
        args = self.args.split()
        spell_name = args[0]
        target = None
        
        if "at" in args:
            at_index = args.index("at")
            spell_name = " ".join(args[:at_index])
            target_name = " ".join(args[at_index + 1:])
            target = self.caller.search(target_name)
            if not target:
                return
        
        # Check if character knows the spell
        if spell_name not in self.caller.db.known_spells:
            self.caller.msg(f"You don't know the spell '{spell_name}'.")
            return
            
        # Check mana
        spell_cost = self.caller.db.spells.get(spell_name, {}).get('cost', 10)
        if self.caller.db.mana < spell_cost:
            self.caller.msg("You don't have enough mana to cast that spell.")
            return
            
        # Cast spell
        self.caller.cast_spell(spell_name, target)


class CmdSkills(Command):
    """
    Display your skills and spells
    
    Usage:
        skills
    """
    
    key = "skills"
    aliases = ["spells", "abilities"]
    locks = "cmd:all()"
    
    def func(self):
        skills = self.caller.db.skills or {}
        spells = self.caller.db.known_spells or []
        
        if skills:
            self.caller.msg("Skills:")
            for skill, level in skills.items():
                self.caller.msg(f"  {skill}: {level}")
        else:
            self.caller.msg("You have no skills.")
            
        if spells:
            self.caller.msg("\nKnown Spells:")
            for spell in spells:
                cost = self.caller.db.spells.get(spell, {}).get('cost', 10)
                self.caller.msg(f"  {spell} (cost: {cost} mana)")
        else:
            self.caller.msg("\nYou know no spells.")


class CmdWield(Command):
    """
    Wield a weapon
    
    Usage:
        wield <weapon>
    """
    
    key = "wield"
    aliases = ["hold"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Wield what?")
            return
            
        weapon = self.caller.search(self.args)
        if not weapon:
            return
            
        if not weapon.has_tag("weapon"):
            self.caller.msg("That's not a weapon!")
            return
            
        # Unequip current weapon
        if self.caller.db.equipment['wield']:
            self.caller.db.equipment['wield'].move_to(self.caller.location)
            self.caller.msg(f"You stop wielding {self.caller.db.equipment['wield'].key}.")
            
        # Equip new weapon
        self.caller.db.equipment['wield'] = weapon
        weapon.move_to(self.caller, quiet=True)
        self.caller.msg(f"You wield {weapon.key}.")
        self.caller.location.msg_contents(f"{self.caller.key} wields {weapon.key}.", 
                                        exclude=self.caller)


class CmdUnwield(Command):
    """
    Stop wielding your weapon
    
    Usage:
        unwield
    """
    
    key = "unwield"
    locks = "cmd:all()"
    
    def func(self):
        if not self.caller.db.equipment['wield']:
            self.caller.msg("You are not wielding anything.")
            return
            
        weapon = self.caller.db.equipment['wield']
        self.caller.db.equipment['wield'] = None
        weapon.move_to(self.caller.location)
        self.caller.msg(f"You stop wielding {weapon.key}.")
        self.caller.location.msg_contents(f"{self.caller.key} stops wielding {weapon.key}.", 
                                        exclude=self.caller)


class CmdWear(Command):
    """
    Wear armor or clothing
    
    Usage:
        wear <item>
    """
    
    key = "wear"
    aliases = ["put"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Wear what?")
            return
            
        item = self.caller.search(self.args)
        if not item:
            return
            
        if not item.has_tag("armor"):
            self.caller.msg("That's not armor!")
            return
            
        # Determine equipment slot
        slot = item.db.equipment_slot or "body"
        
        # Unequip current item in slot
        if self.caller.db.equipment[slot]:
            self.caller.db.equipment[slot].move_to(self.caller.location)
            self.caller.msg(f"You remove {self.caller.db.equipment[slot].key}.")
            
        # Equip new item
        self.caller.db.equipment[slot] = item
        item.move_to(self.caller, quiet=True)
        self.caller.msg(f"You wear {item.key}.")
        self.caller.location.msg_contents(f"{self.caller.key} wears {item.key}.", 
                                        exclude=self.caller)


class CmdRemove(Command):
    """
    Remove armor or clothing
    
    Usage:
        remove <item>
    """
    
    key = "remove"
    aliases = ["take"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Remove what?")
            return
            
        item_name = self.args.lower()
        
        # Find item in equipment
        for slot, item in self.caller.db.equipment.items():
            if item and item.key.lower() == item_name:
                self.caller.db.equipment[slot] = None
                item.move_to(self.caller.location)
                self.caller.msg(f"You remove {item.key}.")
                self.caller.location.msg_contents(f"{self.caller.key} removes {item.key}.", 
                                                exclude=self.caller)
                return
                
        self.caller.msg("You are not wearing that.")


class CmdEquipment(Command):
    """
    Display your equipment
    
    Usage:
        equipment
    """
    
    key = "equipment"
    aliases = ["eq", "worn"]
    locks = "cmd:all()"
    
    def func(self):
        self.caller.msg("Equipment:")
        for slot, item in self.caller.db.equipment.items():
            if item:
                self.caller.msg(f"  {slot}: {item.key}")
            else:
                self.caller.msg(f"  {slot}: <empty>")