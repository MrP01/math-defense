import pygame, random
from pygame.locals import *


def int_pos(pos):
    return (int(pos[0]), int(pos[1]))


class Basis(object):
    def __init__(self, manager):
        self.manager = manager
        self.health = 1000.0
        self.maxspawn = 20
        self.spawn = 0

    def plus(self, max):
        a = random.randint(0, max)
        b = random.randint(0, max - a)
        zahl = random.choice([a + b, random.randint(1, max)])
        if zahl == a + b:
            richtig = True
        else:
            richtig = False
        return "%s + %s = %s" % (a, b, zahl), richtig

    def minus(self, max):
        a = random.randint(0, max)
        b = random.randint(0, a)
        zahl = random.choice([a - b, random.randint(1, max)])
        if zahl == a - b:
            richtig = True
        else:
            richtig = False
        return "%s - %s = %s" % (a, b, zahl), richtig

    def mal(self, max):
        a = random.randint(0, max / 10)
        b = random.randint(0, max / 10)
        zahl = random.choice([a * b, random.randint(1, max)])
        if zahl == a * b:
            richtig = True
        else:
            richtig = False
        return "%s * %s = %s" % (a, b, zahl), richtig

    def update(self):
        self.spawn -= self.manager.time_passed / 1000.0
        self.health += (self.manager.data.score / 2000.0) * (
            self.manager.time_passed / 1000.0
        )
        self.maxspawn = 20 - (self.manager.data.score / 10.0) ** 0.5
        if self.spawn <= 0:
            rechnung = random.choice(
                [self.plus(100), self.minus(100), self.minus(100), self.mal(100)]
            )
            while rechnung in self.manager.data.rechnungen:
                rechnung = random.choice(
                    [self.plus(100), self.minus(100), self.minus(100), self.mal(100)]
                )
            self.manager.data.rechnungen.append(rechnung)
            self.manager.data.schiffe.append(Raumschiff(self.manager, rechnung))
            self.spawn = self.maxspawn
        if self.health <= 0:
            self.manager.game_over()
        if self.health > 1000:
            self.health = 1000.0
        self.draw()

    def draw(self):
        pygame.draw.ellipse(
            self.manager.screen, (70, 40, 70), pygame.Rect((-160, 950), (2000, 500))
        )
        pygame.draw.rect(
            self.manager.screen, (0, 0, 0), pygame.Rect((339, 1019), (1002, 22)), 1
        )
        pygame.draw.rect(
            self.manager.screen,
            (255, 0, 0),
            pygame.Rect((340, 1020), ((self.health / 1000.0) * 1000, 20)),
        )
        pygame.draw.circle(self.manager.screen, (255, 255, 0), (20, 1030), 20)
        pygame.draw.circle(self.manager.screen, (255, 255, 0), (1660, 1030), 20)


class Tower(object):
    def __init__(self, manager, pos, range):
        self.manager = manager
        self.pos = pos
        self.range = range


class DefenseTower(Tower):
    def __init__(self, manager, pos):
        Tower.__init__(self, manager, pos, 200)
        self.strength = 10

    def update(self):
        self.draw()
        for schiff in self.manager.data.markiert:
            dx, dy = schiff.pos[0] - self.pos[0], schiff.pos[1] - self.pos[1]
            distance = (dx * dx + dy * dy) ** 0.5
            if distance <= self.range:
                pygame.draw.line(
                    self.manager.screen, (255, 0, 0), schiff.pos, self.pos, 2
                )
                schiff.health -= (
                    self.strength
                    * (self.manager.data.score / 2500.0)
                    * (self.manager.time_passed / 1000.0)
                )

    def draw(self):
        pygame.draw.circle(self.manager.screen, (255, 255, 0), int_pos(self.pos), 18)
        pygame.draw.circle(
            self.manager.screen, (0, 0, 0), int_pos(self.pos), self.range, 1
        )


