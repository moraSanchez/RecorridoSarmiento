from abc import ABC, abstractmethod

class BaseScene(ABC):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
    
    @abstractmethod
    def handle_events(self, event):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass
    
    def change_state(self, new_state):
        self.game.current_state = new_state