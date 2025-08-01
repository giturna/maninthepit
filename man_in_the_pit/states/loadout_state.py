# loadout_state
import pygame
import sys
from man_in_the_pit.states.state import BaseState
from man_in_the_pit.states.play_state import PlayState
from man_in_the_pit.entities.player import Player
from man_in_the_pit.entities.weapon import Weapon, Pistol, Shotgun, SubmachineGun
from man_in_the_pit.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class LoadoutState(BaseState):
    def __init__(self, manager):
        super().__init__(manager)        
        # Main character
        self.hero = Player()

        self.image_pistol = pygame.image.load("man_in_the_pit/assets/loadout/pistol.png").convert_alpha()
        self.image_submachinegun = pygame.image.load("man_in_the_pit/assets/loadout/submachinegun.png").convert_alpha()
        self.image_shotgun = pygame.image.load("man_in_the_pit/assets/loadout/shotgun.png").convert_alpha()
        width = self.image_pistol.get_width()

        self.btn_opt_pistol = self.image_pistol.get_rect(center=(SCREEN_WIDTH//2 -(width+5), SCREEN_HEIGHT//3))
        self.btn_opt_shotgun = self.image_shotgun.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.btn_opt_submachinegun = self.image_submachinegun.get_rect(center=(SCREEN_WIDTH//2 +(width+5), SCREEN_HEIGHT//3))
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.btn_opt_pistol.collidepoint(event.pos):
                    self.weapon = Pistol(self.hero)
                elif self.btn_opt_shotgun.collidepoint(event.pos):
                    self.weapon = Shotgun(self.hero)
                else:
                    self.weapon = SubmachineGun(self.hero)
                
                self.hero.weapon = self.weapon
                self.hero._apply_weapon_skin()
                self.manager.change_state(PlayState(self.manager, self.hero))
            

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        s = pygame.Surface(screen.get_size(), pygame.SRCALPHA) 
        s.fill((0,0,0,100))
        screen.blit(s, (0,0))

        screen.blit(self.image_pistol, self.btn_opt_pistol)
        screen.blit(self.image_shotgun, self.btn_opt_shotgun)
        screen.blit(self.image_submachinegun, self.btn_opt_submachinegun)