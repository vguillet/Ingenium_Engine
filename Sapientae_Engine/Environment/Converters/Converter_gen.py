
################################################################################################################
"""
# TODO: Add reputation?
"""

# Built-in/Generic Imports

# Libs

# Own modules
from Sapientae_Engine.Tools.Inventory_tools import Inventory_tools
from Sapientae_Engine.Tools.Interests_tools import Interests_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Converter:
    def __init__(self, name: "Converter name", item_types: list):
        self.ef_type = "Converter"
        self.name = name

        # --> Setting up converter inventory
        self.inventory = Inventory_tools().gen_market_inventory_dict(item_types)

        # --> Setting up converter interests
        self.interests = Interests_tools().gen_market_interests_dict(item_types)
