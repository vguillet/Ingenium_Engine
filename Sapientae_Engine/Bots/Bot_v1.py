
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Sapientae_Engine.Bots.Bot_properties.Traits_tools import traits_tools
from Sapientae_Engine.Bots.Bot_properties.Inventory_tools import inventory_tools
from Sapientae_Engine.Bots.Bot_logic.Decision_tree import decision_tree

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Bot_v1:
    def __init__(self, job, traits_dict=None, inventory_dict=None):

        # --> Setup role of the bot in a simulation
        self.job = job

        # --> Setting up bot traits
        if traits_dict is not None:
            self.traits_dict = traits_dict
        else:
            self.traits_dict = traits_tools().gen_traits_dict()

        # --> Setting up bot inventories
        if inventory_dict is not None:
            self.inventory_dict = inventory_dict
        else:
            self.account_dict = inventory_tools().gen_inventory_dict()
        self.inventory_dict = inventory_dict

    def gen_activity_decision(self):
        return
