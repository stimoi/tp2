"""
creer_images.py - Fabrique toutes les images du TP « Labyrinthe du Singe ».

Lance ce script UNE fois, dans le dossier de ton jeu :
    python creer_images.py
Il crée un dossier images/ avec tous les sprites (30 x 30 pixels)
et l'écran d'accueil (450 x 450 pixels).
"""

import os
import random
import pygame

TAILLE = 30          # taille d'un sprite en pixels
ZOOM = 2             # chaque "pixel" des dessins ci-dessous fait 2 x 2 pixels
COTE = 15 * TAILLE   # taille de la fenêtre du jeu

# Couleurs (R, V, B). "." = transparent
PALETTE = {
    "B": (59, 35, 20),     # contour brun foncé
    "b": (138, 90, 43),    # fourrure
    "f": (232, 195, 154),  # visage, mains
    "k": (26, 26, 26),     # yeux
    "w": (255, 255, 255),  # reflet des yeux
    "r": (192, 57, 43),    # bouche
    "K": (90, 61, 10),     # contour des bananes
    "Y": (244, 208, 63),   # banane
    "y": (201, 162, 39),   # ombre de banane
    "g": (62, 125, 50),    # tige
}

SINGE_BAS = [
    "....BBBBBBB....",
    "..BBbbbbbbbBB..",
    ".BbbbbbbbbbbbB.",
    "BBbbfffffffbbBB",
    "BfbfwkfffwkfbfB",
    "BfbffkfffkffbfB",
    ".BbfffffffffbB.",
    "..BbfffffffbB..",
    "...BffrrrffB...",
    "....BBfffBB....",
    "...BbbBBBbbB...",
    "..BbbbfffbbbB..",
    ".BbbBbfffbBbbB.",
    "..BBBbbbbbBBB..",
    "...BbbB.BbbB...",
]

SINGE_HAUT = [
    "....BBBBBBB....",
    "..BBbbbbbbbBB..",
    ".BbbbbbbbbbbbB.",
    "BBbbbbbbbbbbbBB",
    "BfbbbbbbbbbbbfB",
    "BfbbbbbbbbbbbfB",
    ".BbbbbbbbbbbbB.",
    "..BbbbbbbbbbB..",
    "...BbbbbbbbB...",
    "....BBbbbBB....",
    "...BbbBBBbbB...",
    "..BbbbbbbbbbB..",
    ".BbbBbbbbbBbbB.",
    "..BBBbbbbbBBB..",
    "...BbbB.BbbB...",
]

SINGE_DROITE = [
    ".....BBBBBB....",
    "...BBbbbbbbB...",
    "..BbbbbbbbbbB..",
    "..BbbbbbffffB..",
    ".BfBbbbfwkfffB.",
    ".BfBbbbffkffffB",
    "..BbbbbfffffffB",
    "..BbbbbffffrrB.",
    "...BbbbBffffB..",
    "....BBbbBBBB...",
    "...BbbbbbbbB...",
    "..BbbbbffbbbbB.",
    "B..BbbffbbbBffB",
    "BB.BbbbbbbbBBB.",
    ".BBBbbB.BbbB...",
]

# Le singe qui va à gauche, c'est le singe qui va à droite... dans un miroir !
SINGE_GAUCHE = [ligne[::-1] for ligne in SINGE_DROITE]

BANANES = [
    "...........gg..",
    "..........Kgg..",
    ".........KYYK..",
    "........KYYyK..",
    ".......KYYyKYK.",
    "......KYYyKYYK.",
    ".....KYYyKYYyK.",
    "...KKYYyKYYyKK.",
    ".KKYYYyKYYYyK..",
    "KYYYYyKYYYyK...",
    "KYYYyKYYYyK....",
    ".KyyKYYyyK.....",
    "..KKKyyKK......",
    ".....KK........",
    "...............",
]


