
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Sapientae_Engine.Bots.Bot_properties.Traits_tools import traits_tools
from Sapientae_Engine.Bots.Bot_properties.Inventory_tools import inventory_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class decision_tree:
    def __init__(self, environment):
        self.environment = environment

    def gen_decision(self):
        return