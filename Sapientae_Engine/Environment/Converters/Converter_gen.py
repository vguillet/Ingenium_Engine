
################################################################################################################
"""
# TODO: Add reputation?
"""

# Built-in/Generic Imports

# Libs

# Own modules
from Sapientae_Engine.Tools.Inventory_tools import Inventory_tools
__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Converter:
    def __init__(self,
                 name: "Converter name",
                 input: "Resource type list",
                 output: "Resource type list"):

        self.ef_type = "Converter"

        self.name = name
        self.input = input
        self.output = output

        self.inventory = Inventory_tools().gen_market_inventory_dict()


