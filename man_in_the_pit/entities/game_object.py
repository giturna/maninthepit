# entities/game_object.py
import pygame

class GameObject:
    def __init__(self, pos_x, pos_y, width, height, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color

    def draw_rect(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.pos_x, self.pos_y, self.width, self.height),
            2
        )
