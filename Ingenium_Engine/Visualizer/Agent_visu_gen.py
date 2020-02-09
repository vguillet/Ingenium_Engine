
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


class gen_agent_visu(pg.sprite.Sprite):
    def __init__(self, agent: "Agent object", margin):
        super().__init__()

        # ----- Setup reference properties
        self.agent = agent
        self.image = pg.image.load("Ingenium_Engine/Visualizer/Assets/agent.png").convert()
        self.image = pg.transform.scale(self.image, (20, 20))
        self.image.set_colorkey((0, 0, 0))  # Don't display black

        self.rect = self.image.get_rect()
        self.rect.center = (agent.pos[0] - margin, agent.pos[-1] - 2*margin)

    # def update(self, new_pos):
    #     self.rect.x = new_pos[0]
    #     self.rect.y = new_pos[-1]
    def update(self):
        import random
        self.rect.x += random.randint(-10, 10)
        self.rect.y += random.randint(-10, 10)

        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.x > 800:
            self.rect.x = 800

        if self.rect.y > 800:
            self.rect.y = 800
