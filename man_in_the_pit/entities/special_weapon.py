# man_in_the_pit/entities/special_weapon.py
import pygame
from man_in_the_pit.entities.bullet import Bullet
from man_in_the_pit.entities.weapon import Weapon

class SpecialWeapon(Weapon):
    def __init__(self, owner, cooldown_time):
        super().__init__(owner,
                         fire_rate      = 1.0,
                         magazine_size  = 1,
                         reload_time    = cooldown_time)
        self.ammo = 1                     # is always one

    # No ammo, no reload. Just Cooldown after firing the projectile
    def fire(self, target_pos, obj_list, aux_list=None):
        if not self.can_fire():
            return
        self.perform_attack(target_pos, obj_list, aux_list)
        self.cooldown = self.fire_delay   # fire_delay = 1s (doesn't matter)
        self.is_reloading = True          # for cooldown tracking
        self.reload_timer = self.reload_time

    def perform_attack(self, target_pos, obj_list, aux_list):
        raise NotImplementedError("The actual attack should be written in the subclass")
