import pygame
from Classes.boss import Boss
from Classes.supermonster import SuperMonster


class Event():
    """
    docstring
    """

    def __init__(self,  game, sc_width, sc_height):
        self.percent = 0
        self.game = game
        # groupe de boss
        self.all_boss = pygame.sprite.Group()
        self.is_event = False
        self.sc_width = sc_width
        self.sc_height = sc_height

    def add_precent(self):
        self.percent = int(self.game.player.point /
                           self.game.player.point_MAX*100)

    def is_full_loaded(self):
        return self.percent >= 100

    def reset_percent(self):
        self.percent = 0

    def stock(self):
        if self.game.player.lv < 2:
            boss = Boss(self.game, self.sc_width, self.sc_height, self)
        else:
            boss = Boss(self.game, self.sc_width,
                        self.sc_height, self, "boss2")
        self.all_boss.add(boss)

    def attempt_event(self):
        # la jauge d'event est totalement chargée
        if self.is_full_loaded():
            self.stock()
            self.is_event = True  # active l'evenement

    def update_bar(self, surface):
        # dessiner la barre de fond
        # on demande un surface, la couleur de la barre, les coord de la barre et une épaisseur
        pygame.draw.rect(surface, (0, 0, 0), [
            10,  # axe des x
            surface.get_height()-50,  # axe des y
            surface.get_width()-20,  # longueur de la barre
            20  # epaisseur
        ])
        # jauge d'apparition
        pygame.draw.rect(surface, (255, 0, 0), [
            10,  # axe des x
            surface.get_height()-50,  # axe des y
            (surface.get_width()-20)/self.game.player.point_MAX * \
            self.game.player.point,  # longueur de la barre
            20  # epaisseur
        ])

    def spawn_super_monster(self, ship_image):
        super_monster = SuperMonster(self.game, self.sc_width, self.sc_height,
                                     ship_image)
        # on l'ajoute a notre groupe de monstre
        self.game.all_monsters.add(super_monster)


if __name__ == '__main__':
    # Attention, __mro__ est un attribut special de classe.
    # Il doit donc etre recupere depuis la classe
    print(Event.__mro__)
    from game import Game
    from boss import Boss
    game = Game(1280, 760)
    event = Event(game, 1280, 760)
    print(event.stock())
