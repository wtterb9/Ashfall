"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter
from evennia.utils import logger
from django.conf import settings

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """

    def at_object_creation(self):
        """Called when character is first created"""
        super().at_object_creation()
        
        # Initialize character stats
        self.db.level = 1
        self.db.experience = 0
        self.db.remorts = 0
        self.db.class_name = None
        self.db.advanced_class = None
        
        # Base stats (similar to tbaMUD)
        self.db.strength = 10
        self.db.intelligence = 10
        self.db.wisdom = 10
        self.db.dexterity = 10
        self.db.constitution = 10
        self.db.charisma = 10
        
        # Combat stats
        self.db.hit_points = 100
        self.db.max_hit_points = 100
        self.db.mana = 0
        self.db.max_mana = 0
        self.db.move = 100
        self.db.max_move = 100
        
        # Combat modifiers
        self.db.armor_class = 0
        self.db.damage_bonus = 0
        self.db.hit_bonus = 0
        
        # Status flags
        self.db.is_combat = False
        self.db.is_resting = False
        self.db.is_sitting = False
        self.db.is_sleeping = False
        
        # Equipment slots
        self.db.equipment = {
            'head': None,
            'neck': None,
            'body': None,
            'about': None,
            'arms': None,
            'hands': None,
            'finger_l': None,
            'finger_r': None,
            'wield': None,
            'shield': None,
            'legs': None,
            'feet': None,
        }
        
        # Skills and spells
        self.db.skills = {}
        self.db.spells = {}
        self.db.known_spells = []
        
        # Remort tracking
        self.db.remort_history = []
        
        logger.log_info(f"Character {self.key} created with default stats")

    def get_level(self):
        """Get current level"""
        return self.db.level or 1

    def get_experience(self):
        """Get current experience"""
        return self.db.experience or 0

    def get_remorts(self):
        """Get number of remorts"""
        return self.db.remorts or 0

    def get_class_name(self):
        """Get current class name"""
        return self.db.class_name or "None"

    def get_advanced_class(self):
        """Get advanced class name"""
        return self.db.advanced_class or "None"

    def set_class(self, class_name):
        """Set character class"""
        if class_name in ['warrior', 'mage', 'cleric', 'thief', 'psionicist']:
            self.db.class_name = class_name
            self.apply_class_bonuses()
            return True
        return False

    def apply_class_bonuses(self):
        """Apply class-specific stat bonuses"""
        class_name = self.get_class_name()
        
        if class_name == 'warrior':
            self.db.strength += 2
            self.db.constitution += 1
            self.db.hit_points += 20
            self.db.max_hit_points += 20
            # Warriors get combat skills
            self.db.skills = {'sword': 10, 'shield': 10, 'armor': 10}
        elif class_name == 'mage':
            self.db.intelligence += 3
            self.db.mana += 50
            self.db.max_mana += 50
            # Mages get spells
            self.db.known_spells = ['fireball', 'magic_missile', 'light']
            self.db.spells = {
                'fireball': {'cost': 15, 'level': 1},
                'magic_missile': {'cost': 10, 'level': 1},
                'light': {'cost': 5, 'level': 1}
            }
        elif class_name == 'cleric':
            self.db.wisdom += 3
            self.db.mana += 30
            self.db.max_mana += 30
            self.db.hit_points += 10
            self.db.max_hit_points += 10
            # Clerics get healing spells
            self.db.known_spells = ['heal', 'cure_light', 'bless']
            self.db.spells = {
                'heal': {'cost': 20, 'level': 1},
                'cure_light': {'cost': 10, 'level': 1},
                'bless': {'cost': 15, 'level': 1}
            }
        elif class_name == 'thief':
            self.db.dexterity += 3
            self.db.hit_points += 10
            self.db.max_hit_points += 10
            # Thieves get stealth skills
            self.db.skills = {'stealth': 15, 'lockpick': 10, 'sneak': 15}
        elif class_name == 'psionicist':
            self.db.intelligence += 2
            self.db.wisdom += 2
            self.db.mana += 40
            self.db.max_mana += 40
            self.db.hit_points += 10
            self.db.max_hit_points += 10
            # Psionicists get mental powers
            self.db.known_spells = ['mind_blast', 'telekinesis', 'mind_scan']
            self.db.spells = {
                'mind_blast': {'cost': 12, 'level': 1},
                'telekinesis': {'cost': 8, 'level': 1},
                'mind_scan': {'cost': 5, 'level': 1}
            }

    def gain_experience(self, amount):
        """Gain experience and check for level up"""
        if not amount:
            return
            
        self.db.experience += amount
        self.msg(f"You gain {amount} experience points.")
        
        # Check for level up
        required_exp = self.get_exp_for_level(self.get_level() + 1)
        if self.db.experience >= required_exp and self.get_level() < getattr(settings, 'MAX_PLAYER_LEVEL', 50):
            self.level_up()

    def get_exp_for_level(self, level):
        """Calculate experience required for a given level"""
        if level <= 1:
            return 0
        return int(1000 * (level - 1) * (level - 1) * 1.2)

    def level_up(self):
        """Handle level up"""
        old_level = self.get_level()
        self.db.level += 1
        new_level = self.get_level()
        
        # Increase stats based on class
        self.increase_stats_on_level()
        
        # Increase hit points
        hp_gain = self.get_hp_gain()
        self.db.hit_points += hp_gain
        self.db.max_hit_points += hp_gain
        
        # Increase mana
        mana_gain = self.get_mana_gain()
        if mana_gain > 0:
            self.db.mana += mana_gain
            self.db.max_mana += mana_gain
        
        self.msg(f"You have gained a level! You are now level {new_level}!")
        self.msg(f"You gain {hp_gain} hit points and {mana_gain} mana.")
        
        # Check if we can advance to advanced class
        if self.get_remorts() >= getattr(settings, 'REQUIRED_REMORTS_FOR_ADVANCED_CLASS', 50):
            self.msg("You are now eligible for advanced class selection!")

    def increase_stats_on_level(self):
        """Increase stats on level up based on class"""
        class_name = self.get_class_name()
        
        if class_name == 'warrior':
            self.db.strength += 1
            self.db.constitution += 1
        elif class_name == 'mage':
            self.db.intelligence += 2
        elif class_name == 'cleric':
            self.db.wisdom += 2
        elif class_name == 'thief':
            self.db.dexterity += 2
        elif class_name == 'psionicist':
            self.db.intelligence += 1
            self.db.wisdom += 1

    def get_hp_gain(self):
        """Calculate hit point gain on level up"""
        class_name = self.get_class_name()
        base_con = self.db.constitution or 10
        
        if class_name == 'warrior':
            return max(1, (base_con - 10) // 2 + 10)
        elif class_name in ['cleric', 'thief', 'psionicist']:
            return max(1, (base_con - 10) // 2 + 6)
        elif class_name == 'mage':
            return max(1, (base_con - 10) // 2 + 4)
        return 1

    def get_mana_gain(self):
        """Calculate mana gain on level up"""
        class_name = self.get_class_name()
        
        if class_name == 'mage':
            return (self.db.intelligence or 10) // 2 + 10
        elif class_name == 'cleric':
            return (self.db.wisdom or 10) // 2 + 8
        elif class_name == 'psionicist':
            return (self.db.intelligence or 10) // 2 + (self.db.wisdom or 10) // 2 + 6
        return 0

    def remort(self):
        """Handle character remort"""
        if self.get_level() < getattr(settings, 'MAX_PLAYER_LEVEL', 50):
            self.msg("You must reach maximum level before you can remort!")
            return False
            
        self.db.remorts += 1
        self.db.level = 1
        self.db.experience = 0
        
        # Reset stats but keep some bonuses
        self.db.strength = 10
        self.db.intelligence = 10
        self.db.wisdom = 10
        self.db.dexterity = 10
        self.db.constitution = 10
        self.db.charisma = 10
        
        # Apply class bonuses again
        self.apply_class_bonuses()
        
        # Reset hit points and mana
        self.db.hit_points = self.db.max_hit_points
        self.db.mana = self.db.max_mana
        
        self.msg(f"You have remorted! This is your {self.get_remorts()} remort.")
        
        # Check if eligible for advanced class
        if self.get_remorts() >= getattr(settings, 'REQUIRED_REMORTS_FOR_ADVANCED_CLASS', 50):
            self.msg("You are now eligible for advanced class selection!")
            
        return True

    def set_advanced_class(self, advanced_class):
        """Set advanced class"""
        if not self.can_choose_advanced_class():
            self.msg("You need 50 remorts to choose an advanced class!")
            return False
            
        class_name = self.get_class_name()
        valid_advanced = self.get_valid_advanced_classes(class_name)
        
        if advanced_class in valid_advanced:
            self.db.advanced_class = advanced_class
            self.apply_advanced_class_bonuses()
            self.msg(f"You have chosen the {advanced_class} advanced class!")
            return True
        else:
            self.msg(f"Invalid advanced class for {class_name}. Valid options: {', '.join(valid_advanced)}")
            return False

    def can_choose_advanced_class(self):
        """Check if character can choose advanced class"""
        return self.get_remorts() >= getattr(settings, 'REQUIRED_REMORTS_FOR_ADVANCED_CLASS', 50)

    def get_valid_advanced_classes(self, class_name):
        """Get valid advanced classes for a given class"""
        advanced_classes = {
            'warrior': ['warlord', 'juggernaut'],
            'mage': ['warlock', 'arcanist'],
            'cleric': ['inquisitor', 'hierophant'],
            'thief': ['assassin', 'ashstalker'],
            'psionicist': ['mindreaver', 'seer']
        }
        return advanced_classes.get(class_name, [])

    def apply_advanced_class_bonuses(self):
        """Apply advanced class bonuses"""
        advanced_class = self.get_advanced_class()
        
        if advanced_class == 'warlord':
            self.db.strength += 3
            self.db.charisma += 2
            self.db.hit_points += 50
            self.db.max_hit_points += 50
        elif advanced_class == 'juggernaut':
            self.db.strength += 2
            self.db.constitution += 3
            self.db.hit_points += 100
            self.db.max_hit_points += 100
        elif advanced_class == 'warlock':
            self.db.intelligence += 3
            self.db.charisma += 2
            self.db.mana += 100
            self.db.max_mana += 100
        elif advanced_class == 'arcanist':
            self.db.intelligence += 4
            self.db.mana += 150
            self.db.max_mana += 150
        elif advanced_class == 'inquisitor':
            self.db.wisdom += 3
            self.db.strength += 2
            self.db.hit_points += 30
            self.db.max_hit_points += 30
            self.db.mana += 50
            self.db.max_mana += 50
        elif advanced_class == 'hierophant':
            self.db.wisdom += 4
            self.db.mana += 100
            self.db.max_mana += 100
        elif advanced_class == 'assassin':
            self.db.dexterity += 3
            self.db.strength += 2
            self.db.hit_points += 20
            self.db.max_hit_points += 20
        elif advanced_class == 'ashstalker':
            self.db.dexterity += 4
            self.db.wisdom += 2
            self.db.hit_points += 30
            self.db.max_hit_points += 30
        elif advanced_class == 'mindreaver':
            self.db.intelligence += 3
            self.db.wisdom += 3
            self.db.mana += 80
            self.db.max_mana += 80
        elif advanced_class == 'seer':
            self.db.wisdom += 4
            self.db.intelligence += 2
            self.db.mana += 120
            self.db.max_mana += 120

    def get_stat_display(self):
        """Get formatted stat display"""
        return f"""
