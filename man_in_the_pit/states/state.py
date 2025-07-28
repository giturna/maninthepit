# state.py

class BaseState:
    def __init__(self, manager):
        self.manager = manager
    def handle_events(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass