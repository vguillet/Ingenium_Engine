
################################################################################################################
"""
# TODO: Add reputation?
"""

# Built-in/Generic Imports

# Libs

# Own modules
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools
from Ingenium_Engine.Tools.Interests_tools import Interests_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Converter:
    def __init__(self, name, pos: tuple, item_types: list):
        # --> Setup reference properties
        self.type = "Converter"
        self.name = name
        self.pos = pos

        # --> Setup converter inventory
        self.inventory = Inventory_tools().gen_market_inventory_dict(item_types)

        # --> Setup converter interests
        self.interests = Interests_tools().gen_market_interests_dict(item_types)
