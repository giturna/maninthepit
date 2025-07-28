# entities/bullet.py
import math
import pygame
from man_in_the_pit.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from man_in_the_pit.entities.game_object import GameObject

class Bullet(GameObject):
    def __init__(self, pos_x, pos_y, width, height, color, velocity, dmg):
        super().__init__(pos_x, pos_y, width, height, color)
        self.velocity = velocity
        self.dmg = dmg
        self.direction_x = 0
        self.direction_y = 0

    def set_direction(self, mouse_x, mouse_y):
        dx = mouse_x - self.pos_x
        dy = mouse_y - self.pos_y
        distance = math.hypot(dx, dy)  # (dx**2 + dy**2)**0.5

        if distance > 0:
            self.direction_x = dx / distance
            self.direction_y = dy / distance

    def move(self, dt):
        self.pos_x += self.velocity * self.direction_x * dt
        self.pos_y += self.velocity * self.direction_y * dt

    def is_out_of_window(self):
        return (
            self.pos_x < 0 or
            self.pos_x > SCREEN_WIDTH or
            self.pos_y < 0 or
            self.pos_y > SCREEN_HEIGHT
        )

    def is_hit_the_enemy(self, enemy):
        bullet_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        enemy_rect = pygame.Rect(enemy.pos_x, enemy.pos_y, enemy.width, enemy.height)
        return bullet_rect.colliderect(enemy_rect)
