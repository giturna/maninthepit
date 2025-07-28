# play_state

import pygame
import sys
import random

from man_in_the_pit.states.state import BaseState
from man_in_the_pit.states.pause_state import PauseState

from man_in_the_pit.states.wave_manager import WaveManager

from man_in_the_pit.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from man_in_the_pit.entities.player import Player
from man_in_the_pit.entities.enemy import Enemy
from man_in_the_pit.entities.enemy import Slime
from man_in_the_pit.entities.enemy import Slime_Boss
from man_in_the_pit.entities.bullet import Bullet
from man_in_the_pit.entities.weapon import Shotgun, Pistol, SubmachineGun

class PlayState(BaseState):
    def __init__(self, manager):
        super().__init__(manager)

        self.elapsed_time = 0.0
        self.running = True

        # Background
        self.bg_img = pygame.image.load("man_in_the_pit/assets/background2.png").convert()

        # Main character
        self.hero = Player()
        self.hero.stamina = self.hero.max_stamina

        # Ammo icons
        self.icon_pistol  = pygame.image.load(
            "man_in_the_pit/assets/bullets/pistol_bullet.png"
        ).convert_alpha()
        self.icon_shotgun = pygame.image.load(
            "man_in_the_pit/assets/bullets/shotgun_bullet.png"
        ).convert_alpha()
            # Makes ammo icons same size
        ICON_H = 24
        scale = ICON_H / self.icon_pistol.get_height()
        self.icon_pistol  = pygame.transform.scale(
            self.icon_pistol,
            (int(self.icon_pistol.get_width()*scale), ICON_H)
        )
        self.icon_shotgun = pygame.transform.scale(
            self.icon_shotgun,
            (int(self.icon_shotgun.get_width()*scale), ICON_H)
        )

        # Stat bar position/size
        self.hp_bar_bg      = pygame.Rect(50, 50, 300, 24)   # red
        self.stamina_bar_bg = pygame.Rect(50, self.hp_bar_bg.bottom + 6, 250, 12)  # blue
        self.exp_bar_bg     = pygame.Rect(50, self.stamina_bar_bg.bottom + 4, 250, 12)  # yellow

        # Wave counter
        self.wave_manager = WaveManager()
        self.enemies_killed = 0

        # Lists
        self.bullets = []
        self.enemies = []

        # Enemy spawn controll
        self.last_spawn_time = pygame.time.get_ticks()
        # self.spawn_interval = 1000  # milisecond


    # -----------------------------------------------------------------------------
    # 1) glass effect for status bars
    def _render_bar(self, surface, bg_rect, ratio, color,
                    radius=8, shadow_alpha=60, gloss_alpha=70):
        pygame.draw.rect(surface, (40, 40, 40), bg_rect, border_radius=radius)

        fill_rect        = bg_rect.copy()
        fill_rect.width  = int(bg_rect.width * ratio)
        if fill_rect.width == 0:
            pygame.draw.rect(surface, (0, 0, 0), bg_rect, 2, border_radius=radius)
            return

        pygame.draw.rect(surface, color, fill_rect, border_radius=radius)

        # --- shadow ---
        sh_h = int(fill_rect.height * 0.4)
        shadow = pygame.Surface((fill_rect.width, sh_h), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, shadow_alpha),
                        shadow.get_rect(), border_radius=radius)
        surface.blit(shadow, (fill_rect.x, fill_rect.bottom - sh_h))

        # --- brightness ---
        gl_h = int(fill_rect.height * 0.5)
        gloss = pygame.Surface((fill_rect.width, gl_h), pygame.SRCALPHA)
        pygame.draw.rect(gloss, (255, 255, 255, gloss_alpha),
                        gloss.get_rect(), border_radius=radius)
        surface.blit(gloss, (fill_rect.x, fill_rect.y))

        pygame.draw.rect(surface, (0, 0, 0), bg_rect, 2, border_radius=radius)



    # -----------------------------------------------------------------------------
    # 2) Draws all bars at once
    def draw_stat_bars(self, surface):
        hp_ratio   = max(self.hero.hp, 0) / self.hero.max_hp
        stam_ratio = self.hero.stamina / self.hero.max_stamina
        xp_ratio   = (self.hero.exp % self.hero.exp_to_level) / self.hero.exp_to_level

        self._render_bar(surface, self.hp_bar_bg,      hp_ratio, (220, 20, 20),  radius=10)
        self._render_bar(surface, self.stamina_bar_bg, stam_ratio, (30, 80, 250))
        self._render_bar(surface, self.exp_bar_bg,     xp_ratio, (230, 230, 40))





    def show_stats(self):
        self.font = pygame.font.SysFont("Arial", 28)
        
        # Health
        self.text_hp = self.font.render("HP: "+f"{self.hero.hp:.0f}", True, (255,255,255))
        self.text_hp_rect = self.text_hp.get_rect(topleft=(50, 50))
        
        # Stamina
        self.text_stamina = self.font.render("Stamina: "+f"{self.hero.stamina:.0f}", True, (255,255,255))
        self.text_stamina_rect = self.text_stamina.get_rect(topleft=(50, 100))
        
        # XP
        self.text_exp = self.font.render("XP: "+f"{self.hero.exp:.0f}", True, (255,255,255))
        self.text_exp_rect = self.text_exp.get_rect(topleft=(50, 150))

    
    def draw_ammo(self, surface):
        # Which type of ammo?
        if isinstance(self.hero.weapon, Shotgun):
            icon = self.icon_shotgun
        else:
            icon = self.icon_pistol

        # Position
        start_x = self.exp_bar_bg.x
        start_y = self.exp_bar_bg.bottom + 10

        for i in range(self.hero.weapon.ammo):
            x = start_x + i * (icon.get_width() + 2)   # 2 px space
            surface.blit(icon, (x, start_y))

    
    def spawn_enemy(self):
        """Creates new enemy and adds it to the list."""
        slime = Slime()
        self.enemies.append(slime)


    def resolve_enemy_collisions(self):
        for i, e1 in enumerate(self.enemies):
            rect1 = e1.get_rect()
            for j, e2 in enumerate(self.enemies):
                if i >= j:
                    continue
                rect2 = e2.get_rect()
                if rect1.colliderect(rect2):
                    dx = e1.pos_x - e2.pos_x
                    dy = e1.pos_y - e2.pos_y
                    distance = (dx**2 + dy**2)**0.5 or 1  # prevent to divide zero

                    move_amount = 2
                    move_x = (dx / distance) * move_amount
                    move_y = (dy / distance) * move_amount

                    e1.pos_x += move_x
                    e1.pos_y += move_y
                    e2.pos_x -= move_x
                    e2.pos_y -= move_y



    def create_action(self, action_name):
        if action_name == "spawn_boss_Slime":
            slimeBoss = Slime_Boss()
            self.enemies.append(slimeBoss)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not getattr(self.hero.weapon, "automatic", False):
                    self.hero.weapon.fire(event.pos, self.bullets)


    def update(self, dt):
        current_time = pygame.time.get_ticks()
        self.elapsed_time += dt # time passed during play state in seconds

        # 1) Wave Manager
        self.wave_manager.update(dt)
        self.wave_manager.spawn_controll()

        for action_info in self.wave_manager.once_actions:
            if not action_info["done"]:
                if action_info["wave"] == self.wave_manager.wave_number and self.wave_manager.wave_timer >= action_info["time"]:
                    self.create_action(action_info["event"])
                    action_info["done"] = True

        # 2) Enemy spawn
        if current_time - self.last_spawn_time > self.wave_manager.spawn_interval:
            self.spawn_enemy()
            self.last_spawn_time = current_time

        # 3) Player movement and Pause
        self.hero.update(dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.manager.change_state(PauseState(self.manager, self))

        # 4) Bullet movement
        for bullet in self.bullets[:]:
            bullet.move(dt)
            # Enemy collide controll
            for enemy in self.enemies[:]:
                if bullet.is_hit_the_enemy(enemy):
                    enemy.get_hit(bullet)
                    if enemy.is_dead():
                        self.enemies.remove(enemy)
                        self.hero.get_exp(enemy)
                        self.enemies_killed += 1
                    self.bullets.remove(bullet)
                    break

            # Window collide controll
            if bullet in self.bullets and bullet.is_out_of_window():
                self.bullets.remove(bullet)

        # 5) Enemy movement
        for enemy in self.enemies:
            enemy.update(dt)
            enemy.set_target(self.hero.pos_x, self.hero.pos_y)
            enemy.move_pattern(dt)
        self.resolve_enemy_collisions()

        #self.show_stats()

        # 6) Automatic weapon fire
        if pygame.mouse.get_pressed()[0]:
            if getattr(self.hero.weapon, "automatic", False):
                self.hero.weapon.fire(pygame.mouse.get_pos(), self.bullets)


    def draw(self, screen):
        screen.fill((72, 138, 72))
        #screen.blit(self.bg_img, (0,0))
        # Player, enemies, bullets
        #self.hero.draw_rect(screen)
        self.hero.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for bullet in self.bullets:
            bullet.draw_rect(screen)
        
        #screen.blit(self.text_hp, self.text_hp_rect)
        #screen.blit(self.text_stamina, self.text_stamina_rect)
        #screen.blit(self.text_exp, self.text_exp_rect)
        self.draw_stat_bars(screen)
        self.draw_ammo(screen)