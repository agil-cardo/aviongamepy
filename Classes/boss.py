import pygame
import random
from Classes.monster import Monster
from Classes.explosion import Explosion
from Classes.projectil import Projectil
from Classes.ship import SHIP_LOAD


class Boss(Monster):
    """
    docstring
    """
    COOLDOWN = 40

    def __init__(self, game, sc_width, sc_height, boss_event, ship_image="boss1"):
        Monster.__init__(self, game, sc_width, sc_height, ship_image="ship2")
        self.boss_event = boss_event
        self.game = game
        self.ship_image = ship_image
        if self.ship_image in SHIP_LOAD:
            self.boss_load = SHIP_LOAD[self.ship_image]
            self.image = pygame.image.load(self.boss_load["image"])
            self._pv = self.boss_load["pv"]
            self.pv_max = self.boss_load["pv_max"]
            self.xp_monstre = self.boss_load["xp_monstre"]
        self.speed_x = 0
        self.image = pygame.transform.scale(self.image, (300, 500))
        self.rect = self.image.get_rect()
        self.rect.x = self.sc_width - self.image.get_width()-20
        self.rect.y = (self.sc_height-self.image.get_height())/2
        self.value = 500

    def kill(self):
        self.game.player.add_xp(self.xp_monstre)
        self.game.player.score += self.value
        self.remove()
        self.game.is_boss = False
        self.game.player.magasin = self.game.player.magasin_max
        if self.game.player.lv < 2:
            self.game.spawn_monster("ship2")
        else:
            self.game.event.spawn_super_monster("ship4")

    def remove(self):
        self.boss_event.all_boss.remove(self)
        # verifier si le nombres de boss est de 0
        if len(self.boss_event.all_boss) == 0:
            # l'event est fini on remet la barre à 0
            self.game.player.point = 0
            self.boss_event.reset_percent()

    def fire(self, type_personnage, name_projectil):
        if self.cooldown_counter == 0:
            # créer une instance de projectil
            projectil = Projectil(self.game, self.rect.x +
                                  self.image_width, type_personnage, name_projectil)
            # on positionne le projectil
            projectil.rect.y = random.randint(
                self.rect.y-projectil.image.get_height(), self.sc_height-self.rect.y)
            if 0 >= self.magasin-projectil.quantite:
                self.magasin = 0
            else:
                self.magasin -= projectil.quantite
            # on ajoute dans le groupe de projectils
            self.all_projectils.add(projectil)
            self.cooldown_counter = 1

    def spawn(self, screen):
        if self.game.player.lv < 2:
            self.fire("boss", "solar")
        else:
            self.fire("boss", "ice")
        self.move_projectil(-1, self.game.player)
        self.update_pv(screen, (self.rect.x+self.image.get_width()))
        self.game.player.move_projectil(1, self)
        self.kamikaze_monster()
        self.all_projectils.draw(screen)
        self.all_explosions.draw(screen)
        self.all_explosions.update()

    def kamikaze_monster(self):
        if self.game.player.rect.colliderect(self.rect):
            self.game.game_over()


if __name__ == '__main__':
    # Attention, __mro__ est un attribut special de classe.
    # Il doit donc etre recupere depuis la classe
    print(Boss.__mro__)
    from game import Game
    game = Game(600, 700)
    boss_one = Boss(game, 600, 700, game.event)
    print(boss_one.ship_image)
    boss = Boss(game, 600, 700, game.event, "ship3")
    print(boss.ship_image)
    print(boss.image)
