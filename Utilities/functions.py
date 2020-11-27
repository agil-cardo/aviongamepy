import yaml
import os
import pickle
from pathlib import Path


def my_path(path):
    myfile = os.getcwd()+path
    myfile = myfile.replace("\\", "/")
    directory = Path(myfile).parent
    if os.path.exists(directory):
        return myfile
    else:
        os.mkdir(directory)
        return myfile


def dict_to_yaml(path, write, dico):
    '''
        path -- chemin du fichier sur lequel on écrit exemple /mon_dossier/mon_fichier.yaml
        write -- mode d'écriture ('w' ecrase le fichier, 'a' ecrit à la fin du fichier)
        dico -- dictionnaire
    '''

    try:
        myfile = my_path(path)
        with open(myfile, write) as yaml_file:
            yaml.dump(dico, yaml_file)
    except OSError:
        print("chemin de fichier invalide")


def yaml_to_dict(path):
    '''
        path -- chemin du fichier sur lequel on écrit exemple /mon_dossier/mon_fichier.yaml
    '''
    try:
        myfile = my_path(path)
        with open(myfile) as yaml_file:
            return yaml.load(yaml_file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print("chemin de fichier invalide")


def lecture(path_file):
    file = my_path(path_file)
    with open(file, 'rb') as fichier:
        mon_depickler = pickle.Unpickler(fichier)
        return mon_depickler.load()


def ecriture(file, item):
    with open(file, 'wb') as fichier:
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(item)


def lines(file):
    with open(file) as fichier:
        # on lit le fichier ligne par ligne
        return fichier.readlines()


def controll(path_file, name):
    myfile = my_path(path_file)
    if os.path.exists(myfile):
        score_recupere = lecture(path_file)
    else:
        score_recupere = {name: {"score_total": 0,
                                 "pt_last_partie": 0, "time_in_game": 0, "lv": 1, "xp": 0}}
        ecriture(myfile, score_recupere)

    if not name in score_recupere.keys():
        score_recupere.update({name: {"score_total": 0,
                                      "pt_last_partie": 0, "time_in_game": 0, "lv": 1, "xp": 0}})
        print(f"Nouveau joueur ajouté {name}")
        ecriture(myfile, score_recupere)


def save_score(path_file, name, score_total, last_partie, time_game, lv, xp):
    myfile = my_path(path_file)
    if os.path.exists(myfile):
        score_recupere = lecture(path_file)
    else:
        score_recupere = {name: {"score_total": score_total,
                                 "pt_last_partie": last_partie, "time_in_game": time_game, "lv": lv, "xp": xp}}
        ecriture(myfile, score_recupere)

    if name in score_recupere.keys():
        score_recupere.update({name: {"score_total": score_total,
                                      "pt_last_partie": last_partie, "time_in_game": time_game, "lv": lv, "xp": xp}})
        print("Votre score actuel {} est de {} point(s)".format(
            name, score_recupere[name]["score_total"]))
        ecriture(myfile, score_recupere)


if __name__ == "__main__":
    type_bullets = {
        "laser": {
            "load": "assets/projectils/laser.png",
            "damage": 15,
            "name": "simple_laser",
            "magasin": 10,
            "speed": 5
        },
        "plasma": {
            "load": "assets/projectils/plasma.png",
            "damage": 20,
            "name": "simple_plasma",
            "magasin": 100,
            "speed": 5
        },
        "lithning": {
            "load": "assets/projectils/lithning.png",
            "damage": 25,
            "name": "blue phaser",
            "magasin": 100,
            "speed": 5
        },
        "boss": {
            "load": "assets/boss/solar.png",
            "damage": 100,
            "name": "Solar",
            "magasin": 100,
            "speed": 7
        }
    }
    # dict_to_yaml("/items/projectils.yaml", "w", type_bullets)
    # my_dict = yaml_to_dict("/items/projectils.yaml")
    # print(my_dict)
    controll("/items/player.data", "jean")
    PLAYER_SCORE = lecture("/items/player.data")
    print(PLAYER_SCORE)
