
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Sapientae_Engine.Bots.Tools.Traits_tools import Traits_tools
from Sapientae_Engine.Tools.Inventory_tools import Inventory_tools
from Sapientae_Engine.Tools.Interests_tools import Interests_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Bot_v1:
    def __init__(self,
                 pos: tuple,
                 traits: dict = None,
                 inventory: dict = None,
                 interests: dict = None):

        # --> Setup role of the bot in a simulation
        self.pos = pos

        # --> Setting up bot traits
        if traits is not None:
            self.traits = traits
        else:
            self.traits = Traits_tools().gen_traits_dict()

        # --> Setting up bot inventory
        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = Inventory_tools().gen_bot_inventory_dict()

        # --> Setting up bot interest
        if interests is not None:
            self.interests = interests
        else:
            self.interests = Interests_tools().gen_bot_interests_dict()

        # --> Setting up bot
    def gen_activity_decision(self):
        return
