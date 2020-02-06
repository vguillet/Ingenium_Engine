
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Ingenium_Engine.Bots.Tools.Traits_tools import Traits_tools
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools
from Ingenium_Engine.Tools.Interests_tools import Interests_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class Bot_v1:
    def __init__(self,
                 name,
                 pos: tuple,
                 traits: dict = None,
                 inventory: dict = None,
                 interests: dict = None):

        # ----- Setup reference properties
        self.name = name

        self.pos = pos
        self.velocity = None

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

    def __str__(self):
        return self.name + " (Bot)"

    def __repr__(self):
        self.__repr__()

    # --> Setting up bot
    def gen_activity_decision(self, environment: "Environment Object"):
        # ----- List options
        option_lst = []

        # --> Checking whether bot is at a POI
        current_POI = None
        for POI in environment.POI_dict.keys():
            if environment.POI_dict[POI].pos == self.pos:
                current_POI = POI
                break

        # --> If at POI, listing available ef
        if current_POI is not None:
            for source in environment.sources_dict.keys():
                if environment.sources_dict[source].pos == self.pos:
                    option_lst.append(source)
            for converter in environment.converters_dict.keys():
                if environment.converters_dict[converter] == self.pos:
                    option_lst.append(converter)

        print(option_lst)
        return
