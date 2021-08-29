import pygame, random
from pygame.locals import *


class Text(object):
    def __init__(self, text, font, pos, color=(0, 0, 0)):
        self.pos = pos
        self.textstring = text
        self.font = font
        self.color = color
        self.update_texts()

    def update_texts(self):
        self.textsurface = self.font.render(self.textstring, True, self.color)
        self.textrect = self.textsurface.get_rect()
        self.textrect.center = self.pos

    def change_text(self, new_text):
        self.textstring = new_text
        self.update_texts()

    def change_font(self, font):
        self.font = font
        self.update_texts()

    def change_color(self, color):
        self.color = color
        self.update_texts()

    def blit(self, surface):
        surface.blit(self.textsurface, self.textrect)


class MenuChoice(object):
    def __init__(self, manager, choices, pos):
        self.pos = pos
        self.manager = manager
        self.choices = choices
        self.choosen = choices[0]
        self.font = pygame.font.SysFont("Comic Sans MS", 96)
        self.choosen_font = pygame.font.SysFont("Comic Sans MS", 128)

    def next(self):
        if self.choices.index(self.choosen) + 1 >= len(self.choices):
            self.choosen = self.choices[0]
        else:
            self.choosen = self.choices[self.choices.index(self.choosen) + 1]

    def before(self):
        if self.choices.index(self.choosen) - 1 < 0:
            self.choosen = self.choices[-1]
        else:
            self.choosen = self.choices[self.choices.index(self.choosen) - 1]

    def update(self):
        mp = pygame.mouse.get_pos()
        for choice in self.choices:
            if choice == self.choosen:
                text = self.choosen_font.render(choice, True, (255, 255, 255))
            else:
                text = self.font.render(choice, True, (200, 200, 200))
            textrect = text.get_rect()
            textrect.topleft = (
                self.pos[0] - (textrect.width / 2.0),
                self.pos[1] + self.choices.index(choice) * 170,
            )
            if textrect.collidepoint(mp):
                self.choosen = choice
            self.manager.screen.blit(text, textrect.topleft)
