# entities/enemy.py
import pygame, random
from man_in_the_pit.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from man_in_the_pit.entities.character import Character
from man_in_the_pit.animation import Animation

class Enemy(Character):
    def __init__(self, pos_x, pos_y, width, height, color, hp, velocity, damage, exp):
        super().__init__(pos_x, pos_y, width, height, color, hp, velocity, exp)
        self.set_position()
        self.damage = damage

    def set_position(self):
        rand_field = random.randint(1, 4)
        if rand_field == 1:
            self.pos_x = random.randint(0, SCREEN_WIDTH - self.width)
            self.pos_y = random.randint(0, 100)
        elif rand_field == 2:
            self.pos_x = random.randint(0, SCREEN_WIDTH - self.width)
            self.pos_y = random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT - self.height)
        elif rand_field == 3:
            self.pos_x = random.randint(0, 100)
            self.pos_y = random.randint(100, SCREEN_HEIGHT - 100)
        elif rand_field == 4:
            self.pos_x = random.randint(SCREEN_WIDTH - 100, SCREEN_WIDTH - self.width)
            self.pos_y = random.randint(100, SCREEN_HEIGHT - self.height)

    def set_target(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y

    def get_rect(self):
        return pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def move_pattern(self, dt):
        pass
    

class Slime(Enemy):
    def __init__(
        self,
        width=32,
        height=32,
        hp=50,
        velocity=60,
        damage=20,
        exp=10,
        anim_path="man_in_the_pit/assets/enemies/slime/slime_sprite_6.png",
        frame_width=32,
        frame_height=32,
        frame_count=6,
        anim_speed=12.0
    ):
        super().__init__(
            pos_x=None,
            pos_y=None,
            width=width,
            height=height,
            color=(255,0,0,0,0),
            hp=hp,
            velocity=velocity,
            damage=damage,
            exp=exp
        )
        
        # Create Animation
        self.animation = Animation(
            sheet_path=anim_path,
            frame_width=frame_width,
            frame_height=frame_height,
            num_frames=frame_count,
            speed=anim_speed
        )

    def move_pattern(self, dt):
        dx = self.target_x - self.pos_x
        dy = self.target_y - self.pos_y
        distance = (dx**2 + dy**2)**0.5

        if distance > 0:
            self.pos_x += self.velocity * dt * (dx / distance)
            self.pos_y += self.velocity * dt * (dy / distance)

    def update(self, dt):
        self.animation.update(dt)

    def draw(self, surface):
        self.animation.draw(surface, self.pos_x, self.pos_y)


class Slime_Boss(Slime):
    def __init__(self):
        super().__init__(
            width=64,
            height=64,
            hp=300,
            velocity=80,
            damage=50,
            exp=70,
            anim_path="man_in_the_pit/assets/enemies/slime/slimeBoss_sprite_6.png",
            frame_width=64,
            frame_height=64,
            frame_count=6,
            anim_speed=12.0
        )