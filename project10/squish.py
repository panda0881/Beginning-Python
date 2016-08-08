import os
import sys
from pygame import *
import project10.config
import project10.objects


class State:
    def handle(self, event):
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()

    def firstDisplay(self, screen):
        screen.fill(project10.config.Background_color)
        pygame.display.flip()

    def display(self, screen):
        pass


class Level(State):
    def __init__(self, number=1):
        self.number = number
        self.remaining = project10.config.Weights_per_level
        speed = project10.config.Drop_speed
        speed += (self.number - 1) * project10.config.Speed_increase
        self.weight = project10.objects.Weight(speed)
        self.banana = project10.objects.Banana()
        both = self.weight, self.banana
        self.sprites = pygame.sprite.RenderUpdates(both)

    def update(self, game):
        self.sprites.update()
        if self.banana.touches(self.weight):
            game.nextState = GameOver()
        elif self.weight.landed:
            self.weight.reset()
            self.remaining -= 1
            if self.remaining == 0:
                game.nextState = LevelCleared(self.number)

    def display(self, screen):
        self.sprites.draw(screen)
        screen.fill(project10.config.Background_color)
        updates = self.sprites.draw(screen)
        pygame.display.update(updates)


class Paused(State):
    nextState = None
    finished = 0
    image = None
    text = ''

    def handle(self, event):
        State.handle(self, event)
        if event.type in [MOUSEBUTTONDOWN, KEYDOWN]:
            self.finished = 1

    def update(self, game):
        if self.finished:
            game.nextState = self.nextState

    def firstDisplay(self, screen):
        screen.fill(project10.config.Background_color)
        font = pygame.font.Font(None, project10.config.font_size)
        lines = self.text.strip().splitlines()
        height = len(lines) * font.get_linesize()
        center, top = screen.get_rect().center
        top -= height // 2
        if self.image:
            image = pygame.image.__loader__(self.image).convert()
            r = image.get_rect()
            top += r.height // 2
            r.midbottom = center, top - 20
            screen.blit(image, r)
        antialias = 1
        black = 0, 0, 0
        for line in lines:
            text = font.render(line.strip(), antialias, black)
            r = text.get_rect()
            r.midtop = center, top
            screen.blit(text, r)
            top += font.get_linesize()
        pygame.display.flip()


class Info(Paused):
    nextState = Level
    text = '''
    In this game you are a banana,
    trying to survive a course in
    self-defense against fruit, where the
    participants will "defend" themselves
    against you with a weight.'''


class StartUp(Paused):
    nextState = Info
    image = project10.config.Splash_image
    text = '''
    Welcome to Squish.
    the game of Fruit Self-defense'''


class LevelCleared(Paused):
    def __init__(self, number):
        self.number = number
        self.text = '''Level %i cleared
        Click to start next level''' % self.number

    def nextState(self):
        return Level(self.number + 1)


class GameOver(Paused):
    nextState = Level
    text = '''
    Game Over
    Click to Restart, Esc to Quit'''


class Game:
    def __init__(self, *args):
        path = os.path.abspath(args[0])
        dir = os.path.split(path)[0]
        os.chdir(dir)
        self.state = None
        self.nextState = StartUp()

    def run(self):
        pygame.init()
        flag = 0
        if project10.config.full_screen:
            flag = FULLSCREEN
        screen_size = project10.config.Screen_size
        screen = pygame.display.set_mode(screen_size, flag)
        pygame.display.set_caption('Fruit Self Defense')
        pygame.mouse.set_visible(False)
        while True:
            if self.state != self.nextState:
                self.state = self.nextState
                self.state.firstDisplay(screen)
            for event in pygame.event.get():
                self.state.handle(event)
            self.state.update(self)
            self.state.display(screen)


if __name__ == '__main__':
    game = Game(*sys.argv)
    game.run()
