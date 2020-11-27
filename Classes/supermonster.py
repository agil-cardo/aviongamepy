from Classes.ship import SHIP_LOAD
from Classes.monster import Monster
import random
import numpy
import pygame
from Classes.projectil import ITEMS_POWER


class SuperMonster(Monster):
    """
        class SuperMonster => class fille de monster << on peut dire que SuperMonster est une sorte de monster >>
    """
    COOLDOWN = 200

    def __init__(self, game, sc_width, sc_height, ship_image="ship4"):
        Monster.__init__(self, game, sc_width, sc_height, ship_image="ship2")
        self.ship_image = ship_image
        if self.ship_image in SHIP_LOAD:
            self.image_load = SHIP_LOAD[self.ship_image]
            self.image = pygame.image.load(
                self.image_load["image"]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.sc_width + 70
        self.rect.y = random.randint(75, self.sc_height - 110)
        self.attack = 10
        self._pv = 150
        self.pv_max = 150
        self.xp_monstre = random.randint(90, 120)

    def kill(self):
        # ajouter xp au player
        self.game.player.add_xp(self.xp_monstre)
        # ajouter du % a la barre d'event
        self.game.player.score += self.value
        self.game.player.add_point()
        self.game.event.add_precent()
        # self.game.event.percent = self.game.player.point
        if len(self.all_gains) == 0:
            self.spawn_gains()
        else:
            self.all_gains.pop()
            self.spawn_gains()
        self.re_init()
        if self.game.event.is_full_loaded():
            # retire du jeu les monstres
            self.game.all_monsters.remove(self)
            self.is_boss = True
            self.game.player.pv = self.game.player.pv_max
            self.game.player.magasin = self.game.player.magasin_max
            # appel de la methode pour essayer de declencher l'event boss
            self.game.event.attempt_event()
