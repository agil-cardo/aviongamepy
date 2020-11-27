import pygame
import random
from pygame import mixer
from Classes.player import Player
from Classes.monster import Monster
from Classes.event import Event
from Classes.projectil import ITEMS_SHIP
from Utilities.functions import save_score, lecture


PRINT_NUM_PROJECTIL = {
    1: {
        "image": pygame.transform.scale(pygame.image.load(ITEMS_SHIP["laser"]["load"]), (20, 20)),
        "title_display": {"num": "num 1", "bool": True, "color": (250, 250, 250)},
        "coord_img": (220, 10),
        "coord_disp": (218, 40)
    },
    2: {
        "image": pygame.transform.scale(pygame.image.load(ITEMS_SHIP["lightning"]["load"]), (20, 10)),
        "title_display": {"num": "num 2", "bool": True, "color": (250, 250, 250)},
        "coord_img": (260, 15),
        "coord_disp": (258, 40)
    },
    3: {
        "image": pygame.transform.scale(pygame.image.load(ITEMS_SHIP["plasma"]["load"]), (20, 10)),
        "title_display": {"num": "num 3", "bool": True, "color": (250, 250, 250)},
        "coord_img": (300, 15),
        "coord_disp": (298, 40)
    }
}


class Game:
    """
    docstring
    """

    def __init__(self, box, sc_width, sc_height):
        self.box = box
        self.name_projectil = "laser"
        self.name_player = ""
        self.player = Player(self, sc_width, sc_height,
                             self.name_player, "ship3")
        self.all_monsters = pygame.sprite.Group()
        self.event = Event(self, sc_width, sc_height)
        self.sc_width = sc_width
        self.sc_height = sc_height
        self.keybord = {}
        self.total_degat = 0
        self.is_running = False
        self.is_boss = False
        self.time = 0
        self.PLAYERS = {}
        self.total_game = 0
        self.last_ammo_update = pygame.time.get_ticks()
        self.tab = PRINT_NUM_PROJECTIL

    def start(self):
        self.is_running = True
        self.PLAYERS = lecture("/items/player.data")
        self.player.total = self.PLAYERS[self.name_player]["score_total"]
        self.player.lv = self.PLAYERS[self.name_player]["lv"]
        self.player.xp = self.PLAYERS[self.name_player]["xp"]
        self.player.xp_max = 1000*self.player.lv
        if self.player.lv != 1:
            self.player.pv_max = 200+(200*self.player.lv/100)
        self.name_projectil = self.player.power_up(self.name_projectil)
        if self.player.lv < 2:
            self.spawn_monster("ship2")
        else:
            self.event.spawn_super_monster("ship4")

    def game_over(self):
        save_player = self.PLAYERS[self.name_player]
        save_player["score_total"] += self.player.score
        save_player["pt_last_partie"] = self.player.score
        save_player["time_in_game"] += self.time
        save_player["lv"] = self.player.lv
        save_player["xp"] = self.player.xp
        save_score("/items/player.data", self.name_player,
                   save_player["score_total"], save_player["pt_last_partie"], save_player["time_in_game"], save_player["lv"], save_player["xp"])
        self.player.re_init()
        self.is_boss = False
        self.is_running = False
        self.all_monsters = pygame.sprite.Group()
        self.event.all_boss = pygame.sprite.Group()
        self.event.reset_percent()

    def spawn_monster(self, ship_image):
        monster = Monster(self, self.sc_width, self.sc_height,
                          ship_image)
        # on l'ajoute a notre groupe de monstre
        self.all_monsters.add(monster)

    def weapon_screen(self, screen):
        myfont = pygame.font.SysFont('roboto', 10)

        for elem in PRINT_NUM_PROJECTIL:
            item = PRINT_NUM_PROJECTIL[elem]
            title_disp = item["title_display"]
            screen.blit(
                item["image"], item["coord_img"])
            screen.blit(myfont.render(
                title_disp["num"], title_disp["bool"], title_disp["color"]), item["coord_disp"])

    def weapon_choice(self, screen, name):
        for key, item in enumerate(ITEMS_SHIP.keys()):
            if name == item and key < 3:
                pos = key*40
                pygame.draw.rect(screen, (100, 100, 100, 128),
                                 (215 + pos, 5, 30, 30))
                pygame.draw.rect(screen, (250, 250, 250),
                                 (215 + pos, 5, 30, 30), 2)
            self.weapon_screen(screen)

    def out_of_ammo(self, screen):
        if self.player.magasin <= 0:
            font = pygame.font.SysFont("roboto", 30)
            warn_ammo = font.render(
                "Out Of Ammo Wait ...", True, (250, 10, 10))
            screen.blit(warn_ammo, (self.sc_width/2 - warn_ammo.get_width() /
                                    2, self.sc_height/2 - warn_ammo.get_height() - 20))
            # Timer d'attente pour rechargement munition
            now = pygame.time.get_ticks()
            if now - self.last_ammo_update > 10000:
                self.last_ammo_update = now
                # Rechargement aléatoire
                mun = random.randint(5, 20)
                self.player.magasin = mun

    def start_game(self, screen):
        self.box.active = False
        # injecte l'image de l'player
        screen.blit(self.player.image,
                    (self.player.rect.x, self.player.rect.y))
        self.event.update_bar(screen)
        self.player.shielding(screen)

        # affichage des armes
        self.weapon_screen(screen)
        # affichage de l'arme utilisée
        self.weapon_choice(screen, self.name_projectil)

        if self.is_boss == False:
            for mob in self.all_monsters:
                mob.fire("ship", "laser")
                mob.move_projectil(-1, self.player)
                mob.update_pv(
                    screen, (mob.rect.x+mob.image.get_width()))
                mob.move_left()
                mob.kamikaze_monster()
                mob.all_projectils.draw(screen)
                mob.all_explosions.draw(screen)
                mob.all_explosions.update()
                for gain_load in mob.all_gains:
                    screen.blit(gain_load, mob.spawn_gain_rect)
                self.player.collid(mob.spawn_gain_rect,
                                   mob.all_gains, mob.qte, mob.name)
                self.player.move_projectil(1, mob)

        for boss in self.event.all_boss:
            boss.spawn(screen)

        # Affichage PV et Magasin
        self.player.draw_life_bar(screen, 10, 5)
        self.player.draw_munition_bar(screen, 10, 25)
        self.player.draw_xp_bar(screen, 10, 45)
        self.event.all_boss.draw(screen)

        # on verifie si les touches sont apuyées ou pas
        if self.keybord.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width()-40:
            self.player.move_right()
        elif self.keybord.get(pygame.K_LEFT) and self.player.rect.x > 25:
            self.player.move_left()
        if self.keybord.get(pygame.K_DOWN) and self.player.rect.y + self.player.rect.height < screen.get_height()-self.player.image.get_height():
            self.player.move_down()
        elif self.keybord.get(pygame.K_UP) and self.player.rect.y > 75:
            self.player.move_up()
        if self.keybord.get(pygame.K_SPACE):
            if self.player.magasin > 0:
                bulletSound = mixer.Sound("assets/sounds/laser.wav")
                bulletSound.set_volume(0.02)
                self.name_projectil = self.player.power_up(self.name_projectil)

                self.player.fire("ship", self.name_projectil, bulletSound)
            else:
                bulletSound = mixer.Sound("assets/sounds/alarm.wav")
                bulletSound.set_volume(0.02)
                bulletSound.stop()
                bulletSound.play()

        # Out of ammo:
        self.out_of_ammo(screen)

        if self.keybord.get(pygame.K_1):
            self.name_projectil = "laser"
            self.name_projectil = self.player.power_up(self.name_projectil)
        elif self.keybord.get(pygame.K_2):
            self.name_projectil = "lightning"
            self.name_projectil = self.player.power_up(self.name_projectil)
        elif self.keybord.get(pygame.K_3):
            self.name_projectil = "plasma"
            self.name_projectil = self.player.power_up(self.name_projectil)

        self.player.all_projectils.draw(screen)
        self.player.all_explosions.draw(screen)
        self.player.all_explosions.update()

        self.all_monsters.draw(screen)


if __name__ == '__main__':
    # Attention, __mro__ est un attribut special de classe.
    # Il doit donc etre recupere depuis la classe
    print(Game.__mro__)
    from game import Game
    from input_box import InputBox
    box = InputBox(200, 100, 200, 32)
    game = Game(box, 600, 700)
