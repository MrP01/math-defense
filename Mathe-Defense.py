import pygame
from pygame.locals import *

pygame.init()
from Menu import *
from Objects import *


class Data(object):
    pass


class Manager(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((1680, 1050))
        self.clock = pygame.time.Clock()
        self.h1 = pygame.font.SysFont("Comic Sans MS", 150)
        self.h5 = pygame.font.SysFont("Comic Sans MS", 48)
        self.p = pygame.font.SysFont("Comic Sans MS", 32)
        self.time_passed = 0

    def play(self):
        self.reset_data()
        self.data.basis = Basis(self)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        self.pause()
            self.time_passed = self.clock.tick(24)
            self.screen.fill((110, 0, 180))
            self.screen.blit(
                self.h5.render("Score: %s" % (self.data.score), True, (255, 255, 255)),
                (0, 0),
            )
            for schiff in self.data.schiffe:
                schiff.update()
            for tower in self.data.towers:
                tower.update()
            if self.data.score >= 10000 and self.data.won == False:
                self.data.won = True
                self.win()
            self.data.basis.update()
            pygame.display.flip()

    def pause(self):
        chooser = MenuChoice(self, ["Weiter", "Hauptmenu"], (800, 400))
        header = Text("Pause", self.h1, (800, 200), (255, 255, 255))
        _break = False
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        chooser.before()
                    if event.key == K_DOWN:
                        chooser.next()
                if (event.type == KEYDOWN and event.key == K_RETURN) or (
                    event.type == MOUSEBUTTONDOWN and event.button == 1
                ):
                    if chooser.choosen == "Weiter":
                        _break = True
                    if chooser.choosen == "Hauptmenu":
                        self.menu()
            if _break:
                break
            self.time_passed = self.clock.tick(24)
            self.screen.fill((110, 0, 180))
            header.blit(self.screen)
            chooser.update()
            pygame.display.flip()

    def game_over(self):
        chooser = MenuChoice(
            self,
            ["Sore: %s" % str(self.data.score), "Noch mal", "Hauptmenu"],
            (800, 400),
        )
        header = Text("Game over", self.h1, (800, 200), (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        chooser.before()
                    if event.key == K_DOWN:
                        chooser.next()
                if (event.type == KEYDOWN and event.key == K_RETURN) or (
                    event.type == MOUSEBUTTONDOWN and event.button == 1
                ):
                    if chooser.choosen == "Nochmal":
                        self.play()
                    if chooser.choosen == "Hauptmenu":
                        self.menu()
            self.clock.tick(24)
            self.screen.fill((110, 0, 180))
            header.blit(self.screen)
            chooser.update()
            pygame.display.flip()

    def win(self):
        chooser = MenuChoice(
            self,
            ["Sore: %s" % str(self.data.score), "Weiterspielen", "Hauptmenu"],
            (800, 400),
        )
        header = Text("Gewonnen!", self.h1, (800, 200), (255, 255, 255))
        _break = False
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        chooser.before()
                    if event.key == K_DOWN:
                        chooser.next()
                if (event.type == KEYDOWN and event.key == K_RETURN) or (
                    event.type == MOUSEBUTTONDOWN and event.button == 1
                ):
                    if chooser.choosen == "Weiterspielen":
                        _break = True
                    if chooser.choosen == "Hauptmenu":
                        self.menu()
            if _break:
                break
            self.time_passed = self.clock.tick(24)
            self.screen.fill((110, 0, 180))
            header.blit(self.screen)
            chooser.update()
            pygame.display.flip()

    def menu(self):
        chooser = MenuChoice(self, ["Spielen", "Regeln", "Beenden"], (800, 400))
        header = Text("Mathe-Defense", self.h1, (800, 200), (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        chooser.before()
                    if event.key == K_DOWN:
                        chooser.next()
                if (event.type == KEYDOWN and event.key == K_RETURN) or (
                    event.type == MOUSEBUTTONDOWN and event.button == 1
                ):
                    if chooser.choosen == "Spielen":
                        self.play()
                    if chooser.choosen == "Beenden":
                        exit()
            self.clock.tick(24)
            self.screen.fill((110, 0, 180))
            header.blit(self.screen)
            chooser.update()
            pygame.display.flip()

    def reset_data(self):
        self.data = Data()
        self.data.schiffe = []
        self.data.rechnungen = []
        self.data.markiert = []
        self.data.towers = [
            DefenseTower(self, (440, 500)),
            DefenseTower(self, (740, 500)),
            DefenseTower(self, (1040, 500)),
            DefenseTower(self, (1340, 500)),
        ]
        self.data.won = False
        self.data.score = 0


m = Manager()
m.menu()
