# entities/player.py
import pygame, math
from man_in_the_pit.entities.character import Character
from man_in_the_pit.animation import Animation
from man_in_the_pit.entities.weapon import Weapon, Pistol, Shotgun, SubmachineGun
from man_in_the_pit.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(Character):
    def __init__(self,
                 pos_x = (SCREEN_WIDTH/2)-25,
                 pos_y = (SCREEN_HEIGHT/2)-15,
                 width = 35,
                 height = 60,
                 color = (0,255,255),
                 hp = 100,
                 velocity = 150,
                 exp = 0
                ):
        super().__init__(pos_x, pos_y, width, height, color, hp, velocity, exp)

        # Health variables
        self.max_hp = hp          # to fill the bar

        # XP variables
        self.exp_to_level = 100         # “next level” Threshold (constant for now)

        # Movement variables
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # Stamina variables
        self.stamina = 0.0
        self.stamina_regen_rate = 15#0.10
        self.max_stamina = 100.0

        # Sprint Variables
        self.base_speed        = velocity        # 150 px/s
        self.sprint_mul        = 1.7             # running velocity × 1.7
        self.sprint_cost_rate  = 25              # stamina / second
        self.sprint_anim_mul   = 1.6             # animasyon speed × 1.6
        self.is_sprinting      = False

        # Dash variables
        self.is_dashing = False
        self.dash_timer = 0.0
        self.dash_duration = 0.5
        self.dash_cooldown = 0.0
        self.max_cooldown = 1.0
        self.dash_speed = 400
        self.dash_stamina_cost = 40

        ROLL_FRAMES   = 6
        ROLL_DIR  = "man_in_the_pit/assets/dodge_roll"
        roll_fps      = ROLL_FRAMES / self.dash_duration    # anim. duration = dash duration
        self.roll_anim = Animation.from_dir(ROLL_DIR, roll_fps)

        # Last known movement direction
        self.dash_dir_x = 0
        self.dash_dir_y = 0

        # Weapon
        self.weapon = None
        self._aim_deg = 0.0
            

        # Create Animation
        RUN_DIR = "man_in_the_pit/assets/hero"
        fps = 12
        self.run_anim = {
            "right": Animation.from_dir(f"{RUN_DIR}/run_right",          fps),
            "left" : Animation.from_dir(f"{RUN_DIR}/run_right",          fps, pattern="*.png"),
            "front": Animation.from_dir(f"{RUN_DIR}/run_frontandback",   fps, pattern="*.png"),
            "back" : Animation.from_dir(f"{RUN_DIR}/run_frontandback",   fps, pattern="*.png"),
        }
        for anim in self.run_anim.values():
            anim.base_speed = anim.speed

        IDLE_DIR = "man_in_the_pit/assets/idle"     # animation frames
        self.idle_anim  = Animation.from_dir(IDLE_DIR, fps)

        self.current_anim = self.idle_anim
        self.current_run = self.run_anim["front"]


    def _apply_weapon_skin(self):
        if isinstance(self.weapon, Pistol):
            img_path = "man_in_the_pit/assets/weapons/pistol_arm.png"
            self.arm_pivot_r  = (30, 27)
            self.muzzle_ofs_r = (58, 24)

        elif isinstance(self.weapon, Shotgun):
            img_path = "man_in_the_pit/assets/weapons/shotgun_arm.png"
            self.arm_pivot_r  = (30, 27)
            self.muzzle_ofs_r = (60, 27)

        else:  # SubmachineGun
            img_path = "man_in_the_pit/assets/weapons/submachinegun_arm.png"
            self.arm_pivot_r  = (30, 27)
            self.muzzle_ofs_r = (58, 24)

        # load sprite and mirror it
        self.arm_img_right = pygame.image.load(img_path).convert_alpha()
        self.arm_img_left  = pygame.transform.flip(self.arm_img_right, True, False)

        w = self.arm_img_right.get_width()
        self.arm_pivot_l   = (w - self.arm_pivot_r[0],  self.arm_pivot_r[1])
        self.muzzle_ofs_l  = (w - self.muzzle_ofs_r[0], self.muzzle_ofs_r[1])


    def move_up(self, dt):
        self.pos_y -= self.velocity * dt
    def move_down(self, dt):
        self.pos_y += self.velocity * dt
    def move_left(self, dt):
        self.pos_x -= self.velocity * dt
    def move_right(self, dt):
        self.pos_x += self.velocity * dt

    def start_dash(self):
        self.is_dashing = True
        self.dash_timer = self.dash_duration

        # rewind animation
        self.roll_anim.current_index = 0
        self.roll_anim.timer = 0.0

        dx = 0
        dy = 0
        if self.moving_up: dy -= 1
        if self.moving_down: dy += 1
        if self.moving_left: dx -= 1
        if self.moving_right: dx += 1

        length = (dx**2+dy**2)**0.5
        if length > 0:
            dx = dx / length
            dy = dy / length
        else:
            dx = 1 # Default (when not moving) dash direction is right
        self.dash_dir_x = dx
        self.dash_dir_y = dy

    def set_velocity(self):
        pass

    def get_heal(self, healer):
        self.hp += healer.health

    def get_exp(self, exp_source):
        self.exp += exp_source.exp


    def get_muzzle_pos(self, aim_deg=None):
        if aim_deg is None:
            aim_deg = self._aim_deg
        
        aim_deg = (aim_deg + 360) % 360
        left_side = 90 < aim_deg < 270

        if left_side:
            pivot  = self.arm_pivot_l
            muzzle = self.muzzle_ofs_l
            base = 180
        else:
            pivot  = self.arm_pivot_r
            muzzle = self.muzzle_ofs_r
            base = 0

        # vektor (pivot → barrel)
        vx, vy = muzzle[0] - pivot[0], muzzle[1] - pivot[1]

        # rotate
        rel_deg = aim_deg - base             # Remains within ±90°
        rad = math.radians(rel_deg)
        rx = vx * math.cos(rad) - vy * math.sin(rad)
        ry = vx * math.sin(rad) + vy * math.cos(rad)

        return self.pos_x + pivot[0] + rx, self.pos_y + pivot[1] + ry

    

    
    def update(self, dt):
        # self.animation.update(dt)

        mx, my = pygame.mouse.get_pos()
        aim_deg = math.degrees(math.atan2(my - self.pos_y, mx - self.pos_x))
        aim_deg = (aim_deg + 360) % 360
        self._aim_deg = aim_deg

        
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.pos_y > 0:
            self.move_up(dt)
            self.moving_up = True
        else:
            self.moving_up = False

        if keys[pygame.K_s] and self.pos_y + self.height < SCREEN_HEIGHT:
            self.move_down(dt)
            self.moving_down = True
        else:
            self.moving_down = False

        if keys[pygame.K_a] and self.pos_x > 0:
            self.move_left(dt)
            self.moving_left = True
        else:
            self.moving_left = False

        if keys[pygame.K_d] and self.pos_x + self.width < SCREEN_WIDTH:
            self.move_right(dt)
            self.moving_right = True
        else:
            self.moving_right = False

        # 1) Sprint if SHIFT is pressed
        sprinting = (
            pygame.key.get_pressed()[pygame.K_LSHIFT]
            and (self.moving_up or self.moving_down or self.moving_left or self.moving_right)
            and self.stamina > 0
            and not self.is_dashing
        )
        self.is_sprinting = sprinting
        if sprinting:
            self.velocity = self.base_speed * self.sprint_mul
            self.stamina -= self.sprint_cost_rate * dt
            # animasyon speed
            for anim in self.run_anim.values():
                anim.speed = anim.base_speed * self.sprint_anim_mul
        else:
            self.velocity = self.base_speed
            for anim in self.run_anim.values():
                anim.speed = anim.base_speed


        # 2) Which button is pressed? → dx,dy
        dx = (1 if self.moving_right else 0) - (1 if self.moving_left else 0)
        dy = (1 if self.moving_down  else 0) - (1 if self.moving_up   else 0)
        if dx or dy:                                     # if it moves
            key = "right" if abs(dx) > abs(dy) and dx>0 else \
                "left"  if abs(dx) > abs(dy)          else \
                "front" if dy>0 else "back"
            self.current_anim = self.run_anim[key]
        else:                                            # No movement → idle
            self.current_anim = self.idle_anim

        # Advance the selected animation
        self.current_anim.update(dt)
        
        if keys[pygame.K_SPACE] and self.dash_cooldown <= 0 and not self.is_dashing:
            if self.stamina >= self.dash_stamina_cost:
                self.start_dash()
                self.stamina -= self.dash_stamina_cost

        # Reload weapon
        if keys[pygame.K_r]:
            self.weapon.reload()

        # Stamina regeneration
        if not self.is_sprinting and not pygame.key.get_pressed()[pygame.K_LSHIFT] and self.stamina < self.max_stamina:
            self.stamina += self.stamina_regen_rate * dt
        self.stamina = max(0, min(self.stamina, self.max_stamina))



        # Dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
            if self.dash_cooldown < 0:
                self.dash_cooldown = 0

        if self.is_dashing:
            self.dash_timer -= dt
            self.roll_anim.update(dt)

            self.pos_x += self.dash_dir_x * self.dash_speed * dt
            self.pos_y += self.dash_dir_y * self.dash_speed * dt

            if self.dash_timer <= 0:
                self.is_dashing = False
                self.dash_cooldown = 2.0

        # Weapon update
        self.weapon.update(dt)

    def draw(self, screen):
        x, y = self.pos_x, self.pos_y

        # ------------------------------------------------ dash animation
        if self.is_dashing:
            frame = self.roll_anim.get_current_frame()
            if self.dash_dir_x < 0:
                frame = pygame.transform.flip(frame, True, False)
            screen.blit(frame, (x, y))
            return

        # ------------------------------------------------ body (run / idle)
        base_frame = self.current_anim.get_current_frame()
        if self.current_anim is self.run_anim["left"]:
            base_frame = pygame.transform.flip(base_frame, True, False)

        # ------------------------------------------------ reload animation
        if self.weapon.is_reloading and hasattr(self.weapon, "reload_anim"):
            screen.blit(base_frame, (x, y))            # let the body remain
            frame = self.weapon.reload_anim.get_current_frame()
            offset_x = self.arm_pivot_r[0] - frame.get_width()  // 2
            offset_y = self.arm_pivot_r[1] - frame.get_height() // 2
            screen.blit(frame, (x + offset_x, y + offset_y))
            return

        # ------------------------------------------------ aim angle
        mx, my     = pygame.mouse.get_pos()
        aim_deg    = math.degrees(math.atan2(my - y, mx - x))
        aim_deg = (aim_deg + 360) % 360
        self._aim_deg = aim_deg

        left_side  = 90 < aim_deg < 270          # Which semicircle are we in?

        # ------------------------------------------------ aktive sprite + references
        if left_side:                            # Left side
            arm_img       = self.arm_img_left
            self.arm_pivot = self.arm_pivot_l
            self.muzzle_ofs = self.muzzle_ofs_l
            rel_angle     = aim_deg - 180        # the left sprite's 0° is 180°
        else:                                    # Right side
            arm_img       = self.arm_img_right
            self.arm_pivot = self.arm_pivot_r
            self.muzzle_ofs = self.muzzle_ofs_r
            rel_angle     = aim_deg              # the right sprite's 0° is 0°

        # ------------------------------------------------ rotate the arm
        rotated = pygame.transform.rotate(arm_img, -rel_angle)
        rect    = rotated.get_rect(
                    center=(x + self.arm_pivot[0], y + self.arm_pivot[1]))

        # ------------------------------------------------ drawing order (depth)
        if left_side:
            screen.blit(rotated, rect.topleft)   # the weapon is behind the char. body
            screen.blit(base_frame, (x, y))
        else:
            screen.blit(base_frame, (x, y))
            screen.blit(rotated, rect.topleft)