Level: {self.get_level()} | Class: {self.get_class_name()} | Remorts: {self.get_remorts()}
Advanced Class: {self.get_advanced_class()}

Strength: {self.db.strength}     Intelligence: {self.db.intelligence}
Wisdom: {self.db.wisdom}         Dexterity: {self.db.dexterity}
Constitution: {self.db.constitution}  Charisma: {self.db.charisma}

Hit Points: {self.db.hit_points}/{self.db.max_hit_points}
Mana: {self.db.mana}/{self.db.max_mana}
Move: {self.db.move}/{self.db.max_move}

Armor Class: {self.db.armor_class}
Hit Bonus: {self.db.hit_bonus}
Damage Bonus: {self.db.damage_bonus}
"""

    def at_look(self, target, **kwargs):
        """Custom look method"""
        if target == self:
            return self.get_stat_display()
        return super().at_look(target, **kwargs)

    def start_combat(self, target, weapon=None):
        """Start combat with target"""
        self.db.is_combat = True
        self.db.combat_target = target
        self.db.combat_weapon = weapon
        target.db.is_combat = True
        target.db.combat_target = self
        
        # Start combat timer
        self.start_combat_timer()

    def end_combat(self):
        """End combat"""
        self.db.is_combat = False
        if self.db.combat_target:
            self.db.combat_target.db.is_combat = False
            self.db.combat_target.db.combat_target = None
        self.db.combat_target = None
        self.db.combat_weapon = None

    def start_combat_timer(self):
        """Start combat timer for automatic combat"""
        from evennia import TICKER_HANDLER
        TICKER_HANDLER.add(30, self.combat_tick, persistent=False)

    def combat_tick(self):
        """Handle combat tick"""
        if not self.db.is_combat or not self.db.combat_target:
            return
            
        target = self.db.combat_target
        if not target.db.is_combat:
            self.end_combat()
            return
            
        # Perform combat action
        self.perform_combat_action(target)

    def perform_combat_action(self, target):
        """Perform a combat action"""
        import random
        
        # Calculate hit chance
        hit_chice = 50 + (self.db.hit_bonus or 0) - (target.db.armor_class or 0)
        if random.randint(1, 100) <= hit_chice:
            # Hit!
            damage = self.calculate_damage()
            target.take_damage(damage)
            self.msg(f"You hit {target.key} for {damage} damage!")
            target.msg(f"{self.key} hits you for {damage} damage!")
            self.location.msg_contents(f"{self.key} hits {target.key} for {damage} damage!", 
                                    exclude=[self, target])
        else:
            # Miss!
            self.msg(f"You miss {target.key}!")
            target.msg(f"{self.key} misses you!")
            self.location.msg_contents(f"{self.key} misses {target.key}!", 
                                    exclude=[self, target])

    def calculate_damage(self):
        """Calculate damage dealt"""
        import random
        
        # Base damage from weapon
        weapon = self.db.equipment.get('wield')
        if weapon:
            damage_dice = weapon.db.damage_dice or "1d6"
            dice, sides = damage_dice.split('d')
            dice = int(dice)
            sides = int(sides)
            damage = sum(random.randint(1, sides) for _ in range(dice))
        else:
            damage = random.randint(1, 4)  # Unarmed damage
            
        # Add damage bonus
        damage += (self.db.damage_bonus or 0)
        
        # Add strength bonus
        strength = self.db.strength or 10
        if strength > 10:
            damage += (strength - 10) // 2
            
        return max(1, damage)

    def take_damage(self, amount):
        """Take damage"""
        self.db.hit_points = max(0, (self.db.hit_points or 0) - amount)
        
        if self.db.hit_points <= 0:
            self.die()

    def die(self):
        """Handle character death"""
        self.msg("You have died!")
        self.location.msg_contents(f"{self.key} has died!", exclude=self)
        
        # End combat
        self.end_combat()
        
        # Reset hit points
        self.db.hit_points = self.db.max_hit_points
        
        # Move to starting location
        from evennia import search_object
        neighborhood = search_object("Ruined Neighborhood")[0]
        self.move_to(neighborhood)
        self.msg("You wake up in the neighborhood, having been revived.")

    def cast_spell(self, spell_name, target=None):
        """Cast a spell"""
        if spell_name not in self.db.known_spells:
            self.msg(f"You don't know the spell '{spell_name}'.")
            return
            
        spell_info = self.db.spells.get(spell_name, {})
        cost = spell_info.get('cost', 10)
        
        if self.db.mana < cost:
            self.msg("You don't have enough mana to cast that spell.")
            return
            
        self.db.mana -= cost
        
        # Basic spell effects
        if spell_name == "heal":
            if target:
                target.db.hit_points = min(target.db.max_hit_points, 
                                         (target.db.hit_points or 0) + 20)
                self.msg(f"You heal {target.key} for 20 hit points.")
                target.msg(f"{self.key} heals you for 20 hit points.")
            else:
                self.db.hit_points = min(self.db.max_hit_points, 
                                       (self.db.hit_points or 0) + 20)
                self.msg("You heal yourself for 20 hit points.")
        elif spell_name == "cure_light":
            if target:
                target.db.hit_points = min(target.db.max_hit_points, 
                                         (target.db.hit_points or 0) + 10)
                self.msg(f"You cure {target.key} for 10 hit points.")
                target.msg(f"{self.key} cures you for 10 hit points.")
            else:
                self.db.hit_points = min(self.db.max_hit_points, 
                                       (self.db.hit_points or 0) + 10)
                self.msg("You cure yourself for 10 hit points.")
        elif spell_name == "bless":
            if target:
                target.db.hit_bonus = (target.db.hit_bonus or 0) + 2
                self.msg(f"You bless {target.key}.")
                target.msg(f"{self.key} blesses you.")
            else:
                self.db.hit_bonus = (self.db.hit_bonus or 0) + 2
                self.msg("You bless yourself.")
        elif spell_name == "fireball":
            if target:
                damage = 15
                target.take_damage(damage)
                self.msg(f"You cast fireball at {target.key} for {damage} damage!")
                target.msg(f"{self.key} casts fireball at you for {damage} damage!")
                self.location.msg_contents(f"{self.key} casts fireball at {target.key}!", 
                                        exclude=[self, target])
            else:
                self.msg("You need a target for fireball.")
        elif spell_name == "magic_missile":
            if target:
                damage = 8
                target.take_damage(damage)
                self.msg(f"You cast magic missile at {target.key} for {damage} damage!")
                target.msg(f"{self.key} casts magic missile at you for {damage} damage!")
                self.location.msg_contents(f"{self.key} casts magic missile at {target.key}!", 
                                        exclude=[self, target])
            else:
                self.msg("You need a target for magic missile.")
        elif spell_name == "light":
            self.msg("You cast light, illuminating the area.")
            self.location.msg_contents(f"{self.key} casts light, illuminating the area.", 
                                    exclude=self)
        elif spell_name == "mind_blast":
            if target:
                damage = 12
                target.take_damage(damage)
                self.msg(f"You blast {target.key}'s mind for {damage} damage!")
                target.msg(f"{self.key} blasts your mind for {damage} damage!")
                self.location.msg_contents(f"{self.key} blasts {target.key}'s mind!", 
                                        exclude=[self, target])
            else:
                self.msg("You need a target for mind blast.")
        elif spell_name == "telekinesis":
            if target:
                self.msg(f"You use telekinesis on {target.key}.")
                target.msg(f"{self.key} uses telekinesis on you.")
                self.location.msg_contents(f"{self.key} uses telekinesis on {target.key}!", 
                                        exclude=[self, target])
            else:
                self.msg("You need a target for telekinesis.")
        elif spell_name == "mind_scan":
            if target:
                self.msg(f"You scan {target.key}'s mind.")
                target.msg(f"{self.key} scans your mind.")
                self.location.msg_contents(f"{self.key} scans {target.key}'s mind!", 
                                        exclude=[self, target])
            else:
                self.msg("You need a target for mind scan.")
        else:
            self.msg(f"You cast {spell_name}.")

    def start_recovery(self):
        """Start recovery process while resting"""
        from evennia import TICKER_HANDLER
        TICKER_HANDLER.add(10, self.recovery_tick, persistent=False)

    def recovery_tick(self):
        """Handle recovery tick"""
        if not self.db.is_resting:
            return
            
        # Recover hit points
        if self.db.hit_points < self.db.max_hit_points:
            recovery = min(5, self.db.max_hit_points - self.db.hit_points)
            self.db.hit_points += recovery
            self.msg(f"You recover {recovery} hit points while resting.")
            
        # Recover mana
        if self.db.mana < self.db.max_mana:
            recovery = min(3, self.db.max_mana - self.db.mana)
            self.db.mana += recovery
            self.msg(f"You recover {recovery} mana while resting.")
            
        # Continue recovery if still resting
        if self.db.is_resting and (self.db.hit_points < self.db.max_hit_points or 
                                  self.db.mana < self.db.max_mana):
            self.start_recovery()
