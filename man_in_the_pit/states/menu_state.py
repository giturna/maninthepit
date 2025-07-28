# menu_state

import pygame
import sys
from man_in_the_pit.states.state import BaseState
from man_in_the_pit.states.play_state import PlayState
from man_in_the_pit.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class MenuState(BaseState):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont("Arial", 32)
        self.text_play = self.font.render("Play", True, (255,255,255))
        self.text_play_rect = self.text_play.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.text_quit = self.font.render("Quit", True, (255,255,255))
        self.text_quit_rect = self.text_play.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.text_play_rect.collidepoint(event.pos):
                    self.manager.change_state(PlayState(self.manager))
                if self.text_quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.text_play, self.text_play_rect)
        screen.blit(self.text_quit, self.text_quit_rect)