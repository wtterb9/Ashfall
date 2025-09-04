"""
Items and equipment for Ashfall MUD
"""

from evennia.objects.objects import DefaultObject
from .objects import ObjectParent


class Weapon(ObjectParent, DefaultObject):
    """
    Base weapon class
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("weapon")
        self.db.damage_dice = "1d6"
        self.db.damage_bonus = 0
        self.db.hit_bonus = 0
        self.db.weapon_type = "melee"
        self.db.durability = 100
        self.db.max_durability = 100


class Armor(ObjectParent, DefaultObject):
    """
    Base armor class
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("armor")
        self.db.armor_bonus = 0
        self.db.durability = 100
        self.db.max_durability = 100
        self.db.equipment_slot = "body"


class PostApocWeapon(Weapon):
    """
    Post-apocalyptic weapons
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.weapon_type = "post_apoc"


class PostApocArmor(Armor):
    """
    Post-apocalyptic armor
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.armor_type = "post_apoc"


# Specific weapon types
class RustyPipe(PostApocWeapon):
    """A rusty metal pipe"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.damage_dice = "1d8"
        self.db.damage_bonus = 1
        self.db.durability = 60
        self.db.max_durability = 60


class ScrapMetalClub(PostApocWeapon):
    """A club made from scrap metal"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.damage_dice = "1d10"
        self.db.damage_bonus = 2
        self.db.durability = 80
        self.db.max_durability = 80


class SalvagedRifle(PostApocWeapon):
    """A salvaged rifle"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.damage_dice = "2d8"
        self.db.damage_bonus = 3
        self.db.weapon_type = "ranged"
        self.db.durability = 70
        self.db.max_durability = 70


class LaserPistol(PostApocWeapon):
    """A pre-war laser pistol"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.damage_dice = "1d12"
        self.db.damage_bonus = 4
        self.db.weapon_type = "energy"
        self.db.durability = 90
        self.db.max_durability = 90


# Specific armor types
class LeatherDuster(PostApocArmor):
    """A worn leather duster"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.armor_bonus = 2
        self.db.equipment_slot = "body"
        self.db.durability = 50
        self.db.max_durability = 50


class ScrapMetalArmor(PostApocArmor):
    """Armor made from scrap metal"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.armor_bonus = 4
        self.db.equipment_slot = "body"
        self.db.durability = 80
        self.db.max_durability = 80


class RadiationSuit(PostApocArmor):
    """A pre-war radiation suit"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.armor_bonus = 3
        self.db.equipment_slot = "body"
        self.db.durability = 60
        self.db.max_durability = 60
        self.db.radiation_protection = 5


class CombatHelmet(PostApocArmor):
    """A military combat helmet"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.armor_bonus = 1
        self.db.equipment_slot = "head"
        self.db.durability = 70
        self.db.max_durability = 70


# Utility items
class WaterCanteen(DefaultObject):
    """A water canteen"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("consumable")
        self.db.uses = 10
        self.db.max_uses = 10
        self.db.healing = 20


class Medkit(DefaultObject):
    """A medical kit"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("consumable")
        self.db.uses = 5
        self.db.max_uses = 5
        self.db.healing = 50


class RadAway(DefaultObject):
    """Radiation treatment medicine"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("consumable")
        self.db.uses = 3
        self.db.max_uses = 3
        self.db.radiation_healing = 30


class Caps(DefaultObject):
    """Bottle caps - the currency of the wasteland"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("currency")
        self.db.value = 1


class Ammo(DefaultObject):
    """Ammunition for weapons"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("ammo")
        self.db.ammo_type = "standard"
        self.db.quantity = 10
        self.db.max_quantity = 10


class EnergyCell(Ammo):
    """Energy cells for energy weapons"""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.ammo_type = "energy"
        self.db.quantity = 5
        self.db.max_quantity = 5