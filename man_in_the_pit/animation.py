# animation.py
import glob, os, pygame

class Animation:
    def __init__(self, sheet_path, frame_width, frame_height, num_frames, speed=0.1):
        """
        sheet_path   : Path to sprite sheet file (example: "assets/slime_sprites.png")
        frame_width  : Pixel width of each frame
        frame_height : Pixel heigth of each frame
        num_frames   : How many frames?
        speed        : animation speed
        """
        # Sprite sheet upload
        self.sheet = pygame.image.load(sheet_path).convert_alpha()

        # Cuts the frames and makes a list
        self.frames = self._slice_frames(
            self.sheet, frame_width, frame_height, num_frames
        )

        # Animation controll variables
        self.current_index = 0
        self.speed = speed
        self.timer = 0.0
        self.num_frames = num_frames

    

    @classmethod
    def from_dir(cls, dir_path, speed, pattern="*.png"):
        files  = sorted(glob.glob(os.path.join(dir_path, pattern)))
        frames = [pygame.image.load(f).convert_alpha() for f in files]

        self = cls.__new__(cls)
        self.frames        = frames
        self.num_frames    = len(frames)
        self.current_index = 0
        self.speed         = speed      # for 8 fps   speed = 8/60
        self.timer         = 0.0
        return self



    def _slice_frames(self, sheet, w, h, count):
        # Takes the sprite sheet as horizontally arranged squares and cuts each square into a subsurface.
        frames = []
        for i in range(count):
            rect = pygame.Rect(i * w, 0, w, h)
            frame_surface = sheet.subsurface(rect)
            frames.append(frame_surface)
        return frames

    def update(self, delta_time):
        # Update animation. delta_time, the time (in seconds) from the previous frame to this frame.
        self.timer += self.speed * delta_time
        if self.timer >= 1.0:
            self.current_index = (self.current_index + 1) % self.num_frames
            self.timer = 0.0

    def get_current_frame(self):
        # Returns the current frame Surface.
        return self.frames[self.current_index]

    def draw(self, surface, x, y):
        # Draw the active frame on the screen at (x, y) location.
        current_frame_surf = self.get_current_frame()
        surface.blit(current_frame_surf, (x, y))
