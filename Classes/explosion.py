import pygame
from Utilities.functions import yaml_to_dict

TYPE_EXPLOSIONS = yaml_to_dict("/items/explosions.yaml")


class Explosion(pygame.sprite.Sprite):
    def __init__(self, shot_name, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        # charge l'image via la liste TYPE_EXPLOSIONS et
        # on la stock dans la variable tileset
        self.explosions = TYPE_EXPLOSIONS[shot_name]
        tileset = pygame.image.load(
            self.explosions["load"]).convert_alpha()
        # on récupère la largeur(w) et la hauteur(h) de l'image
        img_w, img_h = tileset.get_size()
        # on divise la largeur de l'image par le nombre de sprite contenu en largeur
        img_w = img_w//self.explosions["width"]
        # on divise la hauteur de l'image par le nombre de sprite contenu en hauteur
        img_h = img_h//self.explosions["height"]
        # on initialise les compteurs X,Y à 0
        X, Y = 0, 0
        # on boucle pour decouper l'image,
        # et ainsi recuper un sprite apres l'autre
        for y in range(self.explosions["height"]):
            for i in range(self.explosions["width"]):
                # on stock le sprite dans une liste
                self.images.append(tileset.subsurface(X, Y, img_w, img_h))
                # on incremente X
                X += img_w
            # on incrémente Y
            Y += img_h
            # on réinitialise X
            X = 0
        self.index = 0
        self.image = self.images[self.index]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.counter = 0

    def update(self):
        explosion_speed = 1
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
