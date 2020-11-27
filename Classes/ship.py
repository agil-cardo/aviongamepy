import pygame
import random
from pygame import mixer
from Utilities.functions import yaml_to_dict
from Classes.projectil import Projectil
from Classes.explosion import Explosion

SHIP_LOAD = yaml_to_dict("/items/ship.yaml")


class Ship(pygame.sprite.Sprite):
    """
        class ship => class mere pour player et monster
    """
    COOLDOWN = 25

    def __init__(self, game, sc_width, sc_height, ship_image="ship2"):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.ship_image = ship_image
        if self.ship_image in SHIP_LOAD:
            self.image_load = SHIP_LOAD[self.ship_image]
            self.image = pygame.image.load(self.image_load["image"])
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = 300
        self.image_width = self.image.get_width()
        self._pv = 100
        self.pv_max = 100
        self.attack = 30
        self.all_projectils = pygame.sprite.Group()
        self.all_explosions = pygame.sprite.Group()
        self.cooldown_counter = 0
        self.speed_x = 6
        self.speed_y = 6
        self.sc_width = sc_width
        self.sc_height = sc_height
        self.magasin = 0
        self.magasin_max = 20

        # Shield
        self.shield = 100
        self.shield_max = 100
        self.last_update = pygame.time.get_ticks()
        self.angle = 0
        self.shield_image_orig = pygame.image.load("assets/shield/shield.png")
        self.shield_image_orig = pygame.transform.scale(
            self.shield_image_orig, (150, 150))
        self.shield_image = self.shield_image_orig.copy()

    def _getpv(self):
        try:
            return self._pv
        except AttributeError:
            print("Les pv sont incorrects")

    def _setpv(self, nouvel_pv):
        if nouvel_pv < 0:
            self._pv = 0
        else:
            self._pv = nouvel_pv

    def _delpv(self):
        del self._pv

    # property(<getter>, <setter>, <deleter>, <helper)
    pv = property(_getpv, _setpv, _delpv, "Je suis les pv")

    def move_left(self):
        self.rect.x -= self.speed_x

    def draw_life_bar(self, surface, x, y):
        if self._pv < 0:
            self._pv = 0
        BAR_LENGTH = 200
        BAR_HEIGHT = 12
        fill = (self._pv / self.pv_max) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, (0, 255, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

        #  Call as : draw_shield_bar(screen, 5, 5, player.shield)

    def draw_munition_bar(self, surface, x, y):
        if self.magasin < 0:
            self.magasin = 0
        BAR_LENGTH = 200
        BAR_HEIGHT = 12
        fill = (self.magasin / self.magasin_max) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, (0, 0, 255), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

    def rotate_pv(self, square_y, color):  # private methode
        """
            square_y -- hauteur du rectangle
            color -- couleur
        """
        pv_image = pygame.Surface([square_y, 5])
        pv_image.fill(color)
        pv_image = pygame.transform.rotate(pv_image, 90)
        return pv_image

    def update_pv(self, surface, pos_x):
        """
            surface -- le background sur lequel on affiche
            pos_x -- la position horizontal

        """
        color = (11, 210, 46)  # vert
        back_color = (255, 0, 0)  # rouge

        # calcul de la bar de pv en fonction des pv_max et de la hauteur de l'avion
        calcul_bar_pv = self.pv/self.pv_max*self.image.get_height()

        # calcul pos_y
        pos_y = self.rect.y+self.image.get_height()-calcul_bar_pv

        # on injecte la barre de pv_max(grise) et la barre de pv(verte)
        surface.blit(self.rotate_pv(self.image.get_height(), back_color),
                     (pos_x, self.rect.y))
        surface.blit(self.rotate_pv(calcul_bar_pv, color),
                     (pos_x, pos_y))

    def move_projectil(self, vecteur, obj):
        self.cooldown()
        for projectil in self.all_projectils:
            projectil.move(vecteur)
            projectil.rotate()
            if not 0 < projectil.rect.x < self.sc_width:
                self.all_projectils.remove(projectil)
            elif projectil.rect.colliderect(obj.rect):
                explosionSound = mixer.Sound("assets/sounds/explosion.wav")
                explosionSound.set_volume(0.02)
                explosionSound.play()
                # si collision destruction le tire
                damage = self.attack + projectil.bullet_degat
                if obj.shield - damage > 0:
                    # perte des pv
                    obj.shield -= damage
                    damage = 0
                elif obj.shield - damage <= 0:
                    damage -= obj.shield
                    obj.shield = 0
                self.all_projectils.remove(projectil)
                # on instantie l'explosion avec le nom du projectil
                # et la position x,y de la où se fera l'explosion
                # (au centre du ship)
                explosion = Explosion(projectil._gettype_bullet(),
                                      obj.rect.centerx, obj.rect.centery)
                # on ajoute l'explosion
                self.all_explosions.add(explosion)
                # on affiche les explosions
                self.all_explosions.update()
                # si pv - bullet_degat >= 0
                if obj.pv - damage > 0:
                    # perte des pv
                    obj.pv -= damage
                else:
                    obj.pv = 0
                    obj.kill()

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def fire(self, type_personnage, name_projectil, sound=''):
        if self.cooldown_counter == 0:
            # créer une instance de projectil
            projectil = Projectil(
                self.game, (self.rect.x+self.image_width), type_personnage, name_projectil)
            # on positionne le projectil
            projectil.rect.y = self.rect.y + \
                (self.image.get_height()-projectil.image.get_height())/2
            if 0 >= self.magasin-projectil.quantite:
                self.magasin = 0
            else:
                self.magasin -= projectil.quantite
            # on ajoute dans le groupe de projectils
            self.all_projectils.add(projectil)
            if sound != '':
                sound.stop()
                sound.play()
            self.cooldown_counter = 1

    def munition_bar(self, surface, pos_x):
        """
            surface -- le background sur lequel on affiche
            pos_x -- la position horizontal

        """
        color = (0, 0, 255)  # blue
        back_color = (255, 0, 0)  # rouge

        # calcul de la bar de munition en fonction du magasin et de la hauteur de l'avion
        calcul_bar_pv = self.magasin/self.magasin_max*self.image.get_height()

        # calcul pos_y
        pos_y = self.rect.y+self.image.get_height()-calcul_bar_pv

        # on injecte la barre de pv_max(grise) et la barre de pv(verte)
        surface.blit(self.rotate_pv(self.image.get_height(), back_color),
                     (pos_x, self.rect.y))
        surface.blit(self.rotate_pv(calcul_bar_pv, color),
                     (pos_x, pos_y))

    def collid(self, elem_rect, my_list, qte, name):
        if self.rect.colliderect(elem_rect):
            elem_rect = self.image.get_rect()
            if len(my_list) != 0:
                my_list.pop()
                if name == "magasin":
                    if (self.magasin+qte) <= self.magasin_max:
                        self.magasin += qte
                    else:
                        self.magasin = self.magasin_max
                if name == "life":
                    if (self.pv+qte) <= self.pv_max:
                        self.pv += qte
                    else:
                        self.pv = self.pv_max
                if name == "armor":
                    if (self.shield+qte) <= self.shield_max:
                        self.shield += qte
                    else:
                        self.shield = self.shield_max

    def shielding(self, screen):
        if self.shield > 0:
            shield_rect = self.shield_image.get_rect()
            shield_rect.centerx = self.rect.centerx
            shield_rect.centery = self.rect.centery

            # Rotation
            self.angle += 5 % 360
            new_image = pygame.transform.rotate(
                self.shield_image_orig, self.angle)
            old_center = shield_rect.center
            self.shield_image = new_image
            shield_rect = self.shield_image.get_rect()
            shield_rect.center = old_center

            screen.blit(self.shield_image, shield_rect)


if __name__ == "__main__":
    from game import Game
    from input_box import InputBox
    box = InputBox(200, 100, 200, 32)
    game = Game(box, 600, 700)
    mon_ship_basique = Ship(game, 600, 700)
    print(mon_ship_basique.move_left())
