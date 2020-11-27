import pygame
from Classes.ship import Ship, SHIP_LOAD
from Utilities.functions import lecture, save_score
from Classes.projectil import ITEMS_SHIP


class Player(Ship):
    """
        class player => class fille de ship << on peut dire que player est une sorte de ship >>
    """

    def __init__(self, game, sc_width, sc_height, name, ship_image="ship3"):
        Ship.__init__(self, game, sc_width, sc_height, ship_image="ship2")
        self.name = name
        self.sc_height = sc_height
        self.sc_width = sc_width
        self.ship_image = ship_image
        if self.ship_image in SHIP_LOAD:
            self.image_load = SHIP_LOAD[self.ship_image]
            self.image = pygame.image.load(
                self.image_load["image"]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = (sc_height/2 - self.image.get_height()/2)
        self._pv = 200
        self.pv_max = 200
        self.image_width = self.image.get_width()
        self.speed_x = 7
        self.speed_y = 8
        self.score = 0
        self.last_score = 0
        self.point = 0
        self.point_MAX = 100
        self.attack = 20
        self.magasin_max = 50
        self.magasin = self.magasin_max
        self.total = 0
        self.lv = 1
        self.xp = 0
        self.xp_max = 1000 * self.lv

    def move_right(self):
        self.rect.x += self.speed_x

    def move_up(self):
        self.rect.y -= self.speed_y

    def move_down(self):
        self.rect.y += self.speed_y

    def add_point(self):
        if self.point+20 <= self.point_MAX:
            self.point += 20
        elif self.point > self.point_MAX:
            self.point = self.point_MAX

    def kill(self):
        self.game.game_over()

    def re_init(self):
        self.last_score = self.score
        self.score = 0
        self.pv = self.pv_max
        self.magasin = self.magasin_max
        self.rect.y = (self.sc_height / 2 - self.image.get_height() / 2)
        self.rect.x = 80
        self.point = 0

    def add_xp(self, xp_monstre):
        if self.xp+xp_monstre <= self.xp_max:
            self.xp += xp_monstre
        else:
            self.xp = self.xp + \
                xp_monstre-self.xp_max
            self.lv += 1

    def draw_xp_bar(self, surface, x, y):
        BAR_LENGTH = 200
        BAR_HEIGHT = 12
        fill = (self.xp / self.xp_max) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, (255, 250, 50), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

    def power_up(self, name):
        if self.lv > 1:
            if name == "laser":
                self.miniature()
                return "wind"
            elif name == "lightning":
                self.miniature()
                return "frozen"
            elif name == "plasma":
                self.miniature()
                return "slash"
            else:
                return name
        else:
            return name

    def miniature(self):
        self.game.tab[1]["image"] = pygame.transform.scale(
            pygame.image.load(ITEMS_SHIP["wind"]["load"]), (20, 20))
        self.game.tab[2]["image"] = pygame.transform.scale(
            pygame.image.load(ITEMS_SHIP["frozen"]["load"]), (20, 20))
        self.game.tab[3]["image"] = pygame.transform.scale(
            pygame.image.load(ITEMS_SHIP["slash"]["load"]), (20, 20))


if __name__ == '__main__':
    # Attention, __mro__ est un attribut special de classe.
    # Il doit donc etre recupere depuis la classe
    print(Player.__mro__)
    from game import Game
    from input_box import InputBox
    box = InputBox(200, 100, 200, 32)
    game = Game(box, 600, 700)
    player_one = Player(game, 600, 700)
    print(player_one.ship_image)
    player = Player(game, 600, 700, "ship3")
    print(player.ship_image)
    print(player.image)
