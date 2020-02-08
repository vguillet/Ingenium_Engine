
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from Ingenium_Engine.Agents.Tools.Traits_tools import Traits_tools
from Ingenium_Engine.Tools.Inventory_tools import Inventory_tools
from Ingenium_Engine.Tools.Interests_tools import Interests_tools
from Ingenium_Engine.Tools.Characteristics_tools import Characteristics_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '31/01/2020'

################################################################################################################


class gen_Agent:
    def __init__(self,
                 name: "Bot name",
                 pos: tuple,
                 traits: dict = None,
                 inventory: dict = None,
                 interests: dict = None,
                 characteristics: dict = None):
        # ----- Setup reference properties
        self.name = name
        self.pos = pos

        # --> Setup traits/inventory/interests/characteristics dicts
        self.gen_dicts(traits, inventory, interests, characteristics)

    def step(self, environment: "Environment Object"):
        new_state = None
        reward = None
        done = False
        return new_state, reward, done

    # --> Setting up agent
    def gen_action_lst(self, environment: "Environment Object"):
        # ----- List options
        option_lst = []

        # --> Checking whether agent is at a POI
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
                if environment.converters_dict[converter].pos == self.pos:
                    option_lst.append(converter)

        # --> If at POI, listing available links
        for link in environment.graph.edges(current_POI):
            option_lst.append(link[1])
        print(option_lst)
        return option_lst

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
