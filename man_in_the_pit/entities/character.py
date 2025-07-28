# entities/character.py
from man_in_the_pit.entities.game_object import GameObject

class Character(GameObject):
    def __init__(self, pos_x, pos_y, width, height, color, hp, velocity, exp):
        super().__init__(pos_x, pos_y, width, height, color)
        self.hp = hp
        self.velocity = velocity
        self.exp = exp

    def get_hit(self, damager):
        self.hp -= damager.dmg

    def is_dead(self):
        return self.hp <= 0
