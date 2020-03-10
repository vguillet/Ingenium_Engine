
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
    def __init__(self, name, pos: tuple):
        # ----- Setup reference properties
        self.type = "Converter"
        self.name = name
        self.pos = pos
