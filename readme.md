# Space Ship Battle !


## Documentation :

### Main :
- Jeu principal. Boucle while.
- Gestion des modes Jeu et Menu

## Libraries installation:
To install the libraries required for the game, run the following pip command
```bash
pip install -r requirements.txt
```

## Game :
- Class de jeu
- function GameOver()
- function Play()


## Avion :
- Deplacement avion
- Barre de vie avion
- Gestion des points/score
- Barre de vie Boss


## Monster :
- Deplacement mob
- Barre de vie mob
- Collision avion
- spawn weapon monster
- fire monster


## Weapon :
- type bullets {}
```json
type_bullets = {
        "laser": {
            "color": pygame.image.load("assets/laser.png"),
            "damage": 3,
            "name": "simple_laser",
            "magasin": 10,
            "speed": 5
        },
        "plasma": {
            "color": pygame.image.load("assets/plasma.png"),
            "damage": 5,
            "name": "simple_plasma",
            "magasin": 100,
            "speed": 5
        },
        "lithning": {
            "color": pygame.image.load("assets/lithning.png"),
            "damage": 2,
            "name": "blue phaser",
            "magasin": 100,
            "speed": 5
        },
        "boss": {
            "color": pygame.image.load("assets/boss/solar.png"),
            "damage": 100,
            "name": "Solar",
            "magasin": 100,
            "speed": 7
        }
    }
```
- bullet type
- deplacement balle (move_weapon)


## Assets :
- Sounds
- background
- home
- projectils
- ship
- Anim

#### La TODLIST D'Ale ! 👨‍ :
- clear le code:
    - enlevez les doublon. (ok)
    - refacto code (ok)

- Le foutu boss:
    - le rendre mortel (tangible) -> bug fixed
    - event boss (ok)

- Plusieur monstres:
    - gérer l'apparition des mob (prochaine étape)
    - gestion des points (prochaine étape)

- gestion des tirs et des explosions (ok)
- selection des armes (ok)
- gestion des degats (ok)
- gestion des munitions (ok)


> -------------------------------------------------------------------------------------------------------------
> -------------------------------------------------------------------------------------------------------------
> -------------------------------------------------------------------------------------------------------------


# GIT:

## Bonne pratique s

### Merge

(si je fait beaucoup de changement je rebase sur la branch que je veut merge --> git rebase)


1 - git checkout -b nom_de_la_branche
​
2 - On travail sur la branche ...
​
3 - git status
​
4 - git add .
​
5 - git commit -m "mon commit ..."
​
6 - git push origin nom_de_la_branche
​
7 - git checkout master
​
8 - git merge nom_de_la_branche
​
9 - On va sur gitlab -> Repository -> Branches , on click sur le bouton merge request de la branche

10 - je valide la merge request sur gitlab en cliquant sur merge

11 - Je récupére l'état du dépot --> git fetch --prune 

12 - Je récupére la version du dépot --> git pull 

### Changer ou créer une branche
Creation -> git checkout -b NewBranch

Si une branche existe en distant
git fetch --prune
git chekout nom_de_la_branche
