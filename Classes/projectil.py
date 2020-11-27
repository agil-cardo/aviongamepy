import pygame
import random
from Utilities.functions import yaml_to_dict


TYPE_BULLETS = yaml_to_dict("/items/projectils.yaml")
ITEMS_BOSS = TYPE_BULLETS["boss"]
ITEMS_SHIP = TYPE_BULLETS["ship"]
ITEMS_POWER = TYPE_BULLETS["power"]


class Projectil(pygame.sprite.Sprite):
    """
    docstring
    """

    def __init__(self, game, pos_x, type_personnage="ship", type_bullet="laser", rand=False):
        super().__init__()
        self.type_personnage = type_personnage
        self._type_bullet = type_bullet
        if self._type_bullet in TYPE_BULLETS[self.type_personnage]:
            self.arme = TYPE_BULLETS[self.type_personnage][self._type_bullet]
            self.name = self.arme["name"]
            self.quantite = self.arme["magasin"]
            self.bullet_speed = self.arme["speed"]
            self.bullet_degat = self.arme["damage"]
            self.image = pygame.image.load(self.arme["load"]).convert_alpha()
            self.rect = self.image.get_rect()
            self.rotation = self.arme["rotation"]
        self.game = game
        self.rect.x = pos_x
        self.origin_image = self.image
        self.angle = 0

    def _gettype_bullet(self):
        try:
            return self._type_bullet
        except AttributeError:
            print("Le type_bullet n'existe pas")

    def _settype_bullet(self, value):
        self._type_bullet = value

    type_bullet = property(_gettype_bullet, _settype_bullet)

    def remove(self):
        self.game.ship.all_projectils.remove(self)

    def move(self, vecteur):
        if vecteur == 1 or vecteur == -1:
            self.rect.x += (self.bullet_speed*vecteur)
        else:
            raise print("erreure de valeure")

    def rotate(self):
        if self.rotation:
            # fait tourner le projectil quand on le lance
            self.angle += 12
            self.image = pygame.transform.rotozoom(
                self.origin_image, self.angle, 1)
            self.rect = self.image.get_rect(center=self.rect.center)


if __name__ == "__main__":
    from game import Game
    import numpy
    from input_box import InputBox
    box = InputBox(200, 100, 200, 32)
    game = Game(box, 600, 700)
    pro = Projectil(game, 20)
    # print(ITEMS_BOSS)
    # print(ITEMS_SHIP)

    elem = []
    for item in ITEMS_SHIP:
        elem.append(item)

    my_pro = numpy.random.choice(elem, 1)[0]
    print(ITEMS_SHIP[my_pro])
