# game_manager.py
import pygame
import sys
import random

from man_in_the_pit.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

from man_in_the_pit.states.menu_state import MenuState
#from man_in_the_pit.states.menu_state import PauseState
#from man_in_the_pit.states.menu_state import PlayState

#font = pygame.font.Font(None, 50)
#text_surface = font.render("Start Game", True, (255, 255, 255))
#screen.blit(text_surface, (100, 100))

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Man in the Pit")

        self.clock = pygame.time.Clock()
        self.running = True

        self.current_state = MenuState(self)

    def change_state(self, new_state):
        self.current_state = new_state

    def run(self):
        """Main game loop."""
        while self.running:

            dt_milis = self.clock.tick(FPS)

            # dt = delta_time: It represents the time (in seconds) from the previous frame to this frame.
            dt = dt_milis / 1000.0
            
            events = pygame.event.get()
            self.current_state.handle_events(events)
            self.current_state.update(dt)
            self.current_state.draw(self.screen)
            

            pygame.display.flip()
            

        pygame.quit()
        sys.exit()
