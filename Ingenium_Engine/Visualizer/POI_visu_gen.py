
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import pygame as pg

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_POI_visu(pg.sprite.Sprite):
    def __init__(self, POI: "POI object", margin):
        super().__init__()

        # ----- Setup reference properties
        self.POI = POI
        self.image = pg.image.load("Ingenium_Engine/Visualizer/Assets/POI.png").convert()
        self.image = pg.transform.scale(self.image, (60, 60))
        self.image.set_colorkey((0, 0, 0))  # Don't display black
        self.image.set_colorkey((255, 255, 255))  # Don't display black

        self.rect = self.image.get_rect()
        self.rect.center = (POI.pos[0] - margin, POI.pos[-1] - 2*margin)
