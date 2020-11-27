from Classes.ship import Ship, SHIP_LOAD
import random
import numpy
import pygame
from Classes.projectil import ITEMS_POWER


class Monster(Ship):
    """
        class monster => class fille de ship << on peut dire que monster est une sorte de ship >>
    """
    COOLDOWN = 100

    def __init__(self, game, sc_width, sc_height, ship_image="ship2"):
        Ship.__init__(self, game, sc_width, sc_height, ship_image="ship2")
        self.ship_image = ship_image
        if self.ship_image in SHIP_LOAD:
            self.image_load = SHIP_LOAD[self.ship_image]
            self.image = pygame.image.load(
                self.image_load["image"]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = sc_width + 70
        self.rect.y = random.randint(75, sc_height - 110)
        self.image_width = - 70
        self.attack = 0
        self.kamikaze = 100
        self.all_gains = []
        self.spawn_gain_rect = self.image.get_rect()
        self.spawn_gain_rect.x = 0
        self.spawn_gain_rect.y = 0
        self.qte = 0
        self.shield = 0
        self.shield_max = 0
        self.value = random.randint(10, 100)
        self.name = ''
        self.xp_monstre = random.randint(50, 80)

    def kamikaze_monster(self):
        if self.game.player.rect.colliderect(self.rect):
            self.rect.x = self.sc_width + 70
            self.rect.y = random.randint(75, self.sc_height - 110)
            self.pv = self.pv_max
            if (self.game.player.pv - self.kamikaze) > 0:
                self.game.player.pv -= self.kamikaze
            else:
                self.game.game_over()
        elif self.rect.x <= -40:
            if self.game.player.lv < 2:
                self.re_init()
            else:
                self.game.all_monsters.remove(self)
                self.game.event.spawn_super_monster("ship4")

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
        if self.game.player.lv < 2:
            self.re_init()
        else:
            self.game.all_monsters.remove(self)
            self.game.event.spawn_super_monster("ship4")
            # si la barre d'event est chargée à son maximun
        if self.game.event.is_full_loaded():
            # retire du jeu les monstres
            self.game.all_monsters.remove(self)
            self.is_boss = True
            self.game.player.pv = self.game.player.pv_max
            self.game.player.magasin = self.game.player.magasin_max
            # appel de la methode pour essayer de declencher l'event boss
            self.game.event.attempt_event()

    def re_init(self):
        self.rect.x = self.sc_width + 70
        self.rect.y = random.randint(75, self.sc_height - 110)
        self.pv = self.pv_max

    def spawn_gains(self):
        elem = []
        for item in ITEMS_POWER:
            elem.append(item)
        my_projectil = numpy.random.choice(elem, 1)[0]
        select = ITEMS_POWER[my_projectil]
        load = pygame.image.load(select["load"])
        spawn_gain = pygame.transform.scale(load, (60, 60))
        self.qte = random.randint(select["min"], select["max"])
        self.name = select["name"]
        self.spawn_gain_rect = spawn_gain.get_rect()
        self.spawn_gain_rect.x = self.rect.x
        self.spawn_gain_rect.y = self.rect.y
        self.all_gains.append(spawn_gain)


if __name__ == '__main__':
    # Attention, __mro__ est un attribut special de classe.
    # Il doit donc etre recupere depuis la classe
    print(Monster.__mro__)
    from game import Game
    from input_box import InputBox
    box = InputBox(200, 100, 200, 32)
    game = Game(box, 600, 700)
    monster_one = Monster(game, 600, 700)
    print(monster_one.ship_image)
    monster = Monster(game, 600, 700, "ship3")
    print(monster.ship_image)
    print(monster.image)