class CalculatingTower(Tower):
    def __init__(self, manager, pos):
        Tower.__init__(self, manager, pos, 200)
        self.iq = 100

    def update(self):
        self.draw()
        for schiff in self.manager.data.schiffe:
            dx, dy = schiff.pos[0] - self.pos[0], schiff.pos[1] - self.pos[1]
            distance = (dx * dx + dy * dy) ** 0.5
            if distance <= self.range:
                pygame.draw.line(
                    self.manager.screen, (0, 255, 255), schiff.pos, self.pos, 2
                )

    def draw(self):
        pygame.draw.circle(self.manager.screen, (255, 255, 255), int_pos(self.pos), 18)
        pygame.draw.circle(
            self.manager.screen, (0, 0, 0), int_pos(self.pos), self.range, 1
        )


class Raumschiff(object):
    def __init__(self, manager, rechnung):
        self.manager = manager
        self.rechnung = rechnung[0]
        self.gut = rechnung[1]
        self.markiert = False
        self.health = 100
        self.pos = [random.randint(1, 1680), 0]
        self.speed = 15 + (self.manager.data.score / 150.0)

    def update(self):
        mp = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        if (
            buttons[0]
            and ((mp[0] - self.pos[0]) ** 2 + (mp[1] - self.pos[1]) ** 2) ** 0.5 <= 15
        ):
            pygame.draw.line(self.manager.screen, (0, 0, 255), (20, 1030), self.pos, 3)
            pygame.draw.line(
                self.manager.screen, (0, 0, 255), (1660, 1030), self.pos, 3
            )
            self.health -= (
                (10 + 5 * (self.manager.data.score / 2000.0))
                * (self.manager.time_passed / 1000.0)
                * 2
            )
        if (
            buttons[2]
            and ((mp[0] - self.pos[0]) ** 2 + (mp[1] - self.pos[1]) ** 2) ** 0.5 <= 15
        ):
            if self.markiert != True:
                self.manager.data.markiert.append(self)
                self.markiert = True
        if self.health <= 0:
            self.explode()
        dx, dy = 840 - self.pos[0], 1100 - self.pos[1]
        distance = (dx * dx + dy * dy) ** 0.5
        if distance >= 150:
            direction = float(dx) / distance, float(dy) / distance
            self.pos[0] += direction[0] * self.speed * self.manager.time_passed / 1000.0
            self.pos[1] += direction[1] * self.speed * self.manager.time_passed / 1000.0
            self.draw()
        else:
            if self.gut:
                self.manager.data.schiffe.remove(self)
                self.manager.data.basis.health += self.health
                self.manager.data.score += 100

            else:
                self.manager.data.basis.health -= self.health * 2
                self.manager.data.score -= 100
                self.explode()

    def explode(self):
        if self.markiert:
            self.manager.data.markiert.remove(self)
        if self.gut:
            pygame.draw.circle(self.manager.screen, (0, 255, 0), int_pos(self.pos), 50)
            self.manager.data.score -= 100
            self.manager.data.schiffe.remove(self)
        else:
            pygame.draw.circle(self.manager.screen, (255, 0, 0), int_pos(self.pos), 50)
            self.manager.data.score += 100
            self.manager.data.schiffe.remove(self)

    def draw(self):
        if self.markiert:
            pygame.draw.circle(self.manager.screen, (255, 0, 0), int_pos(self.pos), 15)
        else:
            pygame.draw.circle(self.manager.screen, (0, 0, 255), int_pos(self.pos), 15)
        rech_rect = self.manager.p.render(self.rechnung, True, (0, 0, 0)).get_rect()
        rech_rect.topleft = (0, 0)
        rech_rect.width += 20
        rech_rect.height += 10
        rech_surf = pygame.Surface((rech_rect.width, rech_rect.height))
        rech_surf.fill((110, 0, 180))
        rech_surf.set_colorkey((110, 0, 180))
        pygame.draw.ellipse(rech_surf, (255, 255, 255), rech_rect)
        rech_surf.blit(self.manager.p.render(self.rechnung, True, (0, 0, 0)), (10, 5))
        self.manager.screen.blit(rech_surf, (self.pos[0] - 100, self.pos[1] - 80))
