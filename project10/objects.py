from random import randrange
from pygame import *
import project10.config


class SquishSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.__loader__(image).convert()
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        shrink = -project10.config.margin * 2
        self.area = screen.get_rect().inflate(shrink, shrink)


class Weight(SquishSprite):
    def __init__(self, speed):
        SquishSprite.__init__(self, project10.config.Weight_image)
        self.speed = speed
        self.reset()
        self.landed = False

    def reset(self):
        x = randrange(self.area.left, self.area.right)
        self.rect.midbottom = x, 0

    def update(self):
        self.rect.top += self.speed
        self.landed = self.rect.top >= self.area.bottom


class Banana(SquishSprite):
    def __init__(self):
        SquishSprite.__init__(self, project10.config.Banana_image)
        self.rect.bottom = self.area.bottom
        self.pad_top = project10.config.Banana_pad_top
        self.pad_side = project10.config.Banana_pad_side

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect = self.rect.clamp(self.area)

    def touches(self, other):
        bounds = self.rect.inflate(-self.pad_side, -self.pad_top)
        bounds.bottom = self.rect.bottom
        return bounds.colliderect(other.rect)
