
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Settings.SETTINGS import SETTINGS
from Ingenium_Engine.Agents.Tools.Traits_tools import Traits_tools
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools
from Ingenium_Engine.Tools.Interests_tools import Interests_tools
from Ingenium_Engine.Tools.Characteristics_tools import Characteristics_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Agent:
    def __init__(self,
                 name: "Bot name",
                 pos: tuple,
                 traits: dict = None,
                 inventory: dict = None,
                 interests: dict = None,
                 characteristics: dict = None):

        # ----- Setup settings
        self.settings = SETTINGS()
        self.settings.agent_settings.gen_agent_settings()

        # ----- Setup reference properties
        self.name = name
        self.pos = pos
        self.velocity = self.settings.agent_settings.agent_speed

        self.starting_pos = pos
        self.starting_traits = traits
        self.starting_inventory = inventory
        self.starting_interests = interests
        self.starting_characteristics = characteristics

        # --> Setup traits/inventory/interests/characteristics dicts
        self.gen_dicts(self.starting_traits,
                       self.starting_inventory,
                       self.starting_interests,
                       self.starting_characteristics)

    @property
    def used_cargo(self):
        used_cargo = 0
        for resource in self.inventory["Resources"].keys():
            used_cargo += self.inventory["Resources"][resource]
        return used_cargo

    def gen_dicts(self,
                  traits: dict,
                  inventory: dict,
                  interests: dict,
                  characteristics: dict):
        # --> Setting up traits
        if traits is not None:
            self.traits = traits
        else:
            self.traits = Traits_tools().gen_traits_dict()

        # --> Setting up inventory
        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = Inventory_tools().gen_agent_inventory_dict()

        # --> Setting up interest
        if interests is not None:
            self.interests = interests
        else:
            self.interests = Interests_tools().gen_agent_interests_dict()

        # --> Setting up characteristics
        if characteristics is not None:
            self.characteristics = characteristics
        else:
            self.characteristics = Characteristics_tools().gen_agent_characteristics_dict()

    def __str__(self):
        return self.name + " (Bot)"

    def __repr__(self):
        self.__repr__()