def dessin_vers_image(dessin):
    """Transforme un dessin en texte (15 x 15 caractères) en image 30 x 30."""
    image = pygame.Surface((TAILLE, TAILLE), pygame.SRCALPHA)
    for num_ligne, ligne in enumerate(dessin):
        for num_colonne, lettre in enumerate(ligne):
            if lettre in PALETTE:
                rect = (num_colonne * ZOOM, num_ligne * ZOOM, ZOOM, ZOOM)
                image.fill(PALETTE[lettre], rect)
    return image


def creer_fond():
    """Sol de jungle : vert foncé avec des touffes d'herbe."""
    fond = pygame.Surface((COTE, COTE))
    fond.fill((46, 82, 52))
    hasard = random.Random(7)
    for _ in range(420):
        x = hasard.randrange(0, COTE, 2)
        y = hasard.randrange(0, COTE, 2)
        couleur = hasard.choice([(58, 100, 62), (38, 70, 44), (70, 112, 66)])
        fond.fill(couleur, (x, y, 2, 4))
        fond.fill(couleur, (x + 2, y - 2, 2, 4))
    return fond


def creer_mur():
    """Un bloc de pierres grises."""
    mur = pygame.Surface((TAILLE, TAILLE))
    mur.fill((60, 58, 66))                       # joints
    pierre = (128, 126, 138)
    clair = (160, 158, 170)
    rangees = [(0, [(0, 14), (16, 14)]),
               (10, [(-8, 14), (8, 14), (24, 14)]),
               (20, [(0, 14), (16, 14)])]
    for y, briques in rangees:
        for x, largeur in briques:
            mur.fill(pierre, (x + 1, y + 1, largeur - 1, 8))
            mur.fill(clair, (x + 1, y + 1, largeur - 1, 2))
    return mur


def creer_depart():
    """Case de départ : une dalle verte avec un petit drapeau."""
    depart = pygame.Surface((TAILLE, TAILLE))
    depart.fill((46, 139, 87))
    pygame.draw.rect(depart, (88, 194, 125), (2, 2, 26, 26), 2)
    pygame.draw.line(depart, (245, 245, 245), (10, 6), (10, 24), 2)
    pygame.draw.polygon(depart, (245, 245, 245), [(11, 6), (22, 10), (11, 14)])
    return depart


def creer_accueil(singe):
    """Écran d'accueil avec le titre et les touches."""
    accueil = creer_fond()
    voile = pygame.Surface((COTE, COTE), pygame.SRCALPHA)
    voile.fill((10, 25, 15, 150))
    accueil.blit(voile, (0, 0))

    gros_singe = pygame.transform.scale(singe, (150, 150))
    accueil.blit(gros_singe, ((COTE - 150) // 2, 110))

    pygame.font.init()
    titre = pygame.font.Font(None, 54)
    texte = pygame.font.Font(None, 30)
    jaune = (244, 208, 63)
    blanc = (240, 240, 240)

    def centrer(police, message, couleur, y):
        rendu = police.render(message, True, couleur)
        accueil.blit(rendu, ((COTE - rendu.get_width()) // 2, y))

    centrer(titre, "Labyrinthe", jaune, 30)
    centrer(titre, "du Singe", jaune, 70)
    centrer(texte, "F1 : niveau 1", blanc, 290)
    centrer(texte, "F2 : niveau 2", blanc, 320)
    centrer(texte, "Echap : quitter", blanc, 370)
    return accueil


def main():
    pygame.init()
    os.makedirs("images", exist_ok=True)

    singes = {
        "singe_bas": SINGE_BAS,
        "singe_haut": SINGE_HAUT,
        "singe_gauche": SINGE_GAUCHE,
        "singe_droite": SINGE_DROITE,
    }
    for nom, dessin in singes.items():
        pygame.image.save(dessin_vers_image(dessin), f"images/{nom}.png")

    pygame.image.save(dessin_vers_image(BANANES), "images/arrivee.png")
    pygame.image.save(creer_mur(), "images/mur.png")
    pygame.image.save(creer_depart(), "images/depart.png")
    pygame.image.save(creer_fond(), "images/fond.png")
    pygame.image.save(creer_accueil(dessin_vers_image(SINGE_BAS)), "images/accueil.png")

    print("C'est bon ! Les images sont dans le dossier images/")


if __name__ == "__main__":
    main()
