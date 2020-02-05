
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Ingenium_Engine.Bots.Tools.Traits_tools import Traits_tools
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class decision_tree:
    def __init__(self, environment):
        self.environment = environment

    def gen_decision(self):
        return