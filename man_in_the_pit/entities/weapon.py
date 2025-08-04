# weapon.py
import math, random, pygame
from man_in_the_pit.entities.bullet import Bullet
from man_in_the_pit.animation import Animation
from man_in_the_pit.settings import FPS 

class Weapon:
    def __init__(self, owner, fire_rate,
                 magazine_size,
                 reload_time = 1.5):
        self.owner = owner
        self.cooldown = 0.0
        self.fire_delay = 1.0 / fire_rate        # örn. 2 fps = 0.5 sn

        # --- Ammo / reload ---
        self.mag_size     = magazine_size   # magazine size
        self.ammo         = magazine_size   # current bullet number in magazine
        self.reload_time  = reload_time
        self.is_reloading = False
        self.reload_timer = 0.0

    def update(self, dt):
        # Cooldown
        if self.cooldown > 0:
            self.cooldown -= dt

        # reload counter
        if self.is_reloading:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.ammo = self.mag_size
                self.is_reloading = False

    def can_fire(self):
        return (not self.is_reloading) and self.cooldown <= 0 and self.ammo > 0

    # reload mannualy or auto
    def reload(self):
        if self.is_reloading or self.ammo == self.mag_size:
            return
        self.is_reloading = True
        self.reload_timer = self.reload_time



class Pistol(Weapon):
    def __init__(self, owner,
                 bullet_speed  = 1200,
                 bullet_damage = 25,
                 fire_rate     = 3.0):
        super().__init__(owner, fire_rate,
                         magazine_size = 14)   # magazine size

        self.bullet_speed  = bullet_speed
        self.bullet_damage = bullet_damage

        # -------------------------------  RELOAD ANIM.
        IMG_DIR      = "man_in_the_pit/assets"
        fps  = 16
        anim_speed   = fps / self.reload_time   # ≈ 10.7 f/s  → done in 1.5s
        self.reload_anim = Animation.from_dir(f"{IMG_DIR}/pistol_reload", anim_speed, pattern="*.png")

        


    def fire(self, target_pos, bullet_list):
        if not self.can_fire():
            if self.ammo == 0:           # auto reload
                self.reload()
            return

        # mermi üret
        ox, oy = self.owner.get_muzzle_pos()
        mx, my = target_pos
        b = Bullet(ox, oy, 4, 4, (255,255,255),
                   self.bullet_speed, self.bullet_damage)
        b.set_direction(mx, my)
        bullet_list.append(b)

        self.ammo     -= 1               # reduce the number of bullets fired from the magazine
        self.cooldown  = self.fire_delay
        if self.ammo == 0:               # empty magazine → reload auto
            self.reload()


    def reload(self):
        if self.is_reloading or self.ammo == self.mag_size:
            return
        self.is_reloading = True
        self.reload_timer = self.reload_time

        # start the animation from the beginning
        self.reload_anim.current_index = 0
        self.reload_anim.timer = 0.0


    def update(self, dt):
        super().update(dt)              # current counters
        if self.is_reloading:
            self.reload_anim.update(dt)





class Shotgun(Weapon):
    def __init__(self, owner,
                 pellets = 8, spread_deg = 20,
                 bullet_speed = 1200,
                 bullet_damage = 18,
                 fire_rate = 1.5):
        self.shell_reload_time = 0.40
        super().__init__(owner, fire_rate,
                         magazine_size = 6,
                         reload_time=self.shell_reload_time)      # mag. size

        self.pellets       = pellets
        self.spread_rad    = math.radians(spread_deg)
        self.bullet_speed  = bullet_speed
        self.bullet_damage = bullet_damage

        # -------------------------------  RELOAD ANIM.
        IMG_DIR      = "man_in_the_pit/assets"
        anim_speed  = 4 / self.shell_reload_time
        self.reload_anim = Animation.from_dir(f"{IMG_DIR}/shotgun_reload", anim_speed, pattern="*.png")

    def fire(self, target_pos, bullet_list):
        if not self.can_fire():
            if self.ammo == 0:
                self.reload()
            return
        self.is_reloading = False

        ox, oy = self.owner.get_muzzle_pos()
        mx, my = target_pos
        base_angle = math.atan2(my - oy, mx - ox)

        for _ in range(self.pellets):
            offset = random.uniform(-self.spread_rad/2, self.spread_rad/2)
            ang    = base_angle + offset
            dx, dy = math.cos(ang), math.sin(ang)

            b = Bullet(ox, oy, 3, 3, (255,255,0),
                       self.bullet_speed, self.bullet_damage)
            b.direction_x, b.direction_y = dx, dy
            bullet_list.append(b)

        self.ammo    -= 1
        self.cooldown = self.fire_delay
        if self.ammo == 0:
            self.reload()

    # ------------------------------------------
    def reload(self):
        if self.is_reloading or self.ammo == self.mag_size:
            return
        self.is_reloading = True
        self.reload_timer = self.shell_reload_time
        self.reload_anim.current_index = 0
        self.reload_anim.timer = 0.0

    # ------------------------------------------
    def update(self, dt):
        # cd counter
        if self.cooldown > 0:
            self.cooldown -= dt

        if self.is_reloading:
            self.reload_timer -= dt
            self.reload_anim.update(dt)

            if self.reload_timer <= 0:
                self.ammo += 1
                if self.ammo < self.mag_size:
                    self.reload_timer += self.shell_reload_time
                    self.reload_anim.current_index = 0
                    self.reload_anim.timer = 0.0
                else:
                    self.is_reloading = False


class SubmachineGun(Weapon):
    def __init__(self, owner,
                 bullet_speed  = 1200,   # px/s
                 bullet_damage = 20,
                 fire_rate     = 15.0):
        super().__init__(owner, fire_rate,
                         magazine_size=30)
        self.bullet_speed  = bullet_speed
        self.bullet_damage = bullet_damage
        self.automatic     = True        #  ←  keep the button pressed to fire full auto

    # rest is same as pistol
    def fire(self, target_pos, bullet_list):
        if not self.can_fire():
            if self.ammo == 0:
                self.reload()
            return

        ox, oy = self.owner.get_muzzle_pos()
        mx, my = target_pos

        b = Bullet(ox, oy, 4, 4, (255, 255, 255),  # pistol bullet (for now)
                   self.bullet_speed, self.bullet_damage)
        b.set_direction(mx, my)
        bullet_list.append(b)

        self.ammo    -= 1
        self.cooldown = self.fire_delay
        if self.ammo == 0:
            self.reload()
