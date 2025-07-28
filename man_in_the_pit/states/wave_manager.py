# wave_manager.py

class WaveManager:
    def __init__(self,
                 wave_number = 1,
                 wave_duration = 10.0):
        self.wave_number = wave_number
        self.wave_duration = wave_duration
        self.wave_timer = 0.0
        self.spawn_interval = 1000  # milisecond

        self.once_actions = [
            {
                "wave": 2,
                "time": 0.0,
                "event": "spawn_boss_Slime",
                "done": False
            },
            {
                "wave": 3,
                "time": 0.0,
                "event": "spawn_boss_Slime",
                "done": False
            }
        ]
    
    def update(self, dt):
        self.wave_timer += dt
        print(dt)

        if self.wave_timer > self.wave_duration:
            self.wave_duration += 10
            self.wave_number += 1

    def spawn_controll(self):
        # Enemy spawn controll
        if self.wave_number == 1:
            self.spawn_interval = 1000
        elif self.wave_number == 2:
            self.spawn_interval = 800
        else:
            self.spawn_interval = 500
        return self.spawn_interval