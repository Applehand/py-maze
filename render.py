from abc import ABC, abstractmethod

class Renderer(ABC):
    """Abstract Renderer interface."""

    @abstractmethod
    def draw_rect(self, x, y, width, height, color):
        pass

    @abstractmethod
    def draw_line(self, start, end, color, thickness):
        pass

    @abstractmethod
    def clear_screen(self, color):
        pass

    @abstractmethod
    def update_screen(self):
        pass


class PygameRenderer(Renderer):
    """Pygame implementation of the Abstract Renderer interface."""

    def __init__(self, pygame, screen):
        self.pygame = pygame
        self.screen = screen

    def draw_rect(self, x, y, width, height, color):
        self.pygame.draw.rect(self.screen, color, (x, y, width, height))

    def draw_line(self, start, end, color, thickness):
        self.pygame.draw.line(self.screen, color, start, end, thickness)

    def clear_screen(self, color):
        self.screen.fill(color)

    def update_screen(self):
        self.pygame.display.flip()
